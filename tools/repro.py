"""Help for checking old issues by hand: reruns the Python snippets of the issues behind close/recurrence proposals on the
installed numpy and records what happened, so a person can decide whether each old bug is still there. Not part of the
pipeline. The snippets come from the internet and are run only as isolated subprocesses (python -I, minimal environment,
timeout, cwd in repro/).

usage: python tools/repro.py data/<owner>__<name>/repo.db [--only N [N ...]] [--rerun] [--timeout 60]
writes repro/<number>.py: the issue link, the snippet (created once, then hand-edited), and below it as comments, rewritten
on every run of changed code: auto (exception types compared), expected, reported, got on this numpy, the description.
Also repro/sheet.jsonl and repro/review.md next to the db. The verdict and note columns of sheet.jsonl are kept across reruns.
"""
import argparse, collections, hashlib, json, os, re, sqlite3, subprocess, sys, time
from pathlib import Path

PYTHON = Path(os.path.expanduser("~/.dev/venv/bin/python"))
EXPECTED = "2.5.5"
KINDS = ("close_fixed_similar", "close_fixed_linked", "check_recurrence", "close_duplicate_likely", "close_duplicate_marked")
PAIRED = ("close_duplicate_likely", "close_duplicate_marked")  # the original issue is run too, to compare the two outputs
FENCE = re.compile(r"^[ \t]*```([^\n`]*)\n(.*?)^[ \t]*```[ \t]*$", re.S | re.M)
PY_TAGS = {"python", "python3", "py", "ipython"}
DOCTEST = re.compile(r"^\s*(?:>>>|\.\.\.|\.\.\.:|In \[\d+\]:)(?: (.*))?$")
BROKEN = re.compile(r"AttributeError: module 'numpy' has no attribute|ModuleNotFoundError|ImportError|NameError|SyntaxError")


def doctest_code(text):
    return "\n".join(m.group(1) or "" for m in map(DOCTEST.match, text.splitlines()) if m)


def has_doctest(text):
    return any(DOCTEST.match(line) for line in text.splitlines())


def extract(body):
    body = body.replace("\r\n", "\n")  # most older numpy issues use CRLF; the fence regex expects \n
    parts = []
    pos = 0
    for m in list(FENCE.finditer(body)) + [None]:
        text = body[pos:m.start() if m else len(body)]
        if has_doctest(text):
            parts.append(doctest_code(text))
        if m is None:
            break
        pos = m.end()
        tag, block = m.group(1).strip(), m.group(2)
        word = tag.split()[0].lower() if tag else ""
        if re.search(r"^Traceback \(most recent call last\)", block, re.M) or re.search(r"^\s*\$ ", block, re.M):
            continue
        if word in PY_TAGS or (not word and re.search(r"\bimport\b|\bnp\.", block)):
            parts.append(doctest_code(block) if has_doctest(block) else block)
    code = "\n\n".join(p.strip("\n") for p in parts if p.strip())
    if not code:
        return None
    if re.search(r"\bnp\.", code) and not re.search(r"^\s*import numpy\b", code, re.M):
        code = "import numpy as np\n\n" + code
    return code


MARK = "# --- snippet ---"  # layout of the first version (description on top); converted on the next run
GEN = "# ======== generated below: rewritten on every run, edit only the code above ========"
STAMP = re.compile(r"^# --- got on numpy \S+ \(hint: (\w+), code (\w+)\) ---$", re.M)
AUTO = re.compile(r"^# auto: (.*)$", re.M)
HEAD = re.compile(r"\A# https://\S+\n#.*\n# created_at:.*\n")
EXC = re.compile(r"^\s*(?:#\s*)?(?:[\w.]+\.)?(\w+(?:Error|Exception|Warning)):\s*(.*)$", re.M)
EXPECT = re.compile(r"\b(expect\w*|should(?:n't)?|instead|supposed to|would like|correct (?:result|output|answer)|intended)\b", re.I)
EXPECT_CODE = re.compile(r"#.*\b(expect\w*|should|wrong|correct|instead|gives|returns|bug)\b|#\s*(?:->|==>|array\(|\[|-?\d|True|False)", re.I)
MAX_OUT = 200  # lines of output kept in the file


def header(n, title, created):
    return f"# https://github.com/numpy/numpy/issues/{n}\n# {title.replace(chr(10), ' ')}\n# created_at: {created}\n\n"


def code_of(text):
    head = text.split("\n" + GEN, 1)[0]
    if MARK in head:
        head = head.split(MARK + "\n", 1)[1].split("\n# --- output on numpy", 1)[0]
    return HEAD.sub("", head).strip()


def digest(text):
    return hashlib.sha1(code_of(text).encode()).hexdigest()[:10]


def stamp(py):
    """(hint, code hash) of the last run written into the file, or None."""
    m = STAMP.search(py.read_text(encoding="utf-8"))
    return m.groups() if m else None


def auto_of(py):
    m = AUTO.search(py.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def clean_body(body):
    return re.sub(r"<!--.*?-->", "", body.replace("\r\n", "\n"), flags=re.S).strip()


def expected(body, code):
    """What should happen, in the reporter's words: sentences of the description and comments of the snippet."""
    text = FENCE.sub(" ", clean_body(body))
    said = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if EXPECT.search(s) and 10 < len(s.strip()) < 300]
    return list(dict.fromkeys(said))[:6] + [l.strip() for l in code.splitlines() if EXPECT_CODE.search(l)][:10]


def errors(text):
    return list(dict.fromkeys(f"{t}: {m}".strip() for t, m in EXC.findall(text)))


def compare(reported, now):
    if not reported:
        return "no error in the description to compare with"
    kind = lambda e: e.split(":", 1)[0]
    if not now:
        return "reported error gone"
    if kind(now[-1]) in {kind(e) for e in reported}:
        return "same error as reported"
    return f"different error ({kind(now[-1])}; reported {kind(reported[-1])})"


def comment(lines):
    return "\n".join(("# " + l).rstrip() for l in lines)


def write_result(py, body, text, hint):
    """Rewrite everything below the code: expected, reported, got (this run) and the description, all as comments."""
    cur = py.read_text(encoding="utf-8")
    code = code_of(cur)
    lines = text.rstrip().splitlines()
    if len(lines) > MAX_OUT:
        lines = [f"... {len(lines) - MAX_OUT} lines cut ..."] + lines[-MAX_OUT:]
    reported = errors(clean_body(body))
    now = errors(text.split("--- stderr ---", 1)[-1])
    head = HEAD.match(cur).group(0) if HEAD.match(cur) else ""
    exp = expected(body, code)
    py.write_text(
        f"{head}\n{code}\n\n\n{GEN}\n# auto: {compare(reported, now)}\n"
        f"# --- expected (sentences from the description, comments in the code) ---\n{comment(exp or ['(none found)'])}\n"
        f"# --- reported (errors in the description) ---\n{comment(reported[:3] or ['(none)'])}\n"
        f"# --- got on numpy {EXPECTED} (hint: {hint}, code {digest(cur)}) ---\n{comment(lines)}\n"
        f"# --- description (verbatim) ---\n{comment(re.sub(chr(10) + '{3,}', chr(10) * 2, clean_body(body)).splitlines())}\n",
        encoding="utf-8")


def run(py, cwd, timeout):
    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG") if k in os.environ}
    env["MPLBACKEND"] = "Agg"
    t = time.monotonic()
    try:
        p = subprocess.run([str(PYTHON), "-I", py.name], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                           capture_output=True, timeout=timeout)
        code, out, err = str(p.returncode), p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, out, err = "timeout", e.stdout or b"", e.stderr or b""
    dur = time.monotonic() - t
    text = (f"--- stdout ---\n{out.decode(errors='replace')}\n--- stderr ---\n{err.decode(errors='replace')}\n"
            f"--- exit ---\nexit: {code}  duration: {dur:.1f}s\n")
    return text, code, err.decode(errors="replace")


def classify(code, stderr):
    if code == "timeout":
        return "timeout"
    if code == "0" and "Traceback" not in stderr:
        return "ok"
    if BROKEN.search(stderr):
        return "snippet_broken"
    return "error"


def check_interpreter():
    r = subprocess.run([str(PYTHON), "-c", "import numpy; print(numpy.__version__)"], capture_output=True, text=True)
    v = r.stdout.strip()
    print(f"interpreter {PYTHON}: numpy {v or 'NOT IMPORTABLE'}")
    if v != EXPECTED:
        print(f"!!! WARNING: numpy is {v or 'missing'}, not {EXPECTED}; the hints do not test the 2.5.5 behaviour !!!",
              file=sys.stderr)


def tail(text, lines=40):
    ls = text.rstrip().splitlines()
    return "\n".join(ls if len(ls) <= lines else ["…"] + ls[-lines:])


def section_of(block, name):
    m = re.search(rf"^# --- {name}.*---\n((?:#.*\n)*?)(?=# ---|\Z)", block, re.M)
    return [l[2:] for l in m.group(1).splitlines()] if m else []


def write_review(out_dir, rows, con):
    """review.md: every case that ran (ok / error) as code / expected / reported / got, the description folded, by section;
    within a section the reported errors that are gone come first."""
    section = {}
    for kind, n in con.execute("select kind, number from actions where kind in (%s)" % ",".join("?" * len(KINDS)), KINDS):
        section.setdefault(n, kind)
    order = {k: i for i, k in enumerate(KINDS + ("original of a duplicate",))}
    first = lambda a: 0 if a == "reported error gone" else 1 if a.startswith("different") else 2 if a.startswith("same") else 3
    todo = sorted((r for r in rows if r["hint"] in ("ok", "error")),
                  key=lambda r: (order[section.get(r["number"], "original of a duplicate")], first(r["auto"]), r["number"]))
    out = [f"# Reproduce on numpy {EXPECTED}: {len(todo)} cases that ran\n",
           "Compare *got* with *expected* and *reported*; put the verdict in sheet.jsonl "
           "(still_there / gone / snippet_broken / cannot_tell). *auto* only compares exception types.\n"]
    last = None
    for r in todo:
        n, sec = r["number"], section.get(r["number"], "original of a duplicate")
        if sec != last:
            out.append(f"\n## {sec}\n")
            last = sec
        text = (out_dir / f"{n}.py").read_text(encoding="utf-8")
        gen = text.split("\n" + GEN, 1)[-1]
        pair = f" · pair with {', '.join(f'#{w}' for w in r['with'])}" if r["with"] else ""
        bullets = lambda ls: "\n".join(f"- {l}" for l in ls) or "- (none)"
        out.append(f"### [#{n}]({r['url']}) {r['title']}\n\n`{r['hint']}` · auto: **{r['auto']}**{pair}\n\n"
                   f"**Code**\n\n```python\n{code_of(text)}\n```\n\n"
                   f"**Expected**\n\n{bullets(section_of(gen, 'expected'))}\n\n"
                   f"**Reported**\n\n{bullets(section_of(gen, 'reported'))}\n\n"
                   f"**Got**\n\n```\n{tail(chr(10).join(section_of(gen, 'got')))}\n```\n\n"
                   f"<details><summary>Description</summary>\n\n```\n{chr(10).join(section_of(gen, 'description'))}\n```\n"
                   f"</details>\n\n---\n")
    (out_dir / "review.md").write_text("\n".join(out), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--only", type=int, nargs="+")
    ap.add_argument("--rerun", action="store_true")
    ap.add_argument("--timeout", type=float, default=60)
    a = ap.parse_args()
    check_interpreter()
    db = Path(a.db).absolute()
    out_dir = db.parent / "repro"
    out_dir.mkdir(exist_ok=True)
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cases = con.execute("select distinct i.number, i.title, coalesce(i.body,''), i.created_at from items i where i.kind='issue' "
                        "and (i.number in (select number from actions where kind in (%s)) "
                        "or i.number in (select target from actions where kind in (%s))) order by i.number"
                        % (",".join("?" * len(KINDS)), ",".join("?" * len(PAIRED))), KINDS + PAIRED).fetchall()
    pairs = collections.defaultdict(set)
    for n, t in con.execute("select number, target from actions where kind in (%s)" % ",".join("?" * len(PAIRED)), PAIRED):
        pairs[n].add(t)
        pairs[t].add(n)
    sheet = out_dir / "sheet.jsonl"
    prev = {r["number"]: r for r in map(json.loads, sheet.read_text(encoding="utf-8").splitlines())} if sheet.exists() else {}
    selected = set(a.only) if a.only else None
    if selected:
        missing = selected - {c[0] for c in cases}
        if missing:
            print(f"not issue cases, skipped: {sorted(missing)}")
    todo = [c for c in cases if selected is None or c[0] in selected]
    hints, made = {}, 0
    for i, (n, title, body, created) in enumerate(todo, 1):
        py = out_dir / f"{n}.py"
        if not py.exists():
            code = extract(body)
            if code is None:
                hints[n] = "crawl_error"
                continue
            with open(py, "x", encoding="utf-8") as f:
                f.write(header(n, title, created) + code + "\n")
            made += 1
        last = stamp(py)
        if not a.rerun and last and last[1] == digest(py.read_text(encoding="utf-8")):
            hints[n] = last[0]
            continue
        print(f"[{i}/{len(todo)}] #{n}", flush=True)
        text, code, stderr = run(py, out_dir, a.timeout)
        hints[n] = classify(code, stderr)
        write_result(py, body, text, hints[n])
        print(f"    {hints[n]}", flush=True)
    rows = []
    for n, title, body, created in cases:
        if n not in hints:
            if (out_dir / f"{n}.py").exists():
                hints[n] = (stamp(out_dir / f"{n}.py") or ("not_run",))[0]
            else:
                hints[n] = "crawl_error" if prev.get(n, {}).get("hint") == "crawl_error" else "not_run"
        old = prev.get(n, {})
        rows.append({"number": n, "title": title, "url": f"https://github.com/numpy/numpy/issues/{n}", "hint": hints[n],
                     "with": sorted(pairs.get(n, ())),
                     "auto": auto_of(out_dir / f"{n}.py") if (out_dir / f"{n}.py").exists() else "", "verdict": old.get("verdict", ""), "note": old.get("note", "")})
    current = {c[0] for c in cases}
    rows += [r for n, r in prev.items() if n not in current]
    tmp = sheet.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(sheet)
    write_review(out_dir, rows, con)
    print(f"created {made} .py files; sheet {sheet}; review {out_dir / 'review.md'}")
    for hint, count in collections.Counter(r["hint"] for r in rows if r["number"] in current).most_common():
        print(f"{hint:15} {count}")


if __name__ == "__main__":
    sys.exit(main())

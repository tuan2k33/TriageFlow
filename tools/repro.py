"""Help for checking old issues by hand: reruns the Python snippets of the issues behind close/recurrence proposals on the
installed numpy and records what happened, so a person can decide whether each old bug is still there. Not part of the
pipeline. The snippets come from the internet and are run only as isolated subprocesses (python -I, minimal environment,
timeout, cwd in repro/).

usage: python tools/repro.py data/<owner>__<name>/repo.db [--only N [N ...]] [--rerun] [--timeout 60]
writes repro/<number>.py (created once, then hand-edited, never overwritten), repro/<number>.out and repro/sheet.jsonl
next to the db. The verdict and note columns of sheet.jsonl are kept across reruns.
"""
import argparse, collections, json, os, re, sqlite3, subprocess, sys, time
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


MARK = "# --- snippet ---"


def header(n, title, created, body):
    desc = re.sub(r"<!--.*?-->", "", body.replace("\r\n", "\n"), flags=re.S).strip()
    desc = "\n".join(("# " + l).rstrip() for l in re.sub(r"\n{3,}", "\n\n", desc).splitlines())
    return (f"# https://github.com/numpy/numpy/issues/{n}\n# {title.replace(chr(10), ' ')}\n# created_at: {created}\n#\n"
            f"# Description:\n{desc}\n\n{MARK}\n")


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


def hint_from_out(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    exit_pos = text.rfind("\n--- exit ---\n")
    err_pos = text.rfind("\n--- stderr ---\n", 0, exit_pos)
    code = re.match(r"exit: (\S+)", text[exit_pos + len("\n--- exit ---\n"):]).group(1)
    return classify(code, text[err_pos:exit_pos])


def check_interpreter():
    r = subprocess.run([str(PYTHON), "-c", "import numpy; print(numpy.__version__)"], capture_output=True, text=True)
    v = r.stdout.strip()
    print(f"interpreter {PYTHON}: numpy {v or 'NOT IMPORTABLE'}")
    if v != EXPECTED:
        print(f"!!! WARNING: numpy is {v or 'missing'}, not {EXPECTED}; the hints do not test the 2.5.5 behaviour !!!",
              file=sys.stderr)


def prose(body, limit=1500):
    """The description without code, HTML comments and the version block: what the reporter expected and saw."""
    t = re.sub(r"<!--.*?-->", "", body.replace("\r\n", "\n"), flags=re.S)
    t = FENCE.sub(lambda m: "[code]" if m.group(1).strip().lower() in PY_TAGS or not m.group(1).strip() else m.group(0), t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t if len(t) <= limit else t[:limit].rsplit(" ", 1)[0] + " …"


def tail(text, lines=40):
    ls = text.rstrip().splitlines()
    return "\n".join(ls if len(ls) <= lines else ["…"] + ls[-lines:])


def write_review(out_dir, rows, bodies, con):
    """review.md: for every case that ran (ok / error), the description beside the snippet and its output, by section."""
    section = {}
    for kind, n in con.execute("select kind, number from actions where kind in (%s)" % ",".join("?" * len(KINDS)), KINDS):
        section.setdefault(n, kind)
    order = {k: i for i, k in enumerate(KINDS + ("original of a duplicate",))}
    todo = sorted((r for r in rows if r["hint"] in ("ok", "error") and r["number"] in bodies),
                  key=lambda r: (order[section.get(r["number"], "original of a duplicate")], r["hint"], r["number"]))
    out = [f"# Reproduce on numpy {EXPECTED}: {len(todo)} cases that ran\n",
           "Compare the output with what the description says should and should not happen; put the verdict in sheet.jsonl "
           "(still_there / gone / snippet_broken / cannot_tell).\n"]
    last = None
    for r in todo:
        n, sec = r["number"], section.get(r["number"], "original of a duplicate")
        if sec != last:
            out.append(f"\n## {sec}\n")
            last = sec
        pair = f" · pair with {', '.join(f'#{w}' for w in r['with'])}" if r["with"] else ""
        code = (out_dir / f"{n}.py").read_text(encoding="utf-8")
        code = (code.split(MARK + "\n", 1)[1] if MARK in code else re.sub(r"\A(#.*\n){1,3}", "", code)).strip()
        res = (out_dir / f"{n}.out").read_text(encoding="utf-8", errors="replace")
        out.append(f"### [#{n}]({r['url']}) {r['title']}\n\n`{r['hint']}`{pair}\n\n**Description**\n\n"
                   + "\n".join("> " + l for l in prose(bodies[n]).splitlines())
                   + f"\n\n**Snippet**\n\n```python\n{code}\n```\n\n**Output**\n\n```\n{tail(res)}\n```\n\n---\n")
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
        py, outf = out_dir / f"{n}.py", out_dir / f"{n}.out"
        if not py.exists():
            code = extract(body)
            if code is None:
                hints[n] = "crawl_error"
                continue
            with open(py, "x", encoding="utf-8") as f:
                f.write(header(n, title, created, body) + code + "\n")
            made += 1
        if not a.rerun and outf.exists() and outf.stat().st_mtime > py.stat().st_mtime:
            hints[n] = hint_from_out(outf)
            continue
        print(f"[{i}/{len(todo)}] #{n}", flush=True)
        text, code, stderr = run(py, out_dir, a.timeout)
        outf.write_text(text, encoding="utf-8")
        hints[n] = classify(code, stderr)
        print(f"    {hints[n]}", flush=True)
    rows = []
    for n, title, body, created in cases:
        if n not in hints:
            if (out_dir / f"{n}.out").exists():
                hints[n] = hint_from_out(out_dir / f"{n}.out")
            elif (out_dir / f"{n}.py").exists():
                hints[n] = "not_run"
            else:
                hints[n] = "crawl_error" if prev.get(n, {}).get("hint") == "crawl_error" else "not_run"
        old = prev.get(n, {})
        rows.append({"number": n, "title": title, "url": f"https://github.com/numpy/numpy/issues/{n}", "hint": hints[n],
                     "with": sorted(pairs.get(n, ())), "verdict": old.get("verdict", ""), "note": old.get("note", "")})
    current = {c[0] for c in cases}
    rows += [r for n, r in prev.items() if n not in current]
    tmp = sheet.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(sheet)
    write_review(out_dir, rows, {c[0]: c[2] for c in cases}, con)
    print(f"created {made} .py files; sheet {sheet}; review {out_dir / 'review.md'}")
    for hint, count in collections.Counter(r["hint"] for r in rows if r["number"] in current).most_common():
        print(f"{hint:15} {count}")


if __name__ == "__main__":
    sys.exit(main())

"""Help for checking old issues by hand: reruns the Python snippets of the issues behind close/recurrence proposals on the
installed numpy and records what happened, so a person can decide whether each old bug is still there. Not part of the
pipeline. The snippets come from the internet and are run only as isolated subprocesses (python -I, minimal environment,
timeout, cwd in repro/).

usage: python tools/repro.py data/<owner>__<name>/repo.db [--only N [N ...]] [--rerun] [--timeout 60]
writes repro/<number>.py: the issue link, the snippet (created once, then hand-edited), and below it as comments, rewritten
on every run of changed code: auto (exception types compared), expected (what should happen and the error reported; quoted
by tools/llm_extract.py when repro/extract.jsonl has the issue, else found by rules), got on this numpy, the description.
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
RULES = Path(__file__).with_name("issue_templates.json")  # per repo: the issue templates and which section holds what
HEADING = re.compile(r"^#{2,4}[ \t]*(.+?)[ \t]*$", re.M)
FILLER = re.compile(r"^\s*(_?no response_?|none|n/?a|-|\[code\])\s*$", re.I)
MAX_EXPECTED = 25  # lines of a template's description section kept


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


def sections(body):
    """{heading (lower case, no colon): text}; the text before the first heading is "_preamble"."""
    parts = HEADING.split(clean_body(body))
    secs = {"_preamble": parts[0].strip()}
    for h, c in zip(parts[1::2], parts[2::2]):
        secs.setdefault(h.strip().rstrip(":").strip().lower(), c.strip())
    return secs


def template_of(body, rules):
    """(the first template whose headings are all in the description, its sections) or (None, sections)."""
    secs = sections(body)
    return next((t for t in rules if all(h in secs for h in t["match"])), None), secs


def take(secs, names):
    return "\n\n".join(secs[n] for n in names if secs.get(n))


def template_fields(t, secs):
    """(code or None, expected lines, reported lines) read from the sections the template names."""
    raw = take(secs, t.get("code", []))
    code = extract(raw) if raw else None
    if code is None and re.search(r"\bimport\b|\bnp\.", raw):
        code = raw
    lines = lambda text: [l.rstrip() for l in FENCE.sub(lambda m: m.group(2), text).splitlines() if l.strip() and not FILLER.match(l)]
    rep = take(secs, t.get("reported", []))
    reported = errors(rep) or lines(rep)[:15]
    exp = lines(FENCE.sub("[code]", take(secs, t.get("expected", []))))
    return code, exp[:MAX_EXPECTED] + ([f"... {len(exp) - MAX_EXPECTED} more lines in the description"] if len(exp) > MAX_EXPECTED else []), reported


def expected(body, code):
    """What should happen, in the reporter's words: sentences of the description and comments of the snippet."""
    text = FENCE.sub(" ", clean_body(body))
    said = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if EXPECT.search(s) and 10 < len(s.strip()) < 300]
    return list(dict.fromkeys(said))[:6] + [l.strip() for l in code.splitlines() if EXPECT_CODE.search(l)][:10]


def errors(text):
    seen = {}
    for t, m in EXC.findall(text):
        seen.setdefault(re.sub(r"\W+$", "", f"{t}: {m}".strip()), f"{t}: {m}".strip())  # same error with or without a final "."
    return list(seen.values())


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


def write_result(py, body, text, hint, ext=None, tpl=None):
    """Rewrite everything below the code: expected (with the reported errors), got (this run) and the description.
    Expected comes from the issue template's sections when the issue follows one, else from tools/llm_extract.py, else
    from rules over the whole description."""
    cur = py.read_text(encoding="utf-8")
    code = code_of(cur)
    lines = text.rstrip().splitlines()
    if len(lines) > MAX_OUT:
        lines = [f"... {len(lines) - MAX_OUT} lines cut ..."] + lines[-MAX_OUT:]
    tpl, secs = tpl if tpl else (None, None)
    reported = errors(clean_body(body))
    now = errors("\n".join(l for l in text.splitlines() if not l.startswith((">>> ", "... "))))
    head = HEAD.match(cur).group(0) if HEAD.match(cur) else ""
    if tpl:
        _, exp_lines, rep_lines = template_fields(tpl, secs)
        reported = errors("\n".join(rep_lines)) or reported
        names = lambda k: " + ".join(tpl.get(k, [])) or "-"
        title = (f"expected (template '{tpl['name']}': {names('expected')}; 'reported:' is {names('reported')})")
        exp = exp_lines + [f"reported: {r}" for r in rep_lines]
    elif ext and ext["hash"] == hashlib.sha1(body.encode()).hexdigest()[:10]:  # tools/llm_extract.py, quotes checked
        title = f"expected (quoted by an LLM, checked against the description; kind: {ext['kind']}; 'reported:' is what the reporter got)"
        exp = ext["expected"] + [f"reported: {r}" for r in ext["reported"]]
    else:
        title = "expected (no template: guessed from the description and the code; 'reported:' is the error the reporter got)"
        exp = expected(body, code) + [f"reported: {e}" for e in reported[:3]]
    py.write_text(
        f"{head}\n{code}\n\n\n{GEN}\n# auto: {compare(reported, now)}\n"
        f"# --- {title} ---\n{comment(exp or ['(none found)'])}\n"
        f"# --- got on numpy {EXPECTED} (hint: {hint}, code {digest(cur)}) ---\n{comment(lines)}\n"
        f"# --- description (verbatim) ---\n{comment(re.sub(chr(10) + '{3,}', chr(10) * 2, clean_body(body)).splitlines())}\n",
        encoding="utf-8")


RUNNER = r"""
import ast, sys, traceback
path = sys.argv[1]
src = open(path, encoding="utf-8").read()
lines = src.splitlines()
ns = {"__name__": "__main__", "__file__": path}
failed = False
for node in ast.parse(src, path).body:
    print(">>> " + "\n... ".join(lines[node.lineno - 1:node.end_lineno]), flush=True)
    try:
        exec(compile(ast.Interactive([node]), path, "single"), ns)
    except SystemExit:
        raise
    except BaseException:
        failed = True
        traceback.print_exc(file=sys.stdout)
    sys.stdout.flush()
sys.exit(1 if failed else 0)
"""  # run the snippet like the REPL it was copied from: echo each statement, print expression values, go on after an error


def run(py, cwd, timeout):
    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG") if k in os.environ}
    env["MPLBACKEND"] = "Agg"
    t = time.monotonic()
    try:
        p = subprocess.run([str(PYTHON), "-I", "-c", RUNNER, py.name], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        code, out = str(p.returncode), p.stdout
    except subprocess.TimeoutExpired as e:
        code, out = "timeout", e.stdout or b""
    out = out.decode(errors="replace")
    return f"{out.rstrip()}\n(exit {code}, {time.monotonic() - t:.1f}s)\n", code, out


def classify(code, stderr):
    if code == "timeout":
        return "timeout"
    if code == "0":
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
    """review.md: every case that ran (ok / error) as code / expected / got, the description folded, by section;
    within a section the reported errors that are gone come first."""
    section = {}
    for kind, n in con.execute("select kind, number from actions where kind in (%s)" % ",".join("?" * len(KINDS)), KINDS):
        section.setdefault(n, kind)
    for (n,) in con.execute("select target from actions where kind in (%s)" % ",".join("?" * len(PAIRED)), PAIRED):
        section.setdefault(n, "original of a duplicate")
    order = {k: i for i, k in enumerate(KINDS + ("original of a duplicate", "not in the report"))}
    first = lambda a: 0 if a == "reported error gone" else 1 if a.startswith("different") else 2 if a.startswith("same") else 3
    todo = sorted((r for r in rows if r["hint"] in ("ok", "error")),
                  key=lambda r: (order[section.get(r["number"], "not in the report")], first(r["auto"]), r["number"]))
    out = [f"# Reproduce on numpy {EXPECTED}: {len(todo)} cases that ran\n",
           "Compare *got* with *expected* (lines starting `reported:` are the error the reporter got); put the verdict in sheet.jsonl "
           "(still_there / gone / snippet_broken / cannot_tell). *auto* only compares exception types.\n"]
    last = None
    for r in todo:
        n, sec = r["number"], section.get(r["number"], "not in the report")
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
                   f"**Got**\n\n```\n{tail(chr(10).join(section_of(gen, 'got')))}\n```\n\n"
                   f"<details><summary>Description</summary>\n\n```\n{chr(10).join(section_of(gen, 'description'))}\n```\n"
                   f"</details>\n\n---\n")
    (out_dir / "review.md").write_text("\n".join(out), encoding="utf-8")


def write_prs(out_dir, rows, con):
    """prs.jsonl and prs.md: every open PR with the issues it says it fixes (GitHub's closing link, or "fixes #N" in its
    own description) and what the reproduce check has for each of them. Only the link: whether the PR fixes them is not
    judged, and nothing of the PR is built or run."""
    by = {r["number"]: r for r in rows}
    prs = []
    for n, title in con.execute("select number, title from items where kind = 'pr' and state = 'open' order by number"):
        linked = [d for (d,) in con.execute(
            "select distinct l.dst from links l join items i on i.number = l.dst where l.src = ? and i.kind = 'issue' "
            "and l.kind in ('closes_official', 'closes') order by l.dst", (n,))]
        if linked:
            prs.append({"number": n, "title": title, "url": f"https://github.com/numpy/numpy/pull/{n}", "issues": [
                {k: by[d][k] for k in ("number", "template", "hint", "auto")} | {"file": f"{d}.py" if (out_dir / f"{d}.py").exists() else ""}
                if d in by else {"number": d, "template": "", "hint": "not checked", "auto": "", "file": ""} for d in linked]})
    (out_dir / "prs.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in prs), encoding="utf-8")
    md = [f"# Open PRs and the issues they fix: {len(prs)} PRs\n",
          "Each linked issue with its reproduce result on numpy %s; open the issue's .py for code / expected / got.\n" % EXPECTED]
    for p in prs:
        md.append(f"## [#{p['number']}]({p['url']}) {p['title']}\n")
        for i in p["issues"]:
            f = f"[{i['file']}]({i['file']})" if i["file"] else "no snippet file"
            md.append(f"- #{i['number']}: {i['hint']}, template {i['template'] or '?'}"
                      f"{', ' + i['auto'] if i['auto'] else ''} · {f}")
        md.append("")
    (out_dir / "prs.md").write_text("\n".join(md), encoding="utf-8")
    return len(prs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--only", type=int, nargs="+")
    ap.add_argument("--rerun", action="store_true")
    ap.add_argument("--all-open", action="store_true", help="every open issue, not only those in the report")
    ap.add_argument("--timeout", type=float, default=60)
    a = ap.parse_args()
    check_interpreter()
    db = Path(a.db).absolute()
    out_dir = db.parent / "repro"
    out_dir.mkdir(exist_ok=True)
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cases = con.execute("select distinct i.number, i.title, coalesce(i.body,''), i.created_at from items i where i.kind='issue' "
                        "and (i.number in (select number from actions where kind in (%s)) "
                        "or i.number in (select target from actions where kind in (%s))%s) order by i.number"
                        % (",".join("?" * len(KINDS)), ",".join("?" * len(PAIRED)), " or i.state = 'open'" * a.all_open),
                        KINDS + PAIRED).fetchall()
    in_report = {n for (n,) in con.execute("select number from actions where kind in (%s) union select target from actions "
                                          "where kind in (%s)" % (",".join("?" * len(KINDS)), ",".join("?" * len(PAIRED))),
                                          KINDS + PAIRED)}
    pairs = collections.defaultdict(set)
    for n, t in con.execute("select number, target from actions where kind in (%s)" % ",".join("?" * len(PAIRED)), PAIRED):
        pairs[n].add(t)
        pairs[t].add(n)
    sheet = out_dir / "sheet.jsonl"
    repo = con.execute("select v from meta where k = 'repo'").fetchone()[0]
    rules = json.loads(RULES.read_text())[repo]["templates"] if RULES.exists() and repo in json.loads(RULES.read_text()) else []
    ex = out_dir / "extract.jsonl"
    extracts = {r["number"]: r for r in map(json.loads, ex.read_text(encoding="utf-8").splitlines())} if ex.exists() else {}
    prev = {r["number"]: r for r in map(json.loads, sheet.read_text(encoding="utf-8").splitlines())} if sheet.exists() else {}
    selected = set(a.only) if a.only else None
    if selected:
        missing = selected - {c[0] for c in cases}
        if missing:
            print(f"not issue cases, skipped: {sorted(missing)}")
    todo = [c for c in cases if selected is None or c[0] in selected]
    hints, made, templates = {}, 0, {}
    for i, (n, title, body, created) in enumerate(todo, 1):
        py = out_dir / f"{n}.py"
        tpl, secs = template_of(body, rules)
        templates[n] = tpl["name"] if tpl else "none"
        if tpl and tpl.get("repro") is False:
            hints[n] = "not_a_bug"
            continue
        code = template_fields(tpl, secs)[0] if tpl else extract(body)
        if py.exists() and tpl and code and code_of(py.read_text(encoding="utf-8")) == (extract(body) or "").strip() != code.strip():
            py.write_text(header(n, title, created) + code + "\n", encoding="utf-8")  # untouched guess -> the template's code
        if not py.exists():
            if code is None or (tpl is None and a.all_open and n not in in_report):
                hints[n] = "crawl_error" if tpl else "no_template"  # outside the report only templated issues are tried
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
        write_result(py, body, text, hints[n], extracts.get(n), (tpl, secs) if tpl else None)
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
                     "template": templates.get(n) or (lambda t: t["name"] if t else "none")(template_of(body, rules)[0]),
                     "with": sorted(pairs.get(n, ())),
                     "auto": auto_of(out_dir / f"{n}.py") if (out_dir / f"{n}.py").exists() else "", "verdict": old.get("verdict", ""), "note": old.get("note", "")})
    current = {c[0] for c in cases}
    rows += [r for n, r in prev.items() if n not in current]
    tmp = sheet.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(sheet)
    write_review(out_dir, rows, con)
    print(f"{write_prs(out_dir, rows, con)} open PRs linked to issues: {out_dir / 'prs.md'}")
    print(f"created {made} .py files; sheet {sheet}; review {out_dir / 'review.md'}")
    for hint, count in collections.Counter(r["hint"] for r in rows if r["number"] in current).most_common():
        print(f"{hint:15} {count}")


if __name__ == "__main__":
    sys.exit(main())

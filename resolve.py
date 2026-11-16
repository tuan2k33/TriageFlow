"""For open issues that mention a merged PR: should a maintainer close it, or decide? (suggestion only)

usage: python resolve.py data/<owner>__<name>/repo.db   (needs triageflow.py run first)
"""
import collections, json, os, re, sqlite3, sys, time
import importlib.util

spec = importlib.util.spec_from_file_location("suggest", os.path.join(os.path.dirname(os.path.abspath(__file__)), "suggest.py"))
sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)

REF = re.compile(r"(?<![\w/])#(\d+)\b")
BATCH = 12


def mentions(db):
    """open issue -> {merged PR number: [(where, context)]}; merged = {pr: (title, closed_at)}."""
    merged = {n: (t, c or "") for n, t, c in db.execute("select number,title,closed_at from items where kind='pr' and merged=1")}
    is_open = {n for (n,) in db.execute("select number from items where kind='issue' and state='open'")}
    out = collections.defaultdict(dict)
    srcs = [(n, "body", t) for n, t in db.execute("select number, coalesce(title,'')||char(10)||coalesce(body,'') from items where kind='issue' and state='open'")]
    srcs += [(n, "comment", b or "") for n, b in db.execute("select c.number,c.body from comments c join items i using(number) where i.kind='issue' and i.state='open' and c.kind='comment'")]
    for n, where, text in srcs:
        for m in REF.finditer(text):
            k = int(m.group(1))
            if k in merged and k != n:
                out[n].setdefault(k, []).append((where, re.sub(r"\s+", " ", text[max(0, m.start() - 130):m.end() + 90])))
    for pr, issue in db.execute("select src, dst from links where kind='closes_official'"):
        if pr in merged and issue in is_open:
            out[issue].setdefault(pr, []).insert(0, ("GitHub link", "GitHub records this merged PR as closing this issue"))
    return out, merged


def ask(batch, info, merged, key):
    lines = []
    for n in batch:
        title, body, created, labels = info[n]
        ms = []
        for pr, ctxs in list(batch[n].items())[:3]:
            ms.append(f"    PR #{pr} \"{merged[pr][0][:90]}\" merged {merged[pr][1][:10]}; mentioned in {ctxs[0][0]}: ...{ctxs[0][1]}...")
        lines.append(f"[{n}] {title}  (opened {created[:10]}; labels: {labels or 'none'})\n    {re.sub(r'\s+', ' ', body)[:200]}\n" + "\n".join(ms))
    prompt = (
        "You help maintainers triage open GitHub issues. Each issue below mentions one or more already-MERGED pull requests.\n"
        "Decide for each issue:\n"
        '- "close": a merged PR clearly resolves the whole issue, so a maintainer could likely close it.\n'
        '- "needs_decision": a merged PR partly addresses it, or it is unclear/contested whether it is resolved, so a maintainer should look.\n'
        '- "none": the mention is incidental (related work, example, background); the issue is still open on its merits.\n'
        "Be conservative: choose close only with clear evidence in the text shown. Give a reason of at most 15 words.\n\n"
        + "\n".join(lines)
        + '\n\nAnswer with only a JSON array: [{"id": <number>, "verdict": "close"|"needs_decision"|"none", "reason": "..."}, ...]')
    txt = sg.call_llm(prompt, key)
    res = {}
    for o in json.loads(re.search(r"\[.*\]", txt, re.S).group(0)):
        if o.get("verdict") in ("close", "needs_decision", "none"):
            res[int(o["id"])] = (o["verdict"], str(o.get("reason", ""))[:200])
    return res


def main(path):
    db = sqlite3.connect(path, timeout=120)
    key = next(l.split("=", 1)[1].strip().strip("'\"") for l in open(".env") if l.startswith("OPENROUTER_API_KEY="))
    men, merged = mentions(db)
    info = {n: (t, b or "", c, l or "") for n, t, b, c, l in db.execute("select number,title,body,created_at,labels from items where kind='issue' and state='open'")}
    db.execute("create table if not exists resolve_hints(number integer primary key, verdict text, reason text, prs text)")
    done = {r[0] for r in db.execute("select number from resolve_hints")}
    todo = [n for n in sorted(men) if n not in done]
    print(f"{len(men)} candidates, {len(todo)} to judge", flush=True)
    for b in range(0, len(todo), BATCH):
        ch = {n: men[n] for n in todo[b:b + BATCH]}
        res = ask(ch, info, merged, key)
        for n, (v, r) in res.items():
            db.execute("insert or replace into resolve_hints values(?,?,?,?)", (n, v, r, json.dumps(sorted(men[n]))))
        db.commit()
        print(f"  {min(b + BATCH, len(todo))}/{len(todo)}", flush=True)
        time.sleep(3.5)
    print(db.execute("select verdict,count(*) from resolve_hints group by 1").fetchall())


if __name__ == "__main__":
    main(sys.argv[1])

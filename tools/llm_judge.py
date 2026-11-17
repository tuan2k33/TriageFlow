"""Help for checking report rows by hand: a free OpenRouter model reads both items of each proposal (description and
comments, from repo.db) and gives a verdict with one line of reason. Not part of the pipeline: nothing else reads its
output, and its verdicts are only worth something after they are compared with a person's on a sample.

usage: set -a; . ~/.dev/secrets.env; set +a
       python tools/llm_judge.py data/<owner>__<name>/repo.db [--model ID] [--limit N]
       python tools/llm_judge.py data/<owner>__<name>/repo.db --summary
writes judge.jsonl next to the db; a rerun skips rows already judged (free models allow few requests per day).
"""
import argparse, collections, json, os, re, sqlite3, sys, time, urllib.error, urllib.request
from pathlib import Path

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
PER_ITEM = 7000  # characters of description + comments per item
QUESTIONS = {  # kind: (question, allowed verdicts); A is the row's item, B its target
    "close_fixed_linked": ("A is an open issue, B a merged PR that GitHub links as closing it. Does B fully fix what A asks for?",
                           ["fixed", "partly", "not_fixed", "unclear"]),
    "close_duplicate_likely": ("A and B are two open issues. Are they the same problem (a duplicate), only related, or different?",
                               ["same", "related", "different"]),
    "check_recurrence": ("A is an open issue, B an older closed one. Are they the same problem (a duplicate or the old bug back), only related, or different?",
                         ["same", "related", "different"]),
    "close_fixed_similar": ("A is an open issue, B a later merged PR with no link to it. Does B fix A fully, partly, or is it only related or unrelated?",
                            ["fixed", "partly", "related", "unrelated"]),
    "review_competing": ("A and B are two open PRs. Do they make the same change (only one should be merged), overlap in part, or are they independent?",
                         ["same", "overlap", "independent"]),
}


def item_text(db, n):
    kind, title, body, state, reason, merged = db.execute(
        "select kind, title, coalesce(body,''), state, state_reason, merged from items where number=?", (n,)).fetchone()
    status = "merged" if merged else (reason or state)
    com = [f"[{a}{' (maintainer)' if r in ('MEMBER', 'OWNER', 'COLLABORATOR') else ''}] {b}" for a, r, b in db.execute(
        "select author, assoc, coalesce(body,'') from comments where number=? and kind='comment' and bot=0 order by created_at", (n,))]
    text = re.sub(r"<!--.*?-->", "", f"{body}\n\n--- comments ---\n" + "\n\n".join(com), flags=re.S)
    if len(text) > PER_ITEM:  # keep the start (the problem) and the end (how the thread ended)
        text = text[:PER_ITEM // 3] + "\n[...]\n" + text[-2 * PER_ITEM // 3:]
    return f"#{n} [{kind}, {status}] {title}\n{text}"


def ask(model, prompt):
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", method="POST",
                                 data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0}).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["choices"][0]["message"]["content"] or ""


def summary(out):
    rows = [json.loads(l) for l in out.read_text().splitlines()] if out.exists() else []
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[r["kind"]][r["verdict"]] += 1
    for k, c in by.items():
        print(f"{k:24} {sum(c.values()):4}  " + ", ".join(f"{v} {n}" for v, n in c.most_common()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    out = Path(a.db).parent / "judge.jsonl"
    if a.summary:
        return summary(out)
    db = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    done = {(r["kind"], r["number"], r["target"]) for r in map(json.loads, out.read_text().splitlines())} if out.exists() else set()
    todo = [r for r in db.execute("select kind, number, target, signal, reason from actions where kind in (%s) order by kind, score desc"
                                  % ",".join("?" * len(QUESTIONS)), list(QUESTIONS)) if tuple(r[:3]) not in done]
    print(f"{len(todo)} rows to judge with {a.model}", flush=True)
    for i, (kind, n, m, signal, reason) in enumerate(todo[:a.limit or None]):
        q, verdicts = QUESTIONS[kind]
        prompt = (f"You check triage proposals for a GitHub repository. {q}\n\nAnswer with one line of JSON only: "
                  f'{{"verdict": one of {verdicts}, "reason": "one short sentence"}}\n\n=== A ===\n{item_text(db, n)}\n\n=== B ===\n{item_text(db, m)}')
        for attempt in range(4):
            try:
                text = ask(a.model, prompt)
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"  rate limited ({e.read()[:200]!r}); stopping, rerun later to continue", flush=True)
                    return
                if attempt == 3:
                    raise
                time.sleep(10 * (attempt + 1))
            except (urllib.error.URLError, TimeoutError, ConnectionError, KeyError, json.JSONDecodeError):  # network drop, empty answer
                if attempt == 3:
                    raise
                time.sleep(10 * (attempt + 1))
        j = re.search(r"\{.*\}", text, re.S)
        try:
            v = json.loads(j.group(0)) if j else {}
        except json.JSONDecodeError:
            v = {}
        verdict = v.get("verdict") if v.get("verdict") in verdicts else "unparsed"
        with out.open("a") as f:
            f.write(json.dumps({"kind": kind, "number": n, "target": m, "signal": signal, "verdict": verdict,
                                "reason": v.get("reason") or text[:300], "model": a.model}) + "\n")
        print(f"  [{i + 1}/{len(todo)}] {kind} #{n} -> #{m}: {verdict}", flush=True)
        time.sleep(4)  # free models: about 20 requests per minute


if __name__ == "__main__":
    sys.exit(main())

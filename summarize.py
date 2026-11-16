"""Squash each discussion (issue/PR + its comments) into one short summary of what was agreed and the outcome.

Free OpenRouter models are limited (~1000 requests/day), so this is resumable and ordered: open items first,
then closed ones by most recently updated. Re-summarizes an item only when its comment count changed.

usage: python summarize.py data/<owner>__<name>/repo.db [--max-calls 500] [--min-comments 2] [--only-open]
"""
import argparse, json, os, re, sqlite3, time
from concurrent.futures import ThreadPoolExecutor
import importlib.util

spec = importlib.util.spec_from_file_location("suggest", os.path.join(os.path.dirname(os.path.abspath(__file__)), "suggest.py"))
sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)

STATUS = ("resolved", "agreed_plan", "disagreement", "waiting", "abandoned", "unclear")
MAINT = {"OWNER", "MEMBER", "COLLABORATOR"}
PER_CALL_CHARS = 30000
WORKERS = 3


def thread_text(item, comments):
    n, kind, state, reason, merged, title, body = item
    st = state + (" (merged)" if merged else f" ({reason})" if reason else "")
    head = f"[{n}] {kind.upper()} {st}: {title}\n  opening: {re.sub(r'\s+', ' ', body or '')[:500]}"
    cs = comments if len(comments) <= 9 else comments[:2] + comments[-7:]
    lines = [f"  - {'maintainer ' if assoc in MAINT else ''}{author}: {re.sub(r'\s+', ' ', b or '')[:350]}" for author, assoc, b in cs]
    skipped = len(comments) - len(cs)
    if skipped:
        lines.insert(2, f"  - ({skipped} comments omitted)")
    return head + "\n" + "\n".join(lines)


def ask(blocks, key):
    prompt = (
        "Summarize each GitHub discussion below into ONE short paragraph (max 45 words): the problem or proposal, "
        "what participants agreed or disagreed on, and the outcome (e.g. fixed by #N, rejected, waiting for X). "
        "Use only the text shown; do not invent. Also give a status, one of: "
        + ", ".join(STATUS) + ".\n\n" + "\n\n".join(blocks)
        + '\n\nAnswer with only a JSON array: [{"id": <number>, "summary": "...", "status": "..."}, ...]')
    txt = sg.call_llm(prompt, key)
    res = {}
    for o in json.loads(re.search(r"\[.*\]", txt, re.S).group(0)):
        st = o.get("status") if o.get("status") in STATUS else "unclear"
        res[int(o["id"])] = (str(o.get("summary", "")).strip()[:600], st)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--max-calls", type=int, default=500)
    ap.add_argument("--min-comments", type=int, default=2, help="human comments needed for a discussion to be worth summarizing")
    ap.add_argument("--only-open", action="store_true")
    a = ap.parse_args()
    db = sqlite3.connect(a.db, timeout=120)
    key = next(l.split("=", 1)[1].strip().strip("'\"") for l in open(".env") if l.startswith("OPENROUTER_API_KEY="))
    db.execute("create table if not exists summaries(number integer primary key, summary text, status text, n_comments integer, model text)")
    todo = db.execute(f"""
        select i.number, i.kind, i.state, i.state_reason, i.merged, i.title, i.body, count(c.id) n
        from items i join comments c on c.number=i.number and c.bot=0 and c.kind='comment'
        {"where i.state='open'" if a.only_open else ""}
        group by i.number having n >= ?
           and not exists (select 1 from summaries s where s.number=i.number and s.n_comments=n)
        order by (i.state='open') desc, i.updated_at desc""", (a.min_comments,)).fetchall()
    print(f"{len(todo)} discussions to summarize (min {a.min_comments} human comments)", flush=True)

    batches, batch, size = [], [], 0
    for row in todo:
        n, nc = row[0], row[7]
        cs = db.execute("select author, assoc, body from comments where number=? and bot=0 and kind='comment' order by created_at", (n,)).fetchall()
        t = thread_text(row[:7], cs)
        if batch and size + len(t) > PER_CALL_CHARS:
            batches.append(batch)
            batch, size = [], 0
            if len(batches) >= a.max_calls:
                break
        batch.append((n, nc, t))
        size += len(t)
    if batch and len(batches) < a.max_calls:
        batches.append(batch)

    def run(b):
        time.sleep(3.5)  # stay well under the free tier's 20 requests/minute with WORKERS in flight
        try:
            return b, ask([t for _, _, t in b], key)
        except Exception as e:  # one bad answer should not stop the others; those items are retried next run
            print(f"  batch failed: {str(e)[:100]}", flush=True)
            return b, {}

    calls = done = 0
    with ThreadPoolExecutor(WORKERS) as ex:  # LLM calls in parallel, writes stay in this thread
        for b, res in ex.map(run, batches):
            for n, nc, _ in b:
                if n in res:
                    db.execute("insert or replace into summaries values(?,?,?,?,?)", (n, res[n][0], res[n][1], nc, sg.MODEL))
                    done += 1
            db.commit()
            calls += 1
            print(f"  call {calls}/{len(batches)}: {done} summarized", flush=True)
    print(f"done: {done} summarized in {calls} calls; {len(todo) - done} left (rerun to continue)")


if __name__ == "__main__":
    main()

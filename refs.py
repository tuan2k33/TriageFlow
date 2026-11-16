"""Fetch state of numbers referenced by open items but not open themselves (merged PR, closed issue...).

usage: python refs.py data/<owner>__<name>/repo.db
"""
import json, sqlite3, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

JQ = '{kind:(if .pull_request then "pr" else "issue" end),state:.state,merged:((.pull_request.merged_at // null) != null),title:.title,closed_at:.closed_at,state_reason:.state_reason}'


def fetch(a):
    repo, n = a
    for attempt in range(4):
        r = subprocess.run(["gh", "api", f"repos/{repo}/issues/{n}", "--jq", JQ], capture_output=True, text=True)
        if r.returncode == 0:
            return n, json.loads(r.stdout)
        if "404" in r.stderr or "410" in r.stderr:
            return n, None
        time.sleep(5 * 2 ** attempt)
    raise RuntimeError(f"{n}: {r.stderr.strip()}")


def main(path):
    db = sqlite3.connect(path)
    repo = db.execute("select v from meta where k='repo'").fetchone()[0]
    db.execute("create table if not exists refs(number integer primary key, kind text, state text, merged integer, title text, closed_at text, state_reason text)")
    todo = [r[0] for r in db.execute("""select distinct dst from links where dst not in (select number from items)
                                        and dst not in (select number from refs)""")]
    print(f"{len(todo)} to fetch", flush=True)
    with ThreadPoolExecutor(4) as ex:
        for i, (n, o) in enumerate(ex.map(fetch, [(repo, n) for n in todo]), 1):
            if o:
                db.execute("insert or replace into refs values(?,?,?,?,?,?,?)",
                           (n, o["kind"], o["state"], int(o["merged"]), o["title"], o["closed_at"], o["state_reason"]))
            if i % 100 == 0:
                db.commit(); print(f"  {i}/{len(todo)}", flush=True)
    db.commit()
    print(db.execute("select kind, state, merged, count(*) from refs group by 1,2,3").fetchall())


if __name__ == "__main__":
    main(sys.argv[1])

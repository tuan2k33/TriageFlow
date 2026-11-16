"""Crawl ALL closed issues/PRs (no comments) into table `closed`. Resumable: reruns fetch only what changed since.

usage: python closed.py data/<owner>__<name>/repo.db
"""
import json, sqlite3, subprocess, sys

JQ = ('.[] | {number, kind:(if .pull_request then "pr" else "issue" end), title, body, author:.user.login,'
      ' labels:([.labels[].name]|join(",")), milestone:.milestone.title, comments, created_at, closed_at, updated_at,'
      ' state_reason, merged:((.pull_request.merged_at // null) != null), url:.html_url}')


def crawl(db, repo):
    db.execute("""create table if not exists closed(number integer primary key, kind text, title text, body text, author text,
        labels text, milestone text, comments integer, created_at text, closed_at text, updated_at text,
        state_reason text, merged integer, url text)""")
    since = (db.execute("select v from meta where k='closed_since'").fetchone() or [None])[0]
    q = f"repos/{repo}/issues?state=closed&per_page=100&sort=updated&direction=asc" + (f"&since={since}" if since else "")
    print("since", since, flush=True)
    p = subprocess.Popen(["gh", "api", "--paginate", q, "--jq", JQ], stdout=subprocess.PIPE, text=True)
    n = 0
    last = since
    for line in p.stdout:
        o = json.loads(line)
        db.execute("insert or replace into closed values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            o["number"], o["kind"], o["title"], o["body"], o["author"], o["labels"], o["milestone"], o["comments"],
            o["created_at"], o["closed_at"], o["updated_at"], o["state_reason"], int(o["merged"]), o["url"]))
        last = o["updated_at"]
        n += 1
        if n % 1000 == 0:
            db.execute("insert or replace into meta values('closed_since', ?)", (last,))
            db.commit(); print(f"  {n}", flush=True)
    if p.wait() != 0:
        raise RuntimeError("gh failed; progress kept, rerun to resume")
    db.execute("insert or replace into meta values('closed_since', ?)", (last,))
    db.commit()
    print(f"fetched {n}")
    print(db.execute("select kind, state_reason, merged, count(*) from closed group by 1,2,3").fetchall())


def main(path):
    db = sqlite3.connect(path, timeout=120)
    crawl(db, db.execute("select v from meta where k='repo'").fetchone()[0])


if __name__ == "__main__":
    main(sys.argv[1])

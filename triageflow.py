"""Crawl all issues/PRs (open + closed) of a GitHub repo with their comments into SQLite. Content only, no code.

usage: python triageflow.py <repo url | owner/name> [--csv] [--full] [--no-comments] [--review-comments]
Reruns are incremental (GitHub `since` = updated_at) and resume after an interruption or rate limit.

Stages and request cost (100 rows per request):
  items     issues?state=all                   ~ N/100
  comments  issues/comments (whole repo)       ~ C/100   (issue + PR conversation comments)
  reviews   pulls/comments  (whole repo)       ~ R/30    (inline review comments; only with --review-comments)
  links     GraphQL closingIssuesReferences    ~ P/100   (PR -> issue it really closes)
"""
import argparse, csv, json, re, sqlite3, subprocess, sys, time
from pathlib import Path

SCHEMA = """
create table if not exists items(
  number integer primary key, kind text, title text, body text, author text, assoc text,
  state text, state_reason text, merged integer, draft integer, labels text, milestone text,
  comments integer, created_at text, closed_at text, updated_at text, url text);
create table if not exists comments(
  kind text, id integer, number integer, author text, assoc text, bot integer, body text,
  created_at text, updated_at text, primary key(kind, id));
create index if not exists comments_n on comments(number);
create table if not exists links(src integer, dst integer, kind text, primary key(src, dst, kind));
create table if not exists meta(k text primary key, v text);
"""

ITEM_JQ = ('.[] | {number, kind:(if .pull_request then "pr" else "issue" end), title, body, author:.user.login,'
           ' assoc:.author_association, state, state_reason, merged:((.pull_request.merged_at // null) != null),'
           ' draft:(.draft // false), labels:([.labels[].name]|join(",")), milestone:.milestone.title, comments,'
           ' created_at, closed_at, updated_at, url:.html_url}')
COMMENT_JQ = ('.[] | {id, number:(.issue_url|split("/")|last|tonumber), author:.user.login, assoc:.author_association,'
              ' bot:(.user.type=="Bot"), body, created_at, updated_at}')
REVIEW_JQ = ('.[] | {id, number:(.pull_request_url|split("/")|last|tonumber), author:.user.login, assoc:.author_association,'
             ' bot:(.user.type=="Bot"), body, created_at, updated_at}')

CLOSE = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+(?:[\w.-]+/[\w.-]+)?#(\d+)", re.I)
REF = re.compile(r"(?<![\w/])#(\d+)\b")


def parse_repo(s):
    m = re.search(r"(?:github\.com/)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", s.strip())
    if not m:
        sys.exit(f"bad repo: {s}")
    return m.group(1), m.group(2)


def rate():
    r = subprocess.run(["gh", "api", "rate_limit", "--jq", ".resources.core | [.remaining, .reset] | @tsv"],
                       capture_output=True, text=True)
    rem, reset = (int(x) for x in r.stdout.split())
    return rem, reset


def wait_budget(need=0):
    rem, reset = rate()
    if rem < max(need, 50):
        wait = max(0, reset - time.time()) + 5
        print(f"  rate limit low ({rem} left), sleeping {wait/60:.0f} min", flush=True)
        time.sleep(wait)


def stream(db, path, jq, meta_key, insert, label, full, per_page=100):
    """Stream a paginated listing sorted by updated asc, resumable via meta[meta_key]."""
    total, failures = 0, 0
    while True:
        since = None if full else (db.execute("select v from meta where k=?", (meta_key,)).fetchone() or [None])[0]
        q = f"{path}{'&' if '?' in path else '?'}per_page={per_page}&sort=updated&direction=asc" + (f"&since={since}" if since else "")
        p = subprocess.Popen(["gh", "api", "--paginate", q, "--jq", jq], stdout=subprocess.PIPE, text=True)
        n, last, bad = 0, None, False
        for line in p.stdout:
            try:
                o = json.loads(line)
                o["updated_at"]
            except (ValueError, KeyError, TypeError):  # gh prints the error body on a 5xx mid-stream
                bad = True
                p.terminate()
                break
            insert(o)
            n += 1
            total += 1
            last = o["updated_at"]
            if n % 2000 == 0:
                db.execute("insert or replace into meta values(?,?)", (meta_key, last))
                db.commit()
                print(f"  {label}: {total}", flush=True)
        ok = p.wait() == 0 and not bad
        if last:
            db.execute("insert or replace into meta values(?,?)", (meta_key, last))
        db.commit()
        if ok and n >= 300 * per_page - 100:  # GitHub stops a listing at 300 pages: continue from the last updated_at
            print(f"  {label}: {total} (page cap reached, continuing)", flush=True)
            full = False
            continue
        if ok:
            print(f"  {label}: {total} fetched", flush=True)
            return total
        failures += 1
        if rate()[0] < 50:
            wait_budget()
        elif failures > 6:
            raise RuntimeError(f"gh failed on {path} (progress kept, rerun to resume)")
        else:
            print(f"  gh error on {label}, retry {failures}/6 in {30 * failures}s", flush=True)
            time.sleep(30 * failures)
        full = False


def official_links(db, owner, name):
    """PR -> issues it closes, as GitHub itself records them (sidebar + keywords)."""
    q = ("query($o:String!,$n:String!,$c:String){repository(owner:$o,name:$n){pullRequests(first:100,after:$c,"
         "orderBy:{field:UPDATED_AT,direction:DESC},states:[OPEN,MERGED]){pageInfo{hasNextPage endCursor}"
         "nodes{number updatedAt closingIssuesReferences(first:10){nodes{number repository{nameWithOwner}}}}}}}")
    since = (db.execute("select v from meta where k='links_since'").fetchone() or [""])[0]
    cursor, newest, n, pages = None, None, 0, 0
    while True:
        cmd = ["gh", "api", "graphql", "-f", f"query={q}", "-f", f"o={owner}", "-f", f"n={name}"] + (["-f", f"c={cursor}"] if cursor else [])
        for attempt in range(6):
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0:
                break
            print(f"  graphql error ({r.stderr.strip()[:80]}), retry {attempt + 1}/6", flush=True)
            time.sleep(15 * (attempt + 1))
        else:
            raise RuntimeError(r.stderr.strip())
        prs = json.loads(r.stdout)["data"]["repository"]["pullRequests"]
        pages += 1
        stop = False
        for pr in prs["nodes"]:
            newest = newest or pr["updatedAt"]
            if pr["updatedAt"] < since:
                stop = True
                break
            db.execute("delete from links where src=? and kind='closes_official'", (pr["number"],))
            for i in pr["closingIssuesReferences"]["nodes"]:
                if i["repository"]["nameWithOwner"].lower() == f"{owner}/{name}".lower():
                    db.execute("insert or ignore into links values(?,?,'closes_official')", (pr["number"], i["number"]))
                    n += 1
        if stop or not prs["pageInfo"]["hasNextPage"]:
            break
        cursor = prs["pageInfo"]["endCursor"]
    if newest:
        db.execute("insert or replace into meta values('links_since', ?)", (newest,))
    db.commit()
    print(f"  links: {pages} pages, {n} official closes", flush=True)


def text_links(db):
    """closes/mentions found in the text of items and comments, only between known numbers."""
    links = set()

    def add(src, text):
        text = text or ""
        closes = {int(x) for x in CLOSE.findall(text)}
        links.update((src, k, "closes") for k in closes)
        links.update((src, k, "mentions") for k in {int(x) for x in REF.findall(text)} - closes)

    for n, t, b in db.execute("select number, title, body from items"):
        add(n, f"{t}\n{b}")
    for n, b in db.execute("select number, body from comments"):
        add(n, b)
    known = {r[0] for r in db.execute("select number from items")}
    rows = [(s, d, k) for s, d, k in links if s != d and d in known]
    db.execute("delete from links where kind in ('closes','mentions')")
    db.executemany("insert or ignore into links values(?,?,?)", rows)
    db.commit()
    print(f"  text links: {len(rows)}", flush=True)


def rebuild_fts(db):
    db.execute("drop table if exists fts")
    db.execute("create virtual table fts using fts5(title, body)")
    db.execute("""insert into fts(rowid, title, body)
        select i.number, i.title, coalesce(i.body,'') || ' ' || coalesce((select group_concat(body,' ') from comments c where c.number=i.number),'')
        from items i""")
    db.commit()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--csv", action="store_true", help="also export items/comments/links csv")
    ap.add_argument("--full", action="store_true", help="ignore previous sync, refetch everything")
    ap.add_argument("--no-comments", action="store_true", help="skip the comment stages")
    ap.add_argument("--review-comments", action="store_true", help="also fetch inline PR review comments (many requests, low value, off by default)")
    a = ap.parse_args()
    owner, name = parse_repo(a.repo)
    outdir = Path("data") / f"{owner}__{name}"
    outdir.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(outdir / "repo.db", timeout=120)
    db.executescript(SCHEMA)
    db.execute("insert or replace into meta values('repo', ?)", (f"{owner}/{name}",))
    base = f"repos/{owner}/{name}"

    def put_item(o):
        db.execute("insert or replace into items values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            o["number"], o["kind"], o["title"], o["body"], o["author"], o["assoc"], o["state"], o["state_reason"],
            int(o["merged"]), int(o["draft"]), o["labels"], o["milestone"], o["comments"], o["created_at"],
            o["closed_at"], o["updated_at"], o["url"]))

    def put_comment(kind):
        def f(o):
            db.execute("insert or replace into comments values(?,?,?,?,?,?,?,?,?)", (
                kind, o["id"], o["number"], o["author"], o["assoc"], int(o["bot"]), o["body"], o["created_at"], o["updated_at"]))
        return f

    print("items:", flush=True)
    wait_budget(400)
    stream(db, f"{base}/issues?state=all", ITEM_JQ, "items_since", put_item, "items", a.full)
    if not a.no_comments:
        print("comments:", flush=True)
        wait_budget(300)
        stream(db, f"{base}/issues/comments", COMMENT_JQ, "comments_since", put_comment("comment"), "comments", a.full)
        if a.review_comments:
            try:  # this endpoint often answers 502 on big repos; smaller pages help
                stream(db, f"{base}/pulls/comments", REVIEW_JQ, "reviews_since", put_comment("review_comment"), "review comments", a.full, per_page=30)
            except RuntimeError as e:
                print(f"  WARNING: review comments incomplete ({e}); rerun to continue", flush=True)
    print("links:", flush=True)
    wait_budget(200)
    official_links(db, owner, name)
    text_links(db)
    rebuild_fts(db)

    if a.csv:
        for t in ("items", "comments", "links"):
            cur = db.execute(f"select * from {t}")
            with open(outdir / f"{t}.csv", "w", newline="") as f:
                w = csv.writer(f)
                w.writerow([d[0] for d in cur.description])
                w.writerows(cur)
    counts = [db.execute(f"select count(*) from {t}").fetchone()[0] for t in ("items", "comments", "links")]
    n_open = db.execute("select count(*) from items where state='open'").fetchone()[0]
    print(f"done -> {outdir/'repo.db'}  items={counts[0]} (open {n_open}) comments={counts[1]} links={counts[2]}")


if __name__ == "__main__":
    main()

"""Crawl all issues/PRs (open + closed) of a GitHub repo with their comments into SQLite. Content only, no code.

usage: python triageflow.py <repo url | owner/name> [--csv] [--full] [--no-comments] [--review-comments]
Reruns are incremental (GitHub `since` = updated_at, plus an ETag on the first page, so "nothing new" costs no quota)
and resume after an interruption or rate limit. Talks to the GitHub REST/GraphQL API directly; the token comes from `gh auth token`.

Stages and request cost (100 rows per request):
  items     issues?state=all                   ~ N/100
  comments  issues/comments (whole repo)       ~ C/100   (issue + PR conversation comments)
  reviews   pulls/comments  (whole repo)       ~ R/30    (inline review comments; only with --review-comments)
  links     GraphQL, PR side                   ~ P/100   (PR -> issue it really closes)
            GraphQL, issue side                ~ I/100   (closing PRs incl. unmerged ones, marked duplicates, sub-issues)
            text of items and comments         0         (#N, gh-N and same-repo URLs: closes / mentions)
"""
import argparse, collections, csv, json, re, sqlite3, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

API = "https://api.github.com"

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

# a reference to another item of the same repo: #12, gh-12 (numpy's habit, GitHub autolinks it too) or its full URL
NUM = r"(?:(?<![\w/])(?:#|gh-)|github\.com/{repo}/(?:issues|pull)/)(\d+)\b"
CLOSE = r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?):?\s+(?:https?://)?" + NUM


class GitHub:
    """Minimal GitHub API client: auth from gh, rate-limit aware, retries 5xx and network errors."""

    def __init__(self):
        self.token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
        self.requests = 0

    def call(self, url, body=None, etag=None):
        """-> (status, json or None, headers). 304 is returned, not raised."""
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "triageflow"}
        if etag:
            headers["If-None-Match"] = etag
        data = json.dumps(body).encode() if body is not None else None
        for attempt in range(8):
            req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
            try:
                self.requests += 1
                with urllib.request.urlopen(req, timeout=90) as r:
                    out = json.load(r)
                    self._pace(r.headers)
                    return r.status, out, r.headers
            except urllib.error.HTTPError as e:
                if e.code == 304:
                    return 304, None, e.headers
                if e.code in (403, 429) and (e.headers.get("retry-after") or e.headers.get("x-ratelimit-remaining") == "0"):
                    wait = int(e.headers.get("retry-after") or max(0, int(e.headers.get("x-ratelimit-reset", time.time())) - time.time()) + 5)
                    print(f"  rate limited, sleeping {wait / 60:.1f} min", flush=True)
                    time.sleep(wait)
                    continue
                if e.code < 500:
                    raise RuntimeError(f"HTTP {e.code} on {url}: {e.read()[:200]!r}")
                print(f"  HTTP {e.code}, retry {attempt + 1}", flush=True)
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                print(f"  {type(e).__name__}: {str(e)[:80]}, retry {attempt + 1}", flush=True)
            time.sleep(min(300, 15 * 2 ** attempt))
        raise RuntimeError(f"giving up on {url}")

    @staticmethod
    def _pace(h):
        """Sleep until reset when the quota is about to run out, instead of hitting the wall."""
        rem = h.get("x-ratelimit-remaining")
        if rem is not None and int(rem) < 20:
            wait = max(0, int(h.get("x-ratelimit-reset", 0)) - time.time()) + 5
            print(f"  {rem} requests left, sleeping {wait / 60:.0f} min", flush=True)
            time.sleep(wait)

    def graphql(self, query, **variables):
        _, out, _ = self.call(f"{API}/graphql", {"query": query, "variables": variables})
        if out.get("errors"):
            raise RuntimeError(f"GraphQL: {out['errors']}")
        return out["data"]


def next_link(headers):
    m = re.search(r'<([^>]+)>;\s*rel="next"', headers.get("link") or "")
    return m.group(1) if m else None


def parse_repo(s):
    m = re.search(r"(?:github\.com/)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", s.strip())
    if not m:
        sys.exit(f"bad repo: {s}")
    return m.group(1), m.group(2)


def login(u):
    return (u or {}).get("login")


def item_row(o):
    pr = o.get("pull_request")
    return (o["number"], "pr" if pr else "issue", o["title"], o["body"], login(o.get("user")), o.get("author_association"),
            o["state"], o.get("state_reason"), int(bool(pr and pr.get("merged_at"))), int(bool(o.get("draft"))),
            ",".join(l["name"] for l in o.get("labels") or []), (o.get("milestone") or {}).get("title"),
            o.get("comments"), o["created_at"], o.get("closed_at"), o["updated_at"], o["html_url"])


def comment_row(kind, url_key):
    def f(o):
        return (kind, o["id"], int(o[url_key].rsplit("/", 1)[1]), login(o.get("user")), o.get("author_association"),
                int((o.get("user") or {}).get("type") == "Bot"), o.get("body"), o["created_at"], o["updated_at"])
    return f


def meta_get(db, k):
    return (db.execute("select v from meta where k=?", (k,)).fetchone() or [None])[0]


def stream(gh, db, path, table, row, meta_key, label, full, per_page=100):
    """Page through a listing sorted by updated asc, resumable via meta[meta_key] (= last updated_at stored).

    `since` is inclusive, so a rerun always gets at least the last row back; the first page's ETag is stored together
    with the `since` it was fetched with, and sent again only for that same `since` (unchanged data -> 304, free)."""
    total = 0
    while True:
        since = None if full else meta_get(db, meta_key)
        params = {"per_page": per_page, "sort": "updated", "direction": "asc"} | ({"since": since} if since else {})
        url = f"{API}/{path}{'&' if '?' in path else '?'}{urllib.parse.urlencode(params)}"
        saved = (meta_get(db, meta_key + "_etag") or "|").split("|", 1)
        etag = saved[1] if since and saved[0] == since else None
        n, last, first_etag = 0, None, None
        while url:
            status, page, h = gh.call(url, etag=etag if first_etag is None else None)
            if status == 304:
                print(f"  {label}: nothing new", flush=True)
                return total
            first_etag = first_etag or h.get("etag") or ""
            for o in page:
                r = row(o)
                db.execute(f"insert or replace into {table} values({','.join('?' * len(r))})", r)
                last = o["updated_at"]
            n += len(page)
            total += len(page)
            if n and n % 2000 < len(page):
                db.execute("insert or replace into meta values(?,?)", (meta_key, last))
                db.commit()
                print(f"  {label}: {total}", flush=True)
            url = next_link(h)
        if last:
            db.execute("insert or replace into meta values(?,?)", (meta_key, last))
        if last == since:  # only the inclusive row came back: this url will be asked again next time
            db.execute("insert or replace into meta values(?,?)", (meta_key + "_etag", f"{since}|{first_etag}"))
        db.commit()
        if n >= 300 * per_page - per_page:  # GitHub stops a listing at 300 pages: continue from the last updated_at
            print(f"  {label}: {total} (page cap reached, continuing)", flush=True)
            full = False
            continue
        print(f"  {label}: {total} fetched", flush=True)
        return total


def official_links(gh, db, owner, name):
    """PR -> issues it closes, as GitHub itself records them (sidebar + keywords)."""
    q = ("query($o:String!,$n:String!,$c:String){repository(owner:$o,name:$n){pullRequests(first:100,after:$c,"
         "orderBy:{field:UPDATED_AT,direction:DESC},states:[OPEN,MERGED]){pageInfo{hasNextPage endCursor}"
         "nodes{number updatedAt closingIssuesReferences(first:10){nodes{number repository{nameWithOwner}}}}}}}")
    since = (db.execute("select v from meta where k='links_since'").fetchone() or [""])[0]
    cursor, newest, n, pages = None, None, 0, 0
    while True:
        prs = gh.graphql(q, o=owner, n=name, c=cursor)["repository"]["pullRequests"]
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


def issue_links(gh, db, owner, name):
    """What GitHub records on the issue side: marked as duplicate of, sub-issue of, and every PR set to close it
    (also PRs closed without merging, which the PR-side listing above skips)."""
    ref = "... on Issue{number} ... on PullRequest{number}"
    q = ("query($o:String!,$n:String!,$c:String){repository(owner:$o,name:$n){issues(first:100,after:$c,"
         "orderBy:{field:UPDATED_AT,direction:DESC}){pageInfo{hasNextPage endCursor}nodes{number updatedAt parent{number repository{nameWithOwner}}"
         "closedByPullRequestsReferences(first:10,includeClosedPrs:true){nodes{number repository{nameWithOwner}}}"
         "timelineItems(first:10,itemTypes:[MARKED_AS_DUPLICATE_EVENT,UNMARKED_AS_DUPLICATE_EVENT]){nodes{__typename "
         "... on MarkedAsDuplicateEvent{isCrossRepository canonical{%s} duplicate{%s}}"
         "... on UnmarkedAsDuplicateEvent{isCrossRepository canonical{%s} duplicate{%s}}}}}}}}" % (ref, ref, ref, ref))
    here = f"{owner}/{name}".lower()
    local = lambda x: x and x["repository"]["nameWithOwner"].lower() == here
    since = (db.execute("select v from meta where k='issue_links_since'").fetchone() or [""])[0]
    cursor, newest, n, pages = None, None, collections.Counter(), 0
    while True:
        page = gh.graphql(q, o=owner, n=name, c=cursor)["repository"]["issues"]
        pages += 1
        stop = False
        for i in page["nodes"]:
            newest = newest or i["updatedAt"]
            if i["updatedAt"] < since:
                stop = True
                break
            num = i["number"]
            db.execute("delete from links where src=? and kind='sub_issue'", (num,))
            db.execute("delete from links where dst=? and kind='closes_official'", (num,))
            rows = {(p["number"], num, "closes_official") for p in i["closedByPullRequestsReferences"]["nodes"] if local(p)}
            if local(i["parent"]):
                rows.add((num, i["parent"]["number"], "sub_issue"))
            dup, undone = set(), set()  # the event sits on either issue's timeline and names both ends
            for e in i["timelineItems"]["nodes"]:  # in time order: a later "unmarked" takes the mark back
                d, c = (e.get("duplicate") or {}).get("number"), (e.get("canonical") or {}).get("number")
                if d and c and d != c and not e["isCrossRepository"]:
                    marked = e["__typename"] == "MarkedAsDuplicateEvent"
                    (dup.add if marked else dup.discard)((d, c, "duplicate_of"))
                    (undone.discard if marked else undone.add)((d, c))
            db.executemany("delete from links where src=? and dst=? and kind='duplicate_of'", undone)
            rows |= dup
            db.executemany("insert or ignore into links values(?,?,?)", rows)
            n.update(k for _, _, k in rows)
        db.commit()
        if stop or not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
        if pages % 20 == 0:
            print(f"  issue links: {pages} pages", flush=True)
    if newest:
        db.execute("insert or replace into meta values('issue_links_since', ?)", (newest,))
    db.commit()
    print(f"  issue links: {pages} pages, " + ", ".join(f"{v} {k}" for k, v in n.items()), flush=True)


def text_links(db, owner, name):
    """closes/mentions found in the text of items and comments, only between known numbers."""
    links = set()
    repo = re.escape(f"{owner}/{name}")
    CLOSE_RX, REF = re.compile(CLOSE.replace("{repo}", repo), re.I), re.compile(NUM.replace("{repo}", repo), re.I)

    def add(src, text):
        text = text or ""
        closes = {int(x) for x in CLOSE_RX.findall(text)}
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
    outdir = Path(__file__).parent / "data" / f"{owner}__{name}"
    outdir.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(outdir / "repo.db", timeout=120)
    db.executescript(SCHEMA)
    db.execute("insert or replace into meta values('repo', ?)", (f"{owner}/{name}",))
    gh = GitHub()
    base = f"repos/{owner}/{name}"
    t0 = time.time()

    print("items:", flush=True)
    stream(gh, db, f"{base}/issues?state=all", "items", item_row, "items_since", "items", a.full)
    if not a.no_comments:
        print("comments:", flush=True)
        stream(gh, db, f"{base}/issues/comments", "comments", comment_row("comment", "issue_url"), "comments_since", "comments", a.full)
        if a.review_comments:
            try:  # this endpoint often answers 502 on big repos; smaller pages help
                stream(gh, db, f"{base}/pulls/comments", "comments", comment_row("review_comment", "pull_request_url"),
                       "reviews_since", "review comments", a.full, per_page=30)
            except RuntimeError as e:
                print(f"  WARNING: review comments incomplete ({e}); rerun to continue", flush=True)
    print("links:", flush=True)
    official_links(gh, db, owner, name)
    issue_links(gh, db, owner, name)
    text_links(db, owner, name)
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
    print(f"done -> {outdir/'repo.db'}  items={counts[0]} (open {n_open}) comments={counts[1]} links={counts[2]}"
          f"  [{gh.requests} requests, {time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()

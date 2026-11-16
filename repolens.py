"""Crawl open issues/PRs of a GitHub repo into SQLite (content only, no code).

usage: python repolens.py <repo url | owner/name> [--csv]
"""
import argparse, csv, json, re, sqlite3, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCHEMA = """
create table if not exists items(
  number integer primary key, kind text, title text, body text, author text,
  state text, draft integer, labels text, milestone text, comments integer,
  created_at text, updated_at text, url text);
create table if not exists comments(
  id integer primary key, number integer, kind text, author text, body text, created_at text);
create table if not exists links(src integer, dst integer, kind text, primary key(src,dst,kind));
create table if not exists meta(k text primary key, v text);
create index if not exists comments_n on comments(number);
"""


def gh(path):
    for attempt in range(5):
        r = subprocess.run(["gh", "api", "--paginate", path, "--jq", ".[]"], capture_output=True, text=True)
        if r.returncode == 0:
            return [json.loads(l) for l in r.stdout.splitlines() if l.strip()]
        time.sleep(5 * 2 ** attempt)
    raise RuntimeError(f"{path}: {r.stderr.strip()}")


def parse_repo(s):
    m = re.search(r"(?:github\.com/)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", s.strip())
    if not m:
        sys.exit(f"bad repo: {s}")
    return m.group(1), m.group(2)


CLOSE = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+(?:[\w.-]+/[\w.-]+)?#(\d+)", re.I)
REF = re.compile(r"(?<![\w/])#(\d+)\b")


def extract_links(src, text, out):
    text = text or ""
    closes = set(int(n) for n in CLOSE.findall(text))
    for n in closes:
        out.add((src, n, "closes"))
    for n in set(int(n) for n in REF.findall(text)) - closes:
        out.add((src, n, "mentions"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--csv", action="store_true", help="also export items.csv / comments.csv")
    ap.add_argument("--full", action="store_true", help="ignore previous sync, refetch everything")
    a = ap.parse_args()
    owner, name = parse_repo(a.repo)
    base = f"repos/{owner}/{name}"
    outdir = Path("data") / f"{owner}__{name}"
    outdir.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(outdir / "repo.db")
    db.executescript(SCHEMA)

    old = {n: u for n, u in db.execute("select number, updated_at from items")} if not a.full else {}

    rows = gh(f"{base}/issues?state=open&per_page=100")
    print(f"open items: {len(rows)}", flush=True)
    seen = set()
    todo = []
    for r in rows:
        n = r["number"]
        seen.add(n)
        is_pr = "pull_request" in r
        row = (n, "pr" if is_pr else "issue", r["title"], r["body"], (r["user"] or {}).get("login"),
               r["state"], int(bool(r.get("draft"))), ",".join(l["name"] for l in r["labels"]),
               (r["milestone"] or {}).get("title"), r["comments"], r["created_at"], r["updated_at"], r["html_url"])
        if old.get(n) != r["updated_at"]:
            todo.append((n, is_pr, r["comments"], row))
        else:
            db.execute("insert or replace into items values(?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
    # drop items no longer open (closed/merged since last sync)
    for n in set(old) - seen:
        for t in ("items", "comments"):
            db.execute(f"delete from {t} where number=?", (n,))
        db.execute("delete from links where src=?", (n,))

    def fetch(t):
        n, is_pr, nc, row = t
        cs = []
        if nc:
            cs += [("comment", c) for c in gh(f"{base}/issues/{n}/comments?per_page=100")]
        if is_pr:
            cs += [("review", c) for c in gh(f"{base}/pulls/{n}/reviews?per_page=100") if c.get("body")]
            cs += [("review_comment", c) for c in gh(f"{base}/pulls/{n}/comments?per_page=100")]
        return n, cs, row

    print(f"fetching comments for {len(todo)} changed items", flush=True)
    with ThreadPoolExecutor(4) as ex:
        for i, (n, cs, row) in enumerate(ex.map(fetch, todo), 1):
            db.execute("delete from comments where number=?", (n,))
            db.execute("insert or replace into items values(?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
            for kind, c in cs:
                db.execute("insert or replace into comments values(?,?,?,?,?,?)", (
                    c["id"], n, kind, (c.get("user") or {}).get("login"), c["body"],
                    c.get("created_at") or c.get("submitted_at")))
            if i % 100 == 0:
                print(f"  {i}/{len(todo)}", flush=True)
                db.commit()

    # links + fts rebuilt from scratch (cheap)
    links = set()
    for n, title, body in db.execute("select number, title, body from items"):
        extract_links(n, f"{title}\n{body}", links)
    for n, body in db.execute("select number, body from comments"):
        extract_links(n, body, links)
    links = {l for l in links if l[0] != l[1]}
    db.execute("delete from links")
    db.executemany("insert into links values(?,?,?)", links)
    db.execute("drop table if exists fts")
    db.execute("create virtual table fts using fts5(title, body)")
    db.execute("""insert into fts(rowid, title, body)
        select i.number, i.title, coalesce(i.body,'') || ' ' || coalesce((select group_concat(body,' ') from comments c where c.number=i.number),'')
        from items i""")
    db.execute("insert or replace into meta values('repo', ?)", (f"{owner}/{name}",))
    db.commit()

    if a.csv:
        for t in ("items", "comments", "links"):
            cur = db.execute(f"select * from {t}")
            with open(outdir / f"{t}.csv", "w", newline="") as f:
                w = csv.writer(f)
                w.writerow([d[0] for d in cur.description])
                w.writerows(cur)
    n_i, n_c, n_l = (db.execute(f"select count(*) from {t}").fetchone()[0] for t in ("items", "comments", "links"))
    print(f"done -> {outdir/'repo.db'}  items={n_i} comments={n_c} links={n_l}")


if __name__ == "__main__":
    main()

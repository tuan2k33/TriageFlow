"""Local web view of the results: paste a repo link, then browse its four outputs (items, report, actions, database).

usage: python web.py [port]      ->  http://127.0.0.1:8000

Listens on 127.0.0.1 only. The database page opens repo.db read-only; nothing here writes to GitHub.
"""
import html, re, sqlite3, subprocess, sys, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
REPO = re.compile(r"^[\w.-]+__[\w.-]+$")
PAGES = (("browse", "Browse"), ("report", "Report"), ("actions", "Actions"), ("db", "Database"))
running = {}  # repo dir name -> Popen of run.py
CSS = """<style>
:root{--bg:#fafaf8;--panel:#fff;--ink:#1c1c1a;--mute:#6b6b66;--line:#e2e2dc}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--panel:#1c1c1c;--ink:#e8e8e3;--mute:#9a9a94;--line:#2c2c2a}}
*{box-sizing:border-box}html,body{height:100%;margin:0}body{background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,sans-serif;display:flex;flex-direction:column}
nav{display:flex;gap:4px;align-items:center;padding:6px 12px;background:var(--panel);border-bottom:1px solid var(--line);flex:none}
nav a{padding:4px 12px;border-radius:6px;color:var(--mute);text-decoration:none}nav a.on{background:var(--bg);color:var(--ink);font-weight:600}nav b{margin-right:12px}
main{padding:16px 20px;overflow:auto;flex:1}iframe{border:0;flex:1;width:100%}
table{border-collapse:collapse;margin:8px 0 20px}td,th{border:1px solid var(--line);padding:3px 8px;text-align:left;vertical-align:top;max-width:620px;overflow-wrap:break-word}th{background:var(--panel)}
summary{cursor:pointer;margin:14px 0 6px}table.rep{table-layout:fixed;width:100%}table.rep td,table.rep th{max-width:none}table.rep th:nth-child(1){width:30%}table.rep th:nth-child(2){width:20%}
a{color:inherit}pre{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px;overflow:auto}
input[type=text],textarea{width:min(720px,100%);padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink);font:inherit}
button{padding:6px 14px;border:1px solid var(--line);border-radius:6px;background:var(--ink);color:var(--bg);font:inherit;cursor:pointer}.mute{color:var(--mute)}
</style>"""


def page(title, body, repo=None, on=None, raw=False):
    nav = '<nav><b><a href="/" style="color:inherit;padding:0">TriageFlow</a></b>'
    if repo:
        nav += f"<span class=mute>{html.escape(repo.replace('__', '/'))}</span>" + "".join(
            f'<a class="{"on" if k == on else ""}" href="/r/{repo}/{k}">{t}</a>' for k, t in PAGES)
    return (f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title>"
            f"{CSS}{nav}</nav>{body if raw else '<main>' + body + '</main>'}").encode()


def md_to_html(md):
    """Enough Markdown for report.md: headings, paragraphs, tables, [text](url) links, **bold**, `code`, - and 1. lists."""
    link = lambda t: re.sub(r"`([^`]+)`", r"<code>\1</code>", re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>",
                            re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank">\1</a>', html.escape(t))))
    out, table = [], False
    for line in md.split("\n"):
        if line.startswith("<"):  # report.py writes its tables as HTML (fixed column widths); it is our own file
            out.append(line)
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            out.append(("<table class=rep>" if not table else "") + "<tr>" + "".join(f"<{'td' if table else 'th'}>{link(c)}</{'td' if table else 'th'}>" for c in cells) + "</tr>")
            table = True
            continue
        if table:
            out.append("</table>")
            table = False
        m = re.match(r"(#+) (.*)", line)
        if not m and re.match(r"(- |\d+\. )", line):
            out.append(f"<p style='margin:2px 0 2px 16px'>{link(re.sub(r'^- ', '• ', line))}</p>")
            continue
        out.append(f"<h{len(m.group(1))}>{link(m.group(2))}</h{len(m.group(1))}>" if m else f"<p>{link(line)}</p>" if line.strip() else "")
    return "\n".join(out) + ("</table>" if table else "")


def rows_table(cur):
    cols = [d[0] for d in cur.description]
    cell = lambda v: f"<span class=mute>blob {len(v)} bytes</span>" if isinstance(v, bytes) else html.escape(str(v)[:300]) if v is not None else ""
    return ("<table><tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in cols) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{cell(v)}</td>" for v in r) + "</tr>" for r in cur.fetchmany(200)) + "</table>")


def db_page(repo, q):
    db = sqlite3.connect(f"file:{DATA / repo / 'repo.db'}?mode=ro", uri=True, timeout=30)
    tables = [r[0] for r in db.execute("select name from sqlite_master where type='table' and name not like 'fts%' order by 1")]
    sql = q.get("sql", [""])[0].strip() or (f'select * from "{q["t"][0]}" limit 200' if q.get("t", [""])[0] in tables else "")
    body = "<h2>Database</h2><p>" + " · ".join(
        f'<a href="?t={t}">{t}</a> <span class=mute>{db.execute(f"select count(*) from [{t}]").fetchone()[0]}</span>' for t in tables) + "</p>"
    body += (f'<form><textarea name=sql rows=3 placeholder="select ... (read-only, first 200 rows shown)">{html.escape(sql)}</textarea><br><button>Run</button></form>')
    if sql:
        try:
            body += rows_table(db.execute(sql))
        except sqlite3.Error as e:
            body += f"<pre>{html.escape(str(e))}</pre>"
    return body


def home():
    body = ('<h2>Analyze a repository</h2><form method=post action=/run><input type=text name=link placeholder="https://github.com/owner/name"> '
            "<button>Run</button></form><p class=mute>Crawls every issue and PR, then builds the browse page and the report. A rerun only syncs what changed.</p><h2>Repositories</h2>")
    rows = ""
    for d in sorted(p for p in DATA.iterdir() if REPO.match(p.name) and (p / "repo.db").exists()):
        state = "running, <a href='/r/%s/log'>log</a>" % d.name if d.name in running and running[d.name].poll() is None else ""
        n = ""
        if (d / "browse.html").exists():
            db = sqlite3.connect(f"file:{d / 'repo.db'}?mode=ro", uri=True, timeout=30)
            n = "%d items, %d open" % db.execute("select count(*), sum(state='open') from items").fetchone()
        rows += f"<tr><td><a href='/r/{d.name}/browse'>{html.escape(d.name.replace('__', '/'))}</a></td><td>{n}</td><td>{state}</td></tr>"
    return body + (f"<table><tr><th>Repository</th><th>Size</th><th></th></tr>{rows}</table>" if rows else "<p class=mute>None yet.</p>")


class Handler(BaseHTTPRequestHandler):
    def send(self, body, ctype="text/html; charset=utf-8", code=200, headers=()):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        parts = [p for p in u.path.split("/") if p]
        if not parts:
            return self.send(page("TriageFlow", home()))
        if len(parts) != 3 or parts[0] != "r" or not REPO.match(parts[1]):
            return self.send(page("Not found", "<p>Not found.</p>"), code=404)
        repo, what = parts[1], parts[2]
        d = DATA / repo
        if what == "log":
            log = (d / "run.log").read_text(errors="replace") if (d / "run.log").exists() else ""
            busy = repo in running and running[repo].poll() is None
            body = (f"<h2>{'Running' if busy else 'Finished'}</h2><pre>{html.escape(log[-6000:])}</pre>"
                    + ("<script>setTimeout(()=>location.reload(),3000)</script>" if busy else f"<p><a href='/r/{repo}/browse'>Open the results</a></p>"))
            return self.send(page("Run log", body, repo))
        if what == "browse.html" and (d / "browse.html").exists():
            return self.send((d / "browse.html").read_bytes())
        if what == "actions.sh" and (d / "actions.sh").exists():
            return self.send((d / "actions.sh").read_bytes(), "text/plain; charset=utf-8", headers=[("Content-Disposition", "attachment; filename=actions.sh")])
        if not (d / "repo.db").exists():
            return self.send(page("Not found", "<p>No such repository yet.</p>"), code=404)
        if what == "browse":
            return self.send(page(repo, f'<iframe src="/r/{repo}/browse.html"></iframe>', repo, what, raw=True))
        if what == "report":
            md = (d / "report.md").read_text(encoding="utf-8") if (d / "report.md").exists() else "No report yet: run report.py."
            return self.send(page("Report", md_to_html(md), repo, what))
        if what == "actions":
            sh = (d / "actions.sh").read_text(encoding="utf-8") if (d / "actions.sh").exists() else "No actions yet: run report.py."
            body = (f"<h2>Proposed gh commands</h2><p class=mute>Every line is commented out. Download, remove the leading '# ' from the lines you agree with, then run it yourself. "
                    f"<a href='/r/{repo}/actions.sh'>Download actions.sh</a></p><pre>{html.escape(sh)}</pre>")
            return self.send(page("Actions", body, repo, what))
        if what == "db":
            return self.send(page("Database", db_page(repo, q), repo, what))
        self.send(page("Not found", "<p>Not found.</p>"), code=404)

    def do_POST(self):
        if self.headers.get("Host", "").split(":")[0] not in ("127.0.0.1", "localhost"):  # no other site may start a crawl
            return self.send(b"", code=403)
        if self.path != "/run":
            return self.send(b"", code=404)
        link = urllib.parse.parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()).get("link", [""])[0]
        m = re.search(r"(?:github\.com/)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", link.strip())
        if not m:
            return self.send(page("Bad link", "<p>That does not look like a GitHub repository link.</p>"), code=400)
        repo = f"{m.group(1)}__{m.group(2)}"
        if not (repo in running and running[repo].poll() is None):
            (DATA / repo).mkdir(exist_ok=True)
            log = open(DATA / repo / "run.log", "w")
            running[repo] = subprocess.Popen([sys.executable, "-u", str(HERE / "run.py"), f"{m.group(1)}/{m.group(2)}"], stdout=log, stderr=subprocess.STDOUT, cwd=HERE)
        self.send(b"", code=303, headers=[("Location", f"/r/{repo}/log")])

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"http://127.0.0.1:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()

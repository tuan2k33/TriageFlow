"""Offline checks: no network, no model. A small synthetic repo with planted cases goes through analyze, suggest,
report and build_html; plus the text-link patterns.

run: python -m pytest tests -q      (or: python tests/test_flow.py)
"""
import hashlib, json, re, sqlite3, sys, tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
import analyze, build_html, report, suggest, triageflow, web


def make_db(path):
    """6 topics; issues 1..60, PRs 101..120. Planted: 1~2 duplicates, 3 fixed by unlinked merged PR 103,
    4 has a merged closing PR 104, PRs 105 and 106 both close 5, 7 is marked duplicate of 6 on GitHub."""
    rng = np.random.default_rng(0)
    centers = rng.normal(size=(6, 384))
    db = sqlite3.connect(path)
    db.executescript(triageflow.SCHEMA)
    db.execute("insert into meta values('repo', 'acme/demo')")
    db.execute("create table emb(number integer primary key, vec blob, hash text)")
    vecs = {}

    def add(n, kind, topic, state="open", merged=0, labels=(), like=None, day=1, author="ann"):
        title, body = f"{kind} {n} about topic {topic}", f"details of {n}"
        v = vecs[like] + rng.normal(scale=0.01, size=384) if like else centers[topic] + rng.normal(scale=0.6, size=384)
        vecs[n] = v
        db.execute("insert into items values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (n, kind, title, body, author, "NONE", state, None, merged, 0, json.dumps(list(labels)), None, 2,
                    f"2024-01-{day:02d}T00:00:00Z", None, f"2024-02-{day:02d}T00:00:00Z", f"https://github.com/acme/demo/issues/{n}"))
        db.execute("insert into emb values(?,?,?)", (n, (v / np.linalg.norm(v)).astype(np.float16).tobytes(),
                                                     hashlib.md5("\n".join([analyze.EMB_VERSION, title, body]).encode()).hexdigest()))

    for n in range(1, 61):
        topic = n % 6
        add(n, "issue", topic, state="open" if n <= 30 else "closed", labels=[f"area: t{topic}"] if n > 12 else [], day=1 + n % 20,
            like=1 if n == 2 else None)
    for n in range(101, 121):
        topic = {103: 3, 104: 4, 105: 5, 106: 5}.get(n, n % 6)  # a PR is about the same thing as the issue it closes
        add(n, "pr", topic, state="closed" if n < 105 else "open", merged=int(n < 105), like=3 if n == 103 else None,
            day=25, author="bob" if n % 2 else "cy", labels=[f"area: t{topic}"])
    db.executemany("insert into links values(?,?,?)", [(104, 4, "closes_official"), (105, 5, "closes_official"), (106, 5, "closes"),
                                                        (7, 6, "duplicate_of"), (20, 21, "mentions")])
    db.commit()
    return db


def run(tmp):
    path = str(Path(tmp) / "repo.db")
    db = make_db(path)
    analyze.embed_new(db)  # every hash matches: must not load the model
    analyze.init(db, 6)
    for step in (analyze.neighbors, analyze.pr_status, analyze.duplicates, analyze.zombies, analyze.competing):
        step(db)
    db.close()
    sys.argv = ["suggest.py", path]
    suggest.main()
    report.main(path)
    build_html.main(path)
    return path


def test_flow():
    with tempfile.TemporaryDirectory() as tmp:
        path = run(tmp)
        db = sqlite3.connect(path)
        one = lambda q: db.execute(q).fetchone()
        assert one("select level from dup_pairs where a=1 and b=2")[0] == "likely"
        assert one("select level from dup_pairs where a=6 and b=7")[0] == "github"
        assert one("select master from dup_master where number=7")[0] == 6
        assert one("select pr from zombie where number=3")[0] == 103
        assert one("select status from pr_status where number=4")[0] == "merged"
        assert one("select status from pr_status where number=5")[0] == "open"
        assert one("select reason from pr_compete where a=105 and b=106")[0] == "close the same issue"
        kinds = {k: c for k, c in db.execute("select kind, count(*) from actions group by 1")}
        assert kinds["close_duplicate_marked"] == 1 and kinds["close_fixed_linked"] == 1 and kinds["review_competing"] == 1
        assert kinds["add_label"] == db.execute("select count(*) from suggested").fetchone()[0]  # every suggestion has a measured hit rate
        # unlabeled open issues get the label of their topic, and nothing was written into the real labels
        got = db.execute("select number, label from suggested where number <= 12 and number != 2").fetchall()  # 2 is a copy of 1
        right = sum(lab == f"area: t{n % 6}" for n, lab in got)
        assert right >= 8 and right / len(got) >= 0.8, got
        assert one("select labels from items where number=1")[0] == "[]"
        out = Path(path).parent
        assert all(line.startswith("#") or not line for line in (out / "actions.sh").read_text().split("\n"))  # nothing runs by itself
        assert "Triage report: acme/demo" in (out / "report.md").read_text()
        assert "acme/demo" in (out / "browse.html").read_text()
        assert '<table class="rep"' in web.md_to_html((out / "report.md").read_text())


def test_text_links():
    repo = re.escape("numpy/numpy")
    close = re.compile(triageflow.CLOSE.replace("{repo}", repo), re.I)
    ref = re.compile(triageflow.NUM.replace("{repo}", repo), re.I)
    text = ("Fixes gh-17605. Closes #12, see https://github.com/numpy/numpy/pull/21995#issuecomment-1 and scipy/scipy#99, "
            "fix: #7; resolves https://github.com/numpy/numpy/issues/5 ; v1.2#3 x#4 GH-88")
    assert close.findall(text) == ["17605", "12", "7", "5"]
    assert ref.findall(text) == ["17605", "12", "21995", "7", "5", "88"]
    assert triageflow.parse_repo("https://github.com/numpy/numpy.git") == ("numpy", "numpy")


if __name__ == "__main__":
    test_text_links()
    test_flow()
    print("ok")

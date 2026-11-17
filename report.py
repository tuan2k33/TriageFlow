"""Turn the analysis into one list of proposed actions, a Markdown report to review, and a shell script of `gh`
commands (every line commented out: nothing runs until a person enables it).

The report opens with how it is made and the tech used per section; each section is then only a
table (HTML, so the column widths stay fixed in VS Code, on GitHub and in web.py). Confidence (in brackets) is the algorithm's score for
that row, 0-1: 1.00 only when certainly right (a maintainer marked the duplicate on GitHub); anything an algorithm
decides is at most 0.99 (a GitHub link, a title rule's hit rate, cosine similarity, kNN score, share of votes).
Tech used (one line per section) says how that section's proposals are found. Check shows what people and the LLM
said about the row: manual.jsonl (a person's reading, shown first) and judge.jsonl (tools/llm_judge.py), both next to
the db and both optional.

usage: python report.py data/<owner>__<name>/repo.db   ->  report.md, actions.sh next to the db; table `actions`
"""
import collections, hashlib, html, json, shlex, shutil, sqlite3, sys, time
from pathlib import Path

SOFT_MAX = 0.99  # a similarity or vote share never shows as 1.00
EMB = "bge-small-en embeddings (title + description, averaged with an extractive MMR digest of the comments)"
RULES = {  # action kind: (tech used, title); wording as the user edited it in report.md (2026-11-17)
    "close_duplicate_marked": ("GitHub GraphQL `MarkedAsDuplicateEvent`: a maintainer's own action", "Open issues already marked as duplicates"),
    "close_fixed_linked": ("GitHub GraphQL `closingIssuesReferences` and \"fixes #N\" in the PR's description, PR merged (high confidence means "
                           "the link is most likely true, neither the issue nor the PR is done)", "Open issues whose closing PR is merged"),
    "close_duplicate_likely": (f"{EMB}; high similarity between two open issues (confidence = similarity)", "Likely duplicates of an older open issue"),
    "check_recurrence": (f"{EMB}; high similarity to an older closed issue (confidence = similarity)",
                         "Open issues very similar to an older closed one (came back, or a duplicate of something settled?)"),
    "close_fixed_similar": (f"{EMB}; the issue and a later merged PR are each other's nearest neighbor, high similarity, no closing link "
                            "(confidence = similarity)", "Open issues that a later merged PR seems to fix"),
    "review_competing": (f"GitHub closing links to the same issue, or {EMB} with high similarity between open PRs of different authors "
                         "(confidence = similarity)", "Open PRs after the same thing"),
    "add_label": ("title rules learned from labeled items (prefix such as BUG:/ENH:, a component's name; confidence = the rule's hit rate); "
                  "type: kNN over the nearest labeled items (confidence = weighted share carrying the label); component: votes of the nearest "
                  "labeled items plus linked items (confidence = share of the votes)", "Labels to add"),
}


def keep_edits(f):
    """report.md is regenerated on every run; if a person edited it since the last run, keep their copy next to it first."""
    sha = f.with_name(f".{f.name}.sha1")
    if f.exists() and (not sha.exists() or hashlib.sha1(f.read_bytes()).hexdigest() != sha.read_text().strip()):
        backup = f.with_name(f"{f.name}.edited-{time.strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(f, backup)
        print(f"report.md was edited by hand since the last run: kept as {backup.name}")


def main(path):
    db = sqlite3.connect(path, timeout=120)
    repo = db.execute("select v from meta where k='repo'").fetchone()[0]
    info = {n: (k, st, t) for n, k, st, t in db.execute("select number, kind, state, title from items")}
    how_closed = dict(db.execute("select number, coalesce(state_reason, 'closed') from items where state = 'closed'"))
    is_open = {n for n, v in info.items() if v[1] == "open"}
    acts = []  # (kind, number, target, confidence, reason, command)

    def add(kind, n, target, reason, cmd, conf, hard=False):
        acts.append((kind, n, target, 1.0 if hard else round(min(float(conf), SOFT_MAX), 2), reason, cmd))

    tracking = {r[0] for r in db.execute("select number from pr_status where status = 'tracking'")}
    for d, c in db.execute("select src, dst from links where kind = 'duplicate_of'"):
        if d in is_open:
            add("close_duplicate_marked", d, c, f"marked as duplicate of #{c}", f'gh issue close {d} -R {repo} --reason "not planned" --comment "Duplicate of #{c}"', 1, hard=True)
    for n, prs in db.execute("select number, prs from pr_status where status = 'merged'"):
        merged = [p for p, f in json.loads(prs) if f == "merged"]
        add("close_fixed_linked", n, merged[0], "closing PR merged: " + ", ".join(f"#{p}" for p in merged),
            f'gh issue close {n} -R {repo} --reason completed --comment "Closed by #{merged[0]}"', 1)
    marked = {a[1] for a in acts if a[0] == "close_duplicate_marked"}
    sim = {}
    for a, b, s, lv in db.execute("select a, b, sim, level from dup_pairs where level = 'likely'"):
        sim[(a, b)] = sim[(b, a)] = s
    for n, m in db.execute("select number, master from dup_master where master != number"):
        if n in is_open and n not in marked and n not in tracking and (n, m) in sim:
            if m in is_open:
                add("close_duplicate_likely", n, m, f"duplicate of the older open #{m}",
                    f'gh issue close {n} -R {repo} --reason "not planned" --comment "Duplicate of #{m}"', sim[(n, m)])
            else:  # closing it as a duplicate would be wrong if the old problem came back
                add("check_recurrence", n, m, f"like #{m}, closed as {how_closed.get(m, info[m][1]).replace('_', ' ')}",
                    f"gh issue view {m} -R {repo}; gh issue view {n} -R {repo}", sim[(n, m)])
    for n, p, s in db.execute("select number, pr, sim from zombie"):
        if n not in tracking:
            add("close_fixed_similar", n, p, f"merged PR #{p} is its nearest match and has no link to it",
                f'gh issue close {n} -R {repo} --reason completed --comment "Looks fixed by #{p}"', s)
    for a, b, reason, issue, s in db.execute("select a, b, reason, issue, sim from pr_compete"):
        same = issue is not None
        add("review_competing", a, b, f"#{b} ({info[b][2]}) also closes #{issue}: keep one" if same
            else f"looks like #{b} ({info[b][2]}) by another author",
            f"gh pr view {a} -R {repo}; gh pr view {b} -R {repo}", 1 if same else s)
    cal = json.loads((db.execute("select v from meta where k='calibration'").fetchone() or ["{}"])[0])

    has_sug = db.execute("select 1 from sqlite_master where name='suggested'").fetchone()
    for n, ax, lab, sc, share, src in db.execute("select number, axis, label, score, share, source from suggested order by number") if has_sug else []:
        if n in is_open:
            how = "from the title" if src == "title" else f"{sc:g} votes" if src == "vote" else "kNN"
            add("add_label", n, None, f"{lab}, {how}", f"gh {'pr' if info[n][0] == 'pr' else 'issue'} edit {n} -R {repo} --add-label {shlex.quote(lab)}",
                share if src == "vote" else sc)

    db.execute("drop table if exists actions")
    db.execute("create table actions(kind text, number integer, target integer, confidence real, reason text, command text)")
    db.executemany("insert into actions values(?,?,?,?,?,?)", acts)
    db.commit()

    jf = Path(path).parent / "judge.jsonl"
    jrows = [json.loads(l) for l in jf.read_text().splitlines()] if jf.exists() else []
    judge = {(r["kind"], r["number"], r["target"]): (r["verdict"], r["reason"]) for r in jrows}
    mf = Path(path).parent / "manual.jsonl"
    manual = {(r["kind"], r["number"], r["target"]): (r["verdict"], r["note"]) for r in map(json.loads, mf.read_text().splitlines())} if mf.exists() else {}
    by = collections.defaultdict(list)
    for a in acts:
        by[a[0]].append(a)
    issues = sum(1 for n in is_open if info[n][0] == "issue")
    extra = db.execute("select count(*) from dup_master d join items i on i.number = d.number where d.master != d.number and i.state = 'open'").fetchone()[0]
    md = [f"# Triage report: {repo}", "",
          f"{len(is_open)} open items ({issues} issues, about {issues - extra} distinct problems). Proposals only: nothing here changes GitHub.", "",
          "## How this report is made", "",
          "1. **Crawl repo.** Every issue and PR of the repository, open and closed, is copied with its comments into a local database, "
          "together with the links GitHub itself keeps (which PR closes which issue, which issue a maintainer marked as a duplicate). Code is never read.",
          "2. **Read and trim.** Each item becomes one vector from its title, its description and a short digest of its comments, made by a small "
          "local language-embedding model. Items about the same thing end up close to each other.",
          "3. **Compare and group.** Pairs that are very close are proposed as duplicates, as an old bug coming back, or as an issue and the PR that "
          "fixed it without saying so. GitHub's own links are used as they are.",
          "4. **Suggest label.** A missing label comes from the title (\"BUG:\", \"f2py\") or from the labels of the most similar labeled items.",
          "5. **Score and check.** Each proposal gets the algorithm's score; person and LLM recheck afterwards.", "", "## Tech used", ""]
    md += [f"- **{title}**: {tech}." for kind, (tech, title) in RULES.items() if by[kind]]
    md.append("")
    sh = ["#!/bin/sh", f"# Proposed actions for {repo}. Review report.md, then remove the leading '# ' from the lines you agree with.", ""]
    e = html.escape
    for kind, (tech, title) in RULES.items():
        rows = sorted(by[kind], key=lambda a: (-a[3], a[1]))
        if not rows:
            continue
        md += [f'<details><summary><h2 style="display:inline;border:none;padding:0;margin:0">{e(title)} ({len(rows)})</h2></summary>',  # click the title to show / hide the table
               '<table class="rep" style="table-layout:fixed;width:100%"><colgroup><col width="30%" style="width:30%">'
               '<col width="20%" style="width:20%"><col width="50%" style="width:50%"></colgroup>',
               "<tr><th width=\"30%\">Item</th><th width=\"20%\">Proposal (confidence)</th><th width=\"50%\">Check</th></tr>"]  # width on th too: GitHub drops colgroup and style
        sh += [f"# --- {title} ({len(rows)})"]
        for _, n, target, conf, reason, cmd in rows:
            key = (kind, n, target)
            check = ("checked by maintainer" if kind == "close_duplicate_marked" else
                     " ".join(([f"<b>{e(manual[key][0])}</b>, {e(manual[key][1])}."] if key in manual else [])
                              + ([f"<b>{e(judge[key][0])}</b>, {e(judge[key][1])}"] if key in judge else [])))
            md.append(f'<tr><td><a href="https://github.com/{repo}/issues/{n}">#{n}</a> {e(info[n][2])}</td>'
                      f"<td>{e(reason)} ({conf:.2f})</td><td>{check}</td></tr>")
            sh.append(f"# {cmd}   # {conf:.2f}")
        md += ["</table></details>", ""]
        sh.append("")
    out = Path(path).parent
    keep_edits(out / "report.md")
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    (out / ".report.md.sha1").write_text(hashlib.sha1((out / "report.md").read_bytes()).hexdigest())
    (out / "actions.sh").write_text("\n".join(sh), encoding="utf-8")
    print(f"{len(acts)} proposals: " + ", ".join(f"{len(v)} {k}" for k, v in by.items()))
    print(f"{out / 'report.md'}\n{out / 'actions.sh'}")


if __name__ == "__main__":
    main(sys.argv[1])

"""Turn the analysis into one list of proposed actions with a confidence and a reason, a Markdown report to review,
and a shell script of `gh` commands (every line commented out: nothing runs until a person enables it).

Confidence is always "how often this kind of proposal was right when measured": against hidden labels, against links
GitHub records, or by reading a sample by hand (numpy). The source of each number is in RULES.

usage: python report.py data/<owner>__<name>/repo.db   ->  report.md, actions.sh next to the db; table `actions`
"""
import collections, json, shlex, sqlite3, sys
from pathlib import Path

RULES = {  # action kind: (confidence or None when it comes per item, how it was measured, title in the report)
    "close_duplicate_marked": (1.0, "a maintainer marked it as a duplicate on GitHub", "Open issues already marked as duplicates"),
    "close_fixed_linked": (0.7, "hand check of the 14 numpy cases: about 10 are done, the rest track larger work", "Open issues whose closing PR is merged"),
    "close_duplicate_likely": (0.8, "hand-graded sample of 25 numpy pairs with similarity >= 0.90", "Likely duplicates of an older or original issue"),
    "close_fixed_similar": (0.5, "hand-graded sample of 25 numpy cases (82% on closed issues with a known closing PR)", "Open issues that a later merged PR seems to fix"),
    "review_competing": (None, "two open PRs with a closing link to the same issue: certain; similar PRs by different authors: similarity", "Open PRs after the same thing"),
    "add_label": (None, "share of suggestions with this score that matched the hidden real label (a lower bound: real labels are often missing)", "Labels to add"),
}


def main(path):
    db = sqlite3.connect(path, timeout=120)
    repo = db.execute("select v from meta where k='repo'").fetchone()[0]
    info = {n: (k, st, t) for n, k, st, t in db.execute("select number, kind, state, title from items")}
    is_open = {n for n, v in info.items() if v[1] == "open"}
    acts = []  # (kind, number, target, confidence, reason, command)

    def add(kind, n, target, reason, cmd, conf=None):
        acts.append((kind, n, target, RULES[kind][0] if conf is None else conf, reason, cmd))

    tracking = {r[0] for r in db.execute("select number from pr_status where status = 'tracking'")}
    for d, c in db.execute("select src, dst from links where kind = 'duplicate_of'"):
        if d in is_open:
            add("close_duplicate_marked", d, c, f"marked as duplicate of #{c}", f'gh issue close {d} -R {repo} --reason "not planned" --comment "Duplicate of #{c}"')
    for n, prs in db.execute("select number, prs from pr_status where status = 'merged'"):
        merged = [p for p, f in json.loads(prs) if f == "merged"]
        add("close_fixed_linked", n, merged[0], "closing PR merged: " + ", ".join(f"#{p}" for p in merged),
            f'gh issue close {n} -R {repo} --reason completed --comment "Closed by #{merged[0]}"')
    marked = {a[1] for a in acts if a[0] == "close_duplicate_marked"}
    sim = {}
    for a, b, s, lv in db.execute("select a, b, sim, level from dup_pairs where level = 'likely'"):
        sim[(a, b)] = sim[(b, a)] = s
    for n, m in db.execute("select number, master from dup_master where master != number"):
        if n in is_open and n not in marked and n not in tracking and (n, m) in sim:
            add("close_duplicate_likely", n, m, f"{sim[(n, m)]:.0%} similar to the older #{m} ({info[m][1]})",
                f'gh issue close {n} -R {repo} --reason "not planned" --comment "Duplicate of #{m}"')
    for n, p, s in db.execute("select number, pr, sim from zombie"):
        if n not in tracking:
            add("close_fixed_similar", n, p, f"merged PR #{p} is its nearest match ({s:.0%}) and has no link to it",
                f'gh issue close {n} -R {repo} --reason completed --comment "Looks fixed by #{p}"')
    for a, b, reason, issue, s in db.execute("select a, b, reason, issue, sim from pr_compete"):
        same = issue is not None
        add("review_competing", a, b, f"both close #{issue}" if same else f"{s:.0%} similar, different authors",
            f"gh pr view {a} -R {repo}; gh pr view {b} -R {repo}", 1.0 if same else round(s, 2))
    cal = json.loads((db.execute("select v from meta where k='calibration'").fetchone() or ["{}"])[0])

    def measured(axis, score):
        ok = [p for lo, p in cal.get(axis, []) if score >= lo and p is not None]
        return ok[-1] if ok else None

    has_sug = db.execute("select 1 from sqlite_master where name='suggested'").fetchone()
    for n, ax, lab, sc in db.execute("select number, axis, label, score from suggested order by number") if has_sug else []:
        conf = measured(ax, sc)
        if n in is_open and conf is not None:
            why = f"{sc:g} votes from similar and linked items" if ax == "component" else f"kNN score {sc:.2f}"
            add("add_label", n, None, f"{lab} ({why})", f"gh {'pr' if info[n][0] == 'pr' else 'issue'} edit {n} -R {repo} --add-label {shlex.quote(lab)}", conf)

    db.execute("drop table if exists actions")
    db.execute("create table actions(kind text, number integer, target integer, confidence real, reason text, command text)")
    db.executemany("insert into actions values(?,?,?,?,?,?)", acts)
    db.commit()

    by = collections.defaultdict(list)
    for a in acts:
        by[a[0]].append(a)
    issues = sum(1 for n in is_open if info[n][0] == "issue")
    extra = db.execute("select count(*) from dup_master d join items i on i.number = d.number where d.master != d.number and i.state = 'open'").fetchone()[0]
    md = [f"# Triage report: {repo}", "",
          f"{len(is_open)} open items ({issues} issues, about {issues - extra} distinct problems). Proposals only: nothing here changes GitHub.",
          "Confidence = how often this kind of proposal was right when measured.", ""]
    sh = ["#!/bin/sh", f"# Proposed actions for {repo}. Review report.md, then remove the leading '# ' from the lines you agree with.", ""]
    for kind, (_, how, title) in RULES.items():
        rows = sorted(by[kind], key=lambda a: (-a[3], a[1]))
        if not rows:
            continue
        md += [f"## {title} ({len(rows)})", "", f"Measured by: {how}.", "", "| Confidence | Item | Proposal |", "|---|---|---|"]
        sh += [f"# --- {title} ({len(rows)})"]
        for _, n, target, conf, reason, cmd in rows:
            md.append(f"| {conf:.0%} | [#{n}](https://github.com/{repo}/issues/{n}) {info[n][2][:80].replace('|', '/')} | {reason} |")
            sh.append(f"# {cmd}   # {conf:.0%}")
        md.append("")
        sh.append("")
    out = Path(path).parent
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    (out / "actions.sh").write_text("\n".join(sh), encoding="utf-8")
    print(f"{len(acts)} proposals: " + ", ".join(f"{len(v)} {k}" for k, v in by.items()))
    print(f"{out / 'report.md'}\n{out / 'actions.sh'}")


if __name__ == "__main__":
    main(sys.argv[1])

"""Turn the analysis into one list of proposed actions, a Markdown report to review, and a shell script of `gh`
commands (every line commented out: nothing runs until a person enables it).

Each kind of proposal has a level (certain / likely / check) and the evidence behind it, with raw counts: a GitHub
record, a hand-graded sample (numpy only, so small and borrowed by other repos), or the hidden-label test of this repo.
The confidence column is each row's own raw signal (cosine similarity, kNN score, vote count, 1.00 for a GitHub
record), never a percentage derived from it: a sample of 12-30 cases cannot give one per row. What the number means
is written at the top of each section.

usage: python report.py data/<owner>__<name>/repo.db   ->  report.md, actions.sh next to the db; table `actions`
"""
import collections, json, shlex, sqlite3, sys
from pathlib import Path

GRADED_ON = "numpy/numpy"
RULES = {  # action kind: (level or None when it comes per row, evidence, graded by hand on GRADED_ON, title)
    "close_duplicate_marked": ("certain", "a maintainer marked it as a duplicate on GitHub", False, "Open issues already marked as duplicates"),
    "close_fixed_linked": ("likely", "GitHub links a merged PR that closes it; by hand about 10 of 14 were done, the rest track larger work", True,
                           "Open issues whose closing PR is merged"),
    "close_duplicate_likely": ("likely", "similarity >= 0.92; by hand 9.5 of 12 such pairs were the same problem (0.91-0.92: 3.5 of 12)", True,
                               "Likely duplicates of an older open issue"),
    "check_recurrence": ("check", "same test as above; whether the old problem came back or was never fixed is for a person to judge", True,
                         "Open issues very similar to an older closed one (came back, or a duplicate of something settled?)"),
    "close_fixed_similar": ("check", "issue and a later merged PR are each other's nearest, no link; by hand 10 of 20 fixed, 6 partly, 4 only related", True,
                            "Open issues that a later merged PR seems to fix"),
    "review_competing": (None, "certain when both PRs link the same issue; check when they are only similar (not graded)", False, "Open PRs after the same thing"),
    "add_label": (None, "hidden-label test on this repo: the share of suggestions with that score that matched the real label. "
                  "A lower bound, since real labels are often missing; by hand on numpy ~88% of component and ~77% of type suggestions were related", False,
                  "Labels to add"),
}
MEANS = {  # what the confidence number of each kind is
    "close_duplicate_marked": "1.00 = recorded on GitHub",
    "close_fixed_linked": "1.00 = GitHub links a merged PR that closes it",
    "close_duplicate_likely": "cosine similarity of the two issues (0-1)",
    "check_recurrence": "cosine similarity of the two issues (0-1)",
    "close_fixed_similar": "cosine similarity of the issue and the PR (0-1)",
    "review_competing": "1.00 = both PRs link the same issue, otherwise their cosine similarity",
    "add_label": "type: kNN score (0-1, weighted share of the 10 nearest labeled items carrying it); component/label: votes of the 5 nearest labeled items plus linked items",
}


def main(path):
    db = sqlite3.connect(path, timeout=120)
    repo = db.execute("select v from meta where k='repo'").fetchone()[0]
    info = {n: (k, st, t) for n, k, st, t in db.execute("select number, kind, state, title from items")}
    how_closed = dict(db.execute("select number, coalesce(state_reason, 'closed') from items where state = 'closed'"))
    is_open = {n for n, v in info.items() if v[1] == "open"}
    acts = []  # (kind, number, target, level, score, signal, reason, command); score orders rows inside a kind

    def add(kind, n, target, reason, cmd, score, signal, level=None):
        acts.append((kind, n, target, level or RULES[kind][0], score, signal, reason, cmd))

    tracking = {r[0] for r in db.execute("select number from pr_status where status = 'tracking'")}
    for d, c in db.execute("select src, dst from links where kind = 'duplicate_of'"):
        if d in is_open:
            add("close_duplicate_marked", d, c, f"marked as duplicate of #{c}", f'gh issue close {d} -R {repo} --reason "not planned" --comment "Duplicate of #{c}"', 1, "1.00")
    for n, prs in db.execute("select number, prs from pr_status where status = 'merged'"):
        merged = [p for p, f in json.loads(prs) if f == "merged"]
        add("close_fixed_linked", n, merged[0], "closing PR merged: " + ", ".join(f"#{p}" for p in merged),
            f'gh issue close {n} -R {repo} --reason completed --comment "Closed by #{merged[0]}"', 1, "1.00")
    marked = {a[1] for a in acts if a[0] == "close_duplicate_marked"}
    sim = {}
    for a, b, s, lv in db.execute("select a, b, sim, level from dup_pairs where level = 'likely'"):
        sim[(a, b)] = sim[(b, a)] = s
    for n, m in db.execute("select number, master from dup_master where master != number"):
        if n in is_open and n not in marked and n not in tracking and (n, m) in sim:
            if m in is_open:
                add("close_duplicate_likely", n, m, f"duplicate of the older open #{m}",
                    f'gh issue close {n} -R {repo} --reason "not planned" --comment "Duplicate of #{m}"', sim[(n, m)], f"{sim[(n, m)]:.2f}")
            else:  # closing it as a duplicate would be wrong if the old problem came back
                add("check_recurrence", n, m, f"like #{m}, closed as {how_closed.get(m, info[m][1]).replace('_', ' ')}",
                    f"gh issue view {m} -R {repo}; gh issue view {n} -R {repo}", sim[(n, m)], f"{sim[(n, m)]:.2f}")
    for n, p, s in db.execute("select number, pr, sim from zombie"):
        if n not in tracking:
            add("close_fixed_similar", n, p, f"merged PR #{p} is its nearest match and has no link to it",
                f'gh issue close {n} -R {repo} --reason completed --comment "Looks fixed by #{p}"', s, f"{s:.2f}")
    for a, b, reason, issue, s in db.execute("select a, b, reason, issue, sim from pr_compete"):
        same = issue is not None
        add("review_competing", a, b, f"#{b} ({info[b][2][:60]}) also closes #{issue}: keep one" if same
            else f"looks like #{b} ({info[b][2][:60]}) by another author",
            f"gh pr view {a} -R {repo}; gh pr view {b} -R {repo}", 2 if same else s, "1.00" if same else f"{s:.2f}",
            "certain" if same else "check")
    cal = json.loads((db.execute("select v from meta where k='calibration'").fetchone() or ["{}"])[0])

    def measured(axis, score):
        ok = [p for lo, p in cal.get(axis, []) if score >= lo and p is not None]
        return ok[-1] if ok else None

    has_sug = db.execute("select 1 from sqlite_master where name='suggested'").fetchone()
    for n, ax, lab, sc, src in db.execute("select number, axis, label, score, source from suggested order by number") if has_sug else []:
        conf = measured(ax, sc)
        if n in is_open and conf is not None:
            sig = f"{sc:g} votes" if src == "vote" else f"{sc:.2f}"
            add("add_label", n, None, lab, f"gh {'pr' if info[n][0] == 'pr' else 'issue'} edit {n} -R {repo} --add-label {shlex.quote(lab)}",
                conf, sig, "likely" if conf >= 0.8 else "check")

    db.execute("drop table if exists actions")
    db.execute("create table actions(kind text, number integer, target integer, level text, score real, signal text, reason text, command text)")
    db.executemany("insert into actions values(?,?,?,?,?,?,?,?)", acts)
    db.commit()

    by = collections.defaultdict(list)
    for a in acts:
        by[a[0]].append(a)
    issues = sum(1 for n in is_open if info[n][0] == "issue")
    extra = db.execute("select count(*) from dup_master d join items i on i.number = d.number where d.master != d.number and i.state = 'open'").fetchone()[0]
    md = [f"# Triage report: {repo}", "",
          f"{len(is_open)} open items ({issues} issues, about {issues - extra} distinct problems). Proposals only: nothing here changes GitHub.",
          "Level: **certain** = GitHub records it; **likely** = most of a hand-graded sample was right; **check** = worth a look, often wrong. "
          "Confidence = the row's own signal, as measured (similarity, kNN score, votes); each section says which. Rows are sorted by it.", ""]
    sh = ["#!/bin/sh", f"# Proposed actions for {repo}. Review report.md, then remove the leading '# ' from the lines you agree with.", ""]
    for kind, (level, how, graded, title) in RULES.items():
        rows = sorted(by[kind], key=lambda a: (-a[4], a[1]))
        if not rows:
            continue
        borrowed = f" Graded on {GRADED_ON} only; not checked on this repo." if graded and repo != GRADED_ON else ""
        head = f"Level: **{level}**. " if level else ""
        test = ""
        if kind == "add_label":
            def span(bins, i):
                lo, hi = bins[i][0], bins[i + 1][0] if i + 1 < len(bins) else None
                return f"{lo:g}+" if hi is None else f"{lo:g}" if hi - lo == 1 else f"{lo:g}-{hi:g}"
            test = " This repo: " + "; ".join(f"{ax} {span(bins, i)}{' votes' if ax != 'type' else ''}: {p:.0%} matched"
                                              for ax, bins in cal.items() for i, (lo, p) in enumerate(bins) if p is not None) + "."
        md += [f"## {title} ({len(rows)})", "", f"{head}Evidence: {how}.{test}{borrowed}", "", f"Confidence: {MEANS[kind]}.", "",
               "| Confidence | Item | Proposal |" if level else "| Level | Confidence | Item | Proposal |", "|---|---|---|" if level else "|---|---|---|---|"]
        sh += [f"# --- {title} ({len(rows)})"]
        for _, n, target, lv, _, sig, reason, cmd in rows:
            cells = [sig, f"[#{n}](https://github.com/{repo}/issues/{n}) {info[n][2][:80].replace('|', '/')}", reason.replace("|", "/")]
            md.append("| " + " | ".join(cells if level else [lv] + cells) + " |")
            sh.append(f"# {cmd}   # {lv}, {sig}")
        md.append("")
        sh.append("")
    out = Path(path).parent
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    (out / "actions.sh").write_text("\n".join(sh), encoding="utf-8")
    print(f"{len(acts)} proposals: " + ", ".join(f"{len(v)} {k}" for k, v in by.items()))
    print(f"{out / 'report.md'}\n{out / 'actions.sh'}")


if __name__ == "__main__":
    main(sys.argv[1])

"""Turn the analysis into one list of proposed actions, a Markdown report to review, and a shell script of `gh`
commands (every line commented out: nothing runs until a person enables it).

Confidence is a number from 0 to 1 per row, never a percentage made up from a sample. 1.00 only when the proposal is
certainly right: a maintainer marked the duplicate on GitHub. Everything an algorithm decides is at most 0.99: a
GitHub link (0.99: the link is a fact, the issue being done is not), a title rule (its measured hit rate), otherwise
the row's own signal (cosine similarity, kNN score, share of votes). If judge.jsonl (tools/llm_judge.py) is next to
the db, its verdicts are shown in an extra column. Each section states what its number is and the evidence for that kind
of proposal with raw counts (hand-graded samples are numpy's; other repos borrow them and say so).

usage: python report.py data/<owner>__<name>/repo.db   ->  report.md, actions.sh next to the db; table `actions`
"""
import collections, json, shlex, sqlite3, sys
from pathlib import Path

GRADED_ON = "numpy/numpy"
SOFT_MAX = 0.99  # a similarity or vote share never shows as 1.00
RULES = {  # action kind: (evidence, graded by hand on GRADED_ON, what the confidence number is, title)
    "close_duplicate_marked": ("a maintainer marked it as a duplicate on GitHub", False, "1.00 = recorded on GitHub",
                               "Open issues already marked as duplicates"),
    "close_fixed_linked": ("by hand about 10 of 14 were done, the rest track larger work", True, "0.99 = GitHub links a merged PR that closes it",
                           "Open issues whose closing PR is merged"),
    "close_duplicate_likely": ("similarity >= 0.92; by hand 9.5 of 12 such pairs were the same problem (0.91-0.92: 3.5 of 12)", True,
                               "cosine similarity of the two issues", "Likely duplicates of an older open issue"),
    "check_recurrence": ("same test as above; whether the old problem came back or was never fixed is for a person to judge", True,
                         "cosine similarity of the two issues", "Open issues very similar to an older closed one (came back, or a duplicate of something settled?)"),
    "close_fixed_similar": ("issue and a later merged PR are each other's nearest, no link; by hand 10 of 20 fixed, 6 partly, 4 only related", True,
                            "cosine similarity of the issue and the PR", "Open issues that a later merged PR seems to fix"),
    "review_competing": ("similar pairs are not graded", False, "0.99 = both PRs link the same issue, otherwise their cosine similarity",
                         "Open PRs after the same thing"),
    "add_label": ("hidden-label test on this repo, exact match, so a lower bound (real labels are often missing); by hand on numpy ~88% of "
                  "component and ~77% of type suggestions were related", False,
                  "from the title (prefix such as BUG:, or the component's name): that rule's hit rate; type: kNN score, the weighted share of the "
                  "10 nearest labeled items carrying it; component: share of the votes (5 nearest labeled items plus linked items)", "Labels to add"),
}


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
    judge = {(r["kind"], r["number"], r["target"]): (r["verdict"], r["reason"]) for r in map(json.loads, jf.read_text().splitlines())} if jf.exists() else {}
    by = collections.defaultdict(list)
    for a in acts:
        by[a[0]].append(a)
    issues = sum(1 for n in is_open if info[n][0] == "issue")
    extra = db.execute("select count(*) from dup_master d join items i on i.number = d.number where d.master != d.number and i.state = 'open'").fetchone()[0]
    md = [f"# Triage report: {repo}", "",
          f"{len(is_open)} open items ({issues} issues, about {issues - extra} distinct problems). Proposals only: nothing here changes GitHub.",
          "Confidence 0-1, in brackets after each proposal: 1.00 only when certainly right (a maintainer marked it on GitHub); anything "
          "an algorithm decides is at most 0.99 (a GitHub link, a title rule's hit rate, similarity, kNN score, share of votes). "
          "Each section says which. Rows are sorted by it.", ""]
    sh = ["#!/bin/sh", f"# Proposed actions for {repo}. Review report.md, then remove the leading '# ' from the lines you agree with.", ""]
    for kind, (how, graded, means, title) in RULES.items():
        rows = sorted(by[kind], key=lambda a: (-a[3], a[1]))
        if not rows:
            continue
        borrowed = f" Graded on {GRADED_ON} only; not checked on this repo." if graded and repo != GRADED_ON else ""
        test = ""
        if kind == "add_label":
            def span(bins, i):
                lo, hi = bins[i][0], bins[i + 1][0] if i + 1 < len(bins) else None
                return f"{lo:g}+" if hi is None else f"{lo:g}" if hi - lo == 1 else f"{lo:g}-{hi:g}"
            test = " This repo: " + "; ".join(f"{ax} {span(bins, i)}{' votes' if ax != 'type' else ''}: {p:.0%} matched"
                                              for ax, bins in cal.items() if isinstance(bins, list) for i, (lo, p) in enumerate(bins) if p is not None) + "."
            if cal.get("title"):
                test += " Title rules: " + ", ".join(f"{k.split(':', 1)[-1].strip()} {p:.0%}" for k, p in sorted(cal["title"].items())) + "."
        checked = any((kind, a[1], a[2]) in judge for a in rows)
        md += [f"## {title} ({len(rows)})", "", f"Confidence: {means}.", "", f"Evidence: {how}.{test}{borrowed}", "",
               "| Item | Proposal (confidence) |" + (" LLM check |" if checked else ""), "|---|---|" + ("---|" if checked else "")]
        sh += [f"# --- {title} ({len(rows)})"]
        for _, n, target, conf, reason, cmd in rows:
            cells = [f"[#{n}](https://github.com/{repo}/issues/{n}) {info[n][2]}", f"{reason} ({conf:.2f})"]
            if checked:
                v = judge.get((kind, n, target))
                cells.append(f"**{v[0]}**: {v[1]}" if v else "")
            md.append("| " + " | ".join(c.replace("|", "/").replace("\n", " ") for c in cells) + " |")
            sh.append(f"# {cmd}   # {conf:.2f}")
        md.append("")
        sh.append("")
    out = Path(path).parent
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    (out / "actions.sh").write_text("\n".join(sh), encoding="utf-8")
    print(f"{len(acts)} proposals: " + ", ".join(f"{len(v)} {k}" for k, v in by.items()))
    print(f"{out / 'report.md'}\n{out / 'actions.sh'}")


if __name__ == "__main__":
    main(sys.argv[1])

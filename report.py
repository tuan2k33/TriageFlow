"""Turn the analysis into one list of proposed actions, a Markdown report to review, and a shell script of `gh`
commands (every line commented out: nothing runs until a person enables it).

The report opens with three definitions. Confidence (in brackets after each proposal) is the algorithm's score for
that row, 0-1: 1.00 only when certainly right (a maintainer marked the duplicate on GitHub); anything an algorithm
decides is at most 0.99 (a GitHub link, a title rule's hit rate, cosine similarity, kNN score, share of votes).
Tech used (one line per section) says how that section's proposals are found. Check shows what people and the LLM
said about the row: manual.jsonl (a person's reading, shown first) and judge.jsonl (tools/llm_judge.py), both next to
the db and both optional.

usage: python report.py data/<owner>__<name>/repo.db   ->  report.md, actions.sh next to the db; table `actions`
"""
import collections, json, shlex, sqlite3, sys
from pathlib import Path

SOFT_MAX = 0.99  # a similarity or vote share never shows as 1.00
EMB = "bge-small-en embeddings (title + description, averaged with an extractive MMR digest of the comments)"
RULES = {  # action kind: (tech used, title)
    "close_duplicate_marked": ("GitHub GraphQL `MarkedAsDuplicateEvent`: a maintainer's own action (confidence 1.00)",
                               "Open issues already marked as duplicates"),
    "close_fixed_linked": ("GitHub GraphQL `closingIssuesReferences` and \"fixes #N\" in the PR's description, PR merged (confidence 0.99: "
                           "the link is a fact, the issue being done is not; reverted PRs are not detected)", "Open issues whose closing PR is merged"),
    "close_duplicate_likely": (f"{EMB}; cosine similarity >= 0.92 between two open issues; the older one is kept (confidence = similarity)",
                               "Likely duplicates of an older open issue"),
    "check_recurrence": (f"{EMB}; cosine similarity >= 0.92 to an older closed issue (confidence = similarity)",
                         "Open issues very similar to an older closed one (came back, or a duplicate of something settled?)"),
    "close_fixed_similar": (f"{EMB}; the issue and a later merged PR are each other's nearest neighbor, similarity >= 0.88, "
                            "no closing link (confidence = similarity)", "Open issues that a later merged PR seems to fix"),
    "review_competing": ("GitHub closing links to the same issue (confidence 0.99), or "
                         f"{EMB} with similarity >= 0.92 between open PRs of different authors (confidence = similarity)", "Open PRs after the same thing"),
    "add_label": ("title rules learned from labeled items (prefix such as BUG:/ENH:, a component's name; kept only if >= 85% right; "
                  "confidence = the rule's hit rate); type: kNN over the 10 nearest labeled items (confidence = weighted share carrying the label); "
                  "component: votes of the 5 nearest labeled items plus linked items (confidence = share of the votes)", "Labels to add"),
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
    jrows = [json.loads(l) for l in jf.read_text().splitlines()] if jf.exists() else []
    judge = {(r["kind"], r["number"], r["target"]): (r["verdict"], r["reason"]) for r in jrows}
    jmodel = jrows[0]["model"] if jrows else None
    mf = Path(path).parent / "manual.jsonl"
    manual = {(r["kind"], r["number"], r["target"]): (r["verdict"], r["note"]) for r in map(json.loads, mf.read_text().splitlines())} if mf.exists() else {}
    by = collections.defaultdict(list)
    for a in acts:
        by[a[0]].append(a)
    issues = sum(1 for n in is_open if info[n][0] == "issue")
    extra = db.execute("select count(*) from dup_master d join items i on i.number = d.number where d.master != d.number and i.state = 'open'").fetchone()[0]
    md = [f"# Triage report: {repo}", "",
          f"{len(is_open)} open items ({issues} issues, about {issues - extra} distinct problems). Proposals only: nothing here changes GitHub.",
          "", "- **Confidence** (in brackets after each proposal): the algorithm's score for that row, 0-1. 1.00 only when certainly right "
          "(a maintainer marked it on GitHub); anything an algorithm or ML model decides is at most 0.99. Rows are sorted by it.",
          "- **Tech used** (under each section title): how that section's proposals are found.",
          f"- **Check**: manual check (a person read both items) and LLM check ({jmodel or 'no LLM run yet'} read both threads). "
          "Neither is part of the algorithm.", ""]
    sh = ["#!/bin/sh", f"# Proposed actions for {repo}. Review report.md, then remove the leading '# ' from the lines you agree with.", ""]
    for kind, (tech, title) in RULES.items():
        rows = sorted(by[kind], key=lambda a: (-a[3], a[1]))
        if not rows:
            continue
        test = ""
        if kind == "add_label":
            def span(bins, i):
                lo, hi = bins[i][0], bins[i + 1][0] if i + 1 < len(bins) else None
                return f"{lo:g}+" if hi is None else f"{lo:g}" if hi - lo == 1 else f"{lo:g}-{hi:g}"
            test = " Hidden-label test on this repo (exact match, a lower bound): " + "; ".join(f"{ax} {span(bins, i)}{' votes' if ax != 'type' else ''}: {p:.0%} matched"
                                              for ax, bins in cal.items() if isinstance(bins, list) for i, (lo, p) in enumerate(bins) if p is not None) + "."
            if cal.get("title"):
                test += " Title rules: " + ", ".join(f"{k.split(':', 1)[-1].strip()} {p:.0%}" for k, p in sorted(cal["title"].items())) + "."
        checked = True  # same three columns in every section, so the fixed widths line up
        md += [f"## {title} ({len(rows)})", "", f"Tech used: {tech}.{test}", "",
               "| Item | Proposal (confidence) |" + (" Check |" if checked else ""), "|---|---|" + ("---|" if checked else "")]
        sh += [f"# --- {title} ({len(rows)})"]
        for _, n, target, conf, reason, cmd in rows:
            cells = [f"[#{n}](https://github.com/{repo}/issues/{n}) {info[n][2]}", f"{reason} ({conf:.2f})"]
            if checked:
                key = (kind, n, target)
                cells.append(" ".join(([f"Manual: **{manual[key][0]}**, {manual[key][1]}."] if key in manual else [])
                                      + ([f"LLM: **{judge[key][0]}**, {judge[key][1]}"] if key in judge else [])))
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

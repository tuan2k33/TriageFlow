# TriageFlow

Crawl all issues and PRs of a GitHub repo (open and closed, with conversation comments, content only, no code) into SQLite, then sort them into categories, suggest labels from the repo's existing ones, find duplicates, stale and already-fixed issues and competing PRs, and write a report of proposed actions. Everything from the crawl to the report is local data analysis and classic machine learning (a small embedding model, KMeans, kNN votes, rules learned from titles); no LLM makes any proposal. An LLM is used only afterwards, to recheck the report's rows (see below).

```bash
python run.py https://github.com/numpy/numpy   # crawl -> analyze -> report -> browse page, in one go: data/numpy__numpy/{repo.db, browse.html, report.md, actions.sh}
python run.py numpy/numpy --labels             # the same plus label suggestions (optional step)
python web.py                                   # local web view at http://127.0.0.1:8000: paste a link, then Browse / Report / Actions / Database per repo
```

The steps, each rerunnable on its own (`suggest.py` only with `--labels`):

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy       # all issues/PRs + comments + GitHub's own links: PR closes issue, duplicate of, sub-issue (GitHub API; token from `gh auth token`); reruns sync only what changed
python analyze.py $R                   # embed new or changed threads (bge-small, fp16; title+description averaged with an extractive digest of the comments); categories once (--init to redo); semantic links; PR status of open issues; duplicate candidates
python suggest.py $R                   # optional: labels for open items that lack them: rules learned from titles (BUG:, f2py), then kNN (type) and votes of the nearest and linked items (components); neighbors and minimum votes are swept per repo
python report.py $R                    # proposals with the algorithm's confidence -> report.md + actions.sh (gh commands, all commented out)
python build_html.py $R                # -> data/numpy__numpy/browse.html: filters, list of open items, details with a timeline
datasette $R                           # browse / SQL / full-text search
```

Tables: `items` (all states), `comments`, `links` (closes_official / closes / mentions / duplicate_of / sub_issue), `emb`, `categories`, `topics` (category per item), `neighbors`, `similar` (semantic links), `pr_status`, `dup_pairs` / `dup_master` (duplicate candidates), `zombie`, `pr_compete`, `actions`, `suggested`, `fts`.

## Requirements and tests

`gh` logged in (the crawler reads the token from `gh auth token`), Python 3.12+, and `numpy`, `scikit-learn`, `torch`, `transformers` (here they come from the shared env, so `requirements.txt` only lists what this project adds). A GPU is used when there is one; without it the embedding step runs on the CPU, slower. `datasette` is optional.

```bash
python -m pytest tests -q    # offline: a synthetic repo with planted cases through the whole analysis
```

## Reports

`reports/numpy__numpy/` holds the output for numpy/numpy (crawled 2026-11-16): `report.md` (the proposals; open it on GitHub or in any Markdown viewer), `browse.html` (download and open locally: filters, a type x component matrix, details per item), `actions.sh` (the matching `gh` commands, all commented out), `judge.jsonl` (the LLM recheck) and `manual.jsonl` (rows rechecked by hand). The SQLite database is not included (370 MB); `python run.py numpy/numpy` rebuilds it.

Of the 2251 open items, the report proposes a quick action for 228 (219 issues, 9 PRs), not counting label suggestions. Nothing here changes GitHub: every command in `actions.sh` is commented out.

## AI Disclosure

- **Idea and flow:** mine. I designed what to crawl, how to compare items and what to propose, and Claude (Claude Code, Anthropic) implemented it.
- **Results:** every proposal in the report comes from the algorithm described above (GitHub's own links, a local embedding model, kNN and vote counts, rules learned from titles). No LLM makes or edits a proposal.
- **Recheck:** an LLM (`nvidia/nemotron-3-ultra-550b-a55b:free` on OpenRouter, `tools/llm_judge.py`) read both items of each non-label proposal for numpy and judged over 90% of them at least related (220 of 234; 85 the same problem or fixed). The 14 it called unrelated were reread by hand (`manual.jsonl`); all 14 turned out related (same function or area). Its verdicts are the Check column of the report.

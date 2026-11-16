# TriageFlow

Crawl all issues and PRs of a GitHub repo (open and closed, with conversation comments, content only, no code) into SQLite, then sort them into categories, suggest labels from the repo's existing ones find duplicates, stale and already-fixed issues and competing PRs, and write a report of proposed actions. Everything after the crawl is local data analysis and classic machine learning (a small embedding model, KMeans, kNN votes); no LLM anywhere.

```bash
python run.py https://github.com/numpy/numpy   # everything below in one go -> data/numpy__numpy/{repo.db, browse.html, report.md, actions.sh}
python web.py                                   # local web view at http://127.0.0.1:8000: paste a link, then Browse / Report / Actions / Database per repo
```

The steps `run.py` runs, each rerunnable on its own:

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy       # all issues/PRs + comments + GitHub's own links: PR closes issue, duplicate of, sub-issue (GitHub API; token from `gh auth token`); reruns sync only what changed
python analyze.py $R                   # embed new items (bge-small, fp16); categories once (--init to redo); semantic links; PR status of open issues; duplicate candidates
python suggest.py $R                   # labels for open items that lack them, by votes of the 5 nearest labeled items and linked items (any repo)
python report.py $R                    # proposals with confidence -> report.md + actions.sh (gh commands, all commented out)
python build_html.py $R                # -> data/numpy__numpy/browse.html: filters, list of open items, details with a timeline
datasette $R                           # browse / SQL / full-text search
```

Tables: `items` (all states), `comments`, `links` (closes_official / closes / mentions / duplicate_of / sub_issue), `emb`, `categories`, `topics` (category per item), `neighbors`, `similar` (semantic links), `pr_status`, `dup_pairs` / `dup_master` (duplicate candidates), `zombie`, `pr_compete`, `actions`, `suggested`, `fts`.

## Requirements and tests

`gh` logged in (the crawler reads the token from `gh auth token`), Python 3.12+, and `numpy`, `scikit-learn`, `torch`, `transformers` (here they come from the shared env, so `requirements.txt` only lists what this project adds). A GPU is used when there is one; without it the embedding step runs on the CPU, slower. `datasette` is optional.

```bash
python -m pytest tests -q    # offline: a synthetic repo with planted cases through the whole analysis
```

## AI Disclosure

Written with the help of Claude Code (Anthropic).

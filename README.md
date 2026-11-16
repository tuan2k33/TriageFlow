# TriageFlow

Crawl all issues and PRs of a GitHub repo (open and closed, with conversation comments, content only, no code) into SQLite, then sort them into categories, suggest labels from the repo's existing ones and browse the open ones on a map. Everything after the crawl is local data analysis and classic machine learning (a small embedding model, KMeans, kNN votes); no LLM anywhere.

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy       # all issues/PRs + comments + GitHub's own links: PR closes issue, duplicate of, sub-issue (GitHub API; token from `gh auth token`); reruns sync only what changed
python analyze.py $R                   # embed new items (bge-small, fp16); categories once (--init to redo); semantic links; PR status of open issues; duplicate candidates
python suggest.py $R                   # type labels by kNN; component labels by counting votes of the 5 nearest labeled items and linked items
python report.py $R                    # proposals with confidence -> report.md + actions.sh (gh commands, all commented out)
python build_html.py $R                # -> data/numpy__numpy/graph.html (open in a browser)
datasette $R                           # browse / SQL / full-text search
```

Tables: `items` (all states), `comments`, `links` (closes_official / closes / mentions / duplicate_of / sub_issue), `emb`, `categories`, `topics` (category + map position per item), `neighbors`, `similar` (semantic links), `pr_status`, `dup_pairs` / `dup_master` (duplicate candidates), `zombie`, `pr_compete`, `actions`, `suggested`, `fts`.

## AI Disclosure

Written with the help of Claude Code (Anthropic).

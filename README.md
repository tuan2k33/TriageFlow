# TriageFlow

Crawl all issues and PRs of a GitHub repo (open and closed, with conversation comments, content only, no code) into SQLite, then sort them into categories, suggest labels from the repo's existing ones and browse the open ones on a map. No LLM in the default flow.

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy       # all issues/PRs + comments + official PR->issue links (GitHub API; token from `gh auth token`); reruns sync only what changed
python analyze.py $R                   # embed new items (bge-small, fp16); categories are made once (--init to redo), new items join the nearest one
python suggest.py $R                   # type labels by kNN; component labels by a vote of kNN, linked items and title keywords
python build_html.py $R                # -> data/numpy__numpy/graph.html (open in a browser)
datasette $R                           # browse / SQL / full-text search
```

Optional, with an OpenRouter free model (kept for later): `analyze.py --init --llm-names`, `suggest.py --llm`, `resolve.py`, `summarize.py`, then `build_html.py --with-llm` to show their output.

Tables: `items` (all states), `comments`, `links` (closes_official / closes / mentions), `emb`, `categories`, `topics` (category + map position per item), `suggested`, `fts`; LLM only: `resolve_hints`, `summaries`.

## AI Disclosure

Written with the help of Claude Code (Anthropic).

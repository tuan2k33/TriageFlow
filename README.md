# TriageFlow

Crawl all issues and PRs of a GitHub repo (open and closed, with comments, content only, no code) into SQLite, then browse, cluster, label-suggest and graph the open ones.

```bash
R=data/numpy__numpy/repo.db
python triageflow.py numpy/numpy         # all issues/PRs + all comments + official PR->issue links; reruns sync only what changed
                                       #   (inline PR review comments are skipped; add --review-comments to fetch them)
python analyze.py $R                   # embed every item once (bge-small, fp16); topics + 2D map for open items
python suggest.py $R                   # suggest existing type/component labels for unlabeled open items (kNN over all labeled items, then free LLM)
python resolve.py $R                   # open issues that mention a merged PR: close / needs_decision / none (free LLM)
python summarize.py $R --max-calls 500 # one short summary per discussion (free LLM, ~1000 req/day, resumable, open first)
python build_html.py $R                # -> data/numpy__numpy/graph.html (open in a browser)
datasette $R                           # browse / SQL / full-text search
```

Needs `gh` logged in. Tables: `items` (all states), `comments`, `links` (closes_official / closes / mentions), `emb`, `topics` (open only), `suggested`, `resolve_hints`, `summaries`, `fts`.

## AI Disclosure

Written with the help of Claude Code (Anthropic).

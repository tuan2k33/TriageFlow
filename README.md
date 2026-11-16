# repolens

Crawl open issues and PRs of a GitHub repo (content only, no code) into SQLite, then browse, cluster and graph them.

```bash
R=data/numpy__numpy/repo.db
python repolens.py numpy/numpy --csv   # crawl -> $R (+ csv); rerun to sync only what changed
python analyze.py $R                   # embed (bge-small, fp16), KMeans topics, t-SNE 2D -> table `topics`
python build_html.py $R                # -> data/numpy__numpy/graph.html (open in a browser)
datasette $R                           # browse / SQL / full-text search
```

Needs `gh` logged in. Tables: `items`, `comments`, `links` (closes/mentions), `topics`, `fts`.

## AI Disclosure

Written with the help of Claude Code (Anthropic).

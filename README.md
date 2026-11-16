# repolens

Crawl open issues and PRs of a GitHub repo (content only, no code) into SQLite, then browse, cluster and graph them.

```bash
python repolens.py numpy/numpy --csv   # -> data/numpy__numpy/repo.db (+ csv); rerun to sync only what changed
datasette data/numpy__numpy/repo.db    # browse / SQL / full-text search
```

Needs `gh` logged in.

## AI Disclosure

Written with the help of Claude Code (Anthropic).

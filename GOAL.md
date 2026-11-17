# 🎯 TriageFlow: Smart Issue & PR Triage Engine

Legend: ✅ done · 🟡 partly done · ⬜ not done. Status is measured on real data from `numpy/numpy` (33,067 issues/PRs, 2,251 open; crawled 2026-11-16).

## 1. Vision and core value
A tool that analyses, organises and cleans up a GitHub repository from the **metadata and text of its issues and pull requests**, without reading source code or diffs.

* **Light and cheap:** only text meaning (titles, descriptions, comments) and the link graph. Saves GitHub requests (100 items per page, comments fetched repo-wide, incremental sync) and compute (embeddings run locally on a small GPU).
* **A real pain point:** turn thousands of messy issues/PRs into lists that are easy to filter and act on (group, close, label) in a few clicks.
* **No LLM in the pipeline:** from the crawl to the report it is data analysis and classic machine learning on GitHub's data (text, labels, states, GraphQL links) and local embeddings. The LLM steps tried earlier (discussion summaries, close verdicts, LLM-picked labels, LLM-named categories) were removed. An LLM is used only afterwards, outside the pipeline, to recheck the report's rows.
* **End goal (not now):** zero setup, paste any public repo URL and get the analysis, with a full UI. See Phase 4.

---

## 2. Pipeline
1. **Input:** a GitHub repo link (`python run.py <link>`, or paste it in the local web view `web.py`). The end-to-end flow stops at the report; label suggestions (`--labels`) and the LLM recheck are optional steps.
2. **Crawl & storage** ✅ One crawl stores every issue/PR (open and closed), every conversation comment (inline PR review comments are off by default), labels and states (`state_reason`, `merged`) in SQLite. Links GitHub itself records come from GraphQL: which PR closes which issue (abandoned PRs included), which issue a maintainer marked as a duplicate of which, which issue is a sub-issue of which. Reruns only fetch what changed.
3. **Vectorize & links** ✅ One embedding per item (open and closed) from its title, description and an extractive digest of its comments. Hard links, and semantic links (two items in each other's top 5).
4. **Analysis:** categories made once (k = sqrt(open items), 8-60: the embedding has no natural cluster count, so k is a reading choice), new items assigned to existing ones ✅; label suggestions ✅; the PR status of each issue from its links ✅; duplicates, zombies, competing PRs, staleness ✅.
5. **Output & action:** a one-file HTML browser (filters, list of open items, details with a timeline, a type × component matrix) ✅; an overview, a Markdown report and a `gh` script to review ✅.
6. **Recheck (outside the pipeline):** `tools/llm_judge.py` has a free LLM read both items of each proposal; rows it doubts are reread by hand (`manual.jsonl`) ✅.

---

## 3. Features

### 3.1. Context graph and semantic search
When an issue/PR is selected, show everything connected to it:
* ✅ **Hard links:** PRs closing issues (GitHub's official links and `Fixes #12` in the item's own text), duplicates and parent/child issues recorded by GitHub, and cross-references in descriptions and comments (`#56`, `gh-56`, full same-repo URLs).
* ✅ **Semantic links:** issues/PRs about the same thing even when they never cite each other, closed ones included. Criterion: the two are in each other's top 5 (no absolute cosine cut separates them). On numpy: 35k pairs, 15% already hard-linked.
* ✅ **Timeline:** in an item's details, everything hard- or semantically linked to it (open and closed) in time order: where the bug started → how often it was reported again → whether a PR handled it → whether that PR is open, merged or abandoned.
* ✅ **Full-text search** over titles, descriptions and comments.

### 3.2. Actionable cleanup
* ✅ **Duplicates:** three levels for issue pairs: marked on GitHub (numpy: 74 pairs), likely (similarity ≥ 0.92; hand-graded ~79% the same problem, 0.91-0.92 only ~29%; when the older issue is closed the proposal is "check recurrence", not close), possible (each other's nearest issue). The **master issue** is GitHub's original if marked, otherwise the oldest of the direct pairs (no chaining: chains drift from "same problem" to "same topic"). With the thread digest the right original of a marked duplicate ranks first 47% of the time (title + description only: 36%). Proposals with a reason and a sample comment are in `report.md` and `actions.sh`.
* ✅ **Zombie issues (open although a merged PR solved them):** by links and PR state (merged closing PR, open PR, only abandoned PRs, no PR; numpy: 9 / 139 / 151 / 1617 open issues; issues with sub-issues are "tracking"), filterable in the page. When the author forgot to link: the open issue and a later merged PR are each other's nearest, similarity ≥ 0.88, no closing link (numpy: 72 issues; on closed issues with a known closing PR the rule is right 87%; 20 open ones by hand: 10 fixed, 6 partly, 4 only related).
* ✅ **Competing PRs:** two open PRs that close the same issue, or two very similar open PRs (≥ 0.92) by different authors (one author's similar PRs are a series). numpy: 5 + 3 pairs.
* ✅ **Staleness:** filter by last activity (within 1 year, 1-3, 3-5, over 5 years) instead of one fixed cut; numpy: 728 open items quiet for over 5 years. ⬜ "Belongs to an old version" is not detected.
* 🟡 **Reverted fixes:** the LLM recheck found that 3 of the 9 "closing PR merged" issues are open because the PR was reverted; the algorithm does not detect reverts yet (a PR titled `Revert "..."` would be enough).

### 3.3. Labels from the repo's own labels
Only **labels the repo already uses** are suggested, to issues/PRs that lack them. No new labels.
* ✅ **Title rules:** a prefix such as `BUG:` / `ENH:` → type, a component's name in the title (`f2py`, `np.ma`) → component. Learned from labeled items, kept only if right ≥ 85% on ≥ 20 items. numpy: prefixes cover 72% of items at 96%.
* ✅ **History:** kNN over the 10 nearest labeled items for the type (closed items included, so tens of thousands to learn from). Title rule first, then kNN: 93% coverage at 93% on held-out items (kNN alone 79% / 88%).
* ✅ **Components by vote:** each of the K most similar labeled items votes for its components, linked items add votes (official links weigh most); every component with ≥ m votes is suggested, possibly more than one. K and m are swept per repo (most found at exact-match precision ≥ 0.5; numpy: 15 and 4). Finds the real label for 72% of items that have one; by hand ~88% of suggested components are related (exact match 0.50 is a lower bound since real labels are often missing). Never `component: Other`, never for bot PRs, no `component: documentation` on Documentation items.
* ✅ **Scope:** every open item missing a type or a component (numpy: 1613 items, 503 type and 930 component suggestions), not only unlabeled ones.
* ✅ **Two axes:** type (Bug, Enhancement, Documentation...) and component (`component: ...`). **No** process labels (Close?, Needs decision, triaged...): those are the maintainers' judgement.
* ✅ **Suggestions stay apart from real labels** (own table, shown dashed), never overwrite them.
* ✅ **Bulk apply:** `report.py` writes a `gh issue edit --add-label` line per suggestion, to review and run.
* 🟡 **Any repo:** no hand-written axes needed. In a repo without numpy's label scheme every label in use is a candidate, and each is suggested only from the vote count at which the hidden-label test is right at least half the time; labels that do not follow from the text (mostly process labels) drop out. tqdm: 9/21 labels kept. ⬜ Labels of an unknown repo are not grouped into axes, and title rules only run in the numpy-style mode.

### 3.4. Discussion summary: not made
* An abstractive summary needs an LLM, so it is out of scope. An extractive digest of each thread (sentences picked by MMR, no generated text) exists and feeds the embedding, but is not shown as a summary. The outcome of a discussion is read from links, PR states and the item's timeline.

### 3.5. Triage health dashboard ✅
* ✅ **Fragmentation index:** distinct problems vs open issues, shown in the page corner (numpy: *1917 open issues ≈ 1802 problems*, from GitHub-marked and likely duplicates).
* ✅ **Hot spots:** categories with the most comments on open items, and the most discussed items, in the overview (click the repo name).
* ✅ **Type × component matrix:** open items by type (rows) and component (columns), or by last activity and content category in a repo without such labels; size = count, color = share quiet for 3+ years; click a cell to list its items.
* ✅ **Quick wins:** proposals sorted by the algorithm's confidence in the overview and in `report.md` (numpy: 195 items with a quick action besides labels, e.g. 9 open issues already marked as duplicates, 9 with a merged closing PR).

---

## 4. Design principles
* **Never touch code:** no source download, no diffs.
* **Human in the loop:** the tool only analyses and proposes. Any change on GitHub (closing, labeling) happens only when a person approves, or through a script they run themselves (every line commented out).
* **Honest confidence:** each proposal shows the algorithm's own score, 0-1 (similarity, kNN score, share of votes, a title rule's hit rate); 1.00 only when certainly right (a maintainer marked it on GitHub). No per-row percentage is derived from small samples. A separate Check column shows the LLM recheck and hand checks.
* **Measure before trusting:** every suggester is measured on data with known answers (labels hidden and predicted back, GitHub's own links, hand-graded samples).
* **Suggestions apart from the source data:** in their own tables, regenerated at will.
* **Rerunnable and frugal:** incremental sync, resumes after a cut or the rate limit.

---

## 5. Roadmap
- [x] **Phase 1 (core data & search):** crawler → SQLite → embedding → search and browse page (multi-label filters, hard links).
  - [x] Semantic links, timeline in each item's details.
  - A t-SNE 2D/3D point map was built and dropped: the embedding has no clean clusters, so the projection is a blur that shows no structure. The type × component matrix replaced it.
- [x] **Phase 2 (smart cleanup):**
  - [x] Categories made once at init, new items assigned to them.
  - [x] PR status of each issue from its links (no LLM).
  - [x] Duplicates + master issue (thresholds graded by hand and against GitHub-marked pairs), fragmentation index.
  - [x] Semantic zombies, competing PRs, staleness.
  - [x] Triage health overview.
  - [x] Embedding of the whole thread (title + description averaged with an extractive comment digest).
- [x] **Phase 3 (labeling & action):**
  - [x] Label suggestions: title rules, kNN for type, votes for components, no LLM.
  - [x] Confidence = the algorithm's score per row; Check column with LLM recheck + hand checks.
  - [x] `report.md` (folded sections, fixed-width tables) and `actions.sh` (`gh issue close ... --comment ...`, `gh issue edit --add-label`; all commented out).
- [x] One command from link to results (`run.py`) and a local web view to paste a link and see the four outputs (`web.py`: Browse, Report, Actions, Database).
- [x] Published: github.com/tuan2k33/TriageFlow, with numpy's report in `reports/numpy__numpy/`.
- [ ] **Phase 4 (end goal, not now):** zero setup for any repo (title rules and label axes learned for repos without numpy's scheme, thresholds checked per repo), revert detection, a full UI, direct execution through a GitHub token.

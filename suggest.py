"""Suggest existing labels for open items that lack them. Two modes, picked from the repo's own labels:

numpy scheme (labels match AXES): a type and components, as below.
any other repo: every label is a candidate, by the same vote count as components, and each label is suggested only from the
            vote count at which it was right at least half the time when hidden (measured on labeled items), so
            process labels that do not follow from the text drop out by themselves.


type:       kNN vote over embeddings of already-labeled items (open + closed).
component:  vote count: each of the K most similar labeled items gives one vote to each of its components, linked
            items add theirs (GitHub's closing links weigh most); every component with >= m votes is suggested. K and m are
            swept per repo: the pair that finds most with exact-match precision >= TARGET_PRECISION.
            Measured on a balanced held-out sample (items with and without a component).
Written to table `suggested` (score: kNN score, vote count, or a title rule's hit rate; share: votes / possible votes);
nothing touches the real labels.

usage: python suggest.py data/<owner>__<name>/repo.db [--unlabeled-only] [--eval-only]
"""
import argparse, collections, json, random, re, sqlite3
import numpy as np

AXES = {"type": r"^(0[0-7]|17|23|33) - ", "component": r"^component:"}  # type regex fits numpy's numbered scheme
K = 10  # numpy, at confidence >= 0.5: K=3 0.85 coverage / 0.84 precision, 5 0.82/0.86, 10 0.79/0.88, 15+ no better
KC_GRID, M_GRID = (3, 5, 7, 10, 15), (1, 2, 3, 4, 5)  # component vote: neighbors x minimum votes, swept per repo
TARGET_PRECISION = 0.5  # the sweep keeps the (neighbors, votes) pair that finds the most with exact-match precision >= this
# (exact match is a lower bound: on numpy, 5 neighbors / 2 votes measured 0.49 exact and ~88% related by hand; the user chose 0.5)
VAGUE = re.compile(r"(?i):\s*other$")  # "component: Other" says nothing; never suggested
MIN_LABEL_PRECISION, MIN_LABEL_TRIES = 0.5, 10  # other repos: a label is suggested only if the hidden-label test got it right this often
TITLE_PRECISION, TITLE_TRIES = 0.85, 20  # a title prefix ("BUG:") or a component named in the title is used only if it carries that label this often
PREFIX = re.compile(r"^\s*\[?([A-Za-z]{2,6})(?:[,/+ ]{1,3}[A-Za-z]{2,6}){0,3}\]?\s*:")  # bounded: an unbounded (a+)+ backtracks for minutes


def load(db):
    rows = db.execute("select i.number, i.title, coalesce(i.body,''), i.labels, i.state, e.vec from items i join emb e using(number) order by i.number").fetchall()
    E = np.stack([np.frombuffer(r[5], dtype=np.float16) for r in rows]).astype(np.float32)
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    return [r[:5] for r in rows], [r[0] for r in rows], E


def knn_probs(E, ax_all, allowed_ax, has_label, queries):
    """{query index: {label|None: score}} from the top-K most similar already-labeled items (open or closed).

    Each label is scored on its own: the weighted share of neighbors that carry it (labels overlap, so scores of
    one item may add up to more than 1).

    ax_all[i]: labels of item i on this axis; allowed_ax: labels of the current scheme (those used by open items).
    A neighbor whose only labels on this axis are obsolete is skipped; one with other labels but none on this axis votes None."""
    ax = [a & allowed_ax for a in ax_all]
    pop = np.array([i for i in range(len(E)) if has_label[i] and (not ax_all[i] or ax[i])])
    P = E[pop]
    out = {}
    for c in range(0, len(queries), 512):
        q = queries[c:c + 512]
        S = E[q] @ P.T
        for r, i in enumerate(q):
            S[r, pop == i] = -9
        for r, i in enumerate(q):
            top = np.argpartition(-S[r], K)[:K]
            w = np.exp(S[r, top] / 0.05)
            votes = collections.defaultdict(float)
            for j, wj in zip(top, w):
                for l in ax[pop[j]] or {None}:
                    votes[l] += float(wj)
            t = float(w.sum())
            out[i] = {l: v / t for l, v in votes.items()}
    return out


LINK_W = {"closes_official": 3.0, "closes": 2.0, "mentions": 1.0}


def link_votes(db, nums, truth_c):
    """{index: {label: votes}} from the component labels of linked items (both directions)."""
    idx = {n: i for i, n in enumerate(nums)}
    acc = collections.defaultdict(lambda: collections.defaultdict(float))
    for s, d, k in db.execute("select src, dst, kind from links"):
        if k in LINK_W and s in idx and d in idx:
            for a, b in ((idx[s], idx[d]), (idx[d], idx[s])):
                for l in truth_c[b]:
                    acc[a][l] += LINK_W[k] / len(truth_c[b])
    return acc


def component_votes(E, truth_c, has_label, queries, links, kc):
    """{query index: {label: votes}}: one vote from each of the kc most similar labeled items carrying the label
    (an item never votes for itself), plus the votes of linked items."""
    pop = np.where(has_label)[0]
    P = E[pop]
    out = {}
    for c in range(0, len(queries), 512):
        q = queries[c:c + 512]
        S = E[q] @ P.T
        for r, i in enumerate(q):
            S[r, pop == i] = -9
            v = collections.Counter(l for j in np.argpartition(-S[r], kc)[:kc] for l in truth_c[pop[j]])
            for l, w in links.get(i, {}).items():
                v[l] += w
            out[i] = dict(v)
    return out


def generic(db, a, rows, nums, E, labels, is_open):
    """Any repo: vote over all labels, keep the labels the vote gets right, suggest those to open items lacking them."""
    n = len(nums)
    has_label = np.array([bool(ls) for ls in labels])
    used = {l for i in range(n) if is_open[i] for l in labels[i]} or {l for ls in labels for l in ls}
    truth = [set(ls) & used for ls in labels]
    lv = link_votes(db, nums, truth)
    rnd = random.Random(0)
    lab_idx = [i for i in range(n) if has_label[i]]
    ev = rnd.sample(lab_idx, min(3000, len(lab_idx)))
    targets = [i for i in range(n) if is_open[i] and not (a.unlabeled_only and labels[i])]
    print(f"{n} items ({sum(is_open)} open, {len(lab_idx)} labeled); {len(used)} labels in use; hidden-label test on {len(ev)} items:")

    def thresholds(cv, kc):
        """per label, the fewest votes at which the hidden-label test is right often enough; labels that never get there are dropped"""
        need, hits_at = {}, {}
        for l in sorted(used):
            for m in range(2, 2 * kc + 1):
                hits = [l in truth[i] for i in ev if cv[i].get(l, 0) >= m]
                if len(hits) < MIN_LABEL_TRIES:
                    break
                if np.mean(hits) >= MIN_LABEL_PRECISION:
                    need[l], hits_at[l] = m, hits
                    break
        return need, hits_at, sum(sum(h) for h in hits_at.values())

    tried = {kc: thresholds(component_votes(E, truth, has_label, ev, lv, kc), kc) for kc in KC_GRID}
    for kc, (need, _, right) in tried.items():
        print(f"  {kc:2d} neighbors: {len(need)} labels kept, {right} right suggestions")
    KC = max(KC_GRID, key=lambda kc: tried[kc][2])
    need, hits_at, _ = tried[KC]
    print(f"  -> {KC} neighbors")
    for l in sorted(used):
        print(f"  keep  from {need[l]} votes: {np.mean(hits_at[l]):.2f} right of {len(hits_at[l]):4d} suggestions  {l}" if l in need else f"  drop  {l}")
    cv = component_votes(E, truth, has_label, sorted(set(ev) | set(targets)), lv, KC)
    calib = []
    for lo, hi in ((2, 3), (3, 4), (4, 99)):
        b = [l in truth[i] for i in ev for l, v in cv[i].items() if l in need and v >= need[l] and lo <= v < hi]
        calib.append([lo, round(float(np.mean(b)), 2) if b else None])
    pooled = [l in truth[i] for i in ev for l, v in cv[i].items() if l in need and v >= need[l]]
    calib = [[lo, p if p is not None else round(float(np.mean(pooled)), 2)] for lo, p in calib] if pooled else calib  # a vote count the test never saw
    print("calibration by votes (exact match):", calib)
    if a.eval_only:
        return
    bots = {r[0] for r in db.execute("select number from items where author like '%[bot]' or author like 'dependabot%'")}
    db.execute("drop table if exists suggested")
    db.execute("create table suggested(number integer, axis text, label text, score real, source text, share real)")
    db.execute("insert or replace into meta values('calibration', ?)", (json.dumps({"label": calib, "vote": {"neighbors": KC}}),))
    for i in targets:
        if nums[i] not in bots:
            for l, v in cv[i].items():
                if l in need and v >= need[l] and l not in labels[i]:
                    db.execute("insert into suggested values(?,?,?,?,'vote',?)", (nums[i], "label", l, float(v), v / (KC + sum(lv[i].values()))))
    db.commit()
    print(db.execute("select label, count(*) from suggested group by 1 order by 2 desc").fetchall())


def prefix(title):
    m = PREFIX.match(title or "")
    return m.group(1).upper() if m else None


def title_rules(titles, truth_t, truth_c, comps, learn):
    """Learned from the labeled items in `learn`: prefix -> type label, and component -> regex for its name in a title.
    Each rule is kept only if it carried the label in >= TITLE_PRECISION of >= TITLE_TRIES items (exact match: a lower bound);
    component names are measured on items that have some component label, since most items have none."""
    by = collections.defaultdict(collections.Counter)
    for i in learn:
        if truth_t[i] and prefix(titles[i]):
            by[prefix(titles[i])].update(truth_t[i])
    seen = collections.Counter(prefix(titles[i]) for i in learn if truth_t[i] and prefix(titles[i]))
    types = {}
    for pre, c in by.items():
        lab, k = c.most_common(1)[0]
        if seen[pre] >= TITLE_TRIES and k / seen[pre] >= TITLE_PRECISION:
            types[pre] = (lab, round(k / seen[pre], 2))
    names = {}
    for c in comps:
        s = c.split(":", 1)[1].strip()
        last = s.split(".")[-1]
        alts = {s.replace("numpy.", "")} | ({last} if len(last) > 3 and not last.startswith("_") else set())
        rx = re.compile(r"(?<![\w.])(?:np\.|numpy\.)?(?:" + "|".join(map(re.escape, sorted(alts))) + r")\b", re.I)
        hit = [c in truth_c[i] for i in learn if truth_c[i] and rx.search(titles[i])]  # among items that have a component at all
        if len(hit) >= TITLE_TRIES and np.mean(hit) >= TITLE_PRECISION:
            names[c] = (rx, round(float(np.mean(hit)), 2))
    return types, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--unlabeled-only", action="store_true", help="suggest only for open items with no label at all (default: every open item missing a type or a component)")
    ap.add_argument("--eval-only", action="store_true", help="only measure, do not touch the suggested table")
    a = ap.parse_args()
    db = sqlite3.connect(a.db, timeout=120)
    rows, nums, E = load(db)
    n = len(nums)
    labels = [json.loads(r[3] or "[]") for r in rows]
    has_label = [bool(ls) for ls in labels]
    is_open = [r[4] == "open" for r in rows]
    ax_all = {ax: [{l for l in ls if re.search(rx, l)} for ls in labels] for ax, rx in AXES.items()}
    allowed = {ax: {l for i in range(n) if is_open[i] for l in ax_all[ax][i] if not VAGUE.search(l)} for ax in AXES}  # current scheme
    truth = {ax: [ax_all[ax][i] & allowed[ax] for i in range(n)] for ax in AXES}
    if not all(allowed.values()):
        return generic(db, a, rows, nums, E, labels, is_open)
    print(f"{n} items ({sum(is_open)} open, {sum(has_label)} labeled); allowed: " + ", ".join(f"{ax} {len(allowed[ax])}" for ax in AXES))

    targets = [i for i in range(n) if is_open[i] and (not labels[i] if a.unlabeled_only else any(not ax_all[ax][i] for ax in AXES))]
    rnd = random.Random(0)
    ev = rnd.sample([i for i in range(n) if has_label[i]], min(3000, sum(has_label)))
    # balanced component sample: labeled items with a current component label vs labeled items with none at all
    pos = [i for i in range(n) if truth["component"][i]]
    neg = [i for i in range(n) if has_label[i] and not ax_all["component"][i]]
    base_rate = len(pos) / (len(pos) + len(neg))
    bal = rnd.sample(pos, min(600, len(pos))) + rnd.sample(neg, min(600, len(neg)))
    kn = knn_probs(E, ax_all["type"], allowed["type"], has_label, sorted(set(ev) | set(targets)))
    top = lambda i: max(kn[i].items(), key=lambda t: t[1])
    titles = [r[1] for r in rows]
    held = set(ev) | set(bal)
    tt, tc = title_rules(titles, truth["type"], truth["component"], sorted(allowed["component"]),
                         [i for i in range(n) if has_label[i] and i not in held])

    print(f"type, kNN leave-one-out on {len(ev)} random labeled items (top-1 in true labels):")
    e = [i for i in ev if truth["type"][i]]
    for t in (0.0, 0.5, 0.6, 0.7, 0.8):
        pred = [(i, top(i)) for i in e]
        pred = [(i, p) for i, p in pred if p[0] is not None and p[1] >= t]
        hit = sum(p[0] in truth["type"][i] for i, p in pred)
        print(f"    conf>={t:.1f}: coverage {len(pred)/len(e):.2f}  precision {hit/max(1,len(pred)):.2f}")
    guess = {i: tt[prefix(titles[i])][0] if prefix(titles[i]) in tt else top(i)[0] if top(i)[0] is not None and top(i)[1] >= 0.5 else None for i in e}
    byp = [i for i in e if prefix(titles[i]) in tt]
    print(f"  title prefix rules {', '.join(f'{k}->{v[0]}' for k, v in sorted(tt.items()))}: cover {len(byp)/len(e):.2f}, precision "
          f"{np.mean([guess[i] in truth['type'][i] for i in byp]):.2f}; prefix first, else kNN >= 0.5: coverage "
          f"{sum(g is not None for g in guess.values())/len(e):.2f}  precision {np.mean([g in truth['type'][i] for i, g in guess.items() if g]):.2f}")

    # component: vote count, measured on the balanced sample; tag precision rescaled to the real share of items with a component
    lv = link_votes(db, nums, truth["component"])
    bp, bn = [i for i in bal if truth["component"][i]], [i for i in bal if not ax_all["component"][i]]
    print(f"component vote, balanced sample {len(bp)} with / {len(bn)} without; {base_rate:.0%} of labeled items have one "
          f"(exact match: a lower bound, missing labels count as wrong); keep the pair that finds most at precision >= {TARGET_PRECISION}:")
    grid = []
    for kc in KC_GRID:
        cb = component_votes(E, truth["component"], has_label, sorted(bal), lv, kc)
        for m in M_GRID:
            sug = {i: {l for l, v in cb[i].items() if v >= m} for i in bal}
            right = np.mean([len(sug[i] & truth["component"][i]) for i in bp])
            tags_p, tags_n = np.mean([len(sug[i]) for i in bp]), np.mean([len(sug[i]) for i in bn])
            prec = right * base_rate / max(1e-9, tags_p * base_rate + tags_n * (1 - base_rate))
            grid.append((kc, m, float(np.mean([bool(sug[i] & truth["component"][i]) for i in bp])), float(prec), float(np.mean([bool(sug[i]) for i in bn]))))
    ok = [g for g in grid if g[3] >= TARGET_PRECISION]
    KC, MIN_VOTES = max(ok, key=lambda g: (g[2], g[3]))[:2] if ok else max(grid, key=lambda g: g[3])[:2]
    for kc, m, finds, prec, neg in grid:
        print(f"  {'->' if (kc, m) == (KC, MIN_VOTES) else '  '} {kc:2d} neighbors, >= {m} votes: finds {finds:.2f}  items without one get one {neg:.2f}  tag precision {prec:.2f}")
    cv = component_votes(E, truth["component"], has_label, sorted(set(bal) | set(targets)), lv, KC)
    # how often a suggestion with this score was right when the label was hidden: shown next to each label suggestion
    best = [(i, top(i)) for i in e]
    calib = {"type": [], "component": []}
    for lo, hi in ((0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 1.01)):
        b = [l in truth["type"][i] for i, (l, p) in best if l is not None and lo <= p < hi]
        calib["type"].append([lo, round(float(np.mean(b)), 2) if b else None])
    for lo, hi in ((MIN_VOTES, MIN_VOTES + 1), (MIN_VOTES + 1, MIN_VOTES + 2), (MIN_VOTES + 2, 99)):
        tags = [(l in truth["component"][i], bool(truth["component"][i])) for i in bal for l, v in cv[i].items() if lo <= v < hi]
        right, wrong_p = sum(r for r, _ in tags) / len(bp), sum(not r and p for r, p in tags) / len(bp)
        on_neg = sum(not p for _, p in tags) / len(bn)
        calib["component"].append([lo, round(right * base_rate / max(1e-9, (right + wrong_p) * base_rate + on_neg * (1 - base_rate)), 2)])
    calib["title"] = {pre: p for pre, (_, p) in tt.items()} | {c: p for c, (_, p) in tc.items()}
    calib["vote"] = {"neighbors": KC, "min_votes": MIN_VOTES}
    print("component named in the title, kept: " + ", ".join(f"{c.split(':', 1)[1].strip()} {p:.2f}" for c, (_, p) in sorted(tc.items())))
    print("calibration (exact match):", calib)
    bots = {r[0] for r in db.execute("select number from items where author like '%[bot]' or author like 'dependabot%'")}
    print(f"targets: {len(targets)} open items")

    if not a.eval_only:
        db.execute("drop table if exists suggested")
        db.execute("create table suggested(number integer, axis text, label text, score real, source text, share real)")
        db.execute("insert or replace into meta values('calibration', ?)", (json.dumps(calib),))
        for i in targets:
            l, p = top(i)
            typ = set(ax_all["type"][i])
            pre = prefix(titles[i])
            if not typ and pre in tt:  # the author's own "BUG:" beats the neighbors (numpy: kNN right 25% where they disagree)
                db.execute("insert into suggested values(?,?,?,?,'title',null)", (nums[i], "type", tt[pre][0], tt[pre][1]))
                typ.add(tt[pre][0])
            elif l is not None and p >= 0.5 and not typ:
                db.execute("insert into suggested values(?,?,?,?,'knn',null)", (nums[i], "type", l, float(p)))
                typ.add(l)
            if ax_all["component"][i] or nums[i] in bots:
                continue
            named = {c: q for c, (rx, q) in tc.items() if rx.search(titles[i])}
            for c, q in named.items():
                db.execute("insert into suggested values(?,?,?,?,'title',null)", (nums[i], "component", c, q))
            for l, v in cv[i].items():
                if v < MIN_VOTES or l in named or ("documentation" in l.lower() and any("documentation" in t.lower() for t in typ)):
                    continue  # too few votes, already named in the title, or says the same thing as the type label
                db.execute("insert into suggested values(?,?,?,?,'vote',?)", (nums[i], "component", l, float(v), v / (KC + sum(lv[i].values()))))
        db.commit()

    db.commit()
    print(db.execute("select source, axis, count(*) from suggested group by 1,2").fetchall())


if __name__ == "__main__":
    main()

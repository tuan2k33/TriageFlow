"""Suggest existing labels (type + component axes) for unlabeled open items. No LLM by default.

type:       kNN vote over embeddings of already-labeled items (open + closed).
component:  weighted vote of three sources, each measured on a balanced held-out sample (items with and without a
            component): kNN, labels of linked items (GitHub's closing links weigh most), and keywords of the title and
            description (naive Bayes learned from labeled items).
--llm:      optionally let an OpenRouter free model pick from the allowed labels with kNN hints (kept for later).
Written to table `suggested`; nothing touches the real labels.

usage: python suggest.py data/<owner>__<name>/repo.db [--all] [--llm [--eval-only] [--eval-n 60]]
"""
import argparse, collections, json, os, random, re, sqlite3, time, urllib.request, urllib.error
import numpy as np

AXES = {"type": r"^(0[0-7]|17|23|33) - ", "component": r"^component:"}  # type regex fits numpy's numbered scheme
MODEL = os.environ.get("LLM_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")
K = 5  # measured: same recall as 15 at a lower threshold, and closer to the item when labels are missing
BATCH = 20


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


TOKEN = re.compile(r"[a-z_][a-z0-9_.]+")
LINK_W = {"closes_official": 3.0, "closes": 2.0, "mentions": 1.0}
COMBOS = {"knn": (1, 0, 0), "links": (0, 1, 0), "keywords": (0, 0, 1), "knn+keywords": (1, 0, 1),
          "all 1:1:1": (1, 1, 1), "all 1:2:1": (1, 2, 1), "all 2:1:1": (2, 1, 1), "all 1:1:2": (1, 1, 2)}


def tokens(title, body):
    return set(TOKEN.findall((title or "").lower())) | set(TOKEN.findall((body or "")[:1500].lower()))


class KeywordNB:
    """Binary naive Bayes over title/description tokens; classes are component labels and None."""

    def fit(self, docs, ys):
        self.prior = collections.Counter()
        self.cnt = collections.defaultdict(collections.Counter)
        df = collections.Counter()
        for d, labs in zip(docs, ys):
            df.update(d)
            for y in labs or {None}:
                self.prior[y] += 1
                self.cnt[y].update(d)
        self.vocab = {t for t, c in df.items() if c >= 3}
        self.total = sum(self.prior.values())
        V = len(self.vocab)
        self.denom = {y: sum(c for t, c in self.cnt[y].items() if t in self.vocab) + V for y in self.prior}  # tokens of class + |V|
        return self

    def proba(self, d):
        d = d & self.vocab
        s = {y: np.log(py / self.total) + sum(np.log((self.cnt[y][t] + 1) / self.denom[y]) for t in d) for y, py in self.prior.items()}
        m = max(s.values())
        T = max(1.0, len(d) ** 0.5)  # NB is overconfident on long texts: soften by the number of tokens
        e = {y: np.exp((v - m) / T) for y, v in s.items()}
        z = sum(e.values())
        return {y: v / z for y, v in e.items()}


def link_votes(db, nums, truth_c):
    """{index: {label: weight share}} from the component labels of linked items (both directions)."""
    idx = {n: i for i, n in enumerate(nums)}
    acc = collections.defaultdict(lambda: collections.defaultdict(float))
    for s, d, k in db.execute("select src, dst, kind from links"):
        if s in idx and d in idx:
            for a, b in ((idx[s], idx[d]), (idx[d], idx[s])):
                for l in truth_c[b]:
                    acc[a][l] += LINK_W[k] / len(truth_c[b])
    return acc


def combine(w, pk, pl, pn):
    """Weighted mix of the three distributions; a source with no evidence for this item is left out."""
    parts = [(w[0], pk), (w[1], {l: v / sum(pl.values()) for l, v in pl.items()} if pl else None), (w[2], pn)]
    parts = [(a, p) for a, p in parts if a and p]
    z = sum(a for a, _ in parts)
    out = collections.defaultdict(float)
    for a, p in parts:
        for l, v in p.items():
            out[l] += a * v / z
    return out


def call_llm(prompt, key):
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0, "max_tokens": 12000}).encode()
    for attempt in range(6):
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", body,
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                ch = json.load(r)["choices"][0]
                if ch["message"].get("content"):
                    return ch["message"]["content"]
                print(f"  empty content, finish={ch.get('finish_reason')}", flush=True)
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}", flush=True)
            if e.code not in (429, 502, 503):
                raise
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  {type(e).__name__}: {e}", flush=True)
        time.sleep(10 * 2 ** attempt)
    raise RuntimeError("LLM call failed")


def llm_batch(items, allowed, hints, key):
    lines = []
    for n, title, body in items:
        h = "; ".join(f"{ax}: " + ", ".join(f"{l or 'none'} {p:.2f}" for l, p in hints[n][ax]) for ax in AXES)
        lines.append(f"[{n}] {title}\n    {re.sub(r'\s+', ' ', body)[:200]}\n    hints: {h}")
    prompt = (
        "You triage GitHub issues/PRs. For each item pick ONE label per axis from the allowed lists, or null if none fits.\n"
        "Use only labels from the lists, never invent new ones. 'hints' are label votes from similar already-labeled items.\n\n"
        + "\n".join(f"Allowed {ax} labels: {json.dumps(allowed[ax])}" for ax in AXES)
        + "\n\nItems:\n" + "\n".join(lines)
        + '\n\nAnswer with only a JSON array: [{"id": <number>, "type": <label or null>, "component": <label or null>}, ...]')
    txt = call_llm(prompt, key)
    m = re.search(r"\[.*\]", txt, re.S)
    res = {}
    for o in json.loads(m.group(0)):
        res[int(o["id"])] = {ax: (o.get(ax) if o.get(ax) in allowed[ax] else None) for ax in AXES}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--all", action="store_true", help="suggest for every open item missing an axis, not only fully unlabeled ones")
    ap.add_argument("--llm", action="store_true", help="also ask the free LLM (off by default)")
    ap.add_argument("--eval-only", action="store_true", help="with --llm: only measure LLM vs kNN, do not touch the suggested table")
    ap.add_argument("--eval-n", type=int, default=60)
    ap.add_argument("--min-precision", type=float, default=0.9, help="component votes are kept only above the threshold reaching this precision")
    a = ap.parse_args()
    db = sqlite3.connect(a.db, timeout=120)
    rows, nums, E = load(db)
    n = len(nums)
    labels = [[l for l in (r[3] or "").split(",") if l] for r in rows]
    has_label = [bool(ls) for ls in labels]
    is_open = [r[4] == "open" for r in rows]
    ax_all = {ax: [{l for l in ls if re.search(rx, l)} for ls in labels] for ax, rx in AXES.items()}
    allowed = {ax: {l for i in range(n) if is_open[i] for l in ax_all[ax][i]} for ax in AXES}  # labels of the current scheme
    truth = {ax: [ax_all[ax][i] & allowed[ax] for i in range(n)] for ax in AXES}
    if not all(allowed.values()):
        print("this repo's labels do not match the type/component patterns in AXES; nothing to suggest")
        return
    print(f"{n} items ({sum(is_open)} open, {sum(has_label)} labeled); allowed: " + ", ".join(f"{ax} {len(allowed[ax])}" for ax in AXES))

    targets = [i for i in range(n) if is_open[i] and (not labels[i] if not a.all else any(not ax_all[ax][i] for ax in AXES))]
    rnd = random.Random(0)
    ev = rnd.sample([i for i in range(n) if has_label[i]], min(3000, sum(has_label)))
    # balanced component sample: labeled items with a current component label vs labeled items with none at all
    pos = [i for i in range(n) if truth["component"][i]]
    neg = [i for i in range(n) if has_label[i] and not ax_all["component"][i]]
    base_rate = len(pos) / (len(pos) + len(neg))
    bal = rnd.sample(pos, min(600, len(pos))) + rnd.sample(neg, min(600, len(neg)))
    both = [i for i in ev if all(truth[ax][i] for ax in AXES)] or ev
    llm_ev = rnd.sample(both, min(a.eval_n, len(both)))
    Q = sorted(set(ev) | set(targets) | set(llm_ev) | set(bal))
    kn = {ax: knn_probs(E, ax_all[ax], allowed[ax], has_label, Q) for ax in AXES}

    def top(ax, i, k=1):
        return sorted(kn[ax][i].items(), key=lambda t: -t[1])[:k]

    print(f"type, kNN leave-one-out on {len(ev)} random labeled items (top-1 in true labels):")
    e = [i for i in ev if truth["type"][i]]
    for t in (0.0, 0.5, 0.6, 0.7, 0.8):
        pred = [(i, top("type", i)[0]) for i in e]
        pred = [(i, p) for i, p in pred if p[0] is not None and p[1] >= t]
        hit = sum(p[0] in truth["type"][i] for i, p in pred)
        print(f"    conf>={t:.1f}: coverage {len(pred)/len(e):.2f}  precision {hit/max(1,len(pred)):.2f}")

    # component: three sources, measured on the balanced sample, precision rescaled to the real share of items with a component
    docs = [tokens(r[1], r[2]) for r in rows]
    held = set(bal)
    train = [i for i in range(n) if has_label[i] and i not in held and (truth["component"][i] or not ax_all["component"][i])]
    nb = KeywordNB().fit([docs[i] for i in train], [truth["component"][i] for i in train])
    lv = link_votes(db, nums, truth["component"])
    print(f"component, balanced sample {len(bal)} ({min(600, len(pos))} with /{min(600, len(neg))} without);"
          f" {base_rate:.0%} of labeled items have one; links available for {sum(1 for i in bal if lv.get(i)) / len(bal):.0%} of the sample")
    best = None
    for name, w in COMBOS.items():
        pred = {}
        for i in bal:
            p = combine(w, kn["component"][i], lv.get(i), nb.proba(docs[i]))
            pred[i] = max(p.items(), key=lambda t: t[1]) if p else (None, 0.0)
        line = []
        for t in (0.3, 0.4, 0.5, 0.6, 0.7):
            sp = [i for i in bal if truth["component"][i] and pred[i][0] is not None and pred[i][1] >= t]
            tp = sum(pred[i][0] in truth["component"][i] for i in sp) / min(600, len(pos))   # right label, among items with one
            wrong = (len(sp) / min(600, len(pos))) - tp                                      # wrong label, among items with one
            fa = sum(1 for i in bal if not ax_all["component"][i] and pred[i][0] is not None and pred[i][1] >= t) / min(600, len(neg))
            prec = tp * base_rate / max(1e-9, (tp + wrong) * base_rate + fa * (1 - base_rate))
            line.append(f"t{t}: found {tp:.2f} false-alarm {fa:.2f} precision {prec:.2f}")
            if prec >= a.min_precision and (best is None or tp > best[0]):
                best = (tp, name, w, t, prec)
        print(f"  {name:12} " + " | ".join(line))
    if best:
        print(f"  -> using {best[1]} at conf>={best[3]} (finds {best[0]:.0%} of components, precision {best[4]:.2f})")
    else:
        print(f"  -> no combination reaches precision {a.min_precision}; no component suggestions")
    print(f"targets: {len(targets)} open items")

    if not a.eval_only:
        db.execute("create table if not exists suggested(number integer, axis text, label text, score real, source text)")
        db.execute("delete from suggested where source in ('knn','vote')")
        for i in targets:
            l, p = top("type", i)[0]
            if l is not None and p >= 0.5:
                db.execute("insert into suggested values(?,?,?,?,'knn')", (nums[i], "type", l, float(p)))
            if best and not ax_all["component"][i]:
                pr = combine(best[2], kn["component"][i], lv.get(i), nb.proba(docs[i]))
                l, p = max(pr.items(), key=lambda t: t[1])
                if l is not None and p >= best[3]:
                    db.execute("insert into suggested values(?,?,?,?,'vote')", (nums[i], "component", l, float(p)))
        db.commit()

    if a.llm:
        allowed_l = {ax: sorted(allowed[ax]) for ax in AXES}
        hints = {nums[i]: {ax: top(ax, i, 2) for ax in AXES} for i in Q}
        key = next(l.split("=", 1)[1].strip().strip("'\"") for l in open(".env") if l.startswith("OPENROUTER_API_KEY="))
        if a.eval_only:
            print(f"LLM eval on {len(llm_ev)} labeled items (truth hidden from the model; hints are leave-one-out):")
            got = {}
            for b in range(0, len(llm_ev), BATCH):
                got.update(llm_batch([(nums[i], rows[i][1], rows[i][2]) for i in llm_ev[b:b + BATCH]], allowed_l, hints, key))
                time.sleep(3.5)
            for ax in AXES:
                m = [(i, got.get(nums[i], {}).get(ax)) for i in llm_ev if truth[ax][i]]
                kh = sum((top(ax, i)[0][0] in truth[ax][i]) for i, _ in m)
                lh = sum(p in truth[ax][i] for i, p in m)
                print(f"  {ax}: n={len(m)}  kNN top-1 {kh/len(m):.2f}  LLM {lh/len(m):.2f}")
            return
        done = {r[0] for r in db.execute("select distinct number from suggested where source='llm'")}
        todo = [i for i in targets if nums[i] not in done]
        print(f"LLM on {len(todo)} targets ({len(targets) - len(todo)} already have LLM suggestions):")
        for b in range(0, len(todo), BATCH):
            ch = todo[b:b + BATCH]
            res = llm_batch([(nums[i], rows[i][1], rows[i][2]) for i in ch], allowed_l, hints, key)
            for i in ch:
                for ax, l in res.get(nums[i], {}).items():
                    if l:
                        db.execute("insert into suggested values(?,?,?,?,'llm')", (nums[i], ax, l, float(kn[ax][i].get(l, 0.0))))
            db.commit()
            print(f"  {min(b + BATCH, len(todo))}/{len(todo)}", flush=True)
            time.sleep(3.5)
    db.commit()
    print(db.execute("select source, axis, count(*) from suggested group by 1,2").fetchall())


if __name__ == "__main__":
    main()

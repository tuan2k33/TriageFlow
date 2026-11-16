"""Suggest existing labels (type + component axes) for unlabeled items.

Step 1: kNN vote over embeddings of already-labeled items (free, local), with leave-one-out accuracy.
Step 2: LLM (OpenRouter free model) picks from the allowed labels, in batches, with kNN hints.
Both are written to table `suggested`; nothing touches the real labels.

usage: python suggest.py data/<owner>__<name>/repo.db [--no-llm] [--all] [--eval-n 60]
"""
import argparse, collections, json, os, random, re, sqlite3, time, urllib.request, urllib.error
import numpy as np

AXES = {"type": r"^(0[0-7]|17|23|33) - ", "component": r"^component:"}  # type regex fits numpy's numbered scheme
MODEL = os.environ.get("LLM_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")
K = 15
BATCH = 20


def load(db):
    rows = db.execute("select i.number, i.title, coalesce(i.body,''), i.labels, i.state, e.vec from items i join emb e using(number) order by i.number").fetchall()
    E = np.stack([np.frombuffer(r[5], dtype=np.float16) for r in rows]).astype(np.float32)
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    return [r[:5] for r in rows], [r[0] for r in rows], E


def knn_probs(E, ax_all, allowed_ax, has_label, queries):
    """{query index: {label|None: prob}} from the top-K most similar already-labeled items (open or closed).

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
                labs = ax[pop[j]] or {None}
                for l in labs:
                    votes[l] += float(wj) / len(labs)
            t = sum(votes.values())
            out[i] = {l: v / t for l, v in votes.items()}
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
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--all", action="store_true", help="suggest for every open item missing an axis, not only fully unlabeled ones")
    ap.add_argument("--eval-only", action="store_true", help="only measure LLM vs kNN, do not touch the suggested table")
    ap.add_argument("--eval-n", type=int, default=60)
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
    both = [i for i in ev if all(truth[ax][i] for ax in AXES)] or ev
    llm_ev = rnd.sample(both, min(a.eval_n, len(both)))
    Q = sorted(set(ev) | set(targets) | set(llm_ev))
    kn = {ax: knn_probs(E, ax_all[ax], allowed[ax], has_label, Q) for ax in AXES}

    def top(ax, i, k=1):
        return sorted(kn[ax][i].items(), key=lambda t: -t[1])[:k]

    print(f"kNN leave-one-out on {len(ev)} random labeled items (top-1 non-none prediction in true labels):")
    for ax in AXES:
        e = [i for i in ev if truth[ax][i]]
        print(f"  {ax}: {len(e)} items with a true label")
        for t in (0.0, 0.5, 0.6, 0.7, 0.8):
            pred = [(i, top(ax, i)[0]) for i in e]
            pred = [(i, p) for i, p in pred if p[0] is not None and p[1] >= t]
            hit = sum(p[0] in truth[ax][i] for i, p in pred)
            print(f"    conf>={t:.1f}: coverage {len(pred)/len(e):.2f}  precision {hit/max(1,len(pred)):.2f}")
    print(f"targets: {len(targets)} open items")

    allowed_l = {ax: sorted(allowed[ax]) for ax in AXES}
    hints = {nums[i]: {ax: top(ax, i, 2) for ax in AXES} for i in Q}
    if not a.eval_only:
        db.execute("create table if not exists suggested(number integer, axis text, label text, score real, source text)")
        db.execute("delete from suggested where source='knn'")
        for i in targets:
            for ax in AXES:
                l, p = top(ax, i)[0]
                if l is not None and p >= 0.5:
                    db.execute("insert into suggested values(?,?,?,?,'knn')", (nums[i], ax, l, float(p)))
        db.commit()

    if not a.no_llm:
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

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
    rows = db.execute("select number, title, coalesce(body,''), labels from items order by number").fetchall()
    nums = [r[0] for r in rows]
    E = np.stack([np.frombuffer(db.execute("select vec from emb where number=?", (n,)).fetchone()[0], dtype=np.float16)
                  for n in nums]).astype(np.float32)
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    return rows, nums, E


def knn_probs(E, labels, axis_re, population):
    """per item: {label|None: prob} from top-K most similar items in `population` (items with >=1 label)."""
    ax = [{l for l in ls if re.search(axis_re, l)} for ls in labels]
    S = E @ E[population].T
    pop = np.array(population)
    out = []
    for i in range(len(E)):
        s = S[i].copy()
        s[pop == i] = -9
        top = np.argsort(-s)[:K]
        w = np.exp(s[top] / 0.05)
        votes = collections.defaultdict(float)
        for j, wj in zip(top, w):
            for l in (ax[pop[j]] or {None}):
                votes[l] += wj / len(ax[pop[j]] or {None})
        t = sum(votes.values())
        out.append({l: v / t for l, v in votes.items()})
    return out, ax


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
    ap.add_argument("--all", action="store_true", help="suggest for every item missing an axis, not only fully unlabeled ones")
    ap.add_argument("--eval-only", action="store_true", help="only measure LLM vs kNN, do not touch the suggested table")
    ap.add_argument("--eval-n", type=int, default=60)
    a = ap.parse_args()
    db = sqlite3.connect(a.db)
    rows, nums, E = load(db)
    labels = [[l for l in (r[3] or "").split(",") if l] for r in rows]
    population = [i for i, ls in enumerate(labels) if ls]
    allowed = {ax: sorted({l for ls in labels for l in ls if re.search(rx, l)}) for ax, rx in AXES.items()}
    kn, truth = {}, {}
    for ax, rx in AXES.items():
        kn[ax], truth[ax] = knn_probs(E, labels, rx, population)

    def top(ax, i, n=1):
        return sorted(kn[ax][i].items(), key=lambda t: -t[1])[:n]

    print("kNN leave-one-out on labeled items (top-1 non-none prediction in true labels):")
    for ax in AXES:
        ev = [i for i in population if truth[ax][i]]
        print(f"  {ax}: {len(ev)} items with a true label")
        for t in (0.0, 0.5, 0.6, 0.7, 0.8):
            pred = [(i, top(ax, i)[0]) for i in ev]
            pred = [(i, p) for i, p in pred if p[0] is not None and p[1] >= t]
            hit = sum(p[0] in truth[ax][i] for i, p in pred)
            print(f"    conf>={t:.1f}: coverage {len(pred)/len(ev):.2f}  precision {hit/max(1,len(pred)):.2f}")

    targets = [i for i in range(len(nums)) if (not labels[i] if not a.all else any(not truth[ax][i] for ax in AXES))]
    print(f"targets: {len(targets)} items")
    hints = {nums[i]: {ax: top(ax, i, 2) for ax in AXES} for i in range(len(nums))}

    if not a.eval_only:
        db.execute("drop table if exists suggested")
        db.execute("create table suggested(number integer, axis text, label text, score real, source text)")
    for i in [] if a.eval_only else targets:
        for ax in AXES:
            l, p = top(ax, i)[0]
            if l is not None and p >= 0.5:
                db.execute("insert into suggested values(?,?,?,?,'knn')", (nums[i], ax, l, float(p)))

    if not a.no_llm:
        key = next(l.split("=", 1)[1].strip().strip("'\"") for l in open(".env") if l.startswith("OPENROUTER_API_KEY="))
        rnd = random.Random(0)
        ev = rnd.sample([i for i in population if all(truth[ax][i] for ax in AXES)] or population, a.eval_n)
        print(f"LLM eval on {len(ev)} labeled items (truth hidden from the model; hints are leave-one-out):")
        got = {}
        for b in range(0, len(ev), BATCH):
            got.update(llm_batch([(nums[i], rows[i][1], rows[i][2]) for i in ev[b:b + BATCH]], allowed, hints, key))
            time.sleep(3.5)
        for ax in AXES:
            m = [(i, got.get(nums[i], {}).get(ax)) for i in ev if truth[ax][i]]
            kh = sum((top(ax, i)[0][0] in truth[ax][i]) for i, _ in m)
            lh = sum(p in truth[ax][i] for i, p in m)
            print(f"  {ax}: n={len(m)}  kNN top-1 {kh/len(m):.2f}  LLM {lh/len(m):.2f}")
        if a.eval_only:
            return
        print(f"LLM on {len(targets)} targets:")
        for b in range(0, len(targets), BATCH):
            ch = targets[b:b + BATCH]
            res = llm_batch([(nums[i], rows[i][1], rows[i][2]) for i in ch], allowed, hints, key)
            for i in ch:
                for ax, l in res.get(nums[i], {}).items():
                    if l:
                        db.execute("insert into suggested values(?,?,?,?,'llm')", (nums[i], ax, l, float(kn[ax][i].get(l, 0.0))))
            db.commit()
            print(f"  {min(b + BATCH, len(targets))}/{len(targets)}", flush=True)
            time.sleep(3.5)
    db.commit()
    print(db.execute("select source, axis, count(*) from suggested group by 1,2").fetchall())


if __name__ == "__main__":
    main()

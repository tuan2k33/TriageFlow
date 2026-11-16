"""Embed items, keep them sorted into categories, and keep a stable 2D map of the open ones.

usage: python analyze.py data/<owner>__<name>/repo.db [--init] [--k N] [--llm-names]

Categories are made once (first run, or --init): KMeans over the embeddings of every item (open + closed), each
category stored as a normalized centroid and named after its most common labels (or once by the LLM with --llm-names). Later runs only embed new items, put each into the
nearest existing category (or -1 "Unsorted" when it is far from all of them) and place new open items on the map at the
average position of their nearest already-placed neighbors, so categories and the map do not move between runs.

Tables: emb(number, vec), categories(id, name, size, centroid), topics(number, cluster, sim, x, y),
neighbors(number, rank, other, sim): the 5 most similar items of every item.
"""
import argparse, collections, json, os, re, sqlite3, time
import importlib.util
import numpy as np
import torch
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from transformers import AutoModel, AutoTokenizer

MODEL = "BAAI/bge-small-en-v1.5"
NEIGHBORS = 8


def embed(texts):
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModel.from_pretrained(MODEL, dtype=torch.float16).cuda().eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(texts), 64):
            b = tok(texts[i:i + 64], padding=True, truncation=True, max_length=256, return_tensors="pt").to("cuda")
            v = model(**b).last_hidden_state[:, 0].float()
            out.append(torch.nn.functional.normalize(v, dim=-1).cpu())
    return torch.cat(out).numpy()


def unit(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)


def load_emb(db, where="1"):
    rows = db.execute(f"select i.number, i.state, e.vec from items i join emb e using(number) where {where} order by i.number").fetchall()
    if not rows:
        return [], [], np.zeros((0, 384), dtype=np.float32)
    return [r[0] for r in rows], [r[1] for r in rows], unit(np.stack([np.frombuffer(r[2], dtype=np.float16) for r in rows]).astype(np.float32))


def embed_new(db):
    todo = db.execute("select number, title, coalesce(body,'') from items where number not in (select number from emb) order by number").fetchall()
    print(f"embedding {len(todo)} new items", flush=True)
    if not todo:
        return
    texts = [f"{t}\n{b[:1500]}" for _, t, b in todo]
    order = sorted(range(len(texts)), key=lambda i: len(texts[i]))  # similar lengths per batch = less padding
    vecs = embed([texts[i] for i in order])
    for j, i in enumerate(order):
        db.execute("insert or replace into emb values(?,?)", (todo[i][0], vecs[j].astype(np.float16).tobytes()))
    db.commit()


STOP = set("""a an the and or of to in on for with without is are be not no when from by as at it its this that into via
use using add added adding fix fixed fixes support allow make should can does do don't doesn't wrong error fails failing incorrect
bug enh doc docs maint bld typ tst api dep rel dev ci sim numpy np array arrays""".split())


def distinctive_names(members, titles, labels):
    """Name = the label most over-represented in the category (if any) + its most over-represented title words."""
    N = sum(len(ns) for ns in members.values())
    words = {n: set(w for w in re.findall(r"[a-z_][a-z0-9_.]+", t.lower()) if w not in STOP and len(w) > 2) for n, t in titles.items()}
    lab_all = collections.Counter(l for ns in members.values() for n in ns for l in labels[n])
    w_all = collections.Counter(w for ns in members.values() for n in ns for w in words[n])
    names = {}
    for c, ns in members.items():
        m = len(ns)
        lift = lambda k, tot: (k / m) / (tot / N)
        lc = collections.Counter(l for n in ns for l in labels[n])
        lab = [l for l, k in lc.items() if k >= 0.2 * m and lift(k, lab_all[l]) >= 2]
        wc = collections.Counter(w for n in ns for w in words[n])
        top = sorted((w for w, k in wc.items() if k >= max(5, 0.04 * m)), key=lambda w: -lift(wc[w], w_all[w]) * wc[w] ** 0.5)[:3]
        lab = max(lab, key=lambda l: lift(lc[l], lab_all[l]), default=None)
        names[c] = ": ".join(x for x in (lab, ", ".join(top)) if x) or titles[ns[0]][:60]
    return names


def neighbors(db, k=5):
    """Top-k most similar items for every item (open or closed), recomputed each run: new items can be anyone's neighbor."""
    nums, _, E = load_emb(db)
    rows = []
    for c in range(0, len(nums), 1000):
        S = E[c:c + 1000] @ E.T
        S[np.arange(S.shape[0]), np.arange(c, c + S.shape[0])] = -9  # not itself
        top = np.argpartition(-S, k, axis=1)[:, :k]
        for r, t in enumerate(top):
            t = t[np.argsort(-S[r, t])]
            rows += [(nums[c + r], rank, nums[j], float(S[r, j])) for rank, j in enumerate(t)]
    db.execute("drop table if exists neighbors")
    db.execute("create table neighbors(number integer, rank integer, other integer, sim real, primary key(number, rank))")
    db.executemany("insert into neighbors values(?,?,?,?)", rows)
    db.commit()
    print(f"neighbors: top {k} for {len(nums)} items")


def name_categories(db, members, use_llm):
    """One short name per category from the titles closest to its centroid (LLM once; fallback: closest title)."""
    titles = dict(db.execute("select number, title from items"))
    labels = {n: [l for l in (ls or "").split(",") if l] for n, ls in db.execute("select number, labels from items")}
    samples = {c: [titles[n] for n in ns[:12]] for c, ns in members.items()}
    names = distinctive_names(members, titles, labels)
    if not use_llm:
        return names
    spec = importlib.util.spec_from_file_location("suggest", os.path.join(os.path.dirname(os.path.abspath(__file__)), "suggest.py"))
    sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)
    key = next(l.split("=", 1)[1].strip().strip("'\"") for l in open(".env") if l.startswith("OPENROUTER_API_KEY="))
    cs = sorted(samples)
    for b in range(0, len(cs), 25):
        blocks = "\n\n".join(f"[{c}]\n" + "\n".join(f"  - {t[:100]}" for t in samples[c]) for c in cs[b:b + 25])
        prompt = ("Each group below lists issue/PR titles from one GitHub repository that were clustered together. "
                  "Give each group a short topic name (2 to 5 words) that a maintainer would recognize, based only on the titles. "
                  "Names must be distinct from each other.\n\n" + blocks
                  + '\n\nAnswer with only a JSON array: [{"id": <number>, "name": "..."}, ...]')
        try:
            for o in json.loads(re.search(r"\[.*\]", sg.call_llm(prompt, key), re.S).group(0)):
                if int(o["id"]) in names and str(o.get("name", "")).strip():
                    names[int(o["id"])] = str(o["name"]).strip()[:60]
        except Exception as e:  # names are cosmetic: keep the fallback
            print(f"  naming failed for groups {cs[b]}..: {e}", flush=True)
        time.sleep(3.5)
    return names


def init(db, k, use_llm):
    nums, states, E = load_emb(db)
    n = len(nums)
    k = k or int(np.clip(round((n / 10) ** 0.5), 8, 50))
    print(f"init: {k} categories over {n} items", flush=True)
    z = PCA(n_components=min(50, n - 1), random_state=0).fit_transform(E)
    lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(z)
    cent = unit(np.stack([E[lab == c].mean(0) for c in range(k)]))
    sim = (E * cent[lab]).sum(1)
    threshold = float(np.percentile(sim, 2))  # new items less similar than the worst 2% of members go to Unsorted
    members = {c: [nums[i] for i in np.where(lab == c)[0][np.argsort(-sim[lab == c])]] for c in range(k)}
    names = name_categories(db, members, use_llm)

    op = [i for i in range(n) if states[i] == "open"]
    xy = TSNE(n_components=2, perplexity=30, metric="cosine", init="pca", random_state=0).fit_transform(E[op])
    pos = {nums[i]: p for i, p in zip(op, xy)}

    db.execute("drop table if exists categories")
    db.execute("create table categories(id integer primary key, name text, size integer, centroid blob)")
    db.executemany("insert into categories values(?,?,?,?)",
                   [(c, names[c], int((lab == c).sum()), cent[c].astype(np.float32).tobytes()) for c in range(k)])
    db.execute("drop table if exists topics")
    db.execute("create table topics(number integer primary key, cluster integer, sim real, x real, y real)")
    db.executemany("insert into topics values(?,?,?,?,?)",
                   [(nums[i], int(lab[i]), float(sim[i]), *(map(float, pos[nums[i]]) if nums[i] in pos else (None, None))) for i in range(n)])
    db.execute("insert or replace into meta values('category_threshold', ?)", (str(threshold),))
    db.commit()
    for c in sorted(range(k), key=lambda c: -len(members[c])):
        print(f"  [{c:2d}] {len(members[c]):5d}  {names[c]}")


def assign(db):
    """Put items without a category into the nearest existing one, and place open items that are not on the map yet."""
    threshold = float(db.execute("select v from meta where k='category_threshold'").fetchone()[0])
    cats = db.execute("select id, centroid from categories order by id").fetchall()
    ids = np.array([c[0] for c in cats])
    cent = np.stack([np.frombuffer(c[1], dtype=np.float32) for c in cats])
    nums, states, E = load_emb(db, "i.number not in (select number from topics)")
    if nums:
        S = E @ cent.T
        best = S.argmax(1)
        for n, b, s in zip(nums, best, S[np.arange(len(nums)), best]):
            db.execute("insert into topics values(?,?,?,null,null)", (n, int(ids[b]) if s >= threshold else -1, float(s)))
    # map: open items without a position go to the average spot of their nearest placed neighbors
    nums_p, _, E_p = load_emb(db, "i.number in (select number from topics where x is not null)")
    xy_p = np.array(db.execute("select x, y from topics t join emb e using(number) where x is not null order by number").fetchall())
    new, _, E_n = load_emb(db, "i.state='open' and i.number in (select number from topics where x is null)")
    for n, v in zip(new, E_n):
        top = np.argsort(-(E_p @ v))[:NEIGHBORS]
        x, y = xy_p[top].mean(0)
        db.execute("update topics set x=?, y=? where number=?", (float(x), float(y), n))
    db.commit()
    unsorted = sum(1 for n in nums if db.execute("select cluster from topics where number=?", (n,)).fetchone()[0] == -1)
    print(f"assigned {len(nums)} new items ({unsorted} to Unsorted), placed {len(new)} open items on the map")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--init", action="store_true", help="rebuild categories and the map from scratch")
    ap.add_argument("--k", type=int, default=0, help="number of categories at init (default: sqrt(items/10), 8..50)")
    ap.add_argument("--llm-names", action="store_true", help="at init, let the free LLM name the categories (default: their most common labels)")
    a = ap.parse_args()
    db = sqlite3.connect(a.db, timeout=120)
    db.execute("create table if not exists emb(number integer primary key, vec blob)")
    embed_new(db)
    has_cats = db.execute("select 1 from sqlite_master where name='categories'").fetchone()
    if a.init or not has_cats:
        init(db, a.k, a.llm_names)
    else:
        assign(db)
    neighbors(db)


if __name__ == "__main__":
    main()

"""Embed items, keep them sorted into categories, and keep a stable 2D map of the open ones.

usage: python analyze.py data/<owner>__<name>/repo.db [--init] [--k N]

Categories are made once (first run, or --init): KMeans over the embeddings of every item (open + closed), each
category stored as a normalized centroid and named after its most distinctive label and title words. Later runs only embed new items, put each into the
nearest existing category (or -1 "Unsorted" when it is far from all of them) and place new open items on the map at the
average position of their nearest already-placed neighbors, so categories and the map do not move between runs.

Tables: emb(number, vec), categories(id, name, size, centroid), topics(number, cluster, sim, x, y),
neighbors(number, rank, other, sim): the 5 most similar items of every item,
similar(a, b, sim, rank): semantic links, pairs that are in each other's top 5 (rank 0 = each other's nearest),
pr_status(number, status, prs): for every open issue, what happened to the PRs that say they close it.
"""
import argparse, collections, json, re, sqlite3
import numpy as np
import torch
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from transformers import AutoModel, AutoTokenizer

MODEL = "BAAI/bge-small-en-v1.5"
NEIGHBORS = 8
OPEN_PER_CATEGORY = 45


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
    # semantic link = each is among the other's nearest: a relative test, since a raw cosine cut does not separate
    # (numpy: every item has a neighbor at ~0.87, an issue and the PR that fixes it are at ~0.81)
    rank = {(a, b): r for a, r, b, _ in rows}
    db.execute("drop table if exists similar")
    db.execute("create table similar(a integer, b integer, sim real, rank integer, primary key(a, b))")
    db.executemany("insert into similar values(?,?,?,?)",
                   [(a, b, s, max(r, rank[(b, a)])) for a, r, b, s in rows if a < b and (b, a) in rank])
    db.commit()
    print(f"neighbors: top {k} for {len(nums)} items; {db.execute('select count(*) from similar').fetchone()[0]} mutual pairs")


def pr_status(db):
    """Open issues by the fate of the PRs that close them (GitHub's closing links and 'Fixes #N' in a PR);
    an issue with sub-issues is 'tracking' whatever its PRs did."""
    prs = collections.defaultdict(list)
    for issue, pr, state, merged in db.execute(
            "select distinct l.dst, l.src, p.state, p.merged from links l join items p on p.number = l.src "
            "join items i on i.number = l.dst where l.kind in ('closes_official', 'closes') "
            "and p.kind = 'pr' and i.kind = 'issue' and i.state = 'open'"):
        prs[issue].append((pr, "merged" if merged else "open" if state == "open" else "abandoned"))
    parents = {r[0] for r in db.execute("select dst from links where kind = 'sub_issue'")}  # tracking issues stay open by design
    db.execute("drop table if exists pr_status")
    db.execute("create table pr_status(number integer primary key, status text, prs text)")
    count = collections.Counter()
    for (n,) in db.execute("select number from items where kind = 'issue' and state = 'open'").fetchall():
        fates = {f for _, f in prs[n]}
        status = "tracking" if n in parents else next((f for f in ("merged", "open", "abandoned") if f in fates), "none")
        count[status] += 1
        db.execute("insert into pr_status values(?,?,?)", (n, status, json.dumps(sorted(prs[n]))))
    db.commit()
    print("open issues by closing PR: " + ", ".join(f"{k} {v}" for k, v in count.most_common()))


def name_categories(db, members):
    titles = dict(db.execute("select number, title from items"))
    labels = {n: [l for l in (ls or "").split(",") if l] for n, ls in db.execute("select number, labels from items")}
    return distinctive_names(members, titles, labels)


def init(db, k):
    nums, states, E = load_emb(db)
    n = len(nums)
    # as many categories as the repo's numbered triage labels in use on open items ("00 - Bug" ... numpy: 36),
    # the granularity its maintainers chose; repos without such labels: about 45 open items per category (tqdm: 685 -> 15).
    numbered = {l for (ls,) in db.execute("select labels from items where state = 'open'")
                for l in (ls or "").split(",") if re.match(r"^\d+ - ", l)}
    k = k or (len(numbered) if len(numbered) >= 8 else
              int(np.clip(round(sum(s == "open" for s in states) / OPEN_PER_CATEGORY), 8, 80)))
    print(f"init: {k} categories over {n} items", flush=True)
    z = PCA(n_components=min(50, n - 1), random_state=0).fit_transform(E)
    lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(z)
    cent = unit(np.stack([E[lab == c].mean(0) for c in range(k)]))
    sim = (E * cent[lab]).sum(1)
    threshold = float(np.percentile(sim, 2))  # new items less similar than the worst 2% of members go to Unsorted
    members = {c: [nums[i] for i in np.where(lab == c)[0][np.argsort(-sim[lab == c])]] for c in range(k)}
    names = name_categories(db, members)

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
    ap.add_argument("--k", type=int, default=0, help="number of categories at init (default: numbered labels on open items, else open items / 45)")
    a = ap.parse_args()
    db = sqlite3.connect(a.db, timeout=120)
    db.execute("create table if not exists emb(number integer primary key, vec blob)")
    embed_new(db)
    has_cats = db.execute("select 1 from sqlite_master where name='categories'").fetchone()
    if a.init or not has_cats:
        init(db, a.k)
    else:
        assign(db)
    neighbors(db)
    pr_status(db)


if __name__ == "__main__":
    main()

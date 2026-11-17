"""Embed items, sort them into categories, and derive everything the report needs from embeddings and links.

usage: python analyze.py data/<owner>__<name>/repo.db [--init] [--k N]

Categories are made once (first run, or --init): KMeans over the embeddings of every item (open + closed), each
category stored as a normalized centroid and named after its most distinctive label and title words. Later runs only
embed new items and put each into the nearest existing category (or -1 "Unsorted" when it is far from all of them),
so categories do not move between runs. Everything else is recomputed every run.

Tables: emb(number, vec), categories(id, name, size, centroid), topics(number, cluster, sim),
neighbors(number, rank, other, sim): the 5 most similar items of every item,
similar(a, b, sim, rank): semantic links, pairs that are in each other's top 5 (rank 0 = each other's nearest),
pr_status(number, status, prs): for every open issue, what happened to the PRs that say they close it,
dup_pairs(a, b, sim, level), dup_master(number, master): duplicate candidates among issues and the issue to keep,
zombie(number, pr, sim): open issues that a later merged PR seems to fix without linking them,
pr_compete(a, b, reason, issue, sim): open PRs after the same thing.
"""
import argparse, collections, hashlib, json, re, sqlite3
import numpy as np
import torch
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from transformers import AutoModel, AutoTokenizer

import digest

MODEL = "BAAI/bge-small-en-v1.5"
EMB_VERSION = "v3: template lines removed"  # part of every item's hash: changing it re-embeds everything once
CATEGORY_RANGE = (8, 60)  # k = sqrt(open items), clipped
# Similarity thresholds are calibrated on each repo at every run, never typed in (they move whenever the embedding does):
DUP_SHARE = 0.12  # "likely duplicate" = a pair at or above the similarity that the 12% most-similar issues reach with
#                   their nearest issue (per repo; competing() uses the same cut for open PRs). Chosen once, leaning to recall:
#                   on numpy's earlier embedding 12% = cosine 0.915, between the hand-graded 0.92 (~79% the same problem)
#                   and 0.91 (15%, ~29%); the rows below are rechecked afterwards, so a few false alarms are acceptable.
ZOMBIE_PRECISION, ZOMBIE_WINDOW = 0.75, 100  # zombie cut: apply the rule to closed issues with a known closing PR,
#                   sort by similarity and walk down; stop where the 100 cases around the cut pick one of their closing PRs
#                   less than 75% of the time. Local, not cumulative: the cumulative share stays ~0.82 even at 0.78 because
#                   the surest pairs on top carry it (numpy 0.887, opencv 0.871 with this rule; 0.88 was the old hand cut)
ZOMBIE_FALLBACK = 0.86  # fewer than ZOMBIE_WINDOW such issues to calibrate on (small repos): a bit under the lowest
#                   calibrated cut seen (opencv 0.871), leaning to recall


def encoder():
    """(tokenizer, embed(texts, max_length) -> unit vectors in the input order)."""
    tok = AutoTokenizer.from_pretrained(MODEL)
    dev = "cuda" if torch.cuda.is_available() else "cpu"  # fp16 on the GPU; a machine without one still works, slower
    model = AutoModel.from_pretrained(MODEL, dtype=torch.float16 if dev == "cuda" else torch.float32).to(dev).eval()

    def embed(texts, max_length=512):
        order = sorted(range(len(texts)), key=lambda i: len(texts[i]))  # similar lengths per batch = less padding
        out = np.zeros((len(texts), 384), dtype=np.float32)
        with torch.no_grad():
            for c in range(0, len(order), 128):
                idx = order[c:c + 128]
                b = tok([texts[i] for i in idx], padding=True, truncation=True, max_length=max_length, return_tensors="pt").to(dev)
                out[idx] = torch.nn.functional.normalize(model(**b).last_hidden_state[:, 0].float(), dim=-1).cpu().numpy()
        return out
    return tok, embed


def unit(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)


def load_emb(db, where="1"):
    rows = db.execute(f"select i.number, i.state, e.vec from items i join emb e using(number) where {where} order by i.number").fetchall()
    if not rows:
        return [], [], np.zeros((0, 384), dtype=np.float32)
    return [r[0] for r in rows], [r[1] for r in rows], unit(np.stack([np.frombuffer(r[2], dtype=np.float16) for r in rows]).astype(np.float32))


def embed_new(db):
    """Embed items that are new, edited or have new comments (hash of title, description and human comments).

    vector = mean of two embeddings: title + description, and the digest of the whole thread (digest.py).
    Measured on numpy against GitHub's own links: the right original of a marked duplicate ranks first 47% of the
    time (title + description alone, 256 tokens: 36%), an issue's merged closing PR ranks first 41% (34%)."""
    if "hash" not in [c[1] for c in db.execute("pragma table_info(emb)")]:
        db.execute("alter table emb add column hash text")
    done = dict(db.execute("select number, hash from emb"))
    comments = collections.defaultdict(list)
    for n, assoc, b in db.execute("select number, assoc, coalesce(body,'') from comments where kind = 'comment' and bot = 0 order by number, created_at"):
        comments[n].append((assoc in digest.TEAM, b))
    todo = []
    for n, t, b in db.execute("select number, title, coalesce(body,'') from items order by number"):
        h = hashlib.md5("\n".join([EMB_VERSION, t, b] + [c for _, c in comments[n]]).encode()).hexdigest()
        if done.get(n) != h:
            todo.append((n, t, b, h))
    print(f"embedding {len(todo)} new, edited or commented items", flush=True)
    if not todo:
        return
    boiler = digest.boilerplate([b for (b,) in db.execute("select body from items")])
    print(f"  {len(boiler)} template lines left out (repeated verbatim in >= {digest.BOILER_SHARE:.0%} of descriptions)", flush=True)
    todo = [(n, t, digest.strip_boiler(b, boiler), h) for n, t, b, h in todo]
    tok, embed = encoder()
    passages = digest.build({n: digest.units(t, b, [(m, digest.strip_boiler(c, boiler)) for m, c in comments[n]]) for n, t, b, _ in todo}, tok, embed)
    V = unit(embed([f"{t}\n{b[:1500]}" for _, t, b, _ in todo]) + embed([passages[n] for n, *_ in todo]))
    for (n, *_, h), v in zip(todo, V):
        db.execute("insert or replace into emb(number, vec, hash) values(?,?,?)", (n, v.astype(np.float16).tobytes(), h))
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


def share_cut(E):
    """The similarity reached by the DUP_SHARE most-similar items with their nearest other item (1.0 if there are too few)."""
    if len(E) < 2:
        return 1.0
    best = []
    for c in range(0, len(E), 2000):
        S = E[c:c + 2000] @ E.T
        S[np.arange(S.shape[0]), np.arange(c, c + S.shape[0])] = -9
        best.append(S.max(1))
    return float(np.quantile(np.concatenate(best), 1 - DUP_SHARE))


def set_threshold(db, name, value, note=""):
    """Remember the cut each run used (meta 'thresholds'), so the report and a reader can see it."""
    row = db.execute("select v from meta where k = 'thresholds'").fetchone()
    th = json.loads(row[0]) if row else {}
    th[name] = round(value, 4)
    db.execute("insert or replace into meta values('thresholds', ?)", (json.dumps(th),))
    print(f"  {name} cut {value:.4f}{' (' + note + ')' if note else ''}", flush=True)


def neighbors(db, k=5):
    """Top-k most similar items for every item (open or closed), recomputed each run: new items can be anyone's neighbor."""
    nums, _, E = load_emb(db)
    k = min(k, len(nums) - 1)  # a repo with a handful of items
    rows = []
    for c in range(0, len(nums), 1000):
        S = E[c:c + 1000] @ E.T
        S[np.arange(S.shape[0]), np.arange(c, c + S.shape[0])] = -9  # not itself
        top = np.argsort(-S, axis=1)[:, :k]
        for r, t in enumerate(top):
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


def duplicates(db):
    """Duplicate candidates among issues, in three levels: 'github' (marked as duplicate on GitHub), 'likely' (cosine
    >= the repo's DUP_SHARE cut), 'possible' (each is the other's nearest issue). The issue to keep (master) is the
    one GitHub names as the original, else the oldest among an issue's direct likely partners."""
    nums, states, E = load_emb(db, "i.kind = 'issue'")
    idx = {n: i for i, n in enumerate(nums)}
    cut = share_cut(E)
    set_threshold(db, "duplicate", cut)
    pairs = {}
    for c in range(0, len(nums), 2000):
        S = E[c:c + 2000] @ E.T
        S[np.arange(S.shape[0]), np.arange(c, c + S.shape[0])] = -9
        for r, j in enumerate(S.argmax(1)):
            pairs[c + r] = (int(j), float(S[r, j]))
        for r, j in zip(*np.where(S >= cut)):
            a, b = sorted((nums[c + r], nums[j]))
            pairs[(a, b)] = (float(S[r, j]), "likely")
    out = {k: v for k, v in pairs.items() if isinstance(k, tuple)}
    for i, (j, s) in pairs.items():
        if not isinstance(i, tuple) and pairs[j][0] == i:
            out.setdefault(tuple(sorted((nums[i], nums[j]))), (s, "possible"))
    # the issue to keep: GitHub's original if marked, else the oldest of the issue and its direct likely partners
    # (pairs are not chained: chains drift from "same problem" to "same topic", one numpy chain reached 151 issues)
    master = {}
    for (a, b), (_, level) in out.items():
        if level == "likely":
            master[b] = min(master.get(b, b), a)
            master.setdefault(a, a)
    for d, c in db.execute("select src, dst from links where kind = 'duplicate_of'"):
        if d in idx and c in idx:
            out[tuple(sorted((d, c)))] = (float(E[idx[d]] @ E[idx[c]]), "github")
            master[d] = c
            master.setdefault(c, c)
    db.execute("drop table if exists dup_pairs")
    db.execute("create table dup_pairs(a integer, b integer, sim real, level text, primary key(a, b))")
    db.executemany("insert into dup_pairs values(?,?,?,?)", [(a, b, s, l) for (a, b), (s, l) in out.items()])
    db.execute("drop table if exists dup_master")
    db.execute("create table dup_master(number integer primary key, master integer)")
    db.executemany("insert into dup_master values(?,?)", master.items())
    db.commit()
    is_open = {n for n, s in zip(nums, states) if s == "open"}
    extra = sum(1 for x, m in master.items() if x in is_open and m != x)
    lv = collections.Counter(l for _, l in out.values())
    print(f"duplicates: {lv['github']} github, {lv['likely']} likely, {lv['possible']} possible pairs; "
          f"{len(is_open)} open issues are about {len(is_open) - extra} distinct problems ({extra} have an older or original issue)")


def zombies(db):
    """Open issues whose fix may already be merged: the issue and a later merged PR are each other's nearest
    (nearest merged PR of the issue, nearest issue of the PR), similar enough, and the PR has no closing link to it."""
    ni, _, Ei = load_emb(db, "i.kind = 'issue'")
    np_, _, Ep = load_emb(db, "i.kind = 'pr' and i.merged = 1")
    db.execute("drop table if exists zombie")
    db.execute("create table zombie(number integer primary key, pr integer, sim real)")
    if ni and np_:
        created = dict(db.execute("select number, created_at from items"))
        is_open = {r[0] for r in db.execute("select number from items where state = 'open'")}
        linked = set(db.execute("select dst, src from links where kind in ('closes_official', 'closes')"))
        back = np.concatenate([(Ep[c:c + 2000] @ Ei.T).argmax(1) for c in range(0, len(np_), 2000)])
        pairs = []  # (issue, pr, sim) where the issue and a later merged PR are each other's nearest
        for c in range(0, len(ni), 2000):
            S = Ei[c:c + 2000] @ Ep.T
            for r, j in enumerate(S.argmax(1)):
                n, p = ni[c + r], np_[j]
                if back[j] == c + r and created[p] > created[n]:
                    pairs.append((n, p, float(S[r, j])))
        # calibration: closed issues that have a known closing PR, is the matched PR one of them?
        closers = collections.defaultdict(set)
        for i, pr in linked:
            closers[i].add(pr)
        known = sorted(((s, p in closers[n]) for n, p, s in pairs if n not in is_open and closers[n]), reverse=True)
        cut, half = ZOMBIE_FALLBACK, ZOMBIE_WINDOW // 2
        if len(known) >= ZOMBIE_WINDOW:
            hit = np.array([h for _, h in known], dtype=float)
            cut = known[-1][0]
            for k in range(half, len(known)):
                if hit[k - half:k + half].mean() < ZOMBIE_PRECISION:
                    cut = known[k - 1][0]
                    break
        set_threshold(db, "zombie", cut, f"{len(known)} closed issues to calibrate on")
        for n, p, s in pairs:
            if n in is_open and s >= cut and (n, p) not in linked:
                db.execute("insert into zombie values(?,?,?)", (n, p, s))
    db.commit()
    print(f"zombies: {db.execute('select count(*) from zombie').fetchone()[0]} open issues look fixed by an unlinked merged PR")


def competing(db):
    """Open PRs after the same thing: two that close the same issue, or two very similar ones by different authors
    (the same author's similar PRs are a series, not a competition)."""
    cut = json.loads(db.execute("select v from meta where k = 'thresholds'").fetchone()[0])["duplicate"]  # the issues' cut:
    # PRs have near-twins (backports, bot bumps), so a share rule on PRs would give ~0.99; the same similarity as duplicates
    nums, _, E = load_emb(db, "i.kind = 'pr' and i.state = 'open'")
    author = dict(db.execute("select number, author from items where kind = 'pr' and state = 'open'"))
    rows = {}
    for c in range(0, len(nums), 2000):
        S = E[c:c + 2000] @ E.T
        for r, j in zip(*np.where(S >= cut)):
            if c + r < j and author[nums[c + r]] != author[nums[j]]:
                rows[(nums[c + r], nums[j])] = ("very similar", None, float(S[r, j]))
    by_issue = collections.defaultdict(set)
    for issue, pr in db.execute("select l.dst, l.src from links l join items p on p.number = l.src where l.kind in ('closes_official', 'closes') "
                                "and p.kind = 'pr' and p.state = 'open'"):
        by_issue[issue].add(pr)
    idx = {n: i for i, n in enumerate(nums)}
    for issue, prs in by_issue.items():
        prs = sorted(p for p in prs if p in idx)
        for x, a in enumerate(prs):
            for b in prs[x + 1:]:
                rows[(a, b)] = ("close the same issue", issue, float(E[idx[a]] @ E[idx[b]]))
    db.execute("drop table if exists pr_compete")
    db.execute("create table pr_compete(a integer, b integer, reason text, issue integer, sim real, primary key(a, b))")
    db.executemany("insert into pr_compete values(?,?,?,?,?)", [(a, b, *v) for (a, b), v in rows.items()])
    db.commit()
    n = collections.Counter(v[0] for v in rows.values())
    print(f"competing open PRs: {n['close the same issue']} pairs close the same issue, {n['very similar']} pairs are very similar")


def name_categories(db, members):
    titles = dict(db.execute("select number, title from items"))
    labels = {n: json.loads(ls or "[]") for n, ls in db.execute("select number, labels from items")}
    return distinctive_names(members, titles, labels)


def init(db, k):
    nums, states, E = load_emb(db)
    n = len(nums)
    # the embedding has no natural number of clusters (numpy: silhouette ~0.05 and seed agreement ARI 0.4-0.65 for any k
    # from 8 to 150), so k is a reading choice: about sqrt(open items), bigger repos get more groups (numpy 47, tqdm 21)
    k = k or int(np.clip(round(np.sqrt(sum(s == "open" for s in states))), *CATEGORY_RANGE))
    k = min(k, n)
    print(f"init: {k} categories over {n} items", flush=True)
    z = PCA(n_components=min(50, n - 1), random_state=0).fit_transform(E)
    lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(z)
    cent = unit(np.stack([E[lab == c].mean(0) for c in range(k)]))
    sim = (E * cent[lab]).sum(1)
    threshold = float(np.percentile(sim, 2))  # new items less similar than the worst 2% of members go to Unsorted
    members = {c: [nums[i] for i in np.where(lab == c)[0][np.argsort(-sim[lab == c])]] for c in range(k)}
    names = name_categories(db, members)

    db.execute("drop table if exists categories")
    db.execute("create table categories(id integer primary key, name text, size integer, centroid blob)")
    db.executemany("insert into categories values(?,?,?,?)",
                   [(c, names[c], int((lab == c).sum()), cent[c].astype(np.float32).tobytes()) for c in range(k)])
    db.execute("drop table if exists topics")
    db.execute("create table topics(number integer primary key, cluster integer, sim real)")
    db.executemany("insert into topics values(?,?,?)", [(nums[i], int(lab[i]), float(sim[i])) for i in range(n)])
    db.execute("insert or replace into meta values('category_threshold', ?)", (str(threshold),))
    db.commit()
    for c in sorted(range(k), key=lambda c: -len(members[c])):
        print(f"  [{c:2d}] {len(members[c]):5d}  {names[c]}")


def assign(db):
    """Put items without a category into the nearest existing one (-1 "Unsorted" when far from all of them)."""
    threshold = float(db.execute("select v from meta where k='category_threshold'").fetchone()[0])
    cats = db.execute("select id, centroid from categories order by id").fetchall()
    ids = np.array([c[0] for c in cats])
    cent = np.stack([np.frombuffer(c[1], dtype=np.float32) for c in cats])
    nums, _, E = load_emb(db, "i.number not in (select number from topics)")
    unsorted = 0
    if nums:
        S = E @ cent.T
        best = S.argmax(1)
        for n, b, s in zip(nums, best, S[np.arange(len(nums)), best]):
            unsorted += s < threshold
            db.execute("insert into topics(number, cluster, sim) values(?,?,?)", (n, int(ids[b]) if s >= threshold else -1, float(s)))
    db.commit()
    print(f"assigned {len(nums)} new items ({unsorted} to Unsorted)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--init", action="store_true", help="rebuild the categories from scratch")
    ap.add_argument("--k", type=int, default=0, help="number of categories at init (default: sqrt(open items), 8-60)")
    a = ap.parse_args()
    db = sqlite3.connect(a.db, timeout=120)
    db.execute("create table if not exists emb(number integer primary key, vec blob, hash text)")
    embed_new(db)
    has_cats = db.execute("select 1 from sqlite_master where name='categories'").fetchone()
    if a.init or not has_cats:
        init(db, a.k)
    else:
        assign(db)
    neighbors(db)
    pr_status(db)
    duplicates(db)
    zombies(db)
    competing(db)


if __name__ == "__main__":
    main()

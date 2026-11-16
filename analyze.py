"""Embed all items (open + closed, once), cluster open ones by topic, project to 2D.
Writes tables `emb` (all items) and `topics` (open items) into the repo db.

usage: python analyze.py data/<owner>__<name>/repo.db
"""
import sqlite3, sys
import numpy as np
import torch
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from transformers import AutoModel, AutoTokenizer

MODEL = "BAAI/bge-small-en-v1.5"


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


def main(path):
    db = sqlite3.connect(path, timeout=120)
    db.execute("create table if not exists emb(number integer primary key, vec blob)")

    # embed every item once (open and closed), later runs only embed what is new
    todo = db.execute("select number, title, coalesce(body,'') from items where number not in (select number from emb) order by number").fetchall()
    print(f"embedding {len(todo)} new items", flush=True)
    if todo:
        texts = [f"{t}\n{b[:1500]}" for _, t, b in todo]
        order = sorted(range(len(texts)), key=lambda i: len(texts[i]))  # similar lengths per batch = less padding
        vecs = embed([texts[i] for i in order])
        for j, i in enumerate(order):
            db.execute("insert or replace into emb values(?,?)", (todo[i][0], vecs[j].astype(np.float16).tobytes()))
        db.commit()

    # topics and 2D map only for open items
    rows = db.execute("select i.number, i.title, e.vec from items i join emb e using(number) where i.state='open' order by i.number").fetchall()
    nums = [r[0] for r in rows]
    x = np.stack([np.frombuffer(r[2], dtype=np.float16) for r in rows]).astype(np.float32)
    x /= np.linalg.norm(x, axis=1, keepdims=True)

    z = PCA(n_components=min(50, len(x) - 1), random_state=0).fit_transform(x)
    k = int(round((len(x) / 2) ** 0.5))
    lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(z)
    xy = TSNE(n_components=2, perplexity=30, metric="cosine", init="pca", random_state=0).fit_transform(x)

    # cluster names: top tf-idf terms of titles, per cluster
    ids = sorted(set(lab))
    docs = [" ".join(rows[i][1] for i in np.where(lab == c)[0]) for c in ids]
    names = {}
    tf = TfidfVectorizer(stop_words="english", token_pattern=r"[A-Za-z_][A-Za-z0-9_.]{2,}", sublinear_tf=True, max_df=0.25)
    m = tf.fit_transform(docs)
    vocab = np.array(tf.get_feature_names_out())
    for j, c in enumerate(ids):
        names[c] = ", ".join(vocab[m[j].toarray()[0].argsort()[::-1][:3]])

    db.execute("drop table if exists topics")
    db.execute("create table topics(number integer primary key, cluster integer, label text, x real, y real)")
    db.executemany("insert into topics values(?,?,?,?,?)",
                   [(n, int(l), names[int(l)], float(p[0]), float(p[1])) for n, l, p in zip(nums, lab, xy)])
    db.commit()
    print(f"{len(ids)} clusters over {len(nums)} open items")
    for c in ids:
        print(f"  [{c}] {int((lab == c).sum()):4d}  {names[c]}")


if __name__ == "__main__":
    main(sys.argv[1])

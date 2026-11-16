"""Embed items, cluster by topic, project to 2D. Writes table `topics` into the repo db.

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
    db = sqlite3.connect(path)
    rows = db.execute("select number, title, coalesce(body,'') from items order by number").fetchall()
    nums = [r[0] for r in rows]
    texts = [f"{r[1]}\n{r[2][:1500]}" for r in rows]
    x = embed(texts)

    z = PCA(n_components=min(50, len(x) - 1), random_state=0).fit_transform(x)
    k = int(round((len(x) / 2) ** 0.5))
    lab = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(z)
    xy = TSNE(n_components=2, perplexity=30, metric="cosine", init="pca", random_state=0).fit_transform(x)

    # cluster names: top tf-idf terms of titles, per cluster
    ids = sorted(set(lab) - {-1})
    docs = [" ".join(rows[i][1] for i in np.where(lab == c)[0]) for c in ids]
    names = {-1: "unclustered"}  # kept for -1, unused with kmeans
    if ids:
        tf = TfidfVectorizer(stop_words="english", token_pattern=r"[A-Za-z_][A-Za-z0-9_.]{2,}", sublinear_tf=True, max_df=0.25)
        m = tf.fit_transform(docs)
        vocab = np.array(tf.get_feature_names_out())
        for k, c in enumerate(ids):
            row = m[k].toarray()[0]
            names[c] = ", ".join(vocab[row.argsort()[::-1][:3]])

    db.execute("drop table if exists topics")
    db.execute("create table topics(number integer primary key, cluster integer, label text, x real, y real)")
    db.executemany("insert into topics values(?,?,?,?,?)",
                   [(n, int(l), names[int(l)], float(p[0]), float(p[1])) for n, l, p in zip(nums, lab, xy)])
    db.commit()
    print(f"{len(ids)} clusters, {int((lab == -1).sum())}/{len(lab)} unclustered")
    for c in ids:
        print(f"  [{c}] {int((lab == c).sum()):4d}  {names[c]}")


if __name__ == "__main__":
    main(sys.argv[1])

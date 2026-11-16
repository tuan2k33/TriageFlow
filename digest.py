"""One passage per item from its title, description and human comments, short enough for the embedding model.

A thread that fits in BUDGET tokens is kept whole. A longer one keeps its title and first description sentence and
fills the rest by MMR: sentences close to the thread's mean embedding and unlike the ones already taken, with a small
bonus for maintainers and for words that say what happened (fixed, duplicate, closed...). No language model writes
anything: every word comes from the thread, in its original order.
"""
import re
import numpy as np

BUDGET = 500  # tokens; the model reads 512 with [CLS]/[SEP]
LAMBDA = 0.7  # MMR: relevance vs. novelty
TEAM = {"MEMBER", "OWNER", "COLLABORATOR"}
KEY = re.compile(r"\b(fix|duplicate|clos|merg|resolv|supersed|won'?t|not a bug|expected|still|works|deprecat|regress)", re.I)
FLUFF = re.compile(r"^(thanks?|thank you|\+1|lgtm|ping|bump|any update|me too|@\w+\s*$)", re.I)
TEMPLATE = re.compile(r"^(_?no response_?|none|n/?a|-)$", re.I)


def is_code(line):
    s = line.strip()
    if not s:
        return False
    sym = sum(c in "()[]{}=<>,;:*+-/\\'\"_.0123456789" for c in s)
    return (s.startswith((">>>", "...", "$ ", "In [", "Out[", "import ", "from ", "Traceback", "File \"", "    ", "\t"))
            or sym / len(s) > 0.35 or re.match(r"^[\w.]+\s*=", s) is not None
            or re.match(r"^\d+(\.\d+)+(\s|$)", s) is not None)  # version lines of the issue template


def clean(t):
    t = re.sub(r"```.*?(```|$)", "\n", t or "", flags=re.S)
    t = re.sub(r"<!--.*?-->|<details>.*?</details>", " ", t, flags=re.S)
    keep = [l for l in t.split("\n") if not l.lstrip().startswith((">", "#")) and not is_code(l) and not TEMPLATE.match(l.strip())]
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", "\n".join(keep))
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"https?://\S+|(?<![\w/])(?:#|gh-)\d+\b", "", t)  # numbers mean nothing to the model
    return re.sub(r"\s+", " ", t).strip()


def sentences(t):
    out = []
    for s in re.split(r"(?<=[.!?:])\s+(?=[A-Z`@])", clean(t)):
        if len(s) > 25 and not FLUFF.match(s):
            out.append(s if len(s) <= 400 else s[:400].rsplit(" ", 1)[0] + "…")
    return out


def units(title, body, comments):
    """[(sentence, bonus, always keep)]; comments: [(is_maintainer, text)] in thread order."""
    u = [(title.strip(), 0.0, True)] + [(s, 0.0, j == 0) for j, s in enumerate(sentences(body))]
    for team, b in comments:
        u += [(s, 0.05 * team + 0.05 * bool(KEY.search(s)), False) for s in sentences(b)]
    return u


def build(threads, tok, embed):
    """threads: {number: units}; embed(texts, max_length) -> unit vectors. Returns {number: passage}."""
    nums = list(threads)
    flat = [s for n in nums for s, _, _ in threads[n]]
    lens = [len(x) for x in tok(flat, add_special_tokens=False)["input_ids"]] if flat else []
    out, long_items, pos = {}, [], 0
    for n in nums:
        k = len(threads[n])
        if sum(lens[pos:pos + k]) + k <= BUDGET:
            out[n] = " ".join(s for s, _, _ in threads[n])
        else:
            long_items.append((n, pos, k))
        pos += k
    need = [i for _, p, k in long_items for i in range(p, p + k)]
    E = np.zeros((len(flat), 384), dtype=np.float32)
    if need:
        E[need] = embed([flat[i] for i in need], 128)
    for n, p, k in long_items:
        S, L, info = E[p:p + k], lens[p:p + k], threads[n]
        c = S.mean(0)
        c /= np.linalg.norm(c)
        rel = S @ c + np.array([b for _, b, _ in info])
        chosen = [i for i in range(k) if info[i][2]]
        used = sum(L[i] + 1 for i in chosen)
        left = set(range(k)) - set(chosen)
        red = (S @ S[chosen].T).max(1)
        while left:
            cand = [i for i in left if used + L[i] + 1 <= BUDGET]
            if not cand:
                break
            i = max(cand, key=lambda i: LAMBDA * rel[i] - (1 - LAMBDA) * red[i])
            chosen.append(i)
            used += L[i] + 1
            left.discard(i)
            red = np.maximum(red, S @ S[i])
        out[n] = " ".join(info[i][0] for i in sorted(chosen))
    return out

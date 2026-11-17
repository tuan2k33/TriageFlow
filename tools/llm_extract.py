"""Help for the reproduce check (tools/repro.py): a free OpenRouter model reads each issue's description and quotes what
should happen and what the reporter got instead. Only quotes are kept, and each quote is checked against the description
(letters and digits, in order): a line the model made up or reworded is dropped. Not part of the pipeline.

usage: set -a; . ~/.dev/secrets.env; set +a
       python tools/llm_extract.py data/<owner>__<name>/repo.db [--model ID] [--limit N]
reads the cases from repro/ (issues with a snippet file), writes repro/extract.jsonl; a rerun skips issues whose
description has not changed. Then `python tools/repro.py <db> --rerun` puts the quotes into each file.
"""
import argparse, hashlib, json, re, sqlite3, sys, time, urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_judge import ask  # noqa: E402

MODEL = "nvidia/nemotron-3.5-super-vl:free"  # the judge's nemotron-3-ultra answered 503 on 2026-11-18
MAX_DESC = 12000  # characters of description sent
MAX_QUOTE = 400
KINDS = ["bug", "enhancement", "documentation", "question", "other"]
PROMPT = """Below is the description of a GitHub issue of numpy. Quote from it, word for word:
- "expected": what the reporter says should happen or should be the result (correct output, no error, a value). At most 4.
- "reported": what actually happened instead, as the reporter saw it: the wrong output, the error or warning message
  (its last line, e.g. "ValueError: ..."), the wrong value. At most 4.
Copy text exactly as it appears (you may cut a long sentence, but never reword, translate or summarise). Leave a list
empty if the description does not say it; do not guess. Also give "kind": one of %s.

Answer with one line of JSON only: {"kind": ..., "expected": [...], "reported": [...]}

=== issue #%d: %s ===
%s"""


def body_hash(body):
    return hashlib.sha1(body.encode()).hexdigest()[:10]


def letters(s):
    return re.sub(r"[^0-9a-z]+", "", s.lower())


def checked(quotes, desc):
    """Keep the quotes found in the description (compared on letters and digits only, so spacing and markdown differ)."""
    hay = letters(desc)
    out = []
    for q in quotes if isinstance(quotes, list) else []:
        q = re.sub(r"\s+", " ", str(q)).strip()
        if len(letters(q)) >= 4 and letters(q) in hay:
            out.append(q if len(q) <= MAX_QUOTE else q[:MAX_QUOTE].rsplit(" ", 1)[0] + " …")
    return list(dict.fromkeys(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    db = sqlite3.connect(f"file:{Path(a.db).absolute()}?mode=ro", uri=True)
    repro = Path(a.db).parent / "repro"
    out = repro / "extract.jsonl"
    done = {(r["number"], r["hash"]) for r in map(json.loads, out.read_text().splitlines())} if out.exists() else set()
    todo = []
    for py in sorted(repro.glob("*.py"), key=lambda p: int(p.stem)):
        n = int(py.stem)
        title, body = db.execute("select title, coalesce(body,'') from items where number=?", (n,)).fetchone()
        desc = re.sub(r"<!--.*?-->", "", body.replace("\r\n", "\n"), flags=re.S).strip()
        if (n, body_hash(body)) not in done:
            todo.append((n, title, body, desc))
    print(f"{len(todo)} issues to read with {a.model}", flush=True)
    for i, (n, title, body, desc) in enumerate(todo[:a.limit or None]):
        prompt = PROMPT % (KINDS, n, title, desc[:MAX_DESC])
        for attempt in range(4):
            try:
                text = ask(a.model, prompt)
                break
            except urllib.error.HTTPError as e:
                if attempt == 3:
                    if e.code == 429:
                        print(f"  rate limited ({e.read()[:200]!r}); stopping, rerun later to continue", flush=True)
                        return
                    raise
                time.sleep((60 if e.code == 429 else 10) * (attempt + 1))  # 429 from free models is often upstream and brief
            except (urllib.error.URLError, TimeoutError, ConnectionError, KeyError, json.JSONDecodeError):
                if attempt == 3:
                    raise
                time.sleep(10 * (attempt + 1))
        j = re.search(r"\{.*\}", text, re.S)
        try:
            v = json.loads(j.group(0)) if j else {}
        except json.JSONDecodeError:
            v = {}
        exp, rep = checked(v.get("expected"), desc), checked(v.get("reported"), desc)
        dropped = len(v.get("expected") or []) + len(v.get("reported") or []) - len(exp) - len(rep)
        row = {"number": n, "hash": body_hash(body), "kind": v.get("kind") if v.get("kind") in KINDS else "unparsed",
               "expected": exp, "reported": rep, "dropped": dropped, "model": a.model}
        with out.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"  [{i + 1}/{len(todo)}] #{n} {row['kind']}: {len(exp)} expected, {len(rep)} reported, {dropped} dropped",
              flush=True)
        time.sleep(4)


if __name__ == "__main__":
    sys.exit(main())

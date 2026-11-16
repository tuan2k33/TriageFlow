"""Paste a GitHub repo link, get the database, the browse page and the report.

usage: python run.py https://github.com/<owner>/<name>     (or just owner/name)

Runs the five steps in order (crawl, analyze, suggest, report, build_html); a rerun only syncs what changed.
"""
import subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).parent


def main(link):
    sys.path.insert(0, str(HERE))
    from triageflow import parse_repo
    owner, name = parse_repo(link)
    out = HERE / "data" / f"{owner}__{name}"
    db = str(out / "repo.db")
    t0 = time.time()
    for step, args in (("triageflow", [f"{owner}/{name}"]), ("analyze", [db]), ("suggest", [db]), ("report", [db]), ("build_html", [db])):
        print(f"\n== {step}", flush=True)
        subprocess.run([sys.executable, "-u", str(HERE / f"{step}.py"), *args], check=True, cwd=HERE)
    print(f"\ndone in {time.time() - t0:.0f}s:")
    for f in ("repo.db", "browse.html", "report.md", "actions.sh"):
        print(f"  {out / f}")


if __name__ == "__main__":
    main(sys.argv[1])

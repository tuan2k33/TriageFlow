"""Find a repository's label axes from its own labels: which labels say what kind of item it is (type) and which say
where in the project it is (component). Used by suggest.py (label suggestions) and build_html.py (filters, matrix).

type:       a label whose name, without a number ("00 - Bug"), emoji or a note in brackets ("question (invalid tracker)"),
            is a known kind of work, or a label prefixed "type:" / "kind:".
component:  the "prefix: name" group with the most labels ("component: numpy.ma", "category: imgproc"), process
            prefixes excepted. numpy gets exactly the labels its hand-written rules had; opencv gets bug/feature/... and
            its "category:" labels; a repo with neither gets no axis (pseudo labels then come from the categories).
"""
import collections, json, re

TYPE_WORDS = {"bug", "enhancement", "feature", "feature request", "documentation", "docs", "maintenance", "testing", "test",
              "tests", "regression", "deprecation", "task", "question", "wish list", "performance", "optimization", "cleanup",
              "refactor", "refactoring", "security", "chore"}
PROCESS = {"type", "kind", "priority", "status", "pr", "state", "resolution", "triage", "severity", "size", "difficulty",
           "effort", "needs", "port", "backport"}
PREFIX = re.compile(r"^([A-Za-z][\w .-]{0,20}?)\s*:\s*\S")


def type_name(label):
    s = re.sub(r"^\d+\s*-\s*", "", label)
    s = re.sub(r"^(type|kind)\s*:\s*", "", s, flags=re.I)
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^\w /-]", "", s).strip().lower()


def detect(labels):
    """labels: label names in use. -> {"type": sorted type labels, "component": prefix or None}"""
    labels = set(labels)
    types = {l for l in labels if re.match(r"^(type|kind)\s*:", l, re.I) or (not PREFIX.match(l) and type_name(l) in TYPE_WORDS)}
    groups = collections.defaultdict(set)
    for l in labels:
        m = PREFIX.match(l)
        if m and m.group(1).strip().lower() not in PROCESS:
            groups[m.group(1).strip()].add(l)
    best = max(groups, key=lambda g: len(groups[g]), default=None)
    return {"type": sorted(types), "component": best if best and len(groups[best]) >= 3 else None}


def of_repo(db):
    """Axes from the labels on open items (the scheme in use now), falling back to all items."""
    for where in ("state = 'open'", "1"):
        found = detect(l for (ls,) in db.execute(f"select labels from items where {where}") for l in json.loads(ls or "[]"))
        if found["type"] or found["component"]:
            return found
    return found


def is_component(label, prefix):
    return bool(prefix) and label.lower().startswith(prefix.lower() + ":")

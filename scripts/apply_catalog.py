"""Copy catalog numbers from a CSV (columns: slug, catalog) into site/content/releases.json.

Numbers that are malformed, or used by more than one release without "same record" in the note column,
are skipped and reported.
Usage: python3 -I apply_catalog.py <csv> <releases.json>
"""
import collections
import csv
import json
import re
import sys

csv_path, json_path = sys.argv[1:3]
rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
cats = {r["slug"]: r["catalog"].strip().upper() for r in rows if r.get("catalog", "").strip()}
# releases deliberately sharing a number (e.g. two titles from one record) say "same record" in the note column
shared = {r["slug"]: "same record" in r.get("note", "").lower() for r in rows}

uses = collections.Counter(cats.values())
releases = json.load(open(json_path))
applied, skipped = 0, []
for rel in releases:
    cat = cats.get(rel["slug"])
    if not cat:
        rel.setdefault("catalog", None)
    elif not re.fullmatch(r"3B\d{3}", cat):
        skipped.append(f"{rel['slug']}: bad format {cat!r}")
        rel.setdefault("catalog", None)
    elif uses[cat] > 1 and not all(shared.get(slug) for slug, c in cats.items() if c == cat):
        skipped.append(f"{rel['slug']}: {cat} is used by {uses[cat]} releases")
        rel["catalog"] = None
    else:
        rel["catalog"] = cat
        applied += 1

with open(json_path, "w") as f:
    json.dump(releases, f, indent=1, ensure_ascii=False)
print(f"applied {applied} catalog numbers")
for s in skipped:
    print("skipped", s)

"""Add 3Bridge releases from Deezer's public API to the site content.

Merges into site/content/{releases,artists}.json by slug (existing entries are never overwritten)
and saves covers to site/public/media/releases/<slug>.jpg and <slug>-sm.jpg.

Usage: python3 -I import_deezer.py <site_dir> <download_dir> <deezer_album_id> [<id> ...]
Find album ids with: https://api.deezer.com/search/album?q=label:"3bridge records"
"""
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.request

SITE, DL = (os.path.abspath(a) for a in sys.argv[1:3])
IDS = sys.argv[3:]
CONTENT = os.path.join(SITE, "content")
MEDIA = os.path.join(SITE, "public", "media")
UA = {"User-Agent": "3bridge-site-import/1.0"}


def get_json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def mmss(sec):
    return f"{sec // 60}:{sec % 60:02d}" if sec else None


def load(name):
    with open(os.path.join(CONTENT, name)) as f:
        return json.load(f)


releases, artists = load("releases.json"), load("artists.json")
rel_by_slug = {r["slug"]: r for r in releases}
art_by_name = {a["name"].lower(): a for a in artists}
os.makedirs(DL, exist_ok=True)

for album_id in IDS:
    a = get_json(f"https://api.deezer.com/album/{int(album_id)}")
    if a.get("error"):
        print(f"SKIP {album_id}: {a['error']}")
        continue
    if "3bridge" not in a.get("label", "").lower():
        print(f"SKIP {album_id}: label is {a.get('label')!r}")
        continue
    slug = slugify(a["title"])
    if any(r["title"].lower() == a["title"].lower() and r["date"] == a.get("release_date") for r in releases):
        print(f"exists: {slug}")
        continue
    if slug in rel_by_slug:  # different record with the same title, e.g. "Out of Sight" (2019 vs 2026)
        slug = f"{slug}-{slugify(a['artist']['name'])}"
        if slug in rel_by_slug:
            slug = f"{slug}-{a.get('release_date', '')[:4]}"

    # cover: download the 1000px original, then make the two sizes the site uses
    raw = os.path.join(DL, f"{album_id}.jpg")
    with open(raw, "wb") as f:
        f.write(urllib.request.urlopen(urllib.request.Request(a["cover_xl"], headers=UA), timeout=60).read())
    covers = {}
    for suffix, width in (("", 1000), ("-sm", 480)):
        dest = os.path.join(MEDIA, "releases", f"{slug}{suffix}.jpg")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", "-Z", str(width), raw, "--out", dest],
                       check=True, capture_output=True)
        covers[width] = f"/media/releases/{slug}{suffix}.jpg"

    names = [c["name"] for c in a.get("contributors", [])] or [a["artist"]["name"]]
    artist_slugs = []
    for name in names:
        art = art_by_name.get(name.lower())
        if art is None:
            art = {"slug": slugify(name), "name": name, "photo": None, "bio": [], "links": {}, "releases": []}
            artists.append(art)
            art_by_name[name.lower()] = art
            print(f"  new artist: {name}")
        if slug not in art["releases"]:
            art["releases"].append(slug)
        art["photoFallback"] = art.get("photoFallback") or None
        artist_slugs.append(art["slug"])

    rel = {
        "slug": slug,
        "title": a["title"],
        "artistLine": ", ".join(names),
        "artists": artist_slugs,
        "date": a.get("release_date"),
        "buyUrl": None,
        "cover": covers[1000],
        "thumb": covers[480],
        "review": [],
        "tracks": [
            {"n": str(i), "title": t["title"], "duration": mmss(t.get("duration"))}
            for i, t in enumerate(a["tracks"]["data"], 1)
        ],
        "upc": a.get("upc"),
        "deezerUrl": a.get("link"),
        "seq": 0,
    }
    releases.append(rel)
    rel_by_slug[slug] = rel
    print(f"added: {a['release_date']} {a['title']} — {rel['artistLine']} ({len(rel['tracks'])} tracks)")
    time.sleep(0.2)

# keep ordering/derived fields consistent with extract_content.py
releases.sort(key=lambda r: (r["date"] or "", r["slug"]), reverse=True)
for i, r in enumerate(reversed(releases), 1):
    r["seq"] = i
for art in artists:
    own = [rel_by_slug[s] for s in art["releases"] if s in rel_by_slug]
    if not art.get("photo") and own:
        art["photoFallback"] = max(own, key=lambda r: r["date"] or "")["cover"]
artists.sort(key=lambda x: x["name"].lower())

for name, data in (("releases.json", releases), ("artists.json", artists)):
    with open(os.path.join(CONTENT, name), "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
print(f"{len(releases)} releases, {len(artists)} artists")

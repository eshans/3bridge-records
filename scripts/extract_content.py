"""Turn the saved WordPress pages into structured JSON for the Nuxt site.

Usage: python3 -I extract_content.py <mirror_dir> <media_dir> <site_dir>
Writes <site_dir>/content/{releases,artists}.json and resized images to <site_dir>/public/media/.
"""
import glob
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse

MIRROR, MEDIA, SITE = (os.path.abspath(a) for a in sys.argv[1:4])
OUT_IMG = os.path.join(SITE, "public", "media")
CONTENT = os.path.join(SITE, "content")
os.makedirs(CONTENT, exist_ok=True)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def paragraphs(block):
    paras = [text(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", block or "", re.S)]
    paras = [p for p in paras if p]
    return paras or ([text(block)] if text(block) else [])


def slug_of(url, kind):
    m = re.search(rf"/{kind}/([^/]+)/", url)
    return urllib.parse.unquote(m.group(1)) if m else None


_img_cache = {}


def image(timthumb_or_url, width, name):
    """Resize the original behind a timthumb/upload URL to public/media/<name>.jpg; return its public path."""
    if not timthumb_or_url:
        return None
    u = html.unescape(timthumb_or_url)
    q = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
    src = q.get("src", [u])[0]
    if "/uploads/" not in src:
        return None
    rel = urllib.parse.unquote(src.split("/uploads/", 1)[1])
    key = name
    if key in _img_cache:
        return _img_cache[key]
    srcfile = os.path.join(MEDIA, rel)
    if not os.path.exists(srcfile):
        print(f"missing image {rel}")
        _img_cache[key] = None
        return None
    dest = os.path.join(OUT_IMG, f"{name}.jpg")
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", "-Z", str(width), srcfile, "--out", dest],
            check=True, capture_output=True,
        )
    _img_cache[key] = f"/media/{name}.jpg"
    return _img_cache[key]


def iso(d):
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", d or "")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def split_artists(s):
    return [a.strip() for a in re.split(r",\s*", s) if a.strip()]


# ---------- releases ----------
releases = {}
for path in sorted(glob.glob(os.path.join(MIRROR, "release", "*", "index.html"))):
    slug = os.path.basename(os.path.dirname(path))
    t = read(path)
    main = t.split('carousel-slider-container', 1)[0]
    cover = re.search(r'release-cover">\s*(?:<a[^>]*>)?<img src="([^"]+)"', main)
    title = re.search(r'release-title">(.*?)</h4>', main, re.S)
    artist = re.search(r'release-artist">(.*?)</h6>', main, re.S)
    date = re.search(r'release-info">(.*?)</div>', main, re.S)
    buy = re.search(r'button-container[^"]*"><a href="([^"]+)"', main)
    review = re.search(r'<span>Review</span>.*?post-content">(.*?)</div>', main, re.S)
    tracks = []
    for row in re.findall(r"<tr>(.*?)</tr>", main, re.S):
        cells = [text(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        if len(cells) >= 2 and cells[1]:
            tracks.append({"n": cells[0], "title": cells[1], "duration": cells[2] if len(cells) > 2 and cells[2] else None})
    artist_s = text(artist.group(1)) if artist else ""
    buy_url = html.unescape(buy.group(1)) if buy else None
    if buy_url and ("3bridgerecords.com" in buy_url or not buy_url.startswith("http")):
        buy_url = None
    if buy_url:
        buy_url = re.sub(r"^http://", "https://", buy_url).replace("://pro.beatport.com", "://www.beatport.com")
    releases[slug] = {
        "slug": slug,
        "title": text(title.group(1)) if title else slug,
        "artistLine": artist_s,
        "artists": [],
        "date": iso(text(date.group(1)) if date else None),
        "buyUrl": buy_url,
        "cover": image(cover.group(1), 1000, f"releases/{slug}") if cover else None,
        "thumb": image(cover.group(1), 480, f"releases/{slug}-sm") if cover else None,
        "review": paragraphs(review.group(1)) if review else [],
        "tracks": tracks,
    }

# ---------- artists (profile pages) ----------
artists = {}
for path in sorted(glob.glob(os.path.join(MIRROR, "artist", "*", "index.html"))):
    slug = os.path.basename(os.path.dirname(path))
    t = read(path)
    name = re.search(r'page-title wrapper">.*?<h1>(.*?)</h1>', t, re.S)
    photo = re.search(r'artist-thumbnail">\s*<img src="([^"]+)"', t)
    bio = re.search(r"<span>Biography</span>.*?post-content\">(.*?)</div>", t, re.S)
    socials = {}
    sl = re.search(r'artist-social-links">(.*?)</div>', t, re.S)
    if sl:
        for href, cls in re.findall(r'<a href="([^"]+)" class="([^"]+)"', sl.group(1)):
            socials[cls] = html.unescape(href)
    carousel = t.split('carousel-slider-container', 1)[1] if 'carousel-slider-container' in t else ""
    rel_slugs = list(dict.fromkeys(re.findall(r'/release/([^/"]+)/', carousel)))
    artists[slug] = {
        "slug": slug,
        "name": text(name.group(1)) if name else slug,
        "photo": image(photo.group(1), 900, f"artists/{slug}") if photo else None,
        "bio": paragraphs(bio.group(1)) if bio else [],
        "links": socials,
        "releases": rel_slugs,
    }

# photos from the /artists listing, for profiles whose page has no photo
for path in glob.glob(os.path.join(MIRROR, "artists", "**", "*.html"), recursive=True):
    for slug, img in re.findall(r'<a href="https://www\.3bridgerecords\.com/artist/([^/"]+)/"><img src="([^"]+)"', read(path)):
        slug = urllib.parse.unquote(slug)
        if slug in artists and not artists[slug]["photo"]:
            artists[slug]["photo"] = image(img, 900, f"artists/{slug}")

# ---------- artists without pages (sidebar ?a=ID filters) ----------
listing = read(os.path.join(MIRROR, "releases", "index.html"))
sidebar = dict(re.findall(r'href="https://www\.3bridgerecords\.com/releases/\?a=(\d+)"[^>]*>(.*?)</a>', listing))
by_name = {a["name"].lower(): a for a in artists.values()}
for aid, raw in sidebar.items():
    name = text(raw)
    files = glob.glob(os.path.join(MIRROR, "releases", "**", f"index_a={aid}.html"), recursive=True)
    rel_slugs = []
    for f in files:
        body = read(f).split('<div class="sidebar', 1)[0]
        rel_slugs += re.findall(r'/release/([^/"]+)/', body)
    rel_slugs = list(dict.fromkeys(rel_slugs))
    a = by_name.get(name.lower())
    if a is None:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if slug in artists:  # duplicate sidebar entry (e.g. "Second City Firsts" twice)
            a = artists[slug]
        else:
            a = artists[slug] = {"slug": slug, "name": name, "photo": None, "bio": [], "links": {}, "releases": []}
            by_name[name.lower()] = a
    a["releases"] = list(dict.fromkeys(a["releases"] + rel_slugs))

# link releases -> artists
for a in artists.values():
    a["releases"] = [s for s in a["releases"] if s in releases]
    for s in a["releases"]:
        if a["slug"] not in releases[s]["artists"]:
            releases[s]["artists"].append(a["slug"])
# artist photo fallback: latest release cover
for a in artists.values():
    if not a["photo"] and a["releases"]:
        latest = max((releases[s] for s in a["releases"]), key=lambda r: r["date"] or "")
        a["photoFallback"] = latest["cover"]

rel_list = sorted(releases.values(), key=lambda r: (r["date"] or "", r["slug"]), reverse=True)
for i, r in enumerate(reversed(rel_list), 1):
    r["seq"] = i  # chronological index, shown as "No. 001"
art_list = sorted(artists.values(), key=lambda a: a["name"].lower())

with open(os.path.join(CONTENT, "releases.json"), "w") as f:
    json.dump(rel_list, f, indent=1, ensure_ascii=False)
with open(os.path.join(CONTENT, "artists.json"), "w") as f:
    json.dump(art_list, f, indent=1, ensure_ascii=False)

print(f"{len(rel_list)} releases, {len(art_list)} artists, {sum(len(f) for _, _, f in os.walk(OUT_IMG))} images")
print("releases w/o artist link:", [r["slug"] for r in rel_list if not r["artists"]])
print("releases w/o cover:", [r["slug"] for r in rel_list if not r["cover"]])
print("releases w/o date:", [r["slug"] for r in rel_list if not r["date"]])
print("artists w/o releases:", [a["slug"] for a in art_list if not a["releases"]])

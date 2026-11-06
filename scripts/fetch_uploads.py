"""Crawl the open /wp-content/uploads/ directory listing and download original files.

Skips WordPress auto-generated resized copies (name-123x456.jpg).
Usage: python3 -I fetch_uploads.py <dest_dir>
"""
import os
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://www.3bridgerecords.com/wp-content/uploads/"
DEST = os.path.abspath(sys.argv[1])
RESIZED = re.compile(r"-\d+x\d+\.[a-z0-9]+$", re.I)
HREF = re.compile(r'<a href="([^"?][^"]*)">')
UA = {"User-Agent": "3bridge-migration/1.0"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def crawl(url, out):
    html = get(url).decode("utf-8", "replace")
    for href in HREF.findall(html):
        if href.startswith("/") or href.startswith("http"):
            continue  # parent dir / absolute links
        full = urllib.parse.urljoin(url, href)
        if href.endswith("/"):
            crawl(full, out)
        elif not RESIZED.search(urllib.parse.unquote(href)):
            out.append(full)


def download(url):
    rel = urllib.parse.unquote(url[len(BASE):])
    path = os.path.normpath(os.path.join(DEST, rel))
    if not path.startswith(os.path.abspath(DEST)):
        return f"SKIP {rel}"
    if os.path.exists(path):
        return None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        data = get(url)
    except Exception as e:  # noqa: BLE001
        return f"FAIL {rel}: {e}"
    with open(path, "wb") as f:
        f.write(data)
    return None


files = []
crawl(BASE, files)
print(f"{len(files)} original files found")
with ThreadPoolExecutor(8) as pool:
    for msg in pool.map(download, files):
        if msg:
            print(msg)
print("done")

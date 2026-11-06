"""Mirror the HTML pages (plus CSS/JS/fonts) of www.3bridgerecords.com.

Uploaded media is skipped (fetch_uploads.py handles it). Existing files are not re-fetched.
Usage: python3 -I mirror_site.py <dest_dir>
"""
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import deque

HOST = "www.3bridgerecords.com"
START = f"https://{HOST}/"
DEST = os.path.abspath(sys.argv[1])
UA = {"User-Agent": "3bridge-migration/1.0"}
LINK = re.compile(r'(?:href|src)=["\']([^"\'#]+)', re.I)
CSS_URL = re.compile(r'url\(["\']?([^"\')]+)')
SKIP = re.compile(r"/wp-content/uploads/|timthumb|\.php(\?|$)|/wp-json/|/xmlrpc|/wp-login|/wp-admin|/feed/?$|/comments/feed|\?replytocom=|/embed/?$", re.I)
ASSET = re.compile(r"\.(css|js|woff2?|ttf|eot|otf|svg|ico)(\?.*)?$", re.I)


def local_path(url):
    p = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(p.path)
    if path.endswith("/") or not os.path.splitext(path)[1]:
        path = path.rstrip("/") + "/index.html"
    if p.query and not ASSET.search(p.path):
        path = path[:-5] + "_" + re.sub(r"[^\w=-]", "_", p.query) + ".html"
    out = os.path.normpath(os.path.join(DEST, path.lstrip("/")))
    return out if out.startswith(DEST) else None


def norm(base, href):
    u = urllib.parse.urljoin(base, href.strip())
    p = urllib.parse.urlparse(u)
    if p.scheme not in ("http", "https") or p.netloc.lower() not in (HOST, HOST[4:]):
        return None
    u = urllib.parse.urlunparse(("https", HOST, p.path or "/", "", p.query, ""))
    return None if SKIP.search(u) else u


seen, queue, n = {START}, deque([START]), 0
while queue:
    url = queue.popleft()
    path = local_path(url)
    if not path:
        continue
    try:
        if os.path.exists(path):
            body, ctype = open(path, "rb").read(), ("text/html" if path.endswith(".html") else "")
        else:
            resp = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
            ctype, body = resp.headers.get("Content-Type", ""), resp.read()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(body)
            n += 1
            time.sleep(0.3)
    except Exception as e:  # noqa: BLE001
        print(f"FAIL {url}: {e}", flush=True)
        continue
    if "html" in ctype or "css" in ctype or path.endswith(".css"):
        text = body.decode("utf-8", "replace")
        refs = LINK.findall(text) + CSS_URL.findall(text)
        for href in refs:
            u = norm(url, href)
            if u and u not in seen:
                seen.add(u)
                queue.append(u)
print(f"done: {n} new files, {len(seen)} urls seen", flush=True)

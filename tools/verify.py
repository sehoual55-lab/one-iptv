#!/usr/bin/env python3
"""Static checks: internal links resolve, JSON-LD parses, meta present, no stray placeholders."""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
errors, warnings = [], []


def pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("tools", ".git")]
        for fn in filenames:
            # Skip generated preview bundles — they are tools, not site pages.
            if fn in ("ONE-IPTV-preview.html", "seo-preview.html"):
                continue
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def url_to_path(url):
    """Map a site-root URL to a file on disk."""
    url = url.split("#")[0].split("?")[0]
    if not url:
        return None
    if url.startswith("/"):
        p = os.path.join(ROOT, url.lstrip("/"))
    else:
        return None
    if url.endswith("/") or os.path.isdir(p):
        p = os.path.join(p, "index.html")
    return p


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.ids, self.anchors = [], [], set(), []
        self.h1 = 0
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag == "img":
            self.imgs.append(d)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


for path in sorted(pages()):
    rel = os.path.relpath(path, ROOT)
    html = open(path, encoding="utf-8").read()

    p = Tags()
    p.feed(html)

    # --- one h1 -----------------------------------------------------------
    if p.h1 != 1:
        errors.append(f"{rel}: expected exactly 1 <h1>, found {p.h1}")

    # --- title length -----------------------------------------------------
    t = p.title.strip()
    if not t:
        errors.append(f"{rel}: missing <title>")
    elif len(t) > 65:
        warnings.append(f"{rel}: title is {len(t)} chars (>65): {t}")

    # --- meta description -------------------------------------------------
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if not m:
        errors.append(f"{rel}: missing meta description")
    else:
        dl = len(m.group(1))
        if dl > 165:
            warnings.append(f"{rel}: meta description {dl} chars (>165)")
        elif dl < 70:
            warnings.append(f"{rel}: meta description only {dl} chars")

    # --- canonical --------------------------------------------------------
    if 'rel="canonical"' not in html:
        errors.append(f"{rel}: missing canonical")

    # --- og / twitter -----------------------------------------------------
    for req in ['property="og:title"', 'property="og:image"', 'name="twitter:card"']:
        if req not in html:
            errors.append(f"{rel}: missing {req}")

    # --- JSON-LD ----------------------------------------------------------
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(block)
        except Exception as e:
            errors.append(f"{rel}: invalid JSON-LD — {e}")

    # --- images have alt + dimensions -------------------------------------
    for img in p.imgs:
        if "alt" not in img:
            errors.append(f"{rel}: <img src={img.get('src')}> missing alt")
        if not (img.get("width") and img.get("height")):
            warnings.append(f"{rel}: <img src={img.get('src')}> missing width/height")
        if img.get("loading") != "lazy" and img.get("fetchpriority") != "high":
            warnings.append(f"{rel}: <img src={img.get('src')}> not lazy-loaded")

    # --- links ------------------------------------------------------------
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "javascript:")):
            continue
        if href.startswith("#"):
            if href != "#" and href[1:] not in p.ids:
                errors.append(f"{rel}: anchor {href} has no matching id")
            continue
        target = url_to_path(href)
        if target is None:
            warnings.append(f"{rel}: unusual href {href}")
            continue
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href} -> {os.path.relpath(target, ROOT)}")

    # --- unresolved template markers --------------------------------------
    for marker in ("PHONE_TEL_RAW", "PHONE_DISPLAY_TXT", "EMAIL_TXT", "{{", "None</"):
        if marker in html:
            errors.append(f"{rel}: unresolved marker {marker!r}")

    # --- phone number present ---------------------------------------------
    if "data-whatsapp-link" not in html and "wa.me/" not in html:
        errors.append(f"{rel}: missing WhatsApp contact link")
    # contact should be WhatsApp-only now
    if "tel:" in html:
        errors.append(f"{rel}: still contains a tel: link")
    if "mailto:" in html:
        errors.append(f"{rel}: still contains a mailto: link")

# --- asset references exist ---------------------------------------------
for path in sorted(pages()):
    rel = os.path.relpath(path, ROOT)
    html = open(path, encoding="utf-8").read()
    for src in re.findall(r'(?:src|href)="(/assets/[^"]+)"', html):
        if not os.path.exists(os.path.join(ROOT, src.lstrip("/"))):
            errors.append(f"{rel}: missing asset {src}")

# --- sitemap covers every page ------------------------------------------
sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
listed = set(re.findall(r"<loc>https://www\.one-iptv\.website(.*?)</loc>", sitemap))
on_disk = set()
for path in pages():
    rel = os.path.relpath(path, ROOT)
    if rel == "404.html":
        continue
    u = "/" if rel == "index.html" else "/" + rel[: -len("index.html")]
    on_disk.add(u)
missing = on_disk - listed
extra = listed - on_disk
for u in sorted(missing):
    errors.append(f"sitemap.xml: page {u} not listed")
for u in sorted(extra):
    errors.append(f"sitemap.xml: lists non-existent {u}")

# --- report --------------------------------------------------------------
print(f"Checked {len(list(pages()))} pages.")
if warnings:
    print(f"\n{len(warnings)} warning(s):")
    for w in warnings[:40]:
        print("  ⚠ " + w)
    if len(warnings) > 40:
        print(f"  … and {len(warnings)-40} more")
if errors:
    print(f"\n{len(errors)} ERROR(s):")
    for e in errors:
        print("  ✗ " + e)
    sys.exit(1)
print("\n✓ All structural checks passed.")

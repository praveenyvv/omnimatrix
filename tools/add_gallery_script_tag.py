"""
add_gallery_script_tag.py
Inserts <script src="gallery-data.js"></script> into all gallery HTML files
just before the existing <script defer src="script.js"> tag.
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

GALLERY_PAGES = [
    "projects.html",
    "service1.html",
    "service2.html",
    "service3.html",
    "service4.html",
    "service5.html",
    "service6.html",
]

GALLERY_TAG = '<script src="gallery-data.js"></script>'

for fname in GALLERY_PAGES:
    path = os.path.join(BASE, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # Skip if already inserted
    if 'gallery-data.js' in html:
        print(f"  SKIP (already has tag): {fname}")
        continue

    # Insert before the <script defer src="script.js"> line
    new_html = re.sub(
        r'(<script\s[^>]*src=["\']script\.js["\'][^>]*>)',
        GALLERY_TAG + '\n    \\1',
        html,
        count=1
    )

    if new_html == html:
        print(f"  WARN: could not find script.js tag in {fname}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  UPDATED: {fname}")

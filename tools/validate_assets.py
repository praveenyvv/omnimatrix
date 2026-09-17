"""
validate_assets.py  (updated for new folder structure)
Checks that every <img src>, <link href>, <video poster>, <video src>
in all HTML files resolves to an existing file on disk.
Run from the project root OR from tools/ — it auto-detects.
"""
import os, re, glob

# Auto-detect root: if run from tools/, go one level up
_here = os.path.dirname(os.path.abspath(__file__))
BASE = _here if os.path.exists(os.path.join(_here, "index.html")) else os.path.dirname(_here)

def strip_qs(src):
    return src.split("?")[0]

errors = []

# Collect all HTML files: root + pages/
html_files = glob.glob(os.path.join(BASE, "*.html")) + \
             glob.glob(os.path.join(BASE, "pages", "*.html"))

for html in html_files:
    html_dir = os.path.dirname(html)  # resolve relative paths from here
    with open(html, encoding="utf-8") as f:
        content = f.read()

    # img src, video src, video poster, link href (images only)
    for attr, val in re.findall(r'(src|href|poster)=["\']([^"\']+)["\']', content):
        bare = strip_qs(val)
        if bare.startswith("http") or bare.startswith("#") or bare.startswith("mailto") or bare.startswith("tel"):
            continue
        ext = os.path.splitext(bare)[1].lower()
        is_image = ext in {'.png','.jpg','.jpeg','.gif','.webp','.svg','.ico'}
        is_media = ext in {'.mp4','.webm','.ogg'}
        is_style = ext in {'.css'}
        is_script = ext == '.js'
        if not (is_image or is_media or is_style or is_script):
            continue
        full = os.path.normpath(os.path.join(html_dir, bare))
        if not os.path.exists(full):
            errors.append(f"MISSING [{os.path.basename(html)}]  {bare}")

if errors:
    print(f"\nFAIL: {len(errors)} missing asset(s):\n")
    for e in sorted(set(errors)):
        print("  ", e)
else:
    print(f"\nPASS: ALL assets valid across {len(html_files)} HTML files.\n")

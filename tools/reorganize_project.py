"""
reorganize_project.py
Moves files into a clean folder structure:

Version 2/
├── pages/                  ← all HTML pages (except index.html stays at root)
│   ├── about.html
│   ├── projects.html
│   ├── quality.html
│   ├── service1.html … service6.html
├── assets/
│   ├── css/                ← styles.css
│   ├── js/                 ← script.js, gallery-data.js
│   └── video/              ← hero-video.mp4
├── website-assets/         ← image folders (unchanged, canonical)
├── tools/                  ← all Python utility scripts
│   ├── refresh_gallery.py
│   ├── validate_assets.py
│   ├── audit_unused_files.py
│   ├── update_image_paths.py
│   ├── convert_galleries_to_dynamic.py
│   ├── add_gallery_script_tag.py
│   ├── delete_unused.py
│   └── fix_poster.py
├── gallery-manifest.json   ← stays at root (read by gallery-data.js)
└── index.html              ← stays at root (entry point)
"""

import os, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))

# ── 1. Create folders ────────────────────────────────────────────────────────
FOLDERS = [
    "pages",
    os.path.join("assets", "css"),
    os.path.join("assets", "js"),
    os.path.join("assets", "video"),
    "tools",
]
for f in FOLDERS:
    os.makedirs(os.path.join(BASE, f), exist_ok=True)
    print(f"  MKDIR: {f}")

# ── 2. Define moves: (src_rel, dst_rel) ─────────────────────────────────────
MOVES = [
    # HTML pages (index.html stays at root)
    ("about.html",                          "pages/about.html"),
    ("projects.html",                       "pages/projects.html"),
    ("quality.html",                        "pages/quality.html"),
    ("service1.html",                       "pages/service1.html"),
    ("service2.html",                       "pages/service2.html"),
    ("service3.html",                       "pages/service3.html"),
    ("service4.html",                       "pages/service4.html"),
    ("service5.html",                       "pages/service5.html"),
    ("service6.html",                       "pages/service6.html"),
    # CSS
    ("styles.css",                          "assets/css/styles.css"),
    # JS
    ("script.js",                           "assets/js/script.js"),
    ("gallery-data.js",                     "assets/js/gallery-data.js"),
    # Video
    ("hero-video.mp4",                      "assets/video/hero-video.mp4"),
    # Python tools
    ("refresh_gallery.py",                  "tools/refresh_gallery.py"),
    ("validate_assets.py",                  "tools/validate_assets.py"),
    ("audit_unused_files.py",               "tools/audit_unused_files.py"),
    ("update_image_paths.py",               "tools/update_image_paths.py"),
    ("convert_galleries_to_dynamic.py",     "tools/convert_galleries_to_dynamic.py"),
    ("add_gallery_script_tag.py",           "tools/add_gallery_script_tag.py"),
    ("delete_unused.py",                    "tools/delete_unused.py"),
    ("fix_poster.py",                       "tools/fix_poster.py"),
]

print("\n=== Moving files ===")
for src_rel, dst_rel in MOVES:
    src = os.path.join(BASE, src_rel)
    dst = os.path.join(BASE, dst_rel)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"  MOVED: {src_rel} -> {dst_rel}")
    else:
        print(f"  SKIP (not found): {src_rel}")

# ── 3. Path prefix maps for rewriting HTML/JS/CSS references ─────────────────
# We need to rewrite references in HTML/JS after moving files.
# From-location → adjustments needed:
#
# index.html (stays at root):
#   styles.css          → assets/css/styles.css
#   script.js           → assets/js/script.js
#   gallery-data.js     → assets/js/gallery-data.js
#   hero-video.mp4      → assets/video/hero-video.mp4
#   pages/*.html        → pages/*.html   (nav links)
#
# pages/*.html (moved to pages/):
#   styles.css          → ../assets/css/styles.css
#   script.js           → ../assets/js/script.js
#   gallery-data.js     → ../assets/js/gallery-data.js
#   website-assets/...  → ../website-assets/...
#   index.html links    → ../index.html
#   about.html          → about.html  (same dir)
#   projects.html       → projects.html (same dir)
#   quality.html        → quality.html (same dir)
#   service*.html       → service*.html (same dir)
#   gallery-manifest.json → ../gallery-manifest.json

REWRITE_INDEX = [
    # JS/CSS
    (r'href=["\']styles\.css["\']',             'href="assets/css/styles.css"'),
    (r'src=["\']script\.js["\']',               'src="assets/js/script.js"'),
    (r'src=["\']gallery-data\.js["\']',         'src="assets/js/gallery-data.js"'),
    # defer variant
    (r'defer\s+src=["\']script\.js["\']',       'defer src="assets/js/script.js"'),
    # video
    (r'src=["\']hero-video\.mp4["\']',          'src="assets/video/hero-video.mp4"'),
    # page nav links (only the ones without a path prefix already)
    (r'href=["\']about\.html["\']',             'href="pages/about.html"'),
    (r'href=["\']projects\.html["\']',          'href="pages/projects.html"'),
    (r'href=["\']quality\.html["\']',           'href="pages/quality.html"'),
    (r'href=["\']service1\.html["\']',          'href="pages/service1.html"'),
    (r'href=["\']service2\.html["\']',          'href="pages/service2.html"'),
    (r'href=["\']service3\.html["\']',          'href="pages/service3.html"'),
    (r'href=["\']service4\.html["\']',          'href="pages/service4.html"'),
    (r'href=["\']service5\.html["\']',          'href="pages/service5.html"'),
    (r'href=["\']service6\.html["\']',          'href="pages/service6.html"'),
]

REWRITE_PAGES = [
    # JS/CSS (one level up)
    (r'href=["\']styles\.css["\']',             'href="../assets/css/styles.css"'),
    (r'src=["\']script\.js["\']',               'src="../assets/js/script.js"'),
    (r'defer\s+src=["\']script\.js["\']',       'defer src="../assets/js/script.js"'),
    (r'src=["\']gallery-data\.js["\']',         'src="../assets/js/gallery-data.js"'),
    # images (one level up)
    (r'src=["\']website-assets/',               'src="../website-assets/'),
    (r'href=["\']website-assets/',              'href="../website-assets/'),
    (r'poster=["\']website-assets/',            'poster="../website-assets/'),
    # gallery-manifest.json
    (r"'gallery-manifest\.json",                "'../gallery-manifest.json"),
    # Nav: index.html links
    (r'href=["\']index\.html',                  'href="../index.html'),
    # Nav: sibling page links → same dir (already correct since all in pages/)
    # But links might already say "about.html" etc. — they stay relative, correct.
    # favicon / logo links that say website-assets already handled above.
]

def rewrite_file(path, rules):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    original = content
    for pattern, replacement in rules:
        content = re.sub(pattern, replacement, content)
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  REWRITTEN: {os.path.relpath(path, BASE)}")
    else:
        print(f"  unchanged: {os.path.relpath(path, BASE)}")

print("\n=== Rewriting paths in index.html ===")
rewrite_file(os.path.join(BASE, "index.html"), REWRITE_INDEX)

print("\n=== Rewriting paths in pages/*.html ===")
pages_dir = os.path.join(BASE, "pages")
for fname in os.listdir(pages_dir):
    if fname.endswith(".html"):
        rewrite_file(os.path.join(pages_dir, fname), REWRITE_PAGES)

# ── 4. Rewrite gallery-data.js (stays at root) — paths are relative to HTML pages
# gallery-data.js is now loaded from assets/js/ but the image paths inside it
# are used in <img src="..."> from pages/ → need ../website-assets/...
# Actually gallery-data.js itself doesn't need path changes — the img src
# values must be correct relative to the HTML page that uses them.
# pages/service1.html loads ../assets/js/gallery-data.js which has
# "website-assets/..." paths — from pages/ that means "../website-assets/..."
# So we need to update the paths inside gallery-data.js.
print("\n=== Updating paths inside gallery-data.js ===")
gdjs = os.path.join(BASE, "assets", "js", "gallery-data.js")
if os.path.exists(gdjs):
    with open(gdjs, encoding='utf-8') as f:
        content = f.read()
    # Currently: "website-assets/..."
    # After move, pages/ uses it so needs: "../website-assets/..."
    # index.html (root) uses it so needs: "website-assets/..."
    # ── The src values will be resolved relative to the HTML page's location.
    # Since both index.html (root) AND pages/*.html use gallery-data.js,
    # and they're at different depths, we need a consistent approach.
    # Best: use ABSOLUTE paths won't work. Use root-relative paths (/website-assets/...)
    # but that requires a server. Since we're file://, we must pick one.
    # index.html does NOT have a gallery (only pages do), so all gallery consumers
    # are in pages/ → prefix with ../website-assets/
    new_content = content.replace('"website-assets/', '"../website-assets/')
    if new_content != content:
        with open(gdjs, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("  UPDATED: assets/js/gallery-data.js — paths prefixed with ../")
    else:
        print("  unchanged: gallery-data.js")

# Also update refresh_gallery.py so it writes the correct prefix
print("\n=== Updating tools/refresh_gallery.py output prefix ===")
rg = os.path.join(BASE, "tools", "refresh_gallery.py")
if os.path.exists(rg):
    with open(rg, encoding='utf-8') as f:
        rg_content = f.read()
    # Change the path prefix from "website-assets/..." to "../website-assets/..."
    rg_content = rg_content.replace(
        'f"website-assets/{folder_name}/{fname}?v={v}"',
        'f"../website-assets/{folder_name}/{fname}?v={v}"'
    )
    # Update output path for gallery-data.js
    rg_content = rg_content.replace(
        'out_path = os.path.join(BASE, "gallery-data.js")',
        'out_path = os.path.join(BASE, "..", "assets", "js", "gallery-data.js")'
    )
    rg_content = rg_content.replace(
        'json_path = os.path.join(BASE, "gallery-manifest.json")',
        'json_path = os.path.join(BASE, "..", "gallery-manifest.json")'
    )
    # Update BASE
    rg_content = rg_content.replace(
        'BASE = os.path.dirname(os.path.abspath(__file__))',
        'BASE = os.path.dirname(os.path.abspath(__file__))  # tools/\nASSOC_BASE = os.path.join(BASE, "..")  # project root'
    )
    rg_content = rg_content.replace(
        'ASSETS = os.path.join(BASE, "website-assets")',
        'ASSETS = os.path.join(ASSOC_BASE, "website-assets")'
    )
    with open(rg, 'w', encoding='utf-8') as f:
        f.write(rg_content)
    print("  UPDATED: tools/refresh_gallery.py")

# ── 5. Delete now-empty images/ subfolders ───────────────────────────────────
print("\n=== Removing empty images/ subfolders ===")
images_dir = os.path.join(BASE, "images")
if os.path.exists(images_dir):
    try:
        shutil.rmtree(images_dir)
        print("  REMOVED: images/ (was entirely empty)")
    except Exception as e:
        print(f"  WARN: could not remove images/ — {e}")

print("\n=== Done! Final structure ===")
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in {'__pycache__', '.git'}]
    level = root.replace(BASE, '').count(os.sep)
    indent = '  ' * level
    folder = os.path.basename(root)
    print(f"{indent}{folder}/")
    sub = '  ' * (level + 1)
    for fname in sorted(files):
        print(f"{sub}{fname}")

"""
audit_unused_files.py
Scans all HTML + gallery-data.js to build a list of every asset in use,
then walks the entire project folder and reports:
  - Unused image/media files (safe to delete)
  - Duplicate files (same content, different names)
  - Files that will be KEPT
Prints a full report, writes delete_unused.py ready to execute.
"""

import os, re, json, hashlib, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Extensions to consider as "asset" files ─────────────────────────────────
ASSET_EXTS = {'.jpg','.jpeg','.png','.gif','.webp','.svg','.ico',
              '.mp4','.webm','.ogg','.pdf'}

# ── Folders / files to NEVER touch ──────────────────────────────────────────
SKIP_DIRS = {'node_modules', '.git', '__pycache__'}
SKIP_FILES = {
    # scripts & config
    'script.js','styles.css','gallery-data.js','gallery-manifest.json',
    'refresh_gallery.py','validate_assets.py','update_image_paths.py',
    'convert_galleries_to_dynamic.py','add_gallery_script_tag.py',
    'audit_unused_files.py','delete_unused.py',
    # html
}

# ─────────────────────────────────────────────────────────────────────────────
# 1. Collect all USED asset paths from HTML files & gallery-data.js
# ─────────────────────────────────────────────────────────────────────────────
used_rel = set()

# From HTML files
for html_path in glob.glob(os.path.join(BASE, '*.html')):
    with open(html_path, encoding='utf-8') as f:
        content = f.read()
    # src="...", href="...", poster="..." attributes
    for raw in re.findall(r'(?:src|href|poster)=["\']([^"\'#?]+)', content):
        clean = raw.split('?')[0].strip()
        ext = os.path.splitext(clean)[1].lower()
        if ext in ASSET_EXTS:
            used_rel.add(clean.replace('/', os.sep))

# From gallery-data.js (window.GALLERY_MANIFEST)
gdjs = os.path.join(BASE, 'gallery-data.js')
if os.path.exists(gdjs):
    with open(gdjs, encoding='utf-8') as f:
        js_content = f.read()
    # Extract all quoted paths inside the JS object
    for raw in re.findall(r'"(website-assets/[^"?]+)', js_content):
        clean = raw.split('?')[0]
        used_rel.add(clean.replace('/', os.sep))

# Normalise to absolute paths
used_abs = set(os.path.normpath(os.path.join(BASE, r)) for r in used_rel)

print(f"[USED] {len(used_abs)} asset references found in HTML + gallery-data.js")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Walk the project directory and collect all asset files
# ─────────────────────────────────────────────────────────────────────────────
all_assets = []
for root, dirs, files in os.walk(BASE):
    # Skip hidden / irrelevant dirs
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
    for fname in files:
        if fname in SKIP_FILES:
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext in ASSET_EXTS:
            full = os.path.normpath(os.path.join(root, fname))
            all_assets.append(full)

print(f"[FOUND] {len(all_assets)} asset files on disk")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Classify: used vs unused
# ─────────────────────────────────────────────────────────────────────────────
unused = [f for f in all_assets if f not in used_abs]
kept   = [f for f in all_assets if f in used_abs]

# ─────────────────────────────────────────────────────────────────────────────
# 4. Find duplicates by MD5 hash (among ALL files, including used ones)
# ─────────────────────────────────────────────────────────────────────────────
def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

hash_map = {}
for f in all_assets:
    try:
        h = md5(f)
        hash_map.setdefault(h, []).append(f)
    except Exception:
        pass

dup_groups = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
dup_to_delete = []
for h, paths in dup_groups.items():
    # Keep the one in website-assets/ if present, otherwise keep first
    wa = [p for p in paths if 'website-assets' in p]
    keeper = wa[0] if wa else paths[0]
    victims = [p for p in paths if p != keeper]
    dup_to_delete.extend(victims)

# ─────────────────────────────────────────────────────────────────────────────
# 5. Final delete list = unused + duplicate victims
# ─────────────────────────────────────────────────────────────────────────────
to_delete = sorted(set(unused + dup_to_delete))

# ─────────────────────────────────────────────────────────────────────────────
# 6. Report
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  WILL KEEP  : {len(kept)} files")
print(f"  UNUSED     : {len(unused)} files")
print(f"  DUPLICATES : {len(dup_to_delete)} extra copies")
print(f"  TO DELETE  : {len(to_delete)} files total")
print(f"{'='*60}")

if to_delete:
    print("\n--- FILES TO DELETE ---")
    for f in to_delete:
        tag = "[DUP]" if f in dup_to_delete else "[UNUSED]"
        print(f"  {tag} {os.path.relpath(f, BASE)}")

    # Write the delete script
    delete_script = os.path.join(BASE, 'delete_unused.py')
    with open(delete_script, 'w', encoding='utf-8') as out:
        out.write('"""Auto-generated by audit_unused_files.py — deletes unused/duplicate assets."""\n')
        out.write('import os\n')
        out.write(f'BASE = r"{BASE}"\n')
        out.write('files = [\n')
        for f in to_delete:
            out.write(f'    r"{f}",\n')
        out.write(']\n\n')
        out.write('deleted = 0\n')
        out.write('for f in files:\n')
        out.write('    if os.path.exists(f):\n')
        out.write('        os.remove(f)\n')
        out.write('        print("DELETED:", os.path.relpath(f, BASE))\n')
        out.write('        deleted += 1\n')
        out.write('print(f"\\nDone. {deleted} files deleted.")\n')
    print(f"\n[OK] delete_unused.py written. Review the list above, then run it.")
else:
    print("\nNothing to delete — project folder is already clean!")

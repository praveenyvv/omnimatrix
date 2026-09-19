"""
convert_to_pure_static.py
=========================
Removes all PHP / dynamic loaders / manifest files,
and inserts clean, standard static HTML <img> cards directly into
projects.html and service1-6.html.
"""

import os, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
PAGES_DIR = os.path.join(ROOT, "pages")
ASSETS_DIR = os.path.join(ROOT, "website-assets")

# 1. Clean up unneeded files and directories
clean_targets = [
    os.path.join(ROOT, "api"),
    os.path.join(ROOT, ".github"),
    os.path.join(ROOT, "start_website.bat"),
    os.path.join(ROOT, "sync_gallery.bat"),
    os.path.join(ROOT, "gallery-manifest.json"),
    os.path.join(ROOT, "assets", "js", "gallery-data.js"),
    os.path.join(ROOT, "tools", "convert_galleries_to_dynamic.py"),
    os.path.join(ROOT, "tools", "add_gallery_script_tag.py"),
    os.path.join(ROOT, "tools", "dev_server.py"),
    os.path.join(ROOT, "tools", "refresh_gallery.py"),
    os.path.join(ROOT, "tools", "tighten_footer_logo.py"),
    os.path.join(ROOT, "tools", "enhance_footer_logo.py"),
]

for t in clean_targets:
    if os.path.isdir(t):
        shutil.rmtree(t)
        print(f"Deleted directory: {os.path.relpath(t, ROOT)}")
    elif os.path.isfile(t):
        os.remove(t)
        print(f"Deleted file: {os.path.relpath(t, ROOT)}")

# 2. Map of gallery keys to asset folders
GALLERY_FOLDERS = {
    "lab-products":     "3-Products-Laboratory-Plasticware",
    "injection-molds":  "4-Services-Injection-Molds",
    "press-tools":      "5-Services-Press-Tools",
    "die-casting":      "6-Services-Die-Casting",
    "jigs-fixtures":    "7-Services-Jigs-Fixtures",
    "spm-automation":   "8-Services-SPM-Automation",
}

SERVICE_FOLDERS = {
    "service1.html": "4-Services-Injection-Molds",
    "service2.html": "5-Services-Press-Tools",
    "service3.html": "6-Services-Die-Casting",
    "service4.html": "7-Services-Jigs-Fixtures",
    "service5.html": "6-Services-Die-Casting",
    "service6.html": "8-Services-SPM-Automation",
}

def clean_alt_text(filename):
    name = re.sub(r'^\d+-', '', filename)
    name = re.sub(r'\.(jpg|jpeg|png|webp|gif)$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[-_]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name.title()

def generate_cards_html(folder_name):
    folder_path = os.path.join(ASSETS_DIR, folder_name)
    if not os.path.exists(folder_path):
        return ""
    files = sorted(f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')))
    cards = []
    for f in files:
        alt = clean_alt_text(f)
        src = f"../website-assets/{folder_name}/{f}?v=12"
        card = f'''            <div class="gallery-card">
                <img src="{src}" alt="{alt}" loading="lazy">
                <div class="gallery-card-overlay"><div class="gallery-zoom-icon">&#128269;</div></div>
            </div>'''
        cards.append(card)
    return "\n".join(cards)

# 3. Update projects.html
projects_path = os.path.join(PAGES_DIR, "projects.html")
with open(projects_path, encoding='utf-8') as f:
    p_html = f.read()

# Remove gallery-data.js script tag
p_html = re.sub(r'\s*<script\s+src=["\'].*?gallery-data\.js["\']></script>', '', p_html)

for key, folder in GALLERY_FOLDERS.items():
    cards_html = generate_cards_html(folder)
    # Replace the container with data-gallery="key"
    pattern = rf'<div class="gallery-grid" data-gallery="{key}"[^>]*>.*?</div>'
    replacement = f'<div class="gallery-grid" style="padding-top: 15px; padding-bottom: 30px;">\n{cards_html}\n        </div>'
    p_html = re.sub(pattern, replacement, p_html, flags=re.DOTALL)

with open(projects_path, 'w', encoding='utf-8') as f:
    f.write(p_html)
print("Updated projects.html with static gallery cards.")

# 4. Update service1-6.html
for s_file, folder in SERVICE_FOLDERS.items():
    s_path = os.path.join(PAGES_DIR, s_file)
    if not os.path.exists(s_path):
        continue
    with open(s_path, encoding='utf-8') as f:
        s_html = f.read()

    # Remove gallery-data.js script tag
    s_html = re.sub(r'\s*<script\s+src=["\'].*?gallery-data\.js["\']></script>', '', s_html)

    cards_html = generate_cards_html(folder)
    # Replace the gallery-grid container
    pattern = r'<div class="gallery-grid"[^>]*>.*?</div>'
    replacement = f'<div class="gallery-grid">\n{cards_html}\n        </div>'
    s_html = re.sub(pattern, replacement, s_html, flags=re.DOTALL, count=1)

    with open(s_path, 'w', encoding='utf-8') as f:
        f.write(s_html)
    print(f"Updated {s_file} with static gallery cards.")

# 5. Remove gallery-data.js script tags from all remaining HTML files
for h_file in [os.path.join(ROOT, "index.html"), os.path.join(PAGES_DIR, "about.html"), os.path.join(PAGES_DIR, "quality.html")]:
    if os.path.exists(h_file):
        with open(h_file, encoding='utf-8') as f:
            h_html = f.read()
        h_html = re.sub(r'\s*<script\s+src=["\'].*?gallery-data\.js["\']></script>', '', h_html)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(h_html)

print("Cleaned up script tags across all pages.")

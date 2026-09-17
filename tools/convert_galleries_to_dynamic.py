"""
convert_galleries_to_dynamic.py
Replaces all hardcoded gallery-card blocks in projects.html and service1-6.html
with a single empty <div class="gallery-grid" data-gallery="KEY"> container.
The JS loader fills the cards at runtime from gallery-manifest.json.
"""

import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Replace pattern ──────────────────────────────────────────────────────────
# Match: <div class="gallery-grid" ...> ... </div>  (containing gallery-cards)
GRID_RE = re.compile(
    r'<div class="gallery-grid"[^>]*>(.*?)</div>(?=\s*(?:\n|\r|\s)*(?:<hr|</main|<!--))',
    re.DOTALL
)

# ── projects.html: 6 gallery sections ────────────────────────────────────────
PROJECTS_KEYS = [
    "lab-products",
    "injection-molds",
    "press-tools",
    "die-casting",
    "jigs-fixtures",
    "spm-automation",
]

# ── service pages: one gallery each ─────────────────────────────────────────
SERVICE_KEY = {
    "service1.html": "service1-gallery",
    "service2.html": "service2-gallery",
    "service3.html": "service3-gallery",
    "service4.html": "service4-gallery",
    "service5.html": "service5-gallery",
    "service6.html": "service6-gallery",
}

LOADING_PLACEHOLDER = (
    '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:#94a3b8;">'
    '<div style="width:40px;height:40px;border:3px solid #e2e8f0;border-top-color:#2563eb;'
    'border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 12px;"></div>'
    'Loading gallery...</div>'
)

def rewrite_projects(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    matches = list(GRID_RE.finditer(html))
    if len(matches) < len(PROJECTS_KEYS):
        print(f"  WARN: only {len(matches)} gallery-grids found in projects.html (expected {len(PROJECTS_KEYS)})")

    # Replace in reverse order to preserve string indices
    for i, m in reversed(list(enumerate(matches))):
        key = PROJECTS_KEYS[i] if i < len(PROJECTS_KEYS) else f"gallery-{i}"
        replacement = (
            f'<div class="gallery-grid" data-gallery="{key}" '
            f'style="padding-top: 15px; padding-bottom: 30px;">'
            f'{LOADING_PLACEHOLDER}</div>'
        )
        html = html[:m.start()] + replacement + html[m.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  UPDATED: projects.html — {len(matches)} galleries converted")


def rewrite_service(path, key):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    matches = list(GRID_RE.finditer(html))
    if not matches:
        print(f"  WARN: no gallery-grid found in {os.path.basename(path)}")
        return

    # Only replace the first/main gallery grid (ignore any extras in footer etc.)
    m = matches[0]
    replacement = (
        f'<div class="gallery-grid" data-gallery="{key}">'
        f'{LOADING_PLACEHOLDER}</div>'
    )
    html = html[:m.start()] + replacement + html[m.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  UPDATED: {os.path.basename(path)} — gallery key='{key}'")


print("\n=== Converting galleries to dynamic ===")
rewrite_projects(os.path.join(BASE, "projects.html"))

for fname, key in SERVICE_KEY.items():
    rewrite_service(os.path.join(BASE, fname), key)

print("\nDone. Open the pages in a browser to verify (serve via a local server).")

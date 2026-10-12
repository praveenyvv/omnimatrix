"""
tools/rename_to_seo_urls.py
Safely renames pages to SEO-optimized keyword slugs and updates
all references across index.html and pages/*.html.
"""
import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(BASE_DIR, "pages")

RENAME_MAP = {
    "projects.html": "products.html",
    "service1.html": "plastic-injection-moulds.html",
    "service2.html": "press-tools-stamping-dies.html",
    "service3.html": "die-casting-dies.html",
    "service4.html": "scientific-laboratory-plasticware.html",
    "service5.html": "aerospace-drone-components.html",
    "service6.html": "precision-electronic-enclosures.html",
}

def execute_renaming():
    # 1. First, rename the actual physical files in pages/
    print("=== Step 1: Renaming physical files in pages/ ===")
    for old_name, new_name in RENAME_MAP.items():
        old_path = os.path.join(PAGES_DIR, old_name)
        new_path = os.path.join(PAGES_DIR, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"Renamed: pages/{old_name} -> pages/{new_name}")
        elif os.path.exists(new_path):
            print(f"Already renamed: pages/{new_name}")
        else:
            print(f"Warning: Neither {old_name} nor {new_name} found!")

    # 2. Update all occurrences in all HTML files
    print("\n=== Step 2: Updating link references in HTML files ===")
    html_files = glob.glob(os.path.join(BASE_DIR, "*.html")) + glob.glob(os.path.join(PAGES_DIR, "*.html"))
    
    for html_path in html_files:
        rel_path = os.path.relpath(html_path, BASE_DIR)
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content = content
        replaced_counts = {}

        for old_name, new_name in RENAME_MAP.items():
            # Pattern matches old_name bounded by /, ", ', ?, or #
            pattern = re.compile(r'(?<=[\"\'/])' + re.escape(old_name) + r'(?=[\"\'?#])')
            count = len(pattern.findall(updated_content))
            if count > 0:
                updated_content = pattern.sub(new_name, updated_content)
                replaced_counts[old_name] = count

        if updated_content != content:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Updated {rel_path}: {replaced_counts}")
        else:
            print(f"No changes needed in {rel_path}")

    print("\n=== URL Renaming Completed Successfully ===")

if __name__ == "__main__":
    execute_renaming()

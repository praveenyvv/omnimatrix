import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "pages", "*.html"))
for path in files:
    with open(path, encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'href=(["\'][^"\']*styles\.css)(?:\?v=\d+)?(["\'])', r'href=\1?v=6\2', c)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Updated CSS cache-buster to ?v=5 across {len(files)} HTML files.")

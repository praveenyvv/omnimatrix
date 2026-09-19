import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "pages", "*.html"))
for path in files:
    with open(path, encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'02-logo-footer-stacked\.png(?:\?v=\d+)?', '02-logo-footer-stacked.png?v=13', c)
    c = re.sub(r'styles\.css(?:\?v=\d+)?', 'styles.css?v=13', c)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Updated footer logo & CSS cache-buster across {len(files)} HTML files.")

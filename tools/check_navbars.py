import glob, re

for path in sorted(glob.glob("*.html") + glob.glob("pages/*.html")):
    with open(path, encoding='utf-8') as f:
        c = f.read()
    nav = re.findall(r'<ul class="nav-links">(.*?)</ul>', c, re.DOTALL)
    if nav:
        items = re.findall(r'<a[^>]*>(.*?)</a>', nav[0], re.DOTALL)
        clean_items = [re.sub(r'<.*?>', '', x).strip() for x in items]
        print(path, ":", clean_items)

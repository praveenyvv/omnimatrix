path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()
c = c.replace('poster="hero-poster.jpg"', 'poster="website-assets/10-Homepage-Hero-About-Workflow/hero-poster.jpg"')
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed poster path in index.html')

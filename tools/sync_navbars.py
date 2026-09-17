import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
PAGES_DIR = os.path.join(ROOT, "pages")

PAGES = [
    "about.html",
    "projects.html",
    "quality.html",
    "service1.html",
    "service2.html",
    "service3.html",
    "service4.html",
    "service5.html",
    "service6.html",
]

def make_nav(current_page):
    about_active = ' class="active"' if current_page == 'about.html' else ''
    quality_active = ' class="active"' if current_page == 'quality.html' else ''
    products_active = ' active' if current_page == 'projects.html' else ''

    return f'''            <nav id="navMenu">
                <ul class="nav-links">
                    <li><a href="../index.html#home">Home</a></li>
                    <li><a href="about.html"{about_active}>About Us</a></li>
                    <li><a href="../index.html#capabilities">Capabilities</a></li>
                    <li><a href="../index.html#workflow">Workflow</a></li>
                    <li><a href="../index.html#engineering-services">Services</a></li>
                    <li><a href="../index.html#project-fields">Industries</a></li>
                    <li class="nav-dropdown-item">
                        <a href="projects.html" class="nav-dropdown-trigger{products_active}">
                            Products
                            <svg class="dropdown-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a href="projects.html">Injection Molds</a></li>
                            <li><a href="projects.html">Press Tools &amp; Dies</a></li>
                            <li><a href="projects.html">Die Casting Dies</a></li>
                            <li><a href="projects.html">Jigs &amp; Fixtures</a></li>
                            <li><a href="projects.html">SPM &amp; Automation</a></li>
                        </ul>
                    </li>
                    <li><a href="quality.html"{quality_active}>Quality</a></li>
                    <li><a href="../index.html#contact" class="nav-cta">Get a Quote</a></li>
                </ul>
            </nav>'''

for fname in PAGES:
    path = os.path.join(PAGES_DIR, fname)
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()

    new_nav = make_nav(fname)
    # Replace the <nav id="navMenu"> ... </nav> block
    updated_content = re.sub(
        r'<nav id="navMenu">.*?</nav>',
        new_nav,
        content,
        flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"Updated navbar in pages/{fname}")

print("All pages navbar sync complete!")

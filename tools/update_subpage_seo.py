"""
tools/update_subpage_seo.py
Adds Canonical URL, OpenGraph tags, and fine-tuned SEO titles to all subpages in pages/.
"""
import os
import re
import glob

PAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pages")

PAGE_SEO = {
    "products.html": {
        "title": "Manufactured Products & Capabilities Portfolio | OmniMatrix Technologies",
        "desc": "Explore OmniMatrix Technologies' comprehensive portfolio of precision manufactured Tooling, Injection Moulds, and Finished Products including Scientific Labware, Aerospace UAV components, and Electronic Enclosures.",
    },
    "plastic-injection-moulds.html": {
        "title": "High-Precision Plastic Injection Moulds | OmniMatrix Technologies",
        "desc": "Custom high-precision plastic injection mould design and manufacturing. Multi-cavity, hot runner, and tight-tolerance tooling engineered in Hyderabad, India.",
    },
    "press-tools-stamping-dies.html": {
        "title": "Precision Press Tools & Sheet Metal Stamping Dies | OmniMatrix Technologies",
        "desc": "Progressive, transfer, and compound sheet metal stamping dies. Precision engineered press tools for automotive, aerospace, and industrial manufacturing.",
    },
    "die-casting-dies.html": {
        "title": "Pressure Die Casting Dies (PDC) | OmniMatrix Technologies",
        "desc": "High-pressure and low-pressure aluminium and zinc die casting dies engineered for extreme thermal fatigue resistance and high-volume production.",
    },
    "scientific-laboratory-plasticware.html": {
        "title": "Scientific Laboratory Plasticware & Consumables | OmniMatrix Technologies",
        "desc": "High-volume manufacturing of precision medical and scientific laboratory plasticware, cryovials, centrifuge tubes, and diagnostics consumables.",
    },
    "aerospace-drone-components.html": {
        "title": "Aerospace & UAV Drone Polymer Components | OmniMatrix Technologies",
        "desc": "Lightweight, high-strength engineered polymer components, housings, and precision moulded structural parts for aerospace and UAV drone applications.",
    },
    "precision-electronic-enclosures.html": {
        "title": "Precision Electronic Enclosures & Housings | OmniMatrix Technologies",
        "desc": "IP67 waterproof and flame-retardant precision molded electronic enclosures, junction boxes, IoT sensor casings, and industrial housings.",
    },
    "about.html": {
        "title": "About Us | OmniMatrix Technologies Private Limited",
        "desc": "Learn about OmniMatrix Technologies - over 20 years of precision engineering excellence delivering integrated tooling, automation, and finished manufacturing.",
    },
    "quality.html": {
        "title": "Quality Assurance & Metrology Standards | OmniMatrix Technologies",
        "desc": "Rigorous quality assurance, precision CMM inspection, and ISO standards ensuring micrometer-level accuracy across all tooling and manufactured products.",
    },
}

def update_seo():
    for filename, meta in PAGE_SEO.items():
        filepath = os.path.join(PAGES_DIR, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filename}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        canonical_url = f"https://omnimatrixs.com/pages/{filename}"

        # Build SEO head block
        seo_head = f"""    <title>{meta['title']}</title>
    <meta name="description" content="{meta['desc']}">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph / WhatsApp / LinkedIn / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="OmniMatrix Technologies Private Limited">
    <meta property="og:title" content="{meta['title']}">
    <meta property="og:description" content="{meta['desc']}">
    <meta property="og:image" content="https://omnimatrixs.com/website-assets/9-Branding-Logos/01-logo-header-horizontal.png">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{meta['title']}">
    <meta name="twitter:description" content="{meta['desc']}">
    <meta name="twitter:image" content="https://omnimatrixs.com/website-assets/9-Branding-Logos/01-logo-header-horizontal.png">"""

        # Replace existing title and description
        pattern = re.compile(r'<title>.*?</title>\s*<meta name="description" content=".*?">', re.DOTALL)
        if pattern.search(content):
            new_content = pattern.sub(seo_head, content, count=1)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated SEO for {filename}")
        else:
            print(f"Pattern match failed for {filename}")

if __name__ == "__main__":
    update_seo()

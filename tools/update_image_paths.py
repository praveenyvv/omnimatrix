"""
update_image_paths.py
- Rewrites all <img src> references in the 10 HTML files to point into website-assets/
- Deletes old duplicate image files from the project root / images/ subfolder
"""

import os, re, glob

BASE = r"c:\Users\prave\CS\Personal projects\Omni Matrix\Version 2"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Mapping: old src (without query string) → new website-assets/ path
# ─────────────────────────────────────────────────────────────────────────────
REMAP = {
    # ── Logos ────────────────────────────────────────────────────────────────
    "logo-omni.png":                  "website-assets/9-Branding-Logos/01-logo-header-horizontal.png",
    "logo-omni.jpg":                  "website-assets/9-Branding-Logos/03-logo-favicon.jpg",
    "logo-omni-stacked.png":          "website-assets/9-Branding-Logos/02-logo-footer-stacked.png",

    # ── About / Hero / Workflow ───────────────────────────────────────────────
    "about-facility.jpg":             "website-assets/10-Homepage-Hero-About-Workflow/about-facility.jpg",
    "hero-poster.jpg":                "website-assets/10-Homepage-Hero-About-Workflow/hero-poster.jpg",
    "step-tool-design.png":           "website-assets/10-Homepage-Hero-About-Workflow/step-tool-design.png",
    "step-cad-cam.png":               "website-assets/10-Homepage-Hero-About-Workflow/step-cad-cam.png",
    "step-precision-mfg.png":         "website-assets/10-Homepage-Hero-About-Workflow/step-precision-mfg.png",

    # ── End-to-End Engineering Services ──────────────────────────────────────
    "service-product-design.jpg":     "website-assets/10-Homepage-Hero-About-Workflow/service-product-design.jpg",
    "service-reverse-engineering.jpg":"website-assets/10-Homepage-Hero-About-Workflow/service-reverse-engineering.jpg",
    "service-2d-3d.jpg":              "website-assets/10-Homepage-Hero-About-Workflow/service-2d-3d.jpg",
    "service-cnc-vmc.jpg":            "website-assets/10-Homepage-Hero-About-Workflow/service-cnc-vmc.jpg",
    "service-tool-die.jpg":           "website-assets/10-Homepage-Hero-About-Workflow/service-tool-die.jpg",

    # ── Capabilities ─────────────────────────────────────────────────────────
    "cap-injection-molds.jpg":        "website-assets/1-Homepage-Capabilities/01-tooling-injection-molds.jpg",
    "cap-press-tools.jpg":            "website-assets/1-Homepage-Capabilities/02-stamping-press-tools.jpg",
    "cap-die-casting.jpg":            "website-assets/1-Homepage-Capabilities/03-foundry-die-casting.jpg",
    "cap-jigs-fixtures.jpg":          "website-assets/1-Homepage-Capabilities/04-precision-jigs-fixtures.jpg",
    "cap-spm-automation.jpg":         "website-assets/1-Homepage-Capabilities/05-automation-spm-machines.jpg",

    # ── Industry Sectors ─────────────────────────────────────────────────────
    "industry-automotive.jpg":        "website-assets/2-Homepage-Industry-Sectors/industry-automotive.jpg",
    "industry-electrical.jpg":        "website-assets/2-Homepage-Industry-Sectors/industry-electrical.jpg",
    "industry-aerospace.jpg":         "website-assets/2-Homepage-Industry-Sectors/industry-aerospace.jpg",
    "industry-medical.jpg":           "website-assets/2-Homepage-Industry-Sectors/industry-medical.jpg",
    "industry-consumer.jpg":          "website-assets/2-Homepage-Industry-Sectors/industry-consumer.jpg",
    "industry-proto.jpg":             "website-assets/2-Homepage-Industry-Sectors/industry-proto.jpg",

    # ── Lab Products ─────────────────────────────────────────────────────────
    "images/products/labware/reagent-bottles.jpg":  "website-assets/3-Products-Laboratory-Plasticware/01-reagent-bottles-graduated.jpg",
    "images/products/labware/wash-bottles.jpg":     "website-assets/3-Products-Laboratory-Plasticware/02-squeeze-wash-bottles.jpg",
    "images/products/labware/measuring-beakers.jpg":"website-assets/3-Products-Laboratory-Plasticware/03-graduated-measuring-beakers.jpg",
    "images/products/labware/centrifuge-tubes.jpg": "website-assets/3-Products-Laboratory-Plasticware/04-conical-centrifuge-tubes.jpg",
    "images/products/labware/test-tube-racks.jpg":  "website-assets/3-Products-Laboratory-Plasticware/05-multi-rack-test-tube-stands.jpg",
    "images/products/labware/pipette-stands.jpg":   "website-assets/3-Products-Laboratory-Plasticware/06-rotary-pipette-stands.jpg",
    "images/products/labware/aspirator-carboys.jpg":"website-assets/3-Products-Laboratory-Plasticware/07-aspirator-carboys-spigots.jpg",
    "images/products/labware/slide-boxes.jpg":      "website-assets/3-Products-Laboratory-Plasticware/08-microscope-slide-boxes.jpg",

    # ── Injection Molds ───────────────────────────────────────────────────────
    "images/services/injection-molds/mold-1.jpg": "website-assets/4-Services-Injection-Molds/01-mold-core-cavity-plates.jpg",
    "images/services/injection-molds/mold-2.jpg": "website-assets/4-Services-Injection-Molds/02-mold-base-assembly.jpg",
    "images/services/injection-molds/mold-3.jpg": "website-assets/4-Services-Injection-Molds/03-mold-core-cavity-pair.jpg",
    "images/services/injection-molds/mold-4.jpg": "website-assets/4-Services-Injection-Molds/04-mold-hot-runner-manifold.jpg",
    "images/services/injection-molds/mold-5.jpg": "website-assets/4-Services-Injection-Molds/05-mold-slide-action-mechanism.jpg",
    "images/services/injection-molds/mold-6.jpg": "website-assets/4-Services-Injection-Molds/06-mold-medical-cleanroom.jpg",
    "images/services/injection-molds/mold-7.jpg": "website-assets/4-Services-Injection-Molds/07-mold-precision-edm-inserts.jpg",
    "images/services/injection-molds/mold-8.jpg": "website-assets/4-Services-Injection-Molds/08-mold-hardened-cavity-inserts.jpg",

    # ── Press Tools ───────────────────────────────────────────────────────────
    "images/services/press-tools/press-1.jpg": "website-assets/5-Services-Press-Tools/01-press-progressive-die.jpg",
    "images/services/press-tools/press-2.jpg": "website-assets/5-Services-Press-Tools/02-press-stamping-strip-die.jpg",
    "images/services/press-tools/press-3.jpg": "website-assets/5-Services-Press-Tools/03-press-deep-draw-die.jpg",
    "images/services/press-tools/press-4.jpg": "website-assets/5-Services-Press-Tools/04-press-punching-piercing-tool.jpg",
    "images/services/press-tools/press-5.jpg": "website-assets/5-Services-Press-Tools/05-press-heavy-duty-die-set.jpg",
    "images/services/press-tools/press-6.jpg": "website-assets/5-Services-Press-Tools/06-press-sheet-metal-tooling.jpg",

    # ── Die Casting ───────────────────────────────────────────────────────────
    "images/services/die-casting/diecast-1.jpg": "website-assets/6-Services-Die-Casting/01-diecast-aluminum-mold.jpg",
    "images/services/die-casting/diecast-2.jpg": "website-assets/6-Services-Die-Casting/02-diecast-cavity-insert-core.jpg",
    "images/services/die-casting/diecast-3.jpg": "website-assets/6-Services-Die-Casting/03-diecast-high-pressure-die.jpg",

    # ── Jigs & Fixtures ───────────────────────────────────────────────────────
    "images/services/jigs-fixtures/jig-1.jpg": "website-assets/7-Services-Jigs-Fixtures/01-jig-machining-clamping-fixture.jpg",
    "images/services/jigs-fixtures/jig-2.jpg": "website-assets/7-Services-Jigs-Fixtures/02-jig-inspection-checking-gauge.jpg",
    "images/services/jigs-fixtures/jig-3.jpg": "website-assets/7-Services-Jigs-Fixtures/03-jig-robotic-welding-fixture.jpg",

    # ── SPM Automation ────────────────────────────────────────────────────────
    "images/services/spm-automation/spm-1.jpg": "website-assets/8-Services-SPM-Automation/01-spm-rotary-indexing-machine.jpg",
    "images/services/spm-automation/spm-2.jpg": "website-assets/8-Services-SPM-Automation/02-spm-robotic-pick-place-cell.jpg",
    "images/services/spm-automation/spm-3.jpg": "website-assets/8-Services-SPM-Automation/03-spm-automated-testing-bench.jpg",
}

# Also handle favicon href links like <link rel="icon" href="logo-omni.jpg">
HREF_REMAP = {
    "logo-omni.jpg": "website-assets/9-Branding-Logos/03-logo-favicon.jpg",
    "logo-omni.png": "website-assets/9-Branding-Logos/01-logo-header-horizontal.png",
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. Rewrite HTML files
# ─────────────────────────────────────────────────────────────────────────────
def strip_qs(src):
    """Remove ?v=N query string from src."""
    return src.split("?")[0]

def rewrite_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Replace <img src="OLD" or <img src='OLD'
    def replace_img_src(m):
        quote = m.group(1)
        src   = m.group(2)
        bare  = strip_qs(src)
        if bare in REMAP:
            return f'src={quote}{REMAP[bare]}?v=4{quote}'
        return m.group(0)

    content = re.sub(r'src=(["\'])([^"\']+)\1', replace_img_src, content)

    # Replace <link rel="icon" href="OLD">
    def replace_href(m):
        quote = m.group(1)
        href  = m.group(2)
        bare  = strip_qs(href)
        if bare in HREF_REMAP:
            return f'href={quote}{HREF_REMAP[bare]}{quote}'
        return m.group(0)

    content = re.sub(r'href=(["\'])([^"\'#?]+)\1', replace_href, content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  UPDATED: {os.path.basename(filepath)}")
    else:
        print(f"  no changes: {os.path.basename(filepath)}")

html_files = glob.glob(os.path.join(BASE, "*.html"))
print(f"\n=== Rewriting {len(html_files)} HTML files ===")
for html in html_files:
    rewrite_html(html)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Delete old duplicate image files from root / images/ subfolders
# ─────────────────────────────────────────────────────────────────────────────
TO_DELETE_ROOT = [
    "logo-omni.png", "logo-omni.jpg", "logo-omni-stacked.png",
    "about-facility.jpg", "hero-poster.jpg",
    "step-tool-design.png", "step-cad-cam.png", "step-precision-mfg.png",
    "service-product-design.jpg", "service-reverse-engineering.jpg",
    "service-2d-3d.jpg", "service-cnc-vmc.jpg", "service-tool-die.jpg",
    # PNGs that were converted to JPG
    "service-reverse-engineering.png", "service-2d-3d.png",
    "cap-injection-molds.jpg", "cap-press-tools.jpg", "cap-die-casting.jpg",
    "cap-jigs-fixtures.jpg", "cap-spm-automation.jpg", "cap-sand-casting.jpg",
    "industry-automotive.jpg", "industry-electrical.jpg", "industry-aerospace.jpg",
    "industry-medical.jpg", "industry-consumer.jpg", "industry-proto.jpg",
    # raw/intermediate files
    "industry-aerospace-raw.jpg", "industry-electrical-raw.jpg",
    "crop_left_bot.jpg", "crop_left_top.jpg", "crop_makino_okuma.jpg",
]

TO_DELETE_IMAGES = [
    "images/products/labware/reagent-bottles.jpg",
    "images/products/labware/wash-bottles.jpg",
    "images/products/labware/measuring-beakers.jpg",
    "images/products/labware/centrifuge-tubes.jpg",
    "images/products/labware/test-tube-racks.jpg",
    "images/products/labware/pipette-stands.jpg",
    "images/products/labware/aspirator-carboys.jpg",
    "images/products/labware/slide-boxes.jpg",
    "images/services/injection-molds/mold-1.jpg",
    "images/services/injection-molds/mold-2.jpg",
    "images/services/injection-molds/mold-3.jpg",
    "images/services/injection-molds/mold-4.jpg",
    "images/services/injection-molds/mold-5.jpg",
    "images/services/injection-molds/mold-6.jpg",
    "images/services/injection-molds/mold-7.jpg",
    "images/services/injection-molds/mold-8.jpg",
    "images/services/press-tools/press-1.jpg",
    "images/services/press-tools/press-2.jpg",
    "images/services/press-tools/press-3.jpg",
    "images/services/press-tools/press-4.jpg",
    "images/services/press-tools/press-5.jpg",
    "images/services/press-tools/press-6.jpg",
    "images/services/die-casting/diecast-1.jpg",
    "images/services/die-casting/diecast-2.jpg",
    "images/services/die-casting/diecast-3.jpg",
    "images/services/jigs-fixtures/jig-1.jpg",
    "images/services/jigs-fixtures/jig-2.jpg",
    "images/services/jigs-fixtures/jig-3.jpg",
    "images/services/spm-automation/spm-1.jpg",
    "images/services/spm-automation/spm-2.jpg",
    "images/services/spm-automation/spm-3.jpg",
]

print("\n=== Deleting old duplicate files ===")
deleted = 0
skipped = 0
for rel in TO_DELETE_ROOT + TO_DELETE_IMAGES:
    full = os.path.join(BASE, rel)
    if os.path.exists(full):
        os.remove(full)
        print(f"  DELETED: {rel}")
        deleted += 1
    else:
        skipped += 1

print(f"\nDone. {deleted} files deleted, {skipped} already absent.")
print("\n=== All done! Run validate_assets.py to confirm. ===")

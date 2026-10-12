"""
tools/update_footer_address.py
Adds the factory headquarters address to the footer across index.html and all pages/*.html.
"""
import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(BASE_DIR, "pages")

target_files = [os.path.join(BASE_DIR, "index.html")] + glob.glob(os.path.join(PAGES_DIR, "*.html"))

address_html = """                        <div class="footer-contact-row">
                            <svg class="footer-contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>
                            </svg>
                            <span>Phase-1, I.D.A, Jeedimetla, Hyderabad – 500055, Telangana, India.</span>
                        </div>"""

company_marker = '<p class="company-name">OmniMatrix Technologies Pvt Ltd</p>'

for file_path in target_files:
    rel_path = os.path.relpath(file_path, BASE_DIR)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if company_marker in content:
        marker_pos = content.find(company_marker)
        # Check if address already exists in the next 500 characters
        snippet = content[marker_pos:marker_pos + 500]
        if "Phase-1, I.D.A, Jeedimetla" in snippet:
            print(f"Already present in: {rel_path}")
        else:
            updated_content = content[:marker_pos + len(company_marker)] + "\n" + address_html + content[marker_pos + len(company_marker):]
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Added address to: {rel_path}")
    else:
        print(f"Company marker not found in: {rel_path}")

print("\nAddress update completed.")

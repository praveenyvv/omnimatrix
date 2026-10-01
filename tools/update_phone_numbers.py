import glob
import re

files = glob.glob("*.html") + glob.glob("pages/*.html")
print(f"Found {len(files)} files: {files}")

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace index.html contact section phone
    old_contact_section = """<h5>Phone / Support</h5>
                                <p><a href="tel:+919966738638">+91 99667 38638</a></p>"""
    new_contact_section = """<h5>Phone / Support</h5>
                                <p><a href="tel:+919008344055">+91 90083 44055</a></p>
                                <p><a href="tel:+919177017779">+91 91770 17779</a></p>"""
    if old_contact_section in content:
        content = content.replace(old_contact_section, new_contact_section)
        print(f"Updated main contact section in: {filepath}")

    # Replace footer phone rows
    footer_pattern = re.compile(
        r'<div class="footer-contact-row">\s*<svg class="footer-contact-icon"[^>]*>.*?</svg>\s*<a href="tel:\+919966738638">\+91 99667 38638</a>\s*</div>',
        re.DOTALL
    )

    new_footer_phone = """<div class="footer-contact-row">
                            <svg class="footer-contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                            </svg>
                            <div>
                                <a href="tel:+919008344055">+91 90083 44055</a><br>
                                <a href="tel:+919177017779">+91 91770 17779</a>
                            </div>
                        </div>"""

    if footer_pattern.search(content):
        content = footer_pattern.sub(new_footer_phone, content)
        print(f"Updated footer phone numbers in: {filepath}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Phone number updates complete!")

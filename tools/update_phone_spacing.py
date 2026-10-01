import glob
import re

files = glob.glob("*.html") + glob.glob("pages/*.html")
print(f"Updating {len(files)} files...")

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update index.html contact section
    content = content.replace(
        '<p><a href="tel:+919008344055">+91 9008344055</a></p>',
        '<p><a href="tel:+919008344055">+91&nbsp;&nbsp;9008344055</a></p>'
    )
    content = content.replace(
        '<p><a href="tel:+919177017779">+91 9177017779</a></p>',
        '<p><a href="tel:+919177017779">+91&nbsp;&nbsp;9177017779</a></p>'
    )

    # 2. Update footer phone rows
    footer_pattern = re.compile(
        r'<div class="footer-contact-row">\s*<svg class="footer-contact-icon"[^>]*>.*?</svg>\s*(?:<div>|<div class="phone-group">)\s*<a href="tel:\+919008344055">.*?</a>\s*(?:<br>|\s*)\s*<a href="tel:\+919177017779">.*?</a>\s*</div>\s*</div>',
        re.DOTALL
    )

    new_footer_phone = """<div class="footer-contact-row">
                            <svg class="footer-contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                            </svg>
                            <div class="phone-group">
                                <a href="tel:+919008344055">+91&nbsp;&nbsp;9008344055</a>
                                <a href="tel:+919177017779">+91&nbsp;&nbsp;9177017779</a>
                            </div>
                        </div>"""

    if footer_pattern.search(content):
        content = footer_pattern.sub(new_footer_phone, content)
        print(f"Updated footer phone numbers in: {filepath}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Phone number updates complete!")

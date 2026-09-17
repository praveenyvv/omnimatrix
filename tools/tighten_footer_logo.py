import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
logo_path = os.path.join(ROOT, "website-assets", "9-Branding-Logos", "02-logo-footer-stacked.png")

# 1. Load original horizontal logo or crop elements with tight bounds
orig = Image.open(logo_path).convert("RGBA")

# Let's extract the OM Icon (tight crop)
# OM icon is roughly y=16..310, x=150..800
om_icon = orig.crop((165, 16, 785, 315))

# Let's extract OmniMatrix text (tight crop)
# OmniMatrix text is roughly y=330..450, x=40..910
om_text = orig.crop((45, 335, 905, 455))

# Create a clean compact canvas (width: 920, height: 490)
canvas_w = 920
canvas_h = 490
canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 255))

# Paste OM icon (centered at top, compact spacing)
icon_w, icon_h = om_icon.size
canvas.paste(om_icon, ((canvas_w - icon_w) // 2, 10), om_icon)

# Paste OmniMatrix text (just below icon with tight 10px gap)
text_w, text_h = om_text.size
text_y = 10 + icon_h + 8
canvas.paste(om_text, ((canvas_w - text_w) // 2, text_y), om_text)

draw = ImageDraw.Draw(canvas)

# Fonts
font_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 34)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)

# Line 1: "TECHNOLOGIES PRIVATE LIMITED" (bold, dark navy, spans wide)
sub1_text = "TECHNOLOGIES PRIVATE LIMITED"
bbox1 = draw.textbbox((0, 0), sub1_text, font=font_bold)
tw1 = bbox1[2] - bbox1[0]
th1 = bbox1[3] - bbox1[1]

sub1_y = text_y + text_h + 14
sub1_x = (canvas_w - tw1) // 2

# Draw cyan accent lines to match OmniMatrix text width
line_color = (2, 132, 199, 255) # vibrant cyan
text_color1 = (15, 23, 42, 255) # deep navy

line_y = sub1_y + th1 // 2 + 2
line_len = 80
gap = 16

draw.line([(sub1_x - gap - line_len, line_y), (sub1_x - gap, line_y)], fill=line_color, width=4)
draw.line([(sub1_x + tw1 + gap, line_y), (sub1_x + tw1 + gap + line_len, line_y)], fill=line_color, width=4)
draw.text((sub1_x, sub1_y), sub1_text, fill=text_color1, font=font_bold)

# Line 2: "INNOVATE | INTEGRATE | TRANSFORM" (bold cyan, crisp)
sub2_text = "INNOVATE   |   INTEGRATE   |   TRANSFORM"
bbox2 = draw.textbbox((0, 0), sub2_text, font=font_sub)
tw2 = bbox2[2] - bbox2[0]
sub2_x = (canvas_w - tw2) // 2
sub2_y = sub1_y + th1 + 12

text_color2 = (2, 132, 199, 255)
draw.text((sub2_x, sub2_y), sub2_text, fill=text_color2, font=font_sub)

# Final tight crop - trim ALL dead whitespace margins around outer pixels
bbox = canvas.getbbox()
# Give minimal 8px padding
tight_box = (
    max(0, bbox[0] - 6),
    max(0, bbox[1] - 6),
    min(canvas_w, bbox[2] + 6),
    min(canvas_h, bbox[3] + 8)
)
final = canvas.crop(tight_box)
final.save(logo_path, "PNG")

print(f"Tight, wide, ultra-legible logo saved: {final.size} (Ratio: {final.size[0]/final.size[1]:.2f})")

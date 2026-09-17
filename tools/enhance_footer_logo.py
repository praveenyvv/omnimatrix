import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
logo_path = os.path.join(ROOT, "website-assets", "9-Branding-Logos", "02-logo-footer-stacked.png")

# Open original
orig = Image.open(logo_path).convert("RGBA")
orig_w, orig_h = orig.size

# Crop the upper icon + OmniMatrix brand (y = 0 to 455)
top_part = orig.crop((0, 0, orig_w, 455))

# Create a new canvas with plenty of height for large, bold, ultra-readable subtext
new_w = orig_w
new_h = 680
canvas = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 255))

# Paste top brand
canvas.paste(top_part, (0, 0), top_part)

draw = ImageDraw.Draw(canvas)

# Load Windows TrueType Fonts
font_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)

# Line 1: "TECHNOLOGIES PRIVATE LIMITED" with side accent rules
text1 = "TECHNOLOGIES PRIVATE LIMITED"
# Calculate text bbox
bbox1 = draw.textbbox((0, 0), text1, font=font_bold)
tw1 = bbox1[2] - bbox1[0]
th1 = bbox1[3] - bbox1[1]

x1 = (new_w - tw1) // 2
y1 = 490

# Draw left and right accent lines for line 1
line_color = (2, 132, 199, 255) # Cyan blue
text_color1 = (30, 41, 59, 255) # Dark slate navy

line_y = y1 + th1 // 2 + 2
line_len = 110
gap = 20

draw.line([(x1 - gap - line_len, line_y), (x1 - gap, line_y)], fill=line_color, width=4)
draw.line([(x1 + tw1 + gap, line_y), (x1 + tw1 + gap + line_len, line_y)], fill=line_color, width=4)

draw.text((x1, y1), text1, fill=text_color1, font=font_bold)

# Line 2: "INNOVATE  |  INTEGRATE  |  TRANSFORM"
text2 = "INNOVATE   |   INTEGRATE   |   TRANSFORM"
bbox2 = draw.textbbox((0, 0), text2, font=font_sub)
tw2 = bbox2[2] - bbox2[0]
x2 = (new_w - tw2) // 2
y2 = 565

text_color2 = (2, 132, 199, 255) # Primary vibrant blue
draw.text((x2, y2), text2, fill=text_color2, font=font_sub)

# Crop canvas to trim any excess top/bottom whitespace
bbox = canvas.getbbox()
# Add a small 20px padding margin around bbox
padded_box = (
    max(0, bbox[0] - 15),
    max(0, bbox[1] - 10),
    min(new_w, bbox[2] + 15),
    min(new_h, bbox[3] + 15)
)
final_logo = canvas.crop(padded_box)

final_logo.save(logo_path, "PNG")
print(f"Enhanced footer logo saved successfully! New dimensions: {final_logo.size}")

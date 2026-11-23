#!/usr/bin/env python3
"""Draw public/og-image.png (1200x630), the image shown when the site is shared."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent / "public"
INK, TEAL, SUN, CORAL, GREY, WHITE = "#0b1f24", "#0a7a67", "#ffe066", "#ff7a59", "#46585c", "#ffffff"


def font(name, size, weight):
    f = ImageFont.truetype(str(ROOT / "fonts" / name), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


img = Image.new("RGB", (1200, 630), WHITE)
d = ImageDraw.Draw(img)

# Diamonds echoing the logo
d.polygon([(1090, 60), (1140, 110), (1090, 160), (1040, 110)], fill=SUN)
d.polygon([(1010, 150), (1032, 172), (1010, 194), (988, 172)], fill=CORAL)

label = font("spacegrotesk-latin.woff2", 26, 600)
head = font("spacegrotesk-latin.woff2", 76, 700)
body = font("inter-latin.woff2", 30, 400)
brand = font("spacegrotesk-latin.woff2", 36, 700)

d.polygon([(80, 86), (88, 78), (96, 86), (88, 94)], fill=TEAL)
d.text((108, 70), "INDEPENDENT SOFTWARE TESTING", font=label, fill=TEAL)

# Headline with highlighter on "actually works"
d.text((80, 130), "You paid for software.", font=head, fill=INK)
prefix = "Find out if it "
x0 = 80 + d.textlength(prefix, font=head)
x1 = x0 + d.textlength("actually works", font=head)
d.rectangle([x0 - 6, 268, x1 + 6, 300], fill=SUN)
d.text((80, 220), prefix + "actually works.", font=head, fill=INK)

d.text((80, 350), "Acceptance testing · Drop-off audits · Manual QA", font=body, fill=GREY)

# Footer bar
d.rectangle([0, 520, 1200, 630], fill=INK)
d.polygon([(80, 575), (96, 559), (112, 575), (96, 591)], outline=TEAL, width=4)
d.text((128, 552), "Probamo", font=brand, fill=WHITE)
d.text((1120, 560), "probamo.com", font=body, fill="#9fb2b2", anchor="ra")

img.save(ROOT / "og-image.png", optimize=True)
print("wrote public/og-image.png")

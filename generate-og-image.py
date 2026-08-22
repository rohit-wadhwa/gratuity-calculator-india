#!/usr/bin/env python3
"""Generate og-image.png (1200x630) for social sharing.
Run once: python3 generate-og-image.py
Requires: pip install pillow
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys

W, H = 1200, 630
img = Image.new("RGB", (W, H), (244, 240, 232))
d = ImageDraw.Draw(img)

# Decorative wash top-right
for i in range(260):
    d.ellipse([W - 360 + i // 3, -120 + i // 3, W + 120 - i // 3, 260 - i // 3],
              outline=(239, 233, 220), width=1)

def load(paths, size):
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

# macOS system fonts (fallback to DejaVu on other OSes)
serif = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
serif_i = ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"]
sans = ["/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
sans_b = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]

f_eyebrow = load(sans_b, 26)
f_title = load(serif, 104)
f_title_i = load(serif_i, 104)
f_sub = load(sans, 30)
f_chip = load(sans_b, 24)
f_rupee = load(serif, 150)

M = 80
d.text((M, 96), "PAYMENT OF GRATUITY ACT, 1972", font=f_eyebrow, fill=(15, 81, 50))
d.text((M, 150), "Gratuity", font=f_title, fill=(28, 38, 32))
d.text((M, 270), "Calculator", font=f_title_i, fill=(15, 81, 50))
d.text((M, 420), "Estimate your gratuity instantly — free, private,", font=f_sub, fill=(86, 97, 90))
d.text((M, 462), "and mobile-friendly. Enter Basic + DA and service.", font=f_sub, fill=(86, 97, 90))

def chip(x, y, t, fg, bg):
    pad = 22
    w = d.textlength(t, font=f_chip)
    d.rounded_rectangle([x, y, x + w + pad * 2, y + 52], radius=26, fill=bg)
    d.text((x + pad, y + 12), t, font=f_chip, fill=fg)
    return x + w + pad * 2 + 16

nx = chip(M, 532, "15/26 formula", (15, 81, 50), (227, 239, 231))
nx = chip(nx, 532, "5-year rule", (154, 107, 31), (243, 231, 207))
chip(nx, 532, "Tax-free upto Rs 20L", (15, 81, 50), (227, 239, 231))

# Rupee mark in green circle
cx, cy, r = 1000, 250, 150
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(15, 81, 50))
rmark = "\u20B9"
rb = d.textbbox((0, 0), rmark, font=f_rupee)
d.text((cx - (rb[2] - rb[0]) / 2 - 2, cy - (rb[3] - rb[1]) / 2 - rb[1]),
       rmark, font=f_rupee, fill=(251, 249, 244))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og-image.png")
img.save(out, "PNG")
print(f"Wrote {out} ({os.path.getsize(out)} bytes)")

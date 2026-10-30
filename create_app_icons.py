#!/usr/bin/env python3
"""
Generates high-quality Android app icons and splash logo.
Creates both standard and round icons for all mipmap densities:
- mdpi (48x48)
- hdpi (72x72)
- xhdpi (96x96)
- xxhdpi (144x144)
- xxxhdpi (192x192)
- High-res splash logo (512x512)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RES_DIR = Path('/home/b00bs/my_less/English/app_english_cards/app/src/main/res')

DENSITIES = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192,
}

CANVAS_SIZE = 1024

def find_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def create_base_icon(is_round=False):
    # 1024x1024 canvas with RGBA
    img = Image.new('RGBA', (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background shape
    padding = 32
    if is_round:
        draw.ellipse([padding, padding, CANVAS_SIZE - padding, CANVAS_SIZE - padding], fill=(11, 15, 25, 255))
        # Outer neon border
        draw.ellipse([padding, padding, CANVAS_SIZE - padding, CANVAS_SIZE - padding], outline=(56, 189, 248, 220), width=16)
    else:
        # Rounded rectangle
        corner_r = 220
        draw.rounded_rectangle([padding, padding, CANVAS_SIZE - padding, CANVAS_SIZE - padding], radius=corner_r, fill=(11, 15, 25, 255))
        # Outer neon border
        draw.rounded_rectangle([padding, padding, CANVAS_SIZE - padding, CANVAS_SIZE - padding], radius=corner_r, outline=(56, 189, 248, 220), width=16)

    # Subtle inner gradient / glow card
    card_l, card_t, card_r, card_b = 160, 160, 864, 864
    card_r_rad = 140
    # Draw card back
    draw.rounded_rectangle([card_l, card_t, card_r, card_b], radius=card_r_rad, fill=(24, 30, 48, 255), outline=(30, 41, 59, 255), width=8)

    # Sound wave arcs on the right
    # Arc 1
    draw.arc([620, 360, 780, 520], start=-60, end=60, fill=(56, 189, 248, 255), width=24)
    # Arc 2
    draw.arc([600, 300, 840, 580], start=-55, end=55, fill=(34, 197, 94, 255), width=22)

    # Central Bold Typography: "EN"
    font_large = find_font(340)
    # Text shadow
    draw.text((276, 300), "EN", font=font_large, fill=(0, 0, 0, 180))
    # Main text
    draw.text((270, 290), "EN", font=font_large, fill=(255, 255, 255, 255))

    # Badge: "480" inside a cyan pill badge
    badge_w, badge_h = 280, 84
    badge_x = (CANVAS_SIZE - badge_w) // 2
    badge_y = 660
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=42, fill=(30, 41, 59, 255), outline=(56, 189, 248, 255), width=6)

    font_badge = find_font(52)
    draw.text((badge_x + 48, badge_y + 12), "★ 480 ★", font=font_badge, fill=(56, 189, 248, 255))

    return img

def main():
    print("Generating base icons at 1024x1024...")
    icon_square = create_base_icon(is_round=False)
    icon_round = create_base_icon(is_round=True)

    # Save high-res splash logo in drawable
    drawable_dir = RES_DIR / 'drawable'
    drawable_dir.mkdir(parents=True, exist_ok=True)
    splash_logo = icon_square.resize((512, 512), Image.Resampling.LANCZOS)
    splash_logo.save(drawable_dir / 'ic_app_logo.png', 'PNG')
    print("Saved drawable/ic_app_logo.png (512x512)")

    # Save mipmap sizes
    for folder, size in DENSITIES.items():
        out_folder = RES_DIR / folder
        out_folder.mkdir(parents=True, exist_ok=True)

        # Standard icon
        sq = icon_square.resize((size, size), Image.Resampling.LANCZOS)
        sq.save(out_folder / 'ic_launcher.png', 'PNG')

        # Round icon
        rnd = icon_round.resize((size, size), Image.Resampling.LANCZOS)
        rnd.save(out_folder / 'ic_launcher_round.png', 'PNG')
        print(f"Saved {folder}: ic_launcher.png & ic_launcher_round.png ({size}x{size})")

    # Adaptive icons XML in mipmap-anydpi-v26
    anydpi_dir = RES_DIR / 'mipmap-anydpi-v26'
    anydpi_dir.mkdir(parents=True, exist_ok=True)

    # Write ic_launcher.xml
    with open(anydpi_dir / 'ic_launcher.xml', 'w') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/bg_main"/>
    <foreground android:drawable="@drawable/ic_app_logo"/>
</adaptive-icon>
''')

    # Write ic_launcher_round.xml
    with open(anydpi_dir / 'ic_launcher_round.xml', 'w') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/bg_main"/>
    <foreground android:drawable="@drawable/ic_app_logo"/>
</adaptive-icon>
''')
    print("Saved adaptive icon definitions in mipmap-anydpi-v26")

if __name__ == '__main__':
    main()

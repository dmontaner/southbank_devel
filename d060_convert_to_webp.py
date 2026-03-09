#!/usr/bin/env python3
"""
Convert PNG images to WebP format using Pillow.
Requires: pip install Pillow
"""

from pathlib import Path
from PIL import Image

QUALITY = 85  # 0-100, 80-90 is a good balance for artwork

IMAGES_DIR = Path(__file__).parent / "southbank/images"
PNG_DIR = Path(__file__).parent / "images_scaled_png"

PNG_DIR.mkdir(exist_ok=True)


def convert_png_to_webp(png_path: Path, quality: int = QUALITY) -> None:
    webp_path = png_path.with_suffix(".webp")
    with Image.open(png_path) as img:
        img.save(webp_path, "WEBP", quality=quality, method=6)

    original_kb = png_path.stat().st_size / 1024
    converted_kb = webp_path.stat().st_size / 1024
    saving_pct = (1 - converted_kb / original_kb) * 100
    print(
        f"{png_path.name:30s} -> {webp_path.name:30s}  "
        f"{original_kb:6.1f} KB -> {converted_kb:6.1f} KB  "
        f"({saving_pct:.1f}% smaller)"
    )


def main():
    png_files = sorted(IMAGES_DIR.glob("*.png"))
    if not png_files:
        print(f"No PNG files found in {IMAGES_DIR}")
        return

    print(f"Converting {len(png_files)} PNG files in {IMAGES_DIR} ...\n")
    total_original = 0
    total_converted = 0

    for png_path in png_files:
        convert_png_to_webp(png_path)
        webp_path = png_path.with_suffix(".webp")
        total_original += png_path.stat().st_size
        total_converted += webp_path.stat().st_size

    # move pngs to a backup folder
    for png in IMAGES_DIR.glob("*.png"):
        png.rename(PNG_DIR / png.name)

    total_saving = (1 - total_converted / total_original) * 100
    print(
        f"\nTotal: {total_original/1024:.1f} KB -> {total_converted/1024:.1f} KB  "
        f"({total_saving:.1f}% smaller overall)"
    )


if __name__ == "__main__":
    main()

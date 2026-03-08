#!/usr/bin/env python3
"""
Resize PNG images in the images_raw folder for web optimization.
Maintains aspect ratio while reducing size for web serving.
"""

from pathlib import Path
from PIL import Image


def resize_image(input_path, output_path, max_width=1200, max_height=1200, quality=85):
    """
    Resize an image while maintaining aspect ratio.

    Args:
        input_path: Path to the input image
        output_path: Path to save the resized image
        max_width: Maximum width in pixels (default: 1200)
        max_height: Maximum height in pixels (default: 1200)
        quality: JPEG quality for output (default: 85)
    """
    with Image.open(input_path) as img:
        # Get original dimensions
        original_width, original_height = img.size

        # Calculate aspect ratio
        aspect_ratio = original_width / original_height

        # Calculate new dimensions maintaining aspect ratio
        if original_width > max_width or original_height > max_height:
            if aspect_ratio > 1:  # Wider than tall
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:  # Taller than wide
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        else:
            # Image is already smaller than max dimensions
            new_width = original_width
            new_height = original_height

        # Resize using high-quality resampling
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image
        if output_path.suffix.lower() in [".jpg", ".jpeg"]:
            # Convert to RGB if needed (PNG might have alpha channel)
            if resized_img.mode in ("RGBA", "LA", "P"):
                rgb_img = Image.new("RGB", resized_img.size, (255, 255, 255))
                if resized_img.mode == "P":
                    resized_img = resized_img.convert("RGBA")
                rgb_img.paste(
                    resized_img,
                    mask=(
                        resized_img.split()[-1]
                        if resized_img.mode in ("RGBA", "LA")
                        else None
                    ),
                )
                rgb_img.save(output_path, "JPEG", quality=quality, optimize=True)
            else:
                resized_img.save(output_path, "JPEG", quality=quality, optimize=True)
        else:
            # For PNG, preserve transparency
            resized_img.save(output_path, "PNG", optimize=True)

        print(
            f"Resized: {input_path.name} ({original_width}x{original_height}) -> {output_path.name} ({new_width}x{new_height})"
        )


def main():
    # Define paths
    input_dir = Path("images_raw")
    output_dir = Path("southbank/images")

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set max dimensions for web optimization
    max_width = 600
    max_height = 600

    # Process PNG images
    image_extensions = ["*.png"]

    processed_count = 0

    for pattern in image_extensions:
        for image_path in input_dir.glob(pattern):
            # Create output path
            output_path = output_dir / image_path.name

            # Resize the image
            resize_image(image_path, output_path, max_width, max_height)
            processed_count += 1

    print(f"\nTotal images processed: {processed_count}")
    print(f"Output directory: {output_dir.absolute()}")


if __name__ == "__main__":
    main()

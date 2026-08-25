#!/usr/bin/env python3
"""
generate_portrait.py

Turns a normal photo into a "dot matrix" SVG portrait rendered entirely
in a single green tone (like the terminal-green GitHub profile READMEs).

Usage:
    pip install pillow --break-system-packages
    python generate_portrait.py path/to/your_photo.jpg assets/portrait.svg

Tweak the CONFIG block below to control density, dot size, and color.
"""

import sys
from PIL import Image, ImageOps

# ----------------------------- CONFIG ------------------------------
GRID_COLS = 60          # number of dot columns (higher = more detail)
CELL_SIZE = 10           # spacing between dots, in SVG units
DOT_COLOR = "#39D353"    # GitHub-green, matches the rest of the profile theme
BG_COLOR = "none"        # "none" = transparent background
MIN_DOT_RADIUS = 0.4     # radius for the darkest / least-detail areas
MAX_DOT_RADIUS = 4.6     # radius for the brightest / most-detail areas
INVERT = False           # set True if your subject is dark-on-light and
                          # dots come out backwards
CONTRAST_BOOST = 1.15    # >1 sharpens the light/dark separation
# ---------------------------------------------------------------------


def load_and_prepare(path: str) -> Image.Image:
    img = Image.open(path).convert("L")          # grayscale
    img = ImageOps.autocontrast(img, cutoff=1)     # normalize contrast
    if INVERT:
        img = ImageOps.invert(img)
    return img


def resize_to_grid(img: Image.Image, cols: int) -> Image.Image:
    w, h = img.size
    aspect = h / w
    # Dots are roughly square, so keep the row count proportional
    rows = max(1, round(cols * aspect))
    return img.resize((cols, rows), Image.LANCZOS)


def brightness_to_radius(value: int) -> float:
    """0 = black, 255 = white. Faces are usually brightest at the
    features we want to pop (eyes/highlights), so brighter -> bigger dot."""
    norm = (value / 255.0) ** CONTRAST_BOOST
    return MIN_DOT_RADIUS + norm * (MAX_DOT_RADIUS - MIN_DOT_RADIUS)


def build_svg(img: Image.Image, cols: int) -> str:
    w, h = img.size  # w == cols, h == rows after resize
    px = img.load()

    svg_w = w * CELL_SIZE
    svg_h = h * CELL_SIZE

    circles = []
    for y in range(h):
        for x in range(w):
            val = px[x, y]
            r = brightness_to_radius(val)
            if r <= MIN_DOT_RADIUS * 1.05:
                continue  # skip near-invisible dots to keep file size down
            cx = x * CELL_SIZE + CELL_SIZE / 2
            cy = y * CELL_SIZE + CELL_SIZE / 2
            circles.append(
                f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{DOT_COLOR}"/>'
            )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <rect width="100%" height="100%" fill="{BG_COLOR}"/>
  <g>
    {''.join(circles)}
  </g>
</svg>'''
    return svg


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_portrait.py <input_photo> <output_svg>")
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]

    img = load_and_prepare(in_path)
    img = resize_to_grid(img, GRID_COLS)
    svg = build_svg(img, GRID_COLS)

    with open(out_path, "w") as f:
        f.write(svg)

    print(f"Wrote {out_path} ({img.size[0]}x{img.size[1]} dot grid)")


if __name__ == "__main__":
    main()

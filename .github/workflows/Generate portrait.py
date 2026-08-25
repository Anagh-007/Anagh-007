#!/usr/bin/env python3
"""
generate_portrait_transition.py

Builds a looping animated GIF that starts as the green dot-matrix portrait,
crossfades into the real photo, holds, then fades back — for a GitHub
profile README banner.

Usage:
    pip install pillow --break-system-packages
    python generate_portrait_transition.py path/to/photo.jpg assets/portrait.gif

Tweak the CONFIG block to control size, dot density, color, speed.
"""

import sys
from PIL import Image, ImageOps, ImageDraw

# ------------------------------- CONFIG -------------------------------
CANVAS_SIZE = 288        # final square GIF size, in px
GRID_COLS = 46            # dot columns for the matrix version
DOT_COLOR = (57, 211, 83)     # #39D353, GitHub green
BG_COLOR = (13, 17, 23)       # #0D1117, GitHub dark background
MIN_DOT_R_FRAC = 0.10     # min dot radius as a fraction of cell size
MAX_DOT_R_FRAC = 0.62     # max dot radius as a fraction of cell size
CONTRAST_BOOST = 1.15

HOLD_DOTS_FRAMES = 14      # frames to hold on the pure dot-matrix look
FADE_FRAMES = 14           # frames for each crossfade direction
HOLD_PHOTO_FRAMES = 16     # frames to hold on the real photo
FRAME_DURATION_MS = 80     # ms per frame
# ------------------------------------------------------------------------


def crop_to_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def build_photo_frame(path: str) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img = crop_to_square(img)
    img = img.resize((CANVAS_SIZE, CANVAS_SIZE), Image.LANCZOS)
    return img


def build_dot_frame(photo_rgb: Image.Image) -> Image.Image:
    gray = ImageOps.autocontrast(photo_rgb.convert("L"), cutoff=1)
    small = gray.resize((GRID_COLS, GRID_COLS), Image.LANCZOS)
    px = small.load()

    cell = CANVAS_SIZE / GRID_COLS
    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    min_r = MIN_DOT_R_FRAC * cell
    max_r = MAX_DOT_R_FRAC * cell

    for y in range(GRID_COLS):
        for x in range(GRID_COLS):
            val = px[x, y]
            # Darker pixels (hair, features, shadow) get the bigger dots so the
            # subject glows green against a near-black void, matching the
            # reference dot-matrix look — inverse of raw brightness.
            norm = ((255 - val) / 255.0) ** CONTRAST_BOOST
            r = min_r + norm * (max_r - min_r)
            if r < min_r * 1.05:
                continue
            cx = x * cell + cell / 2
            cy = y * cell + cell / 2
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOT_COLOR)

    return canvas


def crossfade(a: Image.Image, b: Image.Image, steps: int, ease=True):
    frames = []
    for i in range(1, steps + 1):
        t = i / steps
        if ease:
            t = t * t * (3 - 2 * t)  # smoothstep easing
        frames.append(Image.blend(a, b, t))
    return frames


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_portrait_transition.py <input_photo> <output_gif>")
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]

    photo = build_photo_frame(in_path)
    dots = build_dot_frame(photo)

    frames = []
    frames += [dots] * HOLD_DOTS_FRAMES
    frames += crossfade(dots, photo, FADE_FRAMES)
    frames += [photo] * HOLD_PHOTO_FRAMES
    frames += crossfade(photo, dots, FADE_FRAMES)

    # Quantize every frame to its own local palette (no dithering) BEFORE
    # saving, and save with optimize=False so Pillow keeps each frame's own
    # local color table instead of collapsing everything into one shared
    # adaptive palette (which is what caused stray speckle pixels in the
    # flat dark background of the dot-matrix frames).
    quantized = [
        f.quantize(colors=64, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
        for f in frames
    ]

    quantized[0].save(
        out_path,
        save_all=True,
        append_images=quantized[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=False,
        disposal=2,
    )
    print(f"Wrote {out_path} ({len(frames)} frames, {CANVAS_SIZE}x{CANVAS_SIZE})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Draw the 24 November 2026 editorial front page as a fixed 1024x1024 PNG.

Every visual decision is seeded, so the file is byte-for-byte reproducible.
No network, no external font download, no clock, no unseeded randomness.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
SEED = 20261124

BOLD_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (244, 239, 228)
INK = (18, 20, 26)
MUTED = (86, 82, 74)
CREAM = (255, 250, 238)
GRAIN_AMPLITUDE = 1
GRAIN_BLOCK = 2

MASTHEAD_END = 155
SCENE_END = 580
BAND_END = 710
STRIP_TOP = 715
STRIP_HEIGHT = 103

ACRONYM = "GLOBAL DAILY BRIEF  •  4 CONTINENTS  •  EVERY STORY FROM THIS DAY"
DATE_TEXT = "24 NOVEMBER 2026"
HERO_LINES = ("SENEGAL: 175 MIGRANTS", "MISSING AT SEA")
HERO_LABEL = "AFRICA  •  YOFF, DAKAR  •  REUTERS"

STRIPS = (
    {
        "top": STRIP_TOP,
        "base": (108, 26, 30),
        "accent": (232, 106, 86),
        "lines": ("GAZA: HAMAS CHIEF", "ABU NAHEL KILLED"),
        "label": "MIDDLE EAST",
    },
    {
        "top": STRIP_TOP + STRIP_HEIGHT,
        "base": (18, 42, 78),
        "accent": (112, 172, 226),
        "lines": ("BANGLADESH: HASINA SETS", "DEC 16 RETURN"),
        "label": "ASIA",
    },
    {
        "top": STRIP_TOP + 2 * STRIP_HEIGHT,
        "base": (24, 72, 54),
        "accent": (232, 188, 84),
        "lines": ("US / FRANCE: SANOFI TO", "BUY INSMED ($41B)"),
        "label": "AMERICAS / EUROPE",
    },
)


def font_at(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a DejaVu face, falling back to the bundled bitmap font."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def width_of(face: ImageFont.FreeTypeFont, text: str) -> int:
    """Measure text width without relying on a bitmap font's anchor support."""
    try:
        box = face.getbbox(text, anchor="lt")
        return max(1, box[2] - box[0])
    except (TypeError, ValueError):
        box = face.getbbox(text)
        return max(1, box[2] - box[0])


def fitted_face(
    lines: tuple[str, ...] | list[str], max_width: int, start: int, floor: int
) -> ImageFont.FreeTypeFont:
    """Shrink from start until every line fits, never below floor."""
    for size in range(start, floor - 1, -1):
        face = font_at(BOLD_FILE, size)
        if all(width_of(face, line) <= max_width for line in lines):
            return face
    return font_at(BOLD_FILE, floor)


def put(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, face, fill) -> None:
    """Draw with a top-left anchor, with a safe fallback for the bitmap font."""
    try:
        draw.text(xy, text, font=face, fill=fill, anchor="lt")
    except (TypeError, ValueError):
        draw.text(xy, text, font=face, fill=fill)


def vertical_gradient(draw: ImageDraw.ImageDraw, top: int, bottom: int, a, b) -> None:
    """Fill a horizontal band with a two-stop linear gradient."""
    span = max(1, bottom - top - 1)
    for y in range(top, bottom):
        t = (y - top) / span
        colour = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
        draw.line([(0, y), (WIDTH, y)], fill=colour)


def draw_masthead(draw: ImageDraw.ImageDraw) -> None:
    """Paper-white header with double rules and the date-dominant lockup."""
    draw.rectangle((0, 0, WIDTH, MASTHEAD_END), fill=PAPER)
    draw.line([(32, 10), (992, 10)], fill=INK, width=3)
    draw.line([(32, 15), (992, 15)], fill=INK, width=1)

    accent = font_at(REGULAR_FILE, 22)
    put(draw, ((WIDTH - width_of(accent, ACRONYM)) // 2, 22), ACRONYM, accent, MUTED)

    date_face = fitted_face((DATE_TEXT,), WIDTH - 64, 96, 80)
    put(draw, ((WIDTH - width_of(date_face, DATE_TEXT)) // 2, 52), DATE_TEXT, date_face, INK)

    draw.line([(32, 128), (992, 128)], fill=INK, width=1)
    draw.line([(32, 133), (992, 133)], fill=INK, width=3)


def draw_sky_and_sea(img: Image.Image, rng: random.Random) -> None:
    """Dusk horizon, sun glow, water gradient, and deterministic wave strokes."""
    draw = ImageDraw.Draw(img)
    horizon = 372
    vertical_gradient(draw, MASTHEAD_END, horizon, (24, 26, 54), (198, 104, 76))
    vertical_gradient(draw, horizon, SCENE_END, (126, 74, 86), (10, 20, 42))
    draw.line([(0, horizon), (WIDTH, horizon)], fill=(236, 176, 126), width=2)

    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for radius in range(150, 18, -6):
        alpha = round(3 + (150 - radius) * 0.32)
        g.ellipse(
            (770 - radius, horizon - radius, 770 + radius, horizon + radius),
            fill=(255, 186, 118, alpha),
        )
    g.ellipse((746, horizon - 26, 794, horizon + 22), fill=(255, 226, 168, 220))
    img.alpha_composite(glow)

    for _ in range(190):
        y = rng.randint(horizon + 4, SCENE_END - 4)
        x = rng.randint(0, WIDTH - 90)
        length = rng.randint(18, 92)
        depth = (y - horizon) / (SCENE_END - horizon)
        shade = round(150 - depth * 96)
        colour = (shade, round(shade * 0.72), round(shade * 0.70))
        draw.line([(x, y), (x + length, y)], fill=colour, width=1)


def draw_route_and_land(draw: ImageDraw.ImageDraw) -> None:
    """Africa shadow at the horizon and a dashed Dakar to Europe route."""
    horizon = 372
    land = (
        (0, horizon),
        (0, 336),
        (44, 340),
        (78, 328),
        (118, 338),
        (158, 352),
        (196, 360),
        (214, horizon),
    )
    draw.polygon(land, fill=(20, 22, 42))

    def bezier(t: float) -> tuple[int, int]:
        u = 1.0 - t
        x = u * u * 62 + 2 * u * t * 520 + t * t * 946
        y = u * u * 366 + 2 * u * t * 158 + t * t * 246
        return round(x), round(y)

    for step in range(64):
        t0 = step / 64
        t1 = min(1.0, t0 + 0.009)
        draw.line([bezier(t0), bezier(t1)], fill=(248, 214, 164), width=2)

    small = font_at(REGULAR_FILE, 16)
    put(draw, (24, 306), "DAKAR", small, (240, 214, 170))
    put(draw, (872, 216), "EUROPE", small, (240, 214, 170))


def draw_number_and_dots(img: Image.Image, rng: random.Random) -> None:
    """Translucent 175 plus exactly 175 seeded dots marking the missing boat."""
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    big = font_at(BOLD_FILE, 300)
    text = "175"
    nx = (WIDTH - width_of(big, text)) // 2 + 90
    put(d, (nx, 232), text, big, (255, 238, 204, 46))

    for index in range(175):
        t = index / 174
        bx = 428 + 470 * t
        by = 500 - 112 * t + 16 * math.sin(t * 9.0)
        x = round(bx + rng.randint(-27, 27))
        y = round(by + rng.randint(-11, 11))
        r = rng.choice((1, 1, 1, 2))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 222, 174, rng.randint(120, 220)))
    img.alpha_composite(layer)


def draw_boat(draw: ImageDraw.ImageDraw) -> None:
    """Wooden hull with passenger silhouettes and a long reflection."""
    hull = ((186, 488), (476, 488), (442, 526), (222, 526))
    draw.polygon(hull, fill=(14, 11, 15))
    draw.line([(196, 496), (466, 496)], fill=(104, 66, 48), width=2)
    for offset in (0, 9, 18):
        draw.line([(222 + offset, 508), (448 - offset, 508)], fill=(58, 38, 32), width=1)
    for i in range(11):
        cx = 226 + i * 22
        top = 462 + (i % 3) * 4
        draw.ellipse((cx - 7, top, cx + 7, top + 14), fill=(10, 9, 12))
        draw.rectangle((cx - 10, top + 12, cx + 10, top + 28), fill=(10, 9, 12))
    draw.line([(300, 462), (520, 548)], fill=(36, 24, 22), width=3)
    for k in range(6):
        y = 532 + k * 8
        draw.line([(236 + k * 3, y), (438 - k * 3, y)], fill=(58, 44, 52), width=1)


def draw_headline_band(draw: ImageDraw.ImageDraw) -> None:
    """Soft shadow above a dark band carrying the hero headline and label."""
    for k in range(8):
        t = k / 7
        colour = tuple(
            round((10, 20, 42)[i] + ((14, 17, 26)[i] - (10, 20, 42)[i]) * t)
            for i in range(3)
        )
        draw.line([(0, 572 + k), (WIDTH, 572 + k)], fill=colour, width=1)
    draw.rectangle((0, SCENE_END, WIDTH, BAND_END), fill=(14, 17, 26))

    face = fitted_face(HERO_LINES, WIDTH - 64, 56, 48)
    put(draw, (32, 586), HERO_LINES[0], face, CREAM)
    put(draw, (32, 632), HERO_LINES[1], face, CREAM)

    label = font_at(REGULAR_FILE, 20)
    put(draw, (32, 684), HERO_LABEL, label, (226, 198, 156))


def draw_strips(draw: ImageDraw.ImageDraw) -> None:
    """Three continental colour-coded strips with large two-line headlines."""
    for strip in STRIPS:
        top = strip["top"]
        bottom = top + STRIP_HEIGHT
        draw.rectangle((0, top, WIDTH, bottom), fill=strip["base"])
        draw.rectangle((0, top, 14, bottom), fill=strip["accent"])
        draw.line([(16, top), (16, bottom)], fill=(255, 255, 255), width=1)

        face = fitted_face(tuple(strip["lines"]), WIDTH - 64, 56, 44)
        put(draw, (30, top + 6), strip["lines"][0], face, CREAM)
        put(draw, (30, top + 54), strip["lines"][1], face, CREAM)

        label = font_at(BOLD_FILE, 20)
        put(draw, (WIDTH - 24 - width_of(label, strip["label"]), top + 62), strip["label"], label, strip["accent"])

        if top > STRIP_TOP:
            draw.line([(0, top), (WIDTH, top)], fill=(250, 244, 230), width=2)


def add_grain(img: Image.Image, amplitude: int) -> None:
    """Seeded block grain over paper, hero and strips; blocks keep the PNG small."""
    rng = random.Random(SEED)
    block = GRAIN_BLOCK
    gw = (WIDTH + block - 1) // block
    gh = (HEIGHT + block - 1) // block
    noise = rng.randbytes(gw * gh * 3)
    pixels = img.load()
    span = 2 * amplitude + 1
    index = 0
    for by in range(0, HEIGHT, block):
        for bx in range(0, WIDTH, block):
            dr = noise[index] % span - amplitude
            dg = noise[index + 1] % span - amplitude
            db = noise[index + 2] % span - amplitude
            index += 3
            for yy in range(by, min(by + block, HEIGHT)):
                for xx in range(bx, min(bx + block, WIDTH)):
                    r, g, b = pixels[xx, yy]
                    pixels[xx, yy] = (
                        max(0, min(255, r + dr)),
                        max(0, min(255, g + dg)),
                        max(0, min(255, b + db)),
                    )


def build() -> Image.Image:
    """Compose the full page from top to bottom, then add print grain."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), PAPER + (255,))
    draw = ImageDraw.Draw(img)
    rng = random.Random(SEED)

    draw_masthead(draw)
    draw_sky_and_sea(img, rng)
    draw_route_and_land(draw)
    draw_number_and_dots(img, rng)
    draw_boat(draw)
    draw_headline_band(draw)
    draw_strips(draw)

    rgb = img.convert("RGB")
    add_grain(rgb, GRAIN_AMPLITUDE)
    return rgb


def main() -> None:
    """Save the deterministic artwork next to this script."""
    target = Path(__file__).resolve().parent / "entry.png"
    build().save(target, format="PNG", optimize=True)


if __name__ == "__main__":
    main()

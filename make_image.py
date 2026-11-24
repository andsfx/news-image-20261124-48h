#!/usr/bin/env python3
"""Build the deterministic 1024x1024 world-news infographic for 24 Nov 2026."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
BG = (9, 14, 28)
PANEL = (19, 28, 51)
BORDER = (48, 68, 108)
WHITE = (242, 247, 255)
CYAN = (86, 224, 236)
MUTED = (150, 172, 210)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size: int, bold: bool = True):
    path = FONT_BOLD if bold else FONT_REGULAR
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def wrap(draw, text, fnt, max_width):
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_icon(draw, cx, cy, kind, color):
    if kind == "tariff":
        draw.rectangle([cx - 20, cy - 4, cx + 20, cy + 18], outline=color, width=4)
        for dx in (-10, 0, 10):
            draw.line([(cx + dx, cy), (cx + dx, cy + 17)], fill=color, width=3)
        draw.polygon([(cx - 14, cy - 10), (cx, cy - 28), (cx + 14, cy - 10)], fill=color)
    elif kind == "strike":
        draw.rectangle([cx - 22, cy - 2, cx + 4, cy + 22], outline=color, width=4)
        draw.line([(cx - 22, cy + 8), (cx + 4, cy + 8)], fill=color, width=3)
        draw.polygon(
            [(cx + 14, cy - 30), (cx + 20, cy - 14), (cx + 36, cy - 12),
             (cx + 22, cy), (cx + 26, cy + 16), (cx + 12, cy + 8),
             (cx - 2, cy + 16), (cx + 2, cy - 2), (cx - 10, cy - 12),
             (cx + 6, cy - 14)],
            fill=color,
        )
    elif kind == "target":
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=color, width=4)
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=color, width=4)
        draw.line([(cx - 32, cy), (cx - 18, cy)], fill=color, width=4)
        draw.line([(cx + 18, cy), (cx + 32, cy)], fill=color, width=4)
        draw.line([(cx, cy - 32), (cx, cy - 18)], fill=color, width=4)
        draw.line([(cx, cy + 18), (cx, cy + 32)], fill=color, width=4)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)
    elif kind == "boat":
        draw.polygon([(cx - 28, cy + 2), (cx + 28, cy + 2),
                      (cx + 18, cy + 22), (cx - 18, cy + 22)], outline=color, width=4)
        draw.line([(cx, cy - 28), (cx, cy + 2)], fill=color, width=4)
        draw.polygon([(cx + 2, cy - 26), (cx + 24, cy - 6), (cx + 2, cy - 6)], fill=color)
        for off in (-8, 8):
            draw.arc([cx - 30, cy + 22 + off, cx + 30, cy + 38 + off],
                     200, 340, fill=color, width=3)
    elif kind == "blast":
        pts = []
        for i in range(16):
            angle = i * 3.141592653589793 / 8
            radius = 29 if i % 2 == 0 else 13
            pts.append((cx + int(radius * __import__("math").cos(angle)),
                        cy + int(radius * __import__("math").sin(angle))))
        draw.polygon(pts, fill=color)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=BG)
    elif kind == "return":
        draw.rectangle([cx - 20, cy - 2, cx + 4, cy + 20], outline=color, width=4)
        draw.line([(cx - 24, cy - 2), (cx - 8, cy - 18)], fill=color, width=4)
        draw.line([(cx - 8, cy - 18), (cx + 8, cy - 2)], fill=color, width=4)
        draw.line([(cx + 28, cy + 6), (cx + 10, cy + 6)], fill=color, width=4)
        draw.polygon([(cx + 18, cy - 2), (cx + 8, cy + 6), (cx + 18, cy + 14)], fill=color)
    elif kind == "deal":
        draw.ellipse([cx - 28, cy - 20, cx + 6, cy + 16], outline=color, width=4)
        draw.ellipse([cx - 6, cy - 20, cx + 28, cy + 16], outline=color, width=4)
        draw.rectangle([cx - 12, cy - 3, cx + 12, cy + 21], fill=color)
        draw.line([(cx - 6, cy + 9), (cx + 6, cy + 9)], fill=BG, width=3)


PANELS = [
    ("BANGLADESH", "HASINA PLANS RETURN FROM EXILE", (255, 183, 77), "return"),
    ("UKRAINE", "ZAPORIZHZHIA: 2 DEAD, 40 HURT", (255, 99, 112), "strike"),
    ("MIDDLE EAST", "HAMAS SECURITY CHIEF KILLED", (255, 138, 92), "target"),
    ("SENEGAL", "175 MIGRANTS LOST OFF SENEGAL", (91, 200, 255), "boat"),
    ("VIETNAM", "HANOI BLAST: 6 DEAD, 10 HURT", (255, 170, 64), "blast"),
    ("BUSINESS", "SANOFI BUYS INSMED: $41B", (110, 231, 165), "deal"),
]


def main():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, SIZE, 14], fill=CYAN)
    title = font(84)
    d.text((SIZE // 2, 42), "24 NOVEMBER 2026", font=title,
           fill=WHITE, anchor="ma")
    sub = font(30, bold=False)
    sub_text = "W O R L D   N E W S   I N   O N E   I M A G E"
    d.text((SIZE // 2, 158), sub_text, font=sub, fill=CYAN, anchor="ma")
    d.line([(28, 202), (SIZE - 28, 202)], fill=BORDER, width=3)

    margin, gap = 26, 16
    panel_w = (SIZE - 2 * margin - gap) // 2
    panel_h, gap_y, top = 250, 14, 218
    label_font = font(34)
    region_font = font(28)
    index_font = font(26)

    for i, (region, label, accent, icon) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (panel_w + gap)
        y = top + row * (panel_h + gap_y)

        d.rounded_rectangle([x, y, x + panel_w, y + panel_h], radius=18,
                            fill=PANEL, outline=BORDER, width=3)
        d.rounded_rectangle([x + 5, y + 20, x + 11, y + panel_h - 20],
                            radius=3, fill=accent)

        cx, cy, r = x + 66, y + 66, 36
        dark = tuple(max(0, int(c * 0.20)) for c in accent)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=dark, outline=accent, width=3)
        draw_icon(d, cx, cy, icon, accent)

        d.text((x + panel_w - 24, y + 30), region, font=region_font,
               fill=accent, anchor="ra")

        lines = wrap(d, label, label_font, panel_w - 60)
        assert len(lines) <= 2, f"label needs more than two lines: {label}"
        ly = y + 120
        for line in lines:
            d.text((x + 28, ly), line, font=label_font, fill=WHITE, anchor="la")
            ly += 44

        d.line([(x + 28, y + panel_h - 22), (x + panel_w - 28, y + panel_h - 22)],
               fill=BORDER, width=2)
        d.text((x + panel_w - 24, y + panel_h - 40),
               f"{i + 1:02d} / 06", font=index_font, fill=MUTED, anchor="ra")

    path = Path(__file__).resolve().parent / "entry.png"
    img.save(path, format="PNG", optimize=False, compress_level=9)
    print(f"wrote {path.name}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render 'The Daily Meridian' — colour vintage newspaper front page.

Summarises the world news of Thursday, 19 November 2026 in six verified
stories. Every letter is typeset with PIL and every picture is drawn in
code with flat newsprint colours. Output is fully deterministic: no
randomness, no timestamps, no network access.

Run:  python3 render_image.py        -> writes entry.png next to this file
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
LEFT = MARGIN
RIGHT = W - MARGIN
CW = RIGHT - LEFT  # 952

# ---- palette: warm newsprint paper, deep-red masthead, flat inks ----
PAPER = (247, 241, 227)
INK = (26, 24, 22)
RED = (143, 29, 29)
RED_DARK = (110, 18, 18)
RED_LIGHT = (178, 58, 48)
GOLD = (201, 158, 60)
BLUE = (58, 74, 90)
BLUE_PALE = (207, 224, 234)
BLUE_SEA = (127, 168, 201)
GREEN = (46, 125, 72)
GREY = (120, 116, 108)
RULE = (60, 52, 44)

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
SERIF = str(FONT_DIR / "LiberationSerif-Regular.ttf")
SERIF_BOLD = str(FONT_DIR / "LiberationSerif-Bold.ttf")
SERIF_ITALIC = str(FONT_DIR / "LiberationSerif-Italic.ttf")
SANS = str(FONT_DIR / "LiberationSans-Regular.ttf")
SANS_BOLD = str(FONT_DIR / "LiberationSans-Bold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(font, lines, leading):
    """Total height of `lines` lines at `leading` spacing."""
    if not lines:
        return 0
    asc, desc = font.getmetrics()
    return (len(lines) - 1) * leading + asc + desc


def draw_centred(draw, cx, y, text, font, fill, leading=None):
    """Draw possibly multi-line text centred on cx, top at y. Returns bottom."""
    lines = text.split("\n")
    lead = leading or int(font.size * 1.18)
    for i, line in enumerate(lines):
        draw.text((cx, y + i * lead), line, font=font, fill=fill, anchor="ma")
    return y + text_h(font, lines, lead)


def draw_left(draw, x, y, text, font, fill, leading=None):
    lines = text.split("\n")
    lead = leading or int(font.size * 1.18)
    for i, line in enumerate(lines):
        draw.text((x, y + i * lead), line, font=font, fill=fill, anchor="la")
    return y + text_h(font, lines, lead)


def rule(draw, y, weight=2, x0=LEFT, x1=RIGHT):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=weight)


# ----------------------------------------------------------------------
# The six verified stories of Thursday, 19 November 2026.
# ----------------------------------------------------------------------
LEAD_HEADLINE = "XI, TRUMP AND PUTIN\nMEET IN SHENZHEN"
LEAD_KICKER = "APEC SUMMIT  •  SHENZHEN, CHINA"
LEAD_STAND = (
    "First three-way summit of the nuclear powers opens at APEC — "
    "Xi calls it groundbreaking, Trump calls it already a win. No deal expected."
)

STORIES = [
    dict(
        kicker="UKRAINE  •  CRIMEA",
        headline="UKRAINE HITS CRIMEAN BRIDGE AGAIN",
        sub="Third strike in a week halts rail traffic hours before the Shenzhen summit.",
        art="bridge",
    ),
    dict(
        kicker="MIDDLE EAST  •  RIYADH",
        headline="MISSILE MENACES RIYADH",
        sub="Saudi-led coalition intercepts a missile aimed at the capital; debris and damage reported.",
        art="missile",
    ),
    dict(
        kicker="MARKETS  •  IPO",
        headline="ANTHROPIC DEBUTS AT $1.5 TRILLION",
        sub="Record $81.3bn IPO priced at $83; ANT begins trading on Nasdaq on Thursday.",
        art="ipo",
    ),
    dict(
        kicker="ASYLUM  •  MALAYSIA",
        headline="UNHCR HALTS MALAYSIA REGISTRATION",
        sub="Refugee agency stops registration and documentation as Malaysia builds its own asylum system.",
        art="unhcr",
    ),
    dict(
        kicker="GAMING  •  RELEASE",
        headline="GTA VI ARRIVES AFTER 13 YEARS",
        sub="Released at midnight worldwide, ending the 13-year wait.",
        art="gta",
    ),
]


# ----------------------------------------------------------------------
# Flat illustrations, drawn in code.
# ----------------------------------------------------------------------
def art_lead(draw, x0, y0, x1, y1):
    """Shenzhen skyline at dusk with the three leaders' flags."""
    import math

    draw.rectangle([x0, y0, x1, y1], fill=BLUE_PALE)
    # low sun
    cx, cy = x0 + (x1 - x0) * 0.72, y0 + 34
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=GOLD)
    # skyline, back row then front row
    base = y1 - 26
    back = [(0, 96), (52, 128), (118, 84), (180, 118), (238, 92), (296, 122)]
    for bx, bh in back:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + 46, base], fill=(96, 112, 128))
    front = [(28, 70), (96, 96), (158, 62), (214, 88), (272, 66)]
    for bx, bh in front:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + 40, base], fill=BLUE)
        # lit windows
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in (x0 + bx + 8, x0 + bx + 22):
                draw.rectangle([wx, wy, wx + 6, wy + 6], fill=GOLD)
    # ground / red carpet
    draw.rectangle([x0, base, x1, y1], fill=(58, 52, 46))
    draw.rectangle([x0, base, x1, base + 8], fill=RED)
    # three flag poles with the three flags
    poles = [
        (x0 + 66, "china"),
        (x0 + 186, "usa"),
        (x0 + 306, "russia"),
    ]
    for px, kind in poles:
        draw.line([(px, base - 8), (px, y0 + 18)], fill=INK, width=3)
        fx0, fy0, fx1, fy1 = px + 2, y0 + 18, px + 46, y0 + 44
        if kind == "china":
            draw.rectangle([fx0, fy0, fx1, fy1], fill=(222, 41, 16))
            draw.ellipse([fx0 + 5, fy0 + 5, fx0 + 11, fy0 + 11], fill=GOLD)
            for sx, sy in ((fx0 + 16, fy0 + 4), (fx0 + 20, fy0 + 9),
                           (fx0 + 16, fy0 + 14), (fx0 + 11, fy0 + 16)):
                draw.ellipse([sx, sy, sx + 3, sy + 3], fill=GOLD)
        elif kind == "usa":
            for i in range(7):
                col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
                draw.rectangle([fx0, fy0 + i * 4, fx1, fy0 + i * 4 + 4], fill=col)
            draw.rectangle([fx0, fy0, fx0 + 18, fy0 + 14], fill=(60, 59, 110))
        else:  # russia: white / blue / red bands
            draw.rectangle([fx0, fy0, fx1, fy0 + 9], fill=(255, 255, 255))
            draw.rectangle([fx0, fy0 + 9, fx1, fy0 + 17], fill=(0, 57, 166))
            draw.rectangle([fx0, fy0 + 17, fx1, fy1], fill=(213, 0, 50))


def art_bridge(draw, x0, y0, x1, y1):
    """The Crimean Bridge over the strait, blast above the deck."""
    import math

    draw.rectangle([x0, y0, x1, y1], fill=(226, 233, 236))
    mid = y0 + (y1 - y0) * 0.62
    draw.rectangle([x0, mid, x1, y1], fill=BLUE_SEA)
    for i in range(5):  # wave ticks
        wx = x0 + 14 + i * 58
        draw.arc([wx, mid + 12, wx + 34, mid + 26], 200, 340, fill=(255, 255, 255), width=2)
    deck = mid - 12
    draw.rectangle([x0, deck, x1, deck + 8], fill=(74, 70, 66))
    for tx in (x0 + 58, x0 + 198):
        draw.rectangle([tx, deck - 58, tx + 10, deck], fill=(74, 70, 66))
        draw.polygon([(tx + 5, deck - 72), (tx - 2, deck - 58), (tx + 12, deck - 58)],
                     fill=(74, 70, 66))
    # suspension cables
    for tx in (x0 + 63, x0 + 203):
        draw.line([(tx, deck - 66), (tx - 62, deck)], fill=INK, width=1)
        draw.line([(tx, deck - 66), (tx + 62, deck)], fill=INK, width=1)
    # blast burst above the deck, centre
    bx, by = x0 + (x1 - x0) // 2, deck - 34
    for r, col in ((30, (232, 126, 32)), (20, (244, 180, 60)), (11, (255, 226, 120))):
        pts = []
        for k in range(12):
            ang = k * math.pi / 6
            rr = r if k % 2 == 0 else r * 0.55
            pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
        draw.polygon(pts, fill=col)
    # smoke puffs
    for sx, sy, sr in ((bx - 44, by - 6, 10), (bx + 42, by - 10, 12), (bx + 52, by + 8, 8)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 146, 138))


def art_missile(draw, x0, y0, x1, y1):
    """Night sky over Riyadh: interceptor burst, missile streak, skyline."""
    import math

    draw.rectangle([x0, y0, x1, y1], fill=(24, 32, 54))
    stars = [(18, 12), (52, 30), (96, 10), (150, 26), (196, 12), (240, 30),
             (282, 14), (36, 48), (120, 44), (228, 50), (268, 44)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(255, 255, 255))
    # interceptor burst
    bx, by = x0 + 150, y0 + 34
    for r, col in ((22, (244, 180, 60)), (13, (255, 226, 120))):
        pts = [(bx + r * math.cos(k * math.pi / 5),
                by + r * math.sin(k * math.pi / 5)) for k in range(10)]
        draw.polygon(pts, fill=col)
    # missile streak diving in from the right
    draw.line([(x1 - 18, y0 + 16), (x0 + 196, y0 + 52)], fill=(255, 255, 255), width=3)
    draw.polygon([(x1 - 18, y0 + 16), (x1 - 34, y0 + 10), (x1 - 32, y0 + 24)],
                 fill=(232, 126, 32))
    # skyline with one tall tower
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(12, 14, 22))
    for bx0, bh in ((8, 22), (48, 16), (96, 26), (196, 18), (240, 24)):
        draw.rectangle([x0 + bx0, y1 - bh, x0 + bx0 + 34, y1], fill=(12, 14, 22))
    tx = x0 + 150
    draw.polygon([(tx - 12, y1 - 34), (tx + 12, y1 - 34), (tx + 5, y1 - 74),
                  (tx - 5, y1 - 74)], fill=(12, 14, 22))
    for wy in range(y1 - 66, y1 - 34, 8):
        draw.rectangle([tx - 2, wy, tx + 2, wy + 3], fill=GOLD)
    # lit windows
    for wx in (x0 + 16, x0 + 56, x0 + 104, x0 + 204, x0 + 248):
        for wy in (y1 - 28, y1 - 18):
            draw.rectangle([wx, wy, wx + 5, wy + 4], fill=GOLD)


def art_ipo(draw, x0, y0, x1, y1):
    """A market board: rising bars, a climbing line, an opening bell."""
    draw.rectangle([x0, y0, x1, y1], fill=(233, 238, 231))
    base = y1 - 14
    bars = [(16, 34), (52, 52), (88, 44), (124, 66), (160, 58), (196, 84), (232, 76)]
    for bx, bh in bars:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + 26, base], fill=(58, 74, 90))
    # climbing line with arrowhead
    pts = [(x0 + 18, base - 30), (x0 + 66, base - 48), (x0 + 112, base - 40),
           (x0 + 160, base - 62), (x0 + 208, base - 56), (x0 + 252, base - 82)]
    draw.line(pts, fill=GREEN, width=4, joint="curve")
    hx, hy = pts[-1]
    draw.polygon([(hx, hy), (hx - 14, hy + 2), (hx - 4, hy + 12)], fill=GREEN)
    # opening bell, top right
    bx, by = x1 - 46, y0 + 26
    draw.pieslice([bx - 16, by - 14, bx + 16, by + 14], 180, 360, fill=GOLD)
    draw.rectangle([bx - 19, by + 10, bx + 19, by + 15], fill=GOLD)
    draw.ellipse([bx - 3, by + 16, bx + 3, by + 21], fill=GOLD)
    draw.text((x0 + 12, y0 + 8), "ANT", font=f(SANS_BOLD, 20), fill=RED, anchor="la")


def art_unhcr(draw, x0, y0, x1, y1):
    """A registration desk: papers, a blue emblem, a red HALTED stamp."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 232, 218))
    # paper sheet, left
    px0, py0, px1, py1 = x0 + 18, y0 + 12, x0 + 150, y1 - 14
    draw.rectangle([px0, py0, px1, py1], fill=(255, 255, 255), outline=INK, width=1)
    for i, ly in enumerate(range(py0 + 14, py1 - 8, 12)):
        ln = 108 if i % 3 else 84
        draw.line([(px0 + 10, ly), (px0 + 10 + ln, ly)], fill=(120, 116, 108), width=2)
    # blue emblem circle, top right
    ex, ey = x0 + 216, y0 + 32
    draw.ellipse([ex - 24, ey - 24, ex + 24, ey + 24], fill=(0, 91, 172))
    draw.ellipse([ex - 17, ey - 17, ex + 17, ey + 17], outline=(255, 255, 255), width=2)
    draw.text((ex, ey), "UN", font=f(SANS_BOLD, 20), fill=(255, 255, 255), anchor="mm")
    # red HALTED stamp, below the emblem, clear of everything else
    sx, sy = x0 + 216, y0 + 74
    draw.ellipse([sx - 48, sy - 14, sx + 48, sy + 14], outline=RED, width=3)
    draw.text((sx, sy), "HALTED", font=f(SANS_BOLD, 16), fill=RED, anchor="mm")


def art_gta(draw, x0, y0, x1, y1):
    """Vice City at night: neon VI, palms, a car cruising the strip."""
    import math

    draw.rectangle([x0, y0, x1, y1], fill=(43, 24, 64))
    # sun, tucked in the top-left corner, clear of the VI
    draw.ellipse([x0 + 14, y0 + 8, x0 + 66, y0 + 44], fill=(255, 110, 150))
    # palms, left and right
    for px, flip in ((x0 + 34, 1), (x1 - 34, -1)):
        draw.line([(px, y1 - 20), (px, y0 + 44)], fill=(20, 12, 30), width=5)
        for ang in (-50, -25, 0, 25, 50):
            a = math.radians(ang)
            ex = px + flip * 26 * math.cos(a)
            ey = y0 + 44 - 12 + 26 * math.sin(a) * 0.4
            draw.line([(px, y0 + 44), (ex, ey)], fill=(20, 12, 30), width=3)
    # neon VI, kept above the street line
    draw.text((x0 + (x1 - x0) // 2, y0 + 26), "VI",
              font=f(SERIF_BOLD, 56), fill=(255, 110, 180), anchor="ma")
    # street and car
    draw.rectangle([x0, y1 - 24, x1, y1], fill=(16, 12, 24))
    draw.line([(x0, y1 - 12), (x1, y1 - 12)], fill=(255, 210, 90), width=2)
    cx0, cy = x0 + 96, y1 - 24
    draw.rectangle([cx0, cy - 14, cx0 + 96, cy], fill=(10, 10, 14))
    draw.polygon([(cx0 + 18, cy - 14), (cx0 + 34, cy - 26), (cx0 + 66, cy - 26),
                  (cx0 + 78, cy - 14)], fill=(10, 10, 14))
    for wx in (cx0 + 14, cx0 + 74):
        draw.ellipse([wx - 8, cy - 9, wx + 8, cy + 9], fill=(30, 30, 34),
                     outline=(200, 200, 200), width=1)


ART = {
    "bridge": art_bridge,
    "missile": art_missile,
    "ipo": art_ipo,
    "unhcr": art_unhcr,
    "gta": art_gta,
}


# ----------------------------------------------------------------------
# Page build.
# ----------------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top double rule ---------------------------------------------
    rule(d, 24, 2)
    rule(d, 29, 1)

    # --- masthead ------------------------------------------------------
    y = 36
    y = draw_centred(d, W // 2, y, "THE DAILY MERIDIAN",
                     f(SERIF_BOLD, 84), RED) + 2
    y = draw_centred(d, W // 2, y, "THE WORLD'S NEWSPAPER  •  EST. 1847",
                     f(SANS_BOLD, 14), INK) + 8

    # --- red dateline band ---------------------------------------------
    d.rectangle([LEFT, y, RIGHT, y + 34], fill=RED)
    d.text((LEFT + 12, y + 17), "No. 19,411", font=f(SANS_BOLD, 13),
           fill=(255, 255, 255), anchor="lm")
    d.text((RIGHT - 12, y + 17), "PRICE: ONE PENNY", font=f(SANS_BOLD, 13),
           fill=(255, 255, 255), anchor="rm")
    d.text((W // 2, y + 17), "THURSDAY, 19 NOVEMBER 2026",
           font=f(SERIF_BOLD, 21), fill=(255, 255, 255), anchor="mm")
    y += 34 + 12

    # --- lead story: headline left, picture right ----------------------
    lead_w = 560
    lead_x1 = LEFT + lead_w
    pic_x0, pic_x1 = lead_x1 + 16, RIGHT
    pic_y0 = y
    y = draw_centred(d, LEFT + lead_w // 2, y, LEAD_KICKER,
                     f(SANS_BOLD, 14), RED) + 6
    y = draw_centred(d, LEFT + lead_w // 2, y, LEAD_HEADLINE,
                     f(SERIF_BOLD, 46), INK, leading=50) + 8
    stand_lines = wrap(d, LEAD_STAND, f(SERIF_ITALIC, 18), lead_w)
    y = draw_centred(d, LEFT + lead_w // 2, y, "\n".join(stand_lines),
                     f(SERIF_ITALIC, 18), INK, leading=23) + 4
    lead_bottom = y
    pic_y1 = pic_y0 + 196
    art_lead(d, pic_x0, pic_y0, pic_x1, pic_y1)
    d.rectangle([pic_x0, pic_y0, pic_x1, pic_y1], outline=INK, width=1)
    d.text((pic_x0 + (pic_x1 - pic_x0) // 2, pic_y1 + 6),
           "The three leaders arrive for the first three-way summit of the nuclear powers.",
           font=f(SERIF_ITALIC, 13), fill=GREY, anchor="ma")
    y = max(lead_bottom, pic_y1 + 26)
    rule(d, y, 2)
    y += 12

    # --- three-column row: stories 1-3 ---------------------------------
    gap = 16
    col_w = (CW - 2 * gap) // 3
    row_y = y
    row_bottom = row_y
    for i, st in enumerate(STORIES[:3]):
        x0 = LEFT + i * (col_w + gap)
        x1 = x0 + col_w
        cy = row_y
        ART[st["art"]](d, x0, cy, x1, cy + 104)
        d.rectangle([x0, cy, x1, cy + 104], outline=INK, width=1)
        cy += 104 + 8
        cy = draw_left(d, x0, cy, st["kicker"], f(SANS_BOLD, 12), RED) + 4
        hl = wrap(d, st["headline"], f(SERIF_BOLD, 24), col_w)
        cy = draw_left(d, x0, cy, "\n".join(hl), f(SERIF_BOLD, 24), INK,
                       leading=27) + 5
        sub = wrap(d, st["sub"], f(SERIF, 15), col_w)
        cy = draw_left(d, x0, cy, "\n".join(sub), f(SERIF, 15), INK,
                       leading=19) + 4
        row_bottom = max(row_bottom, cy)
    y = row_bottom + 6
    rule(d, y, 2)
    y += 12

    # --- two-column row: stories 4-5 -----------------------------------
    col2_w = (CW - gap) // 2
    row_y = y
    row_bottom = row_y
    for i, st in enumerate(STORIES[3:]):
        x0 = LEFT + i * (col2_w + gap)
        x1 = x0 + col2_w
        cy = row_y
        ART[st["art"]](d, x0, cy, x1, cy + 96)
        d.rectangle([x0, cy, x1, cy + 96], outline=INK, width=1)
        cy += 96 + 8
        cy = draw_left(d, x0, cy, st["kicker"], f(SANS_BOLD, 12), RED) + 4
        hl = wrap(d, st["headline"], f(SERIF_BOLD, 26), col2_w)
        cy = draw_left(d, x0, cy, "\n".join(hl), f(SERIF_BOLD, 26), INK,
                       leading=30) + 5
        sub = wrap(d, st["sub"], f(SERIF, 16), col2_w)
        cy = draw_left(d, x0, cy, "\n".join(sub), f(SERIF, 16), INK,
                       leading=20) + 4
        row_bottom = max(row_bottom, cy)
    y = row_bottom + 8

    # --- footer ----------------------------------------------------------
    rule(d, y, 1)
    y += 8
    draw_centred(
        d, W // 2, y,
        "The Daily Meridian  •  All six stories verified from wire reports, Thursday 19 November 2026",
        f(SANS, 13), GREY)
    return img


def main():
    out = Path(__file__).resolve().parent / "entry.png"
    img = build()
    img.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()

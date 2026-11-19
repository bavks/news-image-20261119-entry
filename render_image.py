#!/usr/bin/env python3
"""Render entry.png: a colour newspaper front page for Thursday,
19 November 2026, typeset as "The Daily Meridian".

Every illustration is drawn with PIL shapes in flat newsprint colours
and every word is typeset with real serif fonts -- no generative text
anywhere, so nothing can come out garbled.  Run it and it writes
entry.png next to this file.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024

# --- palette: warm paper, coloured inks -------------------------------
PAPER = (247, 240, 221)
PAPER_SHADE = (238, 228, 199)
INK = (38, 33, 26)
MASTHEAD_RED = (140, 40, 28)
MASTHEAD_DEEP = (108, 28, 20)
CREAM = (250, 243, 224)
GOLD = (198, 150, 46)
NAVY = (31, 55, 92)
TEAL = (24, 102, 108)
RUST = (178, 74, 32)
SKY_DUSK_TOP = (46, 52, 96)
SKY_DUSK_MID = (196, 96, 52)
SEA = (30, 74, 96)
SAND = (214, 178, 106)

DEJAVU = "/usr/share/fonts/truetype/dejavu"
NOTO = "/usr/share/fonts/truetype/noto"


def font(kind, size):
    paths = {
        "display": f"{NOTO}/NotoSerifDisplay-Black.ttf",
        "display_it": f"{NOTO}/NotoSerifDisplay-BoldItalic.ttf",
        "bold": f"{DEJAVU}/DejaVuSerif-Bold.ttf",
        "serif": f"{DEJAVU}/DejaVuSerif.ttf",
        "italic": f"{NOTO}/NotoSerif-Italic.ttf",
    }
    return ImageFont.truetype(paths[kind], size)


def text_w(draw, s, fnt):
    box = draw.textbbox((0, 0), s, font=fnt)
    return box[2] - box[0]


def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, kind, s, max_w, start):
    """Largest size, at or below start, whose text fits max_w."""
    size = start
    while size > 10 and text_w(draw, s, font(kind, size)) > max_w:
        size -= 2
    return font(kind, size)


def centred(draw, cx, y, s, fnt, fill):
    draw.text((cx - text_w(draw, s, fnt) / 2, y), s, font=fnt, fill=fill)
    return y + fnt.size + 6


def block(draw, x, y, s, fnt, fill, max_w, leading=1.18, centre=False):
    for line in wrap(draw, s, fnt, max_w):
        if centre:
            centred(draw, x + max_w / 2, y, line, fnt, fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def grain(img, seed=19, specks=2600):
    """A whisper of newsprint noise over the whole page."""
    rnd = random.Random(seed)
    px = img.load()
    for _ in range(specks):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r, g, b = px[x, y][:3]
        delta = rnd.choice((-14, -9, 9, 14))
        px[x, y] = (max(0, min(255, r + delta)),
                    max(0, min(255, g + delta)),
                    max(0, min(255, b + delta)))
    return img


# --- little drawing helpers --------------------------------------------

def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def burst(draw, cx, cy, r, fill):
    for i in range(8):
        ang = i * math.pi / 4
        draw.line([(cx, cy), (cx + r * math.cos(ang), cy + r * math.sin(ang))],
                  fill=fill, width=3)
    draw.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22], fill=fill)


# --- the six story illustrations ----------------------------------------

def art_flags(draw, box):
    """Lead art: three flags on poles against a pale sky: China, the
    United States, Russia -- the Shenzhen gathering."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    draw.rectangle(box, fill=(206, 226, 238))
    draw.rectangle([x0, y1 - 16, x1, y1], fill=(96, 128, 92))
    fw, fh = 74, 48
    tops = [y0 + 14, y0 + 8, y0 + 14]
    centres = [int(w * 0.22), int(w * 0.50), int(w * 0.78)]
    for i, cx in enumerate(centres):
        fx = x0 + cx - fw // 2
        draw.line([(fx, tops[i]), (fx, y1 - 14)], fill=(70, 60, 50), width=3)
        fy = tops[i]
        if i == 0:  # China: red field, gold stars
            draw.rectangle([fx + 3, fy, fx + 3 + fw, fy + fh], fill=(206, 42, 34))
            star(draw, fx + 20, fy + 15, 9, (250, 208, 60))
            for dx, dy in ((34, 7), (37, 17), (34, 27)):
                star(draw, fx + dx, fy + dy, 4, (250, 208, 60))
        elif i == 1:  # United States: stripes and a blue canton
            for s_i in range(7):
                col = (196, 44, 44) if s_i % 2 == 0 else (246, 244, 238)
                draw.rectangle([fx + 3, fy + s_i * fh // 7, fx + 3 + fw,
                                fy + (s_i + 1) * fh // 7], fill=col)
            draw.rectangle([fx + 3, fy, fx + 3 + fw * 0.44, fy + fh * 0.54], fill=NAVY)
            for r_i in range(3):
                for c_i in range(4):
                    draw.ellipse([fx + 8 + c_i * 8, fy + 4 + r_i * 8,
                                  fx + 11 + c_i * 8, fy + 7 + r_i * 8], fill=(250, 250, 250))
        else:  # Russia: white, blue, red
            for s_i, col in enumerate([(246, 246, 246), (36, 84, 168), (206, 42, 34)]):
                draw.rectangle([fx + 3, fy + s_i * fh // 3, fx + 3 + fw,
                                fy + (s_i + 1) * fh // 3], fill=col)


def art_bridge(draw, box):
    """The Crimean Bridge: a long road deck over a dark strait, one
    arch gaping where the span fell, smoke rising."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    for i in range(h):  # pale dawn sky over the strait
        t = i / h
        top, mid = (214, 226, 232), (238, 214, 178)
        col = tuple(int(top[c] + (mid[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)
    sea_y = y0 + int(h * 0.66)
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i in range(20):  # wave ticks
        rnd = random.Random(i * 11)
        wx = x0 + rnd.randrange(10, x1 - x0 - 60)
        wy = sea_y + 6 + rnd.randrange(0, max(2, y1 - sea_y - 12))
        draw.line([(wx, wy), (wx + 24, wy)], fill=(120, 178, 196), width=2)
    deck_y = y0 + int(h * 0.42)
    # road deck in two pieces, with a gap in the middle
    draw.rectangle([x0 + 6, deck_y, x0 + 118, deck_y + 7], fill=(52, 48, 44))
    draw.rectangle([x0 + 168, deck_y, x1 - 6, deck_y + 7], fill=(52, 48, 44))
    # arch over the left span
    draw.arc([x0 + 16, deck_y - 34, x0 + 108, deck_y + 10], 180, 360, fill=(52, 48, 44), width=4)
    # the fallen arch, tilted into the sea on the right
    draw.line([(x0 + 128, deck_y + 4), (x0 + 158, sea_y + 8)], fill=(52, 48, 44), width=5)
    draw.line([(x0 + 158, sea_y + 8), (x0 + 186, deck_y + 4)], fill=(52, 48, 44), width=5)
    # support pylons
    for px_ in (x0 + 40, x0 + 92, x0 + 210, x0 + 258):
        draw.rectangle([px_, deck_y + 7, px_ + 6, sea_y + 2], fill=(52, 48, 44))
    # smoke and a burst at the gap
    burst(draw, x0 + 143, deck_y - 6, 14, (250, 190, 90))
    for k, (sx, sy, sr) in enumerate([(138, deck_y - 26, 10), (150, deck_y - 40, 13), (142, deck_y - 56, 9)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 116, 110))


def art_missile(draw, box):
    """Night over Riyadh: a missile arc and a burst above a skyline
    of towers."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(18, 24, 54))
    rnd = random.Random(3)
    for _ in range(30):
        sx = x0 + rnd.randrange(4, w - 4)
        sy = y0 + rnd.randrange(4, int(h * 0.55))
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(235, 238, 250))
    # crescent moon
    draw.ellipse([x0 + 10, y0 + 6, x0 + 28, y0 + 24], fill=(246, 240, 214))
    draw.ellipse([x0 + 17, y0 + 3, x0 + 33, y0 + 21], fill=(18, 24, 54))
    # skyline
    base = y1
    towers = [(0.03, 0.42, 0.11), (0.17, 0.30, 0.10), (0.30, 0.48, 0.12),
              (0.45, 0.36, 0.10), (0.58, 0.54, 0.11), (0.72, 0.40, 0.10),
              (0.85, 0.56, 0.11)]
    for fx, fh, fw in towers:
        tx = x0 + int(fx * w)
        tw = int(fw * w)
        th = int(fh * h)
        draw.rectangle([tx, base - th, tx + tw, base], fill=(12, 14, 26))
        for wy in range(base - th + 4, base - 4, 8):
            draw.rectangle([tx + 3, wy, tx + 6, wy + 3], fill=(250, 214, 120))
    # missile arc from the left sky toward the city, staying in-box
    pts = []
    for s_i in range(31):
        t = s_i / 30
        px_ = x0 + int(w * 0.20) + int(w * 0.62) * t
        py_ = y0 + int(h * 0.62) - math.sin(t * math.pi) * int(h * 0.42) + int(h * 0.10) * t
        pts.append((px_, py_))
    draw.line(pts, fill=(250, 214, 120), width=3)
    burst(draw, pts[-1][0], pts[-1][1], 11, (250, 190, 90))


def art_chart(draw, box):
    """Anthropic's debut: a rising share-price chart and the ANT
    ticker on a trading-board panel."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(244, 238, 222))
    # board frame
    draw.rectangle([x0 + 6, y0 + 6, x1 - 6, y1 - 6], outline=INK, width=2)
    # ticker label, top-left
    draw.text((x0 + 12, y0 + 8), "ANT", font=font("bold", 20), fill=INK)
    draw.text((x0 + 62, y0 + 11), "$83", font=font("bold", 16), fill=MASTHEAD_RED)
    # rising bars, scaled to the box
    bars = [0.18, 0.25, 0.22, 0.34, 0.30, 0.44, 0.52, 0.68]
    bw = (w - 40) // len(bars) - 4
    bx = x0 + 16
    base = y1 - 12
    max_bh = int(h * 0.52)
    for i, frac in enumerate(bars):
        bh = int(frac * max_bh)
        col = TEAL if i < len(bars) - 1 else MASTHEAD_RED
        draw.rectangle([bx + i * (bw + 4), base - bh,
                        bx + i * (bw + 4) + bw, base], fill=col)
    # trend line over the bars
    pts = [(bx + i * (bw + 4) + bw // 2, base - int(frac * max_bh) - 3)
           for i, frac in enumerate(bars)]
    draw.line(pts, fill=GOLD, width=3)
    star(draw, pts[-1][0], pts[-1][1] - 4, 6, GOLD)


def art_stamp(draw, box):
    """A registration card stamped PAUSED: the UNHCR halt in
    Malaysia."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(236, 230, 208))
    # the card
    draw.rectangle([x0 + 10, y0 + 8, x1 - 10, y1 - 8], fill=(250, 248, 240), outline=INK, width=2)
    draw.text((x0 + 16, y0 + 12), "REGISTRATION CARD", font=font("bold", 11), fill=INK)
    draw.line([(x0 + 16, y0 + 28), (x1 - 16, y0 + 28)], fill=INK, width=1)
    for ly in (y0 + 38, y0 + 48):
        draw.line([(x0 + 16, ly), (x0 + 78, ly)], fill=(140, 134, 120), width=2)
    # small portrait box
    draw.rectangle([x1 - 44, y0 + 34, x1 - 16, y0 + 62], outline=INK, width=2)
    draw.ellipse([x1 - 38, y0 + 39, x1 - 22, y0 + 51], fill=(120, 140, 160))
    draw.rectangle([x1 - 41, y0 + 53, x1 - 19, y0 + 62], fill=(120, 140, 160))
    # the PAUSED stamp, sized to fit inside the card
    stamp_f = font("bold", 15)
    cx, cy = (x0 + x1) // 2, y1 - 20
    draw.ellipse([cx - 56, cy - 13, cx + 56, cy + 13], outline=MASTHEAD_RED, width=3)
    draw.ellipse([cx - 50, cy - 9, cx + 50, cy + 9], outline=MASTHEAD_RED, width=1)
    draw.text((cx - text_w(draw, "PAUSED", stamp_f) / 2, cy - 9), "PAUSED",
              font=stamp_f, fill=MASTHEAD_RED)


def art_city(draw, box):
    """GTA VI: a neon dusk skyline, palm silhouette and a setting
    sun over Vice City's bay."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    for i in range(h):  # neon dusk gradient
        t = i / h
        top, mid = (64, 32, 96), (238, 110, 84)
        col = tuple(int(top[c] + (mid[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)
    # setting sun
    sx, sy, sr = x0 + int(w * 0.62), y0 + int(h * 0.26), 13
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(250, 214, 120))
    # bay
    sea_y = y0 + int(h * 0.74)
    draw.rectangle([x0, sea_y, x1, y1], fill=(24, 60, 96))
    draw.line([(x0, sea_y), (x1, sea_y)], fill=(250, 214, 120), width=2)
    # skyline, widths and heights proportional to the box
    base = sea_y
    towers = [(0.04, 0.55, 0.15), (0.22, 0.80, 0.14), (0.39, 0.48, 0.15),
              (0.57, 0.88, 0.14), (0.74, 0.64, 0.14)]
    for fx, fh, fw in towers:
        tx = x0 + int(fx * w)
        tw = int(fw * w)
        th = int(fh * (base - y0))
        draw.rectangle([tx, base - th, tx + tw, base], fill=(18, 16, 30))
        for wy in range(base - th + 4, base - 4, 8):
            draw.rectangle([tx + 3, wy, tx + 6, wy + 3], fill=(250, 214, 120))
    # palm silhouette on the left
    px_, py_ = x0 + int(w * 0.12), base
    draw.line([(px_, py_), (px_, py_ - 22)], fill=(14, 12, 22), width=3)
    for ang in (-150, -120, -90, -60, -30):
        rad = math.radians(ang)
        draw.line([(px_, py_ - 22),
                   (px_ + 12 * math.cos(rad), py_ - 22 + 7 * math.sin(rad))],
                  fill=(14, 12, 22), width=2)


# --- page assembly -------------------------------------------------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    MX0, MX1 = 44, 980  # content margins

    # frame
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    draw.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # top strip
    strip_f = font("bold", 20)
    draw.text((MX0, 36), "Vol. CXVII — No. 323", font=strip_f, fill=INK)
    right = "Price: One Day's News"
    draw.text((MX1 - text_w(draw, right, strip_f), 36), right, font=strip_f, fill=INK)
    rule(draw, MX0, MX1, 68, 3)
    rule(draw, MX0, MX1, 74, 1)

    # masthead: deep red band, cream nameplate, auto-fitted to the page
    draw.rectangle([MX0, 82, MX1, 186], fill=MASTHEAD_RED)
    draw.rectangle([MX0, 82, MX1, 90], fill=MASTHEAD_DEEP)
    draw.rectangle([MX0, 178, MX1, 186], fill=MASTHEAD_DEEP)
    name_f = fit_font(draw, "display", "The Daily Meridian", MX1 - MX0 - 56, 96)
    centred(draw, W // 2, 134 - name_f.size // 2, "The Daily Meridian", name_f, CREAM)

    # dateline
    rule(draw, MX0, MX1, 200, 1)
    date_f = font("bold", 40)
    centred(draw, W // 2, 207, "Thursday, 19 November 2026", date_f, MASTHEAD_RED)
    rule(draw, MX0, MX1, 258, 3)
    rule(draw, MX0, MX1, 264, 1)

    # lead story
    lead_f = font("bold", 50)
    y = block(draw, MX0, 274, "XI, TRUMP AND PUTIN MEET IN SHENZHEN",
              lead_f, INK, MX1 - MX0, leading=1.06, centre=True)
    deck_f = font("italic", 22)
    y = block(draw, MX0, y + 2,
              "First-ever three-way talks of the nuclear powers open in "
              "Shenzhen; Xi calls it groundbreaking — but no deal is "
              "expected.",
              deck_f, (74, 62, 48), MX1 - MX0, leading=1.15, centre=True)
    art_flags(draw, (MX0, y + 8, MX1, y + 122))
    y += 142
    rule(draw, MX0, MX1, y, 2)
    y += 12

    # three ruled columns
    col_w = (MX1 - MX0 - 2 * 28) // 3
    head_f, sub_f = font("bold", 23), font("serif", 16)
    columns = [
        ("UKRAINE HITS CRIMEAN BRIDGE AGAIN",
         "Third strike in a week suspends rail traffic across the "
         "19-km bridge, hours before the Shenzhen summit.",
         art_bridge),
        ("HOUTHI MISSILE MENACES RIYADH",
         "The Saudi-led coalition intercepts a missile aimed at the "
         "capital; debris falls and damage is reported.",
         art_missile),
        ("ANTHROPIC DEBUTS AT $1.5 TRILLION",
         "Record $81.3bn IPO priced at $83 a share; ANT starts "
         "trading on the Nasdaq on Thursday.",
         art_chart),
    ]
    col_top = y
    col_end = col_top
    for i, (head, sub, art) in enumerate(columns):
        cx0 = MX0 + i * (col_w + 28)
        art(draw, (cx0, col_top, cx0 + col_w, col_top + 66))
        hy = block(draw, cx0, col_top + 72, head, head_f,
                   NAVY if i != 1 else MASTHEAD_RED, col_w, leading=1.1)
        col_end = max(col_end, block(draw, cx0, hy + 2, sub, sub_f, INK,
                                     col_w, leading=1.15))
        if i < 2:
            draw.line([(cx0 + col_w + 14, col_top), (cx0 + col_w + 14, col_top + 196)],
                      fill=INK, width=1)
    y = col_end + 10
    rule(draw, MX0, MX1, y, 2)
    y += 12

    # two wide stories, art left and text right
    wide = [
        ("UNHCR HALTS MALAYSIA REGISTRATION",
         "The refugee agency stops registering asylum seekers as "
         "Malaysia builds its own system for managing them.",
         art_stamp),
        ("GTA VI ARRIVES AFTER 13 YEARS",
         "Rockstar's blockbuster launches at midnight worldwide, "
         "ending the long wait for a sequel.",
         art_city),
    ]
    half = (MX1 - MX0 - 28) // 2
    wide_end = y
    for i, (head, sub, art) in enumerate(wide):
        wx0 = MX0 + i * (half + 28)
        art(draw, (wx0, y, wx0 + 150, y + 84))
        tx = wx0 + 164
        hy = block(draw, tx, y - 2, head, font("bold", 22),
                   TEAL if i == 0 else NAVY, (wx0 + half) - tx, leading=1.1)
        wide_end = max(wide_end, block(draw, tx, hy + 2, sub, font("serif", 16),
                                       INK, (wx0 + half) - tx, leading=1.15))
        if i == 0:
            draw.line([(wx0 + half + 14, y), (wx0 + half + 14, y + 88)],
                      fill=INK, width=1)
    y = max(wide_end, y + 88) + 8

    # footer
    rule(draw, MX0, MX1, y, 1)
    centred(draw, W // 2, y + 7, "All the news of one day, in one page.",
            font("italic", 20), (74, 62, 48))
    assert y + 34 < H - 24, f"page overflow: content ends at {y}"

    img = grain(img)
    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deterministic generator for the news-image-20261119 poster.

Draws a newspaper front page ("THE WORLD IN ONE PAGE") summing up
Thursday 19 November 2026, at 2x supersampling (2048x2048) and
downsamples to 1024x1024. No network, no timestamps, no randomness:
two runs produce byte-identical poster.png.

All facts come from the competition brief (verified 19 Nov 2026).

Layout coordinates are in 1x units (1024x1024); every value is
multiplied by S=2 when drawing.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "poster.png")

S = 2                      # supersample factor
W, H = 1024, 1024          # 1x layout units
M = 48                     # outer margin (1x)

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (164, 30, 34)
NAVY = (26, 47, 90)
DARK = (18, 24, 38)
GREY = (90, 88, 82)
LIGHT_GREY = (200, 196, 186)
GOLD = (201, 162, 39)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines. max_w in 1x units."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w * S or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=1.28):
    """Draw wrapped text; x, y, max_w in 1x units. Returns end y (1x)."""
    lines = wrap(draw, text, fnt, max_w)
    lh = fnt.size / S * leading
    for ln in lines:
        draw.text((x * S, y * S), ln, font=fnt, fill=fill)
        y += lh
    return y


def draw_tracked(draw, cx, y, text, fnt, fill=INK, tracking=6):
    """Draw centred text with extra letter spacing (1x units)."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = (sum(widths) + tracking * S * (len(text) - 1)) / S
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x * S, y * S), ch, font=fnt, fill=fill)
        x += w / S + tracking
    return total


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rect(d, x0, y0, x1, y1, fill):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill)


def ell(d, x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill,
              outline=outline, width=int(width * S))


# ---------------------------------------------------------------- flags
def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        rect(d, x, y + i * stripe, x + w, y + (i + 1) * stripe,
             (178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.4, stripe * 7
    rect(d, x, y, x + cw, y + ch, (30, 50, 110))
    for r in range(4):
        for c in range(5):
            sx = x + cw * (c + 0.5) / 5
            sy = y + ch * (r + 0.5) / 4
            ell(d, sx - 0.8, sy - 0.8, sx + 0.8, sy + 0.8, fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    rect(d, x, y, x + w, y + h, (222, 41, 16))
    pts = star_points((x + w * 0.22) * S, (y + h * 0.28) * S,
                      h * 0.22 * S, h * 0.09 * S)
    d.polygon(pts, fill=(255, 222, 0))
    for fx, fy in [(0.52, 0.14), (0.64, 0.28), (0.62, 0.48), (0.46, 0.58)]:
        pts = star_points((x + w * fx) * S, (y + h * fy) * S,
                          h * 0.09 * S, h * 0.036 * S)
        d.polygon(pts, fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        rect(d, x, y + i * h / 3, x + w, y + (i + 1) * h / 3, col)


# ---------------------------------------------------------------- art panels
# All art functions take a box in 1x units and draw strictly inside it.

def panel_lead_art(d, x0, y0, x1, y1):
    """Shenzhen skyline at dusk + summit table with three leaders."""
    bw, bh = x1 - x0, y1 - y0
    rect(d, x0, y0, x1, y1, (38, 52, 96))
    bands = [(58, 66, 118), (84, 78, 128), (150, 92, 110), (214, 128, 88)]
    for i, col in enumerate(bands):
        rect(d, x0, y0 + i * bh / 4, x1, y0 + (i + 1) * bh / 4 + 0.5, col)
    # sun low on horizon
    sx, sy, sr = x0 + bw * 0.72, y0 + bh * 0.40, 26
    ell(d, sx - sr, sy - sr, sx + sr, sy + sr, fill=(255, 196, 110))
    # back skyline
    base = y0 + bh * 0.66
    bx, i = x0, 0
    while bx < x1:
        w = 17 + ((i * 37) % 23)
        hgt = 45 + ((i * 53) % 75)
        rect(d, bx, base - hgt, bx + w, base, (52, 58, 104))
        bx += w + 3
        i += 1
    # front skyline with lit windows
    bx, i = x0, 0
    while bx < x1:
        w = 24 + ((i * 29) % 26)
        hgt = 60 + ((i * 71) % 75)
        top = base - hgt
        if i == 3:  # tapered landmark tower
            d.polygon([(bx * S, base * S), ((bx + w * 0.42) * S, (top - 42) * S),
                       ((bx + w * 0.58) * S, (top - 42) * S),
                       ((bx + w) * S, base * S)], fill=(24, 28, 52))
        else:
            rect(d, bx, top, bx + w, base, (24, 28, 52))
        for wy in range(int(top) + 7, int(base) - 4, 8):
            for wx in range(int(bx) + 4, int(bx + w) - 3, 7):
                if (wx * 7 + wy * 13 + i) % 5 == 0:
                    rect(d, wx, wy, wx + 2.5, wy + 3.5, (255, 214, 120))
        bx += w + 5
        i += 1
    # ground + table
    rect(d, x0, base, x1, y1, (30, 32, 48))
    ty = y0 + bh * 0.80
    rect(d, x0 + 12, ty, x1 - 12, ty + 20, (96, 58, 40))
    rect(d, x0 + 12, ty, x1 - 12, ty + 5, (128, 80, 54))
    # three seated leaders
    seats = [(0.22, (52, 68, 120), "USA", flag_us),
             (0.50, (178, 34, 34), "CHINA", flag_cn),
             (0.78, (34, 90, 60), "RUSSIA", flag_ru)]
    for frac, suit, label, flagfn in seats:
        cx = x0 + bw * frac
        # torso
        d.polygon([((cx - 26) * S, (ty + 2) * S), ((cx + 26) * S, (ty + 2) * S),
                   ((cx + 20) * S, (ty - 34) * S), ((cx - 20) * S, (ty - 34) * S)],
                  fill=suit)
        d.polygon([((cx - 6) * S, (ty - 32) * S), ((cx + 6) * S, (ty - 32) * S),
                   (cx * S, (ty - 18) * S)], fill=(255, 255, 255))
        # head
        ell(d, cx - 13, ty - 58, cx + 13, ty - 32, fill=(232, 190, 150))
        d.arc([int((cx - 13) * S), int((ty - 58) * S), int((cx + 13) * S),
               int((ty - 32) * S)],
              start=180, end=360, fill=(90, 88, 82), width=3 * S)
        # small flag standing on the table in front of the leader
        flagfn(d, cx - 18, ty - 18, 36, 20)
        # name plate
        rect(d, cx - 24, ty + 5, cx + 24, ty + 15, PAPER)
        fnt = font(SANS_B, 6.5)
        tw = d.textlength(label, font=fnt) / S
        d.text(((cx - tw / 2) * S, (ty + 6.5) * S), label, font=fnt, fill=INK)
    # caption
    fnt = font(SANS, 8)
    d.text(((x0 + 5) * S, (y1 - 13) * S),
           "SHENZHEN, CHINA — THE THREE PRESIDENTS AT THE SUMMIT TABLE",
           font=fnt, fill=(220, 222, 230))


def panel_gta_art(d, x0, y0, x1, y1):
    """Neon Vice City street at dusk."""
    bw, bh = x1 - x0, y1 - y0
    rect(d, x0, y0, x1, y1, (24, 8, 44))
    bands = [(46, 12, 74), (96, 24, 96), (168, 48, 110), (232, 96, 110)]
    for i, col in enumerate(bands):
        rect(d, x0, y0 + i * bh / 4, x1, y0 + (i + 1) * bh / 4 + 0.5, col)
    # neon sun with slats
    cx, cy, r = x0 + bw * 0.5, y0 + bh * 0.52, 43
    ell(d, cx - r, cy - r, cx + r, cy + r, fill=(255, 214, 90))
    for k in range(4):
        yy = cy + r * 0.15 + k * 6.5
        rect(d, cx - r, yy, cx + r, yy + 2.5, (168, 48, 110))
    # skyline
    base = y0 + bh * 0.74
    bx, i = x0, 0
    while bx < x1:
        w = 20 + ((i * 31) % 22)
        hgt = 30 + ((i * 47) % 55)
        rect(d, bx, base - hgt, bx + w, base, (16, 6, 34))
        for wy in range(int(base - hgt) + 5, int(base) - 4, 7):
            for wx in range(int(bx) + 3, int(bx + w) - 2, 6):
                if (wx + wy + i * 11) % 7 == 0:
                    rect(d, wx, wy, wx + 2, wy + 3, (255, 120, 200))
        bx += w + 4
        i += 1
    # street + neon reflection
    rect(d, x0, base, x1, y1, (10, 4, 26))
    rect(d, cx - 4, base, cx + 4, y1 - 24, (255, 90, 180))
    # stars in the upper sky
    for i in range(16):
        sx = x0 + ((i * 7919) % 1000) / 1000 * bw
        sy = y0 + ((i * 104729) % 1000) / 1000 * bh * 0.32
        ell(d, sx - 0.8, sy - 0.8, sx + 0.8, sy + 0.8, fill=(255, 220, 240))
    # neon title
    fnt = font(SANS_B, 34)
    txt = "GTA VI"
    tw = d.textlength(txt, font=fnt) / S
    tx, ty = x0 + bw / 2 - tw / 2, y0 + 10
    for dx, dy in [(1.5, 1.5), (-1.5, 1.5), (1.5, -1.5), (-1.5, -1.5),
                   (0, 2), (2, 0)]:
        d.text(((tx + dx) * S, (ty + dy) * S), txt, font=fnt,
               fill=(255, 45, 149))
    d.text((tx * S, ty * S), txt, font=fnt, fill=(255, 255, 255))
    # sub-label on the dark street, clear of the sun and skyline
    fnt2 = font(SANS_B, 11)
    sub = "VICE CITY  •  LEONIDA"
    tw2 = d.textlength(sub, font=fnt2) / S
    d.text(((x0 + bw / 2 - tw2 / 2) * S, (y1 - 18) * S), sub, font=fnt2,
           fill=(120, 240, 255))


def panel_capitol_art(d, x0, y0, x1, y1):
    """US Capitol dome, flat illustration."""
    bw, bh = x1 - x0, y1 - y0
    rect(d, x0, y0, x1, y1, (168, 198, 226))
    for fx, fy, r in [(0.2, 0.22, 17), (0.75, 0.16, 20), (0.55, 0.3, 13)]:
        px, py = x0 + bw * fx, y0 + bh * fy
        for dx, rr in [(-r, r * 0.7), (0, r), (r, r * 0.7)]:
            ell(d, px + dx - rr, py - rr * 0.7, px + dx + rr, py + rr * 0.7,
                fill=(235, 242, 248))
    base = y1 - 13
    cx = x0 + bw / 2
    rect(d, x0 + 13, base - 26, x1 - 13, base, (240, 238, 230))
    rect(d, x0 + 13, base - 30, x1 - 13, base - 26, (214, 210, 198))
    rect(d, cx - 75, base - 48, cx + 75, base, (245, 243, 236))
    for k in range(7):
        kx = cx - 63 + k * 21
        rect(d, kx, base - 44, kx + 8, base, (214, 210, 198))
    # drum column + dome silhouette (solid, no floating-disc gap)
    rect(d, cx - 54, base - 88, cx + 54, base - 48, (250, 248, 242))
    ell(d, cx - 54, base - 118, cx + 54, base - 70, fill=(250, 248, 242))
    for k in range(9):
        kx = cx - 46 + k * 11.5
        d.line([(kx * S, (base - 84) * S), (kx * S, (base - 52) * S)],
               fill=(214, 210, 198), width=1 * S)
    rect(d, cx - 7, base - 126, cx + 7, base - 116, (240, 238, 230))
    ell(d, cx - 4, base - 131, cx + 4, base - 124, fill=(120, 116, 104))
    rect(d, x0, base, x1, y1, (96, 140, 80))
    rect(d, cx - 55, base, cx + 55, base + 6, (220, 216, 204))


def panel_cyclone_art(d, x0, y0, x1, y1):
    """Cyclone spiral over the Indian coast."""
    bw, bh = x1 - x0, y1 - y0
    rect(d, x0, y0, x1, y1, (58, 84, 96))
    cx, cy = x0 + bw / 2, y0 + bh * 0.46
    for k in range(9):
        r = 13 + k * 8.5
        start = 20 + k * 52
        d.arc([int((cx - r) * S), int((cy - r * 0.82) * S), int((cx + r) * S),
               int((cy + r * 0.82) * S)], start=start, end=start + 235,
              fill=(235, 240, 242), width=max(2, 6 - k // 2) * S)
    ell(d, cx - 10, cy - 8, cx + 10, cy + 8, fill=(30, 44, 56))
    for k in range(14):
        rx = x0 + ((k * 97) % 100) / 100 * bw
        ry = y0 + ((k * 53) % 60) / 100 * bh
        d.line([(rx * S, ry * S), ((rx - 6) * S, (ry + 13) * S)],
               fill=(200, 214, 220), width=3)
    base = y1 - 23
    d.polygon([(x0 * S, (base + 7) * S), ((x0 + bw * 0.3) * S, (base - 8) * S),
               ((x0 + bw * 0.55) * S, (base + 2) * S),
               ((x0 + bw * 0.8) * S, (base - 6) * S), (x1 * S, (base + 4) * S),
               (x1 * S, y1 * S), (x0 * S, y1 * S)], fill=(196, 168, 120))
    fnt = font(SANS_B, 8.5)
    lab = "ANDHRA PRADESH  •  ODISHA"
    tw = d.textlength(lab, font=fnt) / S
    d.text(((x0 + bw / 2 - tw / 2) * S, (y1 - 15) * S), lab, font=fnt,
           fill=(40, 32, 20))
    ell(d, x0 + 7, y0 + 6, x0 + 59, y0 + 32, fill=RED)
    fnt2 = font(SANS_B, 10)
    d.text(((x0 + 11) * S, (y0 + 13) * S), "145 km/h", font=fnt2,
           fill=(255, 255, 255))


def panel_voyager_art(d, x0, y0, x1, y1):
    """Voyager 1 in deep space, one light-day from Earth."""
    bw, bh = x1 - x0, y1 - y0
    rect(d, x0, y0, x1, y1, (6, 8, 20))
    for i in range(70):
        sx = x0 + ((i * 7919) % 1000) / 1000 * bw
        sy = y0 + ((i * 104729) % 1000) / 1000 * bh
        r = 0.8 if i % 7 else 1.5
        b = 200 if i % 3 else 255
        ell(d, sx - r, sy - r, sx + r, sy + r, fill=(b, b, b))
    ex, ey, er = x0 + 26, y1 - 24, 7.5
    ell(d, ex - er - 3, ey - er - 3, ex + er + 3, ey + er + 3,
        fill=(40, 90, 160))
    ell(d, ex - er, ey - er, ex + er, ey + er, fill=(70, 140, 220))
    d.arc([int((ex - er) * S), int((ey - er) * S), int((ex + er) * S),
           int((ey + er) * S)],
          start=200, end=340, fill=(180, 220, 240), width=3)
    px, py = x0 + bw * 0.62, y0 + bh * 0.42
    for k in range(26):
        t = k / 26
        sx = ex + (px - ex) * t
        sy = ey + (py - ey) * t
        ell(d, sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2, fill=(120, 200, 255))
    # dish (left): thin gold ellipse on a short feed arm from the body
    d.line([(int((px - 12) * S), int(py * S)), (int((px - 24) * S),
             int(py * S))], fill=(235, 210, 130), width=2 * S)
    d.ellipse([int((px - 44) * S), int((py - 12) * S), int((px - 20) * S),
               int((py + 12) * S)], outline=(235, 210, 130),
              width=int(2.5 * S))
    d.ellipse([int((px - 38) * S), int((py - 7) * S), int((px - 26) * S),
               int((py + 7) * S)], outline=(235, 210, 130), width=int(1.5 * S))
    # bus: compact gold box
    rect(d, px - 12, py - 9, px + 12, py + 9, (210, 180, 100))
    rect(d, px - 12, py - 9, px + 12, py - 4, (230, 200, 120))
    # magnetometer boom (right) with tip, RTG boom (down-left)
    d.line([(int((px + 12) * S), int(py * S)), (int((px + 44) * S),
             int((py - 6) * S))], fill=(200, 170, 90), width=2 * S)
    ell(d, px + 42, py - 8, px + 46, py - 4, fill=(230, 200, 120))
    d.line([(int((px - 6) * S), int((py + 9) * S)), (int((px - 26) * S),
             int((py + 26) * S))], fill=(200, 170, 90), width=2 * S)
    rect(d, px - 30, py + 24, px - 20, py + 32, (190, 158, 80))
    fnt = font(SANS_B, 9)
    lab = "SIGNAL TIME: 24 HOURS"
    tw = d.textlength(lab, font=fnt) / S
    d.text(((x1 - tw - 7) * S, (y1 - 17) * S), lab, font=fnt,
           fill=(150, 210, 255))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead (0–156) ----------
    title = "THE WORLD IN ONE PAGE"
    mast_size = 80
    while mast_size > 40:
        f_mast = font(SERIF, mast_size)
        if d.textlength(title, font=f_mast) / S <= W - 2 * M - 10:
            break
        mast_size -= 2
    tw = d.textlength(title, font=f_mast) / S
    d.text(((W - tw) / 2 * S, 18 * S), title, font=f_mast, fill=INK)
    f_date = font(SANS_B, 26)
    draw_tracked(d, W / 2, 112, "THURSDAY  19 NOVEMBER 2026", f_date,
                 fill=RED, tracking=5)
    d.line([M * S, 150 * S, (W - M) * S, 150 * S], fill=INK, width=2 * S)
    d.line([M * S, 156 * S, (W - M) * S, 156 * S], fill=INK, width=1 * S)

    # ---------- lead story (168–438) ----------
    lead_y0, lead_y1 = 168, 438
    lx0, lx1 = M, 560
    ax0, ax1 = 576, W - M
    panel_lead_art(d, ax0, lead_y0, ax1, lead_y1)

    f_kick = font(SANS_B, 14)
    d.text((lx0 * S, (lead_y0 + 4) * S), "LEAD STORY  —  SHENZHEN, CHINA",
           font=f_kick, fill=RED)
    f_head = font(SERIF, 40)
    y = lead_y0 + 26
    for ln in ["FIRST-EVER", "TRUMP–XI–PUTIN SUMMIT"]:
        d.text((lx0 * S, y * S), ln, font=f_head, fill=INK)
        y += 42
    y += 8
    f_deck = font(SANS, 17)
    y = draw_wrapped(
        d, lx0, y,
        "The presidents of the US, China and Russia meet today at the "
        "APEC summit in Shenzhen — the first time all three have ever "
        "met together.",
        f_deck, lx1 - lx0, leading=1.3)
    y += 10
    d.line([lx0 * S, y * S, lx1 * S, y * S], fill=LIGHT_GREY, width=1 * S)
    y += 10
    f_fact = font(SANS_B, 13.5)
    y = draw_wrapped(
        d, lx0, y,
        "ON THE TABLE: NUCLEAR ARMS • UKRAINE • IRAN • TRADE • AI",
        f_fact, lx1 - lx0, fill=NAVY, leading=1.3)
    y += 6
    f_note = font(SERIF_REG, 14)
    draw_wrapped(
        d, lx0, y,
        "Arms control tops the agenda after New START expired in February. "
        "Xi hosts; Trump and Putin attend.",
        f_note, lx1 - lx0, leading=1.28)

    # ---------- divider ----------
    d.line([M * S, 452 * S, (W - M) * S, 452 * S], fill=INK, width=3)

    # ---------- secondary row (466–768) ----------
    row_y0 = 466
    col_w = 293
    gap = 24
    cols = [M, M + col_w + gap, M + 2 * (col_w + gap)]
    arts = [panel_gta_art, panel_capitol_art, panel_cyclone_art]
    kickers = ["ENTERTAINMENT — OUT TODAY", "WASHINGTON",
               "WEATHER — INDIA"]
    heads = ["GTA VI IS HERE", "JEFFRIES MAKES\nHISTORY",
             "CYCLONE AKVAN\nBEARS DOWN"]
    decks = [
        "Global rollout begins today after a 13-year wait since GTA V. "
        "Back to Vice City, Leonida, on PS5 and Xbox Series X|S. "
        "$1.65bn in pre-orders; 99 on Metacritic.",
        "House Democrats nominate him for Speaker, 251 votes to 11. "
        "If confirmed by the full House in January, he becomes the "
        "first Black Speaker in US history.",
        "A very severe cyclone bears down on the Andhra Pradesh and "
        "Odisha coasts. Landfall expected about 20 Nov, with winds "
        "of about 145 km/h.",
    ]
    f_ck = font(SANS_B, 12.5)
    f_ch = font(SERIF, 25)
    f_cd = font(SANS, 15)
    for x0, art, kick, head, deck in zip(cols, arts, kickers, heads, decks):
        x1 = x0 + col_w
        art(d, x0, row_y0, x1, row_y0 + 140)
        y = row_y0 + 148
        d.text((x0 * S, y * S), kick, font=f_ck, fill=RED)
        y += 17
        for ln in head.split("\n"):
            d.text((x0 * S, y * S), ln, font=f_ch, fill=INK)
            y += 27
        y += 6
        draw_wrapped(d, x0, y, deck, f_cd, col_w, leading=1.28)

    # ---------- divider ----------
    d.line([M * S, 782 * S, (W - M) * S, 782 * S], fill=INK, width=3)

    # ---------- third row: Voyager + In brief (796–936) ----------
    row3_y0, row3_y1 = 796, 936
    vx0, vx1 = M, 600
    panel_voyager_art(d, vx0, row3_y0, vx0 + 180, row3_y1)
    tx0 = vx0 + 196
    f_vk = font(SANS_B, 12)
    d.text((tx0 * S, (row3_y0 + 4) * S), "SPACE — NASA", font=f_vk, fill=RED)
    f_vh = font(SERIF, 23)
    y = row3_y0 + 22
    for ln in ["VOYAGER 1, ONE", "LIGHT-DAY AWAY"]:
        d.text((tx0 * S, y * S), ln, font=f_vh, fill=INK)
        y += 25
    y += 4
    f_vd = font(SANS, 14)
    draw_wrapped(
        d, tx0, y,
        "Crossed one light-day from Earth on 18 Nov — 25.9 billion km, "
        "173 times the Earth–Sun distance. A signal now takes 24 hours.",
        f_vd, vx1 - tx0, leading=1.28)

    bx0, bx1 = 624, W - M
    f_bh = font(SANS_B, 13)
    d.text((bx0 * S, (row3_y0 + 4) * S), "IN BRIEF", font=f_bh, fill=INK)
    d.line([bx0 * S, (row3_y0 + 22) * S, bx1 * S, (row3_y0 + 22) * S],
           fill=RED, width=3)
    f_bi = font(SANS, 13.5)
    briefs = [
        "EU: €45bn Ukraine loan — repaid after Russia pays reparations.",
        "Ebola, DR Congo: 11,000+ cases, 5,400 deaths (UN).",
        "US–Iran strikes continue: Qeshm Island, Bahrain, Kuwait.",
        "Gaza rain: 46,000+ households displaced.",
    ]
    y = row3_y0 + 30
    for item in briefs:
        rect(d, bx0, y + 4, bx0 + 5, y + 9, RED)
        y = draw_wrapped(d, bx0 + 10, y, item, f_bi, bx1 - bx0 - 10,
                         leading=1.24)
        y += 4

    # ---------- markets strip (946–1024) ----------
    strip_y0, strip_y1 = 946, 1024
    rect(d, 0, strip_y0, W, strip_y1, DARK)
    f_mk = font(SANS_B, 16)
    d.text((M * S, (strip_y0 + 6) * S), "MARKETS", font=f_mk, fill=GOLD)
    f_mv = font(SANS_B, 16)
    d.text(((M + 108) * S, (strip_y0 + 6) * S), "S&P 500  –1.03%",
           font=f_mv, fill=(255, 255, 255))
    d.text(((M + 300) * S, (strip_y0 + 6) * S),
           "GOLD  ~$3,767  •  14-MONTH LOW", font=f_mv,
           fill=(255, 255, 255))
    f_ms = font(SANS, 13.5)
    d.text((M * S, (strip_y0 + 30) * S),
           "NVIDIA: earlier pay raises and more stock grants promised; "
           "H-series shipments to China stopped.",
           font=f_ms, fill=(205, 208, 216))
    d.text((M * S, (strip_y0 + 52) * S),
           "FED MINUTES: most officials expect further rate hikes if "
           "inflation stays hot.",
           font=f_ms, fill=(205, 208, 216))

    img_small = img.resize((1024, 1024), Image.LANCZOS)
    img_small.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    print("wrote", path)

#!/usr/bin/env python3
"""Render 'The World in One Day - Saturday 21 November 2026' broadsheet PNG (v5).

Cream broadsheet design with serif masthead, stat band, region chips,
three illustrated lead panels, ten brief cards, a world map drawn from
hardcoded simplified coastline polygons (lon/lat, equirectangular
projection) with geographically placed pins, a numbered extra-stories
list and a DATE CHECK box. All artwork is original, drawn in code.

Story set: 48 stories, each happened or was first reported on Saturday
21 November 2026. Figures re-verified 22 Nov 2026: Kryvyi Rih toll is
2 killed / 58 injured (42 was the stale Friday-night count); three
ballistic missiles were downed over Riyadh early Saturday (the Jazan
pair was Friday evening, so it sits in DATE CHECK); Las Vegas pole went
to Verstappen after Antonelli's grid penalty; India closed day three at
486/4 with Rahul on 136.

Output: entry.png 1024x1024, deterministic (byte-identical across runs).
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (248, 244, 233)        # cream page
CARD = (255, 253, 247)      # near-white card
INK = (22, 20, 18)
SOFT = (74, 67, 56)         # secondary text
FAINT = (120, 110, 94)
RED = (185, 28, 28)
DEEPRED = (158, 22, 22)
NAVY = (20, 42, 82)
STEEL = (52, 92, 140)
OCHRE = (196, 132, 30)
TEAL = (16, 108, 108)
GREEN = (34, 110, 60)
RULE = (150, 142, 125)
CARDBORD = (204, 195, 174)
OCEAN = (198, 218, 232)
LAND = (237, 225, 197)
LAND_EDGE = (162, 140, 98)
GRAT = (172, 198, 216)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, int(size))


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 24
R = W - M
CW = R - M


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, color, maxw, leading=1.12):
    lh = int(font.size * leading)
    for ln in wrap(text, font, maxw):
        d.text((x, y), ln, font=font, fill=color)
        y += lh
    return y


def center(x0, x1, y, text, font, color):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=color)


def rtext(x1, y, text, font, color):
    d.text((x1 - d.textlength(text, font=font), y), text, font=font, fill=color)


def fit_size(text, path, start, maxw):
    size = start
    while size > 10 and d.textlength(text, font=F(path, size)) > maxw:
        size -= 2
    return size


# ---------- top rule + kicker ----------
d.rectangle([M, 10, R, 13], fill=RED)
d.text((M, 19), "THE WORLD IN ONE DAY", font=F(SANS_B, 14), fill=RED)
rtext(R, 20, "48 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
      F(SANS_B, 10.5), INK)

# ---------- masthead ----------
ms = fit_size("Saturday 21 November 2026", SERIF_B, 68, CW)
center(M, R, 38, "Saturday 21 November 2026", F(SERIF_B, ms), INK)
center(M, R, 108, "Climate summit runs past its deadline \u00b7 Missiles downed over Riyadh "
       "\u00b7 BepiColombo reaches Mercury", F(SERIF_I, 15.5), SOFT)
d.line([(M, 132), (R, 132)], fill=INK, width=3)
d.line([(M, 137), (R, 137)], fill=INK, width=1)

# ---------- stat band ----------
stats = [
    ("0", "climate deal agreed at COP31 by Saturday"),
    ("3", "ballistic missiles downed over Riyadh"),
    ("58", "injured in Kryvyi Rih strike; 2 killed"),
    ("148", "drones in overnight attack on Ukraine"),
    ("6.7", "magnitude of the Peru quake, 00:09 UTC"),
    ("136", "KL Rahul's score as India take control"),
]
sw = CW / 6
for i, (num, cap) in enumerate(stats):
    x0 = M + i * sw
    if i:
        d.line([(x0 - 4, 146), (x0 - 4, 196)], fill=RULE, width=1)
    ns = fit_size(num, SERIF_B, 34, sw - 12)
    d.text((x0 + 4, 144), num, font=F(SERIF_B, ns), fill=INK)
    block(x0 + 4, 180, cap, F(SANS, 8.8), SOFT, sw - 14, 1.1)

# ---------- region chips ----------
chips = [("EUROPE 15", NAVY), ("ASIA 8", DEEPRED), ("MIDDLE EAST 6", OCHRE),
         ("AFRICA 5", GREEN), ("AMERICAS 10", STEEL), ("OCEANIA 4", TEAL)]
for i, (label, col) in enumerate(chips):
    x0 = M + i * sw
    d.rectangle([x0, 202, x0 + sw - 5, 221], fill=col)
    center(x0, x0 + sw - 5, 206, label, F(SANS_B, 11.5), WHITE)

# ---------- lead panels ----------
LEAD_Y = 232
LEAD_H = 110
colw = (CW - 24) / 3


def burst(cx, cy, r, color, width=2):
    for a in range(8):
        ang = a * math.pi / 4
        dx, dy = r * math.cos(ang), r * math.sin(ang)
        d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=color, width=width)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)


def art_cop31(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(206, 226, 240))
    # globe
    gx, gy, gr = x0 + 62, (y0 + y1) / 2 + 6, 30
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 140, 200), outline=(40, 90, 150), width=2)
    d.ellipse([gx - 20, gy - 22, gx - 2, gy - 6], fill=(80, 170, 100))
    d.ellipse([gx + 4, gy - 4, gx + 22, gy + 12], fill=(80, 170, 100))
    d.ellipse([gx - 14, gy + 8, gx + 2, gy + 22], fill=(90, 180, 110))
    for off in (-14, 0, 14):
        d.arc([gx - gr, gy + off - 8, gx + gr, gy + off + 8], 0, 180, fill=(40, 90, 150), width=1)
    # thermometer
    tx = x1 - 58
    d.rectangle([tx, y0 + 18, tx + 9, y1 - 22], fill=WHITE, outline=(120, 120, 120), width=1)
    d.rectangle([tx + 2, y0 + 26, tx + 7, y1 - 22], fill=RED)
    d.ellipse([tx - 6, y1 - 30, tx + 15, y1 - 9], fill=RED, outline=(120, 120, 120), width=1)
    # clock
    cx, cy, cr = x1 - 26, y0 + 34, 13
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=WHITE, outline=INK, width=2)
    d.line([(cx, cy), (cx, cy - 8)], fill=INK, width=2)
    d.line([(cx, cy), (cx + 6, cy + 3)], fill=INK, width=2)


def art_kryvyi(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 24, 54))
    # moon
    mx, my = x1 - 30, y0 + 24
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(240, 236, 200))
    d.ellipse([mx - 4, my - 13, mx + 16, my + 9], fill=(16, 24, 54))
    # skyline
    heights = [34, 48, 28, 54, 40, 30, 46, 36, 50, 32]
    bw = (x1 - x0 - 16) / len(heights)
    for j, bh in enumerate(heights):
        bx = x0 + 8 + j * bw
        d.rectangle([bx, y1 - bh, bx + bw - 5, y1], fill=(38, 52, 96))
        for wy in range(int(y1 - bh + 5), int(y1 - 4), 8):
            for wx in range(int(bx + 3), int(bx + bw - 8), 7):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(250, 210, 110))
    burst(x0 + 60, y0 + 26, 11, (250, 205, 80))
    burst(x0 + 150, y0 + 18, 9, (250, 205, 80))
    burst(x0 + 230, y0 + 30, 10, (250, 205, 80))


def art_riyadh(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(86, 22, 22))
    heights = [40, 26, 52, 34, 44, 28, 48, 36, 42, 30]
    bw = (x1 - x0 - 16) / len(heights)
    for j, bh in enumerate(heights):
        bx = x0 + 8 + j * bw
        d.rectangle([bx, y1 - bh, bx + bw - 5, y1], fill=(52, 14, 14))
        for wy in range(int(y1 - bh + 5), int(y1 - 4), 8):
            for wx in range(int(bx + 3), int(bx + bw - 8), 7):
                if (wx * 11 + wy * 7) % 5 == 0:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(250, 200, 120))
    # missile arcs + intercepts
    for sx, sy in ((70, 30), (160, 22), (245, 34)):
        cx, cy = x0 + sx, y0 + sy
        d.arc([cx - 46, cy - 6, cx + 46, cy + 66], 200, 320, fill=(250, 220, 130), width=2)
        burst(cx, cy, 8, (255, 230, 150))


leads = [
    (1, "COP31: OVERTIME", "Talks continue \u00b7 AP", art_cop31,
     "ANTALYA, T\u00dcRK\u0130YE \u2014 CLIMATE",
     "Climate summit runs into Saturday with no deal",
     "COP31 missed its Friday close. A draft with no mention of fossil fuels split nearly "
     "200 countries; a third text is promised. (AP)"),
    (2, "KRYVYI RIH: STRUCK", "Overnight \u00b7 AP", art_kryvyi,
     "KRYVYI RIH \u2014 WAR",
     "Russian double strike kills two in Kryvyi Rih",
     "Ballistic missiles and 148 drones overnight. A boy of 7 and a paramedic died; 58 hurt, "
     "six of them children. (AP, Kyiv Post)"),
    (3, "RIYADH: 3 DOWNED", "Coalition count \u00b7 AFP", art_riyadh,
     "RIYADH \u2014 CONFLICT",
     "Three missiles downed over Riyadh",
     "Saudi air defences destroyed three ballistic missiles fired at the capital early on "
     "Saturday, the coalition said. (Reuters, AFP)"),
]
for i, (n, label, cap, art, kick, head, summ) in enumerate(leads):
    x0 = M + i * (colw + 12)
    x1 = x0 + colw
    art(x0, LEAD_Y, x1, LEAD_Y + LEAD_H)
    d.text((x0 + 8, LEAD_Y + 6), label, font=F(SANS_B, 17), fill=WHITE,
           stroke_width=3, stroke_fill=(0, 0, 0))
    capw = d.textlength(cap, font=F(SANS, 8.5)) + 10
    d.rectangle([x0, LEAD_Y + LEAD_H - 16, x0 + capw, LEAD_Y + LEAD_H], fill=INK)
    d.text((x0 + 5, LEAD_Y + LEAD_H - 13), cap, font=F(SANS, 8.5), fill=WHITE)
    d.rectangle([x0, LEAD_Y, x1, LEAD_Y + LEAD_H], outline=INK, width=1)
    ky = LEAD_Y + LEAD_H + 8
    d.ellipse([x0, ky, x0 + 15, ky + 15], fill=RED)
    center(x0, x0 + 15, ky + 2, str(n), F(SANS_B, 10), WHITE)
    d.text((x0 + 20, ky + 2), kick, font=F(SANS_B, 10), fill=INK)
    y = block(x0, ky + 20, head, F(SERIF_B, 18.5), INK, colw, 1.05)
    block(x0, y + 2, summ, F(SERIF, 10.8), SOFT, colw, 1.14)

# ---------- mid cards (stories 4-13) ----------
CARD_Y = 462
CARD_H = 104
cardw = (CW - 32) / 5


def mini_planet(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(14, 18, 40))
    for sx, sy in ((18, 8), (52, 14), (120, 7), (160, 12), (88, 10)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=WHITE)
    px, py = x0 + 130, (y0 + y1) / 2
    d.ellipse([px - 13, py - 13, px + 13, py + 13], fill=(170, 165, 155), outline=(110, 105, 95), width=1)
    d.ellipse([px - 7, py - 6, px - 1, py], fill=(140, 135, 125))
    d.rectangle([x0 + 40, py - 4, x0 + 56, py + 4], fill=(220, 200, 120))
    d.line([(x0 + 56, py), (x0 + 72, py - 6)], fill=(220, 200, 120), width=2)
    d.ellipse([x0 + 70, py - 10, x0 + 78, py - 2], outline=(220, 200, 120), width=2)


def mini_plane(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 230, 244))
    cy = (y0 + y1) / 2
    d.polygon([(x0 + 30, cy + 2), (x0 + 120, cy - 2), (x0 + 150, cy - 2),
               (x0 + 120, cy + 4), (x0 + 30, cy + 6)], fill=(60, 80, 110))
    d.polygon([(x0 + 78, cy), (x0 + 96, cy - 12), (x0 + 104, cy - 12), (x0 + 92, cy + 1)], fill=(60, 80, 110))
    d.polygon([(x0 + 34, cy + 2), (x0 + 26, cy - 9), (x0 + 34, cy - 9), (x0 + 42, cy + 2)], fill=DEEPRED)


def mini_cricket(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(120, 180, 110))
    d.rectangle([x0 + 60, y0 + 4, x0 + 72, y1 - 4], fill=(232, 214, 170))
    d.ellipse([x0 + 120, y0 + 10, x0 + 132, y0 + 22], fill=(200, 30, 30))
    d.arc([x0 + 120, y0 + 10, x0 + 132, y0 + 22], 300, 60, fill=WHITE, width=1)


def mini_f1(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(30, 30, 38))
    cy = y1 - 8
    d.line([(x0 + 4, cy), (x1 - 4, cy)], fill=(240, 240, 240), width=2)
    for i in range(6):
        d.rectangle([x0 + 8 + i * 30, cy - 4, x0 + 20 + i * 30, cy], fill=WHITE if i % 2 else (30, 30, 38))
    d.rectangle([x0 + 60, cy - 12, x0 + 118, cy - 6], fill=(210, 40, 40))
    d.rectangle([x0 + 82, cy - 17, x0 + 98, cy - 12], fill=(210, 40, 40))
    d.ellipse([x0 + 66, cy - 8, x0 + 76, cy + 2], fill=(10, 10, 10))
    d.ellipse([x0 + 102, cy - 8, x0 + 112, cy + 2], fill=(10, 10, 10))


def mini_quake(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(250, 244, 220))
    cy = (y0 + y1) / 2
    pts = [(x0 + 6, cy), (x0 + 40, cy), (x0 + 52, cy - 10), (x0 + 62, cy + 10),
           (x0 + 72, cy - 13), (x0 + 82, cy + 13), (x0 + 92, cy - 6), (x0 + 100, cy + 6),
           (x0 + 112, cy), (x1 - 6, cy)]
    d.line(pts, fill=RED, width=2)
    d.line([(x0 + 6, cy), (x1 - 6, cy)], fill=(180, 170, 150), width=1)


def mini_boat(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(170, 205, 228))
    cy = y0 + 16
    d.polygon([(x0 + 50, cy), (x0 + 130, cy), (x0 + 118, cy + 9), (x0 + 62, cy + 9)], fill=(90, 60, 40))
    d.line([(x0 + 90, cy), (x0 + 90, cy - 10)], fill=(90, 60, 40), width=2)
    for wx in range(int(x0 + 8), int(x1 - 12), 18):
        d.arc([wx, cy + 8, wx + 14, cy + 16], 180, 360, fill=(60, 120, 180), width=2)


def mini_deal(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 238, 230))
    d.ellipse([x0 + 52, y0 + 5, x0 + 82, y0 + 25], fill=NAVY)
    d.ellipse([x0 + 92, y0 + 5, x0 + 122, y0 + 25], fill=DEEPRED)
    center(x0 + 52, x0 + 82, y0 + 9, "UK", F(SANS_B, 10), WHITE)
    center(x0 + 92, x0 + 122, y0 + 9, "EU", F(SANS_B, 10), WHITE)


def mini_flag(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(242, 230, 200))
    d.polygon([(x0, y1), (x0 + 90, y0 + 14), (x1, y1)], fill=(214, 188, 140))
    d.line([(x0 + 90, y0 + 14), (x0 + 90, y0 + 3)], fill=INK, width=2)
    d.rectangle([x0 + 90, y0 + 3, x0 + 108, y0 + 10], fill=GREEN)


def mini_ballot(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 240, 235))
    d.rectangle([x0 + 66, y0 + 12, x0 + 112, y1 - 3], fill=(90, 90, 90))
    d.rectangle([x0 + 76, y0 + 3, x0 + 102, y0 + 14], fill=WHITE, outline=(150, 150, 150), width=1)
    d.text((x0 + 84, y0 + 5), "\u2713", font=F(SANS_B, 10), fill=GREEN)


def mini_tennis(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(110, 170, 100))
    d.ellipse([x0 + 66, y0 + 3, x0 + 92, y0 + 24], outline=(60, 40, 20), width=3)
    d.line([(x0 + 86, y0 + 21), (x0 + 100, y1 - 2)], fill=(60, 40, 20), width=3)
    d.ellipse([x0 + 120, y0 + 12, x0 + 130, y0 + 22], fill=(220, 240, 90))


cards = [
    ("MERCURY: 19:24", NAVY, mini_planet, "4 \u00b7 SPACE",
     "BepiColombo reaches Mercury", "Thrusters fire tonight after an 8-year voyage. (ESA)"),
    ("WARSAW: TALKS", STEEL, mini_plane, "5 \u00b7 POLAND",
     "Rutte flies to Warsaw for NATO talks", "Warsaw wants more NATO forces. (AP)"),
    ("WELLINGTON: 486/4", GREEN, mini_cricket, "6 \u00b7 CRICKET",
     "Rahul ton puts India in charge", "136 as India close 118 ahead at stumps. (Scorecard)"),
    ("LAS VEGAS: POLE", (38, 38, 46), mini_f1, "7 \u00b7 FORMULA 1",
     "Verstappen inherits pole", "Antonelli fastest but takes a grid penalty. (F1)"),
    ("PERU: QUAKE 6.7", DEEPRED, mini_quake, "8 \u00b7 EARTHQUAKE",
     "Magnitude 6.7 quake hits Peru", "Struck 00:09 GMT near Jun\u00edn; felt in Lima. (USGS)"),
    ("BAYELSA: 4 DEAD", TEAL, mini_boat, "9 \u00b7 NIGERIA",
     "Funeral boat capsizes", "At least four dead in Bayelsa. (Reports)"),
    ("LONDON: DEAL", NAVY, mini_deal, "10 \u00b7 BRITAIN",
     "UK and EU seal a reset deal", "Youth mobility agreed: 100,000 visas a year. (AP)"),
    ("IRAQ: RETAKEN", OCHRE, mini_flag, "11 \u00b7 IRAQ",
     "Forces retake Jurf al-Sakhar", "Town held since 2014 back in Iraqi hands. (Reports)"),
    ("S. AFRICA: 31%", GREEN, mini_ballot, "12 \u00b7 POLITICS",
     "ANC scrambles after worst result", "31% is its weakest showing since 1994. (BBC)"),
    ("TURIN: SEMI", (96, 64, 140), mini_tennis, "13 \u00b7 TENNIS",
     "Medvedev meets Zverev tonight", "Beat Rune on Friday to reach the last four. (ATP)"),
]
for idx, (band, bcol, art, kick, head, line) in enumerate(cards):
    row, col = divmod(idx, 5)
    x0 = M + col * (cardw + 8)
    x1 = x0 + cardw
    y0 = CARD_Y + row * (CARD_H + 8)
    d.rectangle([x0, y0, x1, y0 + CARD_H], fill=CARD, outline=CARDBORD, width=1)
    d.rectangle([x0, y0, x1, y0 + 20], fill=bcol)
    center(x0, x1, y0 + 4, band, F(SANS_B, 10.5), WHITE)
    art(x0 + 1, y0 + 20, x1 - 1, y0 + 50)
    d.text((x0 + 7, y0 + 53), kick, font=F(SANS_B, 8.5), fill=RED)
    y = block(x0 + 7, y0 + 64, head, F(SERIF_B, 12), INK, cardw - 14, 1.05)
    block(x0 + 7, y + 1, line, F(SERIF, 8.8), SOFT, cardw - 14, 1.08)

# ---------- world map (stories 1-13) ----------
# Simplified coastline polygons in (lon, lat); equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-161, 70), (-152, 71), (-144, 70), (-136, 69), (-128, 70),
     (-121, 69), (-113, 68), (-105, 68), (-97, 69), (-92, 66), (-88, 66),
     (-85, 62), (-82, 60), (-79, 58), (-81, 55), (-84, 54), (-87, 52),
     (-90, 51), (-88, 48), (-85, 47), (-83, 46), (-80, 44), (-77, 43),
     (-74, 41), (-71, 41), (-69, 44), (-66, 45), (-62, 46), (-60, 47),
     (-56, 50), (-53, 49), (-56, 47), (-60, 46), (-65, 44), (-68, 44),
     (-70, 42), (-73, 40), (-75, 38), (-76, 36), (-79, 33), (-81, 31),
     (-81, 27), (-80, 25), (-82, 28), (-84, 30), (-87, 30), (-89, 29),
     (-92, 29), (-95, 29), (-97, 27), (-97, 24), (-96, 20), (-94, 18),
     (-91, 15), (-88, 14), (-86, 12), (-83, 9), (-80, 8), (-77, 7),
     (-79, 9), (-82, 9), (-84, 11), (-86, 13), (-88, 16), (-88, 18),
     (-90, 20), (-91, 19), (-90, 21), (-88, 21), (-87, 21), (-90, 20),
     (-94, 18), (-96, 16), (-97, 16), (-100, 17), (-102, 18), (-105, 20),
     (-108, 23), (-110, 24), (-112, 28), (-114, 30), (-117, 33), (-121, 35),
     (-123, 38), (-124, 42), (-124, 46), (-126, 49), (-129, 52), (-132, 56),
     (-135, 58), (-140, 60), (-146, 61), (-152, 60), (-158, 58), (-162, 60),
     (-165, 62)],
    [(-78, 7), (-76, 9), (-73, 11), (-70, 12), (-67, 11), (-64, 10), (-61, 9),
     (-58, 7), (-55, 6), (-52, 4), (-50, 0), (-47, -2), (-44, -3), (-40, -4),
     (-35, -8), (-37, -11), (-39, -14), (-39, -17), (-40, -20), (-42, -23),
     (-46, -24), (-49, -27), (-52, -30), (-54, -33), (-57, -35), (-58, -38),
     (-62, -39), (-63, -41), (-65, -43), (-65, -46), (-66, -48), (-67, -50),
     (-68, -52), (-68, -54), (-70, -54), (-72, -52), (-74, -48), (-74, -44),
     (-73, -40), (-73, -36), (-72, -32), (-71, -28), (-70, -24), (-70, -20),
     (-70, -18), (-73, -16), (-76, -14), (-77, -11), (-78, -8), (-80, -5),
     (-81, -3), (-81, 0), (-80, 2), (-78, 4)],
    [(-6, 35), (-9, 32), (-13, 28), (-16, 24), (-17, 20), (-17, 16), (-16, 13),
     (-14, 10), (-12, 8), (-8, 5), (-5, 5), (-2, 5), (1, 6), (4, 6), (6, 4),
     (8, 4), (9, -1), (11, -4), (13, -8), (13, -12), (14, -16), (12, -18),
     (13, -20), (14, -23), (15, -27), (17, -31), (19, -34), (20, -35),
     (24, -34), (27, -33), (30, -30), (32, -28), (34, -26), (35, -23),
     (36, -20), (37, -17), (39, -14), (40, -11), (40, -8), (39, -5), (40, -2),
     (42, 1), (45, 4), (48, 7), (51, 10), (51, 12), (48, 11), (45, 11),
     (43, 12), (41, 14), (40, 16), (39, 19), (38, 22), (36, 25), (34, 28),
     (33, 29), (32, 31), (30, 31), (27, 31), (24, 32), (21, 33), (18, 33),
     (15, 32), (12, 33), (10, 34), (9, 37), (6, 37), (3, 37), (0, 36),
     (-2, 35)],
    [(-9, 37), (-9, 39), (-9, 43), (-7, 44), (-4, 44), (-2, 44), (-1, 46),
     (-2, 48), (-4, 48), (-2, 49), (0, 49), (1, 51), (3, 51), (5, 53),
     (7, 54), (8, 55), (8, 57), (7, 58), (5, 59), (5, 61), (7, 63),
     (10, 64), (13, 66), (15, 68), (18, 69), (22, 70), (26, 71), (30, 70),
     (31, 68), (29, 66), (27, 64), (25, 65), (23, 64), (22, 61), (20, 60),
     (19, 59), (17, 58), (16, 56), (14, 55), (16, 54), (18, 56), (20, 55),
     (22, 55), (24, 58), (26, 59), (28, 59), (30, 60), (30, 55), (28, 50),
     (28, 46), (26, 44), (28, 41), (26, 38), (24, 38), (23, 37), (22, 38),
     (20, 40), (19, 42), (18, 40), (17, 40), (16, 38), (16, 40), (15, 42),
     (13, 44), (12, 44), (10, 44), (8, 44), (7, 44), (3, 43), (3, 42),
     (2, 40), (0, 38), (-2, 37), (-6, 36)],
    [(28, 41), (33, 42), (36, 41), (39, 41), (42, 42), (45, 43), (48, 46),
     (50, 50), (53, 54), (55, 58), (58, 62), (60, 66), (66, 68), (70, 70),
     (75, 72), (80, 73), (85, 74), (90, 75), (95, 76), (100, 77), (105, 77),
     (110, 74), (115, 73), (120, 73), (125, 72), (130, 72), (135, 71),
     (140, 72), (145, 72), (150, 70), (155, 70), (160, 69), (165, 69),
     (170, 67), (175, 66), (178, 66), (177, 64), (173, 62), (170, 60),
     (166, 60), (162, 60), (160, 56), (158, 52), (156, 51), (154, 54),
     (152, 58), (150, 59), (147, 59), (144, 59), (142, 54), (141, 50),
     (142, 47), (140, 46), (138, 46), (135, 45), (133, 44), (131, 43),
     (129, 42), (127, 40), (126, 38), (124, 40), (122, 38), (121, 36),
     (120, 34), (121, 31), (122, 29), (120, 27), (118, 25), (116, 23),
     (114, 22), (111, 21), (109, 20), (108, 18), (109, 15), (109, 13),
     (107, 11), (105, 9), (104, 8), (103, 6), (101, 3), (100, 5), (99, 8),
     (98, 10), (98, 13), (96, 15), (94, 17), (92, 20), (91, 22), (89, 22),
     (88, 21), (86, 20), (84, 19), (82, 17), (80, 15), (80, 13), (79, 11),
     (77, 8), (76, 10), (74, 13), (73, 16), (72, 19), (72, 21), (70, 22),
     (68, 23), (66, 25), (63, 25), (61, 25), (59, 24), (58, 23), (57, 24),
     (56, 26), (54, 26), (52, 26), (50, 27), (48, 29), (49, 30), (50, 27),
     (52, 25), (55, 24), (58, 23), (59, 22), (58, 21), (56, 19), (55, 17),
     (53, 16), (50, 15), (48, 14), (45, 13), (43, 12), (42, 14), (40, 17),
     (38, 21), (36, 24), (35, 28), (34, 29), (36, 31), (36, 33), (36, 36),
     (33, 36), (30, 36), (28, 37), (27, 38)],
    [(113, -22), (114, -25), (114, -28), (115, -31), (115, -34), (117, -35),
     (119, -34), (122, -33), (125, -33), (128, -32), (130, -32), (132, -32),
     (134, -33), (135, -35), (136, -35), (137, -35), (138, -36), (139, -37),
     (140, -38), (142, -38), (145, -38), (147, -38), (149, -37), (150, -36),
     (151, -34), (152, -31), (153, -28), (153, -26), (152, -24), (151, -23),
     (150, -22), (149, -21), (148, -20), (147, -19), (146, -18), (146, -17),
     (145, -15), (144, -13), (143, -12), (142, -11), (142, -13), (142, -15),
     (141, -17), (140, -17), (139, -17), (137, -16), (136, -15), (136, -14),
     (135, -12), (133, -12), (132, -11), (130, -12), (128, -13), (126, -14),
     (124, -15), (122, -17), (120, -19), (118, -20), (116, -20), (114, -21)],
    [(-44, 60), (-41, 61), (-38, 63), (-34, 66), (-30, 68), (-26, 70),
     (-22, 71), (-20, 73), (-21, 75), (-24, 77), (-30, 79), (-38, 80),
     (-46, 80), (-53, 78), (-57, 76), (-58, 72), (-56, 68), (-54, 65),
     (-52, 62), (-50, 60), (-47, 60)],
    [(-5, 50), (-4, 51), (-3, 53), (-2, 54), (-3, 56), (-4, 58), (-6, 58),
     (-7, 57), (-7, 55), (-6, 53), (-5, 52)],
    [(-10, 52), (-8, 52), (-6, 52), (-5, 54), (-6, 55), (-8, 55), (-10, 54)],
    [(-22, 64), (-18, 63), (-15, 64), (-14, 65), (-16, 66), (-20, 66), (-22, 65)],
    [(-85, 23), (-82, 23), (-79, 22), (-76, 21), (-74, 20), (-76, 20),
     (-79, 21), (-82, 22), (-85, 22)],
    [(130, 31), (131, 32), (132, 33), (134, 34), (135, 34), (136, 35),
     (137, 35), (138, 36), (139, 37), (140, 38), (141, 40), (141, 41),
     (142, 43), (143, 44), (141, 44), (140, 42), (140, 39), (139, 37),
     (138, 36), (136, 35), (134, 34), (132, 33), (131, 32)],
    [(44, -16), (46, -14), (48, -14), (50, -16), (50, -19), (48, -21),
     (47, -23), (46, -25), (45, -25), (44, -23), (43, -20), (43, -17)],
    [(95, 5), (97, 4), (99, 2), (101, 0), (103, -2), (104, -4), (105, -5),
     (103, -4), (101, -2), (99, 1), (97, 3)],
    [(106, -6), (108, -6), (110, -7), (112, -7), (114, -8), (113, -8),
     (110, -8), (108, -7), (106, -7)],
    [(109, 1), (111, 2), (114, 3), (116, 4), (118, 3), (119, 1), (118, -1),
     (116, -2), (114, -3), (112, -2), (110, -1)],
    [(119, 0), (120, 1), (122, 0), (123, -1), (122, -3), (120, -4), (119, -2)],
    [(131, -1), (133, -2), (136, -2), (139, -3), (142, -4), (145, -5),
     (147, -7), (149, -9), (150, -10), (148, -9), (145, -8), (142, -7),
     (139, -6), (136, -4), (133, -3), (131, -2)],
    [(120, 18), (121, 17), (122, 16), (121, 14), (122, 13), (121, 12),
     (122, 11), (123, 10), (122, 9), (121, 8), (122, 7), (123, 8),
     (123, 10), (124, 11), (123, 13), (122, 15), (121, 16)],
    [(173, -35), (175, -36), (177, -37), (178, -38), (176, -39), (175, -40),
     (174, -39), (173, -37)],
    [(167, -46), (169, -45), (171, -44), (172, -43), (173, -42), (172, -41),
     (171, -42), (170, -44), (168, -46)],
]

PINS = {
    1: (30.7, 36.9),     # Antalya
    2: (33.4, 47.9),     # Kryvyi Rih
    3: (46.7, 24.6),     # Riyadh
    5: (21.0, 52.2),     # Warsaw
    6: (174.8, -41.3),   # Wellington
    7: (-115.1, 36.2),   # Las Vegas
    8: (-75.0, -11.0),   # Junin, Peru
    9: (6.1, 4.9),       # Bayelsa, Nigeria
    10: (-0.1, 51.5),    # London
    11: (44.4, 32.9),    # Jurf al-Sakhar, Iraq
    12: (28.0, -26.0),   # South Africa
    13: (7.7, 45.1),     # Turin
}

d.text((M, 686), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
mx0, my0, mx1, my1 = M, 706, M + 476, 892
LAT_TOP, LAT_BOT = 83.0, -60.0


def proj(lon, lat):
    x = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
    y = my0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (my1 - my0)
    return x, y


d.rectangle([mx0, my0, mx1, my1], fill=OCEAN)
for lon in range(-180, 181, 30):
    x, _ = proj(lon, 0)
    d.line([(x, my0), (x, my1)], fill=GRAT, width=1)
for lat in range(-60, 84, 30):
    _, y = proj(0, lat)
    d.line([(mx0, y), (mx1, y)], fill=GRAT, width=1)
_, yeq = proj(0, 0)
for x in range(mx0, mx1, 10):
    d.line([(x, yeq), (x + 5, yeq)], fill=(120, 160, 195), width=1)
for poly in CONTINENTS:
    pts = [proj(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND, outline=LAND_EDGE)
for n, (lon, lat) in PINS.items():
    cx, cy = proj(lon, lat)
    cx = max(mx0 + 8, min(cx, mx1 - 8))  # keep edge pins (e.g. Wellington) inside
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=WHITE, width=1)
    center(cx - 7, cx + 7, cy - 5, str(n), F(SANS_B, 9), WHITE)
d.rectangle([mx0, my0, mx1, my1], outline=INK, width=1)
d.text((mx0 + 5, my1 - 14), "Red numbers mark stories 1\u201313. No. 4 is in space: Mercury.",
       font=F(SANS, 8), fill=(140, 30, 30))

# ---------- more stories (14-48) ----------
more = [
    "14 Tokyo: Frosty APEC greeting for Takaichi. (Asahi)",
    "15 Los Angeles: Palisades Fire arsonist convicted. (AP)",
    "16 Ottawa: US leadership in doubt, forum warns. (Forum)",
    "17 Brussels: EU-UK summit mends Brexit ties. (Reports)",
    "18 Kabul: UN warns ISIS-K gaining drones. (UN)",
    "19 Berlin: Students march against rearmament. (Reports)",
    "20 Bras\u00edlia: Indigenous land bill advances. (Reports)",
    "21 Sydney: Heatwave breaks records. (Reports)",
    "22 Jakarta: Asset-forfeiture law takes effect. (Reports)",
    "23 New Delhi: SCO forum sessions open. (PTI)",
    "24 Washington: Iran engagement cost $48.3bn. (DoD)",
    "25 Kyiv: Three Russian missile systems hit. (Kyiv)",
    "26 Ankara: '35 by 35' goal enters COP31 text. (Reuters)",
    "27 Santiago: Quake in north Chile. (Reports)",
    "28 Paris: Diallo backed in FIFA election race. (Reuters)",
    "29 Davao: Air Niugini jet lands, all 146 safe. (CAAP)",
    "30 Seoul: Train derails, five cars off rails. (Korea Times)",
    "31 Hodeidah: Port strikes threaten aid lifeline. (UN, AP)",
    "32 The Hague: Swiss hail ICJ Myanmar ruling. (Reports)",
    "33 Melbourne: Australia host England in first T20. (AFP)",
    "34 Banda Sea: M6.8 quake at 09:42 GMT, no tsunami. (USGS)",
    "35 London: Cancer pill clears tumours in 1 in 12. (Reports)",
    "36 Washington: FBI crime database reportedly hacked. (BBC)",
    "37 Copenhagen: Denmark expels Russian diplomat. (BBC)",
    "38 Munich: Kane out months with ankle tear. (Al Jazeera)",
    "39 Turin: Alcaraz beats Cobolli 6-4 6-1, unbeaten. (ATP)",
    "40 Cape Town: Mlambo-Ngcuka dies aged 71. (Reports)",
    "41 Gaza: Israeli fire kills Palestinians. (Reports)",
    "42 Port-au-Prince: Salvadoran troops lose soldiers. (Reports)",
    "43 Basra: Power-station fire kills four, 30 hurt. (Hindu)",
    "44 Kampala: Uganda curbs gatherings over Ebola. (Reports)",
    "45 Geneva: Nations to elaborate AI-weapons rules. (NPR)",
    "46 Sydney: Swimmer Jon Henricks dies aged 91. (ABC)",
    "47 Seoul: Choi wins third straight 1,000m title. (Reports)",
    "48 Cleveland: Harden passes Bryant on 50-pt list. (Al Jazeera)",
]
lx = mx1 + 16
d.text((lx, 686), "ALSO ON SATURDAY 21 NOVEMBER 2026 \u2014 35 MORE STORIES",
       font=F(SANS_B, 11), fill=INK)
colw = (R - lx - 10) / 2
half = (len(more) + 1) // 2
for c in range(2):
    x0 = lx + c * (colw + 10)
    y = 706
    for s in more[c * half:(c + 1) * half]:
        y = block(x0, y, s, F(SERIF, 8.2), INK, colw, 1.04) + 1

# ---------- date check ----------
dy = 902
d.rectangle([M, dy, R, dy + 62], outline=RED, width=2)
d.text((M + 10, dy + 6), "DATE CHECK", font=F(SANS_B, 12), fill=RED)
block(M + 10, dy + 24,
      "Every story here happened, or was first reported, on Saturday 21 November 2026. LEFT OUT \u2014 other days' news: "
      "Russian missiles land in Poland (Fri 20 Nov) \u00b7 two missiles over Jazan (Fri evening) \u00b7 Kyiv bridges hit "
      "(Fri 20 Nov) \u00b7 Cyclone Akvan makes landfall (Fri 20 Nov) \u00b7 ICJ Myanmar genocide ruling (Thu 19 Nov) \u00b7 "
      "Wall Street AI sell-off (Fri 20 Nov) \u00b7 Anthropic debut, shares jump 17% (Thu 19 Nov) \u00b7 GTA VI launch "
      "(Thu 19 Nov) \u00b7 Starc's 7/58 \u2014 that was the 2025 Ashes, a year ago.",
      F(SERIF, 9.3), INK, R - M - 20, 1.12)

d.text((M, 974), "Sources named beside each story \u00b7 Claims attributed, not stated as fact "
       "\u00b7 Pictures and map: original, drawn in code", font=F(SANS, 9), fill=SOFT)
rtext(R, 974, "Saturday 21 November 2026", F(SANS_B, 9), INK)

img.save("entry.png", format="PNG", optimize=False)
print("wrote entry.png", img.size)

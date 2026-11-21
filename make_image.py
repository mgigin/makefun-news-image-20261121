#!/usr/bin/env python3
"""Render 'The World in One Day - Saturday 21 November 2026' broadsheet PNG (v4).

Original layout/code, redesigned to differ clearly from the reference image:
dark navy theme with gold accents, sans-serif masthead, outline region chips,
left rail of stacked leads, two-column brief cards, and a realistic world map
drawn from hardcoded simplified coastline polygons (lon/lat, equirectangular
projection) with graticule, ocean shading and geographically placed pins.

Story set identical to v3: 48 stories, each happened or was first reported on
Saturday 21 November 2026. Kryvyi Rih toll corrected to 2 killed / 58 injured;
the Poland missiles story sits in DATE CHECK as Fri 20 Nov.
Output: entry.png 1024x1024, deterministic (byte-identical across runs).
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (10, 20, 38)          # deep navy page
PANEL = (16, 30, 54)       # slightly lighter panel
PANEL_LINE = (52, 74, 108)
WHITE = (242, 240, 234)
MUTED = (168, 180, 202)
GOLD = (212, 175, 55)
GOLD_DIM = (150, 124, 52)
RED = (232, 84, 70)
OCEAN_TOP = (16, 44, 80)
OCEAN_MID = (22, 60, 100)
OCEAN_BOT = (14, 38, 70)
LAND = (198, 170, 112)
LAND_EDGE = (128, 102, 60)
GRAT = (40, 72, 110)

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 28
R = W - M


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
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


# ---------- kicker ----------
d.text((M, 16), "THE WORLD IN ONE DAY", font=F(SANS_B, 15), fill=GOLD)
rtext(R, 18, "SATURDAY EDITION \u2022 48 STORIES \u2022 EVERY CONTINENT", F(SANS, 12), MUTED)

# ---------- masthead ----------
d.text((M, 38), "Saturday 21 November 2026", font=F(SANS_B, 54), fill=WHITE)
d.rectangle([R - 228, 40, R, 100], outline=GOLD, width=2)
center(R - 228, R, 48, "48 STORIES", F(SANS_B, 26), GOLD)
center(R - 228, R, 80, "ONE DAY \u2022 EVERY CONTINENT", F(SANS, 10.5), MUTED)
d.text((M, 108), "COP31 runs into overtime \u2022 Riyadh downs three missiles \u2022 BepiColombo at Mercury",
       font=F(SERIF_I, 18), fill=GOLD)
d.line([(M, 138), (R, 138)], fill=GOLD, width=2)

# ---------- region chips (outline style, honest counts of the 48-story set) ----------
chips = ["EUROPE 15", "ASIA 8", "MIDDLE EAST 6", "AFRICA 5", "AMERICAS 10", "OCEANIA 4"]
cw = (R - M) / 6
for i, label in enumerate(chips):
    x0 = M + i * cw
    d.rectangle([x0, 148, x0 + cw - 6, 174], outline=GOLD_DIM, width=1)
    center(x0, x0 + cw - 6, 154, label, F(SANS_B, 12.5), WHITE)

# ---------- stat band ----------
stats = [("0", "climate deal agreed at COP31"), ("3", "missiles downed over Riyadh"),
         ("2", "killed in Kryvyi Rih strike, 58 injured"),
         ("148", "drones in overnight attack on Ukraine"),
         ("8 yrs", "BepiColombo's voyage to Mercury"), ("6.7", "Peru quake magnitude")]
for i, (num, cap) in enumerate(stats):
    x0 = M + i * cw
    if i:
        d.line([(x0 - 3, 186), (x0 - 3, 238)], fill=PANEL_LINE, width=1)
    d.text((x0 + 4, 184), num, font=F(SANS_B, 29), fill=GOLD)
    block(x0 + 4, 218, cap, F(SANS, 9.5), MUTED, cw - 14, 1.1)
d.line([(M, 248), (R, 248)], fill=PANEL_LINE, width=1)

# ---------- body headers ----------
RAIL_R = M + 320          # left rail right edge
BODY_X = RAIL_R + 18      # right column start
d.text((M, 258), "TOP STORIES", font=F(SANS_B, 14), fill=GOLD)
d.text((BODY_X, 258), "THE DAY IN BRIEF", font=F(SANS_B, 14), fill=GOLD)
d.line([(RAIL_R + 8, 256), (RAIL_R + 8, 612)], fill=PANEL_LINE, width=1)

# ---------- left rail: 3 leads stacked ----------
leads = [
    ("1 ANTALYA \u2022 CLIMATE", "COP31 runs into overtime with no deal",
     "Talks pass the Friday deadline; a third draft is due Saturday. (AP)", "NO DEAL"),
    ("2 KRYVYI RIH \u2022 WAR", "Russian strikes kill two in Ukraine",
     "Ballistic missiles and 148 drones overnight; a boy of 7 and a paramedic died, 58 hurt. (Kyiv Post, AP)", "2 KILLED"),
    ("3 RIYADH \u2022 CONFLICT", "Coalition downs three missiles over Riyadh",
     "Air defences destroy three ballistic missiles fired at the capital early on Saturday. (Reuters)", "3 DOWNED"),
]
railw = RAIL_R - M
for i, (kick, head, deck, tag) in enumerate(leads):
    y0 = 278 + i * 106
    gx1 = M + railw
    gy1 = y0 + 44
    if i == 0:  # globe + thermometer
        d.rectangle([M, y0, gx1, gy1], fill=(24, 58, 84))
        d.ellipse([M + 14, y0 + 9, M + 40, gy1 - 9], fill=(44, 110, 190))
        d.ellipse([M + 20, y0 + 14, M + 34, y0 + 24], fill=(46, 160, 90))
        d.rectangle([gx1 - 46, y0 + 8, gx1 - 38, gy1 - 12], fill=RED)
        d.ellipse([gx1 - 51, gy1 - 18, gx1 - 33, gy1 - 2], fill=RED)
        d.text((gx1 - 108, y0 + 12), "1.5\u00b0C+", font=F(SANS_B, 15), fill=(255, 150, 130))
    elif i == 1:  # night skyline + bursts
        d.rectangle([M, y0, gx1, gy1], fill=(12, 18, 44))
        for j, bh in enumerate([20, 32, 16, 36, 24, 30, 18, 28]):
            bx = M + 12 + j * (railw - 24) / 8
            d.rectangle([bx, gy1 - bh, bx + 22, gy1], fill=(52, 66, 120))
        for sx in (0.28, 0.55, 0.82):
            cx, cy = M + railw * sx, y0 + 13
            for a in range(6):
                dx, dy = 9 * math.cos(a * math.pi / 3), 9 * math.sin(a * math.pi / 3)
                d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=(240, 200, 60), width=2)
    else:  # skyline + missile arcs
        d.rectangle([M, y0, gx1, gy1], fill=(70, 22, 22))
        for j, bh in enumerate([26, 18, 32, 22, 28, 20, 30, 24]):
            bx = M + 12 + j * (railw - 24) / 8
            d.rectangle([bx, gy1 - bh, bx + 22, gy1], fill=(110, 40, 40))
        for sx in (0.22, 0.5, 0.78):
            cx = M + railw * sx
            d.line([(cx, y0 + 6), (cx + 20, y0 + 26)], fill=(250, 220, 120), width=2)
            d.ellipse([cx + 17, y0 + 23, cx + 25, y0 + 31], fill=(250, 220, 120))
    tw = d.textlength(tag, font=F(SANS_B, 11)) + 12
    d.rectangle([M, gy1 - 18, M + tw, gy1], fill=BG)
    d.text((M + 6, gy1 - 15), tag, font=F(SANS_B, 11), fill=GOLD)
    d.text((M, gy1 + 4), kick, font=F(SANS_B, 10.5), fill=RED)
    y = block(M, gy1 + 18, head, F(SANS_B, 15.5), WHITE, railw, 1.05)
    block(M, y + 1, deck, F(SANS, 9.5), MUTED, railw, 1.1)

# ---------- right column: 10 brief cards, 2 cols x 5 rows ----------
cards = [
    ("19:24 CET", "4 MERCURY \u2022 SPACE", "BepiColombo reaches Mercury",
     "Thrusters fire tonight after an 8-year voyage. (ESA)"),
    ("WARSAW", "5 WARSAW \u2022 NATO", "Rutte flies to Warsaw for NATO talks",
     "Warsaw wants more NATO forces. (AP)"),
    ("239/1", "6 WELLINGTON \u2022 CRICKET", "India fight back at Wellington",
     "Rahul nears a century; India 239/1 at lunch. (Scorecard)"),
    ("TONIGHT", "7 LAS VEGAS \u2022 FORMULA 1", "Verstappen on pole in Las Vegas",
     "Antonelli fastest in qualifying but takes a grid penalty. (F1)"),
    ("M6.7", "8 PERU \u2022 QUAKE", "Magnitude 6.7 quake hits Peru",
     "Hit at 00:09 GMT near Junin; felt in Lima. (USGS)"),
    ("4 DEAD", "9 BAYELSA \u2022 DISASTER", "Nigeria funeral boat capsizes",
     "At least four dead in Bayelsa. (Reports)"),
    ("100,000", "10 LONDON \u2022 DEAL", "UK and EU seal a reset deal",
     "Youth mobility agreed: 100,000 visas a year. (AP)"),
    ("JURF", "11 IRAQ \u2022 WAR", "Iraqi forces retake Jurf al-Sakhar",
     "Troops retake town held since 2014. (Reports)"),
    ("31%", "12 SOUTH AFRICA \u2022 POLITICS", "ANC scrambles after worst result",
     "ANC wins 31%, its worst since 1994. (BBC)"),
    ("SEMI", "13 TURIN \u2022 TENNIS", "Medvedev meets Zverev tonight",
     "Beat Rune on Friday to reach the semi. (ATP)"),
]
cardw = (R - BODY_X - 10) / 2
for idx, (tag, kick, head, deck) in enumerate(cards):
    row, col = divmod(idx, 2)
    x0 = BODY_X + col * (cardw + 10)
    y0 = 278 + row * 64
    d.rectangle([x0, y0, x0 + cardw, y0 + 58], fill=PANEL, outline=PANEL_LINE, width=1)
    tw = d.textlength(tag, font=F(SANS_B, 10)) + 10
    d.rectangle([x0 + 6, y0 + 6, x0 + 6 + tw, y0 + 22], fill=GOLD)
    d.text((x0 + 11, y0 + 8), tag, font=F(SANS_B, 10), fill=BG)
    d.text((x0 + 12 + tw, y0 + 8), kick, font=F(SANS_B, 9), fill=RED)
    y = block(x0 + 8, y0 + 26, head, F(SANS_B, 12.5), WHITE, cardw - 16, 1.05)
    block(x0 + 8, y, deck, F(SANS, 8.8), MUTED, cardw - 16, 1.08)

# ---------- realistic world map (stories 1-13) ----------
# Simplified coastline polygons in (lon, lat), hardcoded from geographic
# knowledge; equirectangular projection onto the map box.
CONTINENTS = [
    # North America
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
    # South America
    [(-78, 7), (-76, 9), (-73, 11), (-70, 12), (-67, 11), (-64, 10), (-61, 9),
     (-58, 7), (-55, 6), (-52, 4), (-50, 0), (-47, -2), (-44, -3), (-40, -4),
     (-35, -8), (-37, -11), (-39, -14), (-39, -17), (-40, -20), (-42, -23),
     (-46, -24), (-49, -27), (-52, -30), (-54, -33), (-57, -35), (-58, -38),
     (-62, -39), (-63, -41), (-65, -43), (-65, -46), (-66, -48), (-67, -50),
     (-68, -52), (-68, -54), (-70, -54), (-72, -52), (-74, -48), (-74, -44),
     (-73, -40), (-73, -36), (-72, -32), (-71, -28), (-70, -24), (-70, -20),
     (-70, -18), (-73, -16), (-76, -14), (-77, -11), (-78, -8), (-80, -5),
     (-81, -3), (-81, 0), (-80, 2), (-78, 4)],
    # Africa
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
    # Europe
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
    # Asia (Siberia, Arabia, India, SE Asia)
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
    # Australia
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
    # Greenland
    [(-44, 60), (-41, 61), (-38, 63), (-34, 66), (-30, 68), (-26, 70),
     (-22, 71), (-20, 73), (-21, 75), (-24, 77), (-30, 79), (-38, 80),
     (-46, 80), (-53, 78), (-57, 76), (-58, 72), (-56, 68), (-54, 65),
     (-52, 62), (-50, 60), (-47, 60)],
    # Britain
    [(-5, 50), (-4, 51), (-3, 53), (-2, 54), (-3, 56), (-4, 58), (-6, 58),
     (-7, 57), (-7, 55), (-6, 53), (-5, 52)],
    # Ireland
    [(-10, 52), (-8, 52), (-6, 52), (-5, 54), (-6, 55), (-8, 55), (-10, 54)],
    # Iceland
    [(-22, 64), (-18, 63), (-15, 64), (-14, 65), (-16, 66), (-20, 66), (-22, 65)],
    # Cuba
    [(-85, 23), (-82, 23), (-79, 22), (-76, 21), (-74, 20), (-76, 20),
     (-79, 21), (-82, 22), (-85, 22)],
    # Japan
    [(130, 31), (131, 32), (132, 33), (134, 34), (135, 34), (136, 35),
     (137, 35), (138, 36), (139, 37), (140, 38), (141, 40), (141, 41),
     (142, 43), (143, 44), (141, 44), (140, 42), (140, 39), (139, 37),
     (138, 36), (136, 35), (134, 34), (132, 33), (131, 32)],
    # Madagascar
    [(44, -16), (46, -14), (48, -14), (50, -16), (50, -19), (48, -21),
     (47, -23), (46, -25), (45, -25), (44, -23), (43, -20), (43, -17)],
    # Sumatra
    [(95, 5), (97, 4), (99, 2), (101, 0), (103, -2), (104, -4), (105, -5),
     (103, -4), (101, -2), (99, 1), (97, 3)],
    # Java
    [(106, -6), (108, -6), (110, -7), (112, -7), (114, -8), (113, -8),
     (110, -8), (108, -7), (106, -7)],
    # Borneo
    [(109, 1), (111, 2), (114, 3), (116, 4), (118, 3), (119, 1), (118, -1),
     (116, -2), (114, -3), (112, -2), (110, -1)],
    # Sulawesi
    [(119, 0), (120, 1), (122, 0), (123, -1), (122, -3), (120, -4), (119, -2)],
    # New Guinea
    [(131, -1), (133, -2), (136, -2), (139, -3), (142, -4), (145, -5),
     (147, -7), (149, -9), (150, -10), (148, -9), (145, -8), (142, -7),
     (139, -6), (136, -4), (133, -3), (131, -2)],
    # Philippines
    [(120, 18), (121, 17), (122, 16), (121, 14), (122, 13), (121, 12),
     (122, 11), (123, 10), (122, 9), (121, 8), (122, 7), (123, 8),
     (123, 10), (124, 11), (123, 13), (122, 15), (121, 16)],
    # New Zealand, North Island
    [(173, -35), (175, -36), (177, -37), (178, -38), (176, -39), (175, -40),
     (174, -39), (173, -37)],
    # New Zealand, South Island
    [(167, -46), (169, -45), (171, -44), (172, -43), (173, -42), (172, -41),
     (171, -42), (170, -44), (168, -46)],
]

# Story pins 1-13 at true geographic locations (lon, lat). Story 4 is in space.
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

d.text((M, 608), "WHERE IT HAPPENED \u2014 STORIES 1\u201313", font=F(SANS_B, 13), fill=GOLD)
mx0, my0, mx1, my1 = M, 628, M + 520, 836
LAT_TOP, LAT_BOT = 83.0, -60.0


def proj(lon, lat):
    x = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
    y = my0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (my1 - my0)
    return x, y


# ocean shading: horizontal gradient bands, lighter toward the equator
for yy in range(my0, my1):
    t = (yy - my0) / (my1 - my0)
    if t < 0.5:
        f = t / 0.5
        col = tuple(int(OCEAN_TOP[c] + (OCEAN_MID[c] - OCEAN_TOP[c]) * f) for c in range(3))
    else:
        f = (t - 0.5) / 0.5
        col = tuple(int(OCEAN_MID[c] + (OCEAN_BOT[c] - OCEAN_MID[c]) * f) for c in range(3))
    d.line([(mx0, yy), (mx1, yy)], fill=col)

# graticule every 30 degrees
for lon in range(-180, 181, 30):
    x, _ = proj(lon, 0)
    d.line([(x, my0), (x, my1)], fill=GRAT, width=1)
for lat in range(-60, 84, 30):
    _, y = proj(0, lat)
    d.line([(mx0, y), (mx1, y)], fill=GRAT, width=1)
_, yeq = proj(0, 0)
for x in range(mx0, mx1, 10):
    d.line([(x, yeq), (x + 5, yeq)], fill=(90, 130, 175), width=1)

# land
for poly in CONTINENTS:
    pts = [proj(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND, outline=LAND_EDGE)

# pins
for n, (lon, lat) in PINS.items():
    cx, cy = proj(lon, lat)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=WHITE, width=1)
    center(cx - 8, cx + 8, cy - 6, str(n), F(SANS_B, 10), WHITE)
d.rectangle([mx0, my0, mx1, my1], outline=PANEL_LINE, width=1)
d.text((mx0 + 6, my1 - 16), "Red numbers mark stories 1\u201313. No. 4 is in space: Mercury.",
       font=F(SANS, 8.5), fill=(255, 170, 160))

# ---------- more stories (14-48) ----------
more = [
    "14 Tokyo: Frosty APEC greeting for Takaichi. (Asahi)",
    "15 Los Angeles: Palisades Fire arsonist convicted. (AP)",
    "16 Ottawa: US leadership in doubt, forum warns. (Forum)",
    "17 Brussels: EU-UK summit mends Brexit ties. (Reports)",
    "18 Kabul: UN warns ISIS-K gaining drones. (UN)",
    "19 Berlin: Students march against rearmament. (Reports)",
    "20 Brasilia: Indigenous land bill advances. (Reports)",
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
d.text((lx, 608), "35 MORE STORIES", font=F(SANS_B, 13), fill=GOLD)
colw = (R - lx - 10) / 2
half = (len(more) + 1) // 2
for c in range(2):
    x0 = lx + c * (colw + 10)
    y = 628
    for s in more[c * half:(c + 1) * half]:
        y = block(x0, y, s, F(SANS, 7.6), WHITE, colw, 1.02) + 0.8

# ---------- date check ----------
dy = 846
d.rectangle([M, dy, R, dy + 86], outline=GOLD, width=2)
d.text((M + 10, dy + 7), "DATE CHECK \u2713", font=F(SANS_B, 13), fill=GOLD)
block(M + 10, dy + 27,
      "Every story here happened, or was first reported, on Saturday 21 November 2026. LEFT OUT \u2014 other days' news: "
      "Russian missiles land in Poland (Fri 20 Nov) \u2022 Kyiv bridges hit (Fri 20 Nov) \u2022 Cyclone Akvan makes landfall "
      "(Fri 20 Nov) \u2022 ICJ Myanmar genocide ruling (Thu 19 Nov) \u2022 Virginia measles death announced (Fri 20 Nov) \u2022 "
      "Wall Street AI sell-off (Fri 20 Nov) \u2022 Shenzhen summit, Trump-Xi-Putin (Thu 19 Nov) \u2022 Anthropic debut, shares "
      "jump 17% (Thu 19 Nov) \u2022 GTA VI launch (Thu 19 Nov) \u2022 Starc's 7/58 \u2014 that was the 2025 Ashes, a year ago.",
      F(SANS, 9.5), WHITE, R - M - 20, 1.12)

d.text((M, 940), "Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Kyiv Post, USGS, ESA \u2022 Claims attributed, not stated as fact "
       "\u2022 Pictures and map: original, drawn in code \u2022 21 November 2026", font=F(SANS, 9), fill=MUTED)

img.save("entry.png", format="PNG", optimize=False)
print("wrote entry.png", img.size)

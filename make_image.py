#!/usr/bin/env python3
"""Draw entry.png for make.fun bounty news-image-20261121.

The artwork is a one-page newspaper front page summing up the world news of
Saturday 21 November 2026: a masthead naming the day, one lead story with a
drawn illustration, two mid-page stories, three lower stories and a row of
briefs. Everything is drawn with Pillow primitives (rectangles, lines,
polygons and text) — no photographs and no copied artwork.

Run:  python3 make_image.py   (writes entry.png beside this file)
The output is deterministic: same code, same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 40

PAPER = (247, 243, 234)
INK = (24, 24, 28)
NAVY = (20, 33, 61)
NAVY_LIGHT = (38, 58, 99)
CREAM = (244, 238, 222)
RED = (168, 32, 32)
GOLD = (150, 104, 8)
GREY = (90, 90, 96)
RULE = (40, 40, 46)
PANEL_BG = (233, 227, 211)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, s, f, fill, max_w, leading):
    """Draw wrapped text; returns the y just below the block."""
    for line in wrap(draw, s, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, s, color):
    draw.text((x, y), s, font=font(SANS_B, 21), fill=color)
    return y + 30


def story(draw, x, y, w, kick, kick_color, headline, head_size, body):
    y = kicker(draw, x, y, kick, kick_color)
    y = draw_block(draw, x, y, headline, font(SERIF_B, head_size), INK, w,
                   int(head_size * 1.12))
    y += 4
    y = draw_block(draw, x, y, body, font(SERIF, 22), (40, 40, 46), w, 27)
    return y


def hrule(draw, y, x0=MARGIN, x1=W - MARGIN, width=3, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_missile_panel(draw, x, y, w, h):
    """Simple drawn panel: a missile arc from the east to a burst over Poland."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=RULE, width=2)
    # ground line
    gy = y + h - 46
    draw.line([(x + 14, gy), (x + w - 14, gy)], fill=GREY, width=2)
    # launch point (east, right side)
    lx, ly = x + w - 44, gy - 6
    draw.polygon([(lx - 16, gy), (lx + 16, gy), (lx, gy - 26)], fill=NAVY_LIGHT)
    # arc (dotted) from launch to impact
    ix, iy = x + 70, gy - 88
    steps = 26
    for i in range(steps + 1):
        t = i / steps
        px = lx + (ix - lx) * t
        py = ly + (iy - ly) * t - 120 * 4 * t * (1 - t) * 0.55
        if i % 2 == 0:
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    # missile body near the top of the arc, angled down-left
    mx, my = x + w // 2 - 6, y + 52
    draw.polygon([(mx - 26, my + 8), (mx + 20, my - 12), (mx + 30, my - 4),
                  (mx - 14, my + 16)], fill=NAVY)
    draw.polygon([(mx + 20, my - 12), (mx + 34, my - 16), (mx + 30, my - 4)],
                 fill=RED)
    # starburst at impact
    import math
    for k in range(12):
        a = math.radians(k * 30)
        r = 26 if k % 2 == 0 else 15
        draw.line([(ix, iy), (ix + r * math.cos(a), iy + r * math.sin(a))],
                  fill=RED, width=4)
    draw.ellipse([ix - 7, iy - 7, ix + 7, iy + 7], fill=RED)
    # labels
    draw.text((x + 16, y + 12), "POLAND (NATO)", font=font(SANS_B, 20), fill=NAVY)
    draw.text((x + w - 122, gy - 34), "RUSSIA", font=font(SANS_B, 19), fill=NAVY)
    draw.text((x + 16, gy + 10), "NATO JETS SCRAMBLED", font=font(SANS_B, 19),
              fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((MARGIN, 18), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 56),
           fill=CREAM)
    d.text((MARGIN, 84),
           "Saturday · 21 November 2026 · World news of the day, summed up in one image",
           font=font(SANS, 22), fill=(205, 211, 226))
    d.rectangle([0, 118, W, 124], fill=RED)

    # --- Lead story -----------------------------------------------------
    y = 140
    lead_w = 620
    y2 = kicker(d, MARGIN, y, "CONFLICT · POLAND / UKRAINE", RED)
    y2 = draw_block(d, MARGIN, y2,
                    "Russian missile hits Poland amid 100-missile barrage",
                    font(SERIF_B, 48), INK, lead_w, 54)
    y2 += 4
    y2 = draw_block(d, MARGIN, y2,
                    "A Russian missile struck Polish territory overnight as some "
                    "100 missiles rained on Ukraine — Kyiv's bridges hit, at "
                    "least 12 killed. NATO jets scrambled.",
                    font(SERIF, 24), (40, 40, 46), lead_w, 30)
    panel_h = 200
    draw_missile_panel(d, MARGIN + lead_w + 24, y, W - MARGIN * 2 - lead_w - 24,
                       panel_h)
    y = max(y2, y + panel_h) + 12
    hrule(d, y)
    y += 16

    # --- Two mid-page stories -------------------------------------------
    col_w = (W - MARGIN * 2 - 36) // 2
    end_l = story(d, MARGIN, y, col_w,
                  "POLITICS · SHENZHEN", NAVY_LIGHT,
                  "Trump, Xi and Putin close summit; allies briefed on Ukraine", 32,
                  "The three leaders wrapped up their first three-way talks with "
                  "a joint declaration on UN reform, oil and nuclear risk. Trump "
                  "then briefed European allies on Ukraine.")
    end_r = story(d, MARGIN + col_w + 36, y, col_w,
                  "IRAN WAR · WASHINGTON", RED,
                  "'We've got time': Trump says Iran war runs into 2027", 32,
                  "Trump signalled the Iran war will stretch into next year as "
                  "the US weighs further strikes. The IEA warned there is no "
                  "going back to the energy world before the war.")
    y = max(end_l, end_r) + 12
    hrule(d, y)
    y += 16

    # --- Three lower stories --------------------------------------------
    col3_w = (W - MARGIN * 2 - 48) // 3
    ends = [
        story(d, MARGIN, y, col3_w,
              "ECONOMY · NEW YORK", GOLD,
              "Anthropic slides as tech sell-off deepens", 28,
              "Anthropic shares slid in a broad tech sell-off days after its "
              "blockbuster debut."),
        story(d, MARGIN + col3_w + 24, y, col3_w,
              "JUSTICE · THE HAGUE", NAVY_LIGHT,
              "Myanmar, China reject ICJ genocide ruling", 28,
              "Myanmar and China denounced the World Court's Rohingya "
              "ruling as unjust."),
        story(d, MARGIN + 2 * (col3_w + 24), y, col3_w,
              "DEFENCE · TOKYO–DELHI", NAVY_LIGHT,
              "Japan, India agree closer military ties", 28,
              "Tokyo and Delhi agreed deeper military and arms-industry "
              "cooperation."),
    ]
    y = max(ends) + 8
    hrule(d, y)
    y += 14

    # --- Briefs row -------------------------------------------------------
    briefs = [
        ("COP31", "UN climate talks reach crunch time."),
        ("SANA'A", "Coalition hits six Houthi missile workshops."),
        ("EL SALVADOR", "Bukele seeks a third term as president."),
        ("UFO FILES", "Pentagon releases more UFO footage."),
    ]
    bw = (W - MARGIN * 2 - 3 * 16) // 4
    bh = 84
    for i, (title, body) in enumerate(briefs):
        bx = MARGIN + i * (bw + 16)
        d.rectangle([bx, y, bx + bw, y + bh], outline=NAVY_LIGHT, width=2)
        d.text((bx + 10, y + 8), title, font=font(SANS_B, 19), fill=NAVY)
        draw_block(d, bx + 10, y + 34, body, font(SANS, 18), (40, 40, 46),
                   bw - 20, 22)

    # --- Footer -----------------------------------------------------------
    fy = H - 44
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((MARGIN, fy + 11),
           "21 NOVEMBER 2026 — ONE DAY, ONE PAGE   ·   Mood: tense   ·   Sources: AP, Reuters, BBC",
           font=font(SANS_B, 20), fill=CREAM)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size, "briefs end at", y + bh)


if __name__ == "__main__":
    main()

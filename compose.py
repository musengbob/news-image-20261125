#!/usr/bin/env python3
"""news-image-20261125 — front-page renderer.

Draws "THE WORLD TODAY", a dense 1024x1024 newspaper front page summing up
Wednesday 25 November 2026: 3 hero stories, 9 briefs, a 24-item numbered
list, a world map with story markers, a stat strip and a date-check box.

Everything on the page is drawn from the story data below with Pillow; the
output is fully deterministic (no clock, no randomness), so re-running this
script always produces the same bytes.

Usage: python3 compose.py   -> writes entry.png next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024

# --- palette -------------------------------------------------------------
PAPER = (246, 241, 229)
INK = (18, 18, 18)
RED = (176, 30, 30)
NAVY = (31, 58, 95)
GREY = (90, 86, 76)
LIGHT_RULE = (220, 212, 192)
OCEAN = (214, 228, 238)
LAND = (216, 200, 160)
LAND_EDGE = (150, 128, 92)
BODY = (40, 38, 34)
PICTO = (245, 242, 233)

# --- fonts ---------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, size):
    """DejaVu from the system font dir, falling back to Pillow's default."""
    path = os.path.join(FONT_DIR, filename)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def load_serif_italic(size):
    """Serif italic if installed, otherwise plain serif."""
    name = "DejaVuSerif-Italic.ttf"
    if not os.path.exists(os.path.join(FONT_DIR, name)):
        name = "DejaVuSerif.ttf"
    return load_font(name, size)


MASTHEAD = load_font("DejaVuSerif-Bold.ttf", 56)
DATELINE = load_font("DejaVuSans-Bold.ttf", 15)
TICKER = load_serif_italic(13)
STAT_NUM = load_font("DejaVuSerif-Bold.ttf", 21)
STAT_LBL = load_font("DejaVuSans.ttf", 10)
COUNTS = load_font("DejaVuSans-Bold.ttf", 11)
KICKER = load_font("DejaVuSans-Bold.ttf", 11)
HERO_HEAD = load_font("DejaVuSerif-Bold.ttf", 19)
HERO_DECK = load_font("DejaVuSans.ttf", 11)
BRIEF_KICK = load_font("DejaVuSans-Bold.ttf", 10)
BRIEF_HEAD = load_font("DejaVuSans-Bold.ttf", 12)
BRIEF_DECK = load_font("DejaVuSans.ttf", 10)
SECTION = load_font("DejaVuSans-Bold.ttf", 13)
MAP_TITLE = load_font("DejaVuSans-Bold.ttf", 12)
MAP_CAP = load_font("DejaVuSans.ttf", 9)
CHECK_TITLE = load_font("DejaVuSans-Bold.ttf", 12)
CHECK_BODY = load_font("DejaVuSans.ttf", 11)
CHECK_FOOT = load_serif_italic(10)
LIST_NUM = load_font("DejaVuSans-Bold.ttf", 11)
FOOTER = load_font("DejaVuSans.ttf", 10)

# --- story data ----------------------------------------------------------
# (kicker, headline, deck, artwork key)
HEROES = [
    ("WASHINGTON \u00b7 TARIFFS",
     "Trump readies sweeping new tariffs",
     "Findings of a probe into excess factory capacity in 16 trading "
     "partners are due any hour; new duties would stack on top of "
     "existing tariffs.",
     "tariff"),
    ("NEW YORK \u00b7 NVIDIA",
     "Nvidia bounce fades, shares slide 6%",
     "The relief rally fizzles as the attorney general dodges questions "
     "on Trump's intervention; Huang said he violated the code of conduct.",
     "fall"),
    ("GAZA",
     "Israeli strike kills Hamas security chief",
     "An air strike kills Hamas's internal security chief in Gaza as the "
     "war's toll mounts.",
     "blast"),
]

# (pictogram, kicker, headline, deck)
BRIEFS = [
    ("flag", "BEIJING", "China probes Politburo member",
     "Shanghai party chief Chen Jining is under investigation, Xinhua says."),
    ("bolt", "CANBERRA", "Australia apologises to LGBTQ veterans",
     "Canberra issues a formal apology for decades of military discrimination."),
    ("bolt", "BEIJING", "China flies Pakistani astronaut",
     "A Pakistani astronaut flies on a historic Chinese space mission."),
    ("target", "WASHINGTON", "US confidence at near 2-year high",
     "Consumer confidence jumps to 103.3, its highest since January 2025."),
    ("waves", "CARACAS", "Citi weighs return to Venezuela",
     "Citigroup considers resuming banking five years after its exit."),
    ("flag", "PARIS", "Sarkozy and wife to face trial",
     "The former French president and Carla Bruni are to face trial."),
    ("waves", "KINSHASA", "DR Congo plane missing",
     "A military aircraft is missing as rebels claim to have shot it down."),
    ("flag", "ABUJA", "Nigerian monarch, 92, suspended",
     "A 92-year-old monarch is suspended after sexual assault claims."),
    ("target", "IOWA", "US Army to detonate toxic explosives",
     "The Army will go ahead with detonating the lead azide stockpile."),
]

# Items 13-36, drawn in three columns (13, 16, 19, ... down column one).
NUMBERED = [
    "Gold ticks lower ahead of US inflation data",
    "Japan's Nikkei to rise, but short of record",
    "Mexico inflation hits six-month high",
    "German business morale rises",
    "Huawei guilty of stealing trade secrets",
    "US farm chief vows to fight court order",
    "Thomas Markle indicted in US",
    "North Koreans 'spied on, beaten, jailed'",
    "Land mine casualties soar in Syria",
    "NATO chief vows space defence",
    "Zimbabwean jailed over Ukraine fight bid",
    "Senegal reinstated as Afcon winners",
    "US court unseals Ilhan Omar records",
    "California Democrat to resign",
    "Two held over royal home burglary",
    "Hasina plans return on 16 December",
    "China AI fakes smear Taiwan candidates",
    "India's food inflation broadening",
    "Russia's own figures: ~500,000 war deaths",
    "Pope diary: 'I saw the devil'",
    "Compass to shift listing to US",
    "Microsoft declares 'Code Red'",
    "Trump pardons turkeys Freedom and Feathers",
    "Car bomb wounds more than 20 in Colombia",
]

# (big number, label) across the stat strip.
STAT_STRIP = [
    ("16", "partners face new tariffs"),
    ("6%", "Nvidia slide as bounce fades"),
    ("103.3", "US consumer confidence"),
    ("$3,544", "gold per ounce"),
    ("3.96%", "Mexico annual inflation"),
    ("90.6", "German Ifo index"),
]

DATE_CHECK_ITEMS = [
    "Nvidia reinstates Huang as CEO \u2014 Mon 23 Nov",
    "Democrats win largest House majority \u2014 Tue 24 Nov",
    "CrowdStrike buys Zscaler, $44bn \u2014 Mon 23 Nov",
    "Indonesia factory fire kills 24 \u2014 Tue 24 Nov",
    "COP31 talks collapse, no deal \u2014 Sun 22 Nov",
]

# --- world map data ------------------------------------------------------
# Rough stylised continents as (lon, lat) outlines.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 68), (-95, 69),
     (-85, 66), (-80, 62), (-65, 60), (-55, 52), (-60, 46), (-70, 43),
     (-75, 38), (-80, 32), (-81, 26), (-86, 21), (-92, 15), (-97, 16),
     (-97, 26), (-105, 20), (-110, 23), (-117, 32), (-124, 40),
     (-124, 48), (-135, 58), (-152, 58), (-162, 55), (-168, 60)],
    [(-58, 64), (-45, 60), (-32, 64), (-22, 70), (-30, 74), (-45, 76),
     (-58, 76), (-62, 70)],
    [(-80, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -9), (-38, -15), (-41, -22), (-48, -27), (-55, -34),
     (-62, -39), (-68, -46), (-70, -52), (-73, -50), (-73, -40),
     (-72, -20), (-77, -12), (-81, -4), (-80, 4)],
    [(-17, 15), (-16, 20), (-10, 30), (-6, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (33, 27), (37, 22), (40, 15),
     (44, 11), (51, 11), (48, 2), (41, -4), (40, -10), (36, -18),
     (33, -26), (28, -33), (20, -35), (16, -29), (13, -18), (12, -8),
     (9, -1), (9, 4), (4, 6), (-8, 5), (-15, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (-1, 50), (3, 52), (7, 54),
     (8, 57), (10, 59), (13, 56), (18, 56), (21, 55), (24, 58),
     (28, 59), (30, 62), (26, 65), (22, 70), (16, 70), (12, 67),
     (6, 62), (5, 58), (-1, 57), (-5, 50), (-9, 43)],
    [(30, 62), (40, 68), (55, 68), (68, 70), (85, 73), (105, 76),
     (125, 72), (145, 71), (160, 69), (178, 65), (170, 60), (162, 56),
     (156, 51), (150, 45), (142, 44), (140, 39), (135, 34), (130, 33),
     (127, 35), (122, 31), (120, 25), (112, 21), (108, 18), (105, 9),
     (100, 7), (98, 14), (96, 16), (92, 21), (88, 22), (85, 19),
     (80, 13), (77, 8), (74, 15), (70, 21), (66, 25), (61, 25),
     (57, 26), (54, 26), (50, 29), (48, 30), (44, 29), (40, 32),
     (36, 36), (33, 36), (30, 36), (27, 37), (26, 40)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (126, -32),
     (132, -32), (137, -35), (140, -38), (146, -39), (150, -37),
     (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
     (132, -11), (126, -14), (122, -17), (117, -20), (113, -22)],
]

# (lon, lat) of the stories the map marks with red dots.
MARKERS = [
    (-77.0, 38.9), (-74.0, 40.7), (34.5, 31.5), (116.4, 39.9),
    (149.1, -35.3), (2.35, 48.85), (15.3, -4.3), (7.5, 9.06),
    (-66.9, 10.5), (-99.1, 19.4), (13.4, 52.5), (-0.1, 51.5),
]

# --- drawing helpers -----------------------------------------------------


def wrap_text(text, font, max_width, draw):
    """Greedy word wrap: pack as many words per line as fit in max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, lines, font, fill, leading):
    """Draw stacked lines, advancing y by leading each time; return new y."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, weight=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def centred(draw, text, font, y, fill):
    """Draw text centred on the page at height y."""
    x = (PAGE_W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


def pictogram(draw, kind, x, y, size=30):
    """Small white pictogram on a navy square (brief-grid icons)."""
    draw.rectangle([x, y, x + size, y + size], fill=NAVY)
    cx, cy = x + size / 2, y + size / 2
    if kind == "flag":
        draw.line([(x + 9, y + 5), (x + 9, y + 25)], fill=PICTO, width=2)
        draw.polygon([(x + 9, y + 5), (x + 23, y + 9), (x + 9, y + 14)],
                     fill=PICTO)
    elif kind == "bolt":
        draw.polygon([(x + 17, y + 4), (x + 9, y + 17), (x + 14, y + 17),
                      (x + 12, y + 26), (x + 21, y + 12), (x + 16, y + 12)],
                     fill=PICTO)
    elif kind == "waves":
        for wy in (11, 17, 23):
            draw.arc([x + 6, y + wy - 4, x + 24, y + wy + 4], 200, 340,
                     fill=PICTO, width=2)
    elif kind == "target":
        draw.ellipse([x + 7, y + 7, x + 23, y + 23], outline=PICTO, width=2)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=PICTO)
    else:
        draw.ellipse([x + 7, y + 7, x + 23, y + 23], outline=PICTO, width=2)
        draw.line([(x + 7, cy), (x + 23, cy)], fill=PICTO, width=1)


def hero_artwork(draw, kind, x, y, w, h):
    """Flat illustration panel topping a hero story."""
    if kind == "tariff":
        # Steel-blue port panel: stacked shipping containers and a big %.
        draw.rectangle([x, y, x + w, y + h], fill=(24, 52, 78))
        draw.rectangle([x, y + h - 16, x + w, y + h], fill=(14, 34, 54))
        cols = [(176, 30, 30), (200, 130, 30), (24, 110, 62),
                (176, 30, 30), (200, 130, 30)]
        for i, c in enumerate(cols):
            bx = x + 14 + i * 52
            draw.rectangle([bx, y + 52, bx + 46, y + 76], fill=c,
                           outline=PICTO, width=1)
            for rib in range(1, 5):
                draw.line([(bx + rib * 9, y + 52), (bx + rib * 9, y + 76)],
                          fill=(0, 0, 0), width=1)
        for i, c in enumerate(cols[:3]):
            bx = x + 40 + i * 52
            draw.rectangle([bx, y + 26, bx + 46, y + 50], fill=c,
                           outline=PICTO, width=1)
        draw.text((x + w - 78, y + 2), "%", font=load_font("DejaVuSans-Bold.ttf", 44),
                  fill=(250, 220, 120))
        draw.line([(x + 14, y + 80), (x + w - 14, y + 80)], fill=PICTO, width=2)
    elif kind == "fall":
        # Dark green market panel: a chip on the left, a falling chart right.
        draw.rectangle([x, y, x + w, y + h], fill=(18, 58, 38))
        draw.rectangle([x + 18, y + 22, x + 66, y + 66], fill=(24, 110, 62),
                       outline=PICTO, width=2)
        draw.rectangle([x + 30, y + 34, x + 54, y + 54], fill=(18, 58, 38))
        for px in (30, 42, 54):
            draw.line([(x + px, y + 14), (x + px, y + 22)], fill=PICTO, width=2)
            draw.line([(x + px, y + 66), (x + px, y + 74)], fill=PICTO, width=2)
        for py in (34, 46, 58):
            draw.line([(x + 10, y + py), (x + 18, y + py)], fill=PICTO, width=2)
            draw.line([(x + 66, y + py), (x + 74, y + py)], fill=PICTO, width=2)
        pts = [(x + 84, y + 14), (x + 120, y + 22), (x + 150, y + 18),
               (x + 185, y + 38), (x + 215, y + 34), (x + 250, y + 56),
               (x + 288, y + 68)]
        draw.line(pts, fill=(240, 90, 70), width=4)
        draw.polygon([(x + 288, y + 68), (x + 276, y + 66), (x + 284, y + 56)],
                     fill=(240, 90, 70))
        draw.text((x + 240, y + h - 18), "-6%", font=STAT_NUM,
                  fill=(240, 90, 70))
    elif kind == "blast":
        # Night skyline panel: dark towers, an orange blast flash, smoke.
        draw.rectangle([x, y, x + w, y + h], fill=(26, 26, 34))
        draw.rectangle([x, y + h - 14, x + w, y + h], fill=(14, 14, 18))
        for bx, bw, bh in [(14, 52, 44), (78, 44, 62), (134, 58, 38),
                           (204, 46, 54), (262, 44, 30)]:
            draw.rectangle([x + bx, y + h - 14 - bh, x + bx + bw, y + h - 14],
                           fill=(52, 52, 62))
            for wy in range(3):
                for wx in range(2):
                    draw.rectangle(
                        [x + bx + 8 + wx * 20, y + h - 14 - bh + 8 + wy * 14,
                         x + bx + 14 + wx * 20, y + h - 14 - bh + 14 + wy * 14],
                        fill=(240, 200, 90))
        # blast flash over the middle towers
        fx0, fy = x + 150, y + h - 14 - 62
        draw.polygon([(fx0, fy + 46), (fx0 + 16, fy), (fx0 + 32, fy + 46)],
                     fill=(240, 120, 30))
        draw.polygon([(fx0 + 8, fy + 46), (fx0 + 16, fy + 16),
                      (fx0 + 24, fy + 46)], fill=(250, 220, 120))
        draw.ellipse([fx0 - 26, fy - 6, fx0 + 58, fy + 22], fill=(250, 200, 90))
        for i in range(8):
            draw.ellipse([x + 20 + i * 34, y + 6 + (i * 5) % 10,
                          x + 28 + i * 34, y + 14 + (i * 5) % 10],
                         fill=(130, 130, 140))
    else:
        draw.rectangle([x, y, x + w, y + h], fill=OCEAN)

# --- page build ----------------------------------------------------------


def build_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 26
    left, right = margin, PAGE_W - margin
    y = 18

    # -- masthead ---------------------------------------------------------
    centred(d, "THE WORLD TODAY", MASTHEAD, y, INK)
    y += 64
    rule(d, left, right, y, 3)
    y += 8
    centred(d, "WEDNESDAY 25 NOVEMBER 2026  \u00b7  36 STORIES FROM AROUND THE WORLD",
            DATELINE, y, RED)
    y += 22
    centred(d, "Trump readies new tariffs  \u00b7  Nvidia bounce fades  \u00b7  "
               "Israeli strike kills Hamas chief  \u00b7  Gold $3,544", TICKER, y, INK)
    y += 20
    rule(d, left, right, y, 1)
    y += 6

    # -- stat strip -------------------------------------------------------
    cell_w = (right - left) / 6
    for i, (number, label) in enumerate(STAT_STRIP):
        cx = left + i * cell_w
        d.text((cx + (cell_w - d.textlength(number, font=STAT_NUM)) / 2, y),
               number, font=STAT_NUM, fill=NAVY)
        d.text((cx + (cell_w - d.textlength(label, font=STAT_LBL)) / 2, y + 26),
               label, font=STAT_LBL, fill=GREY)
        if i:
            d.line([(cx, y + 2), (cx, y + 40)], fill=LIGHT_RULE, width=1)
    y += 48
    rule(d, left, right, y, 1)
    y += 5
    centred(d, "ASIA-PACIFIC 10  \u00b7  EUROPE 7  \u00b7  AMERICAS 13  \u00b7  "
               "MIDDLE EAST 2  \u00b7  AFRICA 4", COUNTS, y, NAVY)
    y += 17
    rule(d, left, right, y, 3)
    y += 10

    # -- three hero stories ----------------------------------------------
    col_w = int((right - left - 24) / 3)
    art_h = 88
    for i, (kicker, headline, deck, art) in enumerate(HEROES):
        hx = left + i * (col_w + 12)
        hero_artwork(d, art, hx, y, col_w, art_h)
        yy = y + art_h + 6
        d.text((hx, yy), kicker, font=KICKER, fill=RED)
        yy += 15
        head_lines = wrap_text(headline, HERO_HEAD, col_w, d)[:2]
        yy = draw_wrapped(d, hx, yy, head_lines, HERO_HEAD, INK, 22)
        deck_lines = wrap_text(deck, HERO_DECK, col_w, d)[:3]
        draw_wrapped(d, hx, yy + 2, deck_lines, HERO_DECK, BODY, 14)
    y += art_h + 6 + 15 + 44 + 2 + 42 + 8

    # -- the day in brief (3 x 3) -----------------------------------------
    rule(d, left, right, y, 2)
    y += 7
    d.text((left, y), "THE DAY IN BRIEF", font=SECTION, fill=INK)
    tail = "9 MORE STORIES"
    d.text((right - d.textlength(tail, font=SECTION), y), tail,
           font=SECTION, fill=RED)
    y += 20
    cell_h = 58
    for row in range(3):
        for col in range(3):
            kind, kicker, headline, deck = BRIEFS[row * 3 + col]
            bx = left + col * (col_w + 12)
            by = y + row * cell_h
            pictogram(d, kind, bx, by + 2)
            tx = bx + 38
            tw = col_w - 38
            d.text((tx, by), kicker, font=BRIEF_KICK, fill=RED)
            head_lines = wrap_text(headline, BRIEF_HEAD, tw, d)[:1]
            yy = draw_wrapped(d, tx, by + 13, head_lines, BRIEF_HEAD, INK, 15)
            deck_lines = wrap_text(deck, BRIEF_DECK, tw, d)[:2]
            draw_wrapped(d, tx, yy + 1, deck_lines, BRIEF_DECK, BODY, 13)
    y += 3 * cell_h + 6

    # -- world map + date check -------------------------------------------
    rule(d, left, right, y, 2)
    y += 8
    map_h = 152
    map_w = 636
    d.rectangle([left, y, left + map_w, y + map_h], fill=OCEAN,
                outline=INK, width=1)
    d.text((left + 8, y + 5), "WHERE IT HAPPENED", font=MAP_TITLE, fill=NAVY)

    def project(lon, lat):
        px = left + (lon + 170) / 360.0 * map_w
        py = y + 16 + (75 - lat) / 132.0 * (map_h - 28)
        return (px, py)

    for polygon in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in polygon],
                  fill=LAND, outline=LAND_EDGE)
    for lon, lat in MARKERS:
        mx, my = project(lon, lat)
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
    d.text((left + 8, y + map_h - 16), "RED DOTS MARK THE STORY LOCATIONS",
           font=MAP_CAP, fill=NAVY)

    check_x = left + map_w + 12
    check_w = right - check_x
    d.rectangle([check_x, y, check_x + check_w, y + map_h],
                outline=RED, width=2)
    d.text((check_x + 10, y + 7), "DATE CHECK", font=CHECK_TITLE, fill=RED)
    d.text((check_x + 10, y + 24),
           "NOT WEDNESDAY'S NEWS \u2014 LEFT OUT ON PURPOSE:",
           font=CHECK_BODY, fill=INK)
    yy = y + 42
    for item in DATE_CHECK_ITEMS:
        d.text((check_x + 10, yy), "\u2022  " + item, font=CHECK_BODY, fill=BODY)
        yy += 16
    d.text((check_x + 10, y + map_h - 18),
           "Only 25 November stories appear above.", font=CHECK_FOOT, fill=GREY)
    y += map_h + 8

    # -- numbered list 13-36 ----------------------------------------------
    rule(d, left, right, y, 2)
    y += 7
    d.text((left, y), "ALSO ON WEDNESDAY 25 NOVEMBER", font=SECTION, fill=INK)
    y += 20
    row_h = 19
    for idx, headline in enumerate(NUMBERED):
        row, col = divmod(idx, 3)
        nx = left + col * (col_w + 12)
        ny = y + row * row_h
        number = "%d." % (idx + 13)
        d.text((nx, ny), number, font=LIST_NUM, fill=RED)
        num_w = d.textlength(number + " ", font=LIST_NUM)
        lines = wrap_text(headline, LIST_NUM, col_w - num_w, d)
        assert len(lines) == 1, "numbered headline wraps: %r -> %r" % (headline, lines)
        d.text((nx + num_w, ny), lines[0], font=LIST_NUM, fill=INK)
    y += 8 * row_h + 4

    # -- footer -----------------------------------------------------------
    rule(d, left, right, y, 1)
    y += 6
    d.text((left, y), "Sources: Reuters \u00b7 BBC \u00b7 Bloomberg \u00b7 Xinhua "
                      "\u00b7 INEGI \u00b7 Ifo Institute", font=FOOTER, fill=GREY)
    y += 14
    d.text((left, y), "All stories happened, or were first reported, on "
                      "Wednesday 25 November 2026 in some time zone. Figures "
                      "as reported that day.", font=FOOTER, fill=GREY)
    y += 14
    print("final y =", y, "(canvas 1024)")
    img.save(OUT_PATH, "PNG", optimize=True)
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    build_page()

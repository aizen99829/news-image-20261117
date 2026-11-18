#!/usr/bin/env python3
"""Render the news-image-20261117 poster (1024x1024, deterministic, PIL only).

Layout (1024x1024):
  masthead  0-112    "THE WORLD IN ONE DAY" + TUESDAY 17 NOVEMBER 2026
  hero img  112-372  procedural Kerch Bridge collapse scene
  hero text 372-500  headline + 2 sub-caption lines
  grid      500-848  2x2 story panels (Iran / Nvidia / Measles / Trump)
  strip     848-1024 ALSO TODAY, 4 one-line items

All facts checked against RESEARCH.md. No randomness, no time, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (246, 241, 231)
INK = (22, 24, 28)
RED = (163, 22, 33)
RED_DK = (122, 14, 24)
GREY = (90, 96, 104)
SKY_TOP = (38, 52, 68)
SKY_BOT = (96, 110, 126)
SEA = (18, 46, 66)
SEA_LT = (46, 96, 120)
STEEL = (28, 38, 48)
STEEL_LT = (70, 84, 98)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def fit_font(draw, text, fname, start, max_w):
    """Largest font size <= start whose text fits max_w."""
    size = start
    while size > 8:
        f = font(fname, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(fname, 8)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked_text(draw, xy, text, f, fill, tracking=4):
    """Draw text with extra letter spacing; returns total width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x - xy[0] - tracking


def vgrad(draw, box, top, bot):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    d.rectangle([0, 0, W, 112], fill=PAPER)
    small = font(SANS_B, 25)
    label = "THE WORLD IN ONE DAY"
    tw = sum(d.textlength(c, font=small) for c in label) + 4 * (len(label) - 1)
    tracked_text(d, ((W - tw) // 2, 12), label, small, RED, tracking=4)
    date_f = fit_font(d, "TUESDAY 17 NOVEMBER 2026", SERIF_B, 62, 980)
    dw = d.textlength("TUESDAY 17 NOVEMBER 2026", font=date_f)
    d.text(((W - dw) // 2, 42), "TUESDAY 17 NOVEMBER 2026",
           font=date_f, fill=INK)
    d.line([(24, 108), (W - 24, 108)], fill=RED, width=4)


# ---------------------------------------------------------------- hero art
def draw_hero_art(d):
    x0, y0, x1, y1 = 0, 112, W, 372
    vgrad(d, (x0, y0, x1, y1), SKY_TOP, SKY_BOT)
    # faint clouds, kept small and high so they never touch the bridge
    for cx, cy, r in [(180, 138, 40), (760, 136, 44), (540, 128, 22)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                  fill=(128, 140, 154))
    # sea
    d.rectangle([x0, 300, x1, y1], fill=SEA)
    for wy in (312, 328, 346, 360):
        for sx in range(0, W, 64):
            d.arc([sx, wy, sx + 44, wy + 12], 200, 340, fill=SEA_LT, width=2)
    # bridge deck (road) across the whole width, with a GAP in the middle
    deck_y = 252
    d.rectangle([0, deck_y, 380, deck_y + 14], fill=STEEL)
    d.rectangle([644, deck_y, W, deck_y + 14], fill=STEEL)
    d.rectangle([0, deck_y, 380, deck_y + 4], fill=(150, 164, 180))
    d.rectangle([644, deck_y, W, deck_y + 4], fill=(150, 164, 180))
    # piers
    for px in (120, 330, 694, 904):
        d.rectangle([px - 9, deck_y + 14, px + 9, 300], fill=STEEL)
    # standing arches: left span and right span, bold and bright
    for ax0, ax1 in ((30, 350), (674, 994)):
        d.arc([ax0, deck_y - 112, ax1, deck_y + 44], 180, 360,
              fill=(128, 146, 164), width=13)
        for vx in range(ax0 + 34, ax1 - 24, 40):
            d.line([(vx, deck_y - 42), (vx, deck_y)], fill=(128, 146, 164),
                   width=4)
    # COLLAPSED middle span: broken arch halves plunging into the sea,
    # plus a tilted deck fragment falling between them
    d.line([(384, deck_y - 2), (468, 320)], fill=(128, 146, 164), width=13)
    d.line([(640, deck_y - 2), (556, 320)], fill=(128, 146, 164), width=13)
    d.line([(384, deck_y - 2), (452, 298)], fill=(150, 164, 180), width=6)
    d.line([(640, deck_y - 2), (572, 298)], fill=(150, 164, 180), width=6)
    # tilted falling deck fragment
    d.polygon([(452, 288), (572, 300), (568, 312), (448, 300)],
              fill=STEEL)
    d.polygon([(452, 288), (572, 300), (570, 303), (452, 291)],
              fill=(150, 164, 180))
    # falling debris
    for dx, dy, dw, dh in [(470, 322, 26, 8), (512, 336, 34, 9),
                           (556, 326, 22, 7), (496, 306, 18, 6)]:
        d.rectangle([dx, dy, dx + dw, dy + dh], fill=(150, 164, 180))
    # splash at impact
    for sx, sy, r in [(512, 330, 34), (482, 334, 20), (544, 334, 20)]:
        d.arc([sx - r, sy - r // 2, sx + r, sy + r // 2], 180, 360,
              fill=(220, 232, 238), width=5)
    # smoke above the break
    for cx, cy, r in [(498, 252, 18), (524, 240, 22), (512, 226, 14)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 176, 184))
    # BREAKING tag
    tag = "BREAKING"
    tf = font(SANS_B, 24)
    tw = d.textlength(tag, font=tf) + 28
    d.rectangle([24, 128, 24 + tw, 166], fill=RED)
    d.text((38, 133), tag, font=tf, fill=(255, 255, 255))


def draw_hero_text(d):
    d.rectangle([0, 372, W, 500], fill=PAPER)
    hf = fit_font(d, "KERCH BRIDGE COLLAPSES", SERIF_B, 58, 980)
    hw = d.textlength("KERCH BRIDGE COLLAPSES", font=hf)
    d.text(((W - hw) // 2, 380), "KERCH BRIDGE COLLAPSES", font=hf, fill=INK)
    sf = font(SANS, 25)
    # two sub-caption lines at y=440 and y=470
    for i, line in enumerate([
            "Road arch falls into the sea; rail runs on one track.",
            "Hours earlier, Russia hit Kyiv's North & South bridges."]):
        lw = d.textlength(line, font=sf)
        d.text(((W - lw) // 2, 440 + i * 30), line, font=sf, fill=(52, 56, 62))


# ---------------------------------------------------------------- panels
PANELS = [
    dict(bg=(253, 238, 218), accent=(176, 92, 20), icon="drone",
         head="IRAN DRONES TARGET US BASE",
         sub="Intercepted over Bahrain \u2014 no damage."),
    dict(bg=(230, 244, 230), accent=(24, 120, 52), icon="chart",
         head="NVIDIA: $115.8BN, UP 103%",
         sub="Record Q3; Huang not reinstated."),
    dict(bg=(253, 232, 232), accent=(163, 22, 33), icon="virus",
         head="US LOSES MEASLES-FREE STATUS",
         sub="5,412 cases \u2014 most since 1991."),
    dict(bg=(232, 238, 252), accent=(28, 64, 140), icon="heads",
         head="TRUMP IN MANILA",
         sub="Quad summit; then Shenzhen, then Xi & Putin."),
]


def icon_drone(d, cx, cy):
    # quadcopter drone with a red interception ring
    d.ellipse([cx - 22, cy - 12, cx + 22, cy + 12], fill=INK)
    for sx, sy in ((-34, -20), (34, -20), (-34, 20), (34, 20)):
        d.line([(cx, cy), (cx + sx, cy + sy)], fill=INK, width=4)
        d.ellipse([cx + sx - 16, cy + sy - 4, cx + sx + 16, cy + sy + 4],
                  outline=INK, width=3)
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=RED, width=5)
    d.line([(cx - 37, cy + 37), (cx + 37, cy - 37)], fill=RED, width=5)


def icon_chart(d, cx, cy):
    bars = [(cx - 44, 34), (cx - 12, 52), (cx + 20, 72)]
    for bx, bh in bars:
        d.rectangle([bx, cy + 40 - bh, bx + 24, cy + 40], fill=(24, 120, 52))
    d.line([(cx - 52, cy + 28), (cx - 28, cy - 2), (cx + 4, cy - 18),
            (cx + 52, cy - 44)], fill=(24, 120, 52), width=5)
    d.polygon([(cx + 52, cy - 44), (cx + 34, cy - 44), (cx + 52, cy - 26)],
              fill=(24, 120, 52))


def icon_virus(d, cx, cy):
    import math
    for k in range(10):
        a = math.radians(k * 36)
        x1, y1 = cx + int(30 * math.cos(a)), cy + int(30 * math.sin(a))
        x2, y2 = cx + int(46 * math.cos(a)), cy + int(46 * math.sin(a))
        d.line([(x1, y1), (x2, y2)], fill=RED_DK, width=5)
        d.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=RED_DK)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=RED)
    for dx, dy in ((-12, -8), (10, 6), (-4, 12)):
        d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                  fill=(255, 255, 255))


def icon_heads(d, cx, cy):
    cols = [(28, 64, 140), (163, 22, 33), (176, 132, 20)]
    for i, c in enumerate(cols):
        hx = cx - 36 + i * 36
        d.ellipse([hx - 15, cy - 34, hx + 15, cy - 4], fill=c)
        d.polygon([(hx - 24, cy + 40), (hx + 24, cy + 40),
                   (hx + 14, cy + 2), (hx - 14, cy + 2)], fill=c)


ICONS = {"drone": icon_drone, "chart": icon_chart,
         "virus": icon_virus, "heads": icon_heads}


def draw_grid(d):
    for i, p in enumerate(PANELS):
        px, py = (i % 2) * 512, 500 + (i // 2) * 174
        d.rectangle([px, py, px + 512, py + 174], fill=p["bg"])
        d.rectangle([px, py, px + 10, py + 174], fill=p["accent"])
        d.line([(px, py), (px + 512, py)], fill=(255, 255, 255), width=2)
        d.line([(px, py), (px, py + 174)], fill=(255, 255, 255), width=2)
        ICONS[p["icon"]](d, px + 78, py + 87)
        tx = px + 150
        maxw = 512 - 150 - 16
        hf = font(SERIF_B, 27)
        lines = wrap(d, p["head"], hf, maxw)
        y = py + 18
        for ln in lines[:2]:
            d.text((tx, y), ln, font=hf, fill=INK)
            y += 33
        sf = font(SANS, 22)
        for ln in wrap(d, p["sub"], sf, maxw)[:2]:
            d.text((tx, y + 4), ln, font=sf, fill=(52, 56, 62))
            y += 28


# ---------------------------------------------------------------- strip
ALSO = [
    "Pentagon fails 9th audit \u2014 $4.8 trillion unverified.",
    "Russian An-12 crashes in Siberia \u2014 19 dead.",
    "UK sanctions 8 West Bank settlement firms.",
    "Japan scrambles jets \u2014 suspected Russian planes.",
]


def draw_strip(d):
    d.rectangle([0, 848, W, H], fill=INK)
    lf = font(SANS_B, 24)
    d.text((24, 860), "ALSO TODAY", font=lf, fill=(255, 255, 255))
    d.line([(24, 894), (W - 24, 894)], fill=RED, width=3)
    sf = font(SANS, 22)
    y = 904
    for item in ALSO:
        d.rectangle([24, y + 8, 34, y + 18], fill=RED)
        d.text((46, y), item, font=sf, fill=(238, 238, 238))
        y += 30


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_hero_art(d)
    draw_hero_text(d)
    draw_grid(d)
    draw_strip(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "assets", "poster.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()

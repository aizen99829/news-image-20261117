#!/usr/bin/env python3
"""Render the news-image-20261117 poster (1024x1024, deterministic, PIL only).

R2 revision of the R1 poster ("The World in One Day", Tuesday 17 Nov 2026).
Changes vs R1 (see BUILD-R2.md): hero redrawn (tall pointed white arches,
towers/piers, much bigger falling deck + splash, one clear smoke plume,
BREAKING moved over the gap); panel subs cut to one short line at 28px;
Trump panel rewritten (Thu trilateral + Manila->Shenzhen route arrow);
ALSO TODAY cut 4 -> 3 items at 27px; word count ~99 -> 83.

Layout (1024x1024):
  masthead  0-112    "THE WORLD IN ONE DAY" + TUESDAY 17 NOVEMBER 2026
  hero img  112-372  procedural Kerch Bridge collapse scene
  hero text 372-492  headline + ONE sub-caption line (19-km)
  grid      492-860  2x2 story panels (Iran / Nvidia / Measles / Trump)
  strip     860-1024 ALSO TODAY, 3 one-line items

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
ARCH = (206, 216, 226)          # near-white: the real Kerch arches are white
ARCH_DK = (150, 164, 180)
ORANGE = (232, 122, 36)
YELLOW = (255, 190, 80)
SMOKE = (172, 180, 188)


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


def bezier(p0, p1, p2, n=28):
    """Quadratic Bezier sample points."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def pointed_arch_points(x0, x1, base_y, apex_y):
    """Tall pointed (Gothic-style) arch: two steep Bezier halves meeting
    in a cusp at the apex. Returns the full polyline, left to right."""
    ax = (x0 + x1) / 2.0
    span = x1 - x0
    h = base_y - apex_y
    left = bezier((x0, base_y), (x0 + 0.06 * span, apex_y + 0.30 * h),
                  (ax, apex_y))
    right = bezier((ax, apex_y), (x1 - 0.06 * span, apex_y + 0.30 * h),
                   (x1, base_y))
    return left + right[1:]


def arch_y_at(pts, x):
    """Interpolate arch height at x from sampled polyline points."""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if x1 <= x <= x2 and x2 != x1:
            t = (x - x1) / (x2 - x1)
            return y1 + t * (y2 - y1)
    return pts[-1][1]


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
    # sea
    d.rectangle([x0, 304, x1, y1], fill=SEA)
    for wy in (316, 332, 350, 364):
        for sx in range(0, W, 64):
            d.arc([sx, wy, sx + 44, wy + 12], 200, 340, fill=SEA_LT, width=2)
    deck_y = 256
    # --- standing spans: tall pointed white arches + hangers + deck ---
    arches = []
    for ax0, ax1 in ((30, 350), (674, 994)):
        pts = pointed_arch_points(ax0, ax1, deck_y, 130)
        arches.append(pts)
        d.line(pts, fill=ARCH, width=14, joint="curve")
        for vx in range(ax0 + 44, ax1 - 30, 44):
            ay = arch_y_at(pts, vx)
            if ay < deck_y - 6:
                d.line([(vx, ay), (vx, deck_y)], fill=ARCH, width=5)
    # --- deck (road), thicker, with a WIDE gap in the middle ---
    d.rectangle([0, deck_y, 360, deck_y + 18], fill=STEEL)
    d.rectangle([664, deck_y, W, deck_y + 18], fill=STEEL)
    d.rectangle([0, deck_y, 360, deck_y + 5], fill=ARCH)
    d.rectangle([664, deck_y, W, deck_y + 5], fill=ARCH)
    # --- verticals: end portal posts + piers into the sea ---
    for px in (60, 964):
        d.rectangle([px - 7, 200, px + 7, deck_y], fill=STEEL)
        d.rectangle([px - 7, 200, px - 2, deck_y], fill=ARCH_DK)
    for px in (120, 330, 694, 904):
        d.rectangle([px - 10, deck_y + 18, px + 10, 304], fill=STEEL)
    # --- broken stub towers framing the gap (remains of the lost span) ---
    for px in (360, 664):
        d.rectangle([px - 8, 196, px + 8, deck_y], fill=STEEL)
        d.rectangle([px - 8, 196, px - 3, deck_y], fill=ARCH_DK)
    # --- COLLAPSED middle span: broken arch stubs plunging into the sea ---
    d.line([(360, deck_y - 2), (470, 322)], fill=ARCH, width=16)
    d.line([(664, deck_y - 2), (554, 322)], fill=ARCH, width=16)
    d.line([(360, deck_y - 2), (452, 302)], fill=ARCH_DK, width=7)
    d.line([(664, deck_y - 2), (572, 302)], fill=ARCH_DK, width=7)
    # --- explosion burst where the arch broke ---
    d.ellipse([512 - 20, 240, 512 + 20, 280], fill=ORANGE)
    d.ellipse([512 - 11, 247, 512 + 11, 269], fill=YELLOW)
    # --- one clear smoke plume above the break (not scattered stains) ---
    for cx, cy, r in [(486, 214, 16), (512, 196, 22), (538, 214, 16),
                      (512, 228, 20), (496, 232, 12), (528, 232, 12)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # --- LARGE tilted falling deck fragment + a second fragment ---
    # Lighter steel than the sea, steeply tilted so it reads as falling,
    # not as a boat: dark outline, pale top edge.
    d.polygon([(436, 268), (598, 306), (590, 334), (428, 296)],
              fill=ARCH_DK, outline=STEEL)
    d.polygon([(436, 268), (598, 306), (596, 311), (436, 273)], fill=ARCH)
    d.polygon([(470, 322), (548, 330), (542, 346), (466, 338)],
              fill=ARCH_DK, outline=STEEL)
    d.polygon([(470, 322), (548, 330), (546, 334), (470, 326)], fill=ARCH)
    # --- BIG white splash: foam band + vertical spray jets at impact ---
    for sx, sy, rx, ry in [(512, 352, 72, 10), (468, 356, 32, 7),
                           (556, 356, 32, 7)]:
        d.ellipse([sx - rx, sy - ry, sx + rx, sy + ry],
                  fill=(235, 244, 248))
    for sx, y1, y2 in [(482, 318, 342), (512, 310, 342), (542, 318, 342)]:
        d.line([(sx, y1), (sx, y2)], fill=(235, 244, 248), width=4)
    for sx, sy, r in [(480, 312, 5), (544, 308, 6), (512, 300, 5),
                      (500, 322, 4), (528, 320, 4), (458, 330, 4),
                      (566, 330, 4)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 244, 248))
    # --- falling debris, bigger ---
    for dx, dy, dw, dh in [(452, 344, 34, 10), (516, 352, 42, 11),
                           (566, 346, 30, 9), (492, 330, 24, 8)]:
        d.rectangle([dx, dy, dx + dw, dy + dh], fill=ARCH_DK)
    # --- BREAKING tag: centred over the gap, clear of both arches ---
    tag = "BREAKING"
    tf = font(SANS_B, 24)
    tw = d.textlength(tag, font=tf) + 28
    tx0 = int((W - tw) // 2)
    d.rectangle([tx0, 124, tx0 + tw, 162], fill=RED)
    d.text((tx0 + 14, 129), tag, font=tf, fill=(255, 255, 255))


def draw_hero_text(d):
    d.rectangle([0, 372, W, 492], fill=PAPER)
    hf = fit_font(d, "KERCH BRIDGE COLLAPSES", SERIF_B, 58, 980)
    hw = d.textlength("KERCH BRIDGE COLLAPSES", font=hf)
    d.text(((W - hw) // 2, 380), "KERCH BRIDGE COLLAPSES", font=hf, fill=INK)
    sf = font(SANS, 26)
    line = "19-km road arch falls into the sea; rail runs on one track."
    lw = d.textlength(line, font=sf)
    d.text(((W - lw) // 2, 448), line, font=sf, fill=(52, 56, 62))


# ---------------------------------------------------------------- panels
PANELS = [
    dict(bg=(253, 238, 218), accent=(176, 92, 20), icon="drone",
         head="IRAN DRONES TARGET US BASE",
         sub="Intercepted \u2014 no damage."),
    dict(bg=(230, 244, 230), accent=(24, 120, 52), icon="chart",
         head="NVIDIA REVENUE $115.8BN, UP 103%",
         sub="Huang not reinstated."),
    dict(bg=(253, 232, 232), accent=(163, 22, 33), icon="virus",
         head="US LOSES MEASLES-FREE STATUS",
         sub="5,412 cases \u2014 after 26 years."),
    dict(bg=(232, 238, 252), accent=(28, 64, 140), icon="heads",
         head="TRUMP IN MANILA",
         sub="Quad today; Thu: first Trump\u2013Xi\u2013Putin talks in Shenzhen",
         route=True),
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


def icon_heads(d, cx, cy, route=False):
    cols = [(28, 64, 140), (163, 22, 33), (176, 132, 20)]
    for i, c in enumerate(cols):
        hx = cx - 36 + i * 36
        d.ellipse([hx - 15, cy - 34, hx + 15, cy - 4], fill=c)
        d.polygon([(hx - 24, cy + 40), (hx + 24, cy + 40),
                   (hx + 14, cy + 2), (hx - 14, cy + 2)], fill=c)
    if route:
        # Manila -> Shenzhen route arrow under the three heads.
        # Labels sit above the dots (clear of the heads' shoulders);
        # dots + arrow sit below, clear of the panel sub-caption.
        # Dots are 80px apart and labels are 11px so MANILA and
        # SHENZHEN read as two separate labels, not one phrase.
        lf = font(SANS_B, 11)
        blue = (28, 64, 140)
        d.text((cx - 56, cy + 44), "MANILA", font=lf, fill=(52, 56, 62))
        sw = d.textlength("SHENZHEN", font=lf)
        d.text((cx + 40 - sw // 2, cy + 44), "SHENZHEN", font=lf,
               fill=(52, 56, 62))
        ay = cy + 62
        d.line([(cx - 34, ay), (cx + 32, ay)], fill=blue, width=4)
        d.polygon([(cx + 40, ay), (cx + 28, ay - 6), (cx + 28, ay + 6)],
                  fill=blue)
        for dx in (cx - 40, cx + 40):
            d.ellipse([dx - 5, ay - 5, dx + 5, ay + 5], fill=blue)


ICONS = {"drone": icon_drone, "chart": icon_chart,
         "virus": icon_virus, "heads": icon_heads}


def draw_grid(d):
    for i, p in enumerate(PANELS):
        px, py = (i % 2) * 512, 492 + (i // 2) * 184
        d.rectangle([px, py, px + 512, py + 184], fill=p["bg"])
        d.rectangle([px, py, px + 10, py + 184], fill=p["accent"])
        d.line([(px, py), (px + 512, py)], fill=(255, 255, 255), width=2)
        d.line([(px, py), (px, py + 184)], fill=(255, 255, 255), width=2)
        # icon top-left; Trump heads sit higher to leave room for the
        # route arrow underneath them
        icy = py + 40 if p.get("route") else py + 54
        if p.get("route"):
            ICONS[p["icon"]](d, px + 68, icy, route=True)
        else:
            ICONS[p["icon"]](d, px + 68, icy)
        # headline right of the icon, up to 2 lines at 26px
        tx = px + 132
        maxw = 512 - 132 - 14
        hf = font(SERIF_B, 26)
        y = py + 16
        for ln in wrap(d, p["head"], hf, maxw)[:2]:
            d.text((tx, y), ln, font=hf, fill=INK)
            y += 31
        # sub-caption: full panel width, 28px, up to 2 lines
        sf = font(SANS, 28)
        y = py + 118
        for ln in wrap(d, p["sub"], sf, 480)[:2]:
            d.text((px + 16, y), ln, font=sf, fill=(38, 42, 48))
            y += 33


# ---------------------------------------------------------------- strip
ALSO = [
    "Pentagon fails 9th audit \u2014 $4.8tn unverified.",
    "An-12 crashes in Siberia \u2014 19 dead.",
    "Japan scrambles jets \u2014 suspected Russian planes.",
]


def draw_strip(d):
    d.rectangle([0, 860, W, H], fill=INK)
    lf = font(SANS_B, 24)
    d.text((24, 872), "ALSO TODAY", font=lf, fill=(255, 255, 255))
    d.line([(24, 906), (W - 24, 906)], fill=RED, width=3)
    sf = font(SANS, 27)
    y = 916
    for item in ALSO:
        d.rectangle([24, y + 8, 34, y + 18], fill=RED)
        d.text((46, y), item, font=sf, fill=(255, 255, 255))
        y += 32


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

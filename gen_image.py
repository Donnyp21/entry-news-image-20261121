"""Draw the news-image-20261121 artwork: a newspaper front page that sums
up Saturday 21 November 2026 in one image.

Build-time tool only (run once, here, with Pillow). The graded entry is
main.py, which copies the generated art.jpg to the output directory.
Every picture below is drawn from scratch with PIL shapes and text --
no photographs, no copied artwork -- so each headline is spelled
exactly as written in this file.

Stories (checked against 21 Nov 2026 reporting: OneTurn's 21 Nov day
page, Majik Morning Brief evening update for 21 Nov, WSOC/AP wire
listings for 21 Nov):
  LEAD  Iran strikes Bahrain: the Revolutionary Guards say they hit
        two US positions, at al-Riffa and Awali; Bahrain says the
        attack hit a civilian industrial site and started a fire,
        with no injuries; air defences intercepted other attacks.
  1.    Mexico captures cartel boss Fausto Isidro Meza Flores, "El
        Chapo Isidro", an FBI ten-most-wanted fugitive, in Guasave,
        Sinaloa; 11 people killed in the operation and its aftermath.
  2.    A Russian ballistic missile hits Kryvyi Rih, President
        Zelensky's hometown, killing two -- a boy aged 7 and a
        paramedic -- and wounding dozens; a Russian cargo ship,
        Sparta II, burns in the Gulf of Finland after a drone strike.
  3.    Trump, Xi and Putin hold a trilateral meeting in Shenzhen at
        the APEC summit and agree to begin talks on nuclear risk
        reduction; Zelensky calls Putin a killer.
  4.    COP31 in Antalya, Turkey runs past its deadline without a
        deal; the final draft does not mention fossil fuels, and
        late on Saturday the summit president says a deal is close.
  MARKETS  AI sell-off: the Nasdaq erases its 2026 gains in its
        worst week since March 2020; the S&P 500 and Dow enter
        correction territory; Brent crude about $91.
  Also today: Wolbachia mosquitoes cut dengue in Brazilian children
        by about 69%; BepiColombo reaches Mercury orbit after eight
        years; the UN court finds Myanmar responsible for the
        Rohingya genocide; the EU and Indonesia sign a trade deal;
        24 die as a boat capsizes in Nigeria; Bolsonaro is in
        intensive care; GTA VI earns $3.8bn on its first day.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
GREY = (74, 74, 74)
NAVY = (26, 42, 74)
RED = (178, 34, 34)
STEEL = (96, 108, 124)
SKY = (206, 224, 236)
SEA = (52, 96, 138)
GOLD = (196, 152, 44)
GREEN = (46, 110, 62)
WHITE = (252, 251, 247)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap against pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.18, align="left"):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    step = int(fnt.size * leading)
    for line in lines:
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += step
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.25)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
centered(d, W / 2, 26, "THE WORLD TODAY", font(SERIF_B, 74), INK)
d.line([(36, 118), (W - 36, 118)], fill=INK, width=3)
d.line([(36, 124), (W - 36, 124)], fill=INK, width=1)
centered(d, W / 2, 136, "SATURDAY 21 NOVEMBER 2026", font(SANS_B, 41), RED)
centered(d, W / 2, 188, "THE DAY'S WORLD NEWS IN ONE IMAGE", font(SANS, 19), GREY)
d.line([(36, 222), (W - 36, 222)], fill=INK, width=2)

# ---------------------------------------------------------------- lead: Iran strikes Bahrain
LY0, LY1 = 238, 468
d.rectangle([36, LY0, W - 36, LY1], outline=INK, width=2)
d.text((66, 254), "THE GULF - CONFLICT", font=font(SANS_B, 19), fill=NAVY)
# pictogram: sea, an oil platform, a missile arc, a burst of flame
d.rectangle([66, 356, 330, 448], fill=SEA)
for wx in (66, 110, 154, 198, 242, 286):
    d.arc([wx, 356, wx + 44, 388], start=180, end=360, fill=WHITE, width=3)
    d.arc([wx, 392, wx + 44, 424], start=180, end=360, fill=WHITE, width=3)
# oil platform on stilts
d.rectangle([110, 300, 230, 318], fill=INK)
d.rectangle([118, 318, 128, 356], fill=INK)
d.rectangle([212, 318, 222, 356], fill=INK)
d.line([(118, 318), (212, 356)], fill=INK, width=3)
d.line([(212, 318), (118, 356)], fill=INK, width=3)
d.rectangle([150, 268, 190, 300], fill=STEEL, outline=INK, width=2)
d.line([(170, 268), (170, 244)], fill=INK, width=3)
d.polygon([(170, 236), (178, 250), (162, 250)], fill=RED)
# missile arc and flame burst over the platform
d.arc([252, 288, 332, 368], start=270, end=90, fill=RED, width=4)
d.polygon([(304, 330), (316, 346), (296, 346)], fill=RED)
d.polygon([(120, 330), (132, 352), (108, 352)], fill=GOLD)
d.polygon([(150, 322), (162, 344), (138, 344)], fill=GOLD)
# lead words
lx = 396
d.text((lx, 252), "MANAMA, BAHRAIN", font=font(SANS_B, 19), fill=RED)
y = text_block(d, (lx, 280), "IRAN STRIKES BAHRAIN",
               font(SERIF_B, 43), INK, W - 36 - lx - 24, leading=1.12)
y = text_block(d, (lx, y + 10),
               "Tehran says it hit two US bases; Bahrain reports an "
               "industrial site ablaze, no injuries.",
               font(SERIF, 23), GREY, W - 36 - lx - 24, leading=1.25)

# ---------------------------------------------------------------- panels
def panel(px, py, kicker, headline, sub, draw_pic):
    pw, ph = 466, 148
    d.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
    d.text((px + 14, py + 9), kicker, font=font(SANS_B, 15), fill=RED)
    draw_pic(px + 14, py + 33)
    text_block(d, (px + 120, py + 31), headline, font(SERIF_B, 25), INK,
               pw - 134, leading=1.12)
    d.text((px + 120, py + 122), sub, font=font(SANS, 16), fill=GREY)


def pic_mexico(x, y):
    # a shield badge with a star, and a pair of handcuffs
    d.polygon([(x + 30, y + 4), (x + 62, y + 12), (x + 62, y + 44),
               (x + 30, y + 66), (x - 2, y + 44), (x - 2, y + 12)],
              fill=NAVY, outline=INK)
    cx, cy, r = x + 30, y + 34, 16
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.48
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=GOLD)
    d.ellipse([x + 58, y + 56, x + 82, y + 80], outline=INK, width=4)
    d.ellipse([x + 70, y + 66, x + 94, y + 90], outline=INK, width=4)


def pic_ukraine(x, y):
    # a city skyline with an explosion burst, and a ship on waves below
    for bx, bh in ((x + 2, 46), (x + 24, 62), (x + 48, 38), (x + 68, 54)):
        d.rectangle([bx, y + 88 - bh, bx + 18, y + 88], fill=STEEL,
                    outline=INK)
    d.polygon([(x + 46, y + 6), (x + 56, y + 24), (x + 36, y + 24)],
              fill=GOLD)
    d.polygon([(x + 62, y + 14), (x + 70, y + 30), (x + 54, y + 30)],
              fill=RED)
    d.line([(x + 84, y + 2), (x + 60, y + 26)], fill=RED, width=4)
    d.arc([x + 2, y + 88, x + 28, y + 106], start=180, end=360, fill=NAVY,
          width=3)


def pic_shenzhen(x, y):
    # three flags on poles above a small globe
    for i, col in enumerate([(196, 40, 40), (38, 62, 140), (70, 110, 180)]):
        fx = x + 6 + i * 30
        d.line([(fx, y + 6), (fx, y + 62)], fill=INK, width=3)
        d.rectangle([fx + 3, y + 8, fx + 27, y + 30], fill=col)
    d.ellipse([x + 26, y + 64, x + 64, y + 92], fill=SKY, outline=NAVY,
              width=2)
    d.line([(x + 26, y + 78), (x + 64, y + 78)], fill=NAVY, width=1)
    d.line([(x + 45, y + 64), (x + 45, y + 92)], fill=NAVY, width=1)


def pic_cop31(x, y):
    # a clock running past midnight, and a smokestack
    d.ellipse([x + 4, y + 6, x + 62, y + 64], fill=WHITE, outline=INK,
              width=3)
    d.line([(x + 33, y + 35), (x + 33, y + 16)], fill=INK, width=3)
    d.line([(x + 33, y + 35), (x + 50, y + 44)], fill=INK, width=3)
    d.ellipse([x + 29, y + 31, x + 37, y + 39], fill=RED)
    d.rectangle([x + 68, y + 40, x + 82, y + 88], fill=STEEL, outline=INK)
    d.ellipse([x + 66, y + 20, x + 80, y + 34], fill=GREY)
    d.ellipse([x + 74, y + 8, x + 88, y + 22], fill=GREY)


panel(36, 482, "SINALOA, MEXICO - JUSTICE",
      "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
      "FBI most-wanted; 11 killed in raid", pic_mexico)
panel(522, 482, "UKRAINE - CONFLICT",
      "MISSILE KILLS BOY, 7, IN KRYVYI RIH",
      "Two dead, dozens hurt; ship ablaze", pic_ukraine)
panel(36, 642, "SHENZHEN, CHINA - DIPLOMACY",
      "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
      "Nuclear risk talks agreed", pic_shenzhen)
panel(522, 642, "ANTALYA, TURKEY - CLIMATE",
      "COP31 RUNS PAST DEADLINE",
      "Draft omits fossil fuels; deal close late Sat.", pic_cop31)

# ---------------------------------------------------------------- markets
MY0, MY1 = 802, 882
d.rectangle([36, MY0, W - 36, MY1], fill=NAVY)
pts = [(58, MY0 + 18), (84, MY0 + 26), (108, MY0 + 22), (132, MY0 + 44),
       (158, MY0 + 58)]
d.line(pts, fill=(240, 120, 110), width=4)
d.polygon([(158, MY0 + 58), (146, MY0 + 56), (154, MY0 + 46)],
          fill=(240, 120, 110))
d.text((196, MY0 + 12), "AI SELL-OFF: NASDAQ ERASES ITS 2026 GAINS",
       font=font(SERIF_B, 24), fill=WHITE)
d.text((196, MY0 + 50),
       "S&P 500 and Dow in correction - Worst week since March 2020",
       font=font(SANS_B, 20), fill=(240, 205, 110))

# ---------------------------------------------------------------- also today
d.line([(36, 896), (W - 36, 896)], fill=INK, width=2)
d.text((36, 904), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
text_block(d, (36, 930),
           "Wolbachia mosquitoes cut dengue in Brazil children by ~69% - "
           "BepiColombo reaches Mercury orbit after 8 years - UN court: "
           "Myanmar responsible for Rohingya genocide - EU-Indonesia trade "
           "deal signed - 24 dead as boat capsizes in Nigeria - Bolsonaro "
           "in ICU - GTA VI earns $3.8bn in a day",
           font(SERIF, 18), INK, W - 72, leading=1.15)

img.save("art.jpg", quality=88)
print("wrote art.jpg", img.size)

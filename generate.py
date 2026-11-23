#!/usr/bin/env python3
"""Generate a 1920x1080 news-infographic PNG with Pillow (stdlib-free of network).
Run: python3 generate.py 22   -> writes news-22/entry.png + preview.png
     python3 generate.py 23   -> writes news-23/entry.png + preview.png
Copy verified from Reuters / AP / BBC / Al Jazeera / ESA / USGS, 22-23 Nov 2026.
The generated PNG is embedded (base64) in main.ts, which writes it to
$MAKEFUN_OUTPUT_DIR/entry.png with Node stdlib only.
"""
import sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

NEWS = {
 "22": {
  "date_big": "22 NOVEMBER 2026", "dow": "SUNDAY",
  "title": "THE WORLD TODAY",
  "panels": [
   ("CLIMATE", "#DC2626", "COP31 COLLAPSES: NO CLIMATE DEAL",
    "EU and ~130 nations reject a draft with no mention of fossil fuels.",
    "NEARLY 200 NATIONS  •  NO DEAL"),
   ("UKRAINE", "#2563EB", "DRONE STRIKE HITS KYIV REGION",
    "A five-storey block in Dymer partly collapses; a boy, 7, is pulled alive from the rubble.",
    "AT LEAST 5 KILLED"),
   ("MEXICO", "#059669", "EL CHAPO ISIDRO SEIZED",
    "Special forces capture FBI most-wanted Fausto Isidro Meza Flores in Sinaloa after a fierce gunfight.",
    "11 DEAD IN THE RAID"),
   ("MIDDLE EAST", "#D97706", "IRAN STRIKES US BASES IN BAHRAIN",
    "Missiles and drones hit US bases; a civilian site is struck and two people are wounded.",
    "2 WOUNDED IN BAHRAIN"),
   ("SPACE", "#7C3AED", "BEPICOLOMBO REACHES MERCURY",
    "After 8 years and 10 billion km, the ESA-JAXA probe is captured by Mercury's gravity.",
    "8 YEARS  •  10 BN KM"),
   ("USA", "#0F766E", "DEMOCRATS WIN 258 HOUSE SEATS",
    "Their largest House majority since 1992, sealed by a North Carolina recount win.",
    "BIGGEST SINCE 1992"),
  ],
  "ticker": "ALSO:  Indonesia factory fire — 3 dead, 36 missing   •   S&P 500 falls 3.7% in AI sell-off   •   EU and Indonesia sign landmark trade deal",
  "sources": "Sources: Reuters  •  AP  •  BBC  •  Al Jazeera  •  ESA  •  22 Nov 2026",
 },
 "23": {
  "date_big": "23 NOVEMBER 2026", "dow": "MONDAY",
  "title": "THE WORLD TODAY",
  "panels": [
   ("CLIMATE", "#DC2626", "COP31: THE FALLOUT, NO DEAL",
    "UN chief warns there is 'no ambiguity in the science' as ~200 nations leave Antalya without a pact.",
    "FIRST FAILURE SINCE 2009"),
   ("PACIFIC", "#0891B2", "M6.5 QUAKE SHAKES VANUATU",
    "A magnitude 6.5 earthquake strikes 600 km deep in the Vanuatu region; no tsunami threat.",
    "600 KM DEEP  •  NO TSUNAMI"),
   ("USA", "#0F766E", "DEMOCRATS' RECORD 258 SEATS",
    "BBC confirms the 258-seat House majority — the Democrats' biggest since 1992.",
    "258 SEATS  •  SINCE 1992"),
   ("SOUTH KOREA", "#DB2777", "MINISTER QUITS OVER AI CHEATING",
    "Education minister resigns days before the Suneung exam after an AI-assisted cheating scandal.",
    "DAYS BEFORE SUNEUNG"),
   ("USA", "#EA580C", "US RACES TO PROTECT THE SKIES",
    "Elite team set up to shield air traffic after a Delta glitch delays 1,000+ flights at Atlanta and beyond.",
    "1,000+ FLIGHTS DELAYED"),
   ("IRAN", "#B91C1C", "TRUMP 'INCLINED' TO STRIKE IRAN",
    "Trump signals he may resume conflict with Iran if no deal is reached by the New Year.",
    "DEADLINE: NEW YEAR"),
  ],
  "ticker": "ALSO:  Ukraine — boy, 7, pulled alive from rubble   •   Nepal PM Balen Shah begins Delhi visit   •   Nigeria boat accident kills 24   •   Kim: N. Korea seeks 'security, not supremacy'",
  "sources": "Sources: Reuters  •  BBC  •  USGS  •  AP  •  AFP  •  23 Nov 2026, morning reports",
 },
}

def build(day):
    cfg = NEWS[day]
    img = Image.new("RGB", (W, H), "#0A1122")
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W, 168], fill="#0A1122")
    d.rectangle([0, 168, W, 172], fill="#F59E0B")
    d.text((56, 30), cfg["title"], font=font(BOLD, 92), fill="white")
    d.text((56, 128), "SIX STORIES  •  ONE PAGE", font=font(BOLD, 26), fill="#F59E0B")
    # date, right aligned
    f_dow, f_date = font(BOLD, 30), font(BOLD, 46)
    d.text((W - 56 - d.textlength(cfg["dow"], font=f_dow), 34), cfg["dow"], font=f_dow, fill="#93C5FD")
    d.text((W - 56 - d.textlength(cfg["date_big"], font=f_date), 72), cfg["date_big"], font=f_date, fill="white")
    d.text((W - 56 - d.textlength("WORLD NEWS IN BRIEF", font=font(BOLD, 24)), 128),
           "WORLD NEWS IN BRIEF", font=font(BOLD, 24), fill="#94A3B8")
    # grid
    mx, my, gap = 48, 192, 20
    pw, ph = (W - 2 * mx - 2 * gap) // 3, 388
    f_cat, f_stat = font(BOLD, 25), font(BOLD, 26)
    for i, (cat, color, head, summ, stat) in enumerate(cfg["panels"]):
        x = mx + (i % 3) * (pw + gap)
        y = my + (i // 3) * (ph + gap)
        # panel
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=18, fill="white")
        d.rounded_rectangle([x, y, x + pw, y + 12], radius=6, fill=color)
        d.rectangle([x, y + 6, x + pw, y + 12], fill=color)
        # big ghost number
        d.text((x + pw - 118, y + 22), f"{i+1:02d}", font=font(BOLD, 72), fill="#E8EDF5")
        # category
        d.rectangle([x + 28, y + 34, x + 40, y + 58], fill=color)
        d.text((x + 52, y + 30), cat, font=f_cat, fill=color)
        # headline, shrink until <=2 lines
        hs = 42
        while hs >= 30:
            fh = font(BOLD, hs)
            lines = wrap(d, head, fh, pw - 56)
            if len(lines) <= 2:
                break
            hs -= 2
        fh = font(BOLD, hs)
        lines = wrap(d, head, fh, pw - 56)
        yy = y + 78
        for ln in lines[:2]:
            d.text((x + 28, yy), ln, font=fh, fill="#0A1122")
            yy += hs + 6
        # summary, <=3 lines
        ss = 28
        while ss >= 23:
            fs = font(REG, ss)
            sl = wrap(d, summ, fs, pw - 56)
            if len(sl) <= 3:
                break
            ss -= 1
        fs = font(REG, ss)
        sl = wrap(d, summ, fs, pw - 56)
        yy += 8
        for ln in sl[:3]:
            d.text((x + 28, yy), ln, font=fs, fill="#334155")
            yy += ss + 7
        # stat line at bottom
        d.line([x + 28, y + ph - 58, x + pw - 28, y + ph - 58], fill="#E2E8F0", width=2)
        d.text((x + 28, y + ph - 46), stat, font=f_stat, fill=color)
    # footer
    d.rectangle([0, 1000, W, H], fill="#111C33")
    d.text((48, 1012), cfg["ticker"], font=font(BOLD, 22), fill="#FDE68A")
    d.text((48, 1044), cfg["sources"], font=font(REG, 20), fill="#94A3B8")
    return img

if __name__ == "__main__":
    day = sys.argv[1]
    import os
    outdir = os.path.expanduser(f"~/workspace/makefun/entries/news-{day}")
    img = build(day)
    img.save(f"{outdir}/entry.png")
    img.save(f"{outdir}/preview.png")
    print(f"day {day}: {outdir}/entry.png {img.size}")

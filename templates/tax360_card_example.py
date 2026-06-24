#!/usr/bin/env python3
# TAX360 daily infographic - quarterly estimated taxes / underpayment penalty
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams["mathtext.default"] = "regular"

NAVY  = "#0E2240"
NAVY2 = "#15315C"
GOLD  = "#E8B23A"
TEAL  = "#2DBFA5"
RED   = "#E2603B"
WHITE = "#FFFFFF"
MUTE  = "#9FB3CC"

W, H = 1080, 1350
fig = plt.figure(figsize=(W/150, H/150), dpi=150)
fig.patch.set_facecolor(NAVY)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
ax.axis("off"); ax.invert_yaxis()

def rbox(x, y, w, h, fc, rad=18, alpha=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
                                fc=fc, ec="none", alpha=alpha, mutation_aspect=1))

# ---- header ----
ax.add_patch(Rectangle((0, 0), W, 130, fc=NAVY2))
t1 = ax.text(60, 55, "TAX", fontsize=32, color=WHITE, weight="bold", va="center")
fig.canvas.draw()
bb = t1.get_window_extent()
inv = ax.transData.inverted()
x0d, _ = inv.transform((bb.x0, bb.y0)); x1d, _ = inv.transform((bb.x1, bb.y0))
tax_w = abs(x1d - x0d)
ax.text(60 + tax_w + 8, 55, "360", fontsize=32, color=GOLD, weight="bold", va="center")
ax.text(62, 96, "Educational Tax Tip", fontsize=13.5, color=MUTE, va="center")

# ---- headline ----
ax.text(60, 182, "Quarterly taxes:", fontsize=32, color=WHITE, weight="bold", va="center")
ax.text(60, 240, "avoid the penalty", fontsize=32, color=GOLD, weight="bold", va="center")
ax.text(60, 300, "Pay as you go in four payments - not one lump sum at filing.",
        fontsize=15, color=MUTE, va="center")

# ---- KPI chips: IRS FY2023 penalty stats ----
ax.text(60, 344, "IRS UNDERPAYMENT PENALTIES - FY2023", fontsize=13.5, color=TEAL, weight="bold", va="center")
chip_y = 364; chip_h = 132; gap = 16
chip_w = (980 - 3*gap) / 4
chips = [("\\$7B", "collected"), ("~\\$500", "avg penalty"),
         ("8%", "interest rate"), ("~14M", "taxpayers")]
for i, (big, lab) in enumerate(chips):
    x = 50 + i*(chip_w + gap)
    rbox(x, chip_y, chip_w, chip_h, NAVY2, rad=18)
    ax.text(x+chip_w/2, chip_y+56, big, fontsize=33, color=GOLD, weight="bold", ha="center", va="center")
    ax.text(x+chip_w/2, chip_y+100, lab, fontsize=13, color=MUTE, ha="center", va="center")

# ---- timeline: four due dates ----
tl_y = 524; tl_h = 168
rbox(50, tl_y, 980, tl_h, NAVY2, rad=20)
ax.text(80, tl_y+38, "FOUR ESTIMATED DUE DATES", fontsize=15, color=WHITE, weight="bold", va="center")
node_y = tl_y + 108
xs = [180, 412, 644, 876]
ax.plot([xs[0], xs[-1]], [node_y, node_y], color=MUTE, lw=2, zorder=1)
dates = ["Apr 15", "Jun 15", "Sep 15", "Jan 15"]
for x, d in zip(xs, dates):
    ax.add_patch(plt.Circle((x, node_y), 13, fc=GOLD, zorder=2))
    ax.text(x, node_y+42, d, fontsize=16, color=WHITE, weight="bold", ha="center", va="center")

# ---- safe harbor panel ----
sh_y = 724; sh_h = 372
rbox(50, sh_y, 980, sh_h, NAVY2, rad=22)
ax.add_patch(Rectangle((50, sh_y+22), 7, sh_h-44, fc=GOLD))
ax.text(88, sh_y+46, "SAFE HARBOR = NO PENALTY", fontsize=19, color=GOLD, weight="bold", va="center")
ax.text(88, sh_y+84, "Pay enough during the year and the penalty goes away:",
        fontsize=15, color=MUTE, va="center")

def bullet(y, text, color=WHITE, size=17, x=110):
    ax.text(x, y, "✓", fontsize=size+2, color=TEAL, weight="bold", va="center")
    ax.text(x+34, y, text, fontsize=size, color=color, weight="bold", va="center")

bullet(sh_y+150, "90% of THIS year's tax,  OR")
bullet(sh_y+200, "100% of LAST year's tax")
ax.text(144, sh_y+238, "(110% if last year's AGI was over \\$150,000)",
        fontsize=13.5, color=MUTE, va="center")

# pay-online chip (sized to enclose the full line incl. EFTPS)
po_x = 88
tp = ax.text(po_x+24, sh_y+314, "Pay online:  IRS Direct Pay  or  EFTPS",
             fontsize=15, color=WHITE, weight="bold", va="center", zorder=4)
fig.canvas.draw()
bbp = tp.get_window_extent()
xa, _ = inv.transform((bbp.x0, bbp.y0)); xb, _ = inv.transform((bbp.x1, bbp.y0))
po_tw = abs(xb - xa)
rbox(po_x, sh_y+286, po_tw + 48, 56, NAVY, rad=16)

# ---- caveat ----
ax.text(W/2, 1142, "Your exact numbers depend on your situation -",
        fontsize=15, color=MUTE, ha="center", va="center")
ax.text(W/2, 1172, "talk to your tax advisor before acting.",
        fontsize=15.5, color=WHITE, weight="bold", ha="center", va="center")

# ---- footer ----
ax.add_patch(Rectangle((0, H-76), W, 76, fc=NAVY2))
ax.text(60, H-38, "SHD Advisory | TAX360",
        fontsize=12.5, color=MUTE, va="center")
ax.text(W-60, H-38, "Source: IRS, FY2023", fontsize=12, color=MUTE, va="center", ha="right")

OUT = "/sessions/focused-friendly-fermat/mnt/outputs/tax360-2026-06-24.png"
BASE = "/sessions/focused-friendly-fermat/mnt/outputs/_base.png"
fig.savefig(BASE, facecolor=NAVY, dpi=150)

# ---- composite the real SHD logo onto a white badge (top-right of header) ----
from PIL import Image, ImageDraw, ImageChops
base = Image.open(BASE).convert("RGBA")
logo = Image.open("/sessions/focused-friendly-fermat/mnt/outputs/shd_logo_raw.png").convert("RGBA")
# autocrop the white border
white = Image.new("RGBA", logo.size, (255, 255, 255, 255))
bbox = ImageChops.difference(logo, white).convert("L").getbbox()
if bbox:
    logo = logo.crop(bbox)
LH = 100
lw = int(logo.size[0] * LH / logo.size[1])
logo = logo.resize((lw, LH), Image.LANCZOS)
pad = 12
bw, bh = lw + 2*pad, LH + 2*pad
badge = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
d = ImageDraw.Draw(badge)
d.rounded_rectangle([0, 0, bw-1, bh-1], radius=18, fill=(255, 255, 255, 255))
badge.paste(logo, (pad, pad), logo)
bx, by = W - 40 - bw, (130 - bh)//2
base.alpha_composite(badge, (bx, by))
base.convert("RGB").save(OUT, quality=95)
import os
print("saved bytes:", os.path.getsize(OUT), "badge", (bw, bh))

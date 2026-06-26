#!/usr/bin/env python3
"""
TAX360 infographic — REFERENCE / HOUSE-STYLE TEMPLATE (brand-aligned, modern).
Adapt this card for each day's topic: keep the structure + styling, swap the
content (headline, stat band, comparison cards, accent strip).

BRAND PALETTE (derived from the SHD logo teal #3C8CA0 — use these, NOT navy/gold):
  BG deep petrol #0B2731 · panels #11343F / #0E2C36
  brand teal #3C8CA0 · bright teal #5BB6CC (accents/labels)
  gold #E7B24C (numbers / one accent only) · white #FFFFFF · muted #9DBBC4
  hairlines #1E4A58
TYPE (modern, real fonts — installed under /usr/share/fonts):
  Poppins-Bold  -> headlines & big numbers
  Poppins-Medium-> subheads / strip titles
  Lato-Bold     -> letter-spaced kickers & section labels (use spaced caps)
  Lato-Regular  -> body / stat labels   ·  Lato-Light -> hero description
LAYOUT (top->bottom): header band (TAX360 wordmark + "Educational Tax Tip" +
  white logo badge top-right) · letter-spaced kicker · big headline · gold
  subhead · 1-2 muted description lines · a stat BAND split by hairline
  dividers (not boxes) · a 2-card comparison (accent underline + dot bullets)
  · a slim accent strip (left gold bar) · caveat (2 lines) · footer band.
EVERGREEN: NO post date anywhere on the card (date lives only in the Doc/filename).
ANTI-BLEED (critical):
  - keep all content inside a 64px margin every side
  - measure rendered widths (textw / get_window_extent) and AUTO-FIT bullet text
    so nothing overflows its card; never hardcode that it fits
  - give the headline a real gap above (kicker) and below (subhead) — use
    generous FIXED y-coordinates with line spacing, not tight stacking
  - for two adjacent-colored words on one line (TAX + 360) measure the first and
    offset the second by its width + gap
  - keep PNG < ~1MB (Facebook pixelates larger). 1080x1350 portrait.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, os
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.font_manager import FontProperties
plt.rcParams["mathtext.default"]="regular"

BG="#0B2731"; PANEL="#11343F"; PANEL2="#0E2C36"
TEAL="#3C8CA0"; TEALB="#5BB6CC"; GOLD="#E7B24C"
WHITE="#FFFFFF"; MUTE="#9DBBC4"; LINE="#1E4A58"
GF="/usr/share/fonts/truetype/google-fonts/"; LF="/usr/share/fonts/truetype/lato/"
FONT={"pb":GF+"Poppins-Bold.ttf","pm":GF+"Poppins-Medium.ttf","pr":GF+"Poppins-Regular.ttf",
      "ll":LF+"Lato-Light.ttf","lr":LF+"Lato-Regular.ttf","lb":LF+"Lato-Bold.ttf"}
def fp(k,s): return FontProperties(fname=FONT[k],size=s)
W,H=1080,1350; M=64
fig=plt.figure(figsize=(W/150,H/150),dpi=150); fig.patch.set_facecolor(BG)
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off"); ax.invert_yaxis()
inv=ax.transData.inverted()
def rbox(x,y,w,h,fc,rad=20):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={rad}",fc=fc,ec="none",mutation_aspect=1))
def T(x,y,s,k,size,color,ha="left",va="center"):
    return ax.text(x,y,s,fontproperties=fp(k,size),color=color,ha=ha,va=va)
def tw(o):
    fig.canvas.draw(); bb=o.get_window_extent()
    a,_=inv.transform((bb.x0,bb.y0)); b,_=inv.transform((bb.x1,bb.y0)); return abs(b-a)
def textw(s,k,size):
    t=ax.text(0,-200,s,fontproperties=fp(k,size)); w=tw(t); t.remove(); return w

# header
t1=T(M,58,"TAX","pb",30,WHITE); T(M+tw(t1)+6,58,"360","pb",30,GOLD)
T(M+2,92,"E D U C A T I O N A L   T A X   T I P","lb",11.5,TEAL)
ax.add_patch(Rectangle((M,124),W-2*M,2,fc=LINE))
# hero (fixed, generously spaced)
T(M,176,"K I C K E R   ·   A U D I E N C E","lb",12,TEAL)
T(M,248,"Headline goes here","pb",40,WHITE)
T(M,314,"Gold subhead — the key idea","pm",22,GOLD)
T(M,362,"One muted description line explaining the tip in plain language,","ll",15,MUTE)
T(M,390,"wrapped to a second line if needed.","ll",15,MUTE)
# stat band (hairline dividers, no inner boxes)
T(M,438,"S E C T I O N   L A B E L","lb",12.5,TEAL)
pY=458; pH=146; rbox(M,pY,W-2*M,pH,PANEL,rad=22); colw=(W-2*M)/3
for i,(big,lab) in enumerate([("$24,500","stat one"),("+ 25%","stat two"),("$72,000","stat three")]):
    cx=M+colw*(i+0.5); T(cx,pY+60,big,"pb",33,GOLD,ha="center"); T(cx,pY+103,lab,"lr",14,MUTE,ha="center")
    if i>0: ax.add_patch(Rectangle((M+colw*i,pY+32),1.6,pH-64,fc=LINE))
T(W/2,pY+pH+30,"A muted qualifier / caveat line under the stat band.","lr",13.5,MUTE,ha="center")
# comparison cards (auto-fit bullets)
T(M,672,"O P T I O N   A   vs   O P T I O N   B","lb",12.5,TEAL)
cY=692; cH=288; gap=24; cw=(W-2*M-gap)/2
A=["Short bullet one","Short bullet two","Short bullet three"]; B=["Short bullet one","Short bullet two","Short bullet three"]
inner=cw-62-30; bsz=15.5
while bsz>13 and max(textw(r,"lr",bsz) for r in A+B)>inner: bsz-=0.5
def card(x,accent,title,rows):
    rbox(x,cY,cw,cH,PANEL,rad=22); T(x+34,cY+50,title,"pb",20,accent)
    ax.add_patch(Rectangle((x+34,cY+74),64,3,fc=accent)); yy=cY+128
    for r in rows: ax.add_patch(plt.Circle((x+42,yy),5,fc=accent)); T(x+62,yy,r,"lr",bsz,WHITE); yy+=54
card(M,TEALB,"OPTION A",A); card(M+cw+gap,GOLD,"OPTION B",B)
# accent strip
dY=1004; dH=92; rbox(M,dY,W-2*M,dH,PANEL2,rad=20); ax.add_patch(Rectangle((M,dY+18),6,dH-36,fc=GOLD))
T(M+36,dY+34,"Key takeaway / deadline line","pm",18,WHITE)
T(M+36,dY+66,"A supporting muted sentence under it.","lr",14,MUTE)
# caveat
T(W/2,1156,"Your exact numbers depend on your situation.","lr",14.5,MUTE,ha="center")
T(W/2,1186,"Talk to your tax advisor before acting.","lb",15,WHITE,ha="center")
# footer
ax.add_patch(Rectangle((M,H-94),W-2*M,1.6,fc=LINE))
T(M,H-46,"SHD Advisory  ·  TAX360","lb",12.5,MUTE)
T(W-M,H-46,"Source: IRS","lr",12,MUTE,ha="right")

fig.savefig("/tmp/_tpl_base.png",facecolor=BG,dpi=150)
# logo badge composite (white rounded badge, autocropped logo, top-right)
from PIL import Image, ImageDraw, ImageChops
base=Image.open("/tmp/_tpl_base.png").convert("RGBA")
logo=Image.open(os.path.join(os.path.dirname(__file__),"..","images","shd_logo.png")).convert("RGBA")
wt=Image.new("RGBA",logo.size,(255,255,255,255)); bb=ImageChops.difference(logo,wt).convert("L").getbbox()
if bb: logo=logo.crop(bb)
LH=98; lw=int(logo.size[0]*LH/logo.size[1]); logo=logo.resize((lw,LH),Image.LANCZOS)
pad=13; bw,bh=lw+2*pad,LH+2*pad
badge=Image.new("RGBA",(bw,bh),(0,0,0,0)); ImageDraw.Draw(badge).rounded_rectangle([0,0,bw-1,bh-1],radius=20,fill=(255,255,255,255))
badge.paste(logo,(pad,pad),logo); base.alpha_composite(badge,(W-M-bw,(132-bh)//2))
base.convert("RGB").save("/tmp/tax360-card.png",quality=92)
print("saved",os.path.getsize("/tmp/tax360-card.png"))

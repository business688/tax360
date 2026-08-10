#!/usr/bin/env python3
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
    return ax.text(x,y,s,fontproperties=fp(k,size),color=color,ha=ha,va=va,parse_math=False)
def tw(o):
    fig.canvas.draw(); bb=o.get_window_extent()
    a,_=inv.transform((bb.x0,bb.y0)); b,_=inv.transform((bb.x1,bb.y0)); return abs(b-a)
def textw(s,k,size):
    t=ax.text(0,-200,s,fontproperties=fp(k,size)); w=tw(t); t.remove(); return w
MAXW=W-2*M

# header
t1=T(M,58,"TAX","pb",30,WHITE); T(M+tw(t1)+6,58,"360","pb",30,GOLD)
T(M+2,92,"E D U C A T I O N A L   T A X   T I P","lb",11.5,TEAL)
ax.add_patch(Rectangle((M,124),W-2*M,2,fc=LINE))

# hero
T(M,176,"H S A   ·   S M A L L   B U S I N E S S   O W N E R S","lb",12,TEAL)
hl="The triple tax advantage"; hsz=40
while hsz>26 and textw(hl,"pb",hsz)>MAXW: hsz-=1
T(M,248,hl,"pb",hsz,WHITE)
T(M,314,"One account. Three tax breaks.","pm",22,GOLD)
T(M,362,"A Health Savings Account is the only account where money goes in,","ll",15,MUTE)
T(M,390,"grows, and comes out for medical costs — all tax-free.","ll",15,MUTE)

# stat band
T(M,438,"2 0 2 6   C O N T R I B U T I O N   L I M I T S","lb",12.5,TEAL)
pY=458; pH=146; rbox(M,pY,W-2*M,pH,PANEL,rad=22); colw=(W-2*M)/3
for i,(big,lab) in enumerate([("$4,400","self-only limit"),("$8,750","family limit"),("+ $1,000","catch-up, age 55+")]):
    cx=M+colw*(i+0.5); T(cx,pY+60,big,"pb",33,GOLD,ha="center"); T(cx,pY+103,lab,"lr",14,MUTE,ha="center")
    if i>0: ax.add_patch(Rectangle((M+colw*i,pY+32),1.6,pH-64,fc=LINE))
T(W/2,pY+pH+30,"2026 IRS limits (Rev. Proc. 2025-19). You must be on an HDHP to contribute.","lr",13.5,MUTE,ha="center")

# comparison cards
T(M,672,"W H Y   I T   W I N S   ·   A N D   A F T E R   6 5","lb",12.5,TEAL)
cY=692; cH=288; gap=24; cw=(W-2*M-gap)/2
A=["Contributions are deductible","Balance grows tax-free","Medical withdrawals tax-free"]
B=["Withdraw for any reason","Taxed like a normal IRA","Doubles as retirement savings"]
inner=cw-62-30; bsz=15.5
while bsz>13 and max(textw(r,"lr",bsz) for r in A+B)>inner: bsz-=0.5
def card(x,accent,title,rows):
    rbox(x,cY,cw,cH,PANEL,rad=22); T(x+34,cY+50,title,"pb",20,accent)
    ax.add_patch(Rectangle((x+34,cY+74),64,3,fc=accent)); yy=cY+128
    for r in rows: ax.add_patch(plt.Circle((x+42,yy),5,fc=accent)); T(x+62,yy,r,"lr",bsz,WHITE); yy+=54
card(M,TEALB,"TRIPLE TAX-FREE",A); card(M+cw+gap,GOLD,"AFTER AGE 65",B)

# accent strip
dY=1004; dH=92; rbox(M,dY,W-2*M,dH,PANEL2,rad=20); ax.add_patch(Rectangle((M,dY+18),6,dH-36,fc=GOLD))
T(M+36,dY+34,"You can still fund your 2026 HSA","pm",18,WHITE)
T(M+36,dY+66,"Contributions for 2026 are allowed up to the April 2027 filing deadline.","lr",14,MUTE)

# caveat
T(W/2,1156,"Your exact numbers depend on your coverage and situation.","lr",14.5,MUTE,ha="center")
T(W/2,1186,"Talk to your tax advisor before acting.","lb",15,WHITE,ha="center")

# footer
ax.add_patch(Rectangle((M,H-94),W-2*M,1.6,fc=LINE))
T(M,H-46,"SHD Advisory  ·  TAX360","lb",12.5,MUTE)
T(W-M,H-46,"Source: IRS Rev. Proc. 2025-19","lr",12,MUTE,ha="right")

fig.savefig("/tmp/_tpl_base.png",facecolor=BG,dpi=150)
from PIL import Image, ImageDraw, ImageChops
base=Image.open("/tmp/_tpl_base.png").convert("RGBA")
logo=Image.open("/tmp/tax360repo/images/shd_logo.png").convert("RGBA")
wt=Image.new("RGBA",logo.size,(255,255,255,255)); bb=ImageChops.difference(logo,wt).convert("L").getbbox()
if bb: logo=logo.crop(bb)
LH=98; lw=int(logo.size[0]*LH/logo.size[1]); logo=logo.resize((lw,LH),Image.LANCZOS)
pad=13; bw,bh=lw+2*pad,LH+2*pad
badge=Image.new("RGBA",(bw,bh),(0,0,0,0)); ImageDraw.Draw(badge).rounded_rectangle([0,0,bw-1,bh-1],radius=20,fill=(255,255,255,255))
badge.paste(logo,(pad,pad),logo); base.alpha_composite(badge,(W-M-bw,(132-bh)//2))
base.convert("RGB").save("/tmp/tax360-card.png",quality=92)
print("headline_size",hsz,"bullet_size",bsz)
print("saved_bytes",os.path.getsize("/tmp/tax360-card.png"))

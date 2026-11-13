"""本文用：キャラクターのひとこと（吹き出し）"""
import sys
from PIL import Image, ImageDraw, ImageFont
FONT_B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
NAVY=(14,27,51); BG=(246,248,250); ACCENT=(126,200,150)
def make(out,pose,text):
    W,H=1200,400
    img=Image.new('RGBA',(W,H),BG+(255,)); d=ImageDraw.Draw(img)
    ch=Image.open(f'poses/{pose}.png').convert('RGBA')
    s=360/ch.height; ch=ch.resize((int(ch.width*s),360),Image.LANCZOS)
    cx=40; d.ellipse([cx-10,40,cx+340,390],fill=(232,240,236,255))
    img.alpha_composite(ch,(cx+165-ch.width//2,H-ch.height))
    bx0,by0,bx1,by1=400,60,1150,340
    d.rounded_rectangle([bx0,by0,bx1,by1],radius=36,fill=(255,255,255),outline=NAVY,width=4)
    d.polygon([(bx0+2,200),(bx0-44,230),(bx0+2,250)],fill=(255,255,255))
    d.line([(bx0,200),(bx0-44,230),(bx0,250)],fill=NAVY,width=4)
    lines=text.split('|'); f=ImageFont.truetype(FONT_B,46,index=0); lh=70
    ty=(by0+by1)//2-len(lines)*lh//2+4
    for i,l in enumerate(lines): d.text((bx0+50,ty+i*lh),l,font=f,fill=NAVY)
    img.convert('RGB').save(out)
make(*sys.argv[1:])

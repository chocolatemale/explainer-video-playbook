"""Pixel-stable drawing vocabulary; layout and editorial values live in the spec."""
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math
W,H=1920,1080
PAPER='#F4F1E8';INK='#161616';YELLOW='#FFE03A';RED='#E8392F';BLUE='#3570E8';GREEN='#1FA971';GRAY='#C9C4B8'
FONT_DIR=Path('build/fonts');STILLS=Path('build/stills');SCREEN_TEXT=set()
@lru_cache(None)
def font(size,weight='Bold'):
    f=ImageFont.truetype(str(FONT_DIR/'NotoSansSC.ttf'),int(size))
    f.set_variation_by_name(weight);return f
def measure(s,size,weight='Bold'):return math.ceil(font(size,weight).getlength(s))
def rounded(im,xy,fill,r=10,outline=None,width=1):
    ImageDraw.Draw(im).rounded_rectangle(tuple(map(round,xy)),radius=r,fill=fill,outline=outline,width=width)
def text(im,s,x,y,size=60,fill=INK,anchor='mm',stroke=0,weight='Bold'):
    SCREEN_TEXT.add(s)
    ImageDraw.Draw(im).text((round(x),round(y)),s,font=font(size,weight),fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=INK)
def alpha_paste(im,tile,x,y):im.alpha_composite(tile,(round(x),round(y)))
def shadow(tile,blur=10,dy=9):
    a=tile.getchannel('A');sh=Image.new('RGBA',tile.size,(0,0,0,0));sh.putalpha(a.point(lambda v:int(v*.2)))
    sh=sh.filter(ImageFilter.GaussianBlur(blur));out=Image.new('RGBA',tile.size)
    out.alpha_composite(sh,(0,dy));out.alpha_composite(tile);return out
def ease(v):v=max(0,min(1,v));return 1-(1-v)**3
def bounce(age):
    u=max(0,min(1,age/4.5))
    return .6+.48*ease(u/.66) if u<.66 else 1.08-.08*ease((u-.66)/.34)
def place(im,tile,cx,cy,age=None,kind='pop'):
    if age is not None and age<0:return
    a=1;s=1
    if age is not None:
        if kind=='card':cy+=30*(1-ease(age/7.5));a=ease(age/7.5)
        elif kind=='flip':s=max(.05,ease(age/7.5))
        else:s=bounce(age)
    if s!=1:
        if kind=='flip':tile=tile.resize((max(1,round(tile.width*s)),tile.height),Image.Resampling.LANCZOS)
        else:tile=tile.resize((max(1,round(tile.width*s)),max(1,round(tile.height*s))),Image.Resampling.LANCZOS)
    if a<1:tile=tile.copy();tile.putalpha(tile.getchannel('A').point(lambda v:round(v*a)))
    alpha_paste(im,tile,cx-tile.width/2,cy-tile.height/2)
@lru_cache(None)
def chip_tile(s,size=60,kind='y',angle=0):
    colors={'y':(YELLOW,INK),'k':(INK,'white'),'g':(GREEN,'white'),'tag':('white',INK),'r':(RED,'white')}
    bg,fg=colors[kind];ww=measure(s,size)+56;hh=round(size*1.6);margin=30
    tile=Image.new('RGBA',(ww+margin*2,hh+margin*2))
    rounded(tile,(margin,margin,margin+ww,margin+hh),bg,4 if kind=='tag' else 10,'white' if kind=='r' else None,6)
    text(tile,s,tile.width/2,tile.height/2-1,size,fg)
    if angle:tile=tile.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    return shadow(tile)
def chip(im,s,cx,cy,size=60,kind='y',age=None,angle=0):place(im,chip_tile(s,size,kind,angle),cx,cy,age)
def tag(im,s,age=None):
    tile=chip_tile(s,58,'tag');place(im,tile,105+tile.width/2-30,125,age)
@lru_cache(None)
def kinetic_tile(s,size=120,highlight='',color='white'):
    while measure(s,size)>1660:size-=2
    ww=measure(s,size);tile=Image.new('RGBA',(ww+70,round(size*1.75)))
    x=35;y=tile.height/2
    # Four-pixel outline plus restrained black drop shadow.
    text(tile,s,x+3,y+7,size,'#161616',anchor='lm',stroke=4)
    text(tile,s,x,y,size,color,anchor='lm',stroke=4)
    if highlight and highlight in s:
        i=s.index(highlight);hx=x+measure(s[:i],size);hw=measure(highlight,size)
        rounded(tile,(hx-7,y-size*.53,hx+hw+7,y+size*.63),YELLOW,3)
        text(tile,highlight,hx,y,size,INK,anchor='lm')
    return tile
def kinetic(im,s,cy=480,size=120,highlight='',age=None,color='white'):
    place(im,kinetic_tile(s,size,highlight,color),960,cy,age)
@lru_cache(None)
def photo(clip,w,h):
    return ImageOps.fit(Image.open(STILLS/f'{clip}.jpg').convert('RGBA'),(w,h),method=Image.Resampling.LANCZOS)
@lru_cache(None)
def card_tile(clip,city,w,h):
    m=30;tile=Image.new('RGBA',(w+2*m,h+2*m));mask=Image.new('L',(w,h))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=10,fill=255)
    pic=photo(str(clip),w,h).copy();pic.putalpha(mask);alpha_paste(tile,pic,m,m)
    ImageDraw.Draw(tile).rounded_rectangle((m,m,w+m-1,h+m-1),radius=10,outline='white',width=6)
    if city:
        label=chip_tile(city,42,'tag');alpha_paste(tile,label,m+4,m-4)
    return shadow(tile)
def card(im,clip,city,x,y,w,h,age=None):place(im,card_tile(str(clip),city,w,h),x+w/2,y+h/2,age,'card')
def count(im,value,x,y,age,size=90,color=INK,unit=''):
    n=round(value*ease(age/12.5));text(im,str(n)+unit,x,y,size,color)
def paper():
    # Flat warm stock and very faint fixed fibers; fully opaque on every B frame.
    im=Image.new('RGBA',(W,H),PAPER);d=ImageDraw.Draw(im)
    for i in range(160):
        x=(i*683+17)%W;y=(i*397+53)%H
        d.line((x,y,x+2+(i%4),y),fill='#ECE9E0',width=1)
    return im

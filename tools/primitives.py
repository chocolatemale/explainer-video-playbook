"""Pixel-stable drawing vocabulary; layout and editorial values live in the spec."""
import json, os, struct
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math
W,H=1920,1080
PAPER='#F4F1E8';INK='#161616';YELLOW='#FFE03A';RED='#E8392F';BLUE='#3570E8';GREEN='#1FA971';GRAY='#C9C4B8'
FONT_DIR=Path('build/fonts');STILLS=Path('build/stills');SCREEN_TEXT=set()
FONT_CONFIG=Path(__file__).resolve().parent/'fonts.json'
PRESET=None

def reset_font_caches():
    _font.cache_clear();cmap.cache_clear();chip_tile.cache_clear();kinetic_tile.cache_clear();card_tile.cache_clear()

def font_bundle():
    data=json.loads(FONT_CONFIG.read_text(encoding='utf-8'))
    name=PRESET or os.environ.get('PLAYBOOK_FONT_PRESET') or data.get('active','noto')
    if name not in data['presets']:raise ValueError(f'Unknown font preset: {name}')
    return data['presets'][name], name

def role_spec(role):
    bundle,_=font_bundle();return dict(bundle.get(role) or bundle['ui'])

def caption_style():
    spec=role_spec('caption')
    return dict(size=int(spec.get('size',46)),stroke=int(spec.get('stroke',5)),y=int(spec.get('y',1010)))

def _u16(data,off):return struct.unpack_from('>H',data,off)[0]
def _u32(data,off):return struct.unpack_from('>I',data,off)[0]
def _i16(data,off):return struct.unpack_from('>h',data,off)[0]

@lru_cache(None)
def cmap(path):
    data=Path(path).read_bytes();n=_u16(data,4);off=None
    for i in range(n):
        rec=12+i*16
        if data[rec:rec+4]==b'cmap':off=_u32(data,rec+8);break
    if off is None:return None
    covered=set();num=_u16(data,off+2);records=[]
    for i in range(num):
        rec=off+4+i*8
        records.append((_u16(data,rec),_u16(data,rec+2),_u32(data,rec+4)))
    for platform,encoding,sub in records:
        if platform not in (0,3):continue
        fmt=_u16(data,off+sub)
        if fmt==4:
            seg=_u16(data,off+sub+6)//2;base=off+sub+14
            ends=[_u16(data,base+2*i) for i in range(seg)]
            starts=[_u16(data,base+2+2*seg+2*i) for i in range(seg)]
            deltas=[_i16(data,base+2+4*seg+2*i) for i in range(seg)]
            ranges=[_u16(data,base+2+6*seg+2*i) for i in range(seg)]
            glyph_off=base+2+6*seg
            for s,e,d,ro,idx in zip(starts,ends,deltas,ranges,range(seg)):
                for cp in range(s,e+1):
                    if ro==0:gid=(cp+d)&0xFFFF
                    else:
                        p=glyph_off+2*idx+ro+2*(cp-s)
                        gid=0 if p+2>len(data) else _u16(data,p)
                        if gid:gid=(gid+d)&0xFFFF
                    if gid:covered.add(cp)
        elif fmt==12:
            nGroups=_u32(data,off+sub+12);g=off+sub+16
            for i in range(nGroups):
                a,b,start=_u32(data,g),_u32(data,g+4),_u32(data,g+8);g+=12
                for cp in range(a,b+1):
                    if start+(cp-a):covered.add(cp)
    return frozenset(covered)

def _open_face(spec,size):
    path=FONT_DIR/spec['file']
    if not path.exists():raise FileNotFoundError(f'Missing font {path}; run tools/fetch_fonts.sh')
    f=ImageFont.truetype(str(path),int(size))
    variation=spec.get('variation')
    if variation:
        try:f.set_variation_by_name(variation)
        except OSError:pass
    return f

@lru_cache(None)
def _font(size,weight,role,font_dir,preset):
    spec=role_spec(role)
    if weight and weight!='Bold' and 'variation' in spec:
        spec=dict(spec,variation=weight)
    return _open_face(spec,size)

def font(size,weight='Bold',role='ui'):
    _,preset=font_bundle()
    return _font(int(size),weight,role,str(FONT_DIR),preset)

def _fallback(size,weight):
    _,preset=font_bundle()
    return _font(int(size),weight,'fallback',str(FONT_DIR),preset)

def _has_glyph(role,ch):
    spec=role_spec(role);table=cmap(str(FONT_DIR/spec['file']))
    if table is None:return True
    return ord(ch) in table

def _runs(s,role):
    if not s:return []
    out=[];cur=_has_glyph(role,s[0]);buf=s[0]
    for ch in s[1:]:
        ok=_has_glyph(role,ch)
        if ok==cur:buf+=ch
        else:out.append((cur,buf));buf=ch;cur=ok
    out.append((cur,buf));return out

def measure(s,size,weight='Bold',role='ui'):
    if not s:return 0
    total=0
    for ok,part in _runs(s,role):
        face=font(size,weight,role) if ok else _fallback(size,weight)
        total+=face.getlength(part)
    return math.ceil(total)

def _anchor_origin(x,y,w,h,anchor):
    ax,ay=anchor[0],anchor[1]
    x=x-(0 if ax=='l' else w if ax=='r' else w/2)
    y=y-(0 if ay=='t' else h if ay=='s' else h/2)
    return x,y

def draw_text(im,s,x,y,size,fill,anchor,stroke,weight,role,stroke_fill=INK):
    runs=_runs(s,role)
    fonts=[(font(size,weight,role) if ok else _fallback(size,weight),part) for ok,part in runs]
    if len(fonts)==1:
        ImageDraw.Draw(im).text((round(x),round(y)),s,font=fonts[0][0],fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=stroke_fill)
        return
    width=sum(f.getlength(part) for f,part in fonts)
    ascent,descent=fonts[0][0].getmetrics();height=ascent+descent
    left,top=_anchor_origin(x,y,width,height,anchor)
    cursor=left;mid=top+ascent
    for f,part in fonts:
        ImageDraw.Draw(im).text((round(cursor),round(mid)),part,font=f,fill=fill,anchor='lm',stroke_width=stroke,stroke_fill=stroke_fill)
        cursor+=f.getlength(part)

def rounded(im,xy,fill,r=10,outline=None,width=1):
    ImageDraw.Draw(im).rounded_rectangle(tuple(map(round,xy)),radius=r,fill=fill,outline=outline,width=width)
def text(im,s,x,y,size=60,fill=INK,anchor='mm',stroke=0,weight='Bold',role='ui',stroke_fill=INK):
    SCREEN_TEXT.add(s)
    draw_text(im,s,x,y,size,fill,anchor,stroke,weight,role,stroke_fill)
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
    bg,fg=colors[kind];ww=measure(s,size,role='title')+56;hh=round(size*1.6);margin=30
    tile=Image.new('RGBA',(ww+margin*2,hh+margin*2))
    rounded(tile,(margin,margin,margin+ww,margin+hh),bg,4 if kind=='tag' else 10,'white' if kind=='r' else None,6)
    text(tile,s,tile.width/2,tile.height/2-1,size,fg,role='title')
    if angle:tile=tile.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    return shadow(tile)
def chip(im,s,cx,cy,size=60,kind='y',age=None,angle=0):place(im,chip_tile(s,size,kind,angle),cx,cy,age)
def tag(im,s,age=None):
    tile=chip_tile(s,58,'tag');place(im,tile,105+tile.width/2-30,125,age)
@lru_cache(None)
def kinetic_tile(s,size=120,highlight='',color='white'):
    while measure(s,size,role='title')>1660:size-=2
    ww=measure(s,size,role='title');tile=Image.new('RGBA',(ww+70,round(size*1.75)))
    x=35;y=tile.height/2
    # Four-pixel outline plus restrained black drop shadow.
    text(tile,s,x+3,y+7,size,'#161616',anchor='lm',stroke=4,role='title')
    text(tile,s,x,y,size,color,anchor='lm',stroke=4,role='title')
    if highlight and highlight in s:
        i=s.index(highlight);hx=x+measure(s[:i],size,role='title');hw=measure(highlight,size,role='title')
        rounded(tile,(hx-7,y-size*.53,hx+hw+7,y+size*.63),YELLOW,3)
        text(tile,highlight,hx,y,size,INK,anchor='lm',role='title')
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
    n=round(value*ease(age/12.5));text(im,str(n)+unit,x,y,size,color,role='ui')
def paper():
    # Flat warm stock and very faint fixed fibers; fully opaque on every B frame.
    im=Image.new('RGBA',(W,H),PAPER);d=ImageDraw.Draw(im)
    for i in range(160):
        x=(i*683+17)%W;y=(i*397+53)%H
        d.line((x,y,x+2+(i%4),y),fill='#ECE9E0',width=1)
    return im

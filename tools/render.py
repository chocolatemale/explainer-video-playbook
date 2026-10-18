"""Interpret data-only layout nodes into random-access RGBA layers and SRT."""
import argparse
import ast
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import primitives as p
from common import load, srt

class ContinueLoop(Exception): pass

class Renderer:
    def __init__(self,spec,timeline,fonts,stills):
        self.spec=spec; self.t=timeline
        if (timeline['width'],timeline['height'],timeline['fps']) != (1920,1080,25):
            raise ValueError('This style preset uses 1920×1080 at 25 fps; scale at composition time')
        p.FONT_DIR=Path(fonts);p.STILLS=Path(stills)
        for fn in (p.font,p.photo,p.chip_tile,p.card_tile,p.kinetic_tile):fn.cache_clear()
        self.segments={s['id']:s for s in spec['segments']}
        self.functions={name:getattr(p,name) for name in ['ease','measure','shadow','photo']}
        self.functions.update(dict(str=str,round=round,len=len,enumerate=enumerate,zip=zip,
                                   range=range,min=min,max=max,int=int,float=float,abs=abs))

    def value(self,v,env):
        if isinstance(v,dict) and set(v)=={'expr'}:
            expr=ast.parse(v['expr'],mode='eval')
            allowed=(ast.Expression,ast.Constant,ast.Name,ast.Load,ast.List,ast.Tuple,ast.Dict,
                ast.Subscript,ast.Slice,ast.BinOp,ast.UnaryOp,ast.BoolOp,ast.Compare,ast.IfExp,
                ast.Call,ast.keyword,ast.Attribute,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.FloorDiv,
                ast.Mod,ast.Pow,ast.USub,ast.UAdd,ast.Not,ast.And,ast.Or,ast.Eq,ast.NotEq,
                ast.Lt,ast.LtE,ast.Gt,ast.GtE,ast.In,ast.NotIn,ast.ListComp,ast.comprehension,ast.Store)
            for n in ast.walk(expr):
                if not isinstance(n,allowed):raise ValueError(f'Unsupported expression: {type(n).__name__}')
                if isinstance(n,ast.Name) and n.id.startswith('_'):raise ValueError('Private names forbidden')
                if isinstance(n,ast.Attribute) and n.attr not in ('get','index'):raise ValueError('Only get/index methods allowed')
                if isinstance(n,ast.Call):
                    if isinstance(n.func,ast.Name) and n.func.id not in {*self.functions,'age','on','stage','event_age'}:
                        raise ValueError(f'Function forbidden: {n.func.id}')
                    if not isinstance(n.func,(ast.Name,ast.Attribute)):raise ValueError('Indirect calls forbidden')
            return eval(compile(expr,'<layout>','eval'),dict(env,__builtins__={}),{})
        if isinstance(v,list):return [self.value(x,env) for x in v]
        if isinstance(v,dict):return {k:self.value(x,env) for k,x in v.items()}
        return v

    def assign(self,names,v,env):
        node=ast.parse(names,mode='eval').body
        def unpack(n,x):
            if isinstance(n,ast.Name):env[n.id]=x
            elif isinstance(n,(ast.Tuple,ast.List)):
                if len(n.elts)!=len(x):raise ValueError('Unpack length mismatch')
                for a,b in zip(n.elts,x):unpack(a,b)
            else:raise ValueError('Assignment must use names')
        unpack(node,v)

    def draw(self,nodes,env):
        for n in nodes:
            kind=n['type'];v=lambda x:self.value(x,env)
            if 'when' in n and not v({'expr':n['when']}):continue
            if kind=='set':self.assign(n['name'],v(n['value']),env)
            elif kind=='if':self.draw(n.get('then',[]) if v({'expr':n['condition']}) else n.get('else',[]),env)
            elif kind=='repeat':
                for item in v(n['items']):
                    self.assign(n['names'],item,env)
                    try:self.draw(n['elements'],env)
                    except ContinueLoop:pass
            elif kind=='continue':raise ContinueLoop()
            elif kind in ('group','formula','table','dots'):self.draw(n['elements'],env)
            elif kind=='include':self.draw(self.spec['layouts'][n['layout']],env.copy())
            elif kind=='layer':env[n['name']]=Image.new('RGBA',tuple(v(n['size'])),v(n.get('color')))
            else:
                target=env[n.get('target','im')];args=v(n.get('args',[]));kw=v(n.get('kwargs',{}))
                aliases={'chip-y':'y','chip-k':'k','chip-g':'g','sticker-r':'r'}
                if kind in aliases:kw['kind']=aliases[kind];kind='chip'
                if kind=='bar':kind='rounded'
                if kind in ('line','ellipse'):getattr(ImageDraw.Draw(target),kind)(*args,**kw)
                elif kind in ('text','rounded','chip','tag','kinetic','card','count','place','alpha_paste'):
                    getattr(p,kind)(target,*args,**kw)
                else:raise ValueError(f'Unknown element type: {kind}')

    def gfx(self,f):
        t=self.t
        sid=next(s['seg'] for s in t['segments'] if s['start']<=f<s['start']+s['frames'])
        mode=next(m for m in reversed(t['modes']) if m['start']<=f)
        im=p.paper() if mode['mode']=='B' else Image.new('RGBA',(p.W,p.H))
        tr=t['triggers'];on=lambda key:key in tr[sid] and f>=tr[sid][key]
        env=dict(self.functions, **self.spec.get('variables',{}))
        env.update({name:getattr(p,name) for name in ['PAPER','INK','YELLOW','RED','BLUE','GREEN','GRAY']})
        env.update(im=im,sid=sid,f=f,mode=mode,T=t,age=lambda key:f-tr[sid][key],on=on,
            event_age=lambda s,k,frame:frame-tr[s][k],
            stage=lambda s,frame,keys:next((k for k in reversed(keys) if k in tr[s] and frame>=tr[s][k]),None))
        self.draw(self.segments[sid]['elements'],env)
        return im

    def subs(self,f):
        im=Image.new('RGBA',(p.W,p.H));c=next((c for c in self.t['captions'] if c['start']<=f<c['end']),None)
        if c:
            shade=Image.new('RGBA',im.size)
            ImageDraw.Draw(shade).text((963,1016),c['text'],font=p.font(46,'Bold'),fill=(0,0,0,170),anchor='ms',stroke_width=5,stroke_fill=(0,0,0,170))
            im.alpha_composite(shade.filter(ImageFilter.GaussianBlur(4)))
            p.text(im,c['text'],960,1010,46,'white',anchor='ms',stroke=5,weight='Bold')
        return im

    def signature(self,f):
        sid=next(s['seg'] for s in self.t['segments'] if s['start']<=f<s['start']+s['frames'])
        mode=next(m for m in reversed(self.t['modes']) if m['start']<=f)
        return (sid,mode['mode'],tuple((e['key'],min(self.spec.get('settle_frames',f+1),f-e['start'])) for e in self.t.get('events',[]) if e['seg']==sid and e['start']<=f))

def main():
    a=argparse.ArgumentParser(description=__doc__)
    for n in ['spec','timeline','fonts','stills','output']:a.add_argument('--'+n,required=True,type=Path)
    a.add_argument('--frames',help='Comma separated frame numbers; omitted renders the whole film')
    args=a.parse_args();r=Renderer(load(args.spec),load(args.timeline),args.fonts,args.stills)
    frames=[int(f) for f in args.frames.split(',')] if args.frames else range(r.t['total_frames'])
    for name in ['gfx','subs']:(args.output/name).mkdir(parents=True,exist_ok=True)
    last=None;lastpath=None;captions={}
    for f in frames:
        if not 0<=f<r.t['total_frames']:raise ValueError(f'Invalid frame: {f}')
        path=args.output/'gfx'/f'{f:05}.png';sig=r.signature(f)
        path.unlink(missing_ok=True)
        if sig==last and lastpath and lastpath!=path:os.link(lastpath,path)
        else:r.gfx(f).save(path,compress_level=3)
        last=sig;lastpath=path
        c=next((c['text'] for c in r.t['captions'] if c['start']<=f<c['end']),'')
        sp=args.output/'subs'/path.name;sp.unlink(missing_ok=True)
        if c in captions and captions[c]!=sp:os.link(captions[c],sp)
        else:r.subs(f).save(sp,compress_level=3);captions[c]=sp
        if f%250==0:print(f'Rendered {f}/{r.t["total_frames"]}',flush=True)
    (args.output/'subs.srt').write_text(srt(r.t['captions'],r.t['fps']),encoding='utf-8')

if __name__=='__main__':main()

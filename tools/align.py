"""Align original manuscript to whisper.cpp character times, never replace manuscript text."""
import argparse, difflib, json, math, re
from pathlib import Path
def chinese(n):
    n=int(n)
    if n==0:return '零'
    if n<0:return '负'+chinese(-n)
    if n>=100000000:
        a,b=divmod(n,100000000)
        return chinese(a)+'亿'+('零' if 0<b<10000000 else '')+(chinese(b) if b else '')
    if n>=10000:
        a,b=divmod(n,10000)
        return chinese(a)+'万'+('零' if 0<b<1000 else '')+(chinese(b) if b else '')
    out='';zero=False
    for unit,suffix in [(1000,'千'),(100,'百'),(10,'十'),(1,'')]:
        v,n=divmod(n,unit)
        if v:
            if zero:out+='零'
            out+=('' if v==1 and unit==10 and not out else '零一二三四五六七八九'[v])+suffix
            zero=False
        elif out and n:zero=True
    return out
def plain(s):return ''.join(ch for ch in s if ch.isalnum())
def recognition(items):
    chars=[]; times=[]
    for item in items:
        text=plain(item['text']);a=item['offsets']['from'];b=item['offsets']['to']
        for k,c in enumerate(text):
            chars.append(c);times.append((a+(b-a)*k/max(1,len(text)),a+(b-a)*(k+1)/max(1,len(text))))
    # Join adjacent numeric tokens BEFORE conversion: recognition may split one number.
    out='';ts=[];i=0
    while i<len(chars):
        j=i+1
        if chars[i].isdigit():
            while j<len(chars) and chars[j].isdigit():j+=1
            word=chinese(''.join(chars[i:j]))
        else:word=chars[i]
        a,b=times[i][0],times[j-1][1]
        for k,c in enumerate(word):
            out+=c;ts.append((a+(b-a)*k/len(word),a+(b-a)*(k+1)/len(word)))
        i=j
    return out,ts
def align(text, items, rec, fps=25):
    src=plain(re.sub(r"[0-9]+", lambda m: chinese(m.group()), text));heard,ht=recognition(items);out=[None]*len(src);changes=[]
    for op,a,b,c,d in difflib.SequenceMatcher(None,src,heard,autojunk=False).get_opcodes():
        if op=='equal':out[a:b]=ht[c:d]
        elif a<b:
            # Equal blocks anchor substitutions and omissions on both sides.
            t0=ht[c][0] if c<len(ht) else ht[-1][1]
            t1=ht[d-1][1] if d>c else t0
            for k in range(a,b):out[k]=(t0+(t1-t0)*(k-a)/(b-a),t0+(t1-t0)*(k-a+1)/(b-a))
            changes.append(dict(original=src[a:b],recognized=heard[c:d],operation=op))
    assert all(x is not None for x in out)
    frames=[];last=rec
    for a,b in out:
        start=max(last,rec+math.floor(a*fps/1000+.5));end=max(start+1,rec+math.floor(b*fps/1000+.5))
        frames.append([start,end]);last=start
    return dict(text=src,chars=frames,recognition=heard,repairs=changes)

def make_timeline(spec, edl, base):
    from common import load
    fps = edl['fps']; total = edl['total_frames']
    segments = {s['seg']: s for s in edl['segments']}
    aligned = {}
    definitions = {s['id']: s for s in spec['segments']}
    for vo in edl['vo']:
        sid = vo['id']; d = definitions[sid]
        text = (base/d['text']).read_text(encoding='utf-8').strip()
        items = load(base/d['timing'])['transcription']
        if not items: raise ValueError(f'Empty timing: {sid}')
        aligned[sid] = align(text, items, vo['rec'], fps)
    events=[]; triggers={}; used={}
    for d in spec['segments']:
        sid=d['id']; triggers[sid]={}
        for beat in d['beats']:
            word=beat.get('word', '开头')
            if 'after' in beat:
                frame=triggers[sid][beat['after']]
            elif word=='开头': frame=segments[sid]['start']
            else:
                a=aligned[sid]; key=(sid,word)
                needle=plain(re.sub(r'[0-9]+', lambda m:chinese(m.group()),word))
                i=a['text'].find(needle, used.get(key,0))
                if i<0: raise ValueError(f'Cannot align {sid} @{word}')
                used[key]=i+len(needle); frame=a['chars'][i][0]
            frame+=beat.get('offset',0)
            if not segments[sid]['start']<=frame<segments[sid]['start']+segments[sid]['frames']:
                raise ValueError(f'Trigger outside segment: {sid}/{beat["key"]}')
            e=dict(beat,seg=sid,start=frame,id=f"{sid}_{beat['key']}",end=segments[sid]['start']+segments[sid]['frames'])
            events.append(e);triggers[sid][beat['key']]=frame
    events.sort(key=lambda e:(e['start'],e['seg'],e['key']))
    modes=[dict(start=e['start'], mode=e['mode'],seg=e['seg'],clip=e.get('clip')) for e in events if 'mode' in e]
    if not modes or modes[0]['start']!=0:raise ValueError('First beat must set F/B at frame zero')
    for i,m in enumerate(modes):m['end']=modes[i+1]['start'] if i+1<len(modes) else total
    captions=[]
    for sid,a in aligned.items():
        original=(base/definitions[sid]['text']).read_text(encoding='utf-8').strip();cursor=0
        for clause in re.split(r'[，。？！；：、,!?;:\n]+',original):
            p=plain(re.sub(r'[0-9]+',lambda m:chinese(m.group()),clause))
            if not p:continue
            pieces=[]
            while len(p)>16:
                cut=16
                for w in ['的','在','让','比','而','还','就','是','有']:
                    options=[i for i,c in enumerate(p[:17]) if c==w and 8<=i<=16]
                    if options:cut=options[-1];break
                pieces.append(p[:cut]);p=p[cut:]
            pieces.append(p)
            for p in pieces:
                i=a['text'].find(p,cursor)
                if i<0:raise ValueError(f'Caption missing: {sid}/{p}')
                start=a['chars'][i][0];stop=min(segments[sid]['start']+segments[sid]['frames'],a['chars'][i+len(p)-1][1])
                captions.append(dict(seg=sid,text=p,start=start,end=max(start+1,stop)));cursor=i+len(p)
    captions.sort(key=lambda c:c['start'])
    for i,c in enumerate(captions[:-1]):c['end']=min(c['end'],captions[i+1]['start'])
    for i,c in enumerate(captions):
        limit=captions[i+1]['start'] if i+1<len(captions) else total
        c['end']=min(limit,segments[c['seg']]['start']+segments[c['seg']]['frames'],c['end']+round(.16*fps))
    return dict(width=spec['width'],height=spec['height'],fps=fps,total_frames=total,
                segments=edl['segments'],events=events,triggers=triggers,modes=modes,
                captions=captions,stills=spec.get('stills',[]),alignment=aligned)

def main():
    from common import load,save,srt
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spec',required=True,type=Path);p.add_argument('--edl',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();t=make_timeline(load(a.spec),load(a.edl),a.spec.parent)
    save(a.output,t);a.output.with_suffix('.srt').write_text(srt(t['captions'],t['fps']),encoding='utf-8')
    print(f"Aligned {len(t['events'])} beats, {len(t['captions'])} captions")

if __name__=='__main__':main()

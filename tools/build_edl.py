"""Build segment timing from WAV durations, or footage cuts from an aligned timeline."""
import argparse
import math
from pathlib import Path
from common import load,save,duration

def segments(spec,base,wav_dir=None):
    fps=spec['fps'];t=0;out=dict(fps=fps,total_frames=0,segments=[],vo=[])
    for s in spec['segments']:
        if 'wav' in s:
            path=wav_dir/f"{s['id']}.wav" if wav_dir else base/s['wav']
            length=spec.get('lead_seconds',.25)+duration(path)+spec.get('tail_seconds',.45)
            # Store portable paths only; mix.py receives the actual directory separately.
            out['vo'].append(dict(id=s['id'],path=s['wav'],rec=round((t+spec.get('lead_seconds',.25))*fps)))
        else:length=s['seconds']
        start=round(t*fps);end=round((t+length)*fps)
        out['segments'].append(dict(seg=s['id'],start=start,frames=end-start));t+=length
    out['total_frames']=round(t*fps);return out

def footage(timeline,folder,fade_seconds=1.2):
    fps=timeline['fps'];total=timeline['total_frames']
    live=[m for m in timeline['modes'] if m['mode']=='F'];shots=[];lengths={}
    if not live or live[0]['start']!=0:raise ValueError('At least one F beat at frame zero is required for V1')
    for i,m in enumerate(live):
        stop=live[i+1]['start'] if i+1<len(live) else total
        rec=m['start'];remaining=stop-rec;clip=str(m['clip'])
        if clip not in lengths:lengths[clip]=duration(folder/f'{clip}.mp4')
        length=lengths[clip]
        while remaining:
            src=1.0 if length>=remaining/fps+1 else 0.0
            capacity=math.floor((length-src)*fps+1e-5)
            if capacity<1:raise ValueError(f'Empty clip: {clip}')
            n=min(remaining,capacity);shots.append(dict(seg=m['seg'],clip=clip,rec=rec,frames=n,src_in_sec=src))
            rec+=n;remaining-=n
    fade=min(total,round(fade_seconds*fps))
    return dict(fps=fps,total_frames=total,shots=shots,ending=dict(start=total-fade,frames=fade,operation='fade_to_black'))

def main():
    p=argparse.ArgumentParser(description=__doc__);m=p.add_mutually_exclusive_group(required=True)
    m.add_argument('--spec',type=Path);m.add_argument('--timeline',type=Path)
    p.add_argument('--wav-dir',type=Path);p.add_argument('--footage',type=Path)
    p.add_argument('--fade-seconds',type=float,default=1.2);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    if a.spec:out=segments(load(a.spec),a.spec.parent,a.wav_dir)
    else:
        if not a.footage:p.error('--timeline requires --footage')
        out=footage(load(a.timeline),a.footage,a.fade_seconds)
    save(a.output,out)
if __name__=='__main__':main()

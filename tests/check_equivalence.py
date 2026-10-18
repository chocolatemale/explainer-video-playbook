"""Render ten distributed samples and compare raw RGBA channels with the original."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
FRAMES=[10,150,600,932,1250,1560,2350,3080,3500,4580]

def main():
    p=argparse.ArgumentParser();p.add_argument('--original',required=True,type=Path)
    p.add_argument('--work',required=True,type=Path);p.add_argument('--fonts',required=True,type=Path)
    p.add_argument('--output',default=ROOT/'tests/equivalence.json',type=Path)
    a=p.parse_args();spec=ROOT/'examples/city-choice/beats.json';edl=ROOT/'examples/city-choice/edl.json'
    a.work.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(ROOT/'tools/align.py'),'--spec',str(spec),'--edl',str(edl),'--output',str(a.work/'timeline.json')],check=True)
    subprocess.run([sys.executable,str(ROOT/'tools/render.py'),'--spec',str(spec),'--timeline',str(a.work/'timeline.json'),
        '--fonts',str(a.fonts),'--stills',str(a.original/'program/stills'),'--output',str(a.work/'layers'),'--frames',','.join(map(str,FRAMES))],check=True)
    records=[]
    timeline=json.loads((a.work/'timeline.json').read_text(encoding='utf-8'))
    for f in FRAMES:
        means={}
        for layer in ['gfx','subs']:
            expected=Image.open(a.original/'program/out'/layer/f'{f:05}.png').convert('RGBA')
            actual=Image.open(a.work/'layers'/layer/f'{f:05}.png').convert('RGBA')
            assert actual.size==expected.size
            means[layer]=sum(ImageStat.Stat(ImageChops.difference(actual,expected)).mean)/4
        mode=next(m['mode'] for m in reversed(timeline['modes']) if m['start']<=f)
        caption=next((c['text'] for c in timeline['captions'] if c['start']<=f<c['end']),'')
        records.append(dict(frame=f,mode=mode,caption=caption,mean_absolute_error_rgba=means))
    avg=sum(v for r in records for v in r['mean_absolute_error_rgba'].values())/20
    out=dict(method='mean absolute difference of all RGBA channels, 0–255',frames=records,mean=avg,threshold=3,passed=all(v<3 for r in records for v in r['mean_absolute_error_rgba'].values()))
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'Mean pixel difference: {avg}')
    assert out['passed']
if __name__=='__main__':main()

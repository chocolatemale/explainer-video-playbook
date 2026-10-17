"""Composite storyboard samples into four-column contact sheets, including short beats."""
import argparse
import json
import subprocess
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw
from common import load,save

def frame(edl,footage,layers,f):
    s=next(s for s in edl['shots'] if s['rec']<=f<s['rec']+s['frames'])
    source=s['src_in_sec']+(f-s['rec'])/edl['fps']
    raw=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-ss',str(source),'-i',str(footage/f"{s['clip']}.mp4"),
        '-frames:v','1','-vf','scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080',
        '-f','image2pipe','-vcodec','png','-threads','1','-'])
    im=Image.open(BytesIO(raw)).convert('RGBA')
    for layer in ['gfx','subs']:im.alpha_composite(Image.open(layers/layer/f'{f:05}.png').convert('RGBA'))
    return im

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['timeline','edl','footage','layers','output']:p.add_argument('--'+n,required=True,type=Path)
    p.add_argument('--boards',action='store_true',help='Sample B beats +1.2 seconds rather than +0.7')
    a=p.parse_args();t=load(a.timeline);e=load(a.edl);a.output.mkdir(parents=True,exist_ok=True)
    cells=[];index=[];events=t['events']
    for i,event in enumerate(events):
        stop=events[i+1]['start'] if i+1<len(events) else t['total_frames']
        mode=next(m['mode'] for m in reversed(t['modes']) if m['start']<=event['start'])
        if a.boards and mode!='B':continue
        offset=round(t['fps']*(1.2 if a.boards else .7))
        f=min(t['total_frames']-1,event['start']+offset)
        samples=[f]
        if 0<stop-event['start']<offset:samples.append((event['start']+stop-1)//2)
        for f in samples:
            im=frame(e,a.footage,a.layers,f)
            cell=Image.new('RGB',(480,300),'#F4F1E8');cell.paste(im.convert('RGB').resize((480,270)),(0,30))
            label=f"{event['id']}  frame {f}";ImageDraw.Draw(cell).text((8,8),label,fill='#161616')
            cells.append(cell);index.append(dict(beat=event['id'],trigger=event['start'],sample=f,short=stop-event['start']<offset,crossed_cut=f>=stop))
    for i in range(0,len(cells),12):
        batch=cells[i:i+12];sheet=Image.new('RGB',(1920,((len(batch)+3)//4)*300),'#C9C4B8')
        for k,cell in enumerate(batch):sheet.paste(cell,((k%4)*480,(k//4)*300))
        sheet.save(a.output/f'{i//12+1:02}.jpg',quality=90)
    save(a.output/'index.json',index)
if __name__=='__main__':main()

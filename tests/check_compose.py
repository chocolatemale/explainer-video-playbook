"""Decode every packet/frame and assert the requested preview duration."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from common import probe

def main():
    p=argparse.ArgumentParser();p.add_argument('video',type=Path)
    p.add_argument('--seconds',type=float,default=20);p.add_argument('--output',type=Path)
    a=p.parse_args()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(a.video),'-f','null','-'],check=True)
    data=probe(a.video);seconds=float(data['format']['duration'])
    assert abs(seconds-a.seconds)<=.1,(seconds,a.seconds)
    video=next(s for s in data['streams'] if s['codec_type']=='video')
    audio=next(s for s in data['streams'] if s['codec_type']=='audio')
    out=dict(fully_decoded=True,duration=seconds,expected_duration=a.seconds,tolerance=.1,
             video_codec=video['codec_name'],audio_codec=audio['codec_name'],frames=int(video['nb_frames']))
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

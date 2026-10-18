"""Normalize V1 shot-by-shot, then composite RGBA graphics, captions and a mix."""
import argparse
import subprocess
import tempfile
from pathlib import Path
from common import load

def run(cmd):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,cmd)],check=True)

def codec(hw):
    return ['-c:v','h264_videotoolbox','-b:v','12M'] if hw else ['-c:v','libx264','-preset','fast','-crf','18']

def layer_args(path,fps):
    return ['-framerate',str(fps),'-start_number','0','-i',str(path)] if '%' in str(path) else ['-i',str(path)]

def compose(edl,footage,gfx,subs,mix,output,seconds=None,hw=False,fade_seconds=1.2):
    fps=edl['fps'];total=edl['total_frames']
    frames=min(total,round(seconds*fps)) if seconds else total
    if frames<1:raise ValueError('Duration must be positive')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    # Temporary media stays outside the repo; independent encoding avoids opening every original at once.
    with tempfile.TemporaryDirectory(prefix='playbook-compose-') as tmp:
        tmp=Path(tmp);parts=[];cursor=0
        for shot in edl['shots']:
            if shot['rec']>=frames:break
            if shot['rec']!=cursor:raise ValueError('V1 EDL must be contiguous from frame zero')
            n=min(shot['frames'],frames-shot['rec']);part=tmp/f'{len(parts):04}.mp4'
            run(['-threads','2','-ss',shot['src_in_sec'],'-i',Path(footage)/f"{shot['clip']}.mp4",
                '-an','-vf',f'fps={fps},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,tpad=stop_mode=clone:stop_duration={n/fps}',
                '-frames:v',n,*codec(hw),'-pix_fmt','yuv420p',part])
            parts.append(part);cursor+=n
        if cursor!=frames:raise ValueError('V1 EDL does not cover requested duration')
        # File names here are generated numeric names under our own temporary directory.
        listing=tmp/'concat.txt';listing.write_text(''.join(f"file '{p.name}'\n" for p in parts),encoding='utf-8')
        run(['-f','concat','-safe','1','-i',listing,'-c','copy',tmp/'base.mp4'])
        duration=frames/fps
        fade=min(fade_seconds,total/fps);start=(total/fps)-fade
        # A preview preserves the film's actual ending: no premature fade at the preview cutoff.
        vf='[0:v][1:v]overlay=shortest=1:format=auto[v1];[v1][2:v]overlay=shortest=1:format=auto'
        vf+=f',fade=t=out:st={start}:d={fade},format=yuv420p[v]'
        run(['-threads','2','-i',tmp/'base.mp4',*layer_args(gfx,fps),*layer_args(subs,fps),'-i',mix,
            '-filter_complex_threads','1','-filter_complex',vf,'-map','[v]','-map','3:a:0',
            '-frames:v',frames,'-t',duration,*codec(hw),'-c:a','aac','-b:a','256k','-ar','48000',
            '-movflags','+faststart',output])
    print(f'Composed {frames} frames ({frames/fps:.3f} seconds)')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['edl','footage','gfx','subs','mix','output']:p.add_argument('--'+n,required=True,type=Path)
    p.add_argument('--duration',type=float);p.add_argument('--fade-seconds',default=1.2,type=float)
    p.add_argument('--hw',action='store_true',help='Use macOS h264_videotoolbox instead of libx264')
    a=p.parse_args();compose(load(a.edl),a.footage,a.gfx,a.subs,a.mix,a.output,a.duration,a.hw,a.fade_seconds)
if __name__=='__main__':main()

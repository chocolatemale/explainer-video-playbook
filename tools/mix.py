"""Place one WAV per segment, duck music with VO and perform measured two-pass loudnorm."""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path
from common import load

def ffmpeg(args,capture=False):
    r=subprocess.run(['ffmpeg','-hide_banner','-y',*map(str,args)],check=True,capture_output=capture,text=capture)
    return r.stderr if capture else ''

def mix(edl,wavs,music,output):
    fps=edl['fps'];duration=edl['total_frames']/fps
    if not edl['vo']:raise ValueError('No voice segments')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='playbook-mix-') as td:
        premix=Path(td)/'premix.wav';args=[];filters=[];voices=[]
        for i,v in enumerate(edl['vo']):
            path=Path(wavs)/f"{v['id']}.wav"
            args+=['-i',path];delay=round(v['rec']/fps*1000)
            filters.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={delay}|{delay}[vo{i}]')
            voices.append(f'[vo{i}]')
        music_index=len(voices);args+=['-stream_loop','-1','-i',music]
        filters.append(''.join(voices)+f'amix=inputs={len(voices)}:normalize=0,apad,atrim=duration={duration},asplit=2[voice][key]')
        filters.append(f'[{music_index}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-15dB[music]')
        filters.append('[music][key]sidechaincompress=threshold=0.015:ratio=10:attack=30:release=600[ducked]')
        filters.append(f'[voice][ducked]amix=inputs=2:normalize=0,atrim=duration={duration},afade=t=out:st={max(0,duration-1.2)}:d={min(duration,1.2)}[out]')
        ffmpeg([*args,'-filter_complex',';'.join(filters),'-map','[out]','-t',duration,'-c:a','pcm_s24le',premix],True)
        stats=ffmpeg(['-i',premix,'-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-'],True)
        measured=json.loads(re.findall(r'\{[^{}]+\}',stats)[-1])
        for key in ['input_i','input_tp','input_lra','input_thresh','target_offset']:
            if measured[key] in ('-inf','inf'):raise ValueError('Mix is silent or invalid for loudnorm')
        norm=('loudnorm=I=-14:TP=-1:LRA=11:linear=true:print_format=json'
              f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
              f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}")
        ffmpeg(['-i',premix,'-af',norm,'-ar','48000','-ac','2','-c:a','pcm_s24le',output],True)
        output.with_suffix('.loudnorm.json').write_text(json.dumps(measured,indent=2)+'\n')
    print('Mixed VO + ducked music; two-pass target −14 LUFS / −1 dBTP')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['edl','wav-dir','music','output']:p.add_argument('--'+n,required=True,type=Path)
    a=p.parse_args();mix(load(a.edl),a.wav_dir,a.music,a.output)
if __name__=='__main__':main()

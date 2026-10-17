"""Extract card-library stills without redistributing the downloaded videos."""
import argparse
import subprocess
from pathlib import Path
from common import load

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['spec','footage','output']:p.add_argument('--'+n,required=True,type=Path)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    for clip in load(a.spec).get('stills',[]):
        dest=a.output/f'{clip}.jpg'
        if dest.exists():continue
        subprocess.run(['ffmpeg','-v','error','-ss','2','-i',str(a.footage/f'{clip}.mp4'),'-frames:v','1',
            '-vf','scale=1000:563:force_original_aspect_ratio=increase,crop=1000:563','-q:v','2','-update','1',str(dest)],check=True)
        if not dest.exists():raise ValueError(f'No still for {clip}; clip shorter than 2 seconds?')
if __name__=='__main__':main()

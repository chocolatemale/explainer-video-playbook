"""Integration checks with generated local media; no third-party files needed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from common import probe

class MediaTests(unittest.TestCase):
    def test_mix_and_composite_decode(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as td:
            d=Path(td);(d/'wav').mkdir();(d/'footage').mkdir()
            def ff(*args):subprocess.run(['ffmpeg','-v','error','-y',*map(str,args)],check=True)
            ff('-f','lavfi','-i','sine=frequency=350:duration=2','-ar','48000',d/'wav/a.wav')
            ff('-f','lavfi','-i','sine=frequency=150:duration=4','-ar','48000',d/'music.wav')
            edl={'fps':25,'total_frames':100,'vo':[{'id':'a','rec':10}],
                 'shots':[{'seg':'a','clip':'1','rec':0,'frames':100,'src_in_sec':0}]}
            (d/'edl.json').write_text(json.dumps(edl),encoding='utf-8')
            subprocess.run([sys.executable,str(ROOT/'tools/mix.py'),'--edl',str(d/'edl.json'),
                '--wav-dir',str(d/'wav'),'--music',str(d/'music.wav'),'--output',str(d/'mix.wav')],check=True)
            self.assertAlmostEqual(float(probe(d/'mix.wav')['format']['duration']),4,places=2)
            self.assertTrue((d/'mix.loudnorm.json').exists())
            ff('-f','lavfi','-i','color=c=blue:s=320x180:r=25:d=4','-c:v','libx264',d/'footage/1.mp4')
            Image.new('RGBA',(320,180),(0,0,0,0)).save(d/'00000.png')
            ff('-loop','1','-i',d/'00000.png','-t','4','-r','25','-c:v','qtrle',d/'layer.mov')
            subprocess.run([sys.executable,str(ROOT/'tools/compose_ffmpeg.py'),'--edl',str(d/'edl.json'),
                '--footage',str(d/'footage'),'--gfx',str(d/'layer.mov'),'--subs',str(d/'layer.mov'),
                '--mix',str(d/'mix.wav'),'--output',str(d/'out.mp4')],check=True)
            ff('-xerror','-i',d/'out.mp4','-f','null','-')
            data=probe(d/'out.mp4');self.assertAlmostEqual(float(data['format']['duration']),4,places=2)
            raw=subprocess.check_output(['ffmpeg','-v','error','-sseof','-0.04','-i',str(d/'out.mp4'),
                '-frames:v','1','-vf','scale=1:1,format=gray','-f','rawvideo','-'])
            self.assertTrue(raw and raw[0]<8,raw)

if __name__=='__main__':unittest.main()

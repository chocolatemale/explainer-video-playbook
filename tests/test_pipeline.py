import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

class PipelineTests(unittest.TestCase):
    def test_numeric_alignment(self):
        import align
        self.assertEqual(align.chinese(157), '一百五十七')
        self.assertEqual(align.chinese(10008), '一万零八')
        self.assertEqual(align.chinese(100000000), '一亿')
        items = [{'text': '15', 'offsets': {'from': 0, 'to': 200}},
                 {'text': '7万', 'offsets': {'from': 200, 'to': 500}}]
        text, times = align.recognition(items)
        self.assertEqual(text, '一百五十七万')
        a = align.align('157万', items, 10, 25)
        self.assertEqual(a['text'], '一百五十七万')
        self.assertEqual(a['chars'][0][0], 10)
        self.assertTrue(all(a['chars'][i][0] <= a['chars'][i+1][0] for i in range(len(a['chars'])-1)))

    def test_renderer_is_data_driven_and_random_access(self):
        from render import Renderer
        timeline = {'width': 1920, 'height': 1080, 'fps': 25, 'total_frames': 30,
                    'segments': [{'seg': 'demo', 'start': 0, 'frames': 30}],
                    'triggers': {'demo': {'cue': 0}}, 'modes': [{'start': 0, 'mode': 'B'}],
                    'captions': [{'text': '新主题', 'start': 0, 'end': 30}]}
        spec = {'variables': {}, 'layouts': {}, 'segments': [{'id': 'demo', 'elements': [
            {'type': 'chip-y', 'args': ['新主题', 960, 400, 80], 'kwargs': {'age': {'expr': "age('cue')"}}}]}]}
        r = Renderer(spec, timeline, Path(os.environ.get('PLAYBOOK_FONTS', ROOT / 'build/fonts')), ROOT / 'build/stills')
        self.assertEqual(r.gfx(18).tobytes(), r.gfx(18).tobytes())
        self.assertNotEqual(r.gfx(0).tobytes(), r.gfx(18).tobytes())
        self.assertEqual(r.gfx(18).getchannel('A').getextrema(), (255, 255))
        self.assertEqual(r.subs(1).size, (1920,1080))
        with self.assertRaises(ValueError): r.value({'expr': "__import__('os').getcwd()"}, {})

    def test_fcpxml_counts(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'timeline.fcpxml'
            subprocess.run([sys.executable, str(ROOT/'tools/export_fcpxml.py'),
                '--edl', str(ROOT/'examples/city-choice/v1_edl.json'),
                '--footage', d, '--gfx', str(Path(d)/'gfx.mov'), '--subs', str(Path(d)/'subs.mov'),
                '--mix', str(Path(d)/'mix.wav'), '--srt', str(ROOT/'examples/city-choice/subs.srt'),
                '--output', str(out)], check=True)
            subprocess.run([sys.executable, str(ROOT/'tests/check_fcpxml.py'), str(out),
                            str(ROOT/'examples/city-choice/v1_edl.json')], check=True)

if __name__ == '__main__': unittest.main()

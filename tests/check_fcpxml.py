"""Structural checks, not a claim that a particular editor imported the file."""
import json
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

def check(xml,edl):
    root=ET.parse(xml).getroot();e=json.loads(Path(edl).read_text());fps=e['fps']
    assert root.tag=='fcpxml' and root.get('version')=='1.10'
    assets=root.findall('./resources/asset');unique={str(s['clip']) for s in e['shots']}
    assert len(assets)==len(unique)+3,(len(assets),len(unique)+3)
    resources=root.findall('./resources/*');ids={r.get('id') for r in resources}
    assert len(ids)==len(resources)
    clips=root.findall('.//spine/asset-clip');all_clips=root.findall('.//asset-clip')
    assert len(clips)==len(e['shots'])
    assert len(all_clips)==len(e['shots'])+3
    for clip in all_clips:assert clip.get('ref') in ids
    t=lambda s:Fraction(s.removesuffix('s'))
    for c,s in zip(clips,e['shots']):
        assert t(c.get('offset'))==Fraction(s['rec'],fps)
        assert t(c.get('duration'))==Fraction(s['frames'],fps)
        assert t(c.get('start'))==Fraction(str(s['src_in_sec']))
    connected=clips[0].findall('./asset-clip')
    assert {c.get('lane') for c in connected}=={'1','2','-1'}
    for c in connected:
        assert t(c.get('duration'))==Fraction(e['total_frames'],fps)
        assert t(c.get('offset'))==t(clips[0].get('start'))
    out=dict(version='1.10',assets=len(assets),footage_resources=len(unique),v1_clips=len(clips),connected_clips=3,total_clips=len(all_clips),total_frames=e['total_frames'])
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':check(*sys.argv[1:])

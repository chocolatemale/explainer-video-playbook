"""Export a four-layer FCPXML 1.10 timeline with portable relative media references."""
import argparse
import shutil
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from common import load,probe

def tm(frames,fps):
    f=Fraction(str(frames))/fps
    return f'{f.numerator}/{f.denominator}s'

def export(edl,footage,gfx,subs,mix,output,srt):
    fps=edl['fps'];total=edl['total_frames'];output=Path(output)
    root=ET.Element('fcpxml',version='1.10');resources=ET.SubElement(root,'resources')
    ET.SubElement(resources,'format',id='r_format',name=f'FFVideoFormat1080p{fps}',frameDuration=tm(1,fps),width='1920',height='1080',colorSpace='1-1-1 (Rec. 709)')
    ids={};formats={};asset_durations={}
    def asset(key,path,audio=False):
        rid=f'r_asset{len(ids)+1}';ids[key]=rid
        # References are relative to XML, so the package can move without publishing local paths.
        import os
        uri=Path(os.path.relpath(Path(path).resolve(),output.parent.resolve())).as_posix()
        from urllib.parse import quote
        uri=quote(uri,safe='/')
        fmt='r_format';dur=tm(total,fps)
        if Path(path).exists():
            data=probe(path);dur=tm(Fraction(data['format']['duration'])*fps,fps)
            video=next((s for s in data['streams'] if s['codec_type']=='video'),None)
            if video:
                rate=Fraction(video['avg_frame_rate']);keyfmt=(video['width'],video['height'],rate)
                if rate<=0:rate=Fraction(fps)
                if keyfmt not in formats:
                    fmtid=f'r_source_format{len(formats)+1}';formats[keyfmt]=fmtid
                    ET.SubElement(resources,'format',id=fmtid,frameDuration=f'{rate.denominator}/{rate.numerator}s',width=str(video['width']),height=str(video['height']),colorSpace='1-1-1 (Rec. 709)')
                fmt=formats[keyfmt]
        else:
            need=max((Fraction(str(s['src_in_sec']))+Fraction(s['frames'],fps) for s in edl['shots'] if str(s['clip'])==key),default=Fraction(total,fps))
            dur=tm(need*fps,fps)
        attrs=dict(id=rid,name=Path(path).name,start='0s',duration=dur,hasVideo='0' if audio else '1',hasAudio='1' if audio else '0')
        if audio:attrs.update(audioSources='1',audioChannels='2',audioRate='48000')
        else:attrs.update(format=fmt,videoSources='1')
        a=ET.SubElement(resources,'asset',attrs);ET.SubElement(a,'media-rep',kind='original-media',src=uri)
        asset_durations[rid]=dur
        return rid
    for clip in sorted({str(s['clip']) for s in edl['shots']}):asset(clip,Path(footage)/f'{clip}.mp4')
    for key,path in [('gfx',gfx),('subs',subs),('mix',mix)]:asset(key,path,key=='mix')
    library=ET.SubElement(root,'library');event=ET.SubElement(library,'event',name='Explainer')
    project=ET.SubElement(event,'project',name='Explainer timeline')
    seq=ET.SubElement(project,'sequence',format='r_format',duration=tm(total,fps),tcStart='0s',tcFormat='NDF',audioLayout='stereo',audioRate='48k')
    spine=ET.SubElement(seq,'spine');first=None;cursor=0
    for s in edl['shots']:
        if s['rec']!=cursor:raise ValueError('V1 must be contiguous from zero')
        cursor+=s['frames']
        c=ET.SubElement(spine,'asset-clip',name=f"V1 {s['seg']} {s['clip']}",ref=ids[str(s['clip'])],offset=tm(s['rec'],fps),start=tm(Fraction(str(s['src_in_sec']))*fps,fps),duration=tm(s['frames'],fps))
        ET.SubElement(c,'adjust-conform',type='fill')
        if first is None:first=c
    if cursor!=total:raise ValueError('V1 duration differs from film')
    # Connected clips use the source time of the parent anchor, not sequence time zero.
    anchor=first.get('start')
    for key,lane in [('gfx',1),('subs',2),('mix',-1)]:
        attrs=dict(name=key,ref=ids[key],lane=str(lane),offset=anchor,start='0s',duration=tm(total,fps))
        if key=='mix':attrs['audioRole']='dialogue'
        ET.SubElement(first,'asset-clip',attrs)
    output.parent.mkdir(parents=True,exist_ok=True)
    ET.indent(root,space='  ')
    output.write_bytes(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n'+ET.tostring(root,encoding='utf-8'))
    if Path(srt).resolve()!=output.with_suffix('.srt').resolve():shutil.copyfile(srt,output.with_suffix('.srt'))
    return root

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['edl','footage','gfx','subs','mix','srt','output']:p.add_argument('--'+n,required=True,type=Path)
    a=p.parse_args();export(load(a.edl),a.footage,a.gfx,a.subs,a.mix,a.output,a.srt)
if __name__=='__main__':main()

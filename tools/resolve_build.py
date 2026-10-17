"""Optional Resolve Studio assembly. External API or explicitly supplied Resolve object."""
import argparse
import math
from pathlib import Path
from common import load

def build(config,resolve=None):
    if resolve is None:
        import DaVinciResolveScript as dvr
        resolve=dvr.scriptapp('Resolve')
    if not resolve:raise RuntimeError('Resolve Studio is not running or external scripting is disabled')
    e=load(config['edl']);fps=e['fps'];pm=resolve.GetProjectManager()
    project=pm.LoadProject(config['project']) or pm.CreateProject(config['project'])
    if not project:raise RuntimeError('Could not open project')
    for k,v in {'timelineFrameRate':str(fps),'timelinePlaybackFrameRate':str(fps),
        'timelineResolutionWidth':'1920','timelineResolutionHeight':'1080'}.items():project.SetSetting(k,v)
    pool=project.GetMediaPool();shots=e['shots'];files=sorted({str((Path(config['footage'])/f"{s['clip']}.mp4").resolve()) for s in shots})
    layers=[str(Path(config[k]).resolve()) for k in ['gfx','subs','mix']]
    imported=pool.ImportMedia(files+layers) or []
    items={str(Path(c.GetClipProperty('File Path')).resolve()):c for c in imported}
    if set(files+layers)-items.keys():raise RuntimeError('Some media failed to import')
    # Always create a new timeline; never delete an existing edit with the same name.
    tl=pool.CreateEmptyTimeline(config.get('timeline','Explainer'))
    if not tl:raise RuntimeError('Choose a new, unique timeline name')
    project.SetCurrentTimeline(tl)
    while tl.GetTrackCount('video')<3:tl.AddTrack('video')
    if tl.GetTrackCount('audio')<1:tl.AddTrack('audio')
    start=tl.GetStartFrame();infos=[]
    for s in shots:
        c=items[str((Path(config['footage'])/f"{s['clip']}.mp4").resolve())]
        try:rate=float(c.GetClipProperty('FPS'))
        except (TypeError,ValueError):rate=fps
        a=round(s['src_in_sec']*rate)
        infos.append(dict(mediaPoolItem=c,startFrame=a,endFrame=a+math.ceil(s['frames']/fps*rate-1e-6),
                          mediaType=1,trackIndex=1,recordFrame=start+s['rec']))
    video=pool.AppendToTimeline(infos) or []
    overlays=pool.AppendToTimeline([dict(mediaPoolItem=items[path],startFrame=0,endFrame=e['total_frames'],mediaType=1,
                     trackIndex=i+2,recordFrame=start) for i,path in enumerate(layers[:2])]) or []
    audio=pool.AppendToTimeline([dict(mediaPoolItem=items[layers[2]],startFrame=0,endFrame=e['total_frames'],
                            mediaType=2,trackIndex=1,recordFrame=start)]) or []
    for i,name in enumerate(['V1 footage','V2 graphics','V3 captions'],1):tl.SetTrackName('video',i,name)
    tl.SetTrackName('audio',1,'Mix');pm.SaveProject()
    if len(video)!=len(shots) or len(overlays)!=2 or len(audio)!=1:raise RuntimeError('Append count mismatch; inspect timeline')
    return dict(video=len(video),graphics=len(overlays),audio=len(audio),frames=tl.GetEndFrame()-start)

def main():
    import json
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['edl','footage','gfx','subs','mix','project']:p.add_argument('--'+n,required=True)
    p.add_argument('--timeline',default='Explainer');a=p.parse_args();print(json.dumps(build(vars(a)),indent=2))
if __name__=='__main__':main()

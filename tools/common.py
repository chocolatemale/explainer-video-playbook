"""Shared file and media helpers."""
import json
import subprocess
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format',
        '-show_streams', '-of', 'json', str(path)]))

def duration(path):
    return float(probe(path)['format']['duration'])

def srt(captions, fps):
    def stamp(f):
        ms = round(f*1000/fps)
        return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
    return '\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(captions))+'\n'

#!/usr/bin/env bash
# Downloads only the selected IDs; the source JSON is reviewable before running.
set -euo pipefail
python3 - "$@" <<'PY'
import json,subprocess,sys
from pathlib import Path
from urllib.parse import urlparse
if len(sys.argv)!=3:raise SystemExit('Usage: fetch_footage.sh manifest.json output-directory')
items=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
for item in items:
    clip=str(item['id']);url=item['url']
    if not clip.isdigit():raise ValueError('ID must contain only digits')
    parsed=urlparse(url)
    if parsed.scheme!='https' or parsed.hostname!='videos.pexels.com':raise ValueError(f'Unsupported CDN URL for {clip}; harvest again')
    dest=out/f'{clip}.mp4'
    if dest.exists():continue
    part=dest.with_suffix('.mp4.part')
    subprocess.run(['curl','--fail','--location','--retry','3',url,'-o',str(part)],check=True)
    subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',str(part)],check=True)
    part.replace(dest)
PY

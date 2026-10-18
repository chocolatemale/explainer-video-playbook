#!/usr/bin/env bash
# Download OFL fonts listed in fonts.json from official GitHub / Google Fonts URLs.
set -euo pipefail
out=${1:-build/fonts}
root=$(cd "$(dirname "$0")/.." && pwd)
python3 - "$root/tools/fonts.json" "$out" <<'PY'
import json, sys, tempfile, zipfile, urllib.request
from pathlib import Path
cfg, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
data = json.loads(cfg.read_text(encoding='utf-8'))

def fetch(url, dest):
    dest = Path(dest)
    part = dest.with_name(dest.name + '.part')
    req = urllib.request.Request(url, headers={'User-Agent': 'explainer-video-playbook-font-fetch'})
    with urllib.request.urlopen(req) as r, part.open('wb') as f:
        while True:
            chunk = r.read(1024 * 256)
            if not chunk:
                break
            f.write(chunk)
    part.replace(dest)

needed = {face['file'] for preset in data['presets'].values() for face in preset.values()}
for name in needed:
    spec = data['files'][name]
    dest = out / name
    if dest.exists() and dest.stat().st_size > 1000:
        print(f'exists {name}', flush=True)
        continue
    print(f'fetch {name}', flush=True)
    if spec.get('zip_member'):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / 'font.zip'
            fetch(spec['url'], archive)
            with zipfile.ZipFile(archive) as z:
                z.extract(spec['zip_member'], td)
            Path(td, spec['zip_member']).replace(dest)
    else:
        fetch(spec['url'], dest)

for lic in data.get('licenses', []):
    dest = out / lic['as']
    if dest.exists():
        continue
    print(f'fetch {lic["as"]}', flush=True)
    fetch(lic['url'], dest)
print(f'Fonts ready in {out}')
PY

#!/usr/bin/env python3
"""Regenerate src/data/downloads.json (size + SHA-256) from public/downloads/.

Put the release files there first, named:
  PharmFlow-<version>-Android.apk
  PharmFlow-Setup-<version>-Windows.exe
then run:  python deploy/update-downloads.py
"""
import glob, hashlib, json, os, re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(root, 'public', 'downloads')


def newest(pattern):
    files = sorted(glob.glob(os.path.join(d, pattern)), key=os.path.getmtime)
    if not files:
        raise SystemExit(f'missing file matching {pattern} in {d}')
    return files[-1]


def info(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    name = os.path.basename(path)
    version = re.search(r'(\d+\.\d+\.\d+)', name).group(1)
    return {'file': '/downloads/' + name, 'size_mb': round(os.path.getsize(path) / 1048576, 1),
            'sha256': h.hexdigest(), 'version': version}


data = {'android': info(newest('*Android.apk')), 'windows': info(newest('*Windows.exe'))}
with open(os.path.join(root, 'src', 'data', 'downloads.json'), 'w') as f:
    json.dump(data, f, indent=2)
print(json.dumps(data, indent=2))

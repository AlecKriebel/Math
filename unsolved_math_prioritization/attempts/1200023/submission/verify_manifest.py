#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
for name,want in manifest.items():
    data=(root/name).read_bytes()
    got=hashlib.sha256(data).hexdigest()
    if got!=want['sha256'] or len(data)!=want['bytes']:
        raise SystemExit('FAIL: '+name)
print('PASS: '+str(len(manifest))+' files; manifest excludes itself.')

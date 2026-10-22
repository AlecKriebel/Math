#!/usr/bin/env python3
"""Verify exact packet inventory and hashes, excluding this manifest's own bytes."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'SHA256SUMS.json').read_text())
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
assert actual==set(m['files']), (actual-set(m['files']),set(m['files'])-actual)
for n,entry in m['files'].items():
    b=(root/n).read_bytes()
    assert len(b)==entry['bytes'], n
    assert hashlib.sha256(b).hexdigest()==entry['sha256'], n
print(json.dumps({'passed':True,'files_verified':len(actual)}))

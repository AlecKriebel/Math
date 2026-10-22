#!/usr/bin/env python3
"""Verify every frozen public file, excluding this manifest's own bytes."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent.parent
entries=json.loads((root/'SHA256SUMS.json').read_text())
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
assert actual==set(entries),{'unlisted':sorted(actual-set(entries)),'missing':sorted(set(entries)-actual)}
for name,record in entries.items():
    data=(root/name).read_bytes()
    assert len(data)==record['bytes'],name
    assert hashlib.sha256(data).hexdigest()==record['sha256'],name
print(json.dumps({'passed':True,'files':len(entries)},indent=2))

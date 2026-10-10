#!/usr/bin/env python3
"""Verify the exact allowlisted public packet, excluding MANIFEST.json itself."""
import hashlib
import json
from pathlib import Path

base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
expected={x['path']:x for x in manifest['files']}
actual={p.name for p in base.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
assert actual==set(expected), {'extra':sorted(actual-set(expected)),'missing':sorted(set(expected)-actual)}
assert not any(p.is_dir() for p in base.iterdir()), 'Unexpected directory in frozen packet'
for name,item in sorted(expected.items()):
    b=(base/name).read_bytes()
    assert len(b)==item['bytes'], name
    assert hashlib.sha256(b).hexdigest()==item['sha256'], name
print(json.dumps({'passed':True,'files_verified':len(expected),'manifest_self_excluded':True},sort_keys=True))

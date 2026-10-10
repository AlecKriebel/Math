#!/usr/bin/env python3
"""Read-only integrity check for this delta acceptance package."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
actual={p.name for p in root.iterdir() if p.is_file()}
expected=set(manifest['files'])|{'MANIFEST.json'}
if actual!=expected:
    raise AssertionError((actual-expected,expected-actual))
for name,meta in manifest['files'].items():
    b=(root/name).read_bytes()
    if len(b)!=meta['bytes'] or hashlib.sha256(b).hexdigest()!=meta['sha256']:
        raise AssertionError(name)
print(json.dumps({'result':'PASS','files_checked':len(manifest['files']),'manifest_self_excluded':True}))

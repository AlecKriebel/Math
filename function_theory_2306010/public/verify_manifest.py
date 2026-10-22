#!/usr/bin/env python3
"""Verify the frozen public file set and its SHA256 hashes, excluding this manifest."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
expected=set(manifest['files'])
assert actual==expected, {'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
for name,info in manifest['files'].items():
 b=(root/name).read_bytes()
 assert len(b)==info['bytes'],name
 assert hashlib.sha256(b).hexdigest()==info['sha256'],name
print(json.dumps({'result':'PASS','files':len(expected)},sort_keys=True))

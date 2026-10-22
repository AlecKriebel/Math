#!/usr/bin/env python3
"""Verify exactly the frozen files; fails on modified or unexpected bytes."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected={entry['path'] for entry in manifest['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.json'}
assert actual==expected, {'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for entry in manifest['files']:
    data=(root/entry['path']).read_bytes()
    assert len(data)==entry['bytes'],entry['path']+' byte count'
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],entry['path']+' digest'
print('PASS:',len(expected),'frozen files match exact byte counts and SHA-256 hashes')

#!/usr/bin/env python3
"""Strict byte and membership verification of this audit package."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}
if len(expected)!=len(manifest['files']):raise AssertionError('duplicate manifest path')
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual!=expected|{'AUDIT_MANIFEST.json'}:raise AssertionError({'missing':sorted(expected-actual),'extra':sorted(actual-expected-{'AUDIT_MANIFEST.json'})})
for entry in manifest['files']:
    path=root/entry['path']
    if path.is_symlink():raise AssertionError('symlink '+entry['path'])
    b=path.read_bytes()
    if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:raise AssertionError('hash '+entry['path'])
print(json.dumps({'status':'PASS_AUDIT_MANIFEST','files':len(expected),'source_payload_included':False}))

#!/usr/bin/env python3
"""Verify the exact publication-safe audit payload, including file membership."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent
manifest_path=root/'AUDIT_MANIFEST.json'
data=manifest_path.read_bytes()
manifest=json.loads(data)
expected={f['path'] for f in manifest['files']} | {'AUDIT_MANIFEST.json'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual!=expected:
    raise RuntimeError('Unexpected or missing payload files')
for entry in manifest['files']:
    p=root/entry['path']
    if p.is_symlink() or not p.is_file():
        raise RuntimeError('Nonregular payload file')
    b=p.read_bytes()
    if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
        raise RuntimeError('Payload hash mismatch: '+entry['path'])
print(json.dumps({'status':'PASS','verified_files':len(manifest['files']),
                  'manifest_sha256':hashlib.sha256(data).hexdigest()},sort_keys=True))

#!/usr/bin/env python3
"""Verify the exact safe audit file set and bytes."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='AUDIT_MANIFEST.json'}
if expected!=actual:
    raise SystemExit('Unexpected or missing audit files')
for entry in manifest['files']:
    b=(root/entry['path']).read_bytes()
    if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
        raise SystemExit('Integrity failure: '+entry['path'])
print(json.dumps({'status':'PASS','verified_files':len(expected),'scope':'Exact file set, sizes, and SHA-256 values'}))

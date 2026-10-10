#!/usr/bin/env python3
"""Verify this audit's declared safe-file inventory without changing it."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
manifest = json.loads((base/'MANIFEST.json').read_text())
entries = manifest['files']
names = {e['path'] for e in entries}
actual = {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
if actual != names | {'MANIFEST.json'}:
    raise SystemExit('Unexpected or missing audit file')
for e in entries:
    p = base/e['path']
    if p.is_symlink() or p.resolve().parent != base:
        raise SystemExit('Unsafe path: '+e['path'])
    data = p.read_bytes()
    if len(data) != e['bytes'] or hashlib.sha256(data).hexdigest() != e['sha256']:
        raise SystemExit('Integrity failure: '+e['path'])
print(json.dumps({'status':'PASS','files_verified':len(entries),
                  'manifest_self_hashed':False},sort_keys=True))

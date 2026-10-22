#!/usr/bin/env python3
"""Strict safe-packet integrity check, offline and read-only."""
import hashlib,json,pathlib,sys
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={x['path']:x for x in manifest['files']}
for p in root.rglob('*'):
    if p.is_symlink():sys.exit('Symlink rejected: '+p.relative_to(root).as_posix())
for name in expected:
    part=pathlib.PurePosixPath(name)
    if part.is_absolute() or '..' in part.parts or name in ('','MANIFEST.json'):sys.exit('Unsafe manifest path')
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p != root/'MANIFEST.json'}
if actual!=set(expected):
    sys.exit('Inventory mismatch: missing='+str(sorted(set(expected)-actual))+' extra='+str(sorted(actual-set(expected))))
for name,rec in expected.items():
    p=root/name
    if p.is_symlink():sys.exit('Symlink rejected: '+name)
    data=p.read_bytes()
    if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:sys.exit('Mismatch: '+name)
print(json.dumps({'status':'PASS','files_verified':len(expected)},sort_keys=True))

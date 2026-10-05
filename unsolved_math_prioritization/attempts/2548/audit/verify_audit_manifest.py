#!/usr/bin/env python3
"""Check this audit's file inventory and content hashes, read-only."""
import hashlib
import json
from pathlib import Path, PurePosixPath

root=Path(__file__).resolve().parent
m=json.loads((root/'AUDIT_MANIFEST.json').read_bytes())
names=[]
for r in m['files']:
    p=PurePosixPath(r['path'])
    if p.is_absolute() or '..' in p.parts or str(p)!=r['path']:
        raise SystemExit('Unsafe audit path')
    f=root/r['path']
    if not f.is_file() or f.is_symlink():
        raise SystemExit('Missing, nonregular, or symlinked audit file')
    b=f.read_bytes()
    if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
        raise SystemExit('Audit content mismatch: '+r['path'])
    names.append(r['path'])
if len(names)!=len(set(names)):
    raise SystemExit('Duplicate audit path')
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual!=set(names)|{'AUDIT_MANIFEST.json'}:
    raise SystemExit('Audit inventory mismatch')
print(json.dumps({'status':'PASS','files_verified':len(names),'original_problem_solved':False},sort_keys=True))

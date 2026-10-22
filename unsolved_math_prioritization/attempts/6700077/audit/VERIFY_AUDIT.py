#!/usr/bin/env python3
"""Validate the safe audit against a separately supplied manifest hash."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('audit');p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
root=Path(a.audit);mf=root/'AUDIT_MANIFEST.json'
if mf.is_symlink() or not mf.is_file(): raise ValueError('manifest missing or symlink')
b=mf.read_bytes()
if hashlib.sha256(b).hexdigest()!=a.manifest_sha256: raise ValueError('external audit anchor mismatch')
m=json.loads(b)
expected={'AUDIT_MANIFEST.json'}
for row in m['files']:
    name=row['path']
    if not isinstance(name,str) or Path(name).name!=name or name in expected or name in ('.','..'): raise ValueError('unsafe path')
    expected.add(name);f=root/name
    if f.is_symlink() or not f.is_file(): raise ValueError('file kind')
    v=f.read_bytes()
    if len(v)!=row['bytes'] or hashlib.sha256(v).hexdigest()!=row['sha256']: raise ValueError('changed payload')
if {f.name for f in root.iterdir()}!=expected: raise ValueError('file set')
if any(Path(n).suffix not in ('.md','.json','.py') for n in expected): raise ValueError('non-safe artifact extension')
print(json.dumps({'outcome':'PASS','audit_payload_files':len(expected)-1,'audit_manifest_sha256':a.manifest_sha256},indent=2,sort_keys=True))

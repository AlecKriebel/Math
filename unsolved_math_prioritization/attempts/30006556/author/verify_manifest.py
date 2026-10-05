#!/usr/bin/env python3
"""Strict exact safe-folder inventory and byte verification."""
from pathlib import Path
import hashlib,json,sys

def verify(root):
    root=Path(root)
    manifest_path=root/'AUTHOR_MANIFEST.json'
    if manifest_path.is_symlink():raise ValueError('symlink manifest')
    data=json.loads(manifest_path.read_text())
    if data['format']!='sha256-complete-flat-inventory-v1':raise ValueError('unknown format')
    expected={x['path']:x for x in data['files']}
    if len(expected)!=len(data['files']):raise ValueError('duplicate path')
    for name in expected:
        if Path(name).name!=name or name in {'.','..','AUTHOR_MANIFEST.json'}:raise ValueError('unsafe path')
    actual={p.name for p in root.iterdir()}
    if actual!=set(expected)|{'AUTHOR_MANIFEST.json'}:raise ValueError('inventory mismatch')
    for name,entry in expected.items():
        p=root/name
        if p.is_symlink() or not p.is_file():raise ValueError('not regular file: '+name)
        b=p.read_bytes()
        if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
            raise ValueError('digest mismatch: '+name)
    return {'status':'PASS','files_verified':len(expected),'self_manifest_not_hashed':True}
if __name__=='__main__':
    try:print(json.dumps(verify(Path(__file__).resolve().parent),sort_keys=True))
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)

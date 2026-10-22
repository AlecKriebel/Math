#!/usr/bin/env python3
"""Validate exact payload inventory, sizes and hashes; safe under python -O."""
import hashlib
import json
from pathlib import Path, PurePosixPath

def verify(root):
    root=Path(root)
    manifest=root/'AUTHOR_MANIFEST.json'
    if manifest.is_symlink():
        raise ValueError('Symlink manifest')
    data=json.loads(manifest.read_text())
    expected=set()
    for entry in data['files']:
        name=entry['path']
        p=PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or len(p.parts)!=1 or name in expected or name=='AUTHOR_MANIFEST.json':
            raise ValueError('Unsafe or duplicate inventory entry')
        expected.add(name)
        target=root/name
        if target.is_symlink() or not target.is_file():
            raise ValueError('Missing, non-file, or symlink: '+name)
        content=target.read_bytes()
        if len(content)!=entry['bytes'] or hashlib.sha256(content).hexdigest()!=entry['sha256']:
            raise ValueError('Byte mismatch: '+name)
    actual={p.name for p in root.iterdir() if p.name!='AUTHOR_MANIFEST.json'}
    if actual!=expected:
        raise ValueError('Inventory mismatch')
    return {'status':'PASS_EXACT_MANIFEST','files':len(expected)}

if __name__=='__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent),sort_keys=True))

#!/usr/bin/env python3
"""Fail closed on missing, extra, linked, changed, or wrongly-sized files."""
import hashlib
import json
from pathlib import Path

def verify(root):
    root=Path(root)
    manifest=root/'MANIFEST.json'
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('manifest is missing or linked')
    m=json.loads(manifest.read_text())
    listed={x['path']:x for x in m['files']}
    if len(listed)!=len(m['files']):
        raise ValueError('duplicate manifest path')
    if any(Path(p).is_absolute() or '..' in Path(p).parts or p=='MANIFEST.json' for p in listed):
        raise ValueError('unsafe manifest path')
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError('linked object')
        if p.is_file() and p.name!='MANIFEST.json':
            actual.add(p.relative_to(root).as_posix())
    if actual!=set(listed):
        raise ValueError('file set mismatch')
    for rel,entry in listed.items():
        b=(root/rel).read_bytes()
        if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
            raise ValueError('file integrity mismatch: '+rel)
    return len(listed)
if __name__=='__main__':
    import sys
    n=verify(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent)
    print(json.dumps({'manifest_files_verified':n,'status':'pass'},sort_keys=True))

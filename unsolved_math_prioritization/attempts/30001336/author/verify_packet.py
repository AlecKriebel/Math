#!/usr/bin/env python3
"""Strict flat-directory inventory and byte binding; never executes checked files."""
import hashlib
import json
import stat
from pathlib import Path


def verify(root):
    manifest=root/'MANIFEST.json'
    if not stat.S_ISREG(manifest.lstat().st_mode):
        raise RuntimeError('Manifest must be a regular nonsymlink file')
    data=json.loads(manifest.read_text())
    if data.get('format')!='rooted-tree-30001336-v1':
        raise RuntimeError('Manifest format mismatch')
    entries=data.get('files')
    if not isinstance(entries,list):
        raise RuntimeError('Manifest files must be a list')
    names=[x['path'] for x in entries]
    if len(names)!=len(set(names)) or any('/' in p or '\\' in p or p in ('','.', '..','MANIFEST.json') for p in names):
        raise RuntimeError('Invalid or duplicate manifest path')
    actual={p.name for p in root.iterdir()}
    if actual!=set(names)|{'MANIFEST.json'}:
        raise RuntimeError('Strict inventory mismatch')
    for item in entries:
        p=root/item['path']
        if not stat.S_ISREG(p.lstat().st_mode):
            raise RuntimeError('Nonregular entry: '+item['path'])
        raw=p.read_bytes()
        if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
            raise RuntimeError('Byte binding mismatch: '+item['path'])
    return {'status':'PASS_STRICT_INVENTORY','bound_files':len(entries),'total_regular_files':len(entries)+1,
            'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()}

if __name__=='__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent),sort_keys=True,indent=2))

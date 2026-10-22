#!/usr/bin/env python3
"""Verify the complete flat public audit inventory, sizes and SHA-256 digests."""
import hashlib,json,sys
from pathlib import Path

def check(root):
    root=Path(root);mf=root/'AUDIT_MANIFEST.json'
    if mf.is_symlink() or not mf.is_file():raise ValueError('invalid manifest file')
    data=json.loads(mf.read_bytes());assert data['format']=='independent-audit-flat-sha256-v1'
    names=[]
    for record in data['files']:
        name=record['path']
        if not isinstance(name,str) or '/' in name or '\\' in name or name in ('','.','..','AUDIT_MANIFEST.json'):
            raise ValueError('unsafe manifest name')
        names.append(name)
    if len(names)!=len(set(names)):raise ValueError('duplicate manifest entry')
    if set(p.name for p in root.iterdir())!=set(names)|{'AUDIT_MANIFEST.json'}:raise ValueError('inventory mismatch')
    for record in data['files']:
        p=root/record['path']
        if p.is_symlink() or not p.is_file():raise ValueError('non-regular file')
        b=p.read_bytes()
        if len(b)!=record['bytes'] or hashlib.sha256(b).hexdigest()!=record['sha256']:raise ValueError('content mismatch')
    return {'status':'PASS','verified_files':len(names),'manifest_self_excluded':True}

if __name__=='__main__':
    try:print(json.dumps(check(Path(__file__).resolve().parent),sort_keys=True))
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)

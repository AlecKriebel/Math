#!/usr/bin/env python3
"""Strict exact-file-set manifest verifier. Only the root manifest excludes itself."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys


def verify(root, expected_manifest_sha256=None):
    root=Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Root is missing, linked, or not a directory')
    manifest=root/'MANIFEST.json'
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('Manifest is missing or linked')
    raw=manifest.read_bytes()
    if expected_manifest_sha256 is not None and hashlib.sha256(raw).hexdigest()!=expected_manifest_sha256:
        raise ValueError('External manifest binding mismatch')
    m=json.loads(raw)
    if not isinstance(m,dict) or not isinstance(m.get('files'),list):
        raise ValueError('Invalid manifest schema')
    listed={}
    for item in m['files']:
        if not isinstance(item,dict) or set(item)!={'path','bytes','sha256'}:
            raise ValueError('Invalid file entry')
        p=item['path']
        if not isinstance(p,str) or not p or '\\' in p or p=='MANIFEST.json':
            raise ValueError('Invalid path')
        q=PurePosixPath(p)
        if q.is_absolute() or any(x in ('','..','.') for x in p.split('/')) or q.as_posix()!=p:
            raise ValueError('Unsafe or noncanonical path')
        if p in listed:
            raise ValueError('Duplicate path')
        if type(item['bytes']) is not int or item['bytes']<0:
            raise ValueError('Invalid byte count')
        if not isinstance(item['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',item['sha256']):
            raise ValueError('Invalid SHA-256')
        listed[p]=item
    actual=set()
    for p in root.rglob('*'):
        s=p.lstat()
        if stat.S_ISLNK(s.st_mode):
            raise ValueError('Linked object')
        if stat.S_ISDIR(s.st_mode):
            continue
        if not stat.S_ISREG(s.st_mode):
            raise ValueError('Nonregular object')
        rel=p.relative_to(root).as_posix()
        if rel!='MANIFEST.json':
            actual.add(rel)
    if actual != set(listed):
        raise ValueError('Exact file-set mismatch')
    for rel,item in listed.items():
        b=(root/rel).read_bytes()
        if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:
            raise ValueError('File binding mismatch: '+rel)
    return len(listed)

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
    expected=sys.argv[2] if len(sys.argv)>2 else None
    n=verify(root,expected)
    print(json.dumps({'status':'PASS','bound_payload_files':n},sort_keys=True))

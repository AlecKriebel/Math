#!/usr/bin/env python3
"""Offline read-only strict inventory and byte/hash verification."""
import argparse,hashlib,json,pathlib,re

def verify(root, expected=None):
    root=pathlib.Path(root)
    manifest=root/'MANIFEST.json'
    if manifest.is_symlink():raise ValueError('symlink manifest')
    raw=manifest.read_bytes()
    if expected and hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('manifest pin mismatch')
    data=json.loads(raw); entries=data['files']; found={}
    if not isinstance(entries,list) or not entries:raise ValueError('invalid entries')
    for record in entries:
        name=record['path'];p=pathlib.PurePosixPath(name)
        if not isinstance(name,str) or p.is_absolute() or '..' in p.parts or '\\' in name or p.as_posix()!=name or name in ('','.','MANIFEST.json'):
            raise ValueError('unsafe path')
        if name in found:raise ValueError('duplicate path')
        if not isinstance(record['bytes'],int) or isinstance(record['bytes'],bool) or record['bytes']<0:raise ValueError('invalid size')
        if not re.fullmatch('[0-9a-f]{64}',record['sha256']):raise ValueError('invalid hash')
        found[name]=record
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('symlink')
        if p.is_file() and p!=manifest:actual.add(p.relative_to(root).as_posix())
    if actual!=set(found):raise ValueError('inventory mismatch')
    for name,record in found.items():
        value=(root/name).read_bytes()
        if len(value)!=record['bytes'] or hashlib.sha256(value).hexdigest()!=record['sha256']:raise ValueError('content mismatch')
    return {'status':'PASS','files_verified':len(found),'manifest_sha256':hashlib.sha256(raw).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',nargs='?',default=str(pathlib.Path(__file__).resolve().parent));p.add_argument('--expected-manifest')
    a=p.parse_args();print(json.dumps(verify(a.root,a.expected_manifest),sort_keys=True))

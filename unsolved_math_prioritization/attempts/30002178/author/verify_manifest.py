#!/usr/bin/env python3
"""Strict release integrity checker; manifest itself is the external trust anchor."""
import hashlib,json,re,sys
from pathlib import Path,PurePosixPath

def verify(root):
    root=Path(root)
    if root.is_symlink():raise ValueError('root symlink')
    mf=root/'MANIFEST.json'
    if mf.is_symlink():raise ValueError('manifest symlink')
    data=json.loads(mf.read_text())
    if data.get('schema')!='sha256-bytes-v1' or not isinstance(data.get('files'),list):raise ValueError('schema')
    expected={}
    for item in data['files']:
        name=item.get('path');size=item.get('bytes');sha=item.get('sha256')
        if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_.\-/]+',name):raise ValueError('invalid path')
        q=PurePosixPath(name)
        if q.is_absolute() or str(q)!=name or any(p in ('','..','.') for p in q.parts) or name=='MANIFEST.json':raise ValueError('unsafe path')
        if name in expected:raise ValueError('duplicate path')
        if not isinstance(size,int) or isinstance(size,bool) or size<0:raise ValueError('invalid bytes')
        if not isinstance(sha,str) or not re.fullmatch('[a-f0-9]{64}',sha):raise ValueError('invalid hash')
        expected[name]=(size,sha)
    actual=set()
    for path in root.rglob('*'):
        if path.is_symlink():raise ValueError('symlink')
        if path.is_file():
            rel=path.relative_to(root).as_posix()
            if rel!='MANIFEST.json':actual.add(rel)
    if actual!=set(expected):raise ValueError('file set mismatch')
    for name,(size,sha) in expected.items():
        b=(root/name).read_bytes()
        if len(b)!=size or hashlib.sha256(b).hexdigest()!=sha:raise ValueError('content mismatch '+name)
    return len(expected)
if __name__=='__main__':
    try:print(json.dumps({'status':'PASS','files':verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent)}))
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)

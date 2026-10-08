#!/usr/bin/env python3
"""Strict manifest verifier; rejects missing, changed, extra and symlinked files."""
import hashlib,json,pathlib,sys

def check(root):
    root=pathlib.Path(root)
    manifest_path=root/'MANIFEST.json'
    if manifest_path.is_symlink(): raise ValueError('symlinked manifest')
    manifest=json.loads(manifest_path.read_text())
    expected={x['path']:x for x in manifest['files']}
    if len(expected)!=len(manifest['files']): raise ValueError('duplicate path')
    found=set()
    for p in root.rglob('*'):
        if p.is_symlink(): raise ValueError('symlink '+str(p))
        if p.is_file(): found.add(p.relative_to(root).as_posix())
    if found!=set(expected)|{'MANIFEST.json'}: raise ValueError('unexpected file set')
    for name,item in expected.items():
        p=root/name
        if pathlib.PurePosixPath(name).is_absolute() or '..' in pathlib.PurePosixPath(name).parts: raise ValueError('invalid path')
        data=p.read_bytes()
        if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise ValueError('hash/size mismatch '+name)
    return len(expected)

if __name__=='__main__':
    root=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
    print(json.dumps({'status':'PASS','manifest_files':check(root)},sort_keys=True))

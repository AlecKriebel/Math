#!/usr/bin/env python3
"""Strict offline inventory/hash/replay check. The manifest digest is externally pinned."""
import hashlib,json,pathlib,subprocess,sys,tempfile,shutil

def verify(root, replay=True):
    root=pathlib.Path(root)
    raw=(root/'MANIFEST.json').read_bytes()
    m=json.loads(raw)
    if m.get('schema')!='sha256-file-inventory-v1':raise ValueError('manifest schema')
    records=m['files']
    expected={'MANIFEST.json'}
    for r in records:
        name=r['path']; p=pathlib.PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or str(p)!=name:raise ValueError('unsafe manifest path')
        if name in expected:raise ValueError('duplicate path')
        expected.add(name)
    found=set()
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('symlink')
        if p.is_file():found.add(p.relative_to(root).as_posix())
        elif not p.is_dir():raise ValueError('special filesystem node')
    if found!=expected:raise ValueError('inventory mismatch')
    for r in records:
        b=(root/r['path']).read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:raise ValueError('hash mismatch')
    if replay:
        out=subprocess.check_output([sys.executable,'-B',str(root/'controls.py')],cwd=root)
        if out!=(root/'CONTROL_RESULTS.json').read_bytes():raise ValueError('replay mismatch')
    return {'files':len(expected),'manifest_sha256':hashlib.sha256(raw).hexdigest()}

def selftest(root):
    changes=[('changed',lambda p:(p/'README.md').write_bytes(b'changed')),
             ('missing',lambda p:(p/'README.md').unlink()),
             ('extra',lambda p:(p/'unexpected.txt').write_bytes(b'x')),
             ('nested_extra',lambda p:((p/'unexpected').mkdir(),(p/'unexpected/file').write_bytes(b'x'))),
             ('symlink',lambda p:(p/'link').symlink_to(p/'README.md')),
             ('manifest_traversal',lambda p:(p/'MANIFEST.json').write_text(json.dumps({'schema':'sha256-file-inventory-v1','files':[{'path':'../escape','bytes':0,'sha256':'0'*64}]}))),
             ('manifest_duplicate',lambda p:(p/'MANIFEST.json').write_text(json.dumps({'schema':'sha256-file-inventory-v1','files':[{'path':'MANIFEST.json','bytes':0,'sha256':'0'*64}]})))]
    result={}
    for name,change in changes:
        with tempfile.TemporaryDirectory(prefix='polyhedra-packet-check-') as d:
            p=pathlib.Path(d)/'packet';shutil.copytree(root,p);change(p)
            try:verify(p,False)
            except (ValueError,KeyError,FileNotFoundError):result[name]='rejected'
            else:raise RuntimeError('negative control accepted: '+name)
    return result
if __name__=='__main__':
    root=pathlib.Path(__file__).resolve().parent
    r=verify(root)
    if '--self-test' in sys.argv:r['negative_controls']=selftest(root)
    print(json.dumps(r,sort_keys=True,indent=2))

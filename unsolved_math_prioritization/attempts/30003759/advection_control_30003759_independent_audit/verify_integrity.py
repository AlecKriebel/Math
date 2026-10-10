#!/usr/bin/env python3
"""Strict closed-file integrity check, with pinned author freeze and optional audit manifest."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,sys,zipfile
A='d6686eca2815c676f65d76bc552a2d41c9b8080dd6bca844c7d0a4815d231b26'
M='d60b749ef5914027eed0e03da99de7e712e52a755f18c4d243ee3f6251cdb1f1'

def check(root,pin=None):
    p=root/'MANIFEST.json'; b=p.read_bytes()
    if pin and hashlib.sha256(b).hexdigest()!=pin:raise ValueError('Pinned manifest mismatch')
    d=json.loads(b);rows=d['files'];paths=[r['path'] for r in rows]
    if len(paths)!=len(set(paths)):raise ValueError('Duplicate manifest path')
    for s in paths:
        q=PurePosixPath(s)
        if q.is_absolute() or '..' in q.parts or str(q)!=s:raise ValueError('Unsafe manifest path')
        if s=='MANIFEST.json':raise ValueError('Self-inclusion')
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('Symlink rejected')
        if p.is_file():actual.add(p.relative_to(root).as_posix())
        elif not p.is_dir():raise ValueError('Special file rejected')
    if actual!={'MANIFEST.json',*paths}:raise ValueError('Closed file set mismatch')
    for r in rows:
        b=(root/r['path']).read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
            raise ValueError('Payload hash/size mismatch: '+r['path'])
    return {'status':'PASS','files':len(paths),'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()}

root=Path(__file__).resolve().parent
base=root.parent
out={'author':check(base/'advection_control_30003759',M)}
z=base/'ADVECTION_CONTROL_30003759_SAFE_FREEZE.zip'
if hashlib.sha256(z.read_bytes()).hexdigest()!=A:raise ValueError('Archive pin mismatch')
with zipfile.ZipFile(z) as f:
    entries=[i for i in f.infolist() if not i.is_dir()]
    names=[i.filename for i in entries]
    if len(names)!=len(set(names)):raise ValueError('Duplicate archive entry')
    prefix='advection_control_30003759/'
    expected={prefix+p.relative_to(base/'advection_control_30003759').as_posix()
              for p in (base/'advection_control_30003759').rglob('*') if p.is_file()}
    # Some archivers omit a top-level directory. Recognize only these two forms.
    stripped={n[len(prefix):] if n.startswith(prefix) else n for n in names}
    allowed={n[len(prefix):] for n in expected}
    if stripped!=allowed:raise ValueError('Archive file set mismatch')
    for i in entries:
        if stat.S_ISLNK(i.external_attr>>16):raise ValueError('Archive symlink rejected')
        n=i.filename[len(prefix):] if i.filename.startswith(prefix) else i.filename
        if f.read(i)!=(base/'advection_control_30003759'/n).read_bytes():raise ValueError('Archive payload mismatch')
out['archive']={'status':'PASS','sha256':A,'file_count':len(entries)}
if (root/'MANIFEST.json').exists():out['audit']=check(root)
print(json.dumps(out,indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Verify the frozen relative-path allowlist, sizes and SHA-256 digests."""
from pathlib import Path, PurePosixPath
import hashlib,json,re
root=Path(__file__).resolve().parent
manifest=root/'MANIFEST.json'
assert manifest.is_file() and not manifest.is_symlink()
m=json.loads(manifest.read_text())
assert m['format']=='sha256-allowlist-v1'
entries=m['files']; names=[e['path'] for e in entries]
assert len(names)==len(set(names))
for e in entries:
    rel=PurePosixPath(e['path'])
    assert not rel.is_absolute() and '..' not in rel.parts and '.' not in rel.parts
    assert str(rel)==e['path'] and e['path']!='MANIFEST.json'
    assert re.fullmatch(r'[0-9a-f]{64}',e['sha256'])
    assert type(e['bytes']) is int and e['bytes']>=0
actual=set()
for p in root.rglob('*'):
    assert not p.is_symlink(),f'Symlink forbidden: {p.name}'
    if p.is_file() and p!=manifest:actual.add(p.relative_to(root).as_posix())
assert actual==set(names),{'missing':sorted(set(names)-actual),'extra':sorted(actual-set(names))}
for e in entries:
    data=(root/e['path']).read_bytes()
    assert len(data)==e['bytes'],e['path']
    assert hashlib.sha256(data).hexdigest()==e['sha256'],e['path']
print(json.dumps({'status':'PASS','files':len(entries),'manifest_self_hash_excluded':True},sort_keys=True))

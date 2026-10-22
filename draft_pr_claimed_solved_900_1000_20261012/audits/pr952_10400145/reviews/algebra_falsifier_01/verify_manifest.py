#!/usr/bin/env python3
"""Verify the explicit public allowlist. Does not read any private source body."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected=set(manifest['files'])
actual={p.name for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
assert actual==expected, {'unexpected':sorted(actual-expected),'missing':sorted(expected-actual)}
assert 'private' not in expected
for name,r in manifest['files'].items():
    assert Path(name).name==name and name not in ('.','..')
    p=root/name
    assert not p.is_symlink()
    b=p.read_bytes()
    assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],name
for name in ['AUTHENTICATION_INITIAL.json','AUTHENTICATION_FINAL.json']:
    a=json.loads((root/name).read_text())
    assert a['all_pass'] and a['count']==33
    assert a['head']=='989a532ae1d50894190d010a0a02ba8c3d71ee05'
print(json.dumps({'status':'PASS','public_files':len(expected),'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()},indent=2))

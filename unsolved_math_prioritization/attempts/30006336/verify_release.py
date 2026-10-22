#!/usr/bin/env python3
"""Strict final-layout binding plus all author/audit replays."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'RELEASE_BINDING.json').read_text())
assert set(manifest)=={'schema','id','status','attempt_turns','author_manifest_sha256','audit_manifest_sha256','files'}
assert manifest['schema']==1 and manifest['id']==30006336
assert manifest['status']=='unsolved' and manifest['attempt_turns']==5
assert manifest['author_manifest_sha256']=='05a9835d5c4c302afe24c47d6143096301ce658e7bd29e4fef884f2c2a2705c8'
assert manifest['audit_manifest_sha256']=='b36e7c9481af737325f1499b56c3da1c06c0d27d7d54213da4268e4e8e31577a'
expected=manifest['files']
assert len(expected)==27
for key,value in expected.items():
    pure=PurePosixPath(key)
    assert not pure.is_absolute() and '..' not in pure.parts and '.' not in pure.parts
    assert str(pure)==key and '\\' not in key
    assert set(value)=={'bytes','sha256'}
    assert isinstance(value['bytes'],int) and value['bytes']>=0
    assert re.fullmatch('[0-9a-f]{64}',value['sha256'])
actual={}
for path in root.rglob('*'):
    assert not path.is_symlink(),f'Symlink: {path}'
    key=path.relative_to(root).as_posix()
    if path.is_dir():
        assert key in {'author','audit'},f'Unexpected directory: {key}'
        continue
    assert path.is_file()
    if key=='RELEASE_BINDING.json':continue
    data=path.read_bytes()
    actual[key]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
assert actual==expected,'Release inventory or bytes mismatch'
assert hashlib.sha256((root/'author/SHA256SUMS.json').read_bytes()).hexdigest()==manifest['author_manifest_sha256']
assert hashlib.sha256((root/'audit/AUDIT_SHA256SUMS.json').read_bytes()).hexdigest()==manifest['audit_manifest_sha256']
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
r=subprocess.run([sys.executable,'-B','audit/verify_audit.py'],cwd=root,env=env,text=True,capture_output=True,check=True)
result=json.loads(r.stdout)
assert result['all_replays_pass'] and result['independent_controls']==655
print(json.dumps({'release_manifest_valid':True,'files':28,'author_files':12,'audit_files':11,'all_replays_pass':True,'independent_controls':655,'status':'unsolved'},sort_keys=True))

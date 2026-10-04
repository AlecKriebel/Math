#!/usr/bin/env python3
"""Validate the self-excluded explicit public inventory in this owned root."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
expected=set()
for e in m['files']:
    r=Path(e['path'])
    assert not r.is_absolute() and '..' not in r.parts
    assert str(r)!='PUBLIC_MANIFEST.json'
    assert not any(p in set(m['private_excluded']) for p in r.parts)
    assert str(r) not in expected
    expected.add(str(r))
    data=(ROOT/r).read_bytes()
    assert len(data)==e['bytes']
    assert hashlib.sha256(data).hexdigest()==e['sha256']
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
        and not any(x in set(m['private_excluded']) for x in p.relative_to(ROOT).parts)
        and p.name!='PUBLIC_MANIFEST.json'}
assert actual==expected
for label in ['SOURCE_FIRST_BASELINE','MATHEMATICAL_VERDICT']:
    s=json.loads((ROOT/f'{label}_SEAL.json').read_text())
    assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
print(json.dumps({'status':'PASS','owned_public_files':len(expected),'candidate_head':m['candidate_head'],
                  'self_excluded':m['self_excluded'],'sealed_stage_files_verified':2},indent=2,sort_keys=True))

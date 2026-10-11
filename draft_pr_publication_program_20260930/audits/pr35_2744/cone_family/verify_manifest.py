#!/usr/bin/env python3
"""Verify the closed self-excluding first-party inventory and private-source receipts."""
from pathlib import Path
import json,hashlib
here=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def first_party():
    return {p.relative_to(here).as_posix():p for p in here.rglob('*') if p.is_file() and p.relative_to(here).parts[0] not in {'primary_sources','private_replay','__pycache__'} and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
m=json.loads((here/'MANIFEST.json').read_text());actual=first_party();expected={v['path']:v for v in m['files']}
assert actual.keys()==expected.keys(),{'extra':list(actual.keys()-expected.keys()),'missing':list(expected.keys()-actual.keys())}
for path,p in actual.items():assert sha(p)==expected[path]['sha256'] and p.stat().st_size==expected[path]['bytes'],path
seal=json.loads((here/'INITIAL_SEAL.json').read_text())
for name,digest in seal['files'].items():assert sha(here/name)==digest,name
bindings=json.loads((here/'SOURCE_BINDINGS.json').read_text())
private=here/'primary_sources'
if private.exists():
    for row in bindings['local_sources']:
        for key in ['pdf','text']:
            p=here/row[key]['path'];assert sha(p)==row[key]['sha256'] and p.stat().st_size==row[key]['bytes'],row['id']
assert bindings['dix_web_primary']['fresh_local_byte_hash'] is None
print(json.dumps({'closed_first_party_files':len(actual),'all_hashes_verified':True,'initial_seal_verified':True,'private_sources_receipt_bound':len(bindings['local_sources']),'fresh_dix_bytes_claimed':False,'manifest_sha256':sha(here/'MANIFEST.json')},indent=2))

#!/usr/bin/env python3
"""Verify audit artifacts and the unchanged frozen input. Standard library."""
import hashlib,json,pathlib,sys
here=pathlib.Path(__file__).resolve().parent
manifest=json.loads((here/'AUDIT_SHA256SUMS.json').read_text())
actual={p.name:p for p in here.iterdir() if p.is_file() and p.name!='AUDIT_SHA256SUMS.json'}
assert set(actual)==set(manifest),'audit file set mismatch'
for name,meta in manifest.items():
    data=actual[name].read_bytes()
    assert len(data)==meta['bytes'],name+' bytes'
    assert hashlib.sha256(data).hexdigest()==meta['sha256'],name+' hash'
packet=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else here.parent/'packet'
binding=json.loads((here/'INPUT_BINDING.json').read_text())
expected={row['name']:row for row in binding['frozen_input_files']}
actual_input={p.name:p for p in packet.iterdir() if p.is_file()}
assert set(actual_input)==set(expected),'candidate file set mismatch'
for name,meta in expected.items():
    data=actual_input[name].read_bytes()
    assert len(data)==meta['bytes'],name+' input bytes'
    assert hashlib.sha256(data).hexdigest()==meta['sha256'],name+' input hash'
assert expected['SHA256SUMS.json']['sha256']==binding['expected_manifest_sha256']
assert expected['PROOF.md']['sha256']==binding['expected_proof_sha256']
print(json.dumps({'result':'PASS','audit_files_verified':len(manifest),'frozen_input_files_verified':len(expected)},sort_keys=True))

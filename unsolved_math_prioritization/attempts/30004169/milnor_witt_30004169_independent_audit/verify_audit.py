#!/usr/bin/env python3
"""Verify audit bytes and replay all self-contained independent controls."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
m=json.loads((p/'AUDIT_MANIFEST.json').read_text())
assert {x.name for x in p.iterdir()}==set(m['files'])|{'AUDIT_MANIFEST.json'}
for name,meta in m['files'].items():
    data=(p/name).read_bytes()
    assert len(data)==meta['bytes'] and hashlib.sha256(data).hexdigest()==meta['sha256'],name
r=subprocess.run([sys.executable,str(p/'independent_verifier.py')],check=True,capture_output=True,text=True)
actual=json.loads(r.stdout); expected=json.loads((p/'INDEPENDENT_RESULTS.json').read_text())
for key,value in actual.items(): assert value==expected[key],key
print(json.dumps({'audit_manifest':'PASS','self_contained_independent_controls':'PASS',
 'external_source_dataset_and_catalog_hashes':'Recorded from audit; optional inputs needed to replay.',
 'original_problem_solved':False,'verdict':'PASS within unresolved scope'},sort_keys=True))

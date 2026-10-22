#!/usr/bin/env python3
"""Portable release integrity and exact-control replay. Does not download sources."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser()
p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
root=p.parse_args().root.resolve()
def sha(data): return hashlib.sha256(data).hexdigest()
manifest_bytes=(root/'AUTHOR_MANIFEST.json').read_bytes()
assert sha(manifest_bytes)=='936f36854d5782e7815ddea50158a4404a23dcbf4c410d80af9513ce7593b357'
manifest=json.loads(manifest_bytes)
assert len(manifest['files'])==13
for entry in manifest['files']:
    data=(root/entry['path']).read_bytes()
    assert len(data)==entry['bytes'],entry['path']
    assert sha(data)==entry['sha256'],entry['path']
    gitsha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert gitsha==entry['git_blob_sha1'],entry['path']
audit=(root/'independent_review_v1/FULL_ADVERSARIAL_AUDIT.md').read_bytes()
assert sha(audit)=='278992214da8f68ae7f4223a31ed6dd6f69507c1a965112240c77b69054a0144'
audit_result=json.loads((root/'independent_review_v1/AUDIT_RESULT.json').read_text())
assert audit_result['report_sha256']==sha(audit)
assert not audit_result['blocking_mathematical_repairs']
assert audit_result['original_problem_disposition']=='unsolved'
assert audit_result['substantive_attempts']==5
status=json.loads((root/'PUBLICATION_STATUS.json').read_text())
assert status['original_problem_status']=='unsolved'
assert status['substantive_author_attempts']==5
assert status['global_resolution'] is False
assert status['historical_novelty_established'] is False
assert status['nonblocking_clarifications_included'] is True
clarification=(root/'NONBLOCKING_CLARIFICATIONS.md').read_text()
assert 'almost every normal' in clarification
assert 'strict for some normals' in clarification
child=subprocess.run([sys.executable,str(root/'verify_exact.py')],capture_output=True,text=True,check=True,cwd=root)
replay=json.loads(child.stdout)
expected=json.loads((root/'EXACT_CHECKS.json').read_text())
assert replay==expected
assert replay['status']=='PASS' and replay['exact_assertions']==228
print(json.dumps({'status':'PASS','original_author_files_verified':14,'author_manifest_sha256':sha(manifest_bytes),'public_audit_sha256':sha(audit),'exact_controls_replayed':228,'replay_matches_frozen_output':True,'two_nonblocking_clarifications_included':True,'original_problem_status':'unsolved','substantive_attempts':5,'scope':'Portable byte-integrity checks and finite exact algebra replay only; no global-resolution, novelty, human-review or formal-verification claim.'},indent=2,sort_keys=True))

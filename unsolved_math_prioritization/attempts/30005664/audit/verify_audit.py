#!/usr/bin/env python3
"""Verify exact safe audit-file allowlist and every non-manifest fingerprint."""
from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parent
allowed={'AUDIT.md','README.md','SOURCE_REVIEW.json','INPUT_VERIFICATION.json','INDEPENDENT_RESULTS.json','REPLAY.json','independent_check.py','verify_inputs.py','verify_audit.py','MANIFEST.json'}
actual={p.name for p in base.iterdir() if p.is_file()}
assert actual==allowed,(actual-allowed,allowed-actual)
manifest=json.loads((base/'MANIFEST.json').read_bytes())
assert {r['path'] for r in manifest['files']}==allowed-{'MANIFEST.json'}
assert len(manifest['files'])==len(allowed)-1
for row in manifest['files']:
    b=(base/row['path']).read_bytes()
    assert len(b)==row['bytes']
    assert hashlib.sha256(b).hexdigest()==row['sha256']
print(json.dumps({'status':'PASS','allowlisted_files':len(allowed),'file_hashes_verified':len(allowed)-1,'original_problem_solved':False},sort_keys=True))

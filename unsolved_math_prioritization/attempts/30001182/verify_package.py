#!/usr/bin/env python3
"""Verify immutable author/review artifacts and replay exact auxiliary controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
checks=0
for sub,name in [('public','FROZEN_MANIFEST.json'),('audit','AUDIT_MANIFEST.json')]:
    base=root/sub
    manifest=json.loads((base/name).read_text())
    for item in manifest['files']:
        p=base/item['path']
        assert p.is_file() and p.parent==base, item['path']
        data=p.read_bytes()
        assert len(data)==item['bytes'], item['path']
        assert hashlib.sha256(data).hexdigest()==item['sha256'], item['path']
        checks+=1
assert hashlib.sha256((root/'public/FROZEN_MANIFEST.json').read_bytes()).hexdigest()==\
    'b021e926e34ae33bfb761b158d69d18355eddaad87331e2585d0e4977b971a90'
receipt=json.loads((root/'audit/AUDIT_RECEIPT.json').read_text())
assert receipt['verdict']=='pass_no_blocking_mathematical_defect'
out=subprocess.run([sys.executable,str(root/'public/verify.py')],check=True,
                   capture_output=True).stdout
assert out==(root/'public/checks.json').read_bytes()
assert out==(root/'audit/REPLAY_CHECKS.json').read_bytes()
data=json.loads(out)
assert data['all_controls_passed'] is True and data['assertions']==14944
print(json.dumps({'problem_id':'30001182','manifest_file_checks':checks,
                  'original_manifest_hash_verified':True,
                  'byte_identical_replay':True,
                  'auxiliary_assertions':data['assertions'],
                  'audit_verdict':receipt['verdict']},indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Portable local replay of controls and exact-copy bindings; does not prove geometry."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
runs=[]
for name in ['verify_manifest.py','checks.py','test_integrity.py','test_nested_manifest_regression.py']:
    r=subprocess.run([sys.executable,str(root/name)],cwd=root,capture_output=True)
    if r.returncode:
        sys.stderr.buffer.write(r.stderr)
        raise SystemExit(f'Replay failed: {name}')
    payload=json.loads(r.stdout)
    runs.append({'program':name,'exit_code':0,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'result':payload})
bindings=json.loads((root/'review_bindings.json').read_text())['bindings']
for b in bindings:
    raw=(root/b['v2_path']).read_bytes()
    if len(raw)!=b['bytes'] or hashlib.sha256(raw).hexdigest()!=b['sha256']:
        raise AssertionError('Copied review/tool binding mismatch: '+b['v2_path'])
print(json.dumps({'status':'PASS','scope':'portable integrity and finite controls, not geometry verification',
                 'copied_bindings_verified':len(bindings),'program_runs':runs},indent=2,sort_keys=True))

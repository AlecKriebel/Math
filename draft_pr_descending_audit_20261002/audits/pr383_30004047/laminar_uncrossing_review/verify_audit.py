#!/usr/bin/env python3
"""Read-only integrity check for this independent audit and frozen Git scope."""
from pathlib import Path
from hashlib import sha256
import json, subprocess
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
m=json.loads((HERE/'AUDIT_MANIFEST.json').read_text())
assert m['head']=='967e8e489aa4599f712d5ddcde62e591827f7e38'
for f in m['files']:
 b=(HERE/f['path']).read_bytes()
 assert len(b)==f['bytes'] and sha256(b).hexdigest()==f['sha256'],f['path']
sm=json.loads((BASE/'snapshot_manifest.json').read_text())
assert sm['head']==m['head'] and len(sm['files'])==49
for f in sm['files']:
 b=(BASE/'snapshot'/f['path']).read_bytes()
 g=subprocess.check_output(['git','show',m['head']+':'+f['path']],cwd=HERE)
 assert b==g and len(b)==f['bytes'] and sha256(b).hexdigest()==f['sha256'],f['path']
for t in [3,4,5]:
 assert (HERE/'private_B'/f'TURN_{t}_CHECKS.json').read_bytes()==(BASE/'snapshot/unsolved_math_prioritization/attempts/30004047'/f'TURN_{t}_CHECKS.json').read_bytes()
print(json.dumps({'status':'PASS','audit_artifacts':len(m['files']),'frozen_git_files':len(sm['files']),'private_B_byte_matches':3,'head':m['head']},indent=2))

#!/usr/bin/env python3
"""Verify authored packet bytes and replay exact finite controls."""
from pathlib import Path
import hashlib,json,subprocess,sys
base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
for row in manifest['files']:
 p=base/row['path']; data=p.read_bytes()
 assert len(data)==row['bytes'], row['path']
 assert hashlib.sha256(data).hexdigest()==row['sha256'], row['path']
observed=json.loads(subprocess.check_output([sys.executable,str(base/'code/verify_signatures.py')],cwd=base,text=True))
expected=json.loads((base/'results/verification.json').read_text())
assert observed==expected, 'Replay differs from saved output'
print(json.dumps({'status':'PASS','manifest_files_verified':len(manifest['files']),'finite_control_replay':'exact match','general_problem_solved':False},sort_keys=True))

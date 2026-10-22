#!/usr/bin/env python3
"""Strict flat-inventory, SHA-256, and deterministic independent replay."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={x['path']:x for x in manifest['files']}
actual={}
for p in root.rglob('*'):
    name=p.relative_to(root).as_posix()
    if p.is_symlink() or not p.is_file():
        raise SystemExit('FAIL: nonregular or unexpected directory '+name)
    if name!='MANIFEST.json':actual[name]=p
if set(actual)!=set(expected):
    raise SystemExit('FAIL: recursive inventory mismatch')
for name,p in actual.items():
    b=p.read_bytes(); e=expected[name]
    if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:
        raise SystemExit('FAIL: integrity '+name)
p=subprocess.run([sys.executable,'-B',str(root/'independent_verify.py')],capture_output=True)
if p.returncode:
    sys.stderr.buffer.write(p.stderr)
    raise SystemExit('FAIL: independent computation')
if p.stdout!=(root/'independent_verification.json').read_bytes():
    raise SystemExit('FAIL: deterministic replay mismatch')
x=json.loads(p.stdout)
if x['assertion_count']!=manifest['independent_assertions']:
    raise SystemExit('FAIL: assertion count mismatch')
print(json.dumps({'status':'PASS_INDEPENDENT_AUDIT_INTEGRITY_AND_REPLAY','files_verified':len(expected),'independent_assertions':x['assertion_count'],'verdict':manifest['verdict'],'general_projective_question':'unresolved_here'},sort_keys=True))

#!/usr/bin/env python3
"""Verify frozen file integrity and replay all exact author controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
for entry in manifest['files']:
    p=root/entry['path']
    if p.is_symlink() or not p.is_file():
        raise SystemExit('FAIL: missing/nonregular '+entry['path'])
    b=p.read_bytes()
    if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
        raise SystemExit('FAIL: integrity '+entry['path'])
actual=sorted(p.name for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.json')
expected=sorted(x['path'] for x in manifest['files'])
if actual!=expected:
    raise SystemExit('FAIL: packet inventory differs from manifest')
p=subprocess.run([sys.executable,'-B',str(root/'verify.py')],capture_output=True)
if p.returncode:
    sys.stderr.buffer.write(p.stderr)
    raise SystemExit('FAIL: exact control execution')
if p.stdout!=(root/'verification.json').read_bytes():
    raise SystemExit('FAIL: exact control output mismatch')
result=json.loads(p.stdout)
print(json.dumps({'status':'PASS_AUTHOR_PACKET_INTEGRITY_AND_REPLAY',
                  'files_verified':len(expected),
                  'exact_assertions':result['assertion_count'],
                  'mathematical_scope':'Scoped partial only; general AIM question unresolved.'},sort_keys=True))

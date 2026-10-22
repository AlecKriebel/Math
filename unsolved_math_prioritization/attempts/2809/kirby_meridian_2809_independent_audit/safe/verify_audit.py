#!/usr/bin/env python3
"""Mandatory recursive manifest and independent-result replay, active under -O."""
import hashlib, json, subprocess, sys
from pathlib import Path

def need(ok,message):
    if not ok:raise RuntimeError(message)

root=Path(__file__).resolve().parent
entries=json.loads((root/'MANIFEST.json').read_text())['files']
expected={e['path'] for e in entries}
need(len(entries)==len(expected),'Duplicate manifest entries')
paths=list(root.rglob('*'))
need(not any(p.is_symlink() for p in paths),'Symlink in audit packet')
actual={p.relative_to(root).as_posix() for p in paths if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.json'}
need(actual==expected,'Audit packet membership mismatch')
for e in entries:
    p=root/e['path'];need(p.parent==root,'Unexpected nested manifest path')
    b=p.read_bytes();need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],
                        'Audit hash mismatch: '+e['path'])
for flags in ([],['-O']):
    p=subprocess.run([sys.executable,*flags,str(root/'independent_controls.py')],capture_output=True,timeout=30)
    need(p.returncode==0 and p.stdout==(root/'INDEPENDENT_RESULTS.json').read_bytes(),
         'Independent controls do not reproduce the saved result')
print('PASS: complete audit manifest and ordinary/optimized independent replay; author v2 correction acceptance remains pending.')

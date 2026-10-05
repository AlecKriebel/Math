#!/usr/bin/env python3
"""Verify exact allowlist, manifest digests and reproducible finite check output."""
from pathlib import Path
import hashlib, json, subprocess, sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={x['path'] for x in manifest['files']}|{'MANIFEST.json'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual!=expected:
    raise SystemExit('FAIL: payload membership differs: '+repr(actual^expected))
for row in manifest['files']:
    p=root/row['path']
    if p.is_symlink() or '..' in p.relative_to(root).parts:
        raise SystemExit('FAIL: unsafe member')
    data=p.read_bytes()
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise SystemExit('FAIL: bytes/digest: '+row['path'])
result=subprocess.run([sys.executable,str(root/'checks.py')],capture_output=True,text=True,check=True)
if json.loads(result.stdout)!=json.loads((root/'CHECK_RESULTS.json').read_text()):
    raise SystemExit('FAIL: non-reproducing exact check result')
print(json.dumps({'packet':'PASS','payload_files':len(manifest['files']),
                  'finite_checks':json.loads(result.stdout)['assertions'],
                  'mathematical_verdict':'NO RESOLUTION'},sort_keys=True))

#!/usr/bin/env python3
"""Check the frozen author manifest, then replay the deterministic exact tests."""
from pathlib import Path
import hashlib, subprocess, sys, json
root=Path(__file__).resolve().parent
records=[]
for line in (root/'MANIFEST.sha256').read_text().splitlines():
    digest,name=line.split('  ',1)
    path=root/name
    if path.resolve().parent!=root: raise ValueError('Manifest must list only direct packet files')
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=digest: raise AssertionError('Digest mismatch: '+name)
    records.append(name)
expected=(root/'VERIFICATION.json').read_bytes()
actual=subprocess.check_output([sys.executable,str(root/'verify.py')],cwd=root)
if actual!=expected: raise AssertionError('Verification receipt does not replay byte-for-byte')
print(json.dumps({'manifest_files_checked':len(records),'replay':'BYTE_IDENTICAL','status':'PASS'},sort_keys=True))

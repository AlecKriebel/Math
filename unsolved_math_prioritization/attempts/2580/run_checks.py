#!/usr/bin/env python3
"""Reproduce the original finite checks and independent audit controls."""
from pathlib import Path
import hashlib,json,subprocess,sys
r=Path(__file__).resolve().parent
m=json.loads((r/'AUTHOR_MANIFEST.json').read_text())
for name,digest in m['files'].items():
    assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
a=json.loads(subprocess.check_output([sys.executable,str(r/'verify_partial_results.py')]))
assert a==json.loads((r/'verification.json').read_text())
b=json.loads(subprocess.check_output([sys.executable,str(r/'audit/independent_field_euler_checks.py')]))
assert b==json.loads((r/'audit/independent_field_euler_checks.json').read_text())
print('PASS: author hashes, original finite checks and independent controls; KOU-21.71 remains unsolved.')

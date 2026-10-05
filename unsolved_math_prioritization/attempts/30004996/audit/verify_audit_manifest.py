#!/usr/bin/env python3
"""Check all declared audit payloads without source files, network, or packages."""
import hashlib
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'AUDIT_MANIFEST.json').read_bytes())
files = manifest['files']
actual = {p.name for p in HERE.iterdir()}
expected = {r['path'] for r in files} | {'AUDIT_MANIFEST.json', 'AUDIT_MANIFEST.sha256'}
if actual != expected:
    raise SystemExit('FAIL: missing or undeclared audit entries')
for row in files:
    p = HERE / row['path']
    if not p.is_file() or p.is_symlink():
        raise SystemExit('FAIL: not a regular audit file: ' + row['path'])
    raw = p.read_bytes()
    if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise SystemExit('FAIL: payload mismatch: ' + row['path'])
expected_digest, name = (HERE / 'AUDIT_MANIFEST.sha256').read_text().split()
if name != 'AUDIT_MANIFEST.json' or hashlib.sha256((HERE/name).read_bytes()).hexdigest() != expected_digest:
    raise SystemExit('FAIL: audit manifest checksum mismatch')
print(json.dumps({'all_passed': True, 'audit_payloads': len(files), 'audit_manifest_sha256': expected_digest}, indent=2, sort_keys=True))

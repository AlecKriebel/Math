#!/usr/bin/env python3
"""Verify only this frozen author packet, without modifying files."""
from pathlib import Path
import hashlib,json
b=Path(__file__).resolve().parent
m=json.loads((b/'SHA256SUMS.json').read_text())
for name,expected in m['files'].items():
    p=b/name
    if not p.is_file():raise SystemExit('Missing file: '+name)
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual!=expected:raise SystemExit('Hash mismatch: '+name)
actual_names={p.name for p in b.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'}
if actual_names!=set(m['files']):raise SystemExit('Allowlist differs from packet files')
print(json.dumps({'status':'passed','verified_files':len(m['files']),'manifest_excluded_from_own_hash':True},sort_keys=True))

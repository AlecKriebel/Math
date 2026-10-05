#!/usr/bin/env python3
"""Verify the frozen author packet. No source downloads or credentials needed."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected=set(manifest['files'])
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
assert actual==expected,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for name,entry in manifest['files'].items():
    p=root/name
    assert p.resolve().is_relative_to(root)
    data=p.read_bytes()
    assert len(data)==entry['bytes'],name
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],name
assert json.loads((root/'STATUS.json').read_text())['status'] in ('unsolved','claimed_solved','already_solved')
assert len((root/'turns.jsonl').read_text().splitlines())==5
print(json.dumps({'passed':True,'files_verified':len(expected),'mode':'frozen author packet SHA-256 and byte-count verification'},indent=2))

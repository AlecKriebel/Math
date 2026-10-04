#!/usr/bin/env python3
"""Author-freeze integrity, not mathematical correctness."""
from pathlib import Path
import hashlib
import json
import sys
root = Path(__file__).resolve().parent
manifest = json.loads((root / 'SHA256SUMS.json').read_text())
expected = set(manifest['files'])
actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
          and p.name != 'SHA256SUMS.json' and '__pycache__' not in p.parts}
errors = []
if actual != expected:
    errors.append({'missing': sorted(expected-actual), 'extra': sorted(actual-expected)})
for name, record in manifest['files'].items():
    p = root / name
    if p.exists():
        data = p.read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            errors.append(name)
print(json.dumps({'result': 'PASS' if not errors else 'FAIL', 'file_count': len(expected),
                  'errors': errors, 'limit': 'Integrity only, not mathematical correctness.'}, indent=2))
sys.exit(bool(errors))

#!/usr/bin/env python3
"""Verify original file hashes and reproduce bounded exact regression results."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'AUTHOR_MANIFEST.json').read_text())
verified = []
for entry in manifest['files']:
    path = root / entry['path']
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    assert len(data) == entry['bytes'], entry['path']
    assert actual == entry['sha256'], entry['path']
    verified.append(entry['path'])
completed = subprocess.run([sys.executable, str(root / 'verify_partial_results.py')],
                           check=True, capture_output=True, text=True, cwd=root)
actual_results = json.loads(completed.stdout)
expected_results = json.loads((root / 'verification.json').read_text())
assert actual_results == expected_results
print(json.dumps({'status': 'PASS', 'original_files_verified': verified,
                  'regression_results_reproduced': True,
                  'scope': 'partial results; complete original problem unresolved'}, indent=2))

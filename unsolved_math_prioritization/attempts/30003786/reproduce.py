#!/usr/bin/env python3
"""Portable standard-library replay. Run from any working directory."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
for manifest in [ROOT / 'MANIFEST.sha256', ROOT / 'public/MANIFEST.sha256', ROOT / 'audit/MANIFEST.sha256']:
    for line in manifest.read_text().splitlines():
        digest, relative = line.split('  ', 1)
        p = manifest.parent / relative
        assert hashlib.sha256(p.read_bytes()).hexdigest() == digest, str(p)
with tempfile.TemporaryDirectory() as tmp:
    results = []
    for program, expected in [('verify_exact.py', 'verify_exact_results.json'), ('audit/independent_controls.py', 'audit/independent_results.json')]:
        completed = subprocess.run([sys.executable, str(ROOT / program)], cwd=tmp, check=True, capture_output=True)
        assert completed.stdout == (ROOT / expected).read_bytes(), program + ': output mismatch'
        parsed = json.loads(completed.stdout)
        results.append({'program': program, 'status': parsed.get('status'), 'assertions': parsed.get('assertions')})
print(json.dumps({'status': 'PASS', 'all_hashes': 'PASS', 'replays': results}, indent=2))

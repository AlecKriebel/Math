#!/usr/bin/env python3
"""Verify the frozen author inventory and replay its finite controls offline."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

p = Path(__file__).resolve().parent
m = json.loads((p / 'AUTHOR_MANIFEST.json').read_text())
declared = {f['name']: f for f in m['files']}
actual = {f.name for f in p.iterdir() if f.is_file()}
if actual != set(declared) | {'AUTHOR_MANIFEST.json'}:
    raise SystemExit('File inventory does not match frozen author manifest')
for name, record in declared.items():
    data = (p / name).read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise SystemExit('Hash/size mismatch: ' + name)
saved = (p / 'CONTROL_RESULTS.json').read_bytes()
for flags in ([], ['-O']):
    result = subprocess.check_output([sys.executable] + flags + [str(p / 'verify_controls.py')])
    if result != saved:
        raise SystemExit('Finite control replay mismatch')
print(json.dumps({'status': 'pass', 'manifest_bound_files': len(declared),
                  'finite_controls': json.loads(saved)['checks'],
                  'normal_and_optimized_replays_match': True,
                  'scope': 'Integrity and finite algebra only; not a topology proof certificate.'},
                 indent=2, sort_keys=True))

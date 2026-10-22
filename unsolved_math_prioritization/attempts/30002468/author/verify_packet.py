#!/usr/bin/env python3
"""Check the frozen payload and rerun its exact, finite control suite."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
listed = {x['path'] for x in manifest['files']}
actual = {p.name for p in root.iterdir() if p.is_file() and p.name != 'MANIFEST.json'}
assert listed == actual, (listed, actual)
for item in manifest['files']:
    p=root / item['path']
    assert p.parent == root and not p.is_symlink()
    b=p.read_bytes()
    assert len(b)==item['bytes'],item['path']
    assert hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
run = subprocess.run([sys.executable,str(root/'verify_exact.py')],check=True,
                     text=True,capture_output=True)
assert json.loads(run.stdout)==json.loads((root/'EXACT_RESULTS.json').read_text())
print(json.dumps({'status':'PASS','verified_files':len(listed),
                  'exact_controls':'PASS',
                  'formal_proof_checker':False,
                  'external_theorem_reproved':False},indent=2))

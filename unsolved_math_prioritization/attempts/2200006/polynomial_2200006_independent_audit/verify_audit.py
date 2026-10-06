#!/usr/bin/env python3
"""Strict audit-package hash check and full deterministic local replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={row['path'] for row in manifest['files']}|{'MANIFEST.json'}
actual=set()
for p in root.rglob('*'):
    if p.is_symlink() or not p.is_file():
        raise ValueError('Non-regular audit entry: '+p.relative_to(root).as_posix())
    actual.add(p.relative_to(root).as_posix())
if actual != expected:
    raise ValueError('Audit inventory mismatch')
for row in manifest['files']:
    p=Path(row['path'])
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('Unsafe audit path')
    data=(root/p).read_bytes()
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise ValueError('Audit hash or size mismatch: '+str(p))
for script,receipt in [('verify_independent.py','independent_results.json'),('test_author_replay.py','replay_and_mutation_results.json')]:
    run=subprocess.run([sys.executable,'-B',str(root/script)],stdout=subprocess.PIPE,check=True)
    if run.stdout != (root/receipt).read_bytes():
        raise ValueError('Audit replay differs: '+script)
print(json.dumps({'inventory':'PASS','hashes':'PASS','independent_replay':'PASS','author_replay_and_mutations':'PASS','files':len(expected),'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()},sort_keys=True))

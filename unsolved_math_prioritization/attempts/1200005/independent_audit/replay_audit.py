#!/usr/bin/env python3
"""Verify this audit's bindings and reproduce exact offline mathematical checks."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--author',type=Path,default=root.parent/'questions_1200005'/'safe_output')
args=parser.parse_args()
if sys.flags.optimize:
    raise SystemExit('Use Python without -O: the frozen author controls use assertions.')
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
expected_files=set(manifest['files'])|{'AUDIT_MANIFEST.json'}
actual_files={p.name for p in root.iterdir() if p.is_file()}
if actual_files != expected_files:
    raise SystemExit('Audit file allowlist mismatch')
if any(p.is_dir() for p in root.iterdir()):
    raise SystemExit('Unexpected directory inside safe audit')
for name,info in manifest['files'].items():
    p=root/name
    raw=p.read_bytes()
    if p.is_symlink() or len(raw)!=info['bytes'] or hashlib.sha256(raw).hexdigest()!=info['sha256']:
        raise SystemExit('Audit binding mismatch: '+name)
run=subprocess.run([sys.executable,'-B',str(root/'independent_verifier.py'),'--author',str(args.author.resolve())],capture_output=True,check=True)
if run.stdout!=(root/'INDEPENDENT_RESULTS.json').read_bytes():
    raise SystemExit('Independent control results differ')
print(json.dumps({'status':'PASS','audit_bound_files':len(manifest['files']),
                  'mathematical_scope':'partial claims only; unsolved target',
                  'independent_results_sha256':hashlib.sha256(run.stdout).hexdigest()},sort_keys=True))

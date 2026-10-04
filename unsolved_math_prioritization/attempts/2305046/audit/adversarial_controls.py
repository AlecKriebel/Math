#!/usr/bin/env python3
"""Read-only audit of the frozen package; mutation tests use temporary copies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent / 'public'
EXPECTED = 'ea9f5520cee6dbc749de5eceff5522140f37829a4b30859093823137a693e7f8'
manifest = json.loads((ROOT / 'SHA256SUMS.json').read_text())
assert hashlib.sha256((ROOT / 'SHA256SUMS.json').read_bytes()).hexdigest() == EXPECTED
# Only root manifest and actual Python bytecode caches are exempt here.
actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
          and str(p.relative_to(ROOT)) != 'SHA256SUMS.json'
          and not ('__pycache__' in p.relative_to(ROOT).parts and p.suffix == '.pyc')}
assert actual == set(manifest)
for name, digest in manifest.items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest

def run_verifier(where):
    return subprocess.run([sys.executable, str(where/'verify_manifest.py')],
                          capture_output=True, text=True,
                          env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'}).returncode

results = {}
for mutation in ['none', 'edit_proof', 'extra_file', 'nested_manifest']:
    with tempfile.TemporaryDirectory(prefix='maclane-audit-') as tmp:
        copy = Path(tmp)/'public'
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('__pycache__'))
        if mutation == 'edit_proof':
            with (copy/'PROOF.md').open('a') as f:
                f.write('\nAUDIT MUTATION\n')
        elif mutation == 'extra_file':
            (copy/'unexpected.txt').write_text('AUDIT MUTATION\n')
        elif mutation == 'nested_manifest':
            (copy/'unexpected').mkdir()
            (copy/'unexpected'/'SHA256SUMS.json').write_text('{}\n')
        code = run_verifier(copy)
        results[mutation] = {'exit_code':code, 'accepted':code == 0}
assert results['none']['accepted']
assert not results['edit_proof']['accepted']
assert not results['extra_file']['accepted']
assert results['nested_manifest']['accepted']  # documented nonblocking hardening issue
# Check again after all isolated-copy mutations.
assert hashlib.sha256((ROOT / 'SHA256SUMS.json').read_bytes()).hexdigest() == EXPECTED
for name, digest in manifest.items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
print(json.dumps({'strict_frozen_inventory':'passed', 'file_count':len(actual),
                  'manifest_sha256':EXPECTED, 'isolated_mutation_tests':results,
                  'frozen_content_unchanged':True,
                  'limits':'Integrity tests only; no mathematical proof certification.'},
                 indent=2, sort_keys=True))

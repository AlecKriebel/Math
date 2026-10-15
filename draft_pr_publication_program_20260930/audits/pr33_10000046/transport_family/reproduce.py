#!/usr/bin/env python3
"""Reproduce family controls in ignored private copies and verify frozen inputs.
This creates only tmp/* and REPRODUCIBILITY.json in this exclusive folder.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
private = HERE/'tmp/final_reproduction'
private.mkdir(parents=True, exist_ok=True)
for name in ('controls.py', 'check_certificates.py', 'mutation_checks.py'):
    shutil.copyfile(HERE/name, private/name)
records = []
for name in ('controls.py', 'check_certificates.py', 'mutation_checks.py'):
    run = subprocess.run([sys.executable, str(private/name)], capture_output=True)
    (private/(name+'.stdout')).write_bytes(run.stdout)
    (private/(name+'.stderr')).write_bytes(run.stderr)
    if run.returncode:
        raise RuntimeError(name+': '+run.stderr.decode())
    records.append({'program': name, 'exit': run.returncode,
                    'stdout_bytes': len(run.stdout), 'stderr_bytes': len(run.stderr)})
same = []
for name in ('certificates.json', 'controls_results.json', 'MUTATION_RESULTS.json'):
    got, expected = (private/name).read_bytes(), (HERE/name).read_bytes()
    if got != expected:
        raise AssertionError('nondeterministic output: '+name)
    same.append({'file': name, 'bytes': len(got), 'byte_identical': True,
                 'sha256': hashlib.sha256(got).hexdigest()})
frozen = json.loads((AUDIT/'snapshot_manifest.json').read_text())
inputs = []
for entry in frozen['files']:
    raw = (AUDIT/'source_snapshot'/entry['path']).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if digest != entry['sha256'] or len(raw) != entry['size'] or blob != entry['git_blob']:
        raise AssertionError('frozen original changed: '+entry['path'])
    inputs.append({'path': entry['path'], 'bytes': len(raw), 'sha256': digest,
                   'git_blob': blob, 'unchanged': True})
patch = (AUDIT/'pr_input/diff.patch').read_bytes()
if hashlib.sha256(patch).hexdigest() != '7ef73671ccd579fbb59d73588b861a9acb5f60bb0d03b3563ccb036975039f6a':
    raise AssertionError('frozen exact diff changed')
result = {'utc': datetime.now(timezone.utc).isoformat(), 'pass': True,
          'original_head': 'de5877c38bf3604f0a8e074af7a9c55fca334522',
          'actual_and_metadata_base': 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0',
          'programs': records, 'deterministic_outputs': same,
          'frozen_originals': inputs, 'frozen_diff_unchanged': True,
          'seal_sha256': hashlib.sha256((HERE/'SEALED_CLAIM.md').read_bytes()).hexdigest(),
          'scope': 'No imports from old implementations, no shared-state/Git/queue mutation; adds 0 attempts.'}
(HERE/'REPRODUCIBILITY.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'frozen_originals'}, indent=2))

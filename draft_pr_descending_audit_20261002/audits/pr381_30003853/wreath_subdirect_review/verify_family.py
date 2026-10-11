#!/usr/bin/env python3
"""Verify this family's frozen inputs, early seal, sources, and new controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import os

P = Path(__file__).resolve().parent
A = P.parent
REPO = P.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


inputs = json.loads((P/'INPUT_MANIFEST.json').read_text())
assert len(inputs['files']) == 45
for e in inputs['files']:
    p = A/'snapshot'/e['path']
    blob = subprocess.check_output(['git', 'show', inputs['head']+':'+e['path']], cwd=REPO)
    assert p.read_bytes() == blob
    assert sha(p) == e['manifest_sha256'] == e['snapshot_sha256'] == e['git_sha256']
for e in json.loads((P/'EARLY_INDEPENDENCE_SEAL.json').read_text())['files']:
    assert sha(P/e['path']) == e['sha256'], e['path']
for source_name in ['SOURCE_RECEIPT.json', 'ADDITIONAL_SOURCE_RECEIPT.json']:
    for e in json.loads((P/source_name).read_text())['sources']:
        raw = P/'raw_sources'/Path(e['path']).name
        assert len(raw.read_bytes()) == e['bytes'] and sha(raw) == e['sha256']
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
for script in ['new_algebra_checks.py', 'nonabelian_and_lattice_controls.py']:
    actual = subprocess.run([sys.executable, str(P/script)], cwd=P,
                            env=env, capture_output=True, check=True)
    expected = P/(Path(script).stem+'.stdout.json')
    assert actual.stdout == expected.read_bytes(), script
    assert actual.stderr == b''
    assert json.loads(actual.stdout)['all_passed']
out = P/'OUTPUT_MANIFEST.json'
if out.exists():
    for e in json.loads(out.read_text())['files']:
        path = P/e['path']
        assert len(path.read_bytes()) == e['bytes'] and sha(path) == e['sha256'], e['path']
print('PASS: 45 frozen Git/SHA inputs; immutable early seal; five primary PDFs; both new exact-control results; available output bindings.')

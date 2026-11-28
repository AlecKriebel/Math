#!/usr/bin/env python3
"""Verify all public hashes and replay exact controls without modifying frozen files."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def check_manifest(name, base):
    doc = json.loads((base / name).read_text())
    for row in doc['files']:
        data = (base / row['path']).read_bytes()
        assert len(data) == row['bytes'], (name, row['path'], 'length')
        assert hashlib.sha256(data).hexdigest() == row['sha256'], (name, row['path'], 'hash')
    return len(doc['files'])

counts = {
    'frozen_author_files': check_manifest('RELEASE_MANIFEST.json', ROOT),
    'audit_files': check_manifest('AUDIT_MANIFEST.json', ROOT / 'audit'),
    'publication_files': check_manifest('PUBLICATION_MANIFEST.json', ROOT),
}
with tempfile.TemporaryDirectory() as tmp:
    directory = Path(tmp)
    author = directory / 'verify_spectral_obstructions.py'
    shutil.copyfile(ROOT / 'checks' / author.name, author)
    author_stdout = subprocess.check_output([sys.executable, str(author)], cwd=directory)
    assert author_stdout == (ROOT / 'checks' / 'verification_results.json').read_bytes()
    assert (directory / 'verification_results.json').read_bytes() == author_stdout
    independent_stdout = subprocess.check_output(
        [sys.executable, str(ROOT / 'audit' / 'independent_checks.py')], cwd=directory)
    actual = json.loads(independent_stdout)
    recorded = json.loads((ROOT / 'audit' / 'independent_results.json').read_text())
    # The public layout intentionally replaces the audit's former external hook.
    integrity = actual.pop('freeze_integrity')
    historical_integrity = recorded.pop('freeze_integrity')
    assert integrity['status'] == historical_integrity['status'] == 'PASS'
    assert integrity['files'] == historical_integrity['files']
    assert integrity['public_release_manifest_verified'] is True
    assert actual == recorded

print(json.dumps({
    'status': 'PASS', **counts,
    'author_replay_byte_identical': True,
    'independent_mathematical_results_identical': True,
    'portable_frozen_integrity': 'PASS',
    'original_problem': 'unsolved',
    'attempts_completed': 5,
    'full_resolution_claim': False,
}, indent=2))

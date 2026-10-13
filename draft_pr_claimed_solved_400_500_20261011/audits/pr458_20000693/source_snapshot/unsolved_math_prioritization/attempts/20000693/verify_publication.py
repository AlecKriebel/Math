#!/usr/bin/env python3
"""Verify the public research subset; optional isolated replay of both suites."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def verify(root, records):
    for name, expected in records.items():
        b = (root / name).read_bytes()
        assert len(b) == expected['bytes'], f'{name}: byte count mismatch'
        assert sha256(b) == expected['sha256'], f'{name}: SHA-256 mismatch'

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--replay', action='store_true', help='run both scripts in temporary directories')
args = parser.parse_args()
manifest = json.loads((ROOT / 'PUBLICATION_MANIFEST.json').read_text())
verify(ROOT, manifest['files'])
actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert actual == set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing public file'
for folder, name, expected_hash in [
    ('author', 'manifest.json', '49c26cff89e8c5fcd9fd917c586acaa0902d22f30e1c4c8874ed2d212c9ff110'),
    ('review', 'REVIEW_MANIFEST.json', '9f67aaf0515d18c6462599ce02140d81cdb8cf72ed214d02d1b93cdfc51ea417'),
]:
    b = (ROOT / folder / name).read_bytes()
    assert sha256(b) == expected_hash, f'{name}: frozen manifest changed'
    records = json.loads(b)['files']
    excluded = set(manifest['excluded_review_source_files']) if folder == 'review' else set()
    assert excluded <= set(records)
    verify(ROOT / folder, {k: v for k, v in records.items() if k not in excluded})
assert not (ROOT / 'review/topacogullari2019.txt').exists()
state = json.loads((ROOT / 'PUBLICATION_STATE.json').read_text())
assert state['author_turns_used'] == 1 and state['turn_limit'] == 5
assert not state['asymptotic_proved'] and not state['novelty_claimed']
assert state['queue_status'] == 'claimed_solved'
replays = []
if args.replay:
    for script, output, expected in [
        ('author/verify.py', 'verification.json', 'author/verification.json'),
        ('review/reviewer_checks.py', 'REVIEWER_CHECKS.json', 'review/REVIEWER_CHECKS.json'),
    ]:
        with tempfile.TemporaryDirectory(prefix='dirichlet-20000693-') as temp:
            copied = Path(temp) / Path(script).name
            shutil.copyfile(ROOT / script, copied)
            run = subprocess.run([sys.executable, str(copied)], cwd=temp, capture_output=True, text=True)
            assert run.returncode == 0, run.stderr or run.stdout
            generated = (Path(temp) / output).read_bytes()
            assert generated == (ROOT / expected).read_bytes(), f'{script}: replay report differs'
            report = json.loads(generated)
            assert report['status'] == 'PASS' and not report['asymptotic_proved']
            replays.append({'script': script, 'status': 'PASS', 'byte_identical': True,
                            'sha256': sha256(generated)})
print(json.dumps({'status': 'PASS', 'public_files': len(actual), 'frozen_research_files': 23,
                  'author_turns_used': 1, 'asymptotic_proved': False, 'replays': replays}, indent=2))

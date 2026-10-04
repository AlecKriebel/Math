#!/usr/bin/env python3
"""Verify the frozen public publication and replay exact scoped controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_manifest(root, filename):
    manifest = json.loads((root / filename).read_text())
    require(manifest['algorithm'] == 'sha256', 'manifest algorithm')
    for entry in manifest['files']:
        p = Path(entry['path'])
        require(not p.is_absolute() and '..' not in p.parts, 'safe manifest path')
        data = (root / p).read_bytes()
        require(len(data) == entry['bytes'], str(p)+' length')
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], str(p)+' hash')
    return len(manifest['files'])


publication_count = verify_manifest(ROOT, 'PUBLICATION_MANIFEST.json')
author_count = verify_manifest(ROOT / 'author', 'SHA256SUMS.json')
audit_count = verify_manifest(ROOT / 'audit', 'AUDIT_MANIFEST.json')
replay = subprocess.run([sys.executable, str(ROOT / 'author' / 'verify.py')],
                        cwd=ROOT / 'author', check=True, capture_output=True).stdout
require(replay == (ROOT / 'author' / 'CHECKS.json').read_bytes(), 'author exact replay')
audit = subprocess.run([sys.executable, str(ROOT / 'audit' / 'audit_verify.py'),
                        str(ROOT / 'author')], cwd=ROOT, check=True,
                       capture_output=True).stdout
require(audit == (ROOT / 'audit' / 'ADDITIONAL_CONTROLS.json').read_bytes(),
        'independent exact replay')
print(json.dumps({'status': 'PASS', 'publication_manifest_files': publication_count,
                  'author_manifest_files': author_count, 'audit_manifest_files': audit_count,
                  'author_assertions': json.loads(replay)['total_assertions'],
                  'additional_independent_assertions': json.loads(audit)['additional_total_assertions'],
                  'original_problem_status': 'unresolved'}, indent=2, sort_keys=True))

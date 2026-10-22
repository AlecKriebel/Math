#!/usr/bin/env python3
"""Verify the closed authored-file inventory without modifying any files."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest_path = root / 'MANIFEST.json'
data = json.loads(manifest_path.read_text())
expected = data['files']
if len(expected) != data['file_count']:
    raise SystemExit('FAIL: manifest count disagrees')
if len({row['path'] for row in expected}) != len(expected):
    raise SystemExit('FAIL: duplicate paths')
actual = {}
for path in root.rglob('*'):
    if path.is_symlink():
        raise SystemExit('FAIL: unexpected symlink')
    if path.is_file() and path != manifest_path:
        actual[path.relative_to(root).as_posix()] = path
if set(actual) != {row['path'] for row in expected}:
    raise SystemExit('FAIL: recursive regular-file set differs, including hidden files')
for row in expected:
    body = actual[row['path']].read_bytes()
    if len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['sha256']:
        raise SystemExit('FAIL: bytes/hash differ: ' + row['path'])
verdict = json.loads((root / 'VERDICT.json').read_text())
if not verdict['closed'] or not verdict['audit_complete']:
    raise SystemExit('FAIL: verdict is not closed')
print(json.dumps({
    'result': 'PASS',
    'authored_regular_files_excluding_manifest': len(actual),
    'hidden_files_included': True,
    'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    'report_sha256': hashlib.sha256((root / 'REPORT.md').read_bytes()).hexdigest(),
    'verdict_sha256': hashlib.sha256((root / 'VERDICT.json').read_bytes()).hexdigest()
}, indent=2))

#!/usr/bin/env python3
"""Verify closed authored review plus the separately allowed six input snapshots."""
from pathlib import Path
import hashlib
import json
import stat

root = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

manifest = json.loads((root / 'REVIEW_MANIFEST.json').read_text())
listed = {}
for e in manifest['files']:
    name = e['path']
    require('/' not in name and '\\' not in name and name not in ['', '.', '..', 'REVIEW_MANIFEST.json'], 'Bad authored path')
    require(name not in listed, 'Duplicate authored path')
    listed[name] = e
snapshot = {e['path']: e for e in manifest['allowed_frozen_input_snapshot']}
require(len(snapshot) == 6, 'Wrong frozen input count')
expected = set(listed) | {'REVIEW_MANIFEST.json'} | set(snapshot)
actual = {}
for p in root.rglob('*'):
    require(not p.is_symlink(), 'Symlink in closed review')
    if p.is_dir():
        continue
    require(stat.S_ISREG(p.stat().st_mode), 'Nonregular object')
    actual[p.relative_to(root).as_posix()] = p.read_bytes()
require(set(actual) == expected, 'Review file closure mismatch')
for name, e in list(listed.items()) + list(snapshot.items()):
    data = actual[name]
    require(len(data) == e['bytes'] and hashlib.sha256(data).hexdigest() == e['sha256'], 'Fingerprint mismatch: ' + name)
expected_dirs = {'frozen_inputs', 'frozen_inputs/output', 'frozen_inputs/output/pdf'}
actual_dirs = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
require(actual_dirs == expected_dirs, 'Unexpected directory / private residue')
print('PASS:', len(listed), 'authored payloads plus manifest; six pinned allowed input snapshots; no private sources/extracts/renders or extras')

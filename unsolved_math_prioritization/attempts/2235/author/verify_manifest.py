#!/usr/bin/env python3
"""Strict, portable frozen-packet verification; Python standard library only.

The manifest is an internal inventory. Its external trust anchor is the
separately recorded manifest SHA-256 in the author freeze receipt.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest_path = root/'MANIFEST.json'
if manifest_path.is_symlink():
    raise SystemExit('FAIL: manifest is a symlink')
m = json.loads(manifest_path.read_text())
if m.get('schema') != 'erdos-2235-author-packet-v1':
    raise SystemExit('FAIL: unsupported manifest schema')
entries = m.get('files', [])
names = [e['path'] for e in entries]
if len(names) != len(set(names)) or any(Path(n).name != n for n in names):
    raise SystemExit('FAIL: duplicate or non-flat path')
expected = set(names) | {'MANIFEST.json'}
actual = {p.name for p in root.iterdir()}
if actual != expected:
    raise SystemExit('FAIL: inventory mismatch')
for e in entries:
    p = root/e['path']
    if p.is_symlink() or not p.is_file():
        raise SystemExit('FAIL: unsafe entry')
    b = p.read_bytes()
    if len(b) != e['bytes'] or hashlib.sha256(b).hexdigest() != e['sha256']:
        raise SystemExit('FAIL: content mismatch: ' + e['path'])
expected_output = (root/'VERIFICATION.json').read_bytes()
for flags in [[],['-O']]:
    r = subprocess.run([sys.executable,'-B',*flags,str(root/'verify.py')],
                       capture_output=True,check=True)
    if r.stdout != expected_output or r.stderr:
        raise SystemExit('FAIL: regression replay differs')
print(json.dumps({'status':'PASS','inventory_files':len(expected),
                  'hashed_payload_files':len(entries),
                  'normal_and_optimized_replays':'byte-identical',
                  'manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))

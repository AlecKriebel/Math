#!/usr/bin/env python3
"""Verify an authored-only packet's filenames and SHA-256 hashes."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT/'SHA256SUMS.json').read_text())
expected = manifest['files']
actual = {p.name for p in ROOT.iterdir() if p.is_file() and p.name != 'SHA256SUMS.json'}
assert actual == set(expected), (actual-set(expected),set(expected)-actual)
assert not any(p.is_dir() or p.is_symlink() for p in ROOT.iterdir())
for name, digest in expected.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
print(json.dumps({'manifest_passed':True,'files_checked':len(expected),'self_excluded':'SHA256SUMS.json'}))

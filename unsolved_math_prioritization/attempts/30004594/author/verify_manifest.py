#!/usr/bin/env python3
"""Verify bytes of files explicitly frozen in AUTHOR_MANIFEST.json."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
manifest = json.loads((base / 'AUTHOR_MANIFEST.json').read_text())
for row in manifest['files']:
    name = row['path']
    path = Path(name)
    assert not path.is_absolute() and '..' not in path.parts
    data = (base / path).read_bytes()
    assert len(data) == row['bytes'], name
    assert hashlib.sha256(data).hexdigest() == row['sha256'], name
print('PASS:', len(manifest['files']), 'frozen author files hash-match')

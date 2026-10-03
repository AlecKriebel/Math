#!/usr/bin/env python3
"""Verify public packet bytes and bounded checks; not a mathematical proof checker."""
import hashlib
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent
manifest = json.loads((root / 'PUBLIC_PACKET_MANIFEST.json').read_text())
for name, expected in manifest['files'].items():
    data = (root / name).read_bytes()
    assert len(data) == expected['bytes'], (name, 'length')
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], (name, 'sha256')
result = json.loads(subprocess.check_output([sys.executable, str(root / 'check_density_chain.py')], text=True))
assert result['passed'] is True and result['finite_identity_checks'] == 4240
print(json.dumps({'public_files_verified': len(manifest['files']), 'finite_identity_checks': 4240,
                  'scope': 'File integrity and bounded algebraic identities only; no formal proof certification.'}, indent=2))

#!/usr/bin/env python3
"""Verify the authored safe payload without network or file changes."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
expected = {'MANIFEST.json'}
for record in manifest['files']:
    name = record['path']
    path = root / name
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    assert path.is_file() and not path.is_symlink(), name
    assert path.resolve().is_relative_to(root), name
    data = path.read_bytes()
    assert len(data) == record['bytes'], name
    assert hashlib.sha256(data).hexdigest() == record['sha256'], name
    expected.add(name)
actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual == expected, {'unexpected': sorted(actual - expected), 'missing': sorted(expected - actual)}
result = subprocess.check_output([sys.executable, str(root / 'code/check_controls.py')])
assert result == (root / 'verification/controls.json').read_bytes()
print(json.dumps({'status': 'PASS', 'payload_files_including_manifest': len(actual),
                  'hashes': 'all matched', 'control_replay': 'byte-identical'}, sort_keys=True))

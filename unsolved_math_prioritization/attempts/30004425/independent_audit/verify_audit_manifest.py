#!/usr/bin/env python3
"""Read-only audit payload integrity and independent arithmetic replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
expected = set(manifest['files']) | {'MANIFEST.json'}
actual = {p.name for p in root.iterdir() if p.is_file()}
if actual != expected:
    raise AssertionError((expected-actual, actual-expected))
for name, metadata in manifest['files'].items():
    data = (root / name).read_bytes()
    if len(data) != metadata['bytes'] or hashlib.sha256(data).hexdigest() != metadata['sha256']:
        raise AssertionError(name)
replay = subprocess.check_output([sys.executable, str(root / 'independent_verify.py')])
if replay != (root / 'INDEPENDENT_RESULTS.json').read_bytes():
    raise AssertionError('Independent replay differs from saved output')
print(json.dumps({'result':'PASS','manifest_entries':len(manifest['files']),'deterministic_replay':'PASS','manifest_self_excluded':True}))

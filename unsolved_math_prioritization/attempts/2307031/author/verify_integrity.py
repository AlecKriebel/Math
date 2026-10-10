#!/usr/bin/env python3
"""Verify the frozen authored file set and exact deterministic replay."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
expected_names = {row['path'] for row in manifest['files']}
actual_names = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
assert actual_names == expected_names | {'AUTHOR_MANIFEST.json'}, (actual_names, expected_names)
for row in manifest['files']:
    payload = (ROOT/row['path']).read_bytes()
    assert len(payload) == row['bytes'], row['path']
    assert hashlib.sha256(payload).hexdigest() == row['sha256'], row['path']
import verify
replayed = verify.run()
expected = json.loads((ROOT/'EXPECTED_CHECKS.json').read_text())
assert replayed == expected
print(json.dumps({'status': 'frozen_authored_files_and_exact_replay_match',
                  'verified_file_count': len(manifest['files']),
                  'controls_status': replayed['status'],
                  'limits': 'Integrity and finite controls do not independently certify the proofs.'},
                 indent=2, sort_keys=True))

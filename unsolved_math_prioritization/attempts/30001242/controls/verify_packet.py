#!/usr/bin/env python3
"""Verify immutable author/review packets and exact deterministic outputs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
verified = 0
for folder, manifest_name in [('public', 'FROZEN_MANIFEST.json'), ('audit', 'AUDIT_MANIFEST.json')]:
    manifest = json.loads((root/folder/manifest_name).read_text())
    for name, entry in manifest['files'].items():
        data = (root/folder/name).read_bytes()
        assert len(data) == entry['bytes'], name
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], name
        verified += 1
author_manifest = hashlib.sha256((root/'public/FROZEN_MANIFEST.json').read_bytes()).hexdigest()
assert author_manifest == 'f21a7d5d214e56c29508b8758b8a80794deeb8ad3c731538a7b359ad2d7ef13e'
for script, expected in [('public/verify.py','public/checks.json'), ('audit/independent_verify.py','audit/independent_checks.json')]:
    result = subprocess.run([sys.executable, str(root/script)], cwd=root, check=True, capture_output=True)
    assert result.stdout == (root/expected).read_bytes(), script
print(json.dumps({'problem_id':30001242,'result':'PASS','manifest_files_verified':verified,
                  'author_manifest_sha256':author_manifest,'byte_identical_replays':2}, indent=2, sort_keys=True))

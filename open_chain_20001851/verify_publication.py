#!/usr/bin/env python3
"""Check the portable partial-results packet without accessing the network."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'PUBLICATION_MANIFEST.json').read_text())
for name, expected in manifest['files'].items():
    data = (root / name).read_bytes()
    assert len(data) == expected['bytes'], name
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
authors = json.loads((root / 'AUTHOR_MANIFEST.json').read_text())
for name, expected in authors['files'].items():
    data = (root / name).read_bytes()
    assert len(data) == expected['bytes'], name
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
assert authors['status'] == 'unsolved' and authors['turns'] == '5/5'
author_output = subprocess.check_output([sys.executable, str(root / 'verify_certificates.py')])
assert author_output == (root / 'checks.json').read_bytes()
review_output = subprocess.check_output([sys.executable, str(root / 'review/independent_checks.py')])
assert review_output == (root / 'review/independent_checks.txt').read_bytes()
print(json.dumps({'status': 'PASS', 'outcome': 'unsolved', 'turns': '5/5',
                  'manifest_files': len(manifest['files']),
                  'unchanged_author_files': len(authors['files']),
                  'author_output_byte_exact': True,
                  'independent_output_byte_exact': True}, indent=2, sort_keys=True))

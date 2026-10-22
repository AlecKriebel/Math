#!/usr/bin/env python3
"""Verify exact authored snapshot and deterministic mathematical receipts."""
from pathlib import Path
import hashlib
import json
import sys
sys.dont_write_bytecode=True
from cube_verify import run_controls
from verify_algebra import run
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
expected={x['path']:x for x in manifest['files']}
actual={x.name for x in root.iterdir() if x.is_file() and x.name!='AUTHOR_MANIFEST.json'}
assert actual==set(expected),(actual-set(expected),set(expected)-actual)
for name,item in expected.items():
    b=(root/name).read_bytes()
    assert len(b)==item['bytes'],name
    assert hashlib.sha256(b).hexdigest()==item['sha256'],name
assert json.loads(json.dumps(run_controls()))==json.loads((root/'KNOT_CHECKS.json').read_text())
assert run()==json.loads((root/'ALGEBRA_CHECKS.json').read_text())
print(json.dumps(dict(status='PASS',files_verified=len(expected),receipts_replayed=2,
                      universal_problem_solved=False),indent=2))

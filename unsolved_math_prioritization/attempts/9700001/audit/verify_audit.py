#!/usr/bin/env python3
"""Read-only verification of audit files and the supplied frozen author packet."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    raise SystemExit('Usage: python verify_audit.py PATH_TO_FROZEN_PUBLIC_PACKET')
packet = Path(sys.argv[1]).resolve()
expected_manifest = 'b6d9927303b07c183e311b6b1f8a944d16147671b0c6b5f09b686acb9fc5cd62'

def verify_manifest(base, name):
    records = (base/name).read_text().splitlines()
    for line in records:
        digest, filename = line.split('  ',1)
        target = base/filename
        if target.resolve().parent != base.resolve():
            raise AssertionError('Only direct files are allowed in a manifest')
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise AssertionError('Digest mismatch: '+filename)
    return len(records)

number = verify_manifest(root,'MANIFEST.sha256')
if hashlib.sha256((packet/'MANIFEST.sha256').read_bytes()).hexdigest() != expected_manifest:
    raise AssertionError('Wrong author manifest identity')
author_files = verify_manifest(packet,'MANIFEST.sha256')
author = subprocess.check_output([sys.executable,str(packet/'verify.py')],cwd=packet)
if author != (packet/'VERIFICATION.json').read_bytes() or author != (root/'REPRODUCED_VERIFICATION.json').read_bytes():
    raise AssertionError('Author receipt is not byte-identical')
independent = subprocess.check_output([sys.executable,str(root/'independent_checks.py')],cwd=root)
if independent != (root/'INDEPENDENT_CHECKS.json').read_bytes():
    raise AssertionError('Independent receipt is not byte-identical')
result = json.loads((root/'AUDIT_RESULT.json').read_text())
if json.loads(author)['total_assertions'] != result['author_assertions_reproduced']:
    raise AssertionError('Author count disagrees with audit verdict')
if json.loads(independent)['total_assertions'] != result['independent_assertions']:
    raise AssertionError('Independent count disagrees with audit verdict')
print(json.dumps({'status':'PASS','audit_files_checked':number,'author_files_checked':author_files,
                  'author_assertions':json.loads(author)['total_assertions'],
                  'independent_assertions':json.loads(independent)['total_assertions'],
                  'both_receipts':'BYTE_IDENTICAL','frozen_author_manifest':'UNCHANGED'},sort_keys=True))

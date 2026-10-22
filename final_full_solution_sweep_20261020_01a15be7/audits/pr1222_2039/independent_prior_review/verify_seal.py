#!/usr/bin/env python3
"""Read-only verification of the authored review seal and ignored capture seal."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def check_seal(name):
    seal = json.loads((ROOT / name).read_text())
    for entry in seal['files']:
        p = (ROOT / entry['path']).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():
            raise RuntimeError('Missing or out-of-scope path: ' + entry['path'])
        b = p.read_bytes()
        if len(b) != entry['bytes'] or hashlib.sha256(b).hexdigest() != entry['sha256']:
            raise RuntimeError('Seal mismatch: ' + entry['path'])
    return len(seal['files'])

def main():
    authored = check_seal('REVIEW_SEAL.json')
    private = check_seal('PRIVATE_CAPTURE_SEAL.json')
    seal = json.loads((ROOT / 'PRIVATE_CAPTURE_SEAL.json').read_text())
    expected = {x['path'] for x in seal['files']}
    actual = {str(p.relative_to(ROOT)) for p in (ROOT / 'private').rglob('*') if p.is_file()}
    if expected != actual:
        raise RuntimeError('Private capture set changed')
    print(json.dumps({'passed': True, 'authored_files': authored, 'private_captures': private, 'read_only': True}, sort_keys=True))

if __name__ == '__main__':
    main()

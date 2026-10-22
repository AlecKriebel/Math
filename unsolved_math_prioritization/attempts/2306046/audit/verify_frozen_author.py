#!/usr/bin/env python3
"""Authenticate the pinned author tree; this does not verify a general theorem."""
from pathlib import Path
import hashlib
import json
import sys

PIN = '25781fa24baec94cb7087c89e39f7930a97d973a5a4875a57c5a3c6cb8a52411'
NAMES = frozenset(('APPROACH_LOG.md', 'AUTHOR_MANIFEST.json', 'EXPECTED_CHECKS.json',
                   'PROOFS.md', 'README.md', 'SOURCE_VERIFICATION.json',
                   'TARGET_SCOPE.md', 'verify.py', 'verify_integrity.py'))

def verify(root):
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir():
        raise ValueError('author root must be a real directory')
    entries = list(root.iterdir())
    if {p.name for p in entries} != NAMES:
        raise ValueError('author allowlist mismatch')
    if any(p.is_symlink() or not p.is_file() for p in entries):
        raise ValueError('every author entry, including the manifest, must be a regular file')
    manifest_bytes = (root / 'AUTHOR_MANIFEST.json').read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != PIN:
        raise ValueError('author manifest differs from the independently supplied freeze')
    manifest = json.loads(manifest_bytes)
    records = manifest['files']
    if len(records) != 8 or {r['path'] for r in records} != NAMES - {'AUTHOR_MANIFEST.json'}:
        raise ValueError('manifest inventory mismatch')
    verified = []
    for rec in records:
        data = (root / rec['path']).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != rec['bytes'] or digest != rec['sha256']:
            raise ValueError('author bytes changed: ' + rec['path'])
        verified.append(dict(rec))
    verified.append({'path': 'AUTHOR_MANIFEST.json', 'bytes': len(manifest_bytes), 'sha256': PIN})
    return {'all_passed': True, 'target_id': '2306046', 'author_manifest_sha256': PIN,
            'author_files': len(verified), 'total_bytes': sum(r['bytes'] for r in verified),
            'files': sorted(verified, key=lambda r: r['path'])}

if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).parent.parent / 'author'
    print(json.dumps(verify(root), indent=2, sort_keys=True))

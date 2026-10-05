#!/usr/bin/env python3
"""Strict, relocatable file-set and byte verifier; does not audit mathematics."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = 'MANIFEST.json'


def verify(root=ROOT):
    root = Path(root)
    manifest_path = root / MANIFEST
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError('Manifest is not a regular file')
    doc = json.loads(manifest_path.read_text())
    if doc.get('schema') != 1:
        raise ValueError('Unsupported schema')
    expected = doc['files']
    if not isinstance(expected, dict) or not expected:
        raise ValueError('Invalid file map')
    observed = set()
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError('Symlinks are forbidden')
        if path.is_dir():
            raise ValueError('Subdirectories are forbidden')
        if not path.is_file():
            raise ValueError('Non-regular entry')
        relative = path.relative_to(root).as_posix()
        if relative != MANIFEST:
            observed.add(relative)
    if observed != set(expected):
        raise ValueError('Unexpected or missing file')
    for name, metadata in expected.items():
        if name != Path(name).name or name in ('.', '..', MANIFEST):
            raise ValueError('Unsafe manifest path')
        blob = (root / name).read_bytes()
        if len(blob) != metadata['bytes']:
            raise ValueError('Byte-count mismatch: ' + name)
        if hashlib.sha256(blob).hexdigest() != metadata['sha256']:
            raise ValueError('Hash mismatch: ' + name)
    return {'files_verified': len(expected), 'manifest_sha256':
            hashlib.sha256(manifest_path.read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(verify(), sort_keys=True))

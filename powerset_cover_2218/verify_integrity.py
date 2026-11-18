#!/usr/bin/env python3
"""Validate bytes against a manifest, not mathematics or authenticity."""
from pathlib import Path
import hashlib
import json
import re
import sys


def check(root):
    manifest_path = root / 'MANIFEST.json'
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError('Manifest must be a regular nonsymlink file')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if set(manifest) != {'schema_version', 'files'} or manifest['schema_version'] != 1:
        raise ValueError('Invalid manifest schema')
    files = manifest['files']
    if not isinstance(files, list) or not files:
        raise ValueError('Manifest files must be a nonempty list')
    names = set()
    for item in files:
        if not isinstance(item, dict) or set(item) != {'path', 'bytes', 'sha256'}:
            raise ValueError('Invalid file entry')
        name = item['path']
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or name in {'.', '..', 'MANIFEST.json'} or name in names:
            raise ValueError('Unsafe or duplicate file path')
        if type(item['bytes']) is not int or item['bytes'] < 0 or not isinstance(item['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', item['sha256']):
            raise ValueError('Invalid size or SHA-256')
        names.add(name)
    actual = set()
    for path in root.iterdir():
        if path.is_symlink() or not path.is_file():
            raise ValueError('Nonregular package entry: ' + path.name)
        actual.add(path.name)
    if actual != names | {'MANIFEST.json'}:
        raise ValueError('Missing or unexpected package files')
    for item in files:
        data = (root / item['path']).read_bytes()
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('Integrity mismatch: ' + item['path'])
    return len(files)


if __name__ == '__main__':
    try:
        count = check(Path(__file__).resolve().parent)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
    print(f'PASS: {count} files match manifest (integrity only; no proof or authenticity certification)')

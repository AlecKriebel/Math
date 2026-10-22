#!/usr/bin/env python3
"""Check this ordinary file manifest against an independently retained SHA-256."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-sha256', required=True)
    args = parser.parse_args()
    require(re.fullmatch(r'[0-9a-f]{64}', args.expected_sha256) is not None,
            'Expected pin must be a lowercase SHA-256 hex string')
    root = Path(__file__).resolve().parent
    manifest_path = root / 'MANIFEST.json'
    raw = manifest_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == args.expected_sha256,
            'Manifest does not match the externally supplied pin')
    manifest = json.loads(raw)
    require(manifest['schema'] == 'ordinary-sha256-file-manifest-v1', 'Unexpected manifest schema')
    files = manifest['files']
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual == set(files) | {'MANIFEST.json'}, 'Missing or unexpected file')
    for name, record in sorted(files.items()):
        path = root / name
        require(not path.is_symlink(), 'Symlink is outside this manifest format: ' + name)
        require(path.resolve().is_relative_to(root), 'Nonlocal manifest path: ' + name)
        data = path.read_bytes()
        require(len(data) == record['bytes'], 'Byte-count mismatch: ' + name)
        require(hashlib.sha256(data).hexdigest() == record['sha256'], 'SHA-256 mismatch: ' + name)
    print(json.dumps({'status': 'PASS', 'checked_files': len(files),
                      'manifest_sha256': args.expected_sha256}, indent=2))


if __name__ == '__main__':
    main()

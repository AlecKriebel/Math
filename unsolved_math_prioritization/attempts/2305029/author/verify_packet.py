#!/usr/bin/env python3
"""Offline externally pinned integrity verifier; not a mathematical proof checker."""
import argparse
import hashlib
import json
import pathlib
import re
import sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest-sha256', required=True)
    parser.add_argument('--packet-dir', type=pathlib.Path,
                        default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument('--source-dir', type=pathlib.Path)
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{64}', args.expected_manifest_sha256),
            'External manifest pin must be a lowercase SHA-256 value')
    root = args.packet_dir.resolve()
    raw = (root / 'MANIFEST.json').read_bytes()
    require(sha(raw) == args.expected_manifest_sha256, 'External manifest pin mismatch')
    manifest = json.loads(raw)
    require(manifest['schema'] == 1, 'Unsupported manifest schema')
    rows = manifest['files']
    names = [row['name'] for row in rows]
    require(len(names) == len(set(names)), 'Duplicate manifest filenames')
    require(all(re.fullmatch(r'[A-Za-z0-9_.-]+', name) and name not in ('.', '..', 'MANIFEST.json')
                for name in names), 'Unsafe manifest filename')
    require({p.name for p in root.iterdir()} == set(names) | {'MANIFEST.json'},
            'Unexpected or missing packet member')
    for row in rows:
        path = root / row['name']
        require(path.is_file() and not path.is_symlink(), 'Invalid packet file: ' + row['name'])
        data = path.read_bytes()
        require(len(data) == row['bytes'], 'Byte count mismatch: ' + row['name'])
        require(sha(data) == row['sha256'], 'SHA-256 mismatch: ' + row['name'])
    result = {'packet_integrity': 'PASS', 'payload_files': len(rows),
              'manifest_sha256': sha(raw), 'source_identity': 'not_requested',
              'mathematical_proof_check': 'not_performed'}
    if args.source_dir is not None:
        sources = json.loads((root / 'SOURCES.json').read_text())
        for row in sources['pdfs']:
            data = (args.source_dir / row['filename']).read_bytes()
            require(len(data) == row['bytes'], 'Source byte count mismatch: ' + row['filename'])
            require(sha(data) == row['sha256'], 'Source SHA-256 mismatch: ' + row['filename'])
        result['source_identity'] = 'PASS'
        result['source_files'] = len(sources['pdfs'])
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, TypeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)

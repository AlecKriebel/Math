#!/usr/bin/env python3
"""Check the authored artifact manifest, input pins, and optional private sources."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def verify(path, expected, size=None):
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise RuntimeError(f'SHA-256 mismatch: {path.name}')
    if size is not None and len(data) != size:
        raise RuntimeError(f'byte-count mismatch: {path.name}')


def main():
    receipt = json.loads((ROOT / 'ARTIFACT_RECEIPT.json').read_text())
    for row in receipt['authored_files']:
        verify(ROOT / row['path'], row['sha256'], row['bytes'])
    expected_names = {row['path'] for row in receipt['authored_files']}
    expected_names.add('ARTIFACT_RECEIPT.json')
    actual_names = {
        str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
        and not any(part in {'private', 'tmp', '__pycache__'}
                    for part in p.relative_to(ROOT).parts)
    }
    if actual_names != expected_names:
        raise RuntimeError('unlisted or missing authored files: ' +
                           repr(sorted(actual_names ^ expected_names)))
    pins = json.loads((ROOT / 'INPUT_PINS.json').read_text())
    workspace = ROOT.parents[4]
    for row in pins['inputs']:
        verify(workspace / row['path'], row['sha256'], row['bytes'])
    private_count = 0
    for row in json.loads((ROOT / 'SOURCE_PINS.json').read_text())['sources']:
        private = ROOT / row['local_private_path']
        if private.exists():
            verify(private, row['sha256'], row['bytes'])
            private_count += 1
    print(json.dumps({'status': 'passed', 'python_optimization': sys.flags.optimize,
                      'authored_files_checked': len(expected_names) - 1,
                      'inputs_checked': len(pins['inputs']),
                      'private_retrieval_bodies_checked': private_count,
                      'receipt_self_hash': 'intentionally excluded to avoid self-reference'},
                     sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, KeyError, ValueError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error),
                          'python_optimization': sys.flags.optimize}), file=sys.stderr)
        sys.exit(2)

#!/usr/bin/env python3
"""Check package bytes and inventory, not the underlying mathematical theorem."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

EXPECTED = {
    'README.md', 'SOURCE_GATE.md', 'SOURCE_METADATA.json',
    'ACCEPTANCE_AUDIT.md', 'ANALYSIS.md', 'AUDIT_RESULT.json', 'verify_integrity.py',
}


def verify(root):
    actual = {p.name for p in root.iterdir()}
    if actual != EXPECTED | {'MANIFEST.json'}:
        raise ValueError('Unexpected or missing package entries')
    if any(p.is_symlink() or not p.is_file() for p in root.iterdir()):
        raise ValueError('Only regular, non-symlink files are permitted')
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    if manifest.get('schema') != 'sha256-byte-inventory-v1':
        raise ValueError('Unknown manifest schema')
    records = manifest.get('files')
    if not isinstance(records, list) or len(records) != len(EXPECTED):
        raise ValueError('Invalid manifest file count')
    if {r.get('name') for r in records} != EXPECTED:
        raise ValueError('Manifest inventory mismatch')
    for record in records:
        data = (root / record['name']).read_bytes()
        if len(data) != record.get('bytes'):
            raise ValueError('Byte-count mismatch: ' + record['name'])
        if hashlib.sha256(data).hexdigest() != record.get('sha256'):
            raise ValueError('SHA-256 mismatch: ' + record['name'])
    audit = json.loads((root / 'AUDIT_RESULT.json').read_text(encoding='utf-8'))
    if audit.get('acceptance_audit_sha256') != hashlib.sha256(
        (root / 'ACCEPTANCE_AUDIT.md').read_bytes()
    ).hexdigest():
        raise ValueError('Acceptance audit reference mismatch')
    if audit.get('public_analysis_sha256') != hashlib.sha256(
        (root / 'ANALYSIS.md').read_bytes()
    ).hexdigest():
        raise ValueError('Public analysis reference mismatch')


def self_test(root):
    verify(root)
    tests = ['same-size edit', 'truncation', 'missing file', 'extra file',
             'symlink', 'manifest digest edit', 'manifest omission']
    for case in tests:
        with tempfile.TemporaryDirectory(prefix='hypergraph-integrity-') as tmp:
            copy = Path(tmp) / 'package'
            shutil.copytree(root, copy)
            target = copy / 'README.md'
            if case == 'same-size edit':
                data = target.read_bytes()
                target.write_bytes(bytes([data[0] ^ 1]) + data[1:])
            elif case == 'truncation':
                target.write_bytes(target.read_bytes()[:-1])
            elif case == 'missing file':
                target.unlink()
            elif case == 'extra file':
                (copy / 'EXTRA.txt').write_text('not in manifest')
            elif case == 'symlink':
                target.unlink()
                target.symlink_to('SOURCE_GATE.md')
            else:
                path = copy / 'MANIFEST.json'
                manifest = json.loads(path.read_text())
                if case == 'manifest digest edit':
                    manifest['files'][0]['sha256'] = '0' * 64
                else:
                    manifest['files'].pop()
                path.write_text(json.dumps(manifest))
            try:
                verify(copy)
            except (ValueError, OSError, KeyError, TypeError):
                print('PASS: rejected ' + case)
            else:
                raise RuntimeError('Tamper went undetected: ' + case)
    print('PASS: all 7 tamper checks; no mathematical verification claimed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        if args.self_test:
            self_test(root)
        else:
            verify(root)
            print('PASS: file inventory, byte counts, SHA-256 and audit reference')
    except (ValueError, OSError, KeyError, TypeError, RuntimeError) as exc:
        parser.exit(1, 'FAIL: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Verify the source-free audit bundle using an externally supplied pin.

Usage: python verify_audit.py AUDIT_PUBLIC_DIRECTORY EXPECTED_PINS_SHA256
This checks bytes and filenames. It does not rerun or prove the mathematics.
"""
import hashlib
import json
from pathlib import Path
import re
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def verify(folder, expected):
    require(re.fullmatch('[0-9a-f]{64}', expected) is not None, 'invalid external hash')
    require(folder.is_dir() and not folder.is_symlink(), 'invalid bundle directory')
    manifest_path = folder/'AUDIT_PINS.json'
    require(manifest_path.is_file() and not manifest_path.is_symlink(), 'invalid manifest')
    raw = manifest_path.read_bytes()
    require(sha(raw) == expected, 'external audit-manifest pin mismatch')
    manifest = json.loads(raw, object_pairs_hook=no_duplicates)
    require(set(manifest) == {'format', 'files'}, 'manifest keys mismatch')
    require(manifest['format'] == 'kp-4.69-independent-audit-v1', 'manifest format mismatch')
    require(type(manifest['files']) is list and len(manifest['files']) >= 1, 'invalid file list')
    names = set()
    for item in manifest['files']:
        require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'}, 'invalid entry')
        name = item['path']
        require(type(name) is str and re.fullmatch('[A-Za-z0-9_][A-Za-z0-9_.-]*', name),
                'unsafe filename')
        require(name != 'AUDIT_PINS.json' and name not in names, 'duplicate or reserved filename')
        names.add(name)
        require(type(item['bytes']) is int and item['bytes'] >= 0, 'invalid byte count')
        require(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}', item['sha256']),
                'invalid entry hash')
        p = folder/name
        require(p.is_file() and not p.is_symlink(), 'entry is not a regular file')
        data = p.read_bytes()
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'entry pin mismatch')
    require({p.name for p in folder.iterdir()} == names | {'AUDIT_PINS.json'},
            'unexpected or missing bundle entry')
    return {'status': 'PASS', 'files_checked': len(names), 'manifest_sha256': expected}


def main():
    require(len(sys.argv) == 3, 'usage: AUDIT_PUBLIC_DIRECTORY EXPECTED_PINS_SHA256')
    print(json.dumps(verify(Path(sys.argv[1]), sys.argv[2]), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

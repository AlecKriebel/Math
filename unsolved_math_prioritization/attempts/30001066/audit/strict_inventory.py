#!/usr/bin/env python3
"""Fail-closed validation of the reconstructed author ZIP or extracted directory.

Unlike the frozen author validator, this never exempts __pycache__ paths.
The manifest establishes internal consistency; --expected-sha256 optionally
establishes the identity of the ZIP itself. No payload code is executed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import zipfile

EXPECTED = {'README.md', 'proof.md', 'approach_audit.md', 'certificate.json',
            'verify.py', 'test_verifier.py', 'source_audit.json', 'results.json',
            'verify_package.py'}
ALL = EXPECTED | {'MANIFEST.json'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def validate_manifest(payload):
    require(set(payload) == ALL, 'unexpected or missing payload files')
    obj = json.loads(payload['MANIFEST.json'], object_pairs_hook=unique)
    require(type(obj) is dict and set(obj) == {'schema', 'version', 'files'}, 'bad manifest schema')
    require(obj['schema'] == 'isolated-transversal-manifest-v1' and obj['version'] == '1-reconstructed',
            'wrong manifest identity')
    require(type(obj['files']) is list and len(obj['files']) == len(EXPECTED), 'wrong manifest count')
    seen = set()
    for row in obj['files']:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'bad manifest entry')
        name = row['path']
        require(type(name) is str and name in EXPECTED and name not in seen, 'unknown or duplicate path')
        seen.add(name)
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid byte count')
        require(type(row['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}', row['sha256']) is not None,
                'invalid hash')
        require(len(payload[name]) == row['bytes'], 'size mismatch: ' + name)
        require(hashlib.sha256(payload[name]).hexdigest() == row['sha256'], 'hash mismatch: ' + name)
    require(seen == EXPECTED, 'incomplete manifest')
    return {'status': 'PASS', 'payload_files': len(payload), 'cache_exemption': False}


def validate_zip(path, expected_sha256=None):
    data = Path(path).read_bytes()
    if expected_sha256:
        require(hashlib.sha256(data).hexdigest() == expected_sha256, 'archive identity mismatch')
    with zipfile.ZipFile(path) as z:
        info = z.infolist()
        names = [i.filename for i in info]
        require(len(names) == len(ALL) and len(set(names)) == len(names) and set(names) == ALL,
                'duplicate, nested, unlisted, or missing ZIP member')
        require(not z.comment, 'unexpected ZIP archive comment')
        for item in info:
            mode = (item.external_attr >> 16) & 0xFFFF
            require(not item.is_dir() and not stat.S_ISLNK(mode), 'nonregular ZIP member')
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'special ZIP member')
            require(not item.comment and not item.extra, 'unexpected ZIP member metadata')
            require(not item.flag_bits & 1, 'encrypted ZIP member')
            require(item.file_size <= 1_000_000, 'oversized ZIP member')
        require(z.testzip() is None, 'ZIP CRC failure')
        return validate_manifest({name: z.read(name) for name in names})


def validate_directory(path):
    root = Path(path)
    require(root.is_dir() and not root.is_symlink(), 'directory missing or symlink')
    payload = {}
    for p in root.iterdir():
        require(not p.is_symlink() and p.is_file(), 'nonregular or nested directory member')
        payload[p.name] = p.read_bytes()
    return validate_manifest(payload)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--archive', type=Path)
    g.add_argument('--directory', type=Path)
    p.add_argument('--expected-sha256')
    a = p.parse_args()
    if a.archive:
        result = validate_zip(a.archive, a.expected_sha256)
    else:
        require(a.expected_sha256 is None, 'archive digest cannot validate a directory')
        result = validate_directory(a.directory)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile, KeyError, TypeError) as exc:
        raise SystemExit('FAIL: ' + str(exc))

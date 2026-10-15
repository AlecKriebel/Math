#!/usr/bin/env python3
"""Root-only administrative alias build; source preparation is not execution."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
V1 = AUDIT / 'reviewed_candidate'
V2 = AUDIT / 'reviewed_candidate_v2'
V1_SHA = '054b156eb6d44903eadeffeda2012a23c68db530b514294830cc0f45c7b93912'
SELF = 'ALIAS_PREPARATION_MANIFEST.json'


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def names(root):
    files, directories = set(), set()
    require(root.is_dir() and not root.is_symlink(), 'Regular source/destination root required')
    require(all(not p.is_symlink() for p in root.parents), 'Symlink ancestor prohibited')
    for p in root.rglob('*'):
        n = p.relative_to(root).as_posix()
        require(not p.is_symlink(), 'Symlink prohibited: ' + n)
        require(p.is_file() or p.is_dir(), 'Special file prohibited: ' + n)
        (files if p.is_file() else directories).add(n)
    return files, directories


def closure(root, rows, self_name):
    expected, directories = {}, set()
    for row in rows:
        require(set(row) == {'path', 'bytes', 'sha256'}, 'Exact pin schema required')
        n = row['path']; p = PurePosixPath(n)
        require(n and '\\' not in n and not p.is_absolute() and '..' not in p.parts and p.as_posix() == n, 'Unsafe path')
        require(n != self_name and n not in expected, 'Duplicate/self member')
        require(type(row['bytes']) is int and row['bytes'] >= 0 and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'Invalid byte/hash pin')
        expected[n] = row
        directories.update(x.as_posix() for x in p.parents if x.as_posix() != '.')
    actual, actual_dirs = names(root)
    require(actual == set(expected) | {self_name} and actual_dirs == directories, 'Exact recursive file/directory closure required')
    for n, row in expected.items():
        raw = (root / n).read_bytes()
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Member changed: ' + n)


def preparation(pin):
    raw = (HERE / SELF).read_bytes()
    require(re.fullmatch('[0-9a-f]{64}', pin) and digest(raw) == pin, 'Exact root-reviewed preparation SHA required')
    manifest = json.loads(raw)
    require(manifest['self_excluded'] == [SELF], 'Exact preparation self exclusion required')
    closure(HERE, manifest['files'], SELF)


def frozen_v1():
    raw = (V1 / 'MANIFEST.json').read_bytes()
    require(digest(raw) == V1_SHA, 'Frozen v1 manifest changed')
    manifest = json.loads(raw)
    require(manifest['self_excluded'] == ['MANIFEST.json'] and manifest['files_count'] == len(manifest['files']) == 1499, 'Exact original1499 closure required')
    closure(V1, manifest['files'], 'MANIFEST.json')
    require(not (V1 / 'review/REVIEW.md').exists(), 'This revision only restores the recorded missing alias')
    return raw, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--preparation-manifest-sha256', required=True)
    args = parser.parse_args()
    require(args.execute and not sys.flags.optimize, 'Root explicit execution with active guards required')
    require(sys.platform == 'darwin', 'Exclusive publication requires this macOS host')
    require(HERE.name == 'alias_source_revision' and HERE.parent.name == 'acceptance_preparation_family' and AUDIT.name == 'pr38_2765', 'Keep the reviewed source at its audit anchor')
    preparation(args.preparation_manifest_sha256)
    v1_raw, v1 = frozen_v1()
    require(not V2.exists() and not V2.is_symlink(), 'Never overwrite or reuse a v2 destination')
    raw_manifest = (HERE / 'EXPECTED_V2_MANIFEST.json').read_bytes()
    expected = json.loads(raw_manifest)
    receipt_raw = (HERE / 'EXPECTED_V2_ALIAS_RECEIPT.json').read_bytes()
    receipt = json.loads(receipt_raw)
    notice = (HERE / 'ARCHIVAL_NOTICE_APPEND.txt').read_bytes()
    require(expected['self_excluded'] == ['MANIFEST.json'] and expected['files_count'] == len(expected['files']) == 1502, 'Exact prospective v2 closure required')
    require(receipt['source_v1_manifest_sha256'] == V1_SHA and receipt['builder_sha256'] == digest(Path(__file__).read_bytes()), 'Exact derivation source required')
    require(receipt['actual_execution_attested'] is False, 'Deterministic metadata never substitutes for root actual capture')
    payload = {row['path']: (V1 / row['path']).read_bytes() for row in v1['files']}
    for n in ['README.md', 'CURRENT_CONTEXT.md']:
        payload[n] += notice
    payload['review/REVIEW.md'] = payload['original_archive/review/REVIEW.md']
    payload['V1_MANIFEST.json'] = v1_raw
    payload['V2_ALIAS_RECEIPT.json'] = receipt_raw
    actual_rows = [{'path': n, 'bytes': len(raw), 'sha256': digest(raw)} for n, raw in sorted(payload.items())]
    require(actual_rows == expected['files'], 'All and only explicit byte deltas must equal the root-reviewed prospective closure')
    require('see review/REVIEW.md.' in payload['RESULTS.md'].decode(), 'Original unchanged RESULTS link required')
    (AUDIT / 'tmp').mkdir(exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='pr38_review_alias_v2_', dir=AUDIT / 'tmp'))
    for n, raw in payload.items():
        target = stage / n
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(raw)
    (stage / 'MANIFEST.json').write_bytes(raw_manifest)
    closure(stage, expected['files'], 'MANIFEST.json')
    preparation(args.preparation_manifest_sha256)
    frozen_v1()
    # macOS RENAME_EXCL refuses a raced-in destination without replacement.
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(os.fsencode(stage), os.fsencode(V2), 0x00000004) != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), str(V2))
    closure(V2, expected['files'], 'MANIFEST.json')
    frozen_v1()
    print(json.dumps({'status': 'ACTUAL_ADMINISTRATIVE_V2_ALIAS_BUILD_COMPLETE', 'candidate': str(V2), 'files_count': 1502, 'manifest_bytes': len(raw_manifest), 'manifest_sha256': digest(raw_manifest), 'v1_manifest_sha256_unchanged': V1_SHA, 'alias_sha256': digest(payload['review/REVIEW.md']), 'actual_capture_by_root_required': True, 'new_substantive_attempts': 0, 'audit_turns': 0}))


if __name__ == '__main__':
    main()

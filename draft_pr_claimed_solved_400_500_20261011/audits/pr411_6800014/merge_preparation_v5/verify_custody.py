#!/usr/bin/env python3
"""Offline positive-file custody; obtain the expected seal hash independently."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-seal-sha256', required=True)
    args = parser.parse_args()
    require(re.fullmatch(r'[0-9a-f]{64}', args.expected_seal_sha256) is not None, 'explicit external seal SHA256 required')
    root = Path(__file__).resolve().parent
    seal_raw = (root / 'FINAL_SEAL.json').read_bytes()
    require(sha(seal_raw) == args.expected_seal_sha256, 'external seal hash differs')
    seal = json.loads(seal_raw)
    require(seal['format'] == 'pr411-administration-final-seal-v1', 'seal format differs')
    whitelist_raw = (root / 'PUBLICATION_WHITELIST.json').read_bytes()
    require(sha(whitelist_raw) == seal['whitelist_sha256'], 'whitelist hash differs')
    whitelist = json.loads(whitelist_raw)
    require(whitelist['format'] == 'pr411-administration-positive-whitelist-v1', 'whitelist format differs')
    paths = set()
    for item in whitelist['entries']:
        require(set(item) == {'path', 'bytes', 'sha256', 'mode'}, 'entry schema differs')
        path = item['path']
        require(isinstance(path, str) and path and '\\' not in path and '\0' not in path and not path.startswith('/')
                and all(part not in ('', '.', '..') for part in path.split('/'))
                and str(PurePosixPath(path)) == path and path not in paths, 'unsafe/duplicate path')
        paths.add(path)
        target = root
        for part in path.split('/'):
            target = target / part
            require(not target.is_symlink(), 'symlink in positive path')
        require(stat.S_ISREG(target.stat().st_mode) and item['mode'] == '100644' and stat.S_IMODE(target.stat().st_mode) == 0o644,
                'positive regular-file mode differs')
        data = target.read_bytes()
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'positive bytes/hash differ: ' + path)
    require(len(paths) == seal['positive_file_count'], 'positive count differs')
    actual = set()
    expected_directories = {str(parent) for path in paths for parent in PurePosixPath(path).parents if str(parent) != '.'}
    for target in root.rglob('*'):
        relative = target.relative_to(root).as_posix()
        kind = target.lstat().st_mode
        if stat.S_ISREG(kind):
            actual.add(relative)
        elif stat.S_ISDIR(kind):
            require(relative in expected_directories, 'unlisted directory in bundle')
        else:
            raise ValueError('symlink or special file in bundle')
    require(actual == paths | {'PUBLICATION_WHITELIST.json', 'FINAL_SEAL.json'}, 'full file set differs')
    require(len(actual) == seal['full_file_count'], 'full count differs')
    print(json.dumps({'result': 'PASS_OFFLINE_CUSTODY', 'positive_file_count': len(paths), 'full_file_count': len(actual),
                      'actual_external_seal_sha256': args.expected_seal_sha256, 'native_success_certified': False}))


if __name__ == '__main__':
    main()

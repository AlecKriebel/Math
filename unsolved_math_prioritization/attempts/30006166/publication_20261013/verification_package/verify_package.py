#!/usr/bin/env python3
"""Check closed package bytes and optionally replay finite evidence, not the theorem."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def unique(pairs):
    answer = {}
    for key, value in pairs:
        require(key not in answer, 'duplicate JSON key')
        answer[key] = value
    return answer


def load(path):
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def bind(root, trusted):
    manifest = root / 'package_index.json'
    require(stat.S_ISREG(manifest.lstat().st_mode), 'regular manifest')
    require(hashlib.sha256(manifest.read_bytes()).hexdigest() == trusted, 'external index pin')
    data = load(manifest)
    require(data['schema'] == 1 and data['problem_id'] == 30006166, 'package identity')
    rows = data['files']
    names = [row['path'] for row in rows]
    require(len(names) == len(set(names)), 'unique inventory')
    require(all(type(n) is str and n == str(PurePosixPath(n)) and n not in ('', '.', 'package_index.json')
                and not n.startswith('/') and '..' not in PurePosixPath(n).parts and '\\' not in n
                for n in names), 'safe paths')
    expected_dirs = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    actual_files, actual_dirs = set(), set()
    for path in root.rglob('*'):
        mode = path.lstat().st_mode
        name = path.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            actual_files.add(name)
        elif stat.S_ISDIR(mode):
            actual_dirs.add(name)
        else:
            raise RuntimeError('nonregular package member: ' + name)
    require(actual_files == set(names) | {'package_index.json'}, 'closed file inventory')
    require(actual_dirs == expected_dirs, 'closed directory inventory')
    for row in rows:
        content = (root / row['path']).read_bytes()
        require(type(row['bytes']) is int and len(content) == row['bytes'], 'byte count: ' + row['path'])
        require(hashlib.sha256(content).hexdigest() == row['sha256'], 'digest: ' + row['path'])
    return len(actual_files)


def full(root):
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    def run(path, *args):
        result = subprocess.run([sys.executable, *flags, str(root / path), *args],
                                cwd='/', capture_output=True, text=True, timeout=900)
        require(result.returncode == 0, path + ': ' + result.stderr)
        return json.loads(result.stdout)
    original = run('source/verify_publication.py',
                   '7fbaa213b0ed95bf6d653adb5acbfe7ac40f92d0399d57561202505565112d03', '--full')
    require(original['files'] == 61 and original['archive_members_verified'] == 51, 'historical bindings')
    require(original['full']['finite_diagnostics_certify_infinite_theorem'] is False, 'historical scope')
    slab = run('audits/slab/boundary_diagnostics.py')
    require(slab == load(root / 'audits/slab/BOUNDARY_DIAGNOSTICS.json'), 'fresh slab replay')
    require(slab['infinite_theorem_verified'] is False, 'fresh slab scope')
    return {'historical_package': original, 'fresh_slab': slab,
            'infinite_theorem_verified_by_program': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trusted_index_sha256')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    result = {'status': 'PASS', 'regular_files': bind(root, args.trusted_index_sha256),
              'infinite_theorem_verified_by_program': False}
    if args.full:
        result['full'] = full(root)
        bind(root, args.trusted_index_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

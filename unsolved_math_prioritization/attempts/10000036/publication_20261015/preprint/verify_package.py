#!/usr/bin/env python3
"""Portable closed-inventory checks; these do not certify analysis or priority."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def decode(raw):
    def nonfinite(value):
        raise RuntimeError('nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)


def regular_read(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'regular file required: ' + str(path))
    return path.read_bytes()


def load(path):
    return decode(regular_read(path))


def bind(root, pin):
    require(stat.S_ISDIR(root.lstat().st_mode), 'regular root directory')
    require(len(pin) == 64 and all(c in '0123456789abcdef' for c in pin), 'external SHA-256 syntax')
    manifest = root / 'package_index.json'
    raw_index = regular_read(manifest)
    require(hashlib.sha256(raw_index).hexdigest() == pin, 'external index pin')
    data = decode(raw_index)
    require(data['schema'] == 'finite-energy-threshold-one-preprint-v1'
            and data['problem_id'] == 10000036
            and data['original_head'] == 'ed2de7249953ba0c1afad253adca9b820d7297c5', 'package identity')
    names = [row['path'] for row in data['files']]
    require(all(type(n) is str and n == str(PurePosixPath(n)) and n not in ('', '.', 'package_index.json')
                and not n.startswith('/') and '..' not in PurePosixPath(n).parts
                and '\\' not in n and ':' not in n for n in names), 'safe paths')
    require(len(names) == len(set(names)), 'unique inventory')
    expected_dirs = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    files, dirs = set(), set()
    for path in root.rglob('*'):
        mode = path.lstat().st_mode
        name = path.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            files.add(name)
        elif stat.S_ISDIR(mode):
            dirs.add(name)
        else:
            raise RuntimeError('nonregular member: ' + name)
    require(files == set(names) | {'package_index.json'} and dirs == expected_dirs, 'closed inventory')
    for row in data['files']:
        raw = regular_read(root / row['path'])
        require(type(row['bytes']) is int and row['bytes'] >= 0 and len(raw) == row['bytes'],
                'byte count: ' + row['path'])
        require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'digest: ' + row['path'])
    return len(files)


def full(root):
    flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='finite energy replay with spaces ') as td:
        scratch = Path(td).resolve()
        shutil.copytree(root / 'source', scratch / 'source')
        shutil.copyfile(root / 'root_evidence/SOURCE_MANIFEST.json', scratch / 'SOURCE_MANIFEST.json')
        checker = scratch / 'check_original_data_package.py'
        shutil.copyfile(root / 'root_evidence/check_original_data_package.py', checker)
        run = subprocess.run([sys.executable, *flags, str(checker)], cwd='/',
                             capture_output=True, text=True, timeout=90)
        require(run.returncode == 0 and not run.stderr, 'original integrity replay: ' + run.stderr)
        actual = decode(run.stdout)
        expected_name = 'ROOT_ORIGINAL_DATA_INTEGRITY_O.json' if sys.flags.optimize else 'ROOT_ORIGINAL_DATA_INTEGRITY.json'
        expected = load(root / 'root_evidence' / expected_name)
        strip = lambda r: {k:v for k,v in r.items() if k != 'timestamp_utc'}
        require(strip(actual) == strip(expected), 'original integrity replay result drift')
        require(actual['status'] == 'PASS' and actual['source_file_count'] == 27
                and actual['archive_member_total'] == 15
                and actual['negative_parser_path_controls_rejected'] == 11
                and actual['optimization_level'] == sys.flags.optimize, 'original integrity coverage')
    return {'original_data_integrity': actual, 'mathematical_program_executed': False,
            'scope': 'Analytical proofs and primary-source reading require independent inspection. '
                     'This replay authenticates the recorded source and archive relationships only.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trusted_index_sha256')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,
            'run with python -I -S -B')
    root = Path(__file__).absolute().parent
    result = {'status': 'PASS', 'regular_files': bind(root, args.trusted_index_sha256),
              'unlimited_mathematical_proof_certified_by_program': False,
              'priority_certified_by_program': False}
    if args.full:
        result['full'] = full(root)
        bind(root, args.trusted_index_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

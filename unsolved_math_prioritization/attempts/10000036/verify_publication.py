#!/usr/bin/env python3
"""Bind the reviewed PR tree and its portable analytical-evidence package."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def regular_read(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'regular file required: ' + str(path))
    return path.read_bytes()


def load(path):
    def nonfinite(value):
        raise RuntimeError('nonfinite JSON constant: ' + value)
    return json.loads(regular_read(path), object_pairs_hook=unique, parse_constant=nonfinite)


def bind(root, pin):
    require(stat.S_ISDIR(root.lstat().st_mode), 'regular root directory')
    raw = regular_read(root / 'PUBLICATION_MANIFEST.json')
    require(hashlib.sha256(raw).hexdigest() == pin, 'external outer pin')
    data = load(root / 'PUBLICATION_MANIFEST.json')
    require(data['schema'] == 'finite-energy-current-publication-v1'
            and data['problem_id'] == 10000036, 'package identity')
    names = [row['path'] for row in data['files']]
    require(all(type(n) is str and n == str(PurePosixPath(n))
                and n not in ('', '.', 'PUBLICATION_MANIFEST.json') and not n.startswith('/')
                and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n
                for n in names), 'safe paths')
    require(len(names) == len(set(names)), 'unique inventory')
    expected_dirs = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    files, dirs = set(), set()
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            files.add(name)
        elif stat.S_ISDIR(mode):
            dirs.add(name)
        else:
            raise RuntimeError('nonregular member: ' + name)
    require(files == set(names) | {'PUBLICATION_MANIFEST.json'} and dirs == expected_dirs, 'closed inventory')
    for row in data['files']:
        content = regular_read(root / row['path'])
        require(type(row['bytes']) is int and len(content) == row['bytes'], 'byte count: ' + row['path'])
        require(hashlib.sha256(content).hexdigest() == row['sha256'], 'digest: ' + row['path'])
    return len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trusted_outer_sha256')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,
            'run with python -I -S -B')
    root = Path(__file__).absolute().parent
    count = bind(root, args.trusted_outer_sha256)
    pre = root / 'publication_20261015/preprint'
    inner = root / 'publication_20261015/verification_package'
    deposit = load(pre / 'zenodo-deposit.json')
    require(load(pre / 'metadata.json') == deposit['metadata'] == load(inner / 'metadata.json')
            == load(root / 'CURRENT_PUBLICATION.json')['zenodo_metadata'], 'exact current metadata')
    require(deposit['files'] == [
        {'path': 'output/pdf/note.pdf', 'name': 'finite-energy-percolation-note.pdf'},
        {'path': 'verification.zip', 'name': 'finite-energy-percolation-verification.zip'}], 'exact upload file set')
    require(regular_read(pre / 'output/pdf/note.pdf') == regular_read(inner / 'note.pdf'), 'PDF identity')
    for name in ['README.md', 'note.tex', 'CURRENT_PRIORITY.md', 'verify_package.py',
                 'build_verification.py', 'package_index.json']:
        require(regular_read(pre / name) == regular_read(inner / name), 'portable identity: ' + name)
    inner_files = {p.relative_to(inner).as_posix(): p for p in inner.rglob('*') if p.is_file()}
    require(len(inner_files) == 108, 'portable member count')
    with zipfile.ZipFile(pre / 'verification.zip') as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and set(names) == set(inner_files), 'archive closed inventory')
        for entry in archive.infolist():
            require(stat.S_ISREG(entry.external_attr >> 16) and not (entry.external_attr >> 16) & 0o111
                    and not entry.flag_bits & 1, 'archive regular unencrypted data member')
            require(archive.read(entry) == regular_read(inner_files[entry.filename]), 'archive member identity')
    original = load(inner / 'root_evidence/SOURCE_MANIFEST.json')
    require(original['frozen_head'] == 'ed2de7249953ba0c1afad253adca9b820d7297c5'
            and original['problem_id'] == 10000036 and len(original['files']) == 27, 'original identity')
    mutable = {'README.md', 'RESEARCH_LOG.md', 'PUBLICATION_MANIFEST.json'}
    for row in original['files']:
        content = regular_read(inner / 'source' / row['path'])
        require(len(content) == row['bytes'] and hashlib.sha256(content).hexdigest() == row['sha256'],
                'frozen original source digest')
        if row['path'] not in mutable:
            require(regular_read(root / row['path']) == content, 'historical current copy changed')
    index_pin = hashlib.sha256(regular_read(inner / 'package_index.json')).hexdigest()
    flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    command = [sys.executable, *flags, str(inner / 'verify_package.py'), index_pin]
    if args.full:
        command.append('--full')
    run = subprocess.run(command, cwd='/', capture_output=True, text=True, timeout=120)
    require(run.returncode == 0 and not run.stderr, 'portable verification: ' + run.stderr)
    checked = json.loads(run.stdout, object_pairs_hook=unique)
    require(checked['status'] == 'PASS' and checked['regular_files'] == 108, 'portable result')
    bind(root, args.trusted_outer_sha256)
    print(json.dumps({'status': 'PASS', 'regular_files': count, 'archive_members_verified': 108,
                      'original_files_preserved': 27, 'historical_current_files_unchanged': 24,
                      'inner': checked, 'unlimited_mathematical_proof_certified_by_program': False,
                      'priority_certified_by_program': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

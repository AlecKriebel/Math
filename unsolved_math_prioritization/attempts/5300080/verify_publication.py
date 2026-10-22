#!/usr/bin/env python3
"""Authenticate the complete publication before executing its frozen checks."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile

ARCHIVES = {
    'author': ('henon_boundary_5300080_author.zip', 'henon_boundary_5300080', 19789,
               '6f7d74f0cd6157fb207d846f7404d22de2b16d09b7e16fdf6f1c2a1a4faed0f6'),
    'independent_audit': ('henon_boundary_5300080_independent_audit.zip',
                         'henon_boundary_5300080_independent_audit', 19387,
                         '5802ca28634da197afd55f45d863c598d5a8e47188cfda1c4de65fd3512587cf')}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def safe_path(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and name and not p.is_absolute()
            and str(p) == name and all(x not in ('', '.', '..') for x in p.parts)
            and '\\' not in name, 'unsafe path')
    return p


def authenticate(root, expected_manifest):
    require(root.is_dir() and not root.is_symlink(), 'publication directory')
    manifest_path = root / 'PUBLICATION_MANIFEST.json'
    require(not manifest_path.is_symlink(), 'manifest symlink')
    require(identity(manifest_path)['sha256'] == expected_manifest, 'external manifest pin mismatch')
    manifest = read_json(manifest_path)
    require(set(manifest) == {'schema', 'algorithm', 'files'}
            and type(manifest['schema']) is int and manifest['schema'] == 1
            and manifest['algorithm'] == 'sha256', 'manifest schema')
    wanted_files = {'PUBLICATION_MANIFEST.json'}
    wanted_dirs = set()
    for e in manifest['files']:
        require(set(e) == {'path', 'bytes', 'sha256'}, 'manifest entry schema')
        p = safe_path(e['path'])
        require(str(p) not in wanted_files, 'duplicate manifest path')
        wanted_files.add(str(p))
        wanted_dirs.update(str(x) for x in p.parents if str(x) != '.')
        path = root / p
        require(path.is_file() and not path.is_symlink(), 'missing payload or symlink')
        require(type(e['bytes']) is int and identity(path) == {k:e[k] for k in ('bytes', 'sha256')},
                'payload identity mismatch: ' + str(p))
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'recursive symlink')
        rel = p.relative_to(root).as_posix()
        if p.is_dir():
            actual_dirs.add(rel)
        else:
            require(p.is_file(), 'nonregular file')
            actual_files.add(rel)
    require(actual_files == wanted_files and actual_dirs == wanted_dirs, 'recursive inventory mismatch')
    for directory, (name, prefix, size, digest) in ARCHIVES.items():
        path = root / 'archives' / name
        require(identity(path) == {'bytes': size, 'sha256': digest}, 'frozen ZIP identity')
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            expected = {prefix + '/' + p.name for p in (root/directory).iterdir()}
            require(len(names) == len(set(names)) and set(names) == expected, 'ZIP inventory')
            for entry in archive.infolist():
                safe_path(entry.filename)
                require(not entry.is_dir() and not stat.S_ISLNK(entry.external_attr >> 16), 'ZIP member type')
                require(archive.read(entry) == (root/directory/PurePosixPath(entry.filename).name).read_bytes(),
                        'ZIP to expanded payload mismatch')
    status = read_json(root/'PUBLICATION_STATUS.json')
    expected_status = {'problem_id': 5300080, 'rank': 793, 'disposition': 'unsolved',
                       'substantive_approaches_used': 5, 'substantive_approach_limit': 5,
                       'original_solution_credit': 0, 'full_target_resolved': False,
                       'required_mathematical_corrections': 0, 'human_peer_review': False,
                       'formal_proof_certificate': False, 'novelty_claim': False}
    for key, value in expected_status.items():
        require(status.get(key) == value and type(status.get(key)) is type(value), 'publication scope')
    return len(wanted_files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest-sha256', required=True)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    count = authenticate(root, args.expected_manifest_sha256)
    if args.integrity_only:
        print(json.dumps({'status': 'PASS_INTEGRITY_ONLY', 'publication_files': count}, sort_keys=True))
        return
    run = subprocess.run([sys.executable, '-B', str(root/'independent_audit/verify_audit.py'),
                          str(root/'archives/henon_boundary_5300080_author.zip')],
                         capture_output=True, text=True, check=True)
    actual = json.loads(run.stdout, object_pairs_hook=pairs)
    expected = read_json(root/'independent_audit/RESULTS.json')
    expected['provenance_checks'] = {}
    require(actual == expected, 'portable audit replay differs from frozen results')
    print(json.dumps({'status': 'PASS_PORTABLE_PUBLICATION', 'problem_id': 5300080,
                      'disposition': 'unsolved', 'substantive_approaches_used': 5,
                      'original_solution_credit': 0, 'publication_files': count,
                      'author_assertions_per_replay': 14006, 'author_replay_modes': 3,
                      'independent_assertions': 42428, 'author_package_negative_controls': 14,
                      'provenance_checks': 'NOT_RUN_MISSING_OPTIONAL_SOURCE_INPUTS',
                      'analytic_theorems_certified': False, 'human_peer_review': False},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
        raise SystemExit('FAIL: ' + str(exc))

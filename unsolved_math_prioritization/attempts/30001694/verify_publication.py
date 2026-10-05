#!/usr/bin/env python3
"""Offline, relocatable release integrity and independent strict certificate replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PINS = {
    'archives/polyomino_30001694_FROZEN_PUBLIC_PACKET.zip': (61552, '20635fa3e641d5df4ae3ad88bc439a9aed34d31d6eac8dcbcf563087c7f8e1fc'),
    'archives/polyomino_30001694_INDEPENDENT_AUDIT.zip': (69582, 'd24e78892f243dcd30f4945f3bf01cdd89aed52670bbfd45a4f5763b30a42c28'),
    'author/MANIFEST.json': (2456, 'c1d46c560578dc3d19129f2a65d4fd910edd32739e62260de4cea1cf5b29417e'),
    'audit/MANIFEST.json': (2686, '3b13269b0cbe14c1464b88f44309d30a5911a7e75175ef0d586dba783c4c754a'),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def parse(data):
    return json.loads(data, object_pairs_hook=unique_object)


def integrity():
    manifest_bytes = (ROOT / 'PUBLICATION_MANIFEST.json').read_bytes()
    manifest = parse(manifest_bytes)
    require((manifest['target_id'], manifest['outcome'], manifest['turns']) == ('30001694', 'unsolved', '5/5'), 'Incorrect release status')
    require(manifest['controlling_validator'] == 'audit/strict_release_validator.py', 'Incorrect controlling validator')
    rows = manifest['files']
    require(len(rows) == len({r['path'] for r in rows}), 'Duplicate publication path')
    records = {r['path']: r for r in rows}
    for name in records:
        path = PurePosixPath(name)
        require(str(path) == name and not path.is_absolute() and '..' not in path.parts, 'Unsafe/noncanonical path')
    actual_files, actual_dirs = set(), set()
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink is not a release artifact')
        name = path.relative_to(ROOT).as_posix()
        if path.is_file():
            actual_files.add(name)
        elif path.is_dir():
            actual_dirs.add(name)
        else:
            raise ValueError('Special file is not a release artifact')
    require(actual_files == set(records) | {'PUBLICATION_MANIFEST.json'}, 'Exact publication allowlist differs')
    expected_dirs = {str(parent) for name in records for parent in PurePosixPath(name).parents if str(parent) != '.'}
    require(actual_dirs == expected_dirs, 'Exact publication directory set differs')
    data = {}
    for name, row in records.items():
        raw = (ROOT / name).read_bytes()
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Publication bytes differ: ' + name)
        data[name] = raw
    for name, (size, sha) in PINS.items():
        require(len(data[name]) == size and digest(data[name]) == sha, 'Frozen anchor differs: ' + name)
    archive_members = 0
    fixed_paths = {'README.md', 'verify_publication.py'} | {name for name in PINS if name.startswith('archives/')}
    for folder, archive in [('author', 'polyomino_30001694_FROZEN_PUBLIC_PACKET.zip'), ('audit', 'polyomino_30001694_INDEPENDENT_AUDIT.zip')]:
        directory = {name[len(folder) + 1:]: raw for name, raw in data.items() if name.startswith(folder + '/')}
        frozen = parse(directory['MANIFEST.json'])
        require(set(frozen['files']) | {'MANIFEST.json'} == set(directory), 'Frozen directory inventory differs: ' + folder)
        fixed_paths.update(folder + '/' + name for name in directory)
        for name, row in frozen['files'].items():
            require(len(directory[name]) == row['bytes'] and digest(directory[name]) == row['sha256'], 'Frozen payload differs: ' + name)
        with zipfile.ZipFile(ROOT / 'archives' / archive) as z:
            names = z.namelist()
            require(len(names) == len(set(names)), 'Duplicate ZIP member')
            require(set(names) == set(directory), 'ZIP member allowlist differs')
            for name in names:
                require(z.read(name) == directory[name], 'Extracted and archived bytes differ: ' + name)
                archive_members += 1
    require(set(records) == fixed_paths, 'Release paths differ from the frozen package and fixed entrypoints')
    return data, {'publication_files_verified': len(records), 'publication_manifest_self_excluded': True, 'publication_manifest_sha256': digest(manifest_bytes), 'archive_members_verified': archive_members}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--integrity-only', action='store_true', help='Skip finite mathematical replay; useful for integrity negative controls')
    args = parser.parse_args()
    before, result = integrity()
    result.update({'passed': True, 'target_id': '30001694', 'outcome': 'unsolved', 'turns': '5/5', 'universal_target_solved': False, 'novelty_claim': False, 'historical_defects': ['F1', 'F2']})
    if not args.integrity_only:
        runs = {}
        for optimized in (False, True):
            command = [sys.executable] + (['-O'] if optimized else []) + ['-B', str(ROOT / 'audit/strict_release_validator.py'), str(ROOT / 'archives/polyomino_30001694_FROZEN_PUBLIC_PACKET.zip'), '--controls']
            raw = subprocess.check_output(command, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            checked = parse(raw)
            require(raw == before['audit/STRICT_VALIDATION_RESULTS.json'], 'Strict replay differs from frozen result')
            require(checked['passed'] and not checked['author_verifiers_used'], 'Strict validation did not pass independently')
            require(checked['certificate']['row_count'] == 9349, 'Incorrect certificate count')
            require(len(checked['negative_controls']) == 17 and all(x['rejected'] for x in checked['negative_controls'].values()), 'Negative controls failed')
            runs['optimized' if optimized else 'normal'] = {'passed': True, 'byte_equal_to_frozen_result': True, 'certificate_rows': 9349, 'negative_controls_rejected': 17}
        result['strict_validation'] = runs
    else:
        result['finite_mathematical_replay'] = 'not run (--integrity-only)'
    after, _ = integrity()
    require(before == after, 'Retained bytes changed during verification')
    result['retained_bytes_unchanged'] = True
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

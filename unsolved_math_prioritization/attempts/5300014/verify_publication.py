#!/usr/bin/env python3
"""Externally pinned, relocation-safe publication byte and replay verifier."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_zip(path, extracted):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'duplicate ZIP member')
        expected = {p.relative_to(extracted).as_posix() for p in extracted.rglob('*') if p.is_file()}
        require(set(names) == expected, 'ZIP inventory differs from extracted payload')
        for name in names:
            pp = PurePosixPath(name)
            require(name == str(pp) and not pp.is_absolute() and '..' not in pp.parts and '\\' not in name, 'unsafe ZIP path')
            require(archive.read(name) == (extracted / name).read_bytes(), 'ZIP bytes differ: ' + name)
    return len(names)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest_path = root / 'PUBLICATION_MANIFEST.json'
    require(manifest_path.is_file() and not manifest_path.is_symlink(), 'manifest must be a regular file')
    raw = manifest_path.read_bytes()
    require(sha256(raw) == args.expected_manifest, 'external publication manifest pin mismatch')
    manifest = json.loads(raw)
    require(set(manifest) == {'format', 'files'} and manifest['format'] == 'sha256-tree-v1', 'manifest schema')
    files = manifest['files']
    dirs = set()
    for name in files:
        pp = PurePosixPath(name)
        require(name == str(pp) and not pp.is_absolute() and '..' not in pp.parts and '\\' not in name and name != manifest_path.name, 'unsafe manifest path')
        dirs.update(str(parent) for parent in pp.parents if str(parent) != '.')
    actual_files, actual_dirs = set(), set()
    for item in root.rglob('*'):
        require(not item.is_symlink(), 'symlink prohibited')
        relative = item.relative_to(root).as_posix()
        if item.is_dir():
            actual_dirs.add(relative)
        else:
            require(item.is_file(), 'nonregular payload')
            actual_files.add(relative)
    require(actual_files == set(files) | {manifest_path.name}, 'file allowlist mismatch')
    require(actual_dirs == dirs, 'directory allowlist mismatch')
    for name, spec in files.items():
        b = (root / name).read_bytes()
        require(set(spec) == {'bytes', 'sha256'} and len(b) == spec['bytes'] and sha256(b) == spec['sha256'], 'payload mismatch: ' + name)
    status = json.loads((root / 'PUBLICATION_STATUS.json').read_bytes())
    require(status['problem_id'] == 5300014 and status['target_status'] == 'UNSOLVED', 'wrong target or status')
    require(status['approach_families_used'] == status['approach_family_limit'] == 5, 'approach budget mismatch')
    require(status['actual_nonmonomial_degree_gt_two_boundary_witness'] is False, 'unsupported boundary witness')
    audit = root / 'independent_audit'
    for name, spec in status['archives'].items():
        b = (root / 'archives' / name).read_bytes()
        require(len(b) == spec['bytes'] and sha256(b) == spec['sha256'], 'original archive mismatch')
    audit_count = verify_zip(root / 'archives/BLASCHKE_COMPACTIFICATIONS_5300014_INDEPENDENT_AUDIT_SAFE.zip', audit)
    author_count = verify_zip(root / 'archives/BLASCHKE_COMPACTIFICATIONS_5300014_AUTHOR_SAFE_FREEZE.zip', audit / 'author')
    require((root / 'archives/BLASCHKE_COMPACTIFICATIONS_5300014_AUTHOR_SAFE_FREEZE.zip').read_bytes() == (audit / 'AUTHOR_SAFE_FREEZE.zip').read_bytes(), 'nested author ZIP mismatch')
    require((root / 'CORRECTIONS.md').read_bytes() == (audit / 'CORRECTIONS.md').read_bytes(), 'correction wrapper mismatch')
    audited = json.loads((audit / 'ATTEMPTS_AUDITED.json').read_bytes())
    require(audited['status'] == 'unsolved' and audited['approaches_used'] == 5, 'operative status mismatch')
    require('estimated_target_completion_percent' not in json.dumps(audited), 'unsupported completion estimate')
    replay = subprocess.run([sys.executable, '-B', str(audit / 'verify_audit.py'), '--expected-manifest', status['audit_manifest_sha256']], capture_output=True, check=True)
    result = json.loads(replay.stdout)
    require(result['exact_replays_match'] is True and result['target_solved'] is False, 'audit replay failed')
    print(json.dumps({'publication_manifest_matches_external_pin': True, 'recursive_inventory_matches': True, 'payload_files_including_manifest': len(actual_files), 'original_author_zip_matches': True, 'original_audit_zip_matches': True, 'audit_zip_members_match': audit_count, 'author_zip_members_match': author_count, 'governing_corrections_match': True, 'exact_math_replays_match': True, 'optimization_modes': ['normal', '-O', '-OO'], 'target_solved': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Externally anchored publication verification, with optional exact replays."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
MANIFEST = 'PUBLICATION_MANIFEST.json'
ANCHORS = {
    'author': ('ROOTS_UNITY_30002178_AUTHOR_FREEZE.zip', 29040, 13,
        '24f88fd09d1f753306be377bcb96e17a0dd85d2ccb674975873a6046ddcbe02d',
        '12236b07d02cdc19409631ce6b56ae41d6509876a3c7fa200e2aafda1df329b6'),
    'audit': ('ROOTS_UNITY_30002178_INDEPENDENT_AUDIT.zip', 34390, 14,
        '2dbd1cf40fac63a763c992ff86b7072cf8673ecc923731120513e07357359ef9',
        'a54ae34c92324d02c3a84747ffcd051dbb15dcaf2170825d6567bae8477a9e79'),
}

def require(value, label):
    if not value:
        raise ValueError(label)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def unique_keys(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def read_json(raw):
    return json.loads(raw, object_pairs_hook=unique_keys)

def manifest_entries(raw, self_name):
    obj = read_json(raw)
    require(obj['schema'] == 'sha256-bytes-v1', 'manifest schema')
    require(isinstance(obj['files'], list), 'manifest file list')
    result = {}
    for row in obj['files']:
        name = row['path']
        require(isinstance(name, str) and re.fullmatch(r'[A-Za-z0-9_./-]+', name), 'path characters')
        path = PurePosixPath(name)
        require(not path.is_absolute() and str(path) == name and '..' not in path.parts, 'unsafe path')
        require(name != self_name and name not in result, 'duplicate or self path')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'byte count')
        require(isinstance(row['sha256'], str) and re.fullmatch(r'[a-f0-9]{64}', row['sha256']), 'hash format')
        result[name] = row
    return result

def verify(root, expected_manifest):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'package directory')
    manifest = root / MANIFEST
    require(manifest.is_file() and not manifest.is_symlink(), 'manifest file')
    raw = manifest.read_bytes()
    require(digest(raw) == expected_manifest, 'external publication manifest anchor')
    entries = manifest_entries(raw, MANIFEST)
    actual = {}
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink prohibited')
        if path.is_dir():
            continue
        require(stat.S_ISREG(path.stat().st_mode), 'nonregular file')
        name = path.relative_to(root).as_posix()
        if name != MANIFEST:
            actual[name] = path
    require(set(entries) == set(actual), 'publication file set')
    for name, path in actual.items():
        raw = path.read_bytes()
        require(len(raw) == entries[name]['bytes'] and digest(raw) == entries[name]['sha256'], 'publication bytes ' + name)
    for folder, (filename, size, count, archive_sha, manifest_sha) in ANCHORS.items():
        archive = root / filename
        raw = archive.read_bytes()
        require(len(raw) == size and digest(raw) == archive_sha, folder + ' archive anchor')
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            names = [info.filename for info in infos]
            require(len(names) == len(set(names)) == count and z.testzip() is None, folder + ' archive members')
            for info in infos:
                require(not info.is_dir() and PurePosixPath(info.filename).name == info.filename, 'flat archive path')
                require(not stat.S_ISLNK(info.external_attr >> 16), 'archive symlink')
            require(digest(z.read('MANIFEST.json')) == manifest_sha, folder + ' manifest anchor')
            inner = manifest_entries(z.read('MANIFEST.json'), 'MANIFEST.json')
            require(set(names) == set(inner) | {'MANIFEST.json'}, folder + ' member set')
            actual_names = {p.relative_to(root / folder).as_posix() for p in (root / folder).rglob('*') if p.is_file()}
            require(actual_names == set(names), folder + ' extraction set')
            for name in names:
                raw = z.read(name)
                require(raw == (root / folder / name).read_bytes(), folder + ' extraction bytes')
                if name in inner:
                    require(len(raw) == inner[name]['bytes'] and digest(raw) == inner[name]['sha256'], folder + ' member bytes')
    for path in ['author/STATUS.json', 'audit/STATUS.json', 'PUBLICATION_STATUS.json']:
        obj = read_json((root / path).read_bytes())
        require(obj['problem_id'] == '30002178' and obj['status'] == 'unsolved', 'unsolved target status')
        require(obj['turns_used'] == obj['turn_limit'] == 5, 'five-turn disposition')
        for key in ['complete_target_proof', 'counterexample', 'verified_complete_prior_resolution', 'novelty_claim', 'global_openness_claim']:
            require(obj[key] is False, 'scope non-claim ' + key)
    return len(actual) + 1

def replay(root):
    root = Path(root).resolve()
    python = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='roots-unity-replay-') as tmp:
        copied = Path(tmp) / 'relocated'
        shutil.copytree(root, copied)
        def run(script, *args):
            process = subprocess.run(python + [str(copied / script), *map(str, args)], cwd=tmp, env=env, text=True, capture_output=True)
            require(process.returncode == 0, script + ' failed: ' + process.stderr)
            return process.stdout
        author_out = Path(tmp) / 'author.json'
        audit_out = Path(tmp) / 'independent.json'
        run('author/verify_manifest.py', copied / 'author')
        run('author/test_manifest.py')
        run('audit/verify_audit.py', copied / 'audit', copied / ANCHORS['author'][0], ANCHORS['audit'][4])
        run('audit/test_audit_integrity.py')
        run('author/verify_math.py', '--output', author_out)
        require(author_out.read_bytes() == (copied / 'author/RESULTS.json').read_bytes(), 'author replay byte equality')
        run('audit/independent_exact_controls.py', copied / ANCHORS['author'][0], '--output', audit_out)
        require(audit_out.read_bytes() == (copied / 'audit/INDEPENDENT_RESULTS.json').read_bytes(), 'independent replay byte equality')
        return {'author_checks': read_json(author_out.read_bytes())['checks'], 'independent_checks': read_json(audit_out.read_bytes())['checks'], 'relocated_byte_identical': True, 'author_integrity_controls': 9, 'audit_integrity_controls': 11}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('expected_manifest_sha256')
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    result = {'status': 'PASS', 'scope': 'scoped proofs and finite checks; full target unsolved', 'package_files': verify(args.root, args.expected_manifest_sha256), 'optimized': bool(sys.flags.optimize)}
    if args.replay:
        result['replay'] = replay(args.root)
        verify(args.root, args.expected_manifest_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()

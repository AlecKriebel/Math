#!/usr/bin/env python3
"""Fail-closed, portable replay of the unchanged stable-root partial theorem."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).absolute().parent
PINS = {
    'author/MANIFEST.json': 'bbc539d32efaccd64ea3918b44e79270cb586a153062643b50d6e8d8024bdf11',
    'independent_audit/MANIFEST.json': 'f417e15077d91f2ddf85d97576ff5fb6d87a5013beffab2e3a215365386bf13c',
    'STABLE_ROOTS_30003442_AUTHOR_PACKET.zip': '388e9f7d81f3c5f13dac355b43721a65bd408cfa5b25c0d61b356c96c8a094ff',
    'STABLE_ROOTS_30003442_INDEPENDENT_AUDIT.zip': '27a99b2f3826c636c9d30eb7b996c25ff94b881ee9fae94dffb1b7ee81354aff',
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def integrity():
    require(ROOT.is_dir() and not ROOT.is_symlink(), 'Regular packet directory required')
    mf = ROOT / 'PUBLICATION_MANIFEST.json'
    require(mf.is_file() and not mf.is_symlink(), 'Regular publication manifest required')
    before = {'PUBLICATION_MANIFEST.json': mf.read_bytes()}
    manifest = json.loads(before['PUBLICATION_MANIFEST.json'])
    require(manifest['problem_id'] == '30003442', 'Wrong problem')
    require(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong status')
    records = {r['path']: r for r in manifest['files']}
    require(len(records) == len(manifest['files']) == 34, 'Wrong payload count or duplicate')
    for name in records:
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'Unsafe path')
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink input: ' + p.name)
        require(p.is_file() or p.is_dir(), 'Special input')
    files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    dirs = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_dir()}
    require(files == set(records) | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing file')
    require(dirs == {'author', 'independent_audit'}, 'Unexpected directory')
    for name, row in records.items():
        b = (ROOT / name).read_bytes()
        require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'File integrity: ' + name)
        before[name] = b
    for name, pin in PINS.items():
        require(digest(before[name]) == pin, 'Frozen binding: ' + name)
    for folder, archive, count, size in [
        ('author', 'STABLE_ROOTS_30003442_AUTHOR_PACKET.zip', 11, 24172),
        ('independent_audit', 'STABLE_ROOTS_30003442_INDEPENDENT_AUDIT.zip', 18, 61111),
    ]:
        inner = json.loads(before[folder + '/MANIFEST.json'])
        names = set(inner['files']) | {'MANIFEST.json'}
        require(len(names) == count and {p.name for p in (ROOT / folder).iterdir()} == names, 'Frozen file set')
        for name, row in inner['files'].items():
            b = before[folder + '/' + name]
            require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'Frozen manifest member')
        require(len(before[archive]) == size, 'Archive size')
        with zipfile.ZipFile(ROOT / archive) as z:
            require(len(z.infolist()) == count and set(z.namelist()) == names, 'Archive allowlist')
            for name in names:
                require(z.read(name) == before[folder + '/' + name], 'Archive member bytes')
    verdict = json.loads(before['independent_audit/AUDIT_VERDICT.json'])
    require(verdict['verdict'] == 'PASS' and not verdict['required_mathematical_corrections'], 'Audit gate')
    status = json.loads(before['PUBLICATION_STATUS.json'])
    require(status['status'] == 'unsolved' and status['turns'] == '5/5', 'Publication status')
    require(status['unrestricted_status'] == 'unresolved by this work', 'Unrestricted scope')
    return before

def run(script, *args, optimized=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    return subprocess.check_output([sys.executable, '-B', *(['-O'] if optimized else []), str(ROOT / script), *map(str, args)], cwd=ROOT, env=env)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    require(sys.version_info >= (3, 11), 'Python 3.11+ required')
    before = integrity()
    result = {'result': 'PASS', 'problem_id': '30003442', 'status': 'unsolved', 'turns': '5/5', 'packet_files': 35, 'frozen_files_preserved': 29, 'archives_preserved': 2, 'manifest_symlinks_rejected': True, 'publication_manifest_sha256': digest(before['PUBLICATION_MANIFEST.json'])}
    if not args.integrity_only:
        for optimized in [False, True]:
            require(run('author/verify.py', optimized=optimized) == before['author/verification.json'], 'Author replay mismatch')
            require(run('author/verify.py', '--self-test', optimized=optimized) == before['author/selftest.json'], 'Author negative controls mismatch')
            require(run('author/audit_manifest.py', '--self-test', optimized=optimized) == before['author/audit_checks.json'], 'Author integrity controls mismatch')
            ind = run('independent_audit/independent_verify.py', '--author', ROOT / 'author', optimized=optimized)
            require(ind == before['independent_audit/independent_results.json'], 'Independent replay mismatch')
            require(run('independent_audit/audit_integrity.py', '--author', ROOT / 'author', '--archive', ROOT / 'STABLE_ROOTS_30003442_AUTHOR_PACKET.zip', '--self-test', optimized=optimized) == before['independent_audit/independent_integrity_results.json'], 'Independent integrity controls mismatch')
        result.update(author_replay_byte_equal=True, independent_replay_byte_equal=True, normal_and_optimized=True, examples=58, author_false_claim_controls=4, author_corruption_controls=14, independent_mathematical_controls=14, independent_corruption_controls=19, sampled_positive_flow_velocities=34, repeated_flow_cases_omitted=2)
    require(integrity() == before, 'Files changed during replay')
    result['scope'] = 'Complete partial theorem min(m,d)<=3; unrestricted target unresolved; no novelty certification or general flow monotonicity.'
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()

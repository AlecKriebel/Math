#!/usr/bin/env python3
"""Externally anchored byte/inventory verification and exact diagnostic replay.

These checks do not certify analytic existence or the mathematical theorem.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
FROZEN = {
    'author': ('RICCI_INVARIANT_CONES_30001006_AUTHOR_SAFE_FREEZE.zip', 17241,
        'c7b2700050482bec8b74874b61ed050c07b3a08e1a8d06eee52d794682b1d8c1',
        'aa66b61301537ca3f73388ae7505c802a5dfce6e67b628ee76926e3b15e6f51d',
        'verify_package.py', 'math_check.py', 'results.json'),
    'audit': ('RICCI_INVARIANT_CONES_30001006_INDEPENDENT_AUDIT_SAFE.zip', 19293,
        '25a812cf211700e23835cd92b187d15969e897f0318d8c636cfc33a72d3d527b',
        '1592ceca7443dc0bb9d5c4a151aff9a37ddd7bca1f22265f82b86c03e38ea3fa',
        'verify_audit.py', 'independent_checks.py', 'independent_results.json'),
    'second_audit': ('RICCI_INVARIANT_CONES_30001006_SECOND_ANALYTIC_AUDIT_SAFE.zip', 20228,
        'c0c1d6d3c44921f953836e5b99fb21bb000d871983f966d38a542b444a64dae7',
        'd49e40a8938be7c12d77fef82a94f857fd63673ce588ca0ed50e234baf75d44c',
        'verify_release.py', 'independent_stress_checks.py', 'stress_results.json'),
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def read_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)

def execute(script, args=(), optimized=False):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    cmd = [sys.executable] + (['-O'] if optimized else []) + ['-B', str(script), *args]
    p = subprocess.run(cmd, capture_output=True, env=env)
    need(p.returncode == 0, 'replay failed: ' + str(script.relative_to(ROOT)) + '\n' + p.stderr.decode())
    return p.stdout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--queue', type=Path)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    need(re.fullmatch('[0-9a-f]{64}', args.expected_manifest) is not None, 'invalid external anchor')
    mp = ROOT / 'PUBLICATION_MANIFEST.json'
    need(mp.is_file() and not mp.is_symlink(), 'nonregular publication manifest')
    raw = mp.read_bytes()
    need(digest(raw) == args.expected_manifest, 'publication manifest anchor mismatch')
    manifest = read_json(raw)
    need(set(manifest) == {'schema', 'files'} and manifest['schema'] == 'ricci-publication-v1', 'bad manifest schema')
    files = manifest['files']
    need(isinstance(files, dict) and bool(files), 'empty inventory')
    directories = set()
    for name, entry in files.items():
        path = PurePosixPath(name)
        need(not path.is_absolute() and str(path) == name and '..' not in path.parts and '\\' not in name,
             'unsafe inventory path')
        need(name != 'PUBLICATION_MANIFEST.json', 'self-listed manifest')
        need(set(entry) == {'bytes', 'sha256'}, 'bad file schema')
        need(type(entry['bytes']) is int and entry['bytes'] >= 0, 'bad length')
        need(re.fullmatch('[0-9a-f]{64}', entry['sha256']) is not None, 'bad digest')
        p = ROOT / name
        need(p.is_file() and not p.is_symlink(), 'nonregular member: ' + name)
        b = p.read_bytes()
        need(len(b) == entry['bytes'] and digest(b) == entry['sha256'], 'member mismatch: ' + name)
        directories.update(str(x) for x in path.parents if str(x) != '.')
    actual_files, actual_dirs = set(), set()
    for p in ROOT.rglob('*'):
        name = p.relative_to(ROOT).as_posix()
        need(not p.is_symlink(), 'symlink in publication')
        if p.is_file():
            actual_files.add(name)
        elif p.is_dir():
            actual_dirs.add(name)
        else:
            raise RuntimeError('nonregular publication object')
    need(actual_files == set(files) | {'PUBLICATION_MANIFEST.json'}, 'publication file-set mismatch')
    need(actual_dirs == directories, 'publication directory-set mismatch')
    archive_members = 0
    for folder, (archive, length, sha, anchor, verifier, diagnostic, result) in FROZEN.items():
        zp = ROOT / 'archives' / archive
        data = zp.read_bytes()
        need(len(data) == length and digest(data) == sha, 'frozen archive mismatch')
        need(digest((ROOT / folder / 'MANIFEST.json').read_bytes()) == anchor, 'frozen manifest mismatch')
        with zipfile.ZipFile(zp) as z:
            names = z.namelist()
            expected = {p.name for p in (ROOT / folder).iterdir()}
            need(len(names) == len(set(names)) and set(names) == expected, 'archive member-set mismatch')
            need(z.testzip() is None, 'ZIP CRC error')
            for info in z.infolist():
                need(not info.is_dir() and PurePosixPath(info.filename).name == info.filename,
                     'unsafe ZIP member')
                need((info.external_attr >> 16) & 0o170000 != 0o120000, 'ZIP symlink')
                need(z.read(info) == (ROOT / folder / info.filename).read_bytes(), 'archive extraction mismatch')
                archive_members += 1
    metadata = read_json((ROOT / 'PUBLICATION_METADATA.json').read_bytes())
    need(metadata['problem_id'] == 30001006 and metadata['status'] == 'unsolved' and metadata['turns'] == '1/5',
         'incorrect disposition')
    need(metadata['full_classification_solved'] is False and metadata['mathematical_corrections_required'] is False,
         'incorrect scope')
    if args.queue:
        need(args.queue.is_file() and not args.queue.is_symlink(), 'nonregular queue')
        need(digest(args.queue.read_bytes()) == metadata['queue']['after_sha256'], 'queue hash mismatch')
    replays = []
    if not args.integrity_only:
        for folder, (_, _, _, anchor, verifier, diagnostic, result) in FROZEN.items():
            for optimized in (False, True):
                label = folder + ('_optimized' if optimized else '_normal')
                execute(ROOT / folder / verifier, ['--expected-manifest', anchor], optimized)
                output = execute(ROOT / folder / diagnostic, optimized=optimized)
                need(output == (ROOT / folder / result).read_bytes(), 'direct diagnostic replay differs: ' + label)
                replays.append(label)
        for folder, script in [('author', 'test_integrity.py'), ('audit', 'test_audit_integrity.py')]:
            output = execute(ROOT / folder / script)
            need(output == (ROOT / folder / 'integrity_results.json').read_bytes(), 'frozen integrity replay differs')
            replays.append(folder + '_full_integrity_harness')
    print(json.dumps({'status': 'PASS', 'mode': 'integrity_only' if args.integrity_only else 'full',
        'publication_files': len(files) + 1, 'archive_members': archive_members,
        'frozen_release_replays': replays, 'queue_checked': args.queue is not None,
        'external_corpora_replayed': False, 'mathematical_certification': False}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)

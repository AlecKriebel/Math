#!/usr/bin/env python3
"""Strict package identity and exact replay checks; no theorem certification."""
import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

EXPECTED = {
    'public/ATTEMPT_LOG.md', 'public/CHECKS.json',
    'public/FROZEN_MANIFEST.json', 'public/PROOF.md', 'public/README.md',
    'public/SOURCE_GATE.md', 'public/SOURCE_MANIFEST.json',
    'public/STATUS.json', 'public/verify.py',
    'independent-audit/AUDIT.md', 'independent-audit/AUDITED_INPUTS.json',
    'independent-audit/AUDIT_MANIFEST.json', 'independent-audit/AUDIT_STATUS.json',
    'independent-audit/README.md', 'independent-audit/REPLAY.json',
    'independent-audit/SOURCE_INSPECTION.json', 'independent-audit/verify_audit.py',
    'RELEASE_NOTES.md', 'verify_release.py',
}
FREEZE = '4ec513d83ee59af8d053982926ab62054a363da10abb82d8e0d4254a2f84d7ff'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'Duplicate JSON key')
        obj[key] = value
    return obj

def read_json(path):
    return json.loads(path.read_bytes(), object_pairs_hook=no_duplicates)

def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}

def validate_names(names):
    for name in names:
        require(isinstance(name, str), 'Non-string path')
        path = PurePosixPath(name)
        require(not path.is_absolute() and '\\' not in name and
                '..' not in path.parts and '.' not in path.parts and
                str(path) == name, 'Unsafe path')

def verify_manifest(root):
    require(not root.is_symlink() and root.is_dir(), 'Invalid root')
    entries = list(root.rglob('*'))
    require(not any(p.is_symlink() for p in entries), 'Symlink in package')
    actual = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    require(actual == EXPECTED | {'RELEASE_MANIFEST.json'}, 'Unexpected file set')
    dirs = {p.relative_to(root).as_posix() for p in entries if p.is_dir()}
    require(dirs == {'public', 'independent-audit'}, 'Unexpected directory set')
    release = read_json(root/'RELEASE_MANIFEST.json')
    validate_names(release['files'])
    require(set(release['files']) == EXPECTED, 'Manifest file set mismatch')
    for name, expected in release['files'].items():
        require(digest(root/name) == expected, 'Digest mismatch: '+name)
    require(digest(root/'public/FROZEN_MANIFEST.json')['sha256'] == FREEZE,
            'Frozen binding mismatch')
    author = read_json(root/'public/FROZEN_MANIFEST.json')
    validate_names(author['files'])
    require(set(author['files']) == {p.split('/', 1)[1] for p in EXPECTED
            if p.startswith('public/')} - {'FROZEN_MANIFEST.json'},
            'Author manifest set mismatch')
    for name, expected in author['files'].items():
        require(digest(root/'public'/name) == expected, 'Author binding mismatch')
    audit = read_json(root/'independent-audit/AUDIT_MANIFEST.json')
    validate_names(audit['files'])
    require(set(audit['files']) == {p for p in EXPECTED
            if p.startswith(('public/', 'independent-audit/'))}
            - {'independent-audit/AUDIT_MANIFEST.json'}, 'Audit manifest set mismatch')
    for name, expected in audit['files'].items():
        require(digest(root/name) == expected, 'Audit binding mismatch')
    return len(actual)

def replays(root):
    for script, stored in [('public/verify.py', 'public/CHECKS.json'),
                           ('independent-audit/verify_audit.py',
                            'independent-audit/REPLAY.json')]:
        run = subprocess.run([sys.executable, '-B', str(root/script)],
                             cwd=root, check=True, capture_output=True)
        require(run.stdout == (root/stored).read_bytes(), 'Replay byte mismatch')
        require(not run.stderr, 'Unexpected replay stderr')
    verify_manifest(root)

def negative_controls(root):
    results = []
    for kind in ('changed_byte', 'missing_file', 'extra_file', 'extra_nested_file',
                 'symlink', 'manifest_traversal'):
        with tempfile.TemporaryDirectory(prefix='planarity-package-test-') as tmp:
            copy = Path(tmp)/'packet'
            shutil.copytree(root, copy)
            target = copy/'public/README.md'
            if kind == 'changed_byte':
                data = target.read_bytes()
                target.write_bytes(bytes([data[0] ^ 1])+data[1:])
            elif kind == 'missing_file':
                target.unlink()
            elif kind == 'extra_file':
                (copy/'unexpected.txt').write_text('unexpected\n')
            elif kind == 'extra_nested_file':
                (copy/'nested').mkdir()
                (copy/'nested/extra.txt').write_text('unexpected\n')
            elif kind == 'symlink':
                target.unlink()
                target.symlink_to(copy/'public/PROOF.md')
            else:
                path = copy/'RELEASE_MANIFEST.json'
                manifest = read_json(path)
                manifest['files']['../outside'] = manifest['files'].pop('RELEASE_NOTES.md')
                path.write_text(json.dumps(manifest))
            try:
                verify_manifest(copy)
            except ValueError:
                results.append(kind)
            else:
                raise ValueError('Negative control accepted: '+kind)
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    count = verify_manifest(root)
    replays(root)
    rejected = negative_controls(root) if args.self_test else []
    print(json.dumps({'passed': True, 'verified_files': count,
                      'author_replay_byte_identical': True,
                      'independent_replay_byte_identical': True,
                      'nested_manifests_matched': True,
                      'rejected_negative_controls': rejected,
                      'status': 'unsolved', 'routes_completed': 5},
                     indent=2, sort_keys=True))

if __name__ == '__main__':
    main()

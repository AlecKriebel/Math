#!/usr/bin/env python3
"""Strict final-layout verification and negative controls; standard library only."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

AUTHOR_MANIFEST = '5f04dcc149f26a7cab938e0fdf5c649e56230667eab8c0f75ebd5c34ea67f1ad'
AUDIT_MANIFEST = 'd0c9688f95c504e489c440edfa329a59a1668de6a11f5f67c0396fdc74571632'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    out = set()
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError('Symlink not permitted')
        if p.is_file():
            out.add(p.relative_to(root).as_posix())
    return out


def strict_manifest(root, filename='MANIFEST.json', expected_hash=None):
    raw = (root/filename).read_bytes()
    if expected_hash is not None and sha(raw) != expected_hash:
        raise ValueError('Manifest identity mismatch')
    manifest = json.loads(raw)
    paths = set()
    for row in manifest['files']:
        rel = row['path']
        pp = PurePosixPath(rel)
        if (not isinstance(rel, str) or not rel or pp.is_absolute() or
                '..' in pp.parts or '.' in rel.split('/') or
                pp.as_posix() != rel or '\\' in rel or
                rel == filename or rel in paths):
            raise ValueError('Unsafe or duplicate manifest path')
        paths.add(rel)
        p = root/rel
        if p.is_symlink() or not p.is_file():
            raise ValueError('Missing file or symbolic link')
        data = p.read_bytes()
        if len(data) != row['bytes'] or sha(data) != row['sha256']:
            raise ValueError('File length/hash mismatch')
    if inventory(root) != paths | {filename}:
        raise ValueError('Inventory differs from manifest')
    return len(paths)


def negative_controls(root):
    passed = []
    for case in ['changed_bytes', 'missing_file', 'unlisted_file',
                 'symlink', 'duplicate_path', 'parent_path']:
        with tempfile.TemporaryDirectory(prefix='baker-release-') as d:
            dest = Path(d)/'packet'
            shutil.copytree(root/'author', dest)
            if case == 'changed_bytes':
                p = dest/'RESULT.md'; p.write_bytes(p.read_bytes()+b'\n')
            elif case == 'missing_file':
                (dest/'RESULT.md').unlink()
            elif case == 'unlisted_file':
                (dest/'EXTRA.txt').write_text('unexpected')
            elif case == 'symlink':
                (dest/'LINK.txt').symlink_to('RESULT.md')
            else:
                p = dest/'MANIFEST.json'; m = json.loads(p.read_text())
                if case == 'duplicate_path':
                    m['files'].append(m['files'][0].copy())
                else:
                    m['files'][0]['path'] = '../RESULT.md'
                p.write_text(json.dumps(m))
            try:
                # Omit pinned manifest hash here to exercise structural defenses.
                strict_manifest(dest)
            except (ValueError, FileNotFoundError):
                passed.append(case)
            else:
                raise AssertionError('Negative control was accepted: '+case)
    return passed


def main():
    root = Path(__file__).resolve().parent
    release_count = strict_manifest(root, 'RELEASE_MANIFEST.json')
    author_count = strict_manifest(root/'author', expected_hash=AUTHOR_MANIFEST)
    audit_count = strict_manifest(root/'audit', expected_hash=AUDIT_MANIFEST)
    run = subprocess.run([sys.executable, str(root/'audit/verify_release.py'),
                          str(root/'author')], capture_output=True, check=True)
    replay = json.loads(run.stdout)
    assert replay['original_replay_byte_identical']
    assert replay['independent_replay_byte_identical']
    negatives = negative_controls(root)
    result = {'status': 'passed', 'target_id': 30001388,
              'release_files_verified': release_count,
              'author_files_verified': author_count,
              'audit_files_verified': audit_count,
              'original_and_audit_replays': 'byte-identical',
              'strict_inventory_verified': True,
              'negative_controls_rejected': negatives,
              'scope': 'Reproducibility and integrity, not resolution of the target.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

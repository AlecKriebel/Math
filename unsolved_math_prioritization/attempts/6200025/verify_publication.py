#!/usr/bin/env python3
"""Offline verification of the exact publication layout and control replays."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue', type=Path)
    args = parser.parse_args()
    manifest = json.loads((root / 'PUBLICATION_MANIFEST.json').read_text())
    rows = manifest['files']
    names = [r['path'] for r in rows]
    assert len(names) == len(set(names)), 'duplicate paths'
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names), 'unsafe paths'
    assert not any(p.is_symlink() for p in root.rglob('*')), 'symlink'
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual == set(names) | {'PUBLICATION_MANIFEST.json'}, 'exact file set differs'
    directories = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
    assert directories == {'submission', 'audit'}, 'directory set differs'
    for row in rows:
        data = (root / row['path']).read_bytes()
        assert len(data) == row['bytes'] and digest(data) == row['sha256'], row['path']
    for folder, binding in manifest['frozen_packages'].items():
        data = (root / folder / 'SHA256SUMS.json').read_bytes()
        assert len(data) == binding['bytes'] and digest(data) == binding['sha256'], folder
    subprocess.run([sys.executable, str(root / 'submission' / 'verify_manifest.py')], check=True)
    subprocess.run([sys.executable, str(root / 'audit' / 'verify_audit.py')], check=True)
    result = {'result': 'pass', 'publication_files': len(actual), 'author_files': 14,
              'audit_files': 10, 'author_and_independent_replays': 'pass', 'queue_checked': False}
    if args.queue:
        data = args.queue.read_bytes()
        q = manifest['queue_change']
        assert len(data) == q['queue_bytes'] and digest(data) == q['queue_sha256'], 'queue bytes'
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == q['queue_git_blob_sha']
        target = [line for line in data.decode().splitlines() if '| 646 | 6200025 / AMR-061-0025 |' in line]
        assert target == [q['new_row']], 'target row'
        prior = data.replace((q['new_row'] + '\n').encode(), (q['old_row'] + '\n').encode(), 1)
        assert len(prior) == q['base_queue_bytes'] and digest(prior) == q['base_queue_sha256'], 'other queue bytes changed'
        assert hashlib.sha1(b'blob ' + str(len(prior)).encode() + b'\0' + prior).hexdigest() == q['base_queue_git_blob_sha']
        result['queue_checked'] = True
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

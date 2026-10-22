#!/usr/bin/env python3
"""Read-only, stdout-only authentication of the immutable 44-file candidate."""
import argparse
import hashlib
import json
import pathlib
import stat
import subprocess
import sys

HEAD = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
PREFIX = 'unsolved_math_prioritization/attempts/30003634'
INVENTORY_SHA256 = 'b197cade40c4804b09fd3d9af3519e1a8258ef9f4d0a7df7635e59825aa60a6d'
PROOF_SHA256 = '0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b'
OUTER_SHA256 = '149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30'
BASE = pathlib.Path(__file__).absolute().parents[2]
REPO = BASE.parents[2]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def regular_no_symlink(path):
    path = path.absolute()
    for parent in [path, *path.parents]:
        require(not parent.is_symlink(), 'symlink rejected: ' + str(parent))
    require(stat.S_ISREG(path.stat().st_mode), 'not a regular file: ' + str(path))
    return path.read_bytes()


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])


def verify(inventory, copied_root):
    raw = regular_no_symlink(inventory)
    require(hashlib.sha256(raw).hexdigest() == INVENTORY_SHA256, 'inventory digest mismatch')
    data = json.loads(raw)
    require(data['head'] == HEAD, 'head mismatch')
    require(len(data['files']) == 44, 'inventory count mismatch')
    actual_tree = {}
    for row in git('ls-tree', '-r', '-z', HEAD, '--', PREFIX).split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = path.decode()
        require(mode == '100644' and kind == 'blob', 'unexpected Git type/mode')
        actual_tree[name] = oid
    require(set(actual_tree) == set(data['files']), 'Git tree/inventory paths differ')
    rows = []
    for path, expected in sorted(data['files'].items()):
        rel = pathlib.PurePosixPath(path)
        require(str(rel).startswith(PREFIX + '/') and '..' not in rel.parts, 'unsafe relative path')
        blob = git('cat-file', 'blob', HEAD + ':' + path)
        disk = regular_no_symlink(copied_root / path)
        digest = hashlib.sha256(blob).hexdigest()
        require(digest == expected and blob == disk, 'blob/disk/inventory mismatch: ' + path)
        rows.append({'path': path, 'bytes': len(blob), 'sha256': digest, 'git_blob_oid': actual_tree[path]})
    require(data['files'][PREFIX + '/original/PROOF.md'] == PROOF_SHA256, 'proof pin mismatch')
    require(data['files'][PREFIX + '/PUBLICATION_MANIFEST.json'] == OUTER_SHA256, 'outer pin mismatch')
    require(git('branch', '--show-current').decode().strip() == 'main', 'branch changed')
    return {'accepted': True, 'head': HEAD, 'count': len(rows), 'git_tree_complete': True,
            'inventory_sha256': INVENTORY_SHA256, 'branch': 'main', 'rows': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=pathlib.Path, default=BASE / 'ORIGINAL_SNAPSHOT.json')
    parser.add_argument('--copied-root', type=pathlib.Path, default=BASE / 'original')
    args = parser.parse_args()
    try:
        result = verify(args.inventory, args.copied_root)
    except (ValueError, OSError, KeyError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'accepted': False, 'error': str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())

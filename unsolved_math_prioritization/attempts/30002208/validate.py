#!/usr/bin/env python3
"""Fail-closed snapshot integrity checks; NOT a mathematical proof checker."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def stamp(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'root must be a real directory')
    files, dirs = {}, []
    def walk(path):
        with os.scandir(path) as entries:
            for e in entries:
                s = e.stat(follow_symlinks=False)
                rel = str(Path(e.path).relative_to(root))
                if stat.S_ISDIR(s.st_mode):
                    dirs.append(rel)
                    walk(Path(e.path))
                else:
                    require(stat.S_ISREG(s.st_mode), 'special file or symlink: ' + rel)
                    require(s.st_nlink == 1, 'hard-linked file: ' + rel)
                    files[rel] = stamp(s)
    walk(root)
    return files, sorted(dirs)


def read_regular(path, expected=None):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'not a singly-linked regular file: ' + str(path))
    if expected is not None:
        require(stamp(before) == expected, 'changed before read: ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        require(stamp(os.fstat(fd)) == stamp(before), 'file replaced during open')
        with os.fdopen(fd, 'rb', closefd=False) as f:
            data = f.read()
        require(stamp(os.fstat(fd)) == stamp(before), 'file changed during read')
    finally:
        os.close(fd)
    require(stamp(path.lstat()) == stamp(before), 'file replaced after read')
    return data


def metadata(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    # Complete recursive type screening before reading package content or manifest.
    files, dirs = inventory(root)
    require(not dirs, 'unexpected directories: ' + repr(dirs))
    receipt_path = args.receipt.absolute()
    require(root not in receipt_path.parents, 'receipt must be outside package')
    receipt = json.loads(read_regular(receipt_path))
    require(receipt['schema'] == 'syndeticity-preserver-freeze-v1', 'receipt schema')
    require(receipt['problem_id'] == 30002208 and receipt['ordered_row'] == 1881, 'wrong target')
    expected = receipt['files']
    require(set(files) == set(expected), 'closed file inventory mismatch')
    data = {name: read_regular(root/name, stamp_) for name, stamp_ in files.items()}
    actual = {name: metadata(content) for name, content in data.items()}
    require(actual == expected, 'external receipt hash/size mismatch')
    manifest = json.loads(data['MANIFEST.json'])
    require(manifest['files'] == {k: v for k, v in actual.items() if k != 'MANIFEST.json'}, 'manifest mismatch')
    provenance = json.loads(data['PROVENANCE.json'])
    for item in provenance['original_artifacts']:
        require(actual[item['package_path']] == {k: item[k] for k in ('bytes', 'sha256')}, 'original artifact hash mismatch')
    require(inventory(root) == (files, dirs), 'inventory changed during validation')
    print(json.dumps({'status':'PASS', 'scope':'integrity only; no mathematical certification', 'problem_id':30002208, 'files':len(files), 'optimized':bool(sys.flags.optimize)}))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)

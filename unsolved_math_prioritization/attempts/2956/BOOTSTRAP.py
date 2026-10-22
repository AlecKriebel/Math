#!/usr/bin/env python3
"""Authenticate this file externally before execution. It pins the exact release."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import os
from pathlib import Path
import stat

MANIFEST_SHA256 = '5ad7d5a5130f4ddd526a3e1baca20164d78eea5bc5d53e6cfc0c206c6a5f85ac'
VERIFIER_SHA256 = 'bc6c9fd7d0faa65ed45da6002147b029c1934167263be5e3b12e18dc3b350c67'
VERIFIER_BYTES = 22236


def need(ok):
    if not ok:
        raise ValueError('bootstrap integrity')


def ordinary(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000)
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as f:
        opened = os.fstat(f.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino))
        raw = f.read(1000001)
    need(len(raw) == before.st_size)
    return raw


def main():
    need(len(sys.argv) == 2)
    root = Path(os.path.abspath(sys.argv[1]))
    for p in (root, *root.parents):
        need(stat.S_ISDIR(p.lstat().st_mode))
    trusted = ordinary(Path(__file__))
    need(ordinary(root/'BOOTSTRAP.py') == trusted)
    manifest = ordinary(root/'PUBLICATION_MANIFEST.json')
    need(hashlib.sha256(manifest).hexdigest() == MANIFEST_SHA256)
    wrapper = ordinary(root/'verify_publication.py')
    need(len(wrapper) == VERIFIER_BYTES and hashlib.sha256(wrapper).hexdigest() == VERIFIER_SHA256)
    sys.argv = ['verify_publication.py', MANIFEST_SHA256, hashlib.sha256(trusted).hexdigest(), str(root)]
    exec(compile(wrapper, '<authenticated-publication-verifier>', 'exec'), {'__name__':'__main__'})


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError):
        print('REJECT: bootstrap integrity validation failed', file=sys.stderr)
        sys.exit(1)

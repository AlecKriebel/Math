#!/usr/bin/env python3
"""Authenticate this file externally before execution. It pins the exact release."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import os
from pathlib import Path
import stat

MANIFEST_SHA256 = 'd082751c14cf1266d01a6f197511f2ea5e486ebd15898241b7a3d0b19a9517ca'
VERIFIER_SHA256 = '13988f4cefa0270922f45d001a34994b1800ca685ce343fd208601305a8602b0'
VERIFIER_BYTES = 22279


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

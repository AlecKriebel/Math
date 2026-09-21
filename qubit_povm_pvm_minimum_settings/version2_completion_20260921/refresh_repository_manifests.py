#!/usr/bin/env python3
"""Refresh checksums for tracked repository files, independently of ZIP manifests.

Stage newly required files before invoking. Local output ZIPs/caches and other
ignored research working directories are deliberately outside these manifests.
Historical nested manifests are preserved byte-for-byte.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import subprocess

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent


def refresh(root: Path) -> int:
    names = subprocess.check_output(['git', 'ls-files', '-z', '--', root.relative_to(REPO).as_posix()],
                                    cwd=REPO).decode().split('\0')
    files = sorted(REPO/name for name in names if name and REPO/name != root/'SHA256SUMS.txt')
    for path in files:
        if not path.is_file() or path.is_symlink():
            raise ValueError(f'Missing or linked tracked artifact: {path}')
    (root/'SHA256SUMS.txt').write_text(''.join(
        hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix()+'\n' for p in files))
    return len(files)


if __name__ == '__main__':
    print('Lean repository files:', refresh(PROJECT/'bell_lean'))
    print('Project repository files:', refresh(PROJECT))

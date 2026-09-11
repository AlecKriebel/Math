#!/usr/bin/env python3
"""Verify a freshly extracted source package's root SHA-256 manifest.

Run before tests/builds regenerate reports. Later legitimate edits invalidate
these shipment hashes. This check does not validate any mathematical statement.
"""
import hashlib
from pathlib import Path
from package import parse_manifest

ROOT = Path(__file__).resolve().parents[1]

def verify(root: Path) -> int:
    manifest = parse_manifest((root/'SHA256SUMS.txt').read_text())
    for name, expected in manifest.items():
        p = root/name
        if p.is_symlink() or not p.is_file():
            raise ValueError(f'Missing or symlinked manifest file: {name}')
        # Check every parent too, so directory links cannot leave the package.
        parent = root
        for part in Path(name).parts[:-1]:
            parent = parent/part
            if parent.is_symlink():
                raise ValueError(f'Symlinked parent for manifest file: {name}')
        if hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Checksum mismatch: {name}')
    print(f'BYTE INTEGRITY PASSED: {len(manifest)} files. Not Lean verification.')
    return len(manifest)

if __name__ == '__main__':
    verify(ROOT)

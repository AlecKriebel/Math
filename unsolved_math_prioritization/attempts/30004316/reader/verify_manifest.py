#!/usr/bin/env python3
"""Check this reader's ordinary file inventory against its local manifest."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    require(manifest['format'] == 'quantum-symmetrizer-reader-manifest-v1', 'unknown manifest format')
    expected = set()
    for entry in manifest['files']:
        name = entry['path']
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and '..' not in parts.parts, 'invalid manifest path')
        require(name not in expected and name != 'MANIFEST.json', 'duplicate or self-referential entry')
        expected.add(name)
        data = (root / name).read_bytes()
        require(len(data) == entry['bytes'], 'byte count mismatch: ' + name)
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'SHA256 mismatch: ' + name)
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual == expected | {'MANIFEST.json'}, 'file inventory mismatch')
    print(json.dumps({'files_verified': len(expected), 'inventory_match': True}, sort_keys=True))


if __name__ == '__main__':
    main()

"""Recursive integrity check, not mathematical proof or an authenticity signature."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys


def verify(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('unsafe package root')
    manifest = root / 'package_manifest.json'
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('missing or unsafe root manifest')
    data = json.loads(manifest.read_text())
    if data.get('schema') != 1 or not isinstance(data.get('files'), list):
        raise ValueError('invalid manifest schema')
    expected = {}
    for item in data['files']:
        name = item['path']
        if not isinstance(name, str) or not name or '\\' in name or '\x00' in name:
            raise ValueError('unsafe manifest path')
        p = PurePosixPath(name)
        if p.is_absolute() or any(x in ('', '.', '..') for x in name.split('/')) or ':' in name:
            raise ValueError('unsafe manifest path')
        if str(p) != name or name == 'package_manifest.json' or name in expected:
            raise ValueError('duplicate, noncanonical, or self-listed path')
        if type(item['bytes']) is not int or item['bytes'] < 0:
            raise ValueError('invalid size')
        h = item['sha256']
        if not isinstance(h, str) or len(h) != 64 or any(c not in '0123456789abcdef' for c in h):
            raise ValueError('invalid digest')
        expected[name] = item
    actual = {}
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError('symlink forbidden: ' + p.relative_to(root).as_posix())
        if p.is_dir():
            continue
        if not p.is_file():
            raise ValueError('nonregular entry')
        name = p.relative_to(root).as_posix()
        if name == 'package_manifest.json':
            continue
        actual[name] = p
    if set(actual) != set(expected):
        raise ValueError('recursive inventory mismatch: ' + repr(sorted(set(actual) ^ set(expected))))
    for name, p in actual.items():
        content = p.read_bytes()
        if len(content) != expected[name]['bytes'] or hashlib.sha256(content).hexdigest() != expected[name]['sha256']:
            raise ValueError('content mismatch: ' + name)
    return {'status': 'PASS', 'files_verified': len(actual), 'manifest_self_hash_excluded': True}


if __name__ == '__main__':
    try:
        print(json.dumps(verify(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent), sort_keys=True))
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)

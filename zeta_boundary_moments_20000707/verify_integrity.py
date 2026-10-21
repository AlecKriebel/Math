"""Strict recursive package inventory; manifest excludes only itself."""
import hashlib
import json
from pathlib import Path, PurePosixPath

def verify(root):
    root = Path(root)
    if root.is_symlink():
        raise RuntimeError('Symlink root forbidden')
    actual = {}
    for path in root.rglob('*'):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise RuntimeError('Symlink forbidden: ' + rel)
        if path.is_dir():
            continue
        if not path.is_file():
            raise RuntimeError('Nonregular file: ' + rel)
        if path.name.lower() == 'manifest.json' and rel != 'MANIFEST.json':
            raise RuntimeError('Nested or ambiguous manifest: ' + rel)
        if rel == 'MANIFEST.json':
            continue
        data = path.read_bytes()
        actual[rel] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    if set(manifest) != {'schema', 'files'} or manifest['schema'] != 1:
        raise RuntimeError('Manifest schema invalid')
    expected = {}
    for row in manifest['files']:
        if set(row) != {'path', 'bytes', 'sha256'}:
            raise RuntimeError('Invalid row')
        name = row['path']
        if not isinstance(name,str) or not name or '\\' in name or any(ord(c)<32 for c in name):
            raise RuntimeError('Unsafe path')
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '.' in name.split('/') or p.as_posix()!=name or ':' in name:
            raise RuntimeError('Unsafe path')
        if name == 'MANIFEST.json' or p.name.lower()=='manifest.json' or name in expected:
            raise RuntimeError('Duplicate or excluded manifest path')
        if type(row['bytes']) is not int or row['bytes'] < 0 or not isinstance(row['sha256'],str) or len(row['sha256']) != 64 or any(c not in '0123456789abcdef' for c in row['sha256']):
            raise RuntimeError('Invalid fingerprint')
        expected[name] = {k:row[k] for k in ('bytes','sha256')}
    if expected != actual:
        raise RuntimeError('Recursive inventory mismatch')
    return {'status':'PASS','files':len(actual),'scope':'Every package file except root MANIFEST.json'}

if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent),indent=2))

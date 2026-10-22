"""Read-only recursive verification of this review's closed authored inventory."""
from pathlib import Path
import hashlib
import json
import stat


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'MANIFEST.json').read_text())
    rows = manifest['authored_files']
    names = [row['path'] for row in rows]
    if len(names) != len(set(names)) or 'MANIFEST.json' in names:
        raise ValueError('Duplicate/self manifest entry')
    actual = set()
    directories = set()
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError('Symlink')
        name = p.relative_to(root).as_posix()
        if p.is_dir():
            directories.add(name)
        elif p.is_file() and stat.S_ISREG(p.stat().st_mode):
            if name != 'MANIFEST.json':
                actual.add(name)
        else:
            raise ValueError('Special object')
    if actual != set(names):
        raise ValueError('Inventory differs')
    expected_dirs = {p.as_posix() for name in actual for p in Path(name).parents if p.as_posix() != '.'}
    if directories != expected_dirs:
        raise ValueError('Empty/unlisted directory')
    for row in rows:
        raw = (root/row['path']).read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('Changed file: '+row['path'])
    print(json.dumps({'status':'PASS','authored_regular_files':len(rows),
                      'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Strict read-only publication inventory, archive equality, and portable replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'PUBLICATION_MANIFEST.json').read_text())
    rows = manifest['files']
    expected = {row['path'] for row in rows} | {'PUBLICATION_MANIFEST.json'}
    require(len(expected) == len(rows) + 1, 'Duplicate manifest entries')
    expected_dirs = set()
    for rel in expected:
        p = Path(rel)
        require(not p.is_absolute() and '..' not in p.parts, 'Unsafe manifest path')
        expected_dirs.update(q.as_posix() for q in p.parents if q != Path('.'))
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        rel = p.relative_to(root).as_posix()
        require(not p.is_symlink(), 'Unexpected symlink: ' + rel)
        if p.is_file():
            actual_files.add(rel)
        elif p.is_dir():
            actual_dirs.add(rel)
        else:
            raise ValueError('Unexpected non-regular entry: ' + rel)
    require(actual_files == expected, 'Publication file inventory mismatch')
    require(actual_dirs == expected_dirs, 'Publication directory inventory mismatch')
    for row in rows:
        b = (root / row['path']).read_bytes()
        require(len(b) == row['bytes'], 'Size mismatch: ' + row['path'])
        require(hashlib.sha256(b).hexdigest() == row['sha256'], 'Hash mismatch: ' + row['path'])
    for dirname, archive in [('polynomial_2200006', 'polynomial_2200006_AUTHORED.zip'),
                             ('polynomial_2200006_independent_audit', 'polynomial_2200006_INDEPENDENT_AUDIT.zip')]:
        names = {p.name for p in (root / dirname).iterdir()}
        with zipfile.ZipFile(root / archive) as z:
            members = z.infolist()
            require(len(members) == len(names), 'Archive member count mismatch')
            require(len({m.filename for m in members}) == len(members), 'Duplicate ZIP members')
            require({Path(m.filename).name for m in members} == names, 'Archive inventory mismatch')
            for m in members:
                p = Path(m.filename)
                require(not m.is_dir() and not p.is_absolute() and '..' not in p.parts, 'Unsafe ZIP member')
                require(z.read(m.filename) == (root / dirname / p.name).read_bytes(), 'Archive byte mismatch')
    results = {}
    for key, script in [('author', 'polynomial_2200006/verify_package.py'),
                        ('audit', 'polynomial_2200006_independent_audit/verify_audit.py')]:
        run = subprocess.run([sys.executable, '-B', str(root / script)], check=True, capture_output=True)
        results[key] = json.loads(run.stdout)
    results.update({'publication_inventory': 'PASS', 'publication_hashes': 'PASS',
                    'archive_member_bytes': 'PASS', 'files': len(expected),
                    'problem_status': 'unsolved', 'turns': '5/5',
                    'formal_proof_claim': False})
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

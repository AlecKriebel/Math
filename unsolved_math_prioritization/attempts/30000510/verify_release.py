#!/usr/bin/env python3
"""Offline release integrity and finite-control replay, not formal proof checking."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import zipfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    require(sys.flags.optimize == 0 and __debug__, 'Run without -O, -OO, or PYTHONOPTIMIZE.')
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'RELEASE_MANIFEST.json').read_text())
    require(manifest['problem_id'] == 30000510 and manifest['rank'] == 657,
            'Wrong problem identity')
    require(manifest['status'] == 'already_solved' and manifest['turns'] == '1/5',
            'Wrong release disposition')
    entries = manifest['files']
    expected = {e['path']: e for e in entries}
    require(len(expected) == len(entries), 'Duplicate manifest paths')
    actual = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlink is not permitted: ' + str(p))
        if p.is_file():
            actual.add(p.relative_to(root).as_posix())
    require(actual == set(expected) | {'RELEASE_MANIFEST.json'}, 'Unexpected or missing file')
    for name, e in expected.items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe path')
        data = (root / name).read_bytes()
        require(len(data) == e['bytes'] and sha256(data) == e['sha256'], 'Changed file: ' + name)
    pins = {
        'AUTHOR_FREEZE.json': '37cf18bd16178ae4c8cc7aefc84712dff2bed750cb5e91e10fdd8a4c556007f1',
        'author-packet.zip': '9aeff19fabf35423f3e8a169212ebf47e56e306d7a55bd323cce1eca7628251e',
        'AUDIT_MANIFEST.json': '6a674b30b1c8d9bf9de8bed653bd12b6c6d9d5e0a9a18ec9425ccccd3dbe5ceb',
        'audit-packet.zip': '6fe1d440bf438881172f1cf48fd40852abd3412c4637b374fa9ddb36a9e69298',
        'AUDIT_BINDING.json': '2aa845cb98d4905667371077e54840e1dc382be80f4187202e91cba84f2408ae',
    }
    for name, digest in pins.items():
        require(sha256((root / name).read_bytes()) == digest, 'Frozen identity changed: ' + name)
    author = json.loads((root / 'AUTHOR_FREEZE.json').read_text())
    audit = json.loads((root / 'AUDIT_MANIFEST.json').read_text())
    binding = json.loads((root / 'AUDIT_BINDING.json').read_text())
    for e in binding['files'] + audit['author_binding']['files']:
        data = (root / e['path']).read_bytes()
        require(len(data) == e['bytes'] and sha256(data) == e['sha256'], 'Binding mismatch')
    archives = {
        'author-packet.zip': {'AUTHOR_FREEZE.json'} | {'packet/' + e['path'] for e in author['files']},
        'audit-packet.zip': {'AUDIT_MANIFEST.json'} | {e['path'] for e in audit['audit_files']},
    }
    for name, members in archives.items():
        with zipfile.ZipFile(root / name) as z:
            require(set(z.namelist()) == members and len(z.infolist()) == len(members),
                    'Unexpected or duplicate archive entry: ' + name)
            for info in z.infolist():
                require(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16),
                        'Nonregular archive entry')
                require(z.read(info.filename) == (root / info.filename).read_bytes(),
                        'Archive/file mismatch: ' + info.filename)
    author_check = subprocess.check_output([sys.executable, '-B', str(root / 'packet/verify_manifest.py')])
    replay = subprocess.check_output([sys.executable, '-B', str(root / 'audit/verify_audit.py'),
                                     '--author-root', str(root)])
    result = {'problem_id': 30000510, 'status': 'already_solved', 'turns': '1/5',
              'files_verified': len(entries), 'archives_exact': True,
              'assertions_enabled': True, 'author_manifest': json.loads(author_check),
              'replay': json.loads(replay), 'passed': True}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

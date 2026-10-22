"""Strict inventory and complete isolated arithmetic replay. No general proof claim."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def main():
    root = Path(__file__).absolute().parent
    require(not root.is_symlink(), 'Symlink package root')
    manifest_path = root / 'MANIFEST.json'
    require(not manifest_path.is_symlink() and manifest_path.is_file(), 'Unsafe root manifest')
    manifest = json.loads(manifest_path.read_text(), object_pairs_hook=unique_object)
    require(set(manifest) == {'schema', 'files'}, 'Unexpected manifest fields')
    require(manifest['schema'] == 1 and type(manifest['files']) is dict, 'Invalid manifest schema')
    files = manifest['files']
    expected_dirs = set()
    for name, record in files.items():
        p = PurePosixPath(name)
        require(type(name) is str and name and '\\' not in name and '\x00' not in name and not p.is_absolute() and str(p) == name and all(part not in ('', '.', '..') for part in name.split('/')), 'Unsafe inventory path')
        require(name != 'MANIFEST.json', 'Manifest must not inventory itself')
        require(type(record) is dict and set(record) == {'bytes', 'sha256'}, 'Invalid file record')
        require(type(record['bytes']) is int and record['bytes'] >= 0, 'Invalid byte count')
        require(type(record['sha256']) is str and len(record['sha256']) == 64 and all(c in '0123456789abcdef' for c in record['sha256']), 'Invalid hash')
        expected_dirs.update(str(parent) for parent in p.parents if str(parent) != '.')
    actual_files = set()
    actual_dirs = set()
    for current, dirs, names in os.walk(root, followlinks=False):
        for name in dirs + names:
            path = Path(current) / name
            require(not path.is_symlink(), 'Symlink found')
            relative = path.relative_to(root).as_posix()
            if path.is_dir():
                actual_dirs.add(relative)
            else:
                require(path.is_file(), 'Nonregular inventory entry')
                if relative != 'MANIFEST.json':
                    actual_files.add(relative)
    require(actual_files == set(files), 'Recursive file inventory mismatch')
    require(actual_dirs == expected_dirs, 'Recursive directory inventory mismatch')
    for name, record in files.items():
        raw = (root / name).read_bytes()
        require(len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256'], 'Hash/size mismatch: ' + name)
    require({'checks.py', 'EXACT_CHECKS.json', 'EXPECTED_STDOUT.txt', 'verify.py'} <= set(files), 'Required verification artifacts missing')
    for optimized in (False, True):
        with tempfile.TemporaryDirectory() as temporary:
            tmp = Path(temporary)
            (tmp / 'checks.py').write_bytes((root / 'checks.py').read_bytes())
            command = [sys.executable] + (['-O'] if optimized else []) + [str(tmp / 'checks.py')]
            result = subprocess.run(command, capture_output=True, timeout=30, cwd=tmp)
            require(result.returncode == 0, 'Arithmetic replay failed')
            require(result.stderr == b'', 'Unexpected arithmetic stderr')
            require(result.stdout == (root / 'EXPECTED_STDOUT.txt').read_bytes(), 'Complete stdout mismatch')
            require((tmp / 'EXACT_CHECKS.json').read_bytes() == (root / 'EXACT_CHECKS.json').read_bytes(), 'Complete JSON replay mismatch')
    print('PASS: recursive inventory, SHA-256/size checks, complete normal/-O stdout and JSON replay')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)

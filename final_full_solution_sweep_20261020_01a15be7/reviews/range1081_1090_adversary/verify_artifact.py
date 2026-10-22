#!/usr/bin/env python3
"""Strict read-only offline identities; not a theorem or completeness certificate."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def regular(path):
    for part in [path, *path.parents]:
        require(not part.is_symlink(), 'symlink input: ' + str(path))
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode), 'nonregular input')
    return path.read_bytes()


def pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def read_json(path):
    return json.loads(regular(path).decode('utf-8'), object_pairs_hook=pairs)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_rows(rows):
    require(type(rows) is list, 'pin rows type')
    names = []
    for row in rows:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'pin schema')
        name = row['path']
        require(type(name) is str and name, 'pin name type')
        path = PurePosixPath(name)
        require(str(path) == name and not path.is_absolute() and '..' not in path.parts
                and '\\' not in name, 'unsafe pin path')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'pin byte count')
        require(type(row['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}', row['sha256']),
                'pin digest type')
        body = regular(ROOT / name)
        require(len(body) == row['bytes'] and digest(body) == row['sha256'], 'changed: ' + name)
        names.append(name)
    require(names == sorted(set(names)), 'pins not sorted unique')
    return set(names)


def main():
    wire = regular(ROOT / 'OUTPUT_MANIFEST.json')
    require(regular(ROOT / 'OUTPUT_MANIFEST.sha256').decode() == digest(wire) + '\n',
            'public manifest seal')
    manifest = read_json(ROOT / 'OUTPUT_MANIFEST.json')
    require(manifest['schema_version'] == 1 and type(manifest['schema_version']) is int,
            'schema version')
    public = check_rows(manifest['public_files'])
    require(public == {'.gitignore', 'REVIEW.md', 'CHECK_RESULTS.json', 'RESEARCH_LOG.md',
                       'verify_artifact.py'}, 'exact public membership')
    private_pin = manifest['private_manifest']
    require(private_pin['path'] == 'private/PRIVATE_MANIFEST.json', 'private manifest locator')
    check_rows([private_pin])
    private = read_json(ROOT / private_pin['path'])
    require(private['schema_version'] == 1 and type(private['schema_version']) is int,
            'private schema')
    expected = check_rows(private['files'])
    require(all(name.startswith('private/') for name in expected), 'private namespace')
    actual_files, actual_dirs = set(), set()
    for path in (ROOT / 'private').rglob('*'):
        require(not path.is_symlink(), 'private symlink')
        name = path.relative_to(ROOT).as_posix()
        if path.is_dir():
            actual_dirs.add(name)
        else:
            regular(path)
            actual_files.add(name)
    require(actual_files == expected | {private_pin['path']}, 'closed private files')
    require(type(private['directories']) is list and private['directories'] == sorted(actual_dirs),
            'closed private directories')
    require({p.name for p in ROOT.iterdir()} == public |
            {'OUTPUT_MANIFEST.json', 'OUTPUT_MANIFEST.sha256', 'private'}, 'closed public directory')
    print(json.dumps({'status': 'PASS', 'public_payload_files': len(public),
                      'private_payload_files': len(expected),
                      'scope': 'Offline byte identities and closed inventories only; no mathematics, priority, authorship, provider-state or global-sweep certificate'}, sort_keys=True))


if __name__ == '__main__':
    main()

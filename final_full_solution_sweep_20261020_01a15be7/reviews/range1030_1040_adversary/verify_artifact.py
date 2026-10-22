#!/usr/bin/env python3
"""Read-only offline PR1030–1040 review inventory verifier; imports no evidence."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import stat
import sys

ROOT = Path(__file__).resolve().parent

def need(condition, message):
    if not condition:
        raise ValueError(message)

def object_unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def reject_number(value):
    raise ValueError('nonfinite or fractional manifest number')

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=object_unique,
                      parse_constant=reject_number, parse_float=reject_number)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def file_regular(path):
    need(not path.is_symlink(), 'symlink file')
    need(stat.S_ISREG(path.lstat().st_mode), 'nonregular file')

def directory_regular(path):
    need(not path.is_symlink() and path.is_dir(), 'invalid directory')

def safe_name(name):
    need(type(name) is str and bool(name) and '\\' not in name and '\x00' not in name,
         'unsafe path type')
    p = PurePosixPath(name)
    need(not p.is_absolute() and str(p) == name and
         all(x not in ('', '.', '..') for x in name.split('/')), 'unsafe path')
    return name

def digest_name(value):
    need(type(value) is str and re.fullmatch(r'[0-9a-f]{64}', value) is not None,
         'invalid digest')

def sealed_json(folder, name):
    path = folder/name
    seal = folder/name.replace('.json', '.sha256')
    file_regular(path)
    file_regular(seal)
    need(seal.read_bytes() == (sha(path.read_bytes()) + '  ' + name + '\n').encode(),
         'manifest seal differs')
    return read_json(path)

def entries(folder, rows):
    need(type(rows) is list, 'invalid file list')
    names = []
    for row in rows:
        need(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'invalid row')
        name = safe_name(row['path'])
        need(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid byte count')
        digest_name(row['sha256'])
        names.append(name)
        path = folder
        for part in PurePosixPath(name).parts[:-1]:
            path = path/part
            directory_regular(path)
        path = folder/name
        file_regular(path)
        body = path.read_bytes()
        need(len(body) == row['bytes'] and sha(body) == row['sha256'], 'file bytes differ')
    need(names == sorted(set(names)), 'duplicate or unsorted file names')
    return set(names)

def observed_tree(folder):
    directory_regular(folder)
    files, dirs = set(), set()
    for base, child_dirs, child_files in os.walk(folder, followlinks=False):
        for name in child_dirs:
            path = Path(base)/name
            directory_regular(path)
            dirs.add(str(path.relative_to(folder)))
        for name in child_files:
            path = Path(base)/name
            file_regular(path)
            files.add(str(path.relative_to(folder)))
    return files, dirs

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private', action='store_true')
    args = parser.parse_args()
    need(not Path(__file__).is_symlink(), 'verifier symlink')
    manifest = sealed_json(ROOT, 'OUTPUT_MANIFEST.json')
    need(type(manifest) is dict and set(manifest) == {
        'schema', 'created_utc', 'scope', 'files', 'private_manifest_sha256'}, 'public schema')
    need(type(manifest['schema']) is int and manifest['schema'] == 1, 'public version')
    need(type(manifest['created_utc']) is str and type(manifest['scope']) is str, 'public metadata')
    digest_name(manifest['private_manifest_sha256'])
    public = entries(ROOT, manifest['files'])
    need(all('/' not in n for n in public), 'public path must be top level')
    observed = {x.name for x in ROOT.iterdir()}
    allowed = public | {'OUTPUT_MANIFEST.json', 'OUTPUT_MANIFEST.sha256'}
    if 'private' in observed:
        directory_regular(ROOT/'private')
        allowed.add('private')
    need(observed == allowed, 'public tree not closed')
    count = None
    if args.private:
        folder = ROOT/'private'
        directory_regular(folder)
        private = sealed_json(folder, 'PRIVATE_MANIFEST.json')
        need(sha((folder/'PRIVATE_MANIFEST.json').read_bytes()) == manifest['private_manifest_sha256'],
             'private anchor differs')
        need(type(private) is dict and set(private) == {'schema', 'files', 'directories'}, 'private schema')
        need(type(private['schema']) is int and private['schema'] == 1, 'private version')
        names = entries(folder, private['files'])
        dirs = private['directories']
        need(type(dirs) is list and all(type(x) is str for x in dirs), 'directory list')
        need(dirs == sorted(set(dirs)), 'duplicate or unsorted directory list')
        for name in dirs:
            safe_name(name)
        found_files, found_dirs = observed_tree(folder)
        need(found_files == names | {'PRIVATE_MANIFEST.json', 'PRIVATE_MANIFEST.sha256'},
             'private files not closed')
        need(found_dirs == set(dirs), 'private directories not closed')
        count = len(names)
    print(json.dumps({'status': 'PASS', 'public_payload_files': len(public),
                      'private_payload_files': count,
                      'scope': 'Offline byte identities and closed inventories only; no mathematical, originality, authorship, live-provider or global-sweep certification'}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status': 'FAIL', 'reason': str(error)}, sort_keys=True))
        sys.exit(1)

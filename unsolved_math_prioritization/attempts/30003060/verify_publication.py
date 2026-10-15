#!/usr/bin/env python3
"""Closed portable evidence checks; arithmetic and integrity do not prove analysis."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def bind(root, pin):
    require(stat.S_ISDIR(root.lstat().st_mode), 'regular root directory')
    manifest = root / 'PUBLICATION_MANIFEST.json'
    require(stat.S_ISREG(manifest.lstat().st_mode), 'regular index')
    require(hashlib.sha256(manifest.read_bytes()).hexdigest() == pin, 'external index pin')
    data = load(manifest)
    require(data['schema'] == 'higher-koszul-current-publication-v1' and data['problem_id'] == 30003060,
            'package identity')
    names = [row['path'] for row in data['files']]
    require(len(names) == len(set(names)), 'unique inventory')
    require(all(type(n) is str and n == str(PurePosixPath(n)) and n not in ('', '.', 'PUBLICATION_MANIFEST.json')
                and not n.startswith('/') and '..' not in PurePosixPath(n).parts and '\\' not in n
                for n in names), 'safe paths')
    expected_dirs = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    files, dirs = set(), set()
    for path in root.rglob('*'):
        mode = path.lstat().st_mode
        name = path.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            files.add(name)
        elif stat.S_ISDIR(mode):
            dirs.add(name)
        else:
            raise RuntimeError('nonregular member: ' + name)
    require(files == set(names) | {'PUBLICATION_MANIFEST.json'} and dirs == expected_dirs, 'closed inventory')
    for row in data['files']:
        raw = (root / row['path']).read_bytes()
        require(type(row['bytes']) is int and len(raw) == row['bytes'], 'byte count: ' + row['path'])
        require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'digest: ' + row['path'])
    return len(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trusted_outer_sha256')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,
            'run with python -I -S -B')
    root = Path(__file__).absolute().parent
    count = bind(root, args.trusted_outer_sha256)
    pre = root / 'publication_20261014/preprint'
    inner = root / 'publication_20261014/verification_package'
    metadata = load(pre / 'metadata.json')
    require(metadata == load(pre / 'zenodo-deposit.json')['metadata']
            == load(inner / 'metadata.json') == load(root / 'PUBLICATION_METADATA.json')['zenodo_metadata'],
            'exact current metadata equality')
    require((pre / 'output/pdf/note.pdf').read_bytes() == (inner / 'note.pdf').read_bytes(),
            'PDF identity')
    for name in ['README.md','note.tex','CURRENT_PRIORITY.md','verify_package.py','build_verification.py','package_index.json']:
        require((pre / name).read_bytes() == (inner / name).read_bytes(), 'preprint/portable identity: ' + name)
    import zipfile
    inner_files = {p.relative_to(inner).as_posix():p for p in inner.rglob('*') if p.is_file()}
    require(len(inner_files) == 140, 'portable member count')
    with zipfile.ZipFile(pre / 'verification.zip') as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and set(names) == set(inner_files), 'archive closed inventory')
        for entry in archive.infolist():
            require(stat.S_ISREG(entry.external_attr >> 16), 'archive regular member')
            require(archive.read(entry) == inner_files[entry.filename].read_bytes(), 'archive member identity')
    original = load(inner / 'root_evidence/SOURCE_MANIFEST.json')
    require(original['frozen_head'] == '286cc67c0727b4decfd4f261a0591cd8823ebce9'
            and len(original['files']) == 65, 'original source identity')
    mutable = {'README.md','RESEARCH_LOG.md','verify_publication.py','PACKAGE_MANIFEST.json'}
    for row in original['files']:
        raw = (inner / 'source' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
                'frozen original source digest')
        if row['path'] not in mutable:
            require((root / row['path']).read_bytes() == raw, 'legacy current bytes differ')
    index_pin = hashlib.sha256((inner / 'package_index.json').read_bytes()).hexdigest()
    flags = ['-I','-S','-B'] + (['-O'] if sys.flags.optimize else [])
    command = [sys.executable,*flags,str(inner / 'verify_package.py'),index_pin]
    if args.full:
        command.append('--full')
    result = subprocess.run(command,cwd='/',capture_output=True,text=True,timeout=1200)
    require(result.returncode == 0 and not result.stderr, 'portable verification: ' + result.stderr)
    checked = json.loads(result.stdout,object_pairs_hook=unique)
    require(checked['regular_files'] == 140 and checked['status'] == 'PASS', 'portable result')
    bind(root,args.trusted_outer_sha256)
    print(json.dumps({'status':'PASS','regular_files':count,'archive_members_verified':140,
                      'original_files_preserved':65,'current_legacy_files_unchanged':61,
                      'inner':checked,'unlimited_proof_certified_by_program':False,
                      'priority_certified_by_program':False},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()

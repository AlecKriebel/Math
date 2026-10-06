#!/usr/bin/env python3
"""Bind publication bytes before executing reviewed mathematical diagnostics."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile
import tempfile
import shutil


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def bind(root, trusted):
    need(stat.S_ISDIR(root.lstat().st_mode), 'root directory')
    manifest = root / 'PUBLICATION_MANIFEST.json'
    need(stat.S_ISREG(manifest.lstat().st_mode), 'manifest regular')
    raw = manifest.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == trusted, 'trusted manifest hash')
    data = json.loads(raw)
    need(data['format'] == 'k-sheets-30001460-publication-v1', 'format')
    files = data['files']
    names = [x['path'] for x in files]
    need(len(names) == len(set(names)), 'duplicate entries')
    need(all(isinstance(n, str) and n == str(PurePosixPath(n)) and not n.startswith('/')
             and '..' not in PurePosixPath(n).parts and '\\' not in n
             and n not in ('', '.', 'PUBLICATION_MANIFEST.json') for n in names), 'safe paths')
    directories = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        mode = p.lstat().st_mode
        name = p.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            actual_files.add(name)
        elif stat.S_ISDIR(mode):
            actual_dirs.add(name)
        else:
            raise RuntimeError('nonregular entry ' + name)
    need(actual_files == set(names) | {'PUBLICATION_MANIFEST.json'}, 'strict file inventory')
    need(actual_dirs == directories, 'strict directory inventory')
    for item in files:
        payload = (root / item['path']).read_bytes()
        need(len(payload) == item['bytes'] and hashlib.sha256(payload).hexdigest() == item['sha256'],
             'bytes ' + item['path'])
    metadata = json.loads((root / 'PUBLICATION_METADATA.json').read_text())
    for a in metadata['archives']:
        payload = (root / a['path']).read_bytes()
        need(len(payload) == a['bytes'] and hashlib.sha256(payload).hexdigest() == a['sha256'], 'archive pin')
        directory = root / a['role']
        need(hashlib.sha256((directory / 'MANIFEST.json').read_bytes()).hexdigest() == a['manifest_sha256'], 'inner manifest pin')
        with zipfile.ZipFile(root / a['path']) as z:
            members = z.infolist()
            need(len({i.filename for i in members}) == len(members), 'duplicate ZIP member')
            need(all(stat.S_ISREG(i.external_attr >> 16) and not i.is_dir() and PurePosixPath(i.filename).name == i.filename for i in members), 'flat regular ZIP')
            need({i.filename for i in members} == {x.name for x in directory.iterdir()}, 'ZIP inventory')
            for i in members:
                need(z.read(i) == (directory / i.filename).read_bytes(), 'ZIP member bytes')
    return {'status': 'PASS_PUBLICATION_INVENTORY', 'files': len(files) + 1,
            'archive_member_equivalence': True}


def full(root):
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    def run(path, *args):
        result = subprocess.run([sys.executable, *flags, str(root / path), *map(str, args)],
                                cwd='/', capture_output=True, text=True, timeout=120)
        need(result.returncode == 0 and not result.stderr, path + ': ' + result.stderr)
        return json.loads(result.stdout)
    author = run('author/verify.py')
    audit = run('audit/verify_audit.py')
    need(author['verified'] is True and author['identities_passed'] == 23, 'author identities')
    need(audit['verified'] is True and audit['files'] == 13, 'audit inventory')
    independent = run('audit/mathematical_controls.py')
    need(independent == json.loads((root / 'audit/MATH_RESULTS.json').read_text()), 'independent output')
    mutations = run('audit/independent_replay.py', '--author-archive', root / 'archives/K_SHEETS_30001460_AUTHOR_SAFE_FREEZE.zip')
    need(mutations == json.loads((root / 'audit/REPLAY_RESULTS.json').read_text()), 'mutation output')
    original = (root / 'author/RESULT.md').read_bytes()
    old = b'with no orbit-separating morphism'
    new = b'with no K-invariant orbit-separating morphism'
    need(original.count(old) == 1, 'exact clarification source')
    with tempfile.TemporaryDirectory(prefix='K sheet actual patch ') as temp:
        copy = Path(temp) / 'author copy'
        shutil.copytree(root / 'author', copy)
        result = subprocess.run(['patch', '--batch', '--forward', '--fuzz=0', '-p1', '-d', str(copy),
                                 '-i', str(root / 'audit/CLARIFICATION.patch')],
                                capture_output=True, text=True, timeout=30)
        need(result.returncode == 0 and not result.stderr and 'fuzz' not in result.stdout.lower(),
             'actual clarification patch: ' + result.stdout + result.stderr)
        need((copy / 'RESULT.md').read_bytes() == original.replace(old, new), 'exact clarification output')
        need({x.name for x in copy.iterdir()} == {x.name for x in (root / 'author').iterdir()}, 'patch inventory')
        for x in (root / 'author').iterdir():
            if x.name != 'RESULT.md':
                need((copy / x.name).read_bytes() == x.read_bytes(), 'patch changed another file')
    need((root / 'author/RESULT.md').read_bytes() == original, 'frozen proof unchanged')
    return {'author_identities': author['identities_passed'],
            'independent_identities': independent['identities_passed'],
            'mathematical_countercontrols': independent['negative_count'],
            'author_positive_controls': mutations['positive_count'],
            'author_mutations_rejected': mutations['negative_count'],
            'all_expected_json_matches': True,
            'actual_clarification_patch_applied_and_exact': True,
            'historical_freezes_unchanged': True,
            'finite_controls_are_descent_proof': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trusted_manifest_sha256')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    result = bind(root, args.trusted_manifest_sha256)
    if args.full:
        result['full'] = full(root)
        bind(root, args.trusted_manifest_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

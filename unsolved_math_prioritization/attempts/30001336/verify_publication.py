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


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def bind(root, trusted):
    manifest = root / 'PUBLICATION_MANIFEST.json'
    need(stat.S_ISREG(manifest.lstat().st_mode), 'manifest regular')
    raw = manifest.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == trusted, 'trusted manifest hash')
    data = json.loads(raw)
    need(data['format'] == 'rooted-tree-30001336-publication-v1', 'format')
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
            need(all(not i.is_dir() and PurePosixPath(i.filename).name == i.filename for i in members), 'flat ZIP')
            need({i.filename for i in members} == {x.name for x in directory.iterdir()}, 'ZIP inventory')
            for i in members:
                need(z.read(i) == (directory / i.filename).read_bytes(), 'ZIP member bytes')
    return {'status': 'PASS_PUBLICATION_INVENTORY', 'files': len(files) + 1,
            'archive_member_equivalence': True}


def full(root):
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    def run(path, *args):
        result = subprocess.run([sys.executable, *flags, str(root / path), *map(str, args)],
                                cwd='/', capture_output=True, text=True, timeout=600)
        need(result.returncode == 0, path + ': ' + result.stderr)
        return json.loads(result.stdout)
    run('author/verify_packet.py')
    run('audit/verify_bundle.py')
    author = run('author/verify_math.py')
    need(author == json.loads((root / 'author/expected_results.json').read_text()), 'author output')
    independent = run('audit/independent_checks.py')
    need(independent == json.loads((root / 'audit/INDEPENDENT_RESULTS.json').read_text()), 'independent output')
    mutations = run('audit/replay_author.py', root / 'archives/ROOTED_TREE_30001336_AUTHOR_SAFE_FREEZE.zip')
    need(mutations == json.loads((root / 'audit/REPLAY_AND_MUTATION_RESULTS.json').read_text()), 'mutation output')
    return {'author_checks': sum(author['assertions_by_family'].values()),
            'independent_checks': independent['checks'],
            'author_replay_and_mutation_controls': len(mutations['controls']),
            'all_expected_json_matches': True}


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

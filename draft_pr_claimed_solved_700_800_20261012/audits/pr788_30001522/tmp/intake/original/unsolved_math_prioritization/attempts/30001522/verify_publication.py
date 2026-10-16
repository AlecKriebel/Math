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
    need(stat.S_ISDIR(root.lstat().st_mode), 'root directory')
    manifest = root / 'PUBLICATION_MANIFEST.json'
    need(stat.S_ISREG(manifest.lstat().st_mode), 'manifest regular')
    raw = manifest.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == trusted, 'trusted manifest hash')
    data = json.loads(raw)
    need(data['format'] == 'free-p-toral-30001522-publication-v1', 'format')
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
    need(metadata['problem_id'] == 30001522 and metadata['catalog_rank'] == 828, 'identity')
    need(metadata['status'] == 'claimed_solved' and metadata['turns'] == '2/5', 'queue outcome')
    need(metadata['novelty_certified'] is False and metadata['current_open_status_certified'] is False, 'scope limits')
    for role, rank_key in [('audit', 'free_p_rank_for_every_odd_prime'), ('second_review', 'free_p_rank_every_odd_prime')]:
        accepted = json.loads((root / role / 'ACCEPTANCE.json').read_text())
        need(accepted['free_toral_rank'] == accepted['free_2_rank'] == 0 and accepted[rank_key] == 1, 'accepted ranks')
        need(accepted['mathematical_corrections_required'] == [] and accepted['novelty_certified'] is False, 'acceptance scope')
    need(json.loads((root / 'second_review/ACCEPTANCE.json').read_text())['full_corpora_reinspected'] is False, 'historical second-review scope')
    return {'status': 'PASS_PUBLICATION_INVENTORY', 'files': len(files) + 1,
            'archive_member_equivalence': True}


def full(root):
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    def run(path):
        result = subprocess.run([sys.executable, *flags, str(root / path)],
                                cwd='/', capture_output=True, text=True, timeout=600)
        need(result.returncode == 0 and not result.stderr, path + ': ' + result.stderr)
        output = json.loads(result.stdout)
        need(output['status'] == 'PASS', path + ' status')
        return output
    author = run('author/VERIFY.py')
    audit = run('audit/VERIFY_AUDIT.py')
    second = run('second_review/VERIFY.py')
    controls = {}
    for role, path in [('author', 'author/TEST_CONTROLS.py'),
                       ('audit', 'audit/TEST_AUDIT_PACKAGE.py'),
                       ('second_review', 'second_review/TEST_PACKAGE.py')]:
        result = run(path)
        controls[role] = result
    need(author['arithmetic'] == json.loads((root / 'author/EXPECTED_RESULTS.json').read_text()), 'author diagnostics')
    need(audit['independent_results'] == json.loads((root / 'audit/INDEPENDENT_RESULTS.json').read_text()), 'independent diagnostics')
    need(controls['author']['mutant_rejections'] == 28, 'author damage controls')
    need(controls['audit']['mutant_rejections'] == 40, 'audit damage controls')
    need(controls['second_review'] == json.loads((root / 'second_review/VERIFICATION_RESULTS.json').read_text()), 'second-review controls')
    return {'author': author, 'audit': audit, 'second_review': second,
            'controls': controls, 'all_recorded_diagnostics_match': True,
            'historical_freezes_unchanged': True,
            'formal_topology_verification': False,
            'source_documents_reauthenticated': False,
            'full_corpora_reinspected_by_this_command': False}


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

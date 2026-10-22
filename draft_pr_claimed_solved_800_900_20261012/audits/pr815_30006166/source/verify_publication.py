#!/usr/bin/env python3
"""Verify frozen publication bytes, then replay finite diagnostics only."""
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


def unique(pairs):
    result = {}
    for k, v in pairs:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result


def load(p):
    return json.loads(p.read_bytes(), object_pairs_hook=unique)


def bind(root, trusted):
    need(stat.S_ISDIR(root.lstat().st_mode), 'regular root directory')
    manifest = root / 'PUBLICATION_MANIFEST.json'
    need(stat.S_ISREG(manifest.lstat().st_mode), 'regular manifest')
    need(hashlib.sha256(manifest.read_bytes()).hexdigest() == trusted, 'trusted manifest hash')
    data = load(manifest)
    need(data['format'] == 'wreath-hyperfinite-30006166-publication-v1', 'format')
    files = data['files']
    names = [x['path'] for x in files]
    need(len(names) == len(set(names)), 'duplicate entries')
    need(all(type(n) is str and n == str(PurePosixPath(n)) and not n.startswith('/')
             and '..' not in PurePosixPath(n).parts and '\\' not in n
             and n not in ('', '.', 'PUBLICATION_MANIFEST.json') for n in names), 'safe paths')
    directories = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        mode = p.lstat().st_mode
        name = p.relative_to(root).as_posix()
        if stat.S_ISREG(mode): actual_files.add(name)
        elif stat.S_ISDIR(mode): actual_dirs.add(name)
        else: raise RuntimeError('nonregular entry ' + name)
    need(actual_files == set(names) | {'PUBLICATION_MANIFEST.json'}, 'strict file inventory')
    need(actual_dirs == directories, 'strict directory inventory')
    for item in files:
        raw = (root / item['path']).read_bytes()
        need(type(item['bytes']) is int and len(raw) == item['bytes']
             and hashlib.sha256(raw).hexdigest() == item['sha256'], 'bytes ' + item['path'])
    metadata = load(root / 'PUBLICATION_METADATA.json')
    members = 0
    for a in metadata['archives']:
        raw = (root / a['path']).read_bytes()
        need(len(raw) == a['bytes'] and hashlib.sha256(raw).hexdigest() == a['sha256'], 'archive pin')
        need(hashlib.sha256((root / a['manifest_path']).read_bytes()).hexdigest() == a['manifest_sha256'], 'inner manifest pin')
        with zipfile.ZipFile(root / a['path']) as z:
            entries = z.infolist()
            need(len(entries) == a['regular_members'] and len({i.filename for i in entries}) == len(entries), 'ZIP inventory')
            for i in entries:
                n = PurePosixPath(i.filename)
                need(not i.is_dir() and not n.is_absolute() and '..' not in n.parts
                     and str(n) == i.filename and stat.S_ISREG(i.external_attr >> 16), 'regular safe ZIP member')
                need(z.read(i) == (root / a['extract_root'] / i.filename).read_bytes(), 'ZIP member bytes')
            members += len(entries)
    for p in (root / 'author').iterdir():
        need(p.read_bytes() == (root / 'audit_bundle/author' / p.name).read_bytes(), 'duplicate author identity')
    return {'status': 'PASS_PUBLICATION_INVENTORY', 'files': len(files) + 1,
            'archive_members_verified': members, 'archive_member_equivalence': True}


def full(root):
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    def run(path, *args):
        result = subprocess.run([sys.executable, *flags, str(root / path), *map(str, args)],
                                cwd='/', capture_output=True, text=True, timeout=600)
        need(result.returncode == 0, path + ': ' + result.stderr)
        return json.loads(result.stdout)
    results = {}
    results['author'] = run('author/verify.py')
    need(results['author']['infinite_theorem_verified_by_program'] is False, 'author scope')
    results['audit'] = run('audit_bundle/audit/verify.py')
    need(results['audit']['independent_counted_diagnostics'] == 20525
         and results['audit']['infinite_theorem_verified_by_program'] is False, 'audit scope/count')
    results['review_2'] = run('independent_review_2/verify.py',
        '--author-proof', root / 'author/PROOF.md',
        '--author-manifest', root / 'author/MANIFEST.json',
        '--author-zip', root / 'archives/WREATH_HYPERFINITE_30006166_AUTHOR_SAFE_FREEZE.zip')
    need(results['review_2']['external_author_files_checked'] == ['manifest', 'proof', 'safe_archive'], 'external author binding')
    need(results['review_2']['certifies_infinite_theorem'] is False, 'review 2 scope')
    for role, directory, key, count in [
        ('author', 'author', 'mutation_rejections', 22),
        ('audit', 'audit_bundle/audit', 'mutation_rejections', 26),
        ('review_2', 'independent_review_2', 'tamper_rejections', 20)]:
        actual = run(directory + '/integrity_tests.py')
        need(actual == load(root / directory / 'INTEGRITY_RESULTS.json'), role + ' frozen integrity output')
        need(actual[key] == count, role + ' integrity count')
        results[role + '_integrity_rejections'] = count
    first = load(root / 'audit_bundle/audit/ACCEPTANCE.json')
    second = load(root / 'independent_review_2/ACCEPTANCE.json')
    need(first['verdict'] == 'accept_complete_affirmative_candidate', 'first acceptance')
    need(second['decision'] == 'accept_complete_affirmative_candidate_relative_to_verified_published_inputs'
         and second['required_mathematical_patch'] is False, 'second acceptance')
    results['all_frozen_integrity_outputs_match'] = True
    results['finite_diagnostics_certify_infinite_theorem'] = False
    return results


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

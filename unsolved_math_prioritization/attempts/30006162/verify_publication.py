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
    need(stat.S_ISDIR(root.lstat().st_mode), 'regular root directory')
    manifest = root / 'PUBLICATION_MANIFEST.json'
    need(stat.S_ISREG(manifest.lstat().st_mode), 'manifest regular')
    raw = manifest.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == trusted, 'trusted manifest hash')
    data = json.loads(raw)
    need(data['format'] == 'surface-generic-points-30006162-publication-v1', 'format')
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
                                cwd='/', capture_output=True, text=True, timeout=300)
        need(result.returncode == 0, path + ': ' + result.stderr)
        return json.loads(result.stdout)
    metadata = json.loads((root / 'PUBLICATION_METADATA.json').read_text())
    by_role = {a['role']: a for a in metadata['archives']}
    pins = {r: by_role[r]['manifest_sha256'] for r in ('author', 'audit')}
    author = run('author/verify.py', '--root', root / 'author', '--manifest-sha256', pins['author'])
    need(author['diagnostics'] == json.loads((root / 'author/EXPECTED_RESULTS.json').read_text()), 'author output')
    need(author['diagnostics']['exact_assertions'] == 2108, 'author count')
    audit = run('audit/verify_audit.py', '--root', root / 'audit', '--manifest-sha256', pins['audit'])
    need(audit['independent_results'] == json.loads((root / 'audit/INDEPENDENT_RESULTS.json').read_text()), 'audit output')
    need(audit['independent_results']['checks'] == 58588, 'audit count')
    author_controls = run('author/integrity_tests.py', '--root', root / 'author', '--manifest-sha256', pins['author'])
    need(author_controls == json.loads((root / 'author/INTEGRITY_RESULTS.json').read_text()), 'author controls')
    need(author_controls['mutations_rejected'] == 28, 'author control count')
    audit_controls = run('audit/integrity_tests.py', '--root', root / 'audit', '--manifest-sha256', pins['audit'])
    need(audit_controls == json.loads((root / 'audit/INTEGRITY_RESULTS.json').read_text()), 'audit controls')
    need(audit_controls['negative_controls'] == 36, 'audit control count')
    source_author = json.loads((root / 'author/SOURCES.json').read_text())
    source_audit = json.loads((root / 'audit/SOURCE_AUDIT.json').read_text())
    by_id = {s['id']: s for s in source_author['sources']}
    for source in source_audit['sources']:
        for key in ('pdf_bytes', 'pdf_sha256', 'url', 'title', 'retrieval_url', 'public_status'):
            if key in source:
                need(source[key] == by_id[source['id']][key], 'source metadata agreement')
        need(source['source_content_distributed'] is False, 'source distribution boundary')
    provenance = json.loads((root / 'author/DATA_PROVENANCE.json').read_text())
    provenance_audit = json.loads((root / 'audit/PROVENANCE_AUDIT.json').read_text())
    for key in ('datasets', 'statement_fingerprint', 'review_fingerprint', 'problem_id', 'problem_number', 'rank'):
        need(provenance[key] == provenance_audit[key], 'dataset metadata agreement')
    return {'author_diagnostics': 2108, 'independent_diagnostics': 58588,
            'author_integrity_controls': 28, 'independent_integrity_controls': 36,
            'source_and_dataset_metadata_agreement': True,
            'all_frozen_expected_json_matches': True,
            'both_target_answers': 'unresolved', 'finite_controls_only': True}


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

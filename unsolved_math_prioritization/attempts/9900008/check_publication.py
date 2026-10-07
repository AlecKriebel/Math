#!/usr/bin/env python3
"""Distribution integrity and supplementary replay; not a mathematical proof."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVES = {
    'DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip': ('author', 18611, 'bd2a43c1d0de12ea87ba217b3b5316a00e008d1b547992d7bdd038ff695aed9b'),
    'DIFFUSE_MASS_9900008_FRESH_REVIEW_ACCEPTED_SAFE.zip': ('review2', 15301, 'ac46400397200608b0b608908a29f8b3917347e32b0a77f5a14496c10cc197cc'),
}
MODES = [[], ['-O'], ['-I'], ['-I', '-O']]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def check_binding(path, row):
    data = path.read_bytes()
    need(len(data) == row['bytes'], 'byte count mismatch: ' + path.name)
    need(sha(data) == row['sha256'], 'digest mismatch: ' + path.name)

def integrity(root):
    manifest = json.loads((root / 'PUBLICATION_MANIFEST.json').read_text())
    need(set(manifest) == {'schema', 'files'}, 'manifest schema keys')
    need(manifest['schema'] == 'diffuse-9900008-publication-manifest-v1', 'manifest schema')
    names = set()
    for row in manifest['files']:
        need(set(row) == {'path', 'bytes', 'sha256'}, 'manifest row keys')
        name = row['path']
        need(isinstance(name, str) and name not in names, 'duplicate or invalid path')
        need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe path')
        need(not (root / name).is_symlink(), 'symlink payload')
        names.add(name)
        check_binding(root / name, row)
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual == names | {'PUBLICATION_MANIFEST.json'}, 'unmanifested or missing payload')
    archive_results = []
    for name, (directory, size, digest) in ARCHIVES.items():
        path = root / 'archives' / name
        check_binding(path, {'bytes': size, 'sha256': digest})
        with zipfile.ZipFile(path) as z:
            members = z.namelist()
            expected = {p.name for p in (root / directory).iterdir() if p.is_file()}
            need(len(members) == len(set(members)) and set(members) == expected, 'archive membership mismatch')
            for member in members:
                need(member == Path(member).name, 'unsafe archive member')
                need(z.read(member) == (root / directory / member).read_bytes(), 'archive member bytes mismatch')
        archive_results.append({'archive': name, 'members': len(members), 'byte_exact': True})
    for directory, filename in [('author', 'MANIFEST.json'), ('review2', 'REVIEW_MANIFEST.json')]:
        inner = json.loads((root / directory / filename).read_text())
        for row in inner['files']:
            check_binding(root / directory / row['path'], row)
        need({p.name for p in (root / directory).iterdir() if p.is_file()} == {r['path'] for r in inner['files']} | {filename}, 'inner manifest membership mismatch')
    acceptance = json.loads((root / 'review2/ACCEPTANCE.json').read_text())
    need(acceptance['decision'] == 'ACCEPTED_WITH_REQUIRED_SOURCE_CREDIT_ADDENDUM', 'acceptance decision')
    need(acceptance['mathematical_verdict'] == 'PASS' and acceptance['mathematical_repair_required'] is False, 'acceptance scope')
    for key, location in [
        ('frozen_author_archive', 'archives/DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip'),
        ('accepted_unchanged_proof', 'author/PROOF.md'),
        ('reviewed_original_source_audit', 'author/SOURCE_AUDIT.md'),
        ('acceptance_report', 'review2/AUDIT.md'),
        ('required_credit_addendum', 'CREDIT_ADDENDUM.md'),
        ('verification_metadata', 'review2/REVIEW_METADATA.json'),
    ]:
        check_binding(root / location, acceptance[key])
    need((root / 'CREDIT_ADDENDUM.md').read_bytes() == (root / 'review2/CREDIT_ADDENDUM.md').read_bytes(), 'credit copies differ')
    return {'status': 'pass', 'manifested_files': len(names), 'archives': archive_results, 'exact_acceptance_bindings': True}

def replay(root):
    results = []
    for flags in MODES:
        for argument in ['--self-test', '--integrity']:
            p = subprocess.run([sys.executable] + flags + [str(root / 'author/verify.py'), argument], cwd=str(root.parent), capture_output=True)
            need(p.returncode == 0, 'author checker replay failed')
            result = json.loads(p.stdout)
            need(result['status'] == 'pass', 'author checker did not pass')
            if argument == '--self-test':
                controls = result['self_test']['negative_controls']
                need(len(controls) == 18 and all(row['rejected'] for row in controls), 'author negative controls')
            results.append({'flags': flags, 'argument': argument, 'exit_code': p.returncode, 'stdout_sha256': sha(p.stdout)})
    return results

def self_test(root):
    outcomes = []
    changes = [
        ('author/PROOF.md', 'append'),
        ('CREDIT_ADDENDUM.md', 'append'),
        ('review2/ACCEPTANCE.json', 'append'),
        ('archives/DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip', 'append'),
        ('extra_payload.txt', 'extra'),
    ]
    with tempfile.TemporaryDirectory(prefix='diffuse_publication_') as temp:
        for index, (name, kind) in enumerate(changes):
            dest = Path(temp) / str(index)
            shutil.copytree(root, dest, copy_function=shutil.copyfile)
            path = dest / name
            path.write_bytes((path.read_bytes() if kind == 'append' else b'') + b'changed\n')
            try:
                integrity(dest)
            except (ValueError, OSError, zipfile.BadZipFile):
                outcomes.append({'mutation': name, 'rejected': True})
            else:
                raise ValueError('negative control accepted: ' + name)
    return outcomes

def main():
    need(sys.argv[1:] in ([], ['--self-test']), 'usage: check_publication.py [--self-test]')
    result = integrity(ROOT)
    result['author_replays'] = replay(ROOT)
    result['historical_executable_audit_replayed'] = False
    result['limits'] = ['Finite checks supplement the analytic proof.', 'No novelty, human-review, or formal-proof certification.', 'The omitted historical executable package is not replayable from this bundle.']
    if sys.argv[1:]:
        result['negative_controls'] = self_test(ROOT)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status': 'fail', 'error': str(exc)}), file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Authenticate this source-free package and replay finite symbolic checks.

Integrity checks are not signatures and do not establish mathematical truth.
Trust a separately verified Git commit or public manifest hash. SymPy 1.14.0 is
needed only for --run-checkers. Assertions in frozen reviewers' scripts are
compiled with optimize=0, even when this driver is run with python -O.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import warnings
import zipfile

ARCHIVE = 'ANTI_INVARIANT_30004549_R3_AUTHOR_PUBLICATION_PACKET.zip'
EXTERNAL = 'ANTI_INVARIANT_30004549_R3_AUTHOR_EXTERNAL_MANIFEST.json'
PINNED = {
    ARCHIVE: (10680, '1ba558617ecbd40e4117da22897137118568204852b009bb2c02c99ef2521fc4'),
    EXTERNAL: (1483, '23b49259d2a3e8938f940323ec69a7cc17737cb4a0636817c6ae238609ffceb4'),
    'author/R3_counterexample_candidate.md': (9997, '50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e'),
    'audit_a/INDEPENDENT_ACCEPTANCE_A.md': (10890, 'a4e8a88320d30cafe7fe5c95fa95f97fab999baa5dba1241c3e7919fb6b20988'),
    'audit_b/INDEPENDENT_ACCEPTANCE_REPORT.md': (12527, '05a1a99f0c825be6a623b0ad827008fb68a442f38f7908593bdef6ce4c612568'),
}
CHECKERS = [
    ('author/verification/check_deformation.py', 'author/verification/check_normal.json'),
    ('audit_a/check_algebra.py', 'audit_a/ALGEBRA_CHECK_OUTPUT.txt'),
    ('audit_b/check_local_algebra.py', 'audit_b/check_local_algebra_result.txt'),
]
SPECIAL = {'PUBLIC_MANIFEST.json', 'PUBLIC_MANIFEST.sha256'}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def safe_path(value):
    need(isinstance(value, str) and value != '', 'empty/non-string path')
    p = PurePosixPath(value)
    need(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts
         and '\\' not in value and str(p) == value, 'unsafe/noncanonical path')
    return value

def check_entries(entries, read):
    need(isinstance(entries, list), 'entries must be a list')
    paths = [safe_path(e['path']) for e in entries]
    need(len(paths) == len(set(paths)), 'duplicate manifest path')
    for e in entries:
        data = read(e['path'])
        need(len(data) == e['bytes'], 'size mismatch: ' + e['path'])
        need(sha256(data) == e['sha256'], 'SHA-256 mismatch: ' + e['path'])
        if 'git_blob_sha1' in e:
            need(git_blob(data) == e['git_blob_sha1'], 'Git blob mismatch: ' + e['path'])
    return set(paths)

def check_archive(data, entries):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        for name in names:
            safe_path(name)
        need(len(names) == len(set(names)), 'duplicate archive member')
        need(set(names) == {e['path'] for e in entries}, 'archive member set mismatch')
        check_entries(entries, archive.read)

def verify(root):
    root = Path(root)
    need(root.is_dir(), 'package directory missing')
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'symlink in package')
    raw = (root / 'PUBLIC_MANIFEST.json').read_bytes()
    sidecar = (root / 'PUBLIC_MANIFEST.sha256').read_text()
    need(sidecar == sha256(raw) + '  PUBLIC_MANIFEST.json\n', 'manifest sidecar mismatch')
    manifest = json.loads(raw)
    need(manifest['schema'] == 'anti-invariant-publication-v1', 'manifest schema')
    need(manifest['problem_id'] == 30004549 and manifest['author_turns'] == '4/5', 'identity/count')
    paths = check_entries(manifest['files'], lambda p: (root / p).read_bytes())
    need(not paths.intersection(SPECIAL), 'manifest cannot inventory its own envelope')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual == paths | SPECIAL, 'complete package file-set mismatch')
    for name, (size, digest) in PINNED.items():
        data = (root / name).read_bytes()
        need(len(data) == size and sha256(data) == digest, 'frozen acceptance pin: ' + name)
    ext = json.loads((root / EXTERNAL).read_bytes())
    need(ext['archive']['filename'] == ARCHIVE, 'archive identity')
    archive_data = (root / ARCHIVE).read_bytes()
    need(ext['archive']['bytes'] == len(archive_data) and ext['archive']['sha256'] == sha256(archive_data), 'external archive pin')
    check_archive(archive_data, ext['files'])
    check_entries(ext['files'], lambda p: (root / 'author' / p).read_bytes())
    author = json.loads((root / 'author/MANIFEST.json').read_bytes())
    check_entries(author['files'], lambda p: (root / 'author' / p).read_bytes())
    proof = (root / 'author/R3_counterexample_candidate.md').read_bytes()
    for label in ('audit_a', 'audit_b'):
        audit = json.loads((root / label / 'AUDIT_MANIFEST.json').read_bytes())
        entries = audit.get('files', audit.get('authored_artifacts'))
        for e in entries:
            name = safe_path(e.get('filename', e.get('name')))
            data = proof if name == 'R3_counterexample_candidate.md' else (root / label / name).read_bytes()
            need(len(data) == e['bytes'] and sha256(data) == e['sha256'], 'audit manifest pin: ' + name)
        if label == 'audit_b':
            need(audit['candidate']['bytes'] == len(proof) and audit['candidate']['sha256'] == sha256(proof), 'audit B acceptance binding')
    return {'result': 'pass', 'files': len(actual), 'frozen_proof_sha256': sha256(proof),
            'archive_members': len(ext['files'])}

def rewrite_manifest(root, mutate):
    p = root / 'PUBLIC_MANIFEST.json'
    doc = json.loads(p.read_bytes())
    mutate(doc)
    p.write_text(json.dumps(doc, indent=2) + '\n')
    (root / 'PUBLIC_MANIFEST.sha256').write_text(sha256(p.read_bytes()) + '  PUBLIC_MANIFEST.json\n')

def self_tests(root):
    passed = ['positive_exact_package']
    def reject(name, action):
        try:
            action()
        except (ValueError, KeyError, FileNotFoundError, zipfile.BadZipFile):
            passed.append(name)
        else:
            raise ValueError('negative test accepted: ' + name)
    def mutation(name, edit):
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp) / 'package'
            shutil.copytree(root, clone)
            edit(clone)
            reject(name, lambda: verify(clone))
    proof = 'author/R3_counterexample_candidate.md'
    mutation('reject_changed_proof', lambda p: (p / proof).write_bytes((p / proof).read_bytes() + b'\n'))
    mutation('reject_missing_audit', lambda p: (p / 'audit_a/INDEPENDENT_ACCEPTANCE_A.md').unlink())
    mutation('reject_extra_file', lambda p: (p / 'unlisted.txt').write_text('unexpected'))
    mutation('reject_wrong_size', lambda p: rewrite_manifest(p, lambda m: m['files'][0].update(bytes=0)))
    mutation('reject_wrong_sha256', lambda p: rewrite_manifest(p, lambda m: m['files'][0].update(sha256='0' * 64)))
    mutation('reject_wrong_git_blob', lambda p: rewrite_manifest(p, lambda m: m['files'][0].update(git_blob_sha1='0' * 40)))
    mutation('reject_traversal', lambda p: rewrite_manifest(p, lambda m: m['files'][0].update(path='../escape')))
    mutation('reject_duplicate_manifest_entry', lambda p: rewrite_manifest(p, lambda m: m['files'].append(m['files'][0])))
    mutation('reject_manifest_sidecar_change', lambda p: (p / 'PUBLIC_MANIFEST.sha256').write_text('0' * 64))
    def rebind(p):
        data = (p / proof).read_bytes() + b'\n'
        (p / proof).write_bytes(data)
        def edit(m):
            for e in m['files']:
                if e['path'] == proof:
                    e.update(bytes=len(data), sha256=sha256(data), git_blob_sha1=git_blob(data))
        rewrite_manifest(p, edit)
    mutation('reject_rebound_frozen_proof', rebind)
    mutation('reject_symlink', lambda p: (p / 'unlisted-link').symlink_to(p / proof))
    entries = json.loads((root / EXTERNAL).read_bytes())['files']
    with zipfile.ZipFile(root / ARCHIVE) as z:
        members = [(name, z.read(name)) for name in z.namelist()]
    def zipped(items):
        out = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(out, 'w') as z:
                for name, data in items:
                    z.writestr(name, data)
        return out.getvalue()
    for name, items in [
        ('reject_archive_missing_member', members[1:]),
        ('reject_archive_extra_member', members + [('extra.txt', b'x')]),
        ('reject_archive_traversal', members + [('../escape', b'x')]),
        ('reject_archive_duplicate_member', members + [members[0]]),
        ('reject_archive_changed_member', [(members[0][0], members[0][1] + b'x')] + members[1:]),
    ]:
        data = zipped(items)
        reject(name, lambda data=data: check_archive(data, entries))
    return passed

def replay_checkers(root):
    # The subprocess remains isolated from package-local modules in every mode.
    wrapper = "import sys; p=sys.argv[1]; exec(compile(open(p,'rb').read(),p,'exec',optimize=0),{'__name__':'__main__','__file__':p})"
    modes = [('normal', []), ('optimized', ['-O']), ('isolated', ['-I'])]
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory() as cwd:
        for name, expected in CHECKERS:
            for mode, flags in modes:
                verify(root)  # Authenticate before every execution.
                run = subprocess.run([sys.executable, *flags, '-c', wrapper, str(root / name)],
                                     cwd=cwd, env=env, capture_output=True, timeout=120)
                need(run.returncode == 0, 'checker failed: ' + name + ' / ' + mode)
                need(run.stdout == (root / expected).read_bytes(), 'checker output differs: ' + name + ' / ' + mode)
                need(not run.stderr, 'unexpected checker stderr: ' + name + ' / ' + mode)
                results.append({'checker': name, 'mode': mode, 'result': 'pass',
                                'stdout_sha256': sha256(run.stdout), 'assertions_enabled': True})
        guard = subprocess.run([sys.executable, '-O', '-c', "exec(compile('assert False', '<guard>', 'exec', optimize=0))"],
                               cwd=cwd, env=env, capture_output=True, timeout=10)
        need(guard.returncode != 0 and b'AssertionError' in guard.stderr, 'optimized assertion guard did not reject')
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--run-checkers', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    result = verify(root)
    if args.self_test:
        result['self_tests'] = self_tests(root)
    if args.run_checkers:
        result['checker_replays'] = replay_checkers(root)
        result['optimized_assertion_guard'] = 'rejected_false_assertion'
    result['limits'] = 'Byte integrity and finite local algebra only; not a global proof, formal verification, human peer review, or novelty certification.'
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

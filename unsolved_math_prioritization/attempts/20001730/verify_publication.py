#!/usr/bin/env python3
"""Optimization-safe publication integrity and portable replay gate.

All checks use runtime exceptions, never Python assert. No external packages.
The finite checks do not formally verify the continuous mathematical proof.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
PINS = {
    'author/MANIFEST.json': '13c0d3e846ff254a8d526574f12446517e56b4d6c6e8c27b1cd8c866af34a193',
    'author/CORRECTED_THEOREM.md': '77354e318baf41c5afc0d062b041fb7ca1a41b2380e2d8da78d058cfd342a93c',
    'audit/AUDIT_MANIFEST.json': 'fa86a4695d80ab85e11931a4508e338ee45ff96f93860e7a810a198ebeb94c39',
    'audit/audit_controls.py': 'fa49f04e174a602638a153ed189cd024fe161aa3ad52183c1fe9f03fb5f7f49b',
    'archives/Gibbs_Leaf_Conull_Correction_Reconstructed_20261005.zip': 'b982ce65c18016451e63bf1520662590a14106731a7150149ed237ec3847ef73',
    'archives/Gibbs_Leaf_Conull_Independent_Audit_20261005.zip': '1949e2b9416a79b90b1695346c20d5e6d34fe844c41d48c631b7fd940a16b3db',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    actual = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symbolic link rejected: ' + str(p))
        if p.is_file():
            actual.add(p.relative_to(root).as_posix())
        else:
            require(p.is_dir(), 'Nonregular entry rejected: ' + str(p))
    return actual


def verify_manifest(root, name, sidecar):
    data = (root / name).read_bytes()
    require((root / sidecar).read_text().split()[0] == sha(data), 'Manifest sidecar mismatch: ' + name)
    manifest = json.loads(data)
    listed = set()
    for entry in manifest['files']:
        path = entry['path']
        parts = PurePosixPath(path)
        require(path and not parts.is_absolute() and parts.as_posix() == path and all(p not in ('..', '.') for p in parts.parts), 'Unsafe path')
        require(path not in listed and path not in (name, sidecar), 'Duplicate or self-referential manifest path')
        listed.add(path)
        p = root / path
        require(not p.is_symlink() and p.is_file() and p.resolve().is_relative_to(root.resolve()), 'Unsafe or missing payload: ' + path)
        blob = p.read_bytes()
        require(len(blob) == entry['bytes'] and sha(blob) == entry['sha256'], 'Payload size/hash mismatch: ' + path)
    require(inventory(root) == listed | {name, sidecar}, 'Strict inventory mismatch: ' + name)
    return manifest


def verify_archive(root, archive_name, payload, prefix):
    archive = root / 'archives' / archive_name
    require((archive.with_name(archive.name + '.sha256')).read_text().split()[0] == sha(archive.read_bytes()), 'Archive sidecar mismatch')
    expected = {prefix + '/' + p for p in inventory(root / payload)}
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) and set(names) == expected, 'Archive inventory mismatch')
        for name in names:
            require(z.read(name) == (root / payload / name.removeprefix(prefix + '/')).read_bytes(), 'Archive byte mismatch: ' + name)


def integrity(root):
    inventory(root)
    for path, pin in PINS.items():
        require(sha((root / path).read_bytes()) == pin, 'Pinned artifact mismatch: ' + path)
    publication = verify_manifest(root, 'PUBLICATION_MANIFEST.json', 'PUBLICATION_MANIFEST.sha256')
    require(publication['bindings'] == PINS, 'Publication binding mismatch')
    author = verify_manifest(root / 'author', 'MANIFEST.json', 'MANIFEST.sha256')
    audit = verify_manifest(root / 'audit', 'AUDIT_MANIFEST.json', 'AUDIT_MANIFEST.sha256')
    require(audit['reviewed_release_manifest_sha256'] == PINS['author/MANIFEST.json'], 'Audit target mismatch')
    require(audit['reviewed_proof_sha256'] == PINS['author/CORRECTED_THEOREM.md'], 'Audit proof mismatch')
    require(author['original_problem_status'] == 'unsolved', 'Original status changed')
    require(author['historical_attempt_budget'] == '5/5_reported_not_replayed', 'Historical budget changed')
    verify_archive(root, 'Gibbs_Leaf_Conull_Correction_Reconstructed_20261005.zip', 'author', 'Gibbs_Leaf_Conull_Correction')
    verify_archive(root, 'Gibbs_Leaf_Conull_Independent_Audit_20261005.zip', 'audit', 'Gibbs_Leaf_Conull_Independent_Audit')
    return len(publication['files']) + 2


def clean_env():
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env.pop('PYTHONPATH', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, env=clean_env(), capture_output=True)


def replay(root):
    expected = (root / 'audit/AUDIT_REPLAY.json').read_bytes()
    for optimized in (False, True):
        cmd = [sys.executable, '-E'] + (['-O'] if optimized else [])
        cmd += [str(root / 'audit/audit_controls.py'), str(root / 'author'), str(root / 'archives/Gibbs_Leaf_Conull_Correction_Reconstructed_20261005.zip')]
        result = run(cmd, root)
        require(result.returncode == 0, 'Independent replay failed: ' + result.stderr.decode(errors='replace'))
        require(result.stdout == expected, 'Frozen audit receipt mismatch')
    receipt = json.loads(expected)
    require(receipt['independent_check_count'] == 1444 and receipt['original_finite_control_assertions'] == 4177, 'Finite check counts changed')
    require(receipt['release_verifier_accepts_modified_proof_under_python_O'] is True, 'Documented verifier caveat not reproduced')


def rewrite_manifest(root, edit):
    p = root / 'PUBLICATION_MANIFEST.json'
    data = json.loads(p.read_bytes())
    edit(data)
    blob = (json.dumps(data, indent=2, sort_keys=True) + '\n').encode()
    p.write_bytes(blob)
    (root / 'PUBLICATION_MANIFEST.sha256').write_text(sha(blob) + '  PUBLICATION_MANIFEST.json\n')


def negative_controls(root):
    mutations = ('proof_append', 'proof_same_size', 'missing_audit', 'unlisted_file', 'duplicate_entry', 'unsafe_path', 'changed_author_binding', 'changed_audit_binding', 'changed_receipt', 'payload_symlink', 'archive_changed')
    with tempfile.TemporaryDirectory(prefix='gibbs-publication-mutations-') as tmp:
        for mutation in mutations:
            dest = Path(tmp) / mutation
            shutil.copytree(root, dest)
            proof = dest / 'author/CORRECTED_THEOREM.md'
            if mutation == 'proof_append':
                proof.write_bytes(proof.read_bytes() + b'\nMutation\n')
            elif mutation == 'proof_same_size':
                data = bytearray(proof.read_bytes()); data[0] ^= 1; proof.write_bytes(data)
            elif mutation == 'missing_audit':
                (dest / 'audit/INDEPENDENT_AUDIT.md').unlink()
            elif mutation == 'unlisted_file':
                (dest / 'EXTRA.txt').write_text('Mutation')
            elif mutation == 'duplicate_entry':
                rewrite_manifest(dest, lambda x: x['files'].append(x['files'][0]))
            elif mutation == 'unsafe_path':
                rewrite_manifest(dest, lambda x: x['files'][0].update(path='../outside'))
            elif mutation == 'changed_author_binding':
                rewrite_manifest(dest, lambda x: x['bindings'].update({'author/MANIFEST.json': '0' * 64}))
            elif mutation == 'changed_audit_binding':
                rewrite_manifest(dest, lambda x: x['bindings'].update({'audit/AUDIT_MANIFEST.json': '0' * 64}))
            elif mutation == 'changed_receipt':
                p = dest / 'audit/AUDIT_REPLAY.json'; p.write_bytes(p.read_bytes() + b'\n')
            elif mutation == 'payload_symlink':
                p = dest / 'README.md'; p.unlink(); p.symlink_to(root / 'README.md')
            elif mutation == 'archive_changed':
                p = dest / 'archives/Gibbs_Leaf_Conull_Correction_Reconstructed_20261005.zip'; p.write_bytes(p.read_bytes() + b'Mutation')
            for optimized in (False, True):
                cmd = [sys.executable, '-E'] + (['-O'] if optimized else []) + [str(dest / 'verify_publication.py'), '--integrity-only']
                result = run(cmd, dest)
                require(result.returncode != 0, 'Mutation accepted: ' + mutation + (' under -O' if optimized else ''))
    return list(mutations)


def main():
    require(sys.argv[1:] in ([], ['--integrity-only']), 'Usage: python verify_publication.py [--integrity-only]')
    files = integrity(ROOT)
    if sys.argv[1:] == ['--integrity-only']:
        print('PASS_INTEGRITY_ONLY')
        return
    replay(ROOT)
    mutations = negative_controls(ROOT)
    integrity(ROOT)
    print(json.dumps({
        'status': 'PASS_PUBLICATION_GATE_WITH_DOCUMENTED_ORIGINAL_VERIFIER_CAVEAT',
        'publication_files': files,
        'publication_manifest_sha256': sha((ROOT / 'PUBLICATION_MANIFEST.json').read_bytes()),
        'bindings': PINS,
        'author_files': 11,
        'audit_files': 6,
        'archive_files_and_sidecars': 4,
        'original_finite_assertions': 4177,
        'independent_finite_checks': 1444,
        'normal_and_optimized_independent_receipts_match': True,
        'negative_controls_rejected_normal_and_optimized': mutations,
        'historical_attempt_budget': '5/5_reported_not_replayed',
        'original_problem_status': 'unsolved',
        'original_assertion_verifier_unsafe_under_optimization': True,
        'continuous_mathematics_formally_verified': False,
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

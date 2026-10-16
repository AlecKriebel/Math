#!/usr/bin/env python3
"""Check frozen bytes and replay finite controls without changing the package."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
PINS = {
    'author/AUTHOR_MANIFEST.json': 'd6a0862cbf2f6500cc5fd7ee2239e0e8a2c5864c9d09a6cd9a13b1b4f99176ef',
    'audit_a/AUDIT_MANIFEST.json': '75c4fdb635d14131759bc47d779c95079c719373d7f9305a649f9f60bf26bfc4',
    'audit_b/AUDIT_MANIFEST.json': '180bee30c70c810f8f92984fd4604ba7fdc25201ff2e579ed99f686935b1a6fd',
    'author/BOUNDED_REGION_PROOF.md': '2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def integrity(root):
    require(not any(p.is_symlink() for p in root.rglob('*')), 'Symlinks are not allowed')
    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text())
    require(manifest['self_excluded'] == 'PACKAGE_MANIFEST.json', 'Wrong self exclusion')
    expected = set(manifest['files']) | {'PACKAGE_MANIFEST.json'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(expected == actual, 'Unexpected or missing package files: ' + str(expected ^ actual))
    for name, record in manifest['files'].items():
        rel = Path(name)
        require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe manifest path')
        require(rel.suffix not in {'.pdf', '.html'}, 'Source documents are excluded')
        require(fingerprint(root / rel) == record, 'Changed bytes: ' + name)
    for name, digest in PINS.items():
        require(fingerprint(root / name)['sha256'] == digest, 'Changed accepted input: ' + name)
    require(fingerprint(root / 'author/BOUNDED_REGION_PROOF.md')['bytes'] == 12771, 'Wrong proof length')
    for folder, filename in [('author', 'AUTHOR_MANIFEST.json'), ('audit_a', 'AUDIT_MANIFEST.json'), ('audit_b', 'AUDIT_MANIFEST.json')]:
        base = root / folder
        frozen = json.loads((base / filename).read_text())
        require(set(frozen['files']) | {filename} == {p.name for p in base.iterdir() if p.is_file()}, 'Wrong frozen file set: ' + folder)
        for name, record in frozen['files'].items():
            require(fingerprint(base / name) == record, 'Changed frozen file: ' + folder + '/' + name)
    return {'status': 'pass', 'file_count': len(actual), 'accepted_proof_sha256': PINS['author/BOUNDED_REGION_PROOF.md']}


def replay(root):
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='fermion-v2-controls-') as tmp:
        work = Path(tmp) / 'package'
        shutil.copytree(root, work)
        commands = {
            'author': [sys.executable, 'author/verify.py'],
            'audit_a': [sys.executable, 'audit_a/independent_checks.py', '--proof', 'author/BOUNDED_REGION_PROOF.md'],
            'audit_b': [sys.executable, 'audit_b/independent_checks.py', '--author-dir', 'author'],
        }
        results = {}
        for label, command in commands.items():
            process = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=900)
            require(process.returncode == 0, label + ' failed: ' + process.stderr)
            results[label] = json.loads(process.stdout)
        require(results['author']['manifest'] == 'pass', 'Author integrity did not pass')
        require(results['audit_a']['status'] == 'PASS' and results['audit_a']['check_count'] == 5659, 'Audit A controls did not pass')
        require(results['audit_b']['input_integrity']['status'] == 'pass' and results['audit_b']['fock_controls']['status'] == 'pass' and results['audit_b']['scaling_and_polynomials']['status'] == 'pass', 'Audit B controls did not pass')
        return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    result = {'integrity': integrity(ROOT)}
    if not args.integrity_only:
        result['finite_controls'] = replay(ROOT)
        result['original_package_after_replay'] = integrity(ROOT)
    result['scope'] = 'Corruption and finite-control checks; not a replacement for the written proof and full audits.'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

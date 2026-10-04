#!/usr/bin/env python3
"""Validate the safe publication layout and exact mathematical replays.

Run with --self-test to reject four deliberately corrupted copies.
Requires Python standard library only. Does not verify topology or novelty.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
AUTHOR = '4f6575af14a3e8b72e61202c45e411b4febcaa7770c3e7e8af45576eda6218f8'
AUDIT = 'b48c8afd46275ecffa62325d34ea5e3c8d68d8a104ee4ce6c3158c024003f72a'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def check_manifest(root, filename):
    m = json.loads((root / filename).read_text())
    listed = {v['path'] for v in m['files']}
    need(len(listed) == len(m['files']), 'duplicate manifest path')
    actual = {f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file()}
    need(actual == listed | {filename}, 'manifest inventory differs')
    need(not any(f.is_symlink() for f in root.rglob('*')), 'symlinks forbidden')
    for item in m['files']:
        p = Path(item['path'])
        need(not p.is_absolute() and '..' not in p.parts, 'unsafe manifest path')
        f = root / p
        need(f.stat().st_size == item['bytes'], 'size mismatch: ' + str(p))
        need(digest(f) == item['sha256'], 'hash mismatch: ' + str(p))
    return len(listed)


def validate(root, replay):
    count = check_manifest(root, 'RELEASE_MANIFEST.json')
    need(digest(root/'package/FROZEN_MANIFEST.json') == AUTHOR, 'author binding differs')
    need(digest(root/'audit-independent/AUDIT_MANIFEST.json') == AUDIT, 'audit binding differs')
    check_manifest(root/'package', 'FROZEN_MANIFEST.json')
    check_manifest(root/'audit-independent', 'AUDIT_MANIFEST.json')
    report = {'result': 'PASS', 'release_files_verified': count,
              'author_manifest_sha256': AUTHOR, 'audit_manifest_sha256': AUDIT,
              'source_files_included': False}
    if replay:
        cases = [('package/controls/check.py', 'package/controls/expected.json'),
                 ('audit-independent/independent_checks.py', 'audit-independent/independent_results.json')]
        outputs = []
        for script, expected in cases:
            r = subprocess.run([sys.executable, str(root/script)], cwd=root,
                               capture_output=True, check=True)
            need(r.stderr == b'', 'unexpected replay stderr')
            need(r.stdout == (root/expected).read_bytes(), 'replay differs: ' + script)
            outputs.append(hashlib.sha256(r.stdout).hexdigest())
        report.update(author_output_byte_identical=True, independent_output_byte_identical=True,
                      replay_output_sha256=outputs, author_pair_checks=30625,
                      independent_matrix_pair_checks=10125)
    return report


def mutant_tests():
    rejected = []
    for mode in ('changed_proof', 'changed_audit', 'missing_expected_output', 'unexpected_file'):
        with tempfile.TemporaryDirectory(prefix='rank611-mutant-') as td:
            target = Path(td)/'release'
            shutil.copytree(ROOT, target)
            if mode == 'changed_proof':
                f = target/'package/PROOF.md'; f.write_bytes(f.read_bytes()+b'\n')
            elif mode == 'changed_audit':
                f = target/'audit-independent/AUDIT.md'; f.write_bytes(f.read_bytes()+b'\n')
            elif mode == 'missing_expected_output':
                (target/'package/controls/expected.json').unlink()
            else:
                (target/'unexpected.txt').write_text('unexpected file\n')
            try:
                validate(target, replay=False)
            except (ValueError, OSError):
                rejected.append(mode)
            else:
                raise ValueError('mutant not rejected: ' + mode)
    return rejected


if __name__ == '__main__':
    need(len(sys.argv) <= 2 and (len(sys.argv) == 1 or sys.argv[1] == '--self-test'), 'unknown argument')
    report = validate(ROOT, replay=True)
    if '--self-test' in sys.argv:
        report['mutants_rejected'] = mutant_tests()
    report['limits'] = ['Integrity and replay checks are not formal proof verification.',
                        'Topology, source scope and priority require the written proof and audit.']
    print(json.dumps(report, sort_keys=True, indent=2))

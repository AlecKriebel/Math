#!/usr/bin/env python3
"""Read-only exact inventory, integrity, and replay checks for this checkpoint."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import shutil
import tempfile


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(root, expected_manifest=None):
    manifest_path = root / 'RELEASE_MANIFEST.json'
    if expected_manifest:
        assert digest(manifest_path) == expected_manifest, 'release manifest changed'
    manifest = json.loads(manifest_path.read_text())
    expected = set(manifest['files']) | {'RELEASE_MANIFEST.json'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual == expected, 'unexpected or missing release file'
    assert not any(p.is_symlink() for p in root.rglob('*')), 'symlink in packet'
    for name, info in manifest['files'].items():
        path = root / name
        assert path.stat().st_size == info['bytes'], name + ': size mismatch'
        assert digest(path) == info['sha256'], name + ': hash mismatch'
    assert digest(root/'submission/MANIFEST.json') == 'b2075d407c7c8549feb69e16fa6ca33dad6d65a57873291da59dda37ce7f0653'
    assert digest(root/'submission/RESULT.md') == '073340a7e505d58912b40e4bca9f4d18fead1362346d336bb7ccffa176d5b3c7'
    for part, name in [('submission', 'MANIFEST.json'), ('audit', 'AUDIT_MANIFEST.json')]:
        directory = root/part
        entries = json.loads((directory/name).read_text())['files']
        assert set(p.name for p in directory.iterdir() if p.is_file()) == set(entries) | {name, 'SHA256SUMS'}
        for f, info in entries.items():
            assert digest(directory/f) == info['sha256']
            assert (directory/f).stat().st_size == info['bytes']
        for line in (directory/'SHA256SUMS').read_text().splitlines():
            sha, f = line.split(maxsplit=1)
            assert digest(directory/f.strip()) == sha
    author_bytes = subprocess.check_output([sys.executable, str(root/'submission/verify_controls.py')])
    audit_bytes = subprocess.check_output([sys.executable, str(root/'audit/verify_audit.py'), '--submission', str(root/'submission')])
    assert author_bytes == (root/'submission/control_results.json').read_bytes(), 'author replay differs'
    assert audit_bytes == (root/'audit/audit_test_results.json').read_bytes(), 'audit replay differs'
    author, audit = json.loads(author_bytes), json.loads(audit_bytes)
    assert author['checks'] == 8233 and author['target_resolution'] is False
    return {'result': 'PASS', 'release_files_verified': len(expected),
            'author_assertions': author['checks'], 'audit_result': audit,
            'author_output_byte_identical': True, 'audit_output_byte_identical': True,
            'frozen_author_and_audit_preserved': True,
            'release_manifest_sha256': digest(manifest_path),
            'limitations': 'Integrity and finite replay are not a general analytic proof verifier.'}


def negative_controls(root):
    expected = digest(root/'RELEASE_MANIFEST.json')
    mutations = {
        'altered_author_proof': ('submission/RESULT.md', 'append'),
        'altered_full_audit': ('audit/AUDIT.md', 'append'),
        'altered_addendum': ('ADDENDUM.md', 'append'),
        'missing_expected_output': ('submission/control_results.json', 'delete'),
        'unexpected_file': ('UNEXPECTED.txt', 'append'),
        'altered_manifest': ('RELEASE_MANIFEST.json', 'append'),
    }
    rejected = []
    with tempfile.TemporaryDirectory(prefix='basin-integrity-') as tmp:
        for name, (rel, operation) in mutations.items():
            copy = Path(tmp)/name
            shutil.copytree(root, copy)
            target = copy/rel
            if operation == 'delete':
                target.unlink()
            else:
                with target.open('ab') as f:
                    f.write(b'\n')
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                '--root', str(copy), '--expected-manifest', expected,
                '--skip-negative-controls'], capture_output=True)
            assert result.returncode != 0, name + ' was not rejected'
            rejected.append(name)
    return rejected


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--expected-manifest')
    p.add_argument('--skip-negative-controls', action='store_true')
    args = p.parse_args()
    result = verify(args.root, args.expected_manifest)
    if not args.skip_negative_controls:
        result['mutants_rejected'] = negative_controls(args.root)
    print(json.dumps(result, indent=2, sort_keys=True))

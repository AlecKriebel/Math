#!/usr/bin/env python3
"""Verify the immutable release bindings and replay finite algebra diagnostics.

This does not compute a Floer invariant or prove either problem target.
Only the Python standard library is needed. No network access is used.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
AUTHOR_MANIFEST = '8074d0a6a5ec04ee4ba269300bb0bddad6b49595e955f456d26a10898b757888'
AUDIT_MANIFEST = '9a35d1eeb6b10378ceae1aea66ff8da42d7d35d2a765c8b58d24ecdcbc0fb841'
PROOF = '4ae92f8adaabff6700ee8a6da5a178e629321729cbd4420153d6c2f64975ac36'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(folder, expected_count, expected_digest=None):
    manifest = folder / 'SHA256SUMS'
    if expected_digest:
        require(digest(manifest) == expected_digest, f'{folder.name}: frozen manifest mismatch')
    entries = {}
    for line in manifest.read_text().splitlines():
        h, relative = line.split('  ', 1)
        require(len(h) == 64 and all(c in '0123456789abcdef' for c in h), 'Invalid digest')
        path = Path(relative)
        require(not path.is_absolute() and '..' not in path.parts, 'Unsafe manifest path')
        require(relative not in entries, f'Duplicate manifest entry: {relative}')
        target = folder / path
        require(not target.is_symlink(), f'Symlink not permitted: {relative}')
        require(target.is_file() and digest(target) == h, f'Hash mismatch: {relative}')
        entries[relative] = h
    require(len(entries) == expected_count, f'{folder.name}: wrong manifest count')
    actual = {str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()}
    require(actual == set(entries) | {'SHA256SUMS'}, f'{folder.name}: unlisted or missing file')
    return entries


def main():
    release_entries = verify_manifest(ROOT, 18)
    author_entries = verify_manifest(ROOT/'author', 8, AUTHOR_MANIFEST)
    audit_entries = verify_manifest(ROOT/'audit', 5, AUDIT_MANIFEST)
    require(digest(ROOT/'author/PROOF.md') == PROOF, 'Frozen proof mismatch')
    binding = json.loads((ROOT/'audit/audit_binding.json').read_text())
    require(binding['frozen_manifest_sha256'] == AUTHOR_MANIFEST, 'Audit manifest binding mismatch')
    require(binding['frozen_proof_sha256'] == PROOF, 'Audit proof binding mismatch')
    require(len(binding['frozen_files']) == 9, 'Wrong audit-bound author count')
    bound_names = set()
    for entry in binding['frozen_files']:
        path = ROOT/'author'/entry['name']
        require(entry['name'] not in bound_names, 'Duplicate author binding')
        bound_names.add(entry['name'])
        require(path.stat().st_size == entry['bytes'] and digest(path) == entry['sha256'],
                f'Audit binding mismatch: {entry["name"]}')
    require(bound_names == set(author_entries) | {'SHA256SUMS'}, 'Audit author inventory mismatch')
    status = json.loads((ROOT/'RELEASE_STATUS.json').read_text())
    require(status['problem_id'] == 2870 and status['disposition'] == 'unsolved'
            and status['turns'] == '5/5', 'Wrong release disposition')
    require(status['part_a_proved'] is False and status['part_b_proved'] is False,
            'Neither target is proved')
    verdict = 'PASS_SCOPED_UNSOLVED_WITH_CITATION_ADDENDUM'
    require(status['independent_audit_verdict'] == binding['verdict'] == verdict, 'Wrong audit verdict')
    require(binding['part_a_resolved'] is False and binding['part_b_resolved'] is False,
            'Wrong audit target scope')
    with tempfile.TemporaryDirectory(prefix='kirby2870-replay-') as temporary:
        author = subprocess.run([sys.executable, '-B', str(ROOT/'author/check_controls.py')],
                                cwd=temporary, check=True, capture_output=True).stdout
        audit = subprocess.run([sys.executable, '-B', str(ROOT/'audit/audit_checks.py')],
                               cwd=temporary, check=True, capture_output=True).stdout
    require(author == (ROOT/'author/controls.json').read_bytes(), 'Author output mismatch')
    require(author == (ROOT/'audit/replayed_controls.json').read_bytes(), 'Audit replay output mismatch')
    require(audit == (ROOT/'audit/audit_controls.json').read_bytes(), 'Independent output mismatch')
    require(json.loads(author)['assertions'] == 9495, 'Wrong author assertion count')
    require(json.loads(audit)['assertions'] == 6470, 'Wrong independent probe count')
    print(json.dumps({
        'problem_id': 2870,
        'result': 'PASS_RELEASE_BINDINGS_AND_FINITE_DIAGNOSTIC_REPLAY',
        'release_files': len(release_entries)+1,
        'frozen_author_files': len(author_entries)+1,
        'frozen_audit_files': len(audit_entries)+1,
        'author_assertions': 9495, 'independent_probes': 6470,
        'outputs_byte_identical': True,
        'disposition': 'unsolved', 'turns': '5/5',
        'part_a_proved': False, 'part_b_proved': False,
        'limitations': 'Finite diagnostics are not Floer computations, manifold independence proofs, formal verification, human peer review, or a CI result.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

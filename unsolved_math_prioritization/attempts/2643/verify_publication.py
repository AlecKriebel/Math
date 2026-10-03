#!/usr/bin/env python3
"""Verify frozen source-certificate bytes and replay its arithmetic checker."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUTHOR_HASH = 'e8733976bfb8e9404a2f309eff6a3f465bdd421f51345397f4044f9211c48541'
AUDIT_HASH = '48c8dd78d4f10f24e1eae9719685bd6813acf9ac88f8233f17fa2001b39e8faf'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_entry(root, entry):
    path = root / entry['path']
    assert path.resolve().is_relative_to(root.resolve()), entry['path']
    assert path.is_file() and path.stat().st_size == entry['bytes'], entry['path']
    assert digest(path) == entry['sha256'], entry['path']


def main():
    package = json.loads((ROOT / 'PUBLICATION_MANIFEST.json').read_text())
    for entry in package['files']:
        verify_entry(ROOT, entry)
    expected = {entry['path'] for entry in package['files']} | {'PUBLICATION_MANIFEST.json'}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert actual == expected, sorted(actual ^ expected)
    original = ROOT / 'frozen_original'
    assert digest(original / 'AUTHOR_MANIFEST.json') == AUTHOR_HASH
    author = json.loads((original / 'AUTHOR_MANIFEST.json').read_text())
    assert author['problem_id'] == 2643 and author['substantive_attempt_turns'] == 0
    for entry in author['files']:
        verify_entry(original, entry)
    assert digest(ROOT / 'INDEPENDENT_AUDIT.md') == AUDIT_HASH
    replay = subprocess.check_output([sys.executable, str(original / 'verify_counts.py')])
    assert replay == (original / 'verification.json').read_bytes()
    result = json.loads(replay)
    assert result['status'] == 'PASS'
    print(json.dumps({
        'status': 'PASS',
        'problem_id': 2643,
        'disposition': 'already_solved',
        'substantive_attempt_turns': 0,
        'publication_file_hash_checks': len(package['files']),
        'frozen_author_payload_hash_checks': len(author['files']),
        'author_manifest_binding': True,
        'independent_audit_binding': True,
        'arithmetic_output_replay_byte_exact': True,
        'independent_group_enumeration': False
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Verify the corrected packet, exact correction, and preserved control replays."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ORIGINAL_SUMS = 'e468ff6825bd523f60483c9bb812a577a6724a03684b75205f70340e7ffc1c8f'
AUDIT_SUMS = 'a09c40caa8025a5a03989cd7d6c5e423b1d5e37e6b51cc3a99e2ec0f4e1dc17b'
CORRECTION_SHA = '04e69a8ad6206071e2e4226c19950c2eb60d57dfa941fe26a97426ca14e7297d'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_relative(name):
    path = Path(name)
    assert not path.is_absolute() and '..' not in path.parts and str(path) == name
    return path


def verify_sums(directory, expected=None):
    sumfile = directory / 'SHA256SUMS'
    if expected:
        assert digest(sumfile) == expected, str(sumfile)
    names = []
    for line in sumfile.read_text().splitlines():
        checksum, name = line.split(None, 1)
        name = name.strip()
        path = validate_relative(name)
        assert digest(directory / path) == checksum, name
        names.append(name)
    assert len(names) == len(set(names)), 'duplicate manifest path'
    return names


def verify_package_manifest():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    listed = manifest['files']
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
              and p.relative_to(ROOT).as_posix() not in ('MANIFEST.json', 'SHA256SUMS')
              and '__pycache__' not in p.parts}
    assert actual == set(listed), 'package file-set mismatch'
    for name, details in listed.items():
        path = ROOT / validate_relative(name)
        assert path.stat().st_size == details['bytes'], name
        assert digest(path) == details['sha256'], name
    names = verify_sums(ROOT)
    assert set(names) == actual | {'MANIFEST.json'}, 'outer checksum scope mismatch'


def run(*arguments):
    process = subprocess.run([sys.executable, *map(str, arguments)], cwd=ROOT,
                             capture_output=True, check=True)
    return process.stdout


def verify_payload():
    original = ROOT / 'original-author'
    current = ROOT / 'current'
    audit = ROOT / 'audit'
    original_names = verify_sums(original, ORIGINAL_SUMS)
    current_names = verify_sums(current)
    audit_names = verify_sums(audit, AUDIT_SUMS)
    assert original_names == current_names
    for folder, names in ((original, original_names), (current, current_names),
                          (audit, audit_names)):
        actual = {p.name for p in folder.iterdir() if p.is_file()}
        assert actual == set(names) | {'SHA256SUMS'}, str(folder)
    changed = [name for name in original_names
               if (original / name).read_bytes() != (current / name).read_bytes()]
    assert changed == ['PROOF.md', 'SOURCES.md'], changed
    diff = ''.join(''.join(difflib.unified_diff(
        (original / name).read_text().splitlines(keepends=True),
        (current / name).read_text().splitlines(keepends=True),
        fromfile='author/' + name, tofile='revised/' + name)) for name in changed)
    assert diff.encode() == (ROOT / 'CORRECTION.diff').read_bytes()
    assert (ROOT / 'CORRECTION.diff').read_bytes() == (audit / 'proposed_corrections.patch').read_bytes()
    assert digest(ROOT / 'CORRECTION.diff') == CORRECTION_SHA

    ledger = json.loads((ROOT / 'CORRECTION_LEDGER.json').read_text())
    assert ledger['status'] == 'unsolved' and ledger['approaches_completed'] == 5
    assert ledger['full_resolution'] is False and ledger['novelty_claim'] is False
    assert ledger['exact_diff_sha256'] == CORRECTION_SHA == ledger['reviewer_patch_sha256']
    assert ledger['original_manifest_sha256'] == ORIGINAL_SUMS
    assert ledger['preserved_audit_sha256sums_sha256'] == AUDIT_SUMS
    assert ledger['current_manifest_sha256'] == digest(current / 'SHA256SUMS')
    recorded = ledger['changes'] + ledger['unchanged_current_files']
    assert {row['path'] for row in recorded} == set(original_names) | {'SHA256SUMS'}
    for row in recorded:
        name = row['path']
        assert row['original_sha256'] == digest(original / name), name
        assert row['corrected_sha256'] == digest(current / name), name
    assert {r['path'] for r in ledger['changes']} == set(changed) | {'SHA256SUMS'}

    proof = (current / 'PROOF.md').read_text()
    sources = (current / 'SOURCES.md').read_text()
    assert 'A covering changes the group unless' not in proof
    assert 'A covering need not preserve the fundamental group;' in proof
    assert 'proper birational modification' in proof and 'proper birational modification' in sources
    assert 'Question 1.2 and Example 1.7' in proof and 'Question 1.2 and Example 1.7' in sources
    assert '2016' in sources and '2019' in sources
    assert 'These are announcements, contain no proof' in sources
    result = json.loads((current / 'RESULT.json').read_text())
    assert result['status'] == 'unsolved' and result['approaches_completed'] == 5
    assert result['full_resolution'] is False and result['novelty_claim'] is False
    assert result['literature_caveat'] == json.loads((original / 'RESULT.json').read_text())['literature_caveat']

    author_original = run(original / 'verify_controls.py')
    author_current = run(current / 'verify_controls.py')
    assert author_original == author_current == (original / 'control_results.json').read_bytes()
    assert author_current == (current / 'control_results.json').read_bytes() == (ROOT / 'author_replay.json').read_bytes()
    author_result = json.loads(author_current)
    assert author_result['total_assertions'] == 506
    assert author_result['invariant_monomial_controls'] == 481
    independent = run(audit / 'verify_audit.py', '--author-dir', original)
    assert independent == (audit / 'audit_control_results.json').read_bytes()
    assert independent == (ROOT / 'independent_replay.json').read_bytes()
    audit_result = json.loads(independent)
    assert audit_result['assertions'] == 93
    assert audit_result['author_replay']['byte_identical'] is True
    assert audit_result['author_replay']['assertions'] == 506
    return {
        'status': 'passed',
        'problem_id': 30002526,
        'target_status': 'unsolved',
        'approaches_completed': 5,
        'full_resolution': False,
        'original_author_manifest_sha256': ORIGINAL_SUMS,
        'preserved_audit_sha256sums_sha256': AUDIT_SUMS,
        'corrected_author_manifest_sha256': digest(current / 'SHA256SUMS'),
        'exact_reviewer_diff_sha256': CORRECTION_SHA,
        'changed_author_content_files': changed,
        'other_author_content_unchanged': True,
        'properness_and_covering_corrections_verified': True,
        'stronger_announcement_literature_caveat_preserved': True,
        'author_assertions': 506,
        'bounded_author_parity_controls': 481,
        'independent_assertions': 93,
        'author_and_independent_replays_byte_identical': True,
        'dependencies': 'Python 3 standard library only',
        'scope_limit': 'Correction and replay verification, not a new mathematical approach or original-reviewer release binding.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    verify_package_manifest()
    payload = json.dumps(verify_payload(), indent=2, sort_keys=True) + '\n'
    if arguments.output:
        destination = arguments.output.resolve()
        assert destination != (ROOT / 'verification_results.json').resolve(), 'preserve supplied verification output'
        destination.write_text(payload)
    print(payload, end='')

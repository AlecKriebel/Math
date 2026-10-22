#!/usr/bin/env python3
"""Read-only binding verification for the exact reviewed corrected release.

Python 3 standard library. The optional release verifier subprocess was reviewed
and is invoked without its output-writing option. Output is printed only.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import sys

RELEASE_MANIFEST = '66e5c688379a999bb99edef5c1b48e14484a47c3f8d5893ef8776eb747013b98'
RELEASE_SUMS = '0fa0e7e0a6798edd82986626ddad5a3ade3c0617d33f04166ea3e7da7c208e76'
ORIGINAL_SUMS = 'e468ff6825bd523f60483c9bb812a577a6724a03684b75205f70340e7ffc1c8f'
AUDIT_SUMS = 'a09c40caa8025a5a03989cd7d6c5e423b1d5e37e6b51cc3a99e2ec0f4e1dc17b'
PATCH_SHA = '04e69a8ad6206071e2e4226c19950c2eb60d57dfa941fe26a97426ca14e7297d'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    nodes = list(root.rglob('*'))
    assert not any(p.is_symlink() for p in nodes), 'symlinks are outside this binding'
    assert all(p.is_file() or p.is_dir() for p in nodes), 'special file found'
    return {p.relative_to(root).as_posix(): sha(p) for p in nodes if p.is_file()}


def sums(root):
    rows = {}
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split(None, 1)
        name = name.strip()
        path = Path(name)
        assert not path.is_absolute() and '..' not in path.parts and str(path) == name
        assert name not in rows
        assert sha(root/path) == digest, name
        rows[name] = digest
    return rows


def verify(root):
    root = root.resolve()
    assert sha(root/'MANIFEST.json') == RELEASE_MANIFEST
    assert sha(root/'SHA256SUMS') == RELEASE_SUMS
    before = inventory(root)
    assert len(before) == 36
    assert all(Path(name).suffix in {'.md','.json','.py','.diff','.patch',''} for name in before)
    assert not any(set(Path(name).parts) & {'private','.git','__pycache__'} for name in before)
    manifest = json.loads((root/'MANIFEST.json').read_text())
    assert set(before) == set(manifest['files']) | {'MANIFEST.json','SHA256SUMS'}
    for name, item in manifest['files'].items():
        assert before[name] == item['sha256'] and (root/name).stat().st_size == item['bytes']
    outer = sums(root)
    assert set(outer) == set(before)-{'SHA256SUMS'}
    original,current,audit = (root/name for name in ('original-author','current','audit'))
    assert sha(original/'SHA256SUMS') == ORIGINAL_SUMS
    assert sha(audit/'SHA256SUMS') == AUDIT_SUMS
    original_names = sums(original)
    assert set(sums(current)) == set(original_names)
    audit_names = sums(audit)
    assert set(inventory(original)) == set(original_names)|{'SHA256SUMS'}
    assert set(inventory(audit)) == set(audit_names)|{'SHA256SUMS'}
    changed = sorted(name for name in original_names if (original/name).read_bytes() != (current/name).read_bytes())
    assert changed == ['PROOF.md','SOURCES.md']
    delta = ''.join(''.join(difflib.unified_diff(
        (original/name).read_text().splitlines(True),
        (current/name).read_text().splitlines(True),
        fromfile='author/'+name,tofile='revised/'+name)) for name in changed)
    assert delta.encode() == (root/'CORRECTION.diff').read_bytes() == (audit/'proposed_corrections.patch').read_bytes()
    assert sha(root/'CORRECTION.diff') == PATCH_SHA
    ledger = json.loads((root/'CORRECTION_LEDGER.json').read_text())
    assert {c['id'] for c in ledger['corrections']} == {'C1','C2'}
    assert {x['path'] for x in ledger['changes']} == {'PROOF.md','SOURCES.md','SHA256SUMS'}
    ledger_rows = ledger['changes'] + ledger['unchanged_current_files']
    assert len(ledger_rows) == 8 and {r['path'] for r in ledger_rows} == set(original_names)|{'SHA256SUMS'}
    for row in ledger_rows:
        assert row['original_sha256'] == sha(original/row['path'])
        assert row['corrected_sha256'] == sha(current/row['path'])
    assert ledger['original_manifest_sha256'] == ORIGINAL_SUMS
    assert ledger['current_manifest_sha256'] == sha(current/'SHA256SUMS')
    assert ledger['preserved_audit_sha256sums_sha256'] == AUDIT_SUMS
    assert ledger['exact_diff_sha256'] == ledger['reviewer_patch_sha256'] == PATCH_SHA
    proof = (current/'PROOF.md').read_text()
    sources = (current/'SOURCES.md').read_text()
    assert 'proper birational modification that is an isomorphism over the NC locus' in proof
    assert 'proper birational modification preserving the NC locus' in sources
    assert 'A covering need not preserve the fundamental group;' in proof
    assert 'A covering changes the group unless' not in proof
    section = '## Stronger announcements requiring caution'
    assert sources.split(section)[1] == (original/'SOURCES.md').read_text().split(section)[1]
    assert '2016' in sources and '2019' in sources and 'These are announcements, contain no proof' in sources
    result = json.loads((current/'RESULT.json').read_text())
    assert result['status'] == 'unsolved' and result['approaches_completed'] == 5
    assert result['full_resolution'] is False and result['novelty_claim'] is False
    assert result == json.loads((original/'RESULT.json').read_text())
    replay = subprocess.run([sys.executable,str(root/'verify_release.py')],cwd=root,capture_output=True,check=True).stdout
    assert replay == (root/'verification_results.json').read_bytes()
    verified = json.loads(replay)
    assert verified['author_assertions'] == 506 and verified['independent_assertions'] == 93
    assert verified['author_and_independent_replays_byte_identical'] is True
    assert inventory(root) == before, 'release changed during verification'
    return {
      'status':'passed',
      'acceptance':'accept_corrected_partial_results_for_exact_bound_release',
      'problem_id':30002526,
      'bound_release_manifest_sha256':RELEASE_MANIFEST,
      'bound_release_sha256sums_sha256':RELEASE_SUMS,
      'bound_correction_diff_sha256':PATCH_SHA,
      'original_author_manifest_sha256':ORIGINAL_SUMS,
      'preserved_audit_sha256sums_sha256':AUDIT_SUMS,
      'regular_release_files':36,
      'original_author_preserved_files':8,
      'audit_preserved_files':11,
      'changed_content_files':changed,
      'regenerated_checksum':'current/SHA256SUMS',
      'corrections_closed':['C1','C2'],
      'author_controls':506,
      'independent_controls':93,
      'byte_identical_replays':True,
      'target_status':'unsolved_in_this_investigation',
      'approaches_completed':5,
      'full_resolution':False,
      'verified_prior_resolution':False,
      'current_literature_openness_certified':False,
      'literature_caveat_preserved':True,
      'release_unchanged_during_review':True,
      'scope':'Correction closure and exact-release binding only; no new proof search or mathematical promotion.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--release-dir',type=Path,default=Path(__file__).resolve().parent.parent/'release')
    args = parser.parse_args()
    print(json.dumps(verify(args.release_dir),indent=2,sort_keys=True))

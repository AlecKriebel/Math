#!/usr/bin/env python3
"""Read-only binding verification for this exact corrected release snapshot.

Outputs must be placed outside the supplied release directory. Computational
replays are performed separately by RELEASE_CHECKS.py; their saved result is
checked here against the bound original release record.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath

MANIFEST_SHA256 = '1857279d8d5a572c27d337e2625d61189ed2a683f642ed941dfee9a52b8ef67d'
ROOT_SUMS_SHA256 = '1bee70377abb0954cd42a454b865d8fa1f142197ccc2ae393e918b49ce031d15'
AUDIT_SUMS_SHA256 = '1f8d06019b95e0673d384b820455aa5367801b3dc0699a6ec405957654ca437c'
ORIGINAL_BINDING_SHA256 = '9d73ff0727f46bee128031b23a0c354106f065f28a7d48303da5858d97dcf03a'
SERIALIZER_SHA256 = '5895b2e230280ed55fb8ec490ae3757d81306655ecdbb81ddd59565ed5735381'


def sha(f):
    return hashlib.sha256(f.read_bytes()).hexdigest()


def safe_path(s):
    p = PurePosixPath(s)
    assert not p.is_absolute() and '..' not in p.parts and '.' not in p.parts
    assert str(p) == s and s
    return p


def check_sums(f):
    rows = {}
    for line in f.read_text().splitlines():
        digest, name = line.split('  ', 1)
        safe_path(name)
        assert name not in rows and len(digest) == 64
        target = f.parent/name
        assert target.is_file() and not target.is_symlink()
        assert sha(target) == digest, name
        rows[name] = digest
    return rows


def verify(release, replay):
    release = release.resolve()
    assert sha(release/'MANIFEST.json') == MANIFEST_SHA256
    assert sha(release/'SHA256SUMS') == ROOT_SUMS_SHA256
    manifest = json.loads((release/'MANIFEST.json').read_text())
    paths = set()
    for entry in manifest['files']:
        name = entry['path']
        safe_path(name)
        assert name not in paths
        paths.add(name)
        f = release/name
        assert f.is_file() and not f.is_symlink()
        assert sha(f) == entry['sha256']
        assert f.stat().st_size == entry['bytes']
    actual = set()
    for f in release.rglob('*'):
        assert not f.is_symlink()
        if f.is_file():
            actual.add(f.relative_to(release).as_posix())
    assert actual == paths | {'MANIFEST.json', 'SHA256SUMS'}
    assert len(actual) == 39 and len(paths) == 37
    root_sums = check_sums(release/'SHA256SUMS')
    assert set(root_sums) == actual-{'SHA256SUMS'}
    assert len(root_sums) == 38
    audit = release/'audit'
    original = release/'original-author'
    current = release/'current'
    assert sha(audit/'SHA256SUMS') == AUDIT_SUMS_SHA256
    audit_sums = check_sums(audit/'SHA256SUMS')
    assert {f.name for f in audit.iterdir()} == set(audit_sums) | {'SHA256SUMS'}
    assert len(audit_sums) == 13
    assert sha(audit/'AUDITED_INPUTS.json') == ORIGINAL_BINDING_SHA256
    binding = json.loads((audit/'AUDITED_INPUTS.json').read_text())
    original_names = set()
    for row in binding['files']:
        name = row['path']
        safe_path(name)
        assert name not in original_names
        original_names.add(name)
        assert sha(original/name) == row['sha256']
    assert len(original_names) == 9
    assert original_names == {f.name for f in original.iterdir()}
    assert original_names == {f.name for f in current.iterdir()}
    check_sums(original/'SHA256SUMS')
    check_sums(current/'SHA256SUMS')
    ledger = json.loads((release/'CORRECTION_LEDGER.json').read_text())
    changed = {n for n in original_names if (original/n).read_bytes() != (current/n).read_bytes()}
    unchanged = original_names-changed
    assert changed == {row['path'] for row in ledger['changes']}
    assert unchanged == {row['path'] for row in ledger['unchanged_current_files']}
    assert unchanged == {'PROOF.md', 'SOURCES.md'} and len(changed) == 7
    for row in ledger['changes'] + ledger['unchanged_current_files']:
        assert sha(original/row['path']) == row['original_sha256']
        assert sha(current/row['path']) == row['corrected_sha256']
    assert ledger['supplied_serializer_sha256'] == SERIALIZER_SHA256
    assert ledger['safe_original_binding_sha256'] == ORIGINAL_BINDING_SHA256
    assert ledger['preserved_audit_sumfile_sha256'] == AUDIT_SUMS_SHA256
    assert ledger['preserved_original_binding'] == 'audit/AUDITED_INPUTS.json'
    assert ledger['preserved_audit_binding'] == 'audit/SHA256SUMS'
    diff = ''.join(''.join(difflib.unified_diff(
        (original/n).read_text().splitlines(keepends=True),
        (current/n).read_text().splitlines(keepends=True),
        fromfile='original-author/'+n, tofile='current/'+n))
        for n in sorted(original_names))
    assert diff == (release/'CORRECTION.diff').read_text()
    assert sha(release/'CORRECTION.diff') == ledger['exact_unified_diff_sha256']
    assert sha(current/'verify_controls.py') == SERIALIZER_SHA256
    assert (current/'verify_controls.py').read_bytes() == (audit/'verify_controls_outward.py').read_bytes()
    for a, b in [('control_results.json', 'corrected_controls_2048_40.json'),
                 ('control_results_high_precision.json', 'corrected_controls_4096_60.json')]:
        assert (current/a).read_bytes() == (audit/b).read_bytes()
    result = json.loads((current/'RESULT.json').read_text())
    for obj in (manifest, result):
        assert obj['status'] == 'unsolved' and obj['substantive_routes'] == 5
        assert obj['full_resolution'] is False and obj['novelty_claim'] is False
    # Exact whitelisting binds the complete inventory. Supplemental textual
    # guards catch an accidental path or raw coordination inventory reference.
    forbidden = ('/private/', '/workspace/')
    for name in actual:
        assert Path(name).suffix.lower() in ('.md', '.py', '.json', '.diff', '')
        assert 'private' not in PurePosixPath(name).parts
        text = (release/name).read_text()
        for marker in forbidden:
            assert marker not in text, (name, marker)
    replay_data = json.loads(replay.read_text())
    assert replay_data['all_checks_passed']
    assert replay.read_bytes() == (release/'verification_results.json').read_bytes()
    assert len(replay_data['replays']) == 4
    assert all(r['saved_output_exact_match'] for r in replay_data['replays'])
    assert len(replay_data['corrected_interval_relationships']) == 11
    for r in replay_data['corrected_interval_relationships']:
        assert r['high_nested_in_low'] and r['low_nested_in_independent']
        assert r['sign'] == ('positive' if r['m'] <= 9 else 'negative')
    assert replay_data['audit_verification']['independent_rerun_exact_match']
    assert replay_data['audit_verification']['outward_serializer_exact_tests'] == 24
    return {
        'problem_id': 30002497,
        'release_manifest_sha256': MANIFEST_SHA256,
        'release_sha256sums_sha256': ROOT_SUMS_SHA256,
        'release_files_exactly_inventoried': 39,
        'manifest_payload_rows_verified': 37,
        'root_checksum_rows_verified': 38,
        'original_author_files_preserved': 9,
        'original_audit_files_preserved': 14,
        'changed_current_files_exactly_ledgered': sorted(changed),
        'unchanged_current_files': sorted(unchanged),
        'unified_diff_reconstructed_exactly': True,
        'audited_serializer_used_verbatim': True,
        'corrected_outputs_match_audited_certificates': True,
        'historical_and_corrected_computational_replays': 4,
        'replayed_release_record_exact_byte_match': True,
        'nested_derivative_intervals': 11,
        'independent_integer_backend_rerun': True,
        'exact_serializer_tests': 24,
        'safe_inventory_and_private_path_guards': True,
        'full_target_status': 'unsolved',
        'correction_C1_status': 'closed_for_this_exact_release',
        'all_checks_passed': True,
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--release', type=Path, required=True)
    p.add_argument('--replay', type=Path, required=True)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    if a.output:
        assert not a.output.resolve().is_relative_to(a.release.resolve())
    data = json.dumps(verify(a.release, a.replay), indent=2)+'\n'
    if a.output:
        a.output.write_text(data)
    else:
        print(data, end='')

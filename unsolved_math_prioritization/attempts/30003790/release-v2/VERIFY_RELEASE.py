#!/usr/bin/env python3
"""Verify corrected-v2 bindings and replay unchanged historical controls.
Standard library only. This verifies assembly integrity, not a new theorem.
"""
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
CANDIDATE = '072aba944c908baf44bb86d6c9a3d1c87444b5f779c53a14b4a9648d9595351c'
ORIGINAL_MANIFEST = 'a18df1c214a6ea7ed7aa14d8a038827f463a7c9ff4f069228e0eb68b247367d2'
ORIGINAL_RESULT = '0c63e1801d50434d217a8a66d16ea8bad27cac4867919f7532abc4819eb9dc16'
FIRST_AUDIT = '546d0d709f61a2f8e25e653a29606b7e7e6512ddabaeb811195057adc31e890b'
AUXILIARY_AUDIT = '954dedd9ec67d2819b211aa6cbb6f33cd578977175fb1478ede820aa3f4aab6f'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_map(base):
    return {str(p.relative_to(base)): p for p in base.rglob('*') if p.is_file()}


def verify_manifest(base, filename='MANIFEST.json'):
    manifest = json.loads((base / filename).read_text())
    named = set()
    for row in manifest['files']:
        assert row['path'] not in named
        named.add(row['path'])
        p = base / row['path']
        assert not p.is_symlink()
        assert p.stat().st_size == row['bytes'], row['path']
        assert sha(p) == row['sha256'], row['path']
    assert set(file_map(base)) == named | {filename}, ('unlisted files', str(base))
    return len(named)


def exact_diff(old, new):
    a, b = file_map(old), file_map(new)
    pieces = []
    for path in sorted(set(a) | set(b)):
        before = a[path].read_text().splitlines(keepends=True) if path in a else []
        after = b[path].read_text().splitlines(keepends=True) if path in b else []
        pieces.extend(difflib.unified_diff(before, after,
                      fromfile='history/public/' + path, tofile='public/' + path))
    return ''.join(pieces)


def run_replay(script, args, expected):
    completed = subprocess.run([sys.executable, str(script), *map(str, args)],
                               check=True, capture_output=True)
    assert completed.stdout == expected.read_bytes(), str(script)
    return json.loads(completed.stdout)


def main():
    historical = ROOT / 'history'
    public = ROOT / 'public'
    assert sha(historical/'public/MANIFEST.json') == ORIGINAL_MANIFEST
    assert sha(historical/'public/RESULT.md') == ORIGINAL_RESULT
    assert sha(historical/'independent-audit/AUDIT.md') == FIRST_AUDIT
    assert sha(historical/'auxiliary-independent-audit/AUDIT.md') == AUXILIARY_AUDIT
    assert sha(historical/'independent-audit/AUXILIARY_CANDIDATE.md') == CANDIDATE
    assert sha(public/'AUXILIARY_THEOREM.md') == CANDIDATE
    for name in ['public', 'independent-audit', 'auxiliary-independent-audit']:
        verify_manifest(historical / name)
    verify_manifest(public)
    verify_manifest(ROOT, 'RELEASE_MANIFEST.json')

    assert (ROOT/'AUTHOR_V1_TO_CORRECTED_V2.diff').read_text() == exact_diff(historical/'public', public)
    changes = json.loads((ROOT/'CHANGES.json').read_text())
    old_map, new_map = file_map(historical/'public'), file_map(public)
    assert {x['path'] for x in changes['files']} == set(old_map) | set(new_map)
    for row in changes['files']:
        for label, mapping in [('before', old_map), ('after', new_map)]:
            item = row[label]
            if row['path'] in mapping:
                p = mapping[row['path']]
                assert item == {'bytes': p.stat().st_size, 'sha256': sha(p)}
            else:
                assert item is None
    assert json.loads((public/'turns.json').read_text())['turns'] == json.loads(
        (historical/'public/turns.json').read_text())['turns']
    state = json.loads((ROOT/'CURRENT_STATUS.json').read_text())
    assert state['queue_disposition'] == 'unsolved' and state['author_turns_used'] == 5
    assert state['literal_bounded_model_consistency'] == 'established'
    assert state['original_model_coverage'] == 'not_established'
    assert state['release_binding_review'] == 'pending'
    assert state['remote_writes'] is False

    allowed_suffixes = {'.md', '.json', '.py', '.diff'}
    for path, p in file_map(ROOT).items():
        assert p.suffix in allowed_suffixes, path
        assert 'private' not in p.relative_to(ROOT).parts, path
        assert '__pycache__' not in p.relative_to(ROOT).parts, path
        assert not p.is_symlink(), path

    author = run_replay(historical/'public/verification/check.py', [],
                        historical/'public/verification/result.json')
    first = run_replay(historical/'independent-audit/verification/audit_check.py',
                       [historical/'public'], historical/'independent-audit/verification/audit-result.json')
    second = run_replay(historical/'auxiliary-independent-audit/verification/check_auxiliary.py',
                        [historical], historical/'auxiliary-independent-audit/verification/result.json')
    # The corrected copy preserves the author numerical controls exactly.
    run_replay(public/'verification/check.py', [], public/'verification/result.json')
    assert all(x['status'] == 'PASS' for x in [author, first, second])
    print(json.dumps({'status': 'PASS', 'historical_inputs_unchanged': True,
                      'accepted_candidate_byte_identical': True, 'exact_diff_verified': True,
                      'all_manifests_verified': True, 'all_three_recorded_control_outputs_byte_identical': True,
                      'author_guard_cases': 700, 'first_audit_guard_cases': 29160,
                      'auxiliary_fixed_guard_cases': 15855, 'auxiliary_adaptive_guard_cases': 1620,
                      'release_binding_review': 'pending', 'remote_writes': False}, indent=2))


if __name__ == '__main__':
    main()

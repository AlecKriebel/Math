#!/usr/bin/env python3
"""Retain and independently bind completed PR37 actual root replays."""
import datetime as dt
import hashlib
import json
from pathlib import Path

A = Path(__file__).resolve().parent
R = A.parents[2]
DEST = A / 'ROOT_REPLAY_SUPPORT_MANIFEST.json'
DIRS = [
    'root_three_closed_family_replay_support',
    'root_closed_families_replay_v2_support',
    'root_replay_preparation_family',
    'root_replay_execution_revision',
    'root_entrypoint_revisions',
]
FILES = [
    'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json',
    'ROOT_CLOSED_FAMILIES_REPLAY_FAILURE_V1.json',
    'ROOT_DATED_REPLAY_INPUT_REBASE.json',
    'reproduce_root_closed_families.py',
    'seal_root_replay_support.py',
]
FORBIDDEN = {'tmp', 'ignoredtmp', '__pycache__', 'foreign_sources',
             'foreign_downloads', 'private_sources', 'private_tmp'}
SUFFIXES = {'.json', '.jsonl', '.py', '.patch', '.md', '.stdout', '.stderr'}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(row, anchor):
    p = anchor / row['path']
    assert p.is_file() and not p.is_symlink(), str(p)
    assert p.stat().st_size == row.get('bytes', row.get('size')), str(p)
    assert digest(p) == row['sha256'], str(p)


def main():
    assert not DEST.exists(), 'Never replace a prior retained root manifest'
    receipt = json.loads((A / FILES[0]).read_text())
    assert receipt['status'] == 'PASS'
    assert receipt['authored_members_verified_before_and_after'] == 48
    assert receipt['root_script_sha256'] == digest(A / 'reproduce_root_closed_families.py')
    assert receipt['original_substantive_turns'] == 1
    assert receipt['turn_limit'] == 5 and receipt['new_substantive_attempts'] == 0
    for key in ['closed_members_and_manifest_self_bytes_unchanged', 'live_read_inputs_unchanged']:
        for row in receipt[key]:
            verify(row, R)
    for row in receipt['actual_outer_program_runs']:
        assert row['exit'] == 0
        verify(row['stdout'], A)
        verify(row['stderr'], A)
    for row in receipt['full_structured_receipt_comparisons']:
        verify(row['actual'], A)
        verify(row['saved'], A)
        if row['required_equality']:
            assert row['equal_after_clock_and_path_exclusions'] and not row['differences']
    paths = [A / p for p in FILES]
    for name in DIRS:
        for p in sorted((A / name).rglob('*')):
            if p.is_file() and not FORBIDDEN.intersection(p.relative_to(A).parts):
                assert not p.is_symlink(), str(p)
                assert p.suffix in SUFFIXES or p.name == '.gitignore', str(p)
                paths.append(p)
    assert len(paths) == len(set(paths))
    parsed_json = 0
    for p in paths:
        if p.suffix == '.json':
            json.loads(p.read_text())
            parsed_json += 1
    nested = []
    for p in sorted((A / 'root_closed_families_replay_v2_support').glob('*_nested/nested_runs.json')):
        rows = json.loads(p.read_text())
        nested.append({'path': str(p.relative_to(A)), 'actual_nested_runs': len(rows)})
    out = {
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'status': 'PASS', 'schema': 'audit_relative_self_excluding_root_retention_v1',
        'self_excluded': [DEST.name],
        'root_reproduction_receipt_sha256': digest(A / FILES[0]),
        'scope': 'Completed actual root V1 failure and V2 success; full streams, receipts, exact revisions and comparison differences. No foreign source PDF or private scratch retained.',
        'parsed_complete_JSON_files': parsed_json,
        'actual_nested_run_inventories': nested,
        'actual_nested_runs_total': sum(x['actual_nested_runs'] for x in nested),
        'original_substantive_turns': 1, 'new_substantive_attempts': 0,
        'files': [{'path': str(p.relative_to(A)), 'bytes': p.stat().st_size,
                   'sha256': digest(p)} for p in sorted(paths)],
    }
    DEST.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'members': len(paths), 'parsed_JSON': parsed_json,
                      'nested_runs': out['actual_nested_runs_total'], 'sha256': digest(DEST)}))


if __name__ == '__main__':
    main()

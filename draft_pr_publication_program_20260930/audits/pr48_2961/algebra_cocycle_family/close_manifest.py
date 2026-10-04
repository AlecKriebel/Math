#!/usr/bin/env python3
"""ROOT-launched, self-only closure. Never execute through this family's driver.

The actual outer capture is outside this tree and completes after this child exits.
Historical capture modes remain historical. This manifest binds final full modes.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import sys

assert __debug__ and sys.flags.optimize == 0
FAMILY = Path(__file__).resolve().parent
EXPECTED_FAMILY = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr48_2961/algebra_cocycle_family')
assert FAMILY == EXPECTED_FAMILY and not EXPECTED_FAMILY.is_symlink()
MANIFEST = FAMILY / 'MANIFEST.json'
ORIGINAL = FAMILY.parent / 'ORIGINAL_PREPARATION_MANIFEST.json'
ORIGINAL_SHA = '278e4fd39b5a13c7a181e3f7d494420c41ea4082fa8ab9add34229671a1be3b4'
EXPECTED_OWNED_PATHS_SHA = '3bf8f86ec149b80968bc32c3184ee48cb7df8abe498e7e0181c56a6b9ef48770'
EXPECTED_DIRECTORY_PATHS_SHA = '309211964aab4b22b38fa202189072959e6cb240c0f72ea9c3e4580767f76849'
EXPECTED_PAYLOAD_COUNT = 489
EXPECTED_DIRECTORY_COUNT = 95
EXPECTED_CAPTURE_COUNT = 85


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strict_load(body):
    def pairs(items):
        out = {}
        for key, value in items:
            assert key not in out, 'duplicate JSON key'
            out[key] = value
        return out
    def invalid(value):
        raise AssertionError('nonfinite JSON: ' + value)
    return json.loads(body, object_pairs_hook=pairs, parse_constant=invalid)


def own_path(value):
    path = Path(value)
    if not path.is_absolute():
        path = FAMILY / path
    assert FAMILY in path.parents and not path.is_symlink()
    assert path.resolve() == path
    assert stat.S_ISREG(path.lstat().st_mode)
    return path


def check_ref(ref):
    path = own_path(ref['path'])
    body = path.read_bytes()
    assert type(ref['bytes']) is int and len(body) == ref['bytes']
    assert digest(body) == ref['sha256']
    return body


def aware_utc(value):
    parsed = datetime.fromisoformat(value)
    assert parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0
    return parsed


def inventory():
    files, directories = [], [FAMILY]
    for path in sorted(FAMILY.rglob('*')):
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode), 'symlink excluded'
        if stat.S_ISDIR(mode):
            directories.append(path)
        else:
            assert stat.S_ISREG(mode), 'special file excluded'
            if path != MANIFEST:
                files.append(path)
    file_names = [p.relative_to(FAMILY).as_posix() for p in files]
    directory_names = sorted('.' if p == FAMILY else p.relative_to(FAMILY).as_posix() for p in directories)
    assert len(files) == EXPECTED_PAYLOAD_COUNT
    assert len(directories) == EXPECTED_DIRECTORY_COUNT
    assert digest(('\n'.join(sorted(file_names)) + '\n').encode()) == EXPECTED_OWNED_PATHS_SHA
    assert digest(('\n'.join(directory_names) + '\n').encode()) == EXPECTED_DIRECTORY_PATHS_SHA
    assert not (FAMILY / 'tmp').exists()
    assert all(p.suffix.lower() not in {'.pdf', '.png', '.sqlite', '.db'} for p in files)
    return files, directories


def original_reference_readback():
    body = ORIGINAL.read_bytes()
    assert digest(body) == ORIGINAL_SHA
    assert ORIGINAL.stat().st_mode & 0o7777 == 0o444
    original = strict_load(body)
    assert len(original['files']) == original['files_count'] == 574
    for entry in original['files']:
        path = FAMILY.parent / entry['path']
        assert path.resolve() == path and not path.is_symlink()
        assert stat.S_ISREG(path.lstat().st_mode)
        data = path.read_bytes()
        assert len(data) == entry['bytes'] and digest(data) == entry['sha256']
        assert path.stat().st_mode & 0o7777 == entry['full_mode'] == 0o444
    assert len(original['owned_directory_bindings']) == 110
    for entry in original['owned_directory_bindings']:
        path = FAMILY.parent / entry['path']
        assert path.resolve() == path and not path.is_symlink() and path.is_dir()
        assert path.stat().st_mode & 0o7777 == entry['full_mode']
    return {'path': str(ORIGINAL), 'bytes': len(body), 'sha256': digest(body),
            'payload_count': 574, 'declared_directory_count': 110,
            'all_reference_bodies_and_full_modes_read': True,
            'foreign_paths_modified': False}


def actual_capture_readback():
    rows = []
    folders = sorted((FAMILY / 'captures').iterdir())
    assert len(folders) == EXPECTED_CAPTURE_COUNT and all(p.is_dir() for p in folders)
    for folder in folders:
        cap_path = folder / 'CAPTURE.json'
        cap = strict_load(cap_path.read_bytes())
        pre = strict_load((folder / 'PRELAUNCH.json').read_bytes())
        assert cap['schema'] == 'pr48-algebra-family-real-command-capture/v1'
        assert pre['schema'] == 'pr48-algebra-family-real-prelaunch/v1'
        assert cap['argv'] == pre['argv'] and cap['cwd'] == pre['cwd']
        assert cap['operator_pid'] == pre['operator_pid']
        assert type(cap['operator_pid']) is int and cap['operator_pid'] > 0
        assert type(cap['child_pid']) is int and cap['child_pid'] > 0
        assert type(cap['exit_code']) is int and cap['exit_code'] == cap['expected_exit'] == pre['expected_exit']
        assert cap['status'] == 'PASS_EXPECTED_EXIT'
        assert cap['operator'] == pre['operator']
        assert cap['child_source'] == pre['child_source']
        assert check_ref(cap['operator']) == (folder / 'prelaunch_operator.py').read_bytes()
        assert check_ref(cap['prelaunch']) == (folder / 'PRELAUNCH.json').read_bytes()
        for stream in ['stdout', 'stderr']:
            assert own_path(cap[stream]['path']) == folder / (stream + '.bin')
            check_ref(cap[stream])
        members = {'CAPTURE.json', 'PRELAUNCH.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
        if cap['child_source'] is not None:
            assert pre['source_copied_before_launch'] is True
            assert check_ref(cap['child_source']) == (folder / 'prelaunch_child_source.py').read_bytes()
            members.add('prelaunch_child_source.py')
        else:
            assert pre['source_copied_before_launch'] is False
        assert {p.name for p in folder.iterdir()} == members
        assert aware_utc(pre['created_utc']) <= aware_utc(cap['started_utc']) <= aware_utc(cap['finished_utc'])
        rows.append({'path': cap_path.relative_to(FAMILY).as_posix(), 'child_pid': cap['child_pid'],
                     'exit_code': cap['exit_code'], 'bytes': cap_path.stat().st_size,
                     'sha256': digest(cap_path.read_bytes()),
                     'complete_prelaunch_source_and_split_streams_read': True})
    assert sum(row['exit_code'] == 1 for row in rows) == 2
    return rows


def verify_manifest():
    files, directories = inventory()
    data = MANIFEST.read_bytes()
    mf = strict_load(data)
    assert mf['schema'] == 'pr48-algebra-cocycle-family-self-only-closure/v1'
    assert mf['self_excluded'] == ['MANIFEST.json']
    assert MANIFEST.stat().st_mode & 0o7777 == 0o444
    assert len(mf['files']) == len(files) == mf['files_count']
    assert [row['path'] for row in mf['files']] == [p.relative_to(FAMILY).as_posix() for p in files]
    for path, row in zip(files, mf['files']):
        body = path.read_bytes()
        assert len(body) == row['bytes'] and digest(body) == row['sha256']
        assert path.stat().st_mode & 0o7777 == row['full_mode'] == 0o444
    expected_dirs = sorted('.' if p == FAMILY else p.relative_to(FAMILY).as_posix() for p in directories)
    assert [row['path'] for row in mf['owned_directories']] == expected_dirs
    for row in mf['owned_directories']:
        path = FAMILY if row['path'] == '.' else FAMILY / row['path']
        assert path.stat().st_mode & 0o7777 == row['full_mode']
        assert row['full_mode'] == (0o755 if path == FAMILY else 0o700)
    original_reference_readback()
    assert actual_capture_readback() == mf['complete_prior_actual_captures']
    return {'status': 'PASS_SELF_ONLY_FROZEN_BODY_MODE_TOPOLOGY_READBACK',
            'manifest_sha256': digest(data), 'manifest_bytes': len(data),
            'payload_count': len(files), 'files_with_self': len(files) + 1,
            'directory_count_including_root': len(directories),
            'complete_prior_actual_capture_count': len(mf['complete_prior_actual_captures'])}


if __name__ == '__main__':
    assert len(sys.argv) <= 2 and (len(sys.argv) == 1 or sys.argv[1] == '--verify')
    if len(sys.argv) == 2:
        result = verify_manifest()
    else:
        assert not MANIFEST.exists(), 'closure is exclusive and cannot rewrite a prior manifest'
        files, directories = inventory()
        verdict = strict_load((FAMILY / 'VERDICT.json').read_bytes())
        assert verdict['status'] == 'PASS_PARTIAL_MATHEMATICS_REPAIR_PROVENANCE'
        assert verdict['problem_status'] == 'unsolved' and verdict['mandatory_mathematical_corrections'] == []
        assert [v['id'] for v in verdict['mandatory_corrections']] == ['S1']
        assert verdict['full_target_resolved'] is False and verdict['new_substantive_turns'] == 0
        assert verdict['original_substantive_turns'] == 2 and verdict['turn_limit'] == 5
        assert verdict['budget_counted_audit_turns'] == 0 and verdict['ROOT_acceptance'] is False
        assert verdict['closure_status'] == 'PENDING_ROOT_ACTUAL_CAPTURE'
        for binding in verdict['evidence_bindings']:
            check_ref(binding)
        removal = strict_load((FAMILY / 'FOREIGN_INPUT_REMOVAL.json').read_bytes())
        assert removal['status'] == 'PASS_ALL_29_FOREIGN_BODIES_REMOVED' and len(removal['removed']) == 29
        assert all(row['removed'] is True and not (FAMILY / row['path']).exists() for row in removal['removed'])
        original_binding = original_reference_readback()
        actual_captures = actual_capture_readback()
        payload = []
        for path in files:
            data = path.read_bytes()
            path.chmod(0o444)
            payload.append({'path': path.relative_to(FAMILY).as_posix(), 'bytes': len(data),
                            'sha256': digest(data), 'full_mode': path.stat().st_mode & 0o7777})
        for path in directories:
            path.chmod(0o755 if path == FAMILY else 0o700)
        directory_rows = sorted([{'path': '.' if p == FAMILY else p.relative_to(FAMILY).as_posix(),
                                  'full_mode': p.stat().st_mode & 0o7777} for p in directories],
                                key=lambda row: row['path'])
        mf = {'schema': 'pr48-algebra-cocycle-family-self-only-closure/v1',
              'actual_closing_child_pid': os.getpid(), 'created_utc': datetime.now(timezone.utc).isoformat(),
              'scope': str(FAMILY), 'self_excluded': ['MANIFEST.json'],
              'files_count': len(payload), 'files': payload,
              'owned_directories_count_including_root': len(directory_rows), 'owned_directories': directory_rows,
              'all_4096_permission_bits_recorded': True, 'original_reference': original_binding,
              'complete_prior_actual_capture_count': len(actual_captures),
              'complete_prior_actual_captures': actual_captures,
              'historical_capture_modes_preserved': True,
              'outer_capture_outside_family_scope': True,
              'outer_capture_status_at_child_closure': 'PENDING_ACTUAL_CHILD_EXIT',
              'outer_capture_rule': 'ROOT completes the genuine external split-stream capture only after this child exits. It is not a payload or retrospective family event.',
              'mathematical_verdict': verdict['mathematical_verdict'],
              'mandatory_provenance_repair': 'S1: prior-report upstream key ABSENT with local {} fallback, not null.',
              'full_target_resolved': False, 'novelty_claim': False, 'original_substantive_turns': 2,
              'turn_limit': 5, 'new_substantive_turns': 0, 'budget_counted_audit_turns': 0,
              'foreign_PDF_OCR_pixel_raw_or_SQL_bodies_owned': False,
              'ROOT_acceptance': False, 'repaired_candidate_acceptance': False,
              'native_transition': False, 'merge': False, 'paper': False, 'DOI': False, 'tracker_row': False}
        with MANIFEST.open('x') as handle:
            handle.write(json.dumps(mf, indent=2) + '\n')
        MANIFEST.chmod(0o444)
        result = verify_manifest()
    result['actual_pid'] = os.getpid()
    result['finished_utc'] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(result, indent=2))

#!/usr/bin/env python3
"""Read-only own closure verifier; one explicitly dated QUEUE observation."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import math
import os
import re
import stat
import sys

assert __debug__ and sys.flags.optimize == 0
F = Path(__file__).resolve().parent
EXPECTED = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr46_30004438/acceptance_source_adversary_family')
R = Path('/Users/alec/Documents/Math')
assert F == EXPECTED and not EXPECTED.is_symlink()
SELF = 'SELF_MANIFEST.json'
QUEUE = R / 'unsolved_math_prioritization/QUEUE.md'
COMMIT = 'e491808c3544ff44e8526d9b24857b5c9ca64208'
BLOB = 'd60e9b1df63bebb7b49af7bbb6c6ed64c83681d0'
Q_SHA = '31dd1f9857c4dcb04138d30d8fb480a97d860bcd5f74a4a32eadb554d032ee94'
PINS_SHA = 'a784fadfa5334b0f9a21b3484de0808d874f7a3c314b55aee2e085ccdae7f6b7'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            assert key not in value, 'duplicate JSON key'
            value[key] = item
        return value
    def invalid(value):
        raise AssertionError('nonfinite JSON ' + value)
    def finite(value):
        result = float(value)
        assert math.isfinite(result)
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid, parse_float=finite)


def equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def utc(value):
    assert type(value) is str
    result = datetime.fromisoformat(value)
    assert result.tzinfo is not None and result.utcoffset().total_seconds() == 0
    assert result <= datetime.now(timezone.utc)
    return result


def regular(path):
    assert path.is_absolute() and path.resolve() == path
    assert not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode)
    assert all(not p.is_symlink() for p in path.parents)
    return path


def inventory():
    files, dirs = [], [F]
    for path in sorted(F.rglob('*')):
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode)
        if stat.S_ISDIR(mode):
            dirs.append(path)
        else:
            assert stat.S_ISREG(mode)
            if path.name != SELF or path.parent != F:
                files.append(path)
    assert not (F / 'PRIVATE_MODEL').exists() and not (F / 'MODE_PROBE').exists()
    assert all(p.suffix.lower() not in {'.pdf', '.png', '.sqlite', '.db'} for p in files)
    parents = {'.'} | {q.as_posix() for p in files for q in PurePosixPath(p.relative_to(F).as_posix()).parents}
    assert {'.' if p == F else p.relative_to(F).as_posix() for p in dirs} == parents
    return files, dirs


def own_ref(ref):
    assert type(ref) is dict and type(ref['path']) is str
    path = Path(ref['path'])
    if not path.is_absolute():
        assert '..' not in path.parts
        path = F / path
    assert F in path.parents
    raw = regular(path).read_bytes()
    assert type(ref['bytes']) is int and ref['bytes'] >= 0
    assert type(ref['sha256']) is str and re.fullmatch('[0-9a-f]{64}', ref['sha256'])
    assert len(raw) == ref['bytes'] and sha(raw) == ref['sha256']
    # Historical own refs retain their observed mode; the self manifest binds frozen modes.
    return raw


def captures():
    rows = []
    for path in sorted((F / 'captures').glob('*/CAPTURE.json')):
        cap = load(path.read_bytes())
        pre = load((path.parent / 'PRELAUNCH.json').read_bytes())
        assert cap['schema'] == 'pr46-source-adversary-real-command-capture/v1'
        assert pre['schema'] == 'pr46-source-adversary-real-prelaunch/v1'
        assert equal(cap['argv'], pre['argv']) and cap['cwd'] == pre['cwd'] == str(R)
        assert type(cap['argv']) is list and cap['argv'] and all(type(x) is str for x in cap['argv'])
        assert type(cap['operator_pid']) is int and cap['operator_pid'] == pre['operator_pid'] > 0
        assert type(cap['child_pid']) is int and cap['child_pid'] > 0
        assert type(cap['exit_code']) is int and type(cap['expected_exit']) is int
        assert equal(cap['expected_exit'], pre['expected_exit'])
        expected = 'PASS_EXPECTED_EXIT' if cap['exit_code'] == cap['expected_exit'] else 'FAIL_UNEXPECTED_EXIT'
        assert cap['status'] == expected
        for key in ['operator', 'prelaunch', 'stdout', 'stderr']:
            own_ref(cap[key])
        assert own_ref(cap['operator']) == (path.parent / 'prelaunch_operator.py').read_bytes()
        assert own_ref(cap['prelaunch']) == (path.parent / 'PRELAUNCH.json').read_bytes()
        members = {'CAPTURE.json', 'PRELAUNCH.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
        if cap['child_source'] is not None:
            assert equal(cap['child_source'], pre['child_source'])
            assert own_ref(cap['child_source']) == (path.parent / 'prelaunch_child_source.py').read_bytes()
            assert pre['source_copied_before_launch'] is True
            members.add('prelaunch_child_source.py')
        else:
            assert pre['child_source'] is None and pre['source_copied_before_launch'] is False
        assert {p.name for p in path.parent.iterdir()} == members
        clocks = [utc(pre['created_utc']), utc(cap['started_utc']), utc(cap['finished_utc'])]
        assert clocks == sorted(clocks)
        rows.append({'path': path.relative_to(F).as_posix(), 'bytes': path.stat().st_size,
                     'sha256': sha(path.read_bytes()), 'child_pid': cap['child_pid'],
                     'exit_code': cap['exit_code'], 'status': cap['status'],
                     'complete_prelaunch_source_and_split_streams_read': True})
    assert len(rows) == 11 and sum(row['exit_code'] != 0 for row in rows) == 1
    return rows


def original_bodies():
    raw = (F / 'ORIGINAL_FAMILY_BODY_PINS.json').read_bytes()
    assert sha(raw) == PINS_SHA
    pins = load(raw)
    assert pins['schema'] == 'pr46-source-adversary-original-payload-body-preservation/v1'
    assert type(pins['original_payload_count']) is int and pins['original_payload_count'] == len(pins['files']) == 51
    names = [ref['path'] for ref in pins['files']]
    assert names == sorted(set(names))
    assert sha(('\n'.join(names) + '\n').encode()) == pins['original_paths_sha256'] == '6784ff56af6f874984f1836eb6d49b691f3974172ae4a39aa2d84d29a7e49b7b'
    assert pins['body_mutation_permitted'] is False and pins['closure_mode_freeze_permitted'] is True
    for ref in pins['files']:
        own_ref(ref)
    return {'original_payload_count': 51, 'all_original_payload_bodies_identical': True,
            'original_body_pins_sha256': sha(raw)}


def live_ref(row):
    path = regular(Path(row['path']))
    assert F not in path.parents
    raw = path.read_bytes()
    assert type(row['bytes']) is int and row['bytes'] >= 0 and len(raw) == row['bytes']
    assert type(row['sha256']) is str and sha(raw) == row['sha256']
    assert type(row['full_mode']) is int and 0 <= row['full_mode'] <= 0o7777
    assert stat.S_IMODE(path.stat().st_mode) == row['full_mode']
    return {k: row[k] for k in ['path', 'bytes', 'sha256', 'full_mode']}


def qualification():
    raw = (F / 'DATED_NATIVE_CLOSURE_QUALIFICATION_V2.json').read_bytes()
    assert sha(raw) == Q_SHA
    q = load(raw)
    assert q['schema'] == 'pr46-source-adversary-dated-native-closure-qualification/v2'
    for key, expected in [('original_external_binding_count', 2611), ('original_live_binding_count', 2610),
                          ('dated_native_qualification_count', 1), ('observation_primary_actual_child', 55086),
                          ('actual_failed_ROOT_closure_child', 84831), ('actual_failed_ROOT_closure_exit', 1)]:
        assert type(q[key]) is int and q[key] == expected
    for key in ['production_imported_compiled_executed', 'fresh_native_authority', 'future_acceptance_approved', 'own_closure_launched']:
        assert q[key] is False
    assert q['source_verdict_unchanged'] == 'REJECT_MANDATORY_SOURCE_CORRECTION' and q['mandatory_finding_unchanged'] == 'S1'
    assert q['all_other_original_bindings_remain_exact_live_body_and_full_mode'] is True
    assert q['ROOT_diagnosis_V1_not_used'] is True and q['ROOT_diagnosis_V2_supersedes_V1_normalization_error'] is True
    assert q['historical_commit'] == COMMIT and q['historical_git_mode'] == '100644'
    assert q['historical_git_path'] == 'unsolved_math_prioritization/QUEUE.md' and q['historical_blob_sha1'] == BLOB
    old = load((F / 'OWN_INPUT_READ_BINDINGS.json').read_bytes())
    queue_rows = [row for row in old['external_bindings'] if row['path'] == str(QUEUE)]
    assert len(queue_rows) == 1 and equal(queue_rows[0], q['original_native_observation'])
    expected = {'path': str(QUEUE), 'bytes': 382073, 'sha256': 'a1210bbc36ebd6cd4ced6480edb0fe5e01d28bac59ebd2cf4910312853e396be', 'full_mode': 0o644}
    normalized = {k: queue_rows[0][k] for k in expected}
    assert equal(normalized, expected)
    primary = load((F / 'PRIVATE_CONTROL_RESULT.json').read_bytes())
    primary_cap = load((F / 'captures/private_source_controls/CAPTURE.json').read_bytes())
    assert primary['actual_pid'] == primary_cap['child_pid'] == 55086
    assert primary['main_before'] == primary['main_after'] == COMMIT
    assert equal(primary['native13_before'], primary['native13_after']) and len(primary['native13_before']) == 13
    for key in ['native13_before', 'native13_after']:
        selected = [row for row in primary[key] if row['path'] == q['historical_git_path']]
        assert len(selected) == 1
        relative_expected = dict(expected, path=q['historical_git_path'])
        assert equal(selected[0], relative_expected)
    assert primary_cap['started_utc'] == q['observation_started_utc'] and primary_cap['finished_utc'] == q['observation_finished_utc']
    git_body = own_ref(q['captured_historical_body'])
    assert len(git_body) == expected['bytes'] and sha(git_body) == expected['sha256']
    assert hashlib.sha1(b'blob ' + str(len(git_body)).encode() + b'\0' + git_body).hexdigest() == BLOB
    recovery = [load(own_ref(ref)) for ref in q['recovery_captures']]
    wanted = [['/usr/bin/git', 'show', COMMIT + ':unsolved_math_prioritization/QUEUE.md'],
              ['/usr/bin/git', 'ls-tree', COMMIT, '--', 'unsolved_math_prioritization/QUEUE.md'],
              ['/usr/bin/git', 'cat-file', 'commit', COMMIT]]
    assert len(recovery) == 3
    for cap, argv in zip(recovery, wanted):
        assert equal(cap['argv'], argv) and cap['cwd'] == str(R)
        assert type(cap['exit_code']) is int and cap['exit_code'] == 0 and cap['status'] == 'PASS_EXPECTED_EXIT'
        assert own_ref(cap['stderr']) == b''
        assert utc(cap['started_utc']) >= utc(q['observation_finished_utc'])
    assert own_ref(recovery[0]['stdout']) == git_body
    assert own_ref(recovery[1]['stdout']) == ('100644 blob ' + BLOB + '\tunsolved_math_prioritization/QUEUE.md\n').encode()
    commit_body = own_ref(recovery[2]['stdout'])
    assert hashlib.sha1(b'commit ' + str(len(commit_body)).encode() + b'\0' + commit_body).hexdigest() == COMMIT
    own_ref(q['original_payload_body_pins'])
    receipts = q['new_fixed_external_receipts']
    a = F.parent
    root_capture = a.parent / 'pr45_9900007/root_pr46_acceptance_adverse_source_closure_actual_capture'
    required = [root_capture / n for n in ['CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin']]
    required += [a / 'ROOT_ACCEPTANCE_ADVERSE_CLOSURE_FAILED_INPUT_DIAGNOSIS_V2.json',
                 a / 'ROOT_ACCEPTANCE_ADVERSE_SOURCE_CLOSURE_PRELAUNCH_SOURCE.py']
    assert [ref['path'] for ref in receipts] == list(map(str, required))
    extra = [live_ref(ref) for ref in receipts]
    cap = load(required[0].read_bytes())
    assert cap['schema'] == 'root-explicit-command-capture/v1'
    assert equal(cap['argv'], ['/usr/bin/python3', '-B', str(F / 'close_source_adversary.py')])
    assert cap['cwd'] == str(R) and type(cap['pid']) is int and cap['pid'] == 84831
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['operator_unchanged'] is True
    assert type(cap['exit_code']) is int and cap['exit_code'] == 1 and cap['status'] == 'FAIL'
    assert type(cap['expected_exit_code']) is int and cap['expected_exit_code'] == 0
    assert utc(cap['started_utc']) <= utc(cap['finished_utc'])
    assert {p.name for p in root_capture.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
    assert sha(required[1].read_bytes()) == cap['operator_sha256']
    for name, actual_path in [('stdout', required[2]), ('stderr', required[3])]:
        ref = cap[name]
        body = actual_path.read_bytes()
        assert ref['path'] == name + '.bin' and type(ref['bytes']) is int
        assert len(body) == ref['bytes'] and sha(body) == ref['sha256']
    assert required[2].read_bytes() == b''
    assert b'foreign = external_bindings()' in required[3].read_bytes() and b'AssertionError' in required[3].read_bytes()
    assert required[5].read_bytes() == (F / 'close_source_adversary.py').read_bytes()
    diagnosis = load(required[4].read_bytes())
    assert diagnosis['schema'] == 'pr46-root-adverse-closure-failed-input-diagnosis/v2'
    assert type(diagnosis['actual_failed_child']) is int and diagnosis['actual_failed_child'] == 84831
    assert type(diagnosis['total']) is int and diagnosis['total'] == 2611 and len(diagnosis['changed']) == 1
    assert equal(diagnosis['changed'][0]['old'], expected)
    assert diagnosis['changed'][0]['now']['path'] == str(QUEUE)
    assert diagnosis['family_closed'] is False and diagnosis['future_acceptance_approved'] is False
    return q, expected, extra


def external_bindings():
    q, historical, extra = qualification()
    old = load((F / 'OWN_INPUT_READ_BINDINGS.json').read_bytes())
    assert type(old['normalized_external_count']) is int and old['normalized_external_count'] == len(old['external_bindings']) == 2611
    assert len({row['path'] for row in old['external_bindings']}) == 2611
    checked = []
    for row in old['external_bindings']:
        if row['path'] == str(QUEUE):
            checked.append(dict(historical, validation_kind='DATED_NATIVE_BODY_AND_DATED_FULL_MODE_OBSERVATION',
                                captured_historical_body=q['captured_historical_body'], current_native_authority=False))
        else:
            checked.append(dict(live_ref(row), validation_kind='EXACT_LIVE_BODY_AND_FULL_MODE'))
    assert sum(row['validation_kind'] == 'EXACT_LIVE_BODY_AND_FULL_MODE' for row in checked) == 2610
    assert len(extra) == 6
    return {'original_count': 2611, 'original_live_count': 2610, 'dated_native_count': 1,
            'original_bindings': checked, 'additional_fixed_external_receipts': extra,
            'future_acceptance_approved': False}


def check_verdict():
    verdict = load((F / 'VERDICT.json').read_bytes())
    assert verdict['schema'] == 'pr46-acceptance-source-adversary-verdict/v1'
    assert verdict['verdict'] == 'REJECT_MANDATORY_SOURCE_CORRECTION'
    assert verdict['preparation_manifest_sha256'] == 'd97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab'
    assert [row['id'] for row in verdict['mandatory_corrections']] == ['S1']
    assert verdict['production_imported_compiled_executed'] is False and verdict['future_acceptance_approved'] is False
    for key, expected in [('original_substantive_attempts', 0), ('original_source_verification_responses', 1),
                          ('new_substantive_attempts', 0), ('audit_turns', 0)]:
        assert type(verdict[key]) is int and verdict[key] == expected
    for ref in verdict['evidence_bindings']:
        own_ref(ref)
    control = load((F / 'CLOSURE_REPAIR_CONTROL_RESULT.json').read_bytes())
    cap = load((F / 'captures/dated_native_closure_repair_controls/CAPTURE.json').read_bytes())
    assert control['schema'] == 'pr46-source-adversary-dated-native-repair-controls/v1'
    assert control['status'] == 'PASS_DATED_NATIVE_REPAIR_CONTROLS'
    assert type(control['actual_pid']) is int and control['actual_pid'] == cap['child_pid']
    assert type(control['original_live_bindings_checked']) is int and control['original_live_bindings_checked'] == 2610
    assert type(control['dated_native_observations_checked']) is int and control['dated_native_observations_checked'] == 1
    assert type(control['additional_fixed_external_receipts_checked']) is int and control['additional_fixed_external_receipts_checked'] == 6
    assert type(control['original_payload_bodies_preserved']) is int and control['original_payload_bodies_preserved'] == 51
    assert type(control['assertions']) is int and control['assertions'] == 45236
    assert len(control['rejected_mutants']) == len(set(control['rejected_mutants'])) == 32
    assert control['original_bindings_body_sha256'] == sha((F / 'OWN_INPUT_READ_BINDINGS.json').read_bytes())
    assert control['qualification_body_sha256'] == Q_SHA and control['original_payload_pins_body_sha256'] == PINS_SHA
    assert utc(cap['started_utc']) <= utc(control['started_utc']) <= utc(control['finished_utc']) <= utc(cap['finished_utc'])
    assert equal(cap['argv'], ['/usr/bin/python3', '-B', str(F / 'dated_native_closure_repair_controls.py')])
    output_keys = ['status', 'actual_pid', 'assertions', 'original_live_bindings_checked',
                   'dated_native_observations_checked', 'additional_fixed_external_receipts_checked',
                   'original_payload_bodies_preserved']
    assert equal(load(own_ref(cap['stdout'])), {key: control[key] for key in output_keys})
    assert own_ref(cap['stderr']) == b''
    assert control['production_imported_compiled_executed'] is False and control['own_closure_launched'] is False
    assert control['fresh_native_authority'] is False and control['mandatory_finding_unchanged'] == 'S1'
    assert control['future_acceptance_approved'] is False and control['source_verdict_unchanged'] == verdict['verdict']
    assert type(cap['exit_code']) is int and cap['exit_code'] == 0
    return verdict


def verify():
    files, dirs = inventory()
    raw = (F / SELF).read_bytes()
    mf = load(raw)
    assert mf['schema'] == 'pr46-acceptance-source-adversary-self-closure/v2'
    assert set(mf) == {'schema', 'actual_closing_child_pid', 'created_utc', 'self_excluded', 'files_count',
                       'files', 'directories', 'all_4096_permission_bits_recorded', 'complete_prior_actual_captures',
                       'original_payload_body_preservation', 'qualified_external_readback', 'verdict',
                       'preparation_manifest_sha256', 'actual_prior_failed_ROOT_closure_child',
                       'actual_prior_failed_ROOT_closure_exit', 'dated_native_scope',
                       'production_imported_compiled_executed', 'fresh_native_authority', 'future_acceptance_approved',
                       'outer_capture_outside_family', 'outer_capture_status_at_child_closure', 'outer_capture_rule',
                       'original_substantive_attempts', 'original_source_verification_responses',
                       'new_substantive_attempts', 'audit_turns', 'native_index_remote_or_paper_DOI_tracker_mutation'}
    assert type(mf['actual_closing_child_pid']) is int and mf['actual_closing_child_pid'] > 0
    utc(mf['created_utc'])
    assert mf['all_4096_permission_bits_recorded'] is True and mf['outer_capture_outside_family'] is True
    assert mf['outer_capture_status_at_child_closure'] == 'PENDING_ACTUAL_CHILD_EXIT'
    for key in ['production_imported_compiled_executed', 'fresh_native_authority', 'future_acceptance_approved',
                'native_index_remote_or_paper_DOI_tracker_mutation']:
        assert mf[key] is False
    for key, expected in [('original_substantive_attempts', 0), ('original_source_verification_responses', 1),
                          ('new_substantive_attempts', 0), ('audit_turns', 0),
                          ('actual_prior_failed_ROOT_closure_child', 84831), ('actual_prior_failed_ROOT_closure_exit', 1)]:
        assert type(mf[key]) is int and mf[key] == expected
    assert mf['self_excluded'] == [SELF] and type(mf['files_count']) is int
    assert len(files) == mf['files_count'] == len(mf['files']) == 80 and len(dirs) == 13
    assert sha(('\n'.join(p.relative_to(F).as_posix() for p in files) + '\n').encode()) == '555d45acdd92a8fd001bcf2dc2a2cbd00f0553111df175bad5a118968340b006'
    assert [p.relative_to(F).as_posix() for p in files] == [r['path'] for r in mf['files']]
    for path, row in zip(files, mf['files']):
        body = path.read_bytes()
        assert type(row['bytes']) is int and len(body) == row['bytes'] and sha(body) == row['sha256']
        assert type(row['full_mode']) is int and stat.S_IMODE(path.stat().st_mode) == row['full_mode'] == 0o444
    assert stat.S_IMODE((F / SELF).stat().st_mode) == 0o444
    actual_dirs = sorted('.' if p == F else p.relative_to(F).as_posix() for p in dirs)
    assert actual_dirs == [r['path'] for r in mf['directories']]
    for row in mf['directories']:
        path = F if row['path'] == '.' else F / row['path']
        assert type(row['full_mode']) is int and stat.S_IMODE(path.stat().st_mode) == row['full_mode'] == (0o755 if path == F else 0o700)
    verdict = check_verdict()
    assert verdict['verdict'] == mf['verdict']
    assert verdict['preparation_manifest_sha256'] == mf['preparation_manifest_sha256']
    assert equal(captures(), mf['complete_prior_actual_captures'])
    assert equal(original_bodies(), mf['original_payload_body_preservation'])
    assert equal(external_bindings(), mf['qualified_external_readback'])
    return {'status': 'PASS_STRICT_FROZEN_SOURCE_ADVERSARY_DATED_NATIVE_READBACK', 'manifest_sha256': sha(raw),
            'payload_files': len(files), 'files_with_self': len(files) + 1, 'directories_including_root': len(dirs),
            'prior_actual_captures': len(mf['complete_prior_actual_captures']),
            'original_live_bindings_checked': 2610, 'dated_native_observations_checked': 1,
            'additional_fixed_external_receipts_checked': 6, 'original_payload_bodies_preserved': 51,
            'source_verdict': mf['verdict'], 'future_acceptance_approved': False}


if __name__ == '__main__':
    result = verify()
    result.update(actual_pid=os.getpid(), finished_utc=datetime.now(timezone.utc).isoformat())
    print(json.dumps(result, indent=2))

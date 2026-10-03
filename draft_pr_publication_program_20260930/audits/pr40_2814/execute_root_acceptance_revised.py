#!/usr/bin/env python3
"""SOURCE ONLY: proposed ROOT child capture for revised PR40 acceptance.

No helper is imported here. ROOT must fully review this wrapper, all five helper
sources and a new adversarial review before explicit execution. ROOT supplies
the completed PR39 mirror and fresh main13 only after PR39 integration. Existing
captures, partial output directories and failed stages are never overwritten.
"""
import argparse
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import traceback
import uuid

R = Path('/Users/alec/Documents/Math')
A = R / 'draft_pr_publication_program_20260930/audits/pr40_2814'
S = A / 'acceptance_execution_preparation_family/integration_source_revision_v2'
C = A / 'reviewed_candidate'
PREVIOUS = A.parent / 'pr39_9500008/state_mirror_bindings.json'
PREP = 'e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba'
SOURCE_HASHES = {
    'pr40_guards.py': '1382ae7f88bd6ace26eb8be09386c7c5d1076e20cfe470824a54945377e936d6',
    'seal_final_evidence.py': 'acca1d4777cce70f3bf209bfd2b5a722c7ecbb4bfc6873a6736b187f8404772c',
    'integrate_reviewed_partial.py': 'e181ed1725b096608481325b2b60f07654b699b1ce802929251d189d936cac5d',
    'state_mirror_reconciliation.py': 'f6dc5e80df90391c8b2e869219ebda5eb3a231a0018efa54efa2c6554e926f1e',
    'verify_post_acceptance.py': 'd31b99ec427f5e07d40e58ccd5c913e1dd8281e959ce214f3d184a2917fcae38',
}
NATIVE13 = (
    'unsolved_math_prioritization/QUEUE.md',
    'unsolved_math_prioritization/state.json',
    'unsolved_math_prioritization/history.jsonl',
    'unsolved_math_prioritization/catalog.json',
    'unsolved_math_prioritization/assessments.json',
    'unsolved_math_prioritization/queue.py',
    'unsolved_math_prioritization/policy.json',
    'unsolved_math_prioritization/manifest.json',
    'unsolved_math_prioritization/cache/problems.json',
    'unsolved_math_prioritization/cache/research_results.json',
    'unsolved_math_prioritization/cache/catalog.sqlite',
    'unsolved_math_prioritization/review_v2/related_target_groups.json',
    'draft_pr_publication_program_20260930/inventory.json',
)
ALLOWED = {
    'overlay': {'unsolved_math_prioritization/QUEUE.md'},
    'finalize': {'draft_pr_publication_program_20260930/inventory.json'},
    'mirror': {'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl'},
}
GATE_NAMES = ('final-plan', 'final-receipt', 'final-manifest',
              'reconciliation-capture', 'previous-mirror', 'fresh-preimage')
CURRENT_PR_AFTER_ACCEPTANCE = 41


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    require(type(value) is str and re.fullmatch(r'[0-9a-f]{64}', value), 'Explicit SHA256 required')
    return value


def strict_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(strict_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def required(value, expected, context):
    require(type(value) is dict, context + ': complete object required')
    for key, item in expected.items():
        require(key in value and strict_equal(value[key], item), context + ': wrong/missing typed field ' + key)


def parse(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError('Nonfinite JSON: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def utc(value):
    require(type(value) is str and value and value == value.strip(), 'UTC clock must be a nonempty stripped string')
    result = dt.datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    require(result.tzinfo is not None and result.utcoffset() == dt.timedelta(0), 'Aware UTC clock required')
    return result


def read_regular(path):
    path = Path(path)
    require(path.is_absolute() and path.is_relative_to(R), 'Path must belong to repository')
    for ancestor in [path, *path.parents]:
        require(not ancestor.is_symlink(), 'Symlink path or ancestor: ' + str(path))
        if ancestor == R:
            break
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as stream:
        mode = os.fstat(stream.fileno()).st_mode
        require(stat.S_ISREG(mode), 'Nonregular file: ' + str(path))
        return stream.read(), stat.S_IMODE(mode)


def repo_path(name):
    require(type(name) is str and name and '\\' not in name and '\0' not in name, 'Canonical relative path required')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name, 'Unsafe relative path')
    return R / name


def row(path):
    raw, mode = read_regular(path)
    return {'path': str(Path(path).relative_to(R)), 'bytes': len(raw), 'sha256': sha(raw)}, mode


def exact(base, names):
    require(base.is_dir() and not base.is_symlink(), 'Unsafe exact closure root')
    files, directories = set(), set()
    for path in base.rglob('*'):
        require(not path.is_symlink() and (path.is_file() or path.is_dir()), 'Unsafe entry in exact closure')
        (directories if path.is_dir() else files).add(path.relative_to(base).as_posix())
    expected_dirs = {p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    require(files == set(names) and directories == expected_dirs, 'Full exact file/directory closure differs')


def fresh_inputs():
    require(len(NATIVE13) == len(set(NATIVE13)) == 13, 'Literal native13 names changed')
    rows, modes = [], {}
    for name in NATIVE13:
        raw, mode = read_regular(R / name)
        rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
        modes[name] = mode
    return rows, modes


def check_preparation():
    raw, mode = read_regular(S / 'PREPARATION_MANIFEST.json')
    require(sha(raw) == PREP and mode == 0o444, 'Revised preparation manifest bytes/mode changed')
    value = parse(raw)
    required(value, {'self_excluded_paths': ['PREPARATION_MANIFEST.json'], 'files_count': 17,
                     'directories': [], 'foreign_excluded_prefixes': [], 'scratch_exclusions': []}, 'Exact revised preparation')
    require(type(value['files']) is list and len(value['files']) == 17, 'Exact revised17+self closure required')
    names = {'PREPARATION_MANIFEST.json'}
    for item in value['files']:
        require(type(item) is dict and type(item['path']) is str, 'Typed preparation row required')
        path = repo_path(str(S.relative_to(R)) + '/' + item['path'])
        require(path.is_relative_to(S) and item['path'] not in names, 'Repeated/outside preparation member')
        names.add(item['path'])
        body, mode = read_regular(path)
        require(type(item['bytes']) is int and item['bytes'] >= 0 and len(body) == item['bytes'] and
                sha(body) == digest(item['sha256']) and mode == 0o444, 'Preparation member bytes/mode changed')
        if item['path'].endswith('.json'):
            parse(body)
    exact(S, names)
    for name, expected in SOURCE_HASHES.items():
        require(sha(read_regular(S / name)[0]) == expected, 'One of five revised source pins changed')


def complete_plan(path, expected_sha):
    raw, mode = read_regular(path)
    require(sha(raw) == digest(expected_sha), 'Complete ROOT plan pin differs')
    expected = parse(read_regular(S / 'DRAFT_FINAL_PLAN.json')[0])
    expected.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',
                    root_full_current_read_completed=True, root_full_whole_read_completed=True,
                    independent_whole_current_pass=True, preparation_manifest_sha256=PREP)
    plan = parse(raw)
    require(strict_equal(plan, expected), 'Entire plan permits only reviewed flags/status and revised preparation pin')
    return raw, mode, plan


def fresh_review(value):
    required(value, {'approved_by_root': True}, 'Actual fresh ROOT review')
    created = utc(value['created_utc'])
    require(created <= dt.datetime.now(dt.timezone.utc), 'Fresh ROOT UTC clock is in the future')
    require(type(value['reason_date_utc']) is str and value['reason_date_utc'] == created.date().isoformat(), 'Fresh reason date must equal actual UTC creation date')
    require(type(value['reason']) is str and value['reason'] == value['reason'].strip() and
            len(value['reason']) >= 40 and len(value['reason'].split()) >= 6, 'Substantive ROOT-reviewed dated rebase reason required')
    require(type(value['current_head']) is str and re.fullmatch('[0-9a-f]{40}', value['current_head']), 'Actual fresh main HEAD required')
    rr = value['files']
    require(type(rr) is list and len(rr) == 13, 'Complete ordered native13 review required')
    for name, item in zip(NATIVE13, rr):
        require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'} and item['path'] == name and
                type(item['bytes']) is int and item['bytes'] >= 0, 'Exact ordered typed fresh13 row required')
        digest(item['sha256'])
    digest(value['whole_queue_sha256'])


def write_new(path, data, mode=0o600):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(data)
        os.fchmod(stream.fileno(), mode)
        stream.flush()
        os.fsync(stream.fileno())


def fsync_directory(path):
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def final_output_check(output, plan, plan_path, source, stdout, started, finished):
    names = {'FINAL_MANIFEST.json', 'ROOT_FINAL_RECONCILIATION.json', 'ROOT_REVIEWED_SCOPE.json'}
    exact(output, names)
    blobs = {name: read_regular(output / name) for name in names}
    require(all(mode == 0o444 for raw, mode in blobs.values()), 'Final three files must remain0444')
    manifest_raw = blobs['FINAL_MANIFEST.json'][0]
    manifest = parse(manifest_raw)
    required(manifest, {'schema': 'pr40-final-root-two-member-closure/v1', 'self_excluded': ['FINAL_MANIFEST.json'],
                        'files_count': 2}, 'Actual final manifest')
    require(type(manifest['files']) is list and len(manifest['files']) == 2, 'Exact two final members required')
    members = set()
    for item in manifest['files']:
        require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'} and item['path'] in names - {'FINAL_MANIFEST.json'} and
                item['path'] not in members and type(item['bytes']) is int and item['bytes'] >= 0, 'Exact final typed member required')
        members.add(item['path'])
        body = blobs[item['path']][0]
        require(len(body) == item['bytes'] and sha(body) == digest(item['sha256']), 'Actual final member bytes differ')
    require(members == names - {'FINAL_MANIFEST.json'}, 'Final manifest membership differs')
    require(strict_equal(parse(blobs['ROOT_REVIEWED_SCOPE.json'][0]), plan), 'Entire final scope copy differs')
    receipt_raw = blobs['ROOT_FINAL_RECONCILIATION.json'][0]
    receipt = parse(receipt_raw)
    required(receipt, {'schema': 'pr40-actual-final-reconciliation/v1', 'status': 'PASS',
                       'actual_root_reconciliation': True, 'pr': 40, 'problem_id': 2814,
                       'preparation_manifest_sha256': PREP, 'entire_scope': plan,
                       'bindings_before': plan['immutable_evidence_references'],
                       'bindings_after': plan['immutable_evidence_references'],
                       'root_reviewed_plan': row(plan_path)[0], 'reconciliation_source': row(source)[0],
                       'science_helpers_executed': False, 'new_substantive_attempts': 0,
                       'audit_turns': 0, 'shared_mutations': False}, 'Entire actual final receipt')
    require(utc(started) <= utc(receipt['utc']) <= utc(finished), 'Actual final receipt outside child UTC interval')
    require(utc(started) <= utc(manifest['utc']) <= utc(finished), 'Actual final manifest outside child UTC interval')
    required(parse(stdout), {'status': 'PASS', 'final_receipt_sha256': sha(receipt_raw),
                            'final_manifest_sha256': sha(manifest_raw), 'science_helpers_executed': False,
                            'shared_mutations': False}, 'Complete actual final child stdout')
    return {'output_directory': str(output.relative_to(R)), 'entire_final_scope_and_receipt_checked': True,
            'files': [row(output / name)[0] for name in sorted(names)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['final', 'preflight', 'overlay', 'prepush', 'finalize', 'mirror', 'post'])
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--reviewed-runner-source-sha256', required=True)
    parser.add_argument('--reviewed-plan-sha256')
    parser.add_argument('--final-output')
    parser.add_argument('--reviewed-gate-arguments-sha256')
    parser.add_argument('--reviewed-previous-mirror-sha256')
    parser.add_argument('--reviewed-fresh-main-sha256')
    parser.add_argument('--reviewed-automatic-merge-sha256')
    args = parser.parse_args()
    phase = args.phase
    require(args.execute, 'Explicit ROOT outer --execute required after complete review')
    runner_path = Path(__file__).resolve()
    require(runner_path == A / 'execute_root_acceptance_revised.py', 'Exact adjacent revised runner path required')
    runner_raw, runner_mode = read_regular(runner_path)
    require(sha(runner_raw) == digest(args.reviewed_runner_source_sha256), 'Explicit complete ROOT runner source pin differs')
    require(sys.platform == 'darwin', 'Reviewed atomic directory publication requires macOS')
    library = ctypes.CDLL(None, use_errno=True)
    rename = library.renamex_np
    rename.argtypes, rename.restype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int
    require(subprocess.check_output(['git', 'branch', '--show-current'], cwd=R, timeout=30).strip() == b'main', 'Stay on main')
    check_preparation()
    filename = {'final': 'seal_final_evidence.py', 'mirror': 'state_mirror_reconciliation.py',
                'post': 'verify_post_acceptance.py'}.get(phase, 'integrate_reviewed_partial.py')
    source = S / filename
    raw, source_mode = read_regular(source)
    guards_raw, guards_mode = read_regular(S / 'pr40_guards.py')
    argv = ['/usr/bin/python3', '-B', str(source)]
    reviews = {}
    def retain_review(path, data, mode):
        name = str(path.relative_to(R))
        pin = {'bytes': len(data), 'sha256': sha(data), 'mode': mode}
        require(name not in reviews or strict_equal(reviews[name], pin), 'Conflicting complete ROOT review pins')
        reviews[name] = pin
    final_output, plan, plan_path = None, None, None
    if phase == 'final':
        plan_path = A / 'ROOT_REVIEWED_FINAL_PLAN.json'
        plan_raw, plan_mode, plan = complete_plan(plan_path, args.reviewed_plan_sha256)
        retain_review(plan_path, plan_raw, plan_mode)
        final_output = repo_path(str(A.relative_to(R)) + '/' + args.final_output) if type(args.final_output) is str else None
        require(final_output is not None and final_output.parent == A and not final_output.exists() and
                not final_output.is_symlink(), 'Explicit new absent direct-child final output basename required')
        reserved_captures = {'root_final_reconciliation_actual_capture'} | {
            'root_integration_' + name + '_actual_capture'
            for name in ['preflight', 'overlay', 'prepush', 'finalize', 'mirror', 'post']}
        require(final_output.name not in reserved_captures, 'Final output may not reserve any phase capture name')
        argv += ['--execute', '--preparation-manifest-sha256', PREP,
                 '--plan', str(plan_path.relative_to(R)), '--plan-sha256', args.reviewed_plan_sha256,
                 '--output', final_output.name]
    else:
        path = A / 'ROOT_REVIEWED_GATE_ARGUMENTS.json'
        gate_raw, gate_mode = read_regular(path)
        require(sha(gate_raw) == digest(args.reviewed_gate_arguments_sha256), 'Complete ROOT gate arguments pin differs')
        gate_review = parse(gate_raw)
        required(gate_review, {'approved_by_root': True, 'root_full_runner_and_helper_review_completed': True,
                              'new_independent_runner_review_completed': True}, 'Genuine complete ROOT gate review')
        gates = gate_review['explicit_arguments']
        keys = {'preparation-manifest-sha256'} | set(GATE_NAMES) | {name + '-sha256' for name in GATE_NAMES}
        require(type(gates) is dict and set(gates) == keys and len(keys) == 13 and
                all(type(value) is str for value in gates.values()), 'Exact thirteen complete explicit gate strings required')
        require(gates['preparation-manifest-sha256'] == PREP, 'Old preparation pin forbidden')
        require(gates['previous-mirror'] == str(PREVIOUS.relative_to(R)), 'Literal actual completed PR39 proposal required')
        require(digest(gates['previous-mirror-sha256']) == digest(args.reviewed_previous_mirror_sha256), 'Explicit reviewed predecessor39 SHA differs')
        for name in GATE_NAMES:
            artifact = repo_path(gates[name])
            require(artifact == PREVIOUS if name == 'previous-mirror' else
                    artifact.is_relative_to(A) and not artifact.is_relative_to(C) and not artifact.is_relative_to(S),
                    'Actual final gate outside selected audit/source/current rules')
            body, mode = read_regular(artifact)
            require(sha(body) == digest(gates[name + '-sha256']), 'Complete actual final gate pin differs')
            retain_review(artifact, body, mode)
        previous = parse(read_regular(PREVIOUS)[0])
        require(type(previous['entries']) is list and len(previous['entries']) == 29 and
                39 in previous['required_completed_prs'] and 40 not in previous['required_completed_prs'], 'Completed predecessor29 entries with39 and without40 required')
        fresh = parse(read_regular(repo_path(gates['fresh-preimage']))[0])
        fresh_review(fresh)
        retain_review(path, gate_raw, gate_mode)
        if phase not in ('mirror', 'post'):
            argv.append(phase)
        argv.append('--execute')
        for key in sorted(gates):
            argv += ['--' + key, gates[key]]
    before, modes_before = fresh_inputs()
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, timeout=30).decode().strip()
    require(re.fullmatch('[0-9a-f]{40}', head), 'Actual main HEAD must be complete')
    if phase == 'preflight':
        require(gates['fresh-preimage'] == str((A / 'ROOT_FRESH_MAIN_PREIMAGES.json').relative_to(R)) and
                digest(args.reviewed_fresh_main_sha256) == gates['fresh-preimage-sha256'], 'Explicit complete fresh root13 review pin required')
        require(strict_equal(before, fresh['files']) and fresh['current_head'] == head and
                sha(read_regular(R / NATIVE13[0])[0]) == fresh['whole_queue_sha256'], 'Entire actual fresh HEAD/native13/queue differs')
    if phase == 'overlay':
        path = A / 'ROOT_AUTOMATIC_MERGE_INSPECTION.json'
        review_raw, review_mode = read_regular(path)
        require(sha(review_raw) == digest(args.reviewed_automatic_merge_sha256), 'Full automatic-merge review pin differs')
        reviewed = parse(review_raw)
        required(reviewed, {'approved_by_root': True}, 'Actual automatic-merge review')
        queue_raw, unused_mode = read_regular(R / NATIVE13[0])
        require(sha(queue_raw) == digest(reviewed['whole_queue_sha256']), 'Entire reviewed automatic queue differs')
        retain_review(path, review_raw, review_mode)
        argv += ['--merge-queue-preimage-sha256', sha(queue_raw)]
    destination = A / ('root_final_reconciliation_actual_capture' if phase == 'final' else 'root_integration_' + phase + '_actual_capture')
    require(not destination.exists() and not destination.is_symlink(), 'Inspect existing capture; no overwrite or retry')
    require(final_output is None or final_output != destination, 'Final output must differ from capture directory')
    stage = A / (destination.name + '.stage.' + uuid.uuid4().hex)
    stage.mkdir(mode=0o700)
    write_new(stage / 'prelaunch_source.py', raw, source_mode)
    if phase != 'final':
        write_new(stage / 'prelaunch_guards.py', guards_raw, guards_mode)
    record = {'schema': 'pr40-root-genuine-child-and-native13-capture/v1', 'phase': phase,
              'source_sha256': sha(raw), 'source_mode': source_mode, 'guards_sha256': sha(guards_raw),
              'guards_mode': guards_mode, 'preparation_manifest_sha256': PREP,
              'argv': argv, 'cwd': str(A), 'started_utc': stamp(), 'actual_execution': False,
              'completed': False, 'stdin_supplied': False, 'head_before': head,
              'fresh_native13_before': before, 'fresh_native13_modes_before': modes_before,
              'outer_runner': {'path': str(runner_path.relative_to(R)), 'bytes': len(runner_raw),
                               'sha256': sha(runner_raw), 'mode': runner_mode},
              'complete_root_review_pins': reviews, 'pid': None, 'exit_code': None, 'timed_out': False,
              'original_substantive_attempts': 0, 'new_substantive_attempts': 0, 'audit_turns': 0,
              'full_problem_solved': False, 'novelty_claimed': False, 'partial_valid': True,
              'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None,
              'paper_or_new_doi_or_tracker': False, 'current_pr_after_acceptance': CURRENT_PR_AFTER_ACCEPTANCE}
    child, out, err = None, b'', b''
    errors = []
    try:
        require(read_regular(source) == (raw, source_mode) and
                read_regular(S / 'pr40_guards.py') == (guards_raw, guards_mode), 'Prelaunch source bytes or mode changed')
        child = subprocess.Popen(argv, cwd=A, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        record.update(pid=child.pid, actual_execution=True)
        try:
            out, err = child.communicate(timeout=180)
        except subprocess.TimeoutExpired:
            record['timed_out'] = True
            child.kill()
            out, err = child.communicate()
        record.update(completed=True, exit_code=child.returncode)
    except BaseException:
        errors.append(traceback.format_exc())
        if child is not None:
            try:
                if child.poll() is None:
                    child.kill()
                out, err = child.communicate()
                record.update(completed=True, exit_code=child.returncode)
            except BaseException:
                errors.append(traceback.format_exc())
    record['finished_utc'] = stamp()
    write_new(stage / 'stdout.bin', out)
    write_new(stage / 'stderr.bin', err)
    native_ok, checks_ok = False, False
    try:
        after, modes_after = fresh_inputs()
        after_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, timeout=30).decode().strip()
        changes = {left['path'] for left, right in zip(before, after) if not strict_equal(left, right)}
        mode_changes = {name for name in NATIVE13 if modes_before[name] != modes_after[name]}
        allowed = ALLOWED.get(phase, set())
        native_ok = changes <= allowed and not mode_changes and after_head == head
        record.update(fresh_native13_after=after, fresh_native13_modes_after=modes_after,
                      head_after=after_head, actual_changed_native_inputs=sorted(changes),
                      actual_changed_native_modes=sorted(mode_changes), allowed_changed_native_inputs=sorted(allowed),
                      allowed_changed_native_modes=[])
        check_preparation()
        require(read_regular(runner_path) == (runner_raw, runner_mode), 'Outer runner source or mode changed during child')
        require(read_regular(source) == (raw, source_mode) and read_regular(S / 'pr40_guards.py') == (guards_raw, guards_mode), 'Helper source bytes/mode changed during child')
        for name, pin in reviews.items():
            current_raw, current_mode = read_regular(R / name)
            require(len(current_raw) == pin['bytes'] and sha(current_raw) == pin['sha256'] and
                    current_mode == pin['mode'], 'Complete ROOT review bytes/mode changed during child')
        require(utc(record['started_utc']) <= utc(record['finished_utc']), 'Actual outer UTC clocks reversed')
        if phase == 'final' and record['actual_execution'] is True and record['exit_code'] == 0 and not record['timed_out']:
            record['actual_final_output_inspection'] = final_output_check(final_output, plan, plan_path, source,
                                                                         out, record['started_utc'], record['finished_utc'])
        if phase in ('finalize', 'mirror', 'post') and record['actual_execution'] is True and record['exit_code'] == 0:
            required(parse(read_regular(R / NATIVE13[-1])[0]), {'current_pr': CURRENT_PR_AFTER_ACCEPTANCE,
                                                              'completed_count': 30}, 'Actual postPR40 next-target inventory')
        checks_ok = True
    except BaseException:
        errors.append(traceback.format_exc())
    record.update(stdout={'path': 'stdout.bin', 'bytes': len(out), 'sha256': sha(out)},
                  stderr={'path': 'stderr.bin', 'bytes': len(err), 'sha256': sha(err)},
                  independent_native13_and_HEAD_checks_pass=native_ok,
                  source_and_complete_review_checks_pass=checks_ok, outer_errors=errors)
    passed = (record['actual_execution'] is True and record['completed'] is True and
              type(record['pid']) is int and record['pid'] > 0 and type(record['exit_code']) is int and record['exit_code'] == 0 and
              not record['timed_out'] and native_ok and checks_ok and not errors)
    record['status'] = 'PASS' if passed else 'FAIL'
    record['publication_protocol'] = 'Fsynced complete stage; macOS RENAME_EXCL; parent fsync; outer actual exit0 witnesses completion'
    write_new(stage / 'CAPTURE.json', (json.dumps(record, indent=2) + '\n').encode())
    names = {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}
    if phase != 'final':
        names.add('prelaunch_guards.py')
    exact(stage, names)
    require(read_regular(stage / 'prelaunch_source.py') == (raw, source_mode), 'Captured source bytes/mode differ')
    if phase != 'final':
        require(read_regular(stage / 'prelaunch_guards.py') == (guards_raw, guards_mode), 'Captured guards bytes/mode differ')
    fsync_directory(stage)
    if rename(os.fsencode(stage), os.fsencode(destination), 0x00000004) != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), str(destination))
    fsync_directory(A)
    print(json.dumps({'phase': phase, 'status': record['status'], 'pid': record['pid'],
                      'exit_code': record['exit_code'], 'capture_sha256': sha(read_regular(destination / 'CAPTURE.json')[0]),
                      'native13_ok': native_ok, 'checks_ok': checks_ok}))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())

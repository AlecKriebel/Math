#!/usr/bin/env python3
"""SOURCE ONLY: proposed ROOT child capture for the revised PR39 acceptance.

No helper is imported. ROOT must review this complete source and the fresh
adversarial review before execution. ROOT owns reviewed-plan activation and
all Git/remote writes. Existing captures and failed stages are never retried.
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
A = R / 'draft_pr_publication_program_20260930/audits/pr39_9500008'
S = A / 'acceptance_execution_preparation_family/integration_source_revision'
PREP = '522cf5062ffcb1aa9c60cb0054063b0f2801378446f2288d7f85e81ee9a70ae7'
SOURCE_HASHES = {
    'pr39_guards.py': '1fbeaf479f893e413b9a85d5f72a974491219c9d0f7cfaab7149a2977a5d9723',
    'seal_final_evidence.py': 'd1ee189304b48f1b21b54b3adcd82e22fce6a8d03d0df663dfde10bc3081df8b',
    'integrate_reviewed_partial.py': '42be7ce20e4231a83b72a01c01b01c28f8790a09f54ee4783b7734440661612a',
    'state_mirror_reconciliation.py': '0958f01368a3e41bcf56098bc28c66ad8d4e70c69a8a46e78877b035f5a53e9d',
    'verify_post_acceptance.py': 'a072de3cacdeedc6ac546b7023baf5ffb6e2474200a5d5abe4c5ba21a60fc1e7',
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
GATE_NAMES = ('whole-manifest', 'root-final-receipt', 'whole-scope-contract',
              'root-final-manifest', 'reconciliation-capture')


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
    require(type(value) is str, 'UTC clock must be a string')
    result = dt.datetime.fromisoformat(value)
    require(result.tzinfo is not None and result.utcoffset() == dt.timedelta(0), 'Aware UTC clock required')
    return result


def read_regular(path):
    path = Path(path)
    require(path.is_absolute() and path.is_relative_to(R), 'Path must belong to repository')
    for ancestor in [path, *path.parents]:
        require(not ancestor.is_symlink(), 'Symlink path or ancestor: ' + str(path))
        if ancestor == R:
            break
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, 'rb') as stream:
        mode = os.fstat(stream.fileno()).st_mode
        require(stat.S_ISREG(mode), 'Nonregular file: ' + str(path))
        return stream.read(), stat.S_IMODE(mode)


def repo_path(name):
    require(type(name) is str and name and '\\' not in name and '\0' not in name, 'Canonical relative path required')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name, 'Unsafe relative path')
    return R / name


def fresh_inputs():
    require(len(NATIVE13) == len(set(NATIVE13)) == 13, 'Literal native13 names changed')
    rows, modes = [], {}
    for name in NATIVE13:
        raw, mode = read_regular(R / name)
        rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
        modes[name] = mode
    return rows, modes


def check_preparation():
    raw, unused_mode = read_regular(S / 'PREPARATION_MANIFEST.json')
    require(sha(raw) == PREP, 'Revised preparation manifest changed')
    value = parse(raw)
    require(value['self_excluded'] == ['PREPARATION_MANIFEST.json'] and
            type(value['files_count']) is int and value['files_count'] == 17 and
            type(value['files']) is list and len(value['files']) == 17, 'Exact revised17+self closure required')
    names = {'PREPARATION_MANIFEST.json'}
    for row in value['files']:
        path = repo_path(str(S.relative_to(R)) + '/' + row['path'])
        require(path.is_relative_to(S) and row['path'] not in names, 'Repeated/outside preparation member')
        names.add(row['path'])
        body, mode = read_regular(path)
        require(type(row['bytes']) is int and len(body) == row['bytes'] and sha(body) == digest(row['sha256']), 'Preparation member changed')
    actual, directories = set(), set()
    for path in S.rglob('*'):
        require(not path.is_symlink(), 'Symlink in source closure')
        require(path.is_dir() or path.is_file(), 'Special entry in source closure')
        (directories if path.is_dir() else actual).add(path.relative_to(S).as_posix())
    expected_dirs = {p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    require(actual == names and directories == expected_dirs, 'Full preparation closure changed')
    for name, expected in SOURCE_HASHES.items():
        require(sha(read_regular(S / name)[0]) == expected, 'One of five revised source pins changed')


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['final', 'preflight', 'overlay', 'prepush', 'finalize', 'mirror', 'post'])
    parser.add_argument('--reviewed-plan-sha256')
    parser.add_argument('--reviewed-gate-arguments-sha256')
    parser.add_argument('--reviewed-fresh-main-sha256')
    parser.add_argument('--reviewed-automatic-merge-sha256')
    args = parser.parse_args()
    phase = args.phase
    runner_path = Path(__file__).resolve()
    require(runner_path == A / 'execute_root_acceptance_revised.py', 'Exact adjacent revised runner path required')
    runner_raw, runner_mode = read_regular(runner_path)
    require(sys.platform == 'darwin', 'Reviewed atomic directory publication requires macOS')
    library = ctypes.CDLL(None, use_errno=True)
    rename = library.renamex_np
    rename.argtypes, rename.restype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int
    require(subprocess.check_output(['git', 'branch', '--show-current'], cwd=R).strip() == b'main', 'Stay on main')
    check_preparation()
    filename = {'final': 'seal_final_evidence.py', 'mirror': 'state_mirror_reconciliation.py',
                'post': 'verify_post_acceptance.py'}.get(phase, 'integrate_reviewed_partial.py')
    source = S / filename
    raw, source_mode = read_regular(source)
    guards_raw, guards_mode = read_regular(S / 'pr39_guards.py')
    argv = ['/usr/bin/python3', '-B', str(source)]
    reviews = {}
    if phase == 'final':
        path = A / 'ROOT_REVIEWED_FINAL_PLAN.json'
        plan_raw, unused_mode = read_regular(path)
        require(sha(plan_raw) == digest(args.reviewed_plan_sha256), 'Complete ROOT plan pin differs')
        expected = parse(read_regular(S / 'DRAFT_FINAL_PLAN.json')[0])
        expected.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',
                        root_full_current_read_completed=True, root_full_whole_scope_read_completed=True,
                        independent_whole_current_pass=True, preparation_manifest_sha256=PREP)
        require(strict_equal(parse(plan_raw), expected), 'Entire plan permits only reviewed flags/status and revised preparation pin')
        reviews[str(path.relative_to(R))] = {'bytes': len(plan_raw), 'sha256': sha(plan_raw)}
        argv += ['--execute', '--preparation-manifest-sha256', PREP,
                 '--plan', str(path.relative_to(R)), '--plan-sha256', args.reviewed_plan_sha256]
    else:
        path = A / 'ROOT_REVIEWED_GATE_ARGUMENTS.json'
        gate_raw, unused_mode = read_regular(path)
        require(sha(gate_raw) == digest(args.reviewed_gate_arguments_sha256), 'Complete ROOT gate arguments pin differs')
        gates = parse(gate_raw)['explicit_arguments']
        keys = {'preparation-manifest-sha256', 'previous-mirror-sha256'}
        keys |= set(GATE_NAMES) | {n + '-sha256' for n in GATE_NAMES}
        require(type(gates) is dict and set(gates) == keys and all(type(v) is str for v in gates.values()), 'Exact complete explicit gate map required')
        require(gates['preparation-manifest-sha256'] == PREP, 'Old preparation pin forbidden')
        prior_raw, unused_mode = read_regular(A.parent / 'pr38_2765/state_mirror_bindings.json')
        require(sha(prior_raw) == digest(gates['previous-mirror-sha256']), 'Actual predecessor mirror pin differs')
        for name in GATE_NAMES:
            artifact = repo_path(gates[name])
            require(artifact.is_relative_to(A) and not artifact.is_relative_to(A / 'reviewed_candidate') and
                    not artifact.is_relative_to(S), 'Final gate must belong to selected audit outside source/current closure')
            require(sha(read_regular(artifact)[0]) == digest(gates[name + '-sha256']), 'Actual final gate artifact pin differs')
        reviews[str(path.relative_to(R))] = {'bytes': len(gate_raw), 'sha256': sha(gate_raw)}
        if phase not in ('mirror', 'post'):
            argv.append(phase)
        argv.append('--execute')
        for key in sorted(gates):
            argv += ['--' + key, gates[key]]
    before, modes_before = fresh_inputs()
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip()
    if phase in ('preflight', 'overlay'):
        name = 'ROOT_FRESH_MAIN_PREIMAGES.json' if phase == 'preflight' else 'ROOT_AUTOMATIC_MERGE_INSPECTION.json'
        expected_sha = args.reviewed_fresh_main_sha256 if phase == 'preflight' else args.reviewed_automatic_merge_sha256
        path = A / name
        review_raw, unused_mode = read_regular(path)
        require(sha(review_raw) == digest(expected_sha), 'Full fresh/automatic queue review pin differs')
        reviewed = parse(review_raw)
        queue_raw, unused_mode = read_regular(R / NATIVE13[0])
        require(sha(queue_raw) == digest(reviewed['whole_queue_sha256']), 'Entire reviewed queue differs')
        if phase == 'preflight':
            require(strict_equal(before, reviewed['files']) and reviewed['head'] == head, 'Complete fresh main HEAD/native13 review differs')
        reviews[str(path.relative_to(R))] = {'bytes': len(review_raw), 'sha256': sha(review_raw)}
        argv += ['--' + ('fresh-queue' if phase == 'preflight' else 'merge-queue') + '-preimage-sha256', sha(queue_raw)]
    destination = A / ('root_final_reconciliation_actual_capture' if phase == 'final' else 'root_integration_' + phase + '_actual_capture')
    require(not destination.exists() and not destination.is_symlink(), 'Inspect existing capture; no overwrite or retry')
    stage = A / (destination.name + '.stage.' + uuid.uuid4().hex)
    stage.mkdir(mode=0o700)
    write_new(stage / 'prelaunch_source.py', raw, source_mode)
    if phase != 'final':
        write_new(stage / 'prelaunch_guards.py', guards_raw, guards_mode)
    record = {'schema': 'pr39-root-genuine-child-and-native13-capture/v2', 'phase': phase,
              'source_sha256': sha(raw), 'source_mode': source_mode, 'guards_sha256': sha(guards_raw),
              'guards_mode': guards_mode, 'preparation_manifest_sha256': PREP,
              'argv': argv, 'cwd': str(A), 'started_utc': stamp(), 'actual_execution': False,
              'completed': False, 'stdin_supplied': False, 'head_before': head,
              'fresh_native13_before': before, 'fresh_native13_modes_before': modes_before,
              'outer_runner': {'path': str(runner_path.relative_to(R)), 'bytes': len(runner_raw),
                               'sha256': sha(runner_raw), 'mode': runner_mode},
              'complete_root_review_pins': reviews, 'pid': None, 'exit_code': None, 'timed_out': False}
    child, out, err = None, b'', b''
    errors = []
    try:
        require(read_regular(source) == (raw, source_mode) and
                read_regular(S / 'pr39_guards.py') == (guards_raw, guards_mode), 'Prelaunch source bytes or mode changed')
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
        after_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip()
        changes = {left['path'] for left, right in zip(before, after) if not strict_equal(left, right)}
        changes |= {name for name in NATIVE13 if modes_before[name] != modes_after[name]}
        allowed = ALLOWED.get(phase, set())
        native_ok = changes <= allowed and after_head == head
        record.update(fresh_native13_after=after, fresh_native13_modes_after=modes_after,
                      head_after=after_head, actual_changed_native_inputs=sorted(changes),
                      allowed_changed_native_inputs=sorted(allowed))
        check_preparation()
        require(read_regular(runner_path) == (runner_raw, runner_mode), 'Outer runner source or mode changed during child')
        require(read_regular(source) == (raw, source_mode) and read_regular(S / 'pr39_guards.py') == (guards_raw, guards_mode), 'Source bytes/mode changed during child')
        for name, pin in reviews.items():
            current_raw, unused_mode = read_regular(R / name)
            require(len(current_raw) == pin['bytes'] and sha(current_raw) == pin['sha256'], 'Complete ROOT review changed during child')
        require(utc(record['started_utc']) <= utc(record['finished_utc']), 'Actual outer UTC clocks reversed')
        checks_ok = True
    except BaseException:
        errors.append(traceback.format_exc())
    record.update(stdout={'path': 'stdout.bin', 'bytes': len(out), 'sha256': sha(out)},
                  stderr={'path': 'stderr.bin', 'bytes': len(err), 'sha256': sha(err)},
                  independent_native13_and_HEAD_checks_pass=native_ok,
                  source_and_complete_review_checks_pass=checks_ok, outer_errors=errors)
    passed = (record['actual_execution'] is True and record['completed'] is True and
              type(record['exit_code']) is int and record['exit_code'] == 0 and
              not record['timed_out'] and native_ok and checks_ok and not errors)
    record['status'] = 'PASS' if passed else 'FAIL'
    write_new(stage / 'CAPTURE.json', (json.dumps(record, indent=2) + '\n').encode())
    names = {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}
    if phase != 'final':
        names.add('prelaunch_guards.py')
    require({p.name for p in stage.iterdir()} == names and
            all(p.is_file() and not p.is_symlink() for p in stage.iterdir()), 'Exact capture closure differs')
    require(read_regular(stage / 'prelaunch_source.py') == (raw, source_mode), 'Captured source bytes/mode differ')
    fsync_directory(stage)
    if rename(os.fsencode(stage), os.fsencode(destination), 0x00000004) != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), str(destination))
    fsync_directory(A)
    print(json.dumps({'phase': phase, 'status': record['status'], 'pid': record['pid'],
                      'exit_code': record['exit_code'], 'capture_sha256': sha((destination / 'CAPTURE.json').read_bytes()),
                      'native13_ok': native_ok, 'checks_ok': checks_ok}))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())

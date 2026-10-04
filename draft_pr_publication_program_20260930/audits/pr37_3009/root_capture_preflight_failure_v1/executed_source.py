#!/usr/bin/env python3
"""STATIC PREPARATION: root-owned actual full replay capture, never run here.

Future root runs /usr/bin/python3 (3.9) with --execute after reading this source.
Only two fresh sibling audit directories are created: full replay output and
raw capture. No helper imports, Git/remote mutation or shared-file write.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
A = HERE.parent.parent
R = A.parents[2]
C = A / 'reviewed_candidate'
W = A / 'whole_current_source_first_family'
PY = '/usr/bin/python3'
PINS = {'current': 'ca440e7d4f378db294256e3d9a7a7b3f4e5344df562db9a2c4bb5092952dd2de',
        'dependencies': '978f8e80fbccc453ec027c428414b6e7420df0c392d3d1c669df91a66f72b263',
        'whole': '859ee278297d08853fcdbc1eefe2d6cf675e5d89c02e756a23ca1eb959dafd48',
        'replay': '4e51f166ba3f4a345b6cdd71b82ad866eef3f946fda540eb0cac09063e53a9b4'}


def require(value, message):
    if not value:
        raise ValueError(message)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def raw(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'Regular file required: ' + str(path))
    require(all(not parent.is_symlink() for parent in path.parents), 'Symlink parent rejected')
    return path.read_bytes()


def pin(path):
    data = raw(path)
    return {'path': str(Path(path).relative_to(R)), 'bytes': len(data), 'sha256': sha(data)}


def save(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def snapshot():
    cm, dm, wm = C / 'MANIFEST.json', C / 'CURRENT_PROOF_DEPENDENCIES.json', W / 'FIRST_PARTY_MANIFEST.json'
    for path, key in [(cm, 'current'), (dm, 'dependencies'), (wm, 'whole'), (W / 'replay_gate.py', 'replay')]:
        require(sha(raw(path)) == PINS[key], 'Exact closed pin changed: ' + key)
    current, dependencies, whole = json.loads(raw(cm)), json.loads(raw(dm)), json.loads(raw(wm))
    require(len(current['files']) == 96 and len(dependencies['files']) == 443 and len(whole['files']) == 1287, 'Closed counts changed')
    require(whole['self_excluded'] == ['FIRST_PARTY_MANIFEST.json'] and whole['foreign_excluded_prefixes'] == ['primary/'] and whole['bytecode_excluded_component'] == '__pycache__', 'Exact closed first-party exclusion declaration changed')
    groups = []
    for base, advertised in [(C, current['files']), (A, dependencies['files']), (W, whole['files'])]:
        require(len({z['path'] for z in advertised}) == len(advertised), 'Duplicate closed path')
        observed = []
        for row in advertised:
            relative = Path(row['path'])
            require(not relative.is_absolute() and '..' not in relative.parts and str(relative) == row['path'], 'Unsafe closed path')
            data = raw(base / row['path'])
            require(len(data) == row['bytes'] and sha(data) == row['sha256'], 'Closed member bytes changed: ' + row['path'])
            if (base / row['path']).suffix == '.json':
                json.loads(data)  # All317 baseline whole JSON parse; no malformed exceptions.
            observed.append(dict(row))
        groups.append(observed)
    current_files = {str(p.relative_to(C)) for p in C.rglob('*') if p.is_file() or p.is_symlink()}
    require(current_files == {z['path'] for z in groups[0]} | {'MANIFEST.json'}, 'Exact current recursive closure changed')
    whole_files = set()
    for path in W.rglob('*'):
        name = str(path.relative_to(W))
        require(not path.is_symlink(), 'Whole recursive symlink rejected')
        if name.startswith('primary/') or '__pycache__' in path.relative_to(W).parts:
            continue
        if path.is_file():
            whole_files.add(name)
    require(whole_files == {z['path'] for z in groups[2]} | {'FIRST_PARTY_MANIFEST.json'}, 'Exact1287 whole first-party recursive closure changed')
    return {'reviewed_candidate': groups[0] + [{'path': 'MANIFEST.json', 'bytes': len(raw(cm)), 'sha256': PINS['current']}],
            'dependencies': groups[1], 'whole_authored_members': groups[2],
            'whole_manifest_self': {'path': 'FIRST_PARTY_MANIFEST.json', 'bytes': len(raw(wm)), 'sha256': PINS['whole']}}


def shared_snapshot():
    return [pin(R / name) for name in ['unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl', 'draft_pr_publication_program_20260930/inventory.json']]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    require(args.execute and sys.version_info[:2] == (3, 9) and Path(sys.executable).resolve() == Path(PY).resolve(), 'Root explicit /usr/bin/python3 (3.9) execution required')
    out = A / 'root_source_first_private_reexecution'
    capture = A / 'root_final_whole_actual_capture'
    require(not out.exists() and not capture.exists(), 'Both root-owned output directories must be fresh; preserve/inspect prior attempt')
    before, shared_before = snapshot(), shared_snapshot()
    capture.mkdir()
    save(capture / 'BINDINGS_BEFORE.json', before)
    save(capture / 'SHARED_BEFORE.json', shared_before)
    wrapper = pin(__file__)
    replay = pin(W / 'replay_gate.py')
    argv = [PY, str(W / 'replay_gate.py'), '--repository-root', str(R), '--output-root', str(out)]
    started = utc()
    returncode = None
    child_pid = None
    failure = None
    try:
        with (capture / 'outer.stdout').open('xb') as stdout, (capture / 'outer.stderr').open('xb') as stderr:
            process = subprocess.Popen(argv, cwd=R, stdout=stdout, stderr=stderr, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0'))
            child_pid = process.pid
            try:
                returncode = process.wait(timeout=1800)
            except subprocess.TimeoutExpired:
                process.kill()
                returncode = process.wait()
                raise
        result = json.loads(raw(out / 'RESULT.json'))
        after, shared_after = snapshot(), shared_snapshot()
        require(before == after and shared_before == shared_after, 'Frozen97/443/1287+self or shared preimages changed around actual replay')
        require(pin(__file__) == wrapper, 'Actual root capture wrapper changed during execution')
        require(returncode == 0 and result['status'] == 'PASS', 'Actual root outer replay did not pass; preserve complete output')
        summary = json.loads(raw(capture / 'outer.stdout'))
        require(summary == {'status': 'PASS', 'output': str(out), 'outer_subprocess_runs': len(result['runs']), 'checks': len(result['checks'])}, 'Complete actual stdout interface differs')
        require(raw(capture / 'outer.stderr') == b'', 'Successful actual outer stderr must be empty')
        save(capture / 'BINDINGS_AFTER.json', after)
        save(capture / 'SHARED_AFTER.json', shared_after)
    except BaseException:
        failure = traceback.format_exc()
        # Keep evidence even when a member changed or result parsing failed.
        save(capture / 'CAPTURE_FAILURE.json', {'at': utc(), 'traceback': failure})
    receipt = {'schema': 'pr37-root-actual-outer-capture/v1', 'actual_execution': child_pid is not None, 'child_pid': child_pid, 'label': 'root_exact_closed_whole_replay',
               'argv': argv, 'cwd': str(R), 'started_at_utc': started, 'finished_at_utc': utc(), 'returncode': returncode,
               'status': 'CAPTURE_PASS' if failure is None else 'CAPTURE_FAIL', 'wrapper': wrapper, 'closed_replay_source': replay,
               'stdout': pin(capture / 'outer.stdout') if (capture / 'outer.stdout').exists() else None,
               'stderr': pin(capture / 'outer.stderr') if (capture / 'outer.stderr').exists() else None,
               'result': pin(out / 'RESULT.json') if (out / 'RESULT.json').is_file() else None,
               'bindings_before': pin(capture / 'BINDINGS_BEFORE.json'), 'bindings_after': pin(capture / 'BINDINGS_AFTER.json') if (capture / 'BINDINGS_AFTER.json').exists() else None,
               'shared_before': pin(capture / 'SHARED_BEFORE.json'), 'shared_after': pin(capture / 'SHARED_AFTER.json') if (capture / 'SHARED_AFTER.json').exists() else None,
               'whole_manifest_sha256': PINS['whole'], 'candidate_manifest_sha256': PINS['current'], 'dependency_manifest_sha256': PINS['dependencies'],
               'root_actual_execution_recorded_only_after_subprocess': True, 'failure': failure}
    save(capture / 'ACTUAL_OUTER_CAPTURE.json', receipt)
    print(json.dumps({'status': receipt['status'], 'actual_outer_returncode': returncode, 'capture': str(capture)}))
    if failure is not None:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

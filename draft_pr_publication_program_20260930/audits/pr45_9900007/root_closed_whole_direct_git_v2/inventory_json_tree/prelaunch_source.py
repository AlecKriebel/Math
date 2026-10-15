"""ROOT complete closed-whole inspection after personal mathematical reading."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
R = A.parents[2]
F = A / 'whole_current_source_first_family'
D = A / 'root_closed_whole_direct_git_v2'
PIN = 'b372d0fdad3ae40c6a1b82530504dd2584022f15e703b468a8631faa455f9646'
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(items):
    result = {}
    for k, v in items:
        if k in result: raise ValueError('duplicate key')
        result[k] = v
    return result
def parse(b): return json.loads(b, object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def read(p, digest=None, size=None):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    assert p.resolve(strict=True).is_relative_to(R.resolve())
    b = p.read_bytes()
    if digest is not None: assert sha(b) == digest, str(p)
    if size is not None: assert type(size) is int and len(b) == size, str(p)
    return b
def ref(p):
    b = read(p)
    return {'path': p.relative_to(R).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def dump(o): return (json.dumps(o, indent=2, allow_nan=False) + '\n').encode()
def clocks(a, b):
    first = dt.datetime.fromisoformat(a.replace('Z', '+00:00'))
    last = dt.datetime.fromisoformat(b.replace('Z', '+00:00'))
    assert first.utcoffset() == last.utcoffset() == dt.timedelta(0)
    assert first <= last <= dt.datetime.now(dt.timezone.utc)
def stream(cap, parent, key):
    z = cap[key]; p = Path(z['path'])
    if not p.is_absolute():
        p = R / p if p.parts[0] == 'draft_pr_publication_program_20260930' else parent / p
    return read(p, z['sha256'], z['bytes'])
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Unoptimized runtime required')
source = read(Path(__file__))
(A / 'ROOT_CLOSED_WHOLE_INSPECTION_PRELAUNCH_SOURCE_V2.py').write_bytes(source)
mf = parse(read(F / 'MANIFEST.json', PIN))
assert mf['schema'] == 'pr45-whole-current-source-first-family-self-only-closure/v1'
assert mf['files_count'] == len(mf['files']) == 1068 and mf['self_excluded'] == ['MANIFEST.json']
names = {z['path'] for z in mf['files']} | {'MANIFEST.json'}
assert len(names) == 1069
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()} == names
dirs = {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}
assert dirs == {z['path'] for z in mf['directories']} == {q.as_posix() for n in names for q in PurePosixPath(n).parents if str(q) != '.'}
assert len(dirs) == 153 and not any(p.is_symlink() for p in F.rglob('*'))
own_bytes = 0
for z in mf['files']:
    p = F / z['path']; raw = read(p, z['sha256'], z['bytes']); own_bytes += len(raw)
    assert z['full_mode'] == '0444' and stat.S_IMODE(p.stat().st_mode) == 0o444
    if p.suffix == '.json': parse(raw)
assert stat.S_IMODE((F / 'MANIFEST.json').stat().st_mode) == 0o444
inv = parse(read(F / 'EXTERNAL_INPUT_INVENTORY.json'))
assert inv['schema'] == 'pr45-whole-current-family-external-read-inventory/v1'
outside = inv['foreign_inputs']
assert len(outside) == len({z['path'] for z in outside}) == 1109
outside_bytes = 0
for z in outside:
    p = Path(z['path'])
    assert p.is_absolute() and str(p) == z['path'] and not p.resolve().is_relative_to(F.resolve())
    outside_bytes += len(read(p, z['sha256'], z['bytes']))
verdict = parse(read(F / 'VERDICT.json'))
read(F / 'REPORT.md', 'c0a40d932c3bf14f09cddf11db9209c1f55b9c05c2a7a75ef740ebf334e68de6')
assert verdict['schema'] == 'pr45-independent-whole-current-source-first-verdict/v1'
assert verdict['verdict'] == 'PASS_WHOLE_CURRENT_SCOPED_NO_MANDATORY_CORRECTION'
assert verdict['mandatory_corrections'] == []
assert verdict['original_substantive_attempts'] == 1 and verdict['new_substantive_attempts'] == verdict['audit_turns'] == 0
assert verdict['full_problem_solved'] is verdict['future_native_acceptance_approved'] is False
captures = []
for z in verdict['own_actual_controls']:
    p = R / z['path']; cap = parse(read(p, z['sha256'])); parent = p.parent
    assert cap['schema'] == 'pr45-own-actual-capture/v1'
    for key in ['operator_pid', 'child_pid', 'exit_code', 'start_utc', 'end_utc']: assert cap[key] == z[key]
    assert cap['source_unchanged'] is cap['operator_unchanged'] is True
    clocks(cap['start_utc'], cap['end_utc'])
    read(parent / 'prelaunch_source.py', cap['source_sha256'])
    read(parent / 'prelaunch_operator.py', cap['operator_sha256'])
    pre = parse(read(parent / 'PRELAUNCH.json'))
    for key in pre: assert pre[key] == cap[key]
    launched = parse(read(parent / 'LAUNCHED.json'))
    assert launched['child_pid'] == cap['child_pid'] and launched['operator_pid'] == cap['operator_pid']
    for channel in ['stdout', 'stderr']: stream(cap, parent, channel)
    captures.append({'capture': ref(p), 'entire_capture': cap})
own_git = parse(read(F / 'OWN_ACTUAL_READ_ONLY_GIT_CAPTURES.json'))['complete_actual_captures']
for cap in own_git:
    assert cap['argv'][0] == 'git' and cap['exit_code'] == 0 and cap['source_unchanged'] is cap['operator_unchanged'] is True
    assert type(cap['child_pid']) is int and cap['child_pid'] > 0
    p = Path(cap['capture']['path']); actual = parse(read(p, cap['capture']['sha256'], cap['capture']['bytes']))
    assert all(actual[k] == v for k, v in cap.items() if k not in ('capture', 'label'))
    clocks(cap['start_utc'], cap['end_utc'])
    read(p.parent / 'prelaunch_source.py', cap['source_sha256'])
    read(p.parent / 'prelaunch_operator.py', cap['operator_sha256'])
    for channel in ['stdout', 'stderr']: stream(cap, p.parent, channel)
    captures.append({'capture': ref(p), 'entire_capture': actual})
close = A / 'whole_current_source_first_closure_actual_capture'
cc = parse(read(close / 'CAPTURE.json', 'fb6f81abdb2dd9df34d60506ae0ea48be53f56803763459f140ffc888de99a71'))
assert cc['schema'] == 'pr45-own-complete-self-closure-capture/v1'
assert cc['operator_pid'] == mf['actual_closure_parent_pid'] == 31140
assert cc['child_pid'] == mf['actual_closure_child_pid'] == 31141 and cc['exit_code'] == 0
assert cc['completed'] is cc['actual_execution'] is cc['source_unchanged'] is cc['operator_unchanged'] is True
clocks(cc['start_utc'], cc['end_utc'])
read(close / 'prelaunch_source.py', cc['source_sha256']); read(close / 'prelaunch_operator.py', cc['operator_sha256'])
for channel in ['stdout', 'stderr']: stream(cc, close, channel)
captures.append({'capture': ref(close / 'CAPTURE.json'), 'entire_capture': cc})
fresh = parse(read(A / 'ROOT_CURRENT_INPUT_PREIMAGES.json'))
frozen = fresh['current_head']
assert frozen == '264c26d539d616b0da6f8df76478a213d20939e4'
four = {'draft_pr_publication_program_20260930/inventory.json', 'unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl'}
assert len(fresh['files']) == 13
D.mkdir(exist_ok=False)
dated_captures = []
def git(label, args):
    dest = D / label; dest.mkdir()
    operator = read(A / 'capture_root_command.py')
    (dest / 'prelaunch_source.py').write_bytes(source); (dest / 'prelaunch_operator.py').write_bytes(operator)
    argv = ['git', *args]; started = utc()
    pre = {'schema': 'pr45-root-independent-frozen-native-git/v1', 'argv': argv, 'cwd': str(R), 'operator_pid': os.getpid(), 'started_utc': started, 'source_sha256': sha(source), 'operator_sha256': sha(operator)}
    (dest / 'PRELAUNCH.json').write_bytes(dump(pre))
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    (dest / 'stdout.bin').write_bytes(out); (dest / 'stderr.bin').write_bytes(err)
    cap = {**pre, 'pid': child.pid, 'exit_code': child.returncode, 'finished_utc': utc(), 'stdout': ref(dest / 'stdout.bin'), 'stderr': ref(dest / 'stderr.bin'), 'source_unchanged': read(Path(__file__)) == source, 'operator_unchanged': read(A / 'capture_root_command.py') == operator}
    (dest / 'CAPTURE.json').write_bytes(dump(cap)); dated_captures.append(cap)
    assert child.returncode == 0 and err == b''
    return out
changes = []
for z in fresh['files']:
    n = z['path']
    if n in four:
        label = Path(n).name.replace('.', '_')
        body = git(label + '_body', ['show', frozen + ':' + n])
        tree = git(label + '_tree', ['ls-tree', frozen, '--', n])
        assert len(body) == z['bytes'] and sha(body) == z['sha256']
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        assert tree == ('100644 blob ' + blob + '\t' + n + '\n').encode()
        live = read(R / n)
        if body != live: changes.append({'path': n, 'historical_bytes': len(body), 'historical_sha256': sha(body), 'present_bytes': len(live), 'present_sha256': sha(live)})
    else: read(R / n, z['sha256'], z['bytes'])
assert len(dated_captures) == 8
result = {'schema': 'pr45-root-complete-closed-whole-inspection/v1', 'status': 'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION', 'created_utc': utc(), 'candidate_manifest_sha256': verdict['reviewed_candidate_manifest_sha256'], 'closed_whole_manifest_sha256': PIN, 'first_party_members': 1068, 'individually_bound_foreign_inputs': 1109, 'complete_VERDICT_object': verdict, 'personal_report_and_verdict_fully_read': True, 'all_first_party_whole_bytes_and_modes_checked': True, 'all_foreign_individual_whole_bytes_checked': True, 'exact_self_only_recursive_closure_checked': True, 'direct_four_independent_ROOT_Git_checks_completed': True, 'dated_four_native_source_head': frozen, 'actual_direct_four_operator_pid': os.getpid(), 'complete_dated_git_captures': dated_captures, 'complete_actual_captures_checked': captures, 'legitimate_dated_native_changes': changes, 'mandatory_defects': [], 'mandatory_corrections': [], 'original_substantive_attempts': 1, 'new_substantive_attempts': 0, 'audit_turns': 0, 'full_target_resolved_in_prior_published_literature': False, 'full_problem_solved_by_project': False, 'future_execution_approved': False, 'source_and_failure_qualification': 'All eight own controls, all retained Git captures and final external closure inspected in full. Original failed controls remain literal. Four native inputs are frozen historical Git evidence; later PR44 acceptance and descending audit queue changes require separate fresh present integration authority. Outside-family source/cache/PDF/OCR/access bytes were read in place and not copied. No full general two-process characterization or exhaustive priority is certified.'}
with (A / 'ROOT_WHOLE_CURRENT_REVIEW.json').open('xb') as handle:
    handle.write(dump(result)); handle.flush(); os.fsync(handle.fileno())
assert read(Path(__file__)) == source
print(json.dumps({'status': result['status'], 'actual_pid': os.getpid(), 'own_members': 1068, 'own_bytes': own_bytes, 'outside_inputs': 1109, 'outside_bytes': outside_bytes, 'own_captures': len(captures), 'ROOT_direct_git_captures': 8, 'future_execution_approved': False}))

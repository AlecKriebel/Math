"""Reproduce unchanged original helpers in private folders and check closed inputs."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
R = A.parents[2]
D = A / 'root_original_actual_reproduction'
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(items):
    result = {}
    for k, v in items:
        if k in result: raise ValueError('duplicate key')
        result[k] = v
    return result
def parse(b): return json.loads(b, object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def equal(x, y):
    if type(x) is not type(y): return False
    if type(x) is dict: return x.keys() == y.keys() and all(equal(x[k], y[k]) for k in x)
    if type(x) is list: return len(x) == len(y) and all(equal(a, b) for a, b in zip(x, y))
    return x == y
def read(p):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    return p.read_bytes()
def ref(p):
    b = read(p); return {'path': p.relative_to(R).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
def dump(o): return (json.dumps(o, indent=2, allow_nan=False) + '\n').encode()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Unoptimized runtime required')
source = read(Path(__file__))
(A / 'ROOT_REPRODUCTION_PRELAUNCH_SOURCE.py').write_bytes(source)
closures = []
for folder, manifest, pin, count in [(A, 'ORIGINAL_PREPARATION_MANIFEST.json', 'da37655e9b3bab420862a0c17c761e67fa9a4bc2028a328d033547249c54ad2e', 318), (A / 'projective_algebra_family', 'FAMILY_MANIFEST.json', '655e5a8c68cdc44efb78a6538000482b3c91301e1abdc15797e783526d6bea64', 34), (A / 'complex_dynamics_family', 'COMPLEX_DYNAMICS_MANIFEST.json', '5172b9086230e932fe47b028a7e242ffa9c4fda1c06f19ee41c63753f73eb18e', 33)]:
    b = read(folder / manifest); assert sha(b) == pin
    mf = parse(b); assert len(mf['files']) == mf['files_count'] == count
    names = {z['path'] for z in mf['files']} | {manifest}; assert len(names) == count + 1
    if folder == A:
        physical = set(mf['authorship_root_files']) | {manifest}
        for n in mf['authorship_directory_roots']:
            physical |= {p.relative_to(folder).as_posix() for p in (folder / n).rglob('*') if p.is_file()}
        assert physical == names
        assert {p.relative_to(folder).as_posix() for n in mf['authorship_directory_roots'] for p in [folder / n, *(folder / n).rglob('*')] if p.is_dir()} == set(mf['owned_directories'])
    else:
        physical = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
        extra = {p.relative_to(folder).as_posix() for p in (folder / 'closure_actual_capture').iterdir()} if folder.name == 'projective_algebra_family' else set()
        assert physical == names | extra
    for z in mf['files']:
        p = folder / z['path']; raw = read(p)
        assert len(raw) == z['bytes'] and sha(raw) == z['sha256'] and stat.S_IMODE(p.stat().st_mode) == z['full_mode'] == 0o444
        if p.suffix == '.json': parse(raw)
    assert stat.S_IMODE((folder / manifest).stat().st_mode) == 0o444
    closures.append({'manifest': ref(folder / manifest), 'complete_members': count, 'all_bytes_and_full_modes_checked': True})
snap = parse(read(A / 'snapshot_manifest.json'))
assert snap['original_files'] == len(snap['files']) == 13
for z in snap['files']:
    b = read(A / 'source_snapshot' / z['relative_path'])
    assert len(b) == z['bytes'] and sha(b) == z['sha256']
turns = parse(read(A / 'source_snapshot/turns.json'))
assert type(turns) is dict and turns['substantive_turns_used'] == 0 and turns['source_verification_responses'] == 1 and turns['turn_limit'] == 5
D.mkdir(exist_ok=False)
captures = []
for label, helper, receipt, count in [('author', 'verify.py', 'verification.json', 51), ('historical_independent', 'independent_review/independent_checks.py', 'independent_review/independent_results.json', 848)]:
    dest = D / label; dest.mkdir()
    original = A / 'source_snapshot' / helper
    copied = dest / original.name
    copied.write_bytes(read(original))
    (dest / 'PRELAUNCH_SOURCE.py').write_bytes(read(original))
    argv = ['/usr/bin/python3', '-B', str(copied)]; started = utc()
    pre = {'schema': 'pr46-root-unchanged-helper-actual-capture/v1', 'argv': argv, 'cwd': str(R), 'started_utc': started, 'operator_pid': os.getpid(), 'source': ref(original), 'copied_source': ref(copied), 'actual_execution': False, 'pid': None, 'exit_code': None, 'completed': False, 'stdin_supplied': False}
    (dest / 'PRELAUNCH.json').write_bytes(dump(pre))
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    (dest / 'stdout.bin').write_bytes(out); (dest / 'stderr.bin').write_bytes(err)
    cap = {**pre, 'actual_execution': True, 'pid': child.pid, 'exit_code': child.returncode, 'completed': True, 'finished_utc': utc(), 'stdout': ref(dest / 'stdout.bin'), 'stderr': ref(dest / 'stderr.bin'), 'source_unchanged': read(original) == read(copied)}
    (dest / 'CAPTURE.json').write_bytes(dump(cap)); captures.append(cap)
    assert child.returncode == 0 and err == b'' and cap['source_unchanged'] is True
    original_receipt = read(A / 'source_snapshot' / receipt)
    actual = read(dest / Path(receipt).name)
    assert actual == original_receipt and equal(parse(actual), parse(original_receipt))
    o = parse(actual); assert type(o['passed']) is int and o['passed'] == count and o['failed'] == 0 and len(o['checks']) == count
    if label == 'author': assert out == actual
    else: assert equal(parse(out), {k: v for k, v in o.items() if k != 'checks'})
result = {'schema': 'pr46-root-original-complete-reproduction/v1', 'created_utc': utc(), 'actual_operator_pid': os.getpid(), 'status': 'PASS_ROOT_UNCHANGED_ORIGINAL_REPRODUCTION', 'closures': closures, 'complete_actual_captures': captures, 'author_result': parse(read(D / 'author/verification.json')), 'historical_independent_result': parse(read(D / 'historical_independent/independent_results.json')), 'all_original13_full_bytes_checked': True, 'original_turns': turns, 'original_substantive_attempts': 0, 'new_substantive_attempts': 0, 'audit_turns': 0, 'finite_checks_are_universal_proof': False, 'future_acceptance_approved': False}
(D / 'ROOT_REPRODUCTION_RESULT.json').write_bytes(dump(result))
assert read(Path(__file__)) == source
print(json.dumps({'status': result['status'], 'actual_operator_pid': os.getpid(), 'author': 51, 'historical_independent': 848, 'all_complete_receipts_byte_and_type_exact': True}))

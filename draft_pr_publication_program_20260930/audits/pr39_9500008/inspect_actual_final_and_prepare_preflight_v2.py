"""ROOT-owned complete final-capture inspection and fresh preflight inputs; no reviewed imports."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
F = A / 'final_evidence_reconciliation'
C = A / 'root_final_reconciliation_actual_capture'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def pairs(rows):
    d = {}
    for k, v in rows:
        assert k not in d
        d[k] = v
    return d

def parse(b):
    return json.loads(b, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def read(p):
    assert not p.is_symlink() and p.is_file()
    for q in p.parents:
        assert not q.is_symlink()
    return p.read_bytes()

def pin(p):
    b = read(p)
    return {'path': str(p.relative_to(R)), 'bytes': len(b), 'sha256': sha(b)}

def check_ref(x):
    assert type(x['bytes']) is int
    p = R / x['path']
    assert not PurePosixPath(x['path']).is_absolute() and '..' not in PurePosixPath(x['path']).parts
    assert same(pin(p), x)

def utc(x):
    v = dt.datetime.fromisoformat(x)
    assert v.tzinfo is not None and v.utcoffset() == dt.timedelta(0)
    return v

def write_new(p, obj):
    b = (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode()
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    return sha(b)

def main():
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=R).strip() == b'main'
    fm = parse(read(F / 'FINAL_MANIFEST.json'))
    assert fm['files_count'] == 2 and type(fm['files_count']) is int
    assert fm['self_excluded'] == ['FINAL_MANIFEST.json']
    assert {p.name for p in F.iterdir()} == {'ROOT_FINAL_GATE.json', 'WHOLE_SCOPE_CONTRACT.json', 'FINAL_MANIFEST.json'}
    for row in fm['files']:
        b = read(F / row['path'])
        assert len(b) == row['bytes'] and sha(b) == row['sha256']
    c = parse(read(C / 'CAPTURE.json'))
    assert sha(read(C / 'CAPTURE.json')) == '7454a9179fef7deb26e21b8bdd9ce1bc2dfae91c49a12733ba8d63cbf4f09821'
    assert {p.name for p in C.iterdir()} == {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}
    assert c['status'] == 'PASS' and c['actual_execution'] is True and c['completed'] is True
    assert type(c['pid']) is int and c['pid'] == 43918 and type(c['exit_code']) is int and c['exit_code'] == 0
    assert c['timed_out'] is False and c['outer_errors'] == []
    assert c['independent_native13_and_HEAD_checks_pass'] is True and c['source_and_complete_review_checks_pass'] is True
    assert same(c['fresh_native13_before'], c['fresh_native13_after'])
    assert same(c['fresh_native13_modes_before'], c['fresh_native13_modes_after'])
    assert c['head_before'] == c['head_after'] and c['actual_changed_native_inputs'] == []
    assert sha(read(C / 'prelaunch_source.py')) == c['source_sha256']
    for k in ('stdout', 'stderr'):
        b = read(C / c[k]['path'])
        assert len(b) == c[k]['bytes'] and sha(b) == c[k]['sha256']
    assert read(C / 'stderr.bin') == b''
    receipt = parse(read(F / 'ROOT_FINAL_GATE.json'))
    scope = parse(read(F / 'WHOLE_SCOPE_CONTRACT.json'))
    plan = parse(read(A / 'ROOT_REVIEWED_FINAL_PLAN.json'))
    assert same(scope, plan) and same(receipt['entire_scope'], plan)
    assert receipt['actual_root_reconciliation'] is True and receipt['status'] == 'PASS'
    assert receipt['science_reexecution_of_current'] is False
    assert same(receipt['bindings_before'], receipt['bindings_after'])
    assert same(receipt['bindings_after'], plan['immutable_evidence_references'])
    for row in receipt['bindings_after']:
        check_ref(row)
    assert utc(c['started_utc']) <= utc(receipt['started_at_utc']) <= utc(receipt['finished_at_utc']) <= utc(c['finished_utc'])
    child = parse(read(C / 'stdout.bin'))
    assert child['status'] == 'PASS' and child['actual_administrative_reconciliation'] is True
    assert child['root_final_receipt_sha256'] == sha(read(F / 'ROOT_FINAL_GATE.json'))
    assert child['whole_scope_contract_sha256'] == sha(read(F / 'WHOLE_SCOPE_CONTRACT.json'))
    assert child['final_manifest_sha256'] == sha(read(F / 'FINAL_MANIFEST.json'))
    for k in ('new_substantive_attempts', 'audit_turns'):
        assert type(child[k]) is int and child[k] == 0
    assert type(child['original_substantive_attempts']) is int and child['original_substantive_attempts'] == 2
    targets = {'whole-manifest': A / 'whole_current_source_first_family/MANIFEST.json',
               'root-final-receipt': F / 'ROOT_FINAL_GATE.json',
               'whole-scope-contract': F / 'WHOLE_SCOPE_CONTRACT.json',
               'root-final-manifest': F / 'FINAL_MANIFEST.json',
               'reconciliation-capture': C / 'CAPTURE.json'}
    gates = {'preparation-manifest-sha256': receipt['preparation_manifest_sha256'],
             'previous-mirror-sha256': sha(read(A.parent / 'pr38_2765/state_mirror_bindings.json'))}
    assert gates['previous-mirror-sha256'] == '82d2d2b1c598fd6c95f6de1ce3ba8cc1f468c6b6291aa859eae9d8b1cd636b3e'
    for name, p in targets.items():
        gates[name] = str(p.relative_to(R))
        gates[name + '-sha256'] = sha(read(p))
    gate_obj = {'schema': 'pr39-root-actual-reviewed-gate-arguments/v1', 'explicit_arguments': gates}
    assert same(parse(read(A / 'ROOT_REVIEWED_GATE_ARGUMENTS.json')), gate_obj)
    gate_sha = sha(read(A / 'ROOT_REVIEWED_GATE_ARGUMENTS.json'))
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip()
    fresh = [pin(R / row['path']) for row in c['fresh_native13_after']]
    assert same(fresh, c['fresh_native13_after']) and head == c['head_after']
    cache_paths = {'unsolved_math_prioritization/cache/problems.json', 'unsolved_math_prioritization/cache/research_results.json', 'unsolved_math_prioritization/cache/catalog.sqlite'}
    for row in fresh:
        entries = subprocess.check_output(['git', 'ls-tree', '-z', head, '--', row['path']], cwd=R)
        if row['path'] in cache_paths:
            assert entries == b''
        else:
            assert len(entries.split(b'\0')[:-1]) == 1
            b = subprocess.check_output(['git', 'show', head + ':' + row['path']], cwd=R)
            assert len(b) == row['bytes'] and sha(b) == row['sha256']
    fresh_sha = write_new(A / 'ROOT_FRESH_MAIN_PREIMAGES.json', {
        'schema': 'pr39-root-fresh-main-preflight-review/v1', 'approved': True,
        'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'head': head,
        'reason': 'ROOT freshly read all thirteen native inputs after the published source-repair checkpoint; no prior target acceptance or scientific budget was changed.',
        'files': fresh, 'whole_queue_sha256': fresh[0]['sha256']})
    result = {'schema': 'pr39-root-complete-actual-final-inspection/v1', 'status': 'PASS',
              'actual_pid': c['pid'], 'internal_interval_contained_in_actual_outer_interval': True,
              'entire_typed_scope_and_before_after_binding_arrays_checked': True, 'immutable_bindings_checked': len(receipt['bindings_after']),
              'complete_root_capture_and_full_streams_checked': True, 'gate_arguments_sha256': gate_sha,
              'fresh_main_review_sha256': fresh_sha, 'head': head, 'native13_unchanged': True,
              'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0,
              'full_problem_solved': False, 'paper_or_new_DOI_or_tracker': False,
              'utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    write_new(A / 'ROOT_ACTUAL_FINAL_GATE_INSPECTION.json', result)
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()

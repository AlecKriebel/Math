"""Independent root inspection of complete actual evidence; no scientific execution."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import collections
import hashlib
import json

A = Path(__file__).resolve().parent
R = A.parents[2]
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())
receipt = A / 'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json'
assert sha(receipt.read_bytes()) == 'b4a0464bb2dd0e0280deebcff61be6cc9c8309200dce732c41b3c0636c21bacc'
v = load(receipt)
S = A / v['support_directory']
M = S / 'ROOT_SUPPORT_MANIFEST.json'
assert sha(M.read_bytes()) == '0ef3c26646ff99ebb67cb165baaa09463218ec7fa33aa2bcbdec254b70267eb0'
m = load(M)
assert m['status'] == v['status'] == 'PASS' and not v['retention_errors']
assert m['excluded'] == ['ROOT_SUPPORT_MANIFEST.json']
assert m['root_reproduction_receipt_sha256'] == sha(receipt.read_bytes())

def check(row, base=A):
    p = Path(row['path'])
    if not p.is_absolute():
        assert PurePosixPath(row['path']).as_posix() == row['path'] and '..' not in p.parts
        p = base / p
    assert p.is_file() and not p.is_symlink()
    b = p.read_bytes()
    assert type(row['size']) is int and len(b) == row['size'] and sha(b) == row['sha256']
    return b

actual = sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file() and p != M)
assert not any(p.is_symlink() for p in S.rglob('*'))
assert actual == sorted(r['path'] for r in m['files']) and len(actual) == 2019
bad, valid = [], 0
for row in m['files']:
    b = check(row, S)
    if row['path'].endswith('.json'):
        try:
            json.loads(b)
            valid += 1
        except (ValueError, UnicodeError) as e:
            bad.append(dict(row, parse_error=str(e)))
            if row['path'].endswith('/nested/PRIMARY_SCOPE_FAMILY_MANIFEST.json') and '/actual_manifest_controls/nested_manifest_same_basename/' in row['path']:
                assert b == b'Undeclared first-party member must be rejected.\n'
                assert sha(b) == '75dddbda2110898b4e883b0a36304b3d5da1814572f789dee7fc808026ffe2f1'
            else:
                assert row['path'].startswith('actual/final_partial_or_complete/reconstructed_controls/actual_control_inputs/manifests/')
                assert '/nested_manifest_extra/nested/' in row['path']
                assert b == b'Nested same-basename extra control.\n'
                assert sha(b) == '24b8e838e5d9969ef3e70ae4e3f12a59cdfcb6e53c9849531eb970cf18eaf73c'
assert len(bad) == 5
assert len(v['actual_outer_program_runs']) == 14 and len(v['actual_nested_program_runs']) == 88
assert len(v['actual_administrative_command_runs']) == 2
for group in ['actual_outer_program_runs', 'actual_nested_program_runs', 'actual_administrative_command_runs']:
    for run in v[group]:
        assert run['launch_attempted'] is True and run['actual_execution'] is True and run['completed'] is True
        assert type(run['exit_code']) is int and run['exit_code'] in (0, 1)
        assert run['stdio_capture'] == {'kind': 'complete_child_streams', 'stdout_available': True, 'stderr_available': True}
        check(run['stdout']); check(run['stderr'])
        if 'prelaunch_source' in run:
            assert sha(check(run['prelaunch_source'])) == run['script_sha256']
        if run.get('script'):
            sr = dict(run['script'], path=run['script']['retained_full_source'])
            check(sr)
        if 'stdin' in run:
            check(run['stdin'])
assert sum('stdin' in r for r in v['actual_nested_program_runs']) == 0
for r in v['original_replays']:
    expected = check(r['expected_receipt'])
    assert check(r['actual_stdout']) == check(r['generated_receipt']) == expected
    assert json.loads(expected) == r['complete_actual_result'] and check(r['actual_stderr']) == b''
assert [r['stdout_bytes'] for r in v['original_replays']] == [520, 520, 899]
policy = v['comparison_exclusion_policy']
assert policy['clock_keys'] == ['at','ended_utc','started_utc','time_utc','utc']
prefix = policy['single_private_path_prefix']
assert prefix['saved'] == str(R) and prefix['actual'].startswith(str(A / 'tmp/root_pr39_actual_'))

def norm(x):
    if isinstance(x, dict): return {k:norm(z) for k,z in x.items() if k not in policy['clock_keys']}
    if isinstance(x, list): return [norm(z) for z in x]
    return x.replace(prefix['actual'],prefix['saved']) if isinstance(x,str) else x

def diff(x,y,path='$'):
    if type(x) is not type(y): return [{'path':path,'actual':x,'saved':y}]
    if isinstance(x,dict):
        assert set(x) == set(y)
        return [d for k in x for d in diff(x[k],y[k],path+'/'+k)]
    if isinstance(x,list):
        assert len(x) == len(y)
        return [d for i in range(len(x)) for d in diff(x[i],y[i],path+'/'+str(i))]
    return [] if x == y else [{'path':path,'actual':x,'saved':y}]

comparisons = []
for c in v['full_structured_receipt_comparisons']:
    ab,sb = check(c['actual']),check(c['saved'])
    ds = diff(norm(json.loads(ab)),norm(json.loads(sb)))
    assert ds == c['full_JSON_differences'] and c['complete_JSON_BYTE_equal'] is (ab == sb)
    assert c['equal_after_explicit_clock_and_private_path_exclusions'] is (not ds)
    assert set(c['precise_qualifications']) == {d['path'] for d in ds}
    for d in ds:
        q=c['precise_qualifications'][d['path']]
        assert q['difference'] == d
        ax,sx=check(q['actual_complete_stream']),check(q['saved_complete_stream'])
        assert ax.decode().replace(prefix['actual'],prefix['saved']) == sx.decode()
        assert d['path'].endswith('/stderr_sha256') and d['actual']==sha(ax) and d['saved']==sha(sx)
    comparisons.append({'label':c['label'],'complete_byte_equal':ab==sb,'qualified_differences':len(ds)})
assert len(comparisons)==4 and [c['qualified_differences'] for c in comparisons]==[0,0,0,10]
for row in v['native_full_file_preimages_before_and_after']: check(row,R)
assert v['authored_members_verified_before_and_after']==732
assert v['strict_root_closure_before_and_after']['before']==v['strict_root_closure_before_and_after']['after']
assert v['full_problem_solved'] is False and v['original_substantive_turns']==2 and v['new_substantive_attempts']==v['audit_turns']==0
out={'schema':1,'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'root_receipt_sha256':sha(receipt.read_bytes()),'support_manifest_sha256':sha(M.read_bytes()),'complete_support_members_verified':len(actual),'valid_JSON_members':valid,'exact_intentionally_malformed_negative_fixtures':bad,'outer_count':14,'nested_count':88,'readonly_admin_count':2,'supplied_nested_stdin_count':0,'nested_exit_counts':dict(collections.Counter(str(r['exit_code']) for r in v['actual_nested_program_runs'])),'complete_comparisons':comparisons,'all_original_generated_files_and_stdout_byte_equal':True,'no_current_acceptance_implied':True}
(A/'ROOT_ACTUAL_REPLAY_INSPECTION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:z for k,z in out.items() if k!='exact_intentionally_malformed_negative_fixtures'},indent=2))

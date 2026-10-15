"""Independent read-only checks; execute only this newly authored source.

Reads external evidence in place. Writes only compact bindings/results to this
file's directory. Does not import, compile, or execute any inspected source.
"""
from pathlib import Path, PurePosixPath
import json, hashlib, stat, datetime, collections

OWN = Path(__file__).resolve().parent
W = OWN.parent
A = W.parent
R = A.parents[2]
C = A / 'reviewed_candidate'
notes = {}

def raw(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents), p
    assert stat.S_ISREG(p.stat().st_mode), p
    return p.read_bytes()

def h(b):
    return hashlib.sha256(b).hexdigest()

def pairs(xs):
    out = {}
    for k, v in xs:
        assert k not in out, ('duplicate key', k)
        out[k] = v
    return out

def obj(p):
    return json.loads(raw(p), object_pairs_hook=pairs,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))

def tokens(x):
    if isinstance(x, dict):
        return ('dict', tuple(sorted((k, tokens(v)) for k, v in x.items())))
    if isinstance(x, list):
        return ('list', tuple(tokens(v) for v in x))
    return (type(x).__name__, x)

def binding(p):
    b = raw(p)
    return dict(path=str(p), bytes=len(b), sha256=h(b))

def relative(n):
    assert type(n) is str and n and '\\' not in n and '\x00' not in n
    q = PurePosixPath(n)
    assert not q.is_absolute() and q.as_posix() == n
    assert not set(q.parts) & {'.', '..', '.git', '__pycache__'}
    return q

def row_binding(row, p):
    assert type(row['bytes']) is int and row['bytes'] >= 0
    b = raw(p)
    assert len(b) == row['bytes'] and h(b) == row['sha256'], p
    return b

def closed(folder, manifest):
    m = obj(folder / manifest)
    rows = m['files']
    names = [str(relative(z['path'])) for z in rows]
    assert len(names) == len(set(names))
    assert m['self_excluded'] == [manifest]
    actual = set()
    actualdirs = set()
    for p in folder.rglob('*'):
        assert not p.is_symlink(), p
        if p.is_dir():
            actualdirs.add(p.relative_to(folder).as_posix())
        else:
            assert stat.S_ISREG(p.stat().st_mode)
            actual.add(p.relative_to(folder).as_posix())
    assert actual == set(names) | {manifest}
    for z in rows:
        p = folder / z['path']
        row_binding(z, p)
        assert stat.S_IMODE(p.stat().st_mode) == 0o444, p
    assert stat.S_IMODE((folder / manifest).stat().st_mode) == 0o444
    if 'directories' in m:
        assert set(m['directories']) == actualdirs
    notes[str(folder.relative_to(A))] = dict(manifest=binding(folder / manifest),
        listed=len(rows), actual_files=len(actual), directories=len(actualdirs), full_mode='0444')
    return m, actual

def time(s):
    v = datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
    assert v.utcoffset() == datetime.timedelta(0)
    return v

def streams(record, base):
    outs = {}
    for ch in ('stdout', 'stderr'):
        z = record[ch]
        assert set(z) == {'path', 'bytes', 'sha256'}
        p = Path(z['path'])
        if not p.is_absolute():
            relative(z['path'])
            p = R / p if p.parts[0] == 'draft_pr_publication_program_20260930' else base / p
        assert p.is_relative_to(R)
        outs[ch] = row_binding(z, p)
    return outs

packet, packet_names = closed(C, 'MANIFEST.json')
reproduction, _ = closed(A / 'root_original_actual_reproduction', 'MANIFEST.json')
prep, _ = closed(A / 'current_preparation_family', 'PREPARATION_MANIFEST.json')
source, _ = closed(A / 'current_source_adversary_family', 'OWN_CLOSURE.json')
assert [len(m['files']) for m in (packet, reproduction, prep, source)] == [497, 41, 47, 70]
deps = obj(C / 'CURRENT_DEPENDENCIES.json')
assert len(deps['files']) == 416
assert len({z['path'] for z in deps['files']}) == 416
for z in deps['files']:
    relative(z['path'])
    row_binding(z, A / z['path'])
source_names = {z['path'] for z in source['files']}
assert not any(n.startswith('current_source_adversary_family/') for n in packet_names)
assert not any(z['path'].startswith('current_source_adversary_family/') for z in deps['files'])
notes['source_outside_packet'] = dict(source_safety=binding(A / 'ROOT_SOURCE_SAFETY_INSPECTION.json'),
                                    source70_plus_self_outside497=True, source_family_outside416=True)

ss = obj(A / 'ROOT_SOURCE_SAFETY_INSPECTION.json')
verdict = obj(A / 'current_source_adversary_family/VERDICT.json')
assert tokens(ss['entire_source_verdict']) == tokens(verdict)
for z in ss['source_closures'] + ss['real_prerequisites'] + [ss['source_adversary_report'], ss['source_adversary_verdict']]:
    row_binding(z, A / str(relative(z['path'])))
sourcecaps = [obj(A / 'current_source_adversary_family' / n) for n in sorted(source_names) if n.endswith('/CAPTURE.json')]
assert len(sourcecaps) == len(ss['complete_actual_source_captures']) == 7
assert {tokens(c) for c in sourcecaps} == {tokens(c) for c in ss['complete_actual_source_captures']}
for n in sorted(source_names):
    if n.endswith('/CAPTURE.json'):
        p = A / 'current_source_adversary_family' / n
        cap = obj(p)
        streams(cap, p.parent)
        assert cap['actual_execution'] is True and cap['completed'] is True
        assert time(cap['started_utc']) <= time(cap['finished_utc'])
assert ss['schema'] == 'pr45-root-complete-current-source-inspection/v1'
assert ss['status'] == 'PASS' and ss['new_whole_current_gate'] == 'PENDING'
for k in ('personally_complete_source_report_read', 'first_party_exclusions_and_distinct_actual_replay_roles_checked'):
    assert ss[k] is True
assert ss['full_problem_solved'] is False
notes['source_safety'] = dict(report_bound=True, verdict_bound_and_typed_equal=True,
    both_closures_bound=True, all7_actual_capture_objects_typed_equal=True,
    all7_fullstreams_bound=True, ROOT_attestations_are_trusted_not_proved=True)

execution = obj(C / 'CURRENT_EXECUTION_REFERENCE.json')
od = A / str(relative(execution['audit_relative_outer_capture']))
inner = A / str(relative(execution['audit_relative_inner_attempt']))
cap = obj(od / 'CAPTURE.json'); pre = obj(od / 'OPERATION_PRELAUNCH.json'); inv = obj(inner / 'INVOCATION.json')
expected_outer = set('schema operator_pid started_utc argv cwd builder_sha256 operator_sha256 administrative_only scientific_helpers_run actual_execution completed pid exit_code stdin_supplied finished_utc stdout stderr builder_unchanged_after_child operator_unchanged_after_child new_whole_current_gate current_whole_verdict capture_requires_ROOT_full_read_before_promotion status'.split())
assert set(cap) == expected_outer
assert set(pre) == set('schema operator_pid started_utc argv cwd builder_sha256 operator_sha256 administrative_only scientific_helpers_run'.split())
assert set(inv) == set('argv cwd pid parent_pid utc source_sha256 administrative_only'.split())
assert {p.name for p in od.iterdir()} == {'CAPTURE.json','OPERATION_PRELAUNCH.json','PRELAUNCH_BUILDER_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}
assert all(p.is_file() and not p.is_symlink() for p in od.iterdir())
assert h(raw(od / 'CAPTURE.json')) == 'bcfa9fc8791326fb79771c74e48d3e1dc51abe38c48c4e624d6800128b9f201b'
assert cap['schema'] == 'PR45_ROOT_ACTUAL_BUILDER_OPERATION_v1'
assert cap['operator_pid'] == pre['operator_pid'] == inv['parent_pid'] == execution['outer_parent_pid'] == 99703
assert cap['pid'] == inv['pid'] == execution['actual_builder_pid'] == 99704
for k in ('operator_pid','pid','exit_code'):
    assert type(cap[k]) is int
for k, expected in [('administrative_only', True), ('scientific_helpers_run', False), ('actual_execution', True), ('completed', True), ('stdin_supplied', False), ('builder_unchanged_after_child', True), ('operator_unchanged_after_child', True), ('capture_requires_ROOT_full_read_before_promotion', True)]:
    assert cap[k] is expected
assert cap['exit_code'] == 0 and cap['current_whole_verdict'] is None
assert cap['new_whole_current_gate'] == 'PENDING'
assert cap['status'] == 'ACTUAL_ADMINISTRATIVE_CAPTURE_COMPLETE_WHOLE_REVIEW_PENDING'
assert cap['argv'] == pre['argv'] and cap['argv'][2:] == inv['argv']
assert cap['cwd'] == pre['cwd'] == inv['cwd'] == str(R)
assert cap['started_utc'] == pre['started_utc']
assert cap['builder_sha256'] == inv['source_sha256'] == h(raw(od/'PRELAUNCH_BUILDER_SOURCE.py')) == h(raw(A/'current_preparation_family/prepare_current_packet.py'))
assert cap['operator_sha256'] == h(raw(od/'PRELAUNCH_OPERATOR.py')) == h(raw(A/'current_preparation_family/capture_root_builder_operation.py'))
assert execution['outer_prelaunch_sha256'] == h(raw(od/'OPERATION_PRELAUNCH.json'))
out = streams(cap, od)
assert out['stderr'] == b''
result = json.loads(out['stdout'], object_pairs_hook=pairs)
assert result['manifest_sha256'] == h(raw(C/'MANIFEST.json'))
assert result['current_whole_verdict'] is None and result['full_problem_solved'] is False
commands = obj(inner / 'GIT_COMMANDS.json')
prefixdir = C / 'build/actual_attempt_prepublication_prefix'
prefix = obj(prefixdir / 'GIT_COMMANDS.json')
assert len(commands) == 47 and len(prefix) == 45 and tokens(commands[:45]) == tokens(prefix)
commandkeys = set('argv cwd started_utc actual_execution completed pid exit_code stdin_supplied finished_utc stdout stderr'.split())
allpaths = set()
for i, cmd in enumerate(commands):
    assert set(cmd) == commandkeys
    assert type(cmd['pid']) is int and cmd['pid'] > 0 and type(cmd['exit_code']) is int and cmd['exit_code'] == 0
    assert cmd['actual_execution'] is True and cmd['completed'] is True and cmd['stdin_supplied'] is False
    assert cmd['cwd'] == str(R) and cmd['argv'][0] == 'git'
    assert time(cap['started_utc']) <= time(cmd['started_utc']) <= time(cmd['finished_utc']) <= time(cap['finished_utc'])
    b = streams(cmd, inner)
    assert b['stderr'] == b''
    for ch in ('stdout', 'stderr'):
        assert cmd[ch]['path'] == 'git/%d.%s' % (i, ch)
        assert cmd[ch]['path'] not in allpaths
        allpaths.add(cmd[ch]['path'])
    if i < 45:
        copied = streams(prefix[i], prefixdir)
        assert copied == b
assert commands[-2]['argv'] == ['git','branch','--show-current']
assert commands[-1]['argv'] == ['git','rev-parse','HEAD']
assert streams(commands[-2], inner)['stdout'] == b'main\n'
assert streams(commands[-1], inner)['stdout'] == (deps['current_main_head']+'\n').encode()
notes['final_outer_inner'] = dict(outer=binding(od/'CAPTURE.json'), six_members=True,
    exact_capture_schema=True, strictly_typed_booleans_and_integers=True,
    source_prelaunch_invocation_chain=True, final47_fullstreams_bound=True,
    copiedprefix45_fullstreams_identical=True, final2_roles_and_frozen_main_head=True,
    genuine_execution_depends_on_honest_operator_evidence=True)

ind = obj(C/'review/independent_results.json')
assert set(ind) == {'passed','failed','arithmetic','reviewed_sha256','scope','checks'}
assert type(ind['passed']) is int and type(ind['failed']) is int
assert (ind['passed'], ind['failed']) == (3044,0)
expected = set(); groups = collections.Counter()
def add(group, label):
    assert label not in expected
    expected.add(label); groups[group] += 1
for n in range(1,10):
    for key in ('mass','fair_last'): add(key, '%s_%d'%(key,n))
    for m in range(n):
        for j in range(1 << (m+1)): add('conditional','conditional_%d_%d_%d'%(n,m,j))
        add('max_finite_history_correlation','max_finite_history_correlation_%d_%d'%(n,m))
for n in range(4,10):
    for mask in range(16):
        for key in ('B_fair','tower','mismatch'): add('anticipative_'+key,'anticipative_%s_%d_%d'%(key,n,mask))
for n in range(6):
    for r in range(5):
        for key in ('window_TV','no_flip_window'): add(key,'%s_%d_%d'%(key,n,r))
for i in range(64):
    for b in (-1,1): add('metric_pointwise','metric_pointwise_%d_%d'%(i,b))
for n in range(40):
    for s in range(9): add('offset_bound','offset_bound_%d_%d'%(n,s))
    add('offset_union_sum','offset_union_sum_%d'%n)
for n in range(1,80): add('double_time_gap','double_time_gap_%d'%n)
assert expected == set(ind['checks']) and len(expected) == 3044
assert all(type(v) is str and v == 'PASS' for v in ind['checks'].values())
assert ind['reviewed_sha256'] == h(raw(C/'PARTIAL.md'))
historical = obj(W/'ALL3044_HISTORICAL_LABEL_INSPECTION.json')
assert {v['label'] for v in historical['ordered_labels']} == expected
assert len(historical['ordered_labels']) == 3044
assert historical['universal_proof_from_counts'] is False
notes['historical3044'] = dict(group_counts=dict(groups), exact_result_schema=True,
    all_keys_and_PASS_values=True, original_source_read_as_text_only=True,
    historical_labels_are_finite_controls_not_all_couplings_proof=True)

dated = obj(W/'DATED_NATIVE4_AND_STABLE_LIVE9.json')
fresh = obj(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')
assert dated['frozen_main_head'] == fresh['current_head'] == deps['current_main_head'] == '264c26d539d616b0da6f8df76478a213d20939e4'
four = {'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
assert len(dated['native13']) == 13
for z in dated['native13']:
    assert z['frozen_binding'] == next(v for v in fresh['files'] if v['path'] == z['path'])
    if z['path'] in four:
        current = binding(R / z['path'])
        z['independent_current_live_equal_parent_inspection'] = current['bytes'] == z['live_binding']['bytes'] and current['sha256'] == z['live_binding']['sha256']
        z['independent_current_live_binding'] = current
        label = Path(z['path']).name.replace('.', '_')
        folder = W/'actual_git/v2'/('frozen_native4_'+label+'_body')
        observed = streams(obj(folder/'CAPTURE.json'), folder)['stdout']
        assert len(observed) == z['frozen_binding']['bytes'] and h(observed) == z['frozen_binding']['sha256']
        assert z['actual_frozen_git_body_equal'] is True
        assert obj(folder/'CAPTURE.json')['argv'] == ['git','show',dated['frozen_main_head']+':'+z['path']]
    else:
        row_binding(z['live_binding'], Path(z['live_binding']['path']))
        row_binding(z['frozen_binding'], R / z['path'])
        assert z['stable_live_equals_frozen_binding'] is True
assert dated['acceptance_on_future_main_approved'] is False
notes['dated_native13'] = dict(frozen_head=dated['frozen_main_head'],
    recorded_later_main_head=dated['live_head_at_inspection'],
    frozen4_body_evidence_bound=True, live9_bound=True,
    native4_current_changes=[dict(path=z['path'], current=z['independent_current_live_binding']) for z in dated['native13'] if z['path'] in four and not z['independent_current_live_equal_parent_inspection']],
    same_four_live_bytes_do_not_imply_same_main_head=True, no_future_main_acceptance=True)

for label, expected in [('complete_whole_inspection',1),('complete_whole_inspection_v2',0)]:
    folder = W/'actual_runs'/label; owncap = obj(folder/'CAPTURE.json')
    assert type(owncap['exit_code']) is int and owncap['exit_code'] == expected
    assert owncap['source_unchanged'] is True and owncap['operator_unchanged'] is True
    row_binding(dict(bytes=len(raw(Path(owncap['source_path']))),sha256=owncap['source_sha256']),Path(owncap['source_path']))
    b = streams(owncap, folder)
    if expected:
        assert b['stdout'] == b'' and b'FileNotFoundError' in b['stderr'] and b'current_author/draft_pr_publication_program_20260930/' in b['stderr']
    else:
        assert b['stderr'] == b''
for p in (W/'first_failed_inspection').iterdir():
    assert raw(p) == raw(W/p.name)
notes['own_first_failure'] = dict(v1_exit1_preserved=True, v2_exit0_preserved=True,
    all4_first_stage_outputs_preserved_byte_exact=True, failure_is_own_resolver_not_input_defect=True)

result = dict(schema='pr45-independent-inspection-falsifier/v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    status='PASS_OBSERVED_BINDINGS_WITH_VALIDATOR_LIMITATIONS',checks=notes,
    executed_inspected_code=False,foreign_bodies_copied=False,external_contact=False,
    mutated_outside_own_directory=False,whole_current_approval=False,discovery_completion_percent=0,
    audit_completion_percent=90)
(OWN/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'], sections=len(notes), output=str(OWN/'INDEPENDENT_CHECK_RESULTS.json')),indent=2))

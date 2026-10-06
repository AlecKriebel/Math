"""Authenticate the closed independent content review without any writer grant."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, stat, sys, ast
if sys.flags.optimize:
    raise RuntimeError('Optimized content-review authentication forbidden.')
D = Path(__file__).resolve().parent
A = D.parent
P = A.parent.parent
R = P.parent
V = D / 'completion_packet_review_01'
sha = lambda b: hashlib.sha256(b).hexdigest()
def pin(p):
    p = Path(p)
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha(b), mode=format(stat.S_IMODE(s.st_mode), '04o'))
def check(p, e, historical_mode=False):
    q = pin(p)
    assert q['bytes'] == e['bytes'] and q['sha256'] == e['sha256'], str(p)
    if not historical_mode:
        mode = int(e['mode'], 8) if isinstance(e['mode'], str) else e['mode']
        assert int(q['mode'], 8) == mode, str(p)
    return q
load = lambda p: json.loads(Path(p).read_bytes())
for name, digest in {
    'REPORT.md':'5da444854d5deed5e96d7cf43ce5c0cc6744d6e348af6c60fb829887cd211fc4',
    'VERDICT.json':'11d08be2a585a5dae239a6963c483e2edb001a2822426aba39f8fa1c548587de',
    'INPUT_INVENTORY.json':'cb63b8daf417fd01a88366adb228b406be8098a6be6f54f87c9e070d4f93ad2f',
    'OUTPUT_INVENTORY.json':'4e3ce674924becfe41dedbd41a582ee137f31effa468589c80341d45648747c8',
}.items():
    assert pin(V / name)['sha256'] == digest
output = load(V / 'OUTPUT_INVENTORY.json')
verdict = load(V / 'VERDICT.json')
results = load(V / 'CHECK_RESULTS.json')
inputs = load(V / 'INPUT_INVENTORY.json')
assert output['mandatory_findings'] == verdict['required_findings_count'] == 0
assert not verdict['required_findings'] and output['optional_findings'] == 2
assert output['reviewer_writes_stopped_after_this_inventory_and_mode_freeze']
assert verdict['status'] == 'PASS_EXACT_PR305_FINAL_COMPLETION_PACKET'
assert verdict['checkpoint_operator_outside_scope']
assert {str(p.relative_to(V)) for p in V.rglob('*') if p.is_file()} == {e['path'] for e in output['files']} | {'OUTPUT_INVENTORY.json'}
assert len(output['files']) == 13
assert all(stat.S_IMODE(p.stat().st_mode) == 0o555 for p in [V, *[q for q in V.rglob('*') if q.is_dir()]])
for e in output['files']:
    check(V / e['path'], e)
assert pin(V / 'OUTPUT_INVENTORY.json')['mode'] == '0444'
assert len(inputs['files']) == 2372
for e in inputs['files']:
    # Only the reviewer's own criteria had its launch-time644 mode frozen444.
    internal = Path(e['path']) == V / 'CRITERIA.json'
    check(e['path'], e, historical_mode=internal)
    if internal:
        assert pin(e['path'])['mode'] == '0444' and e['mode'] == 0o644
criteria = load(V / 'CRITERIA.json')
spec = load(V / 'native_run_001/execution_spec.json')
started = load(V / 'native_run_001/started.json')
native = load(V / 'native_run_001/execution.json')
assert datetime.fromisoformat(criteria['utc']) < datetime.fromisoformat(native['started_utc'])
assert native['actual_PID'] == started['actual_PID'] == verdict['reviewer_native_PID'] == 76310
assert native['exit_code'] == 0 and native['stderr_bytes'] == 0
assert native['argv'] == ['/opt/homebrew/bin/python3','-E','-B',str(V / 'review_packet.py')]
assert native['cwd'] == str(V) and all(native[k] == v for k,v in spec.items())
assert all(native[k] == v for k,v in started.items())
assert datetime.fromisoformat(native['ended_utc']) >= datetime.fromisoformat(native['started_utc'])
for e in native['programs']:
    check(e['path'], e, historical_mode=Path(e['path']).parent == V)
for k in ['stdout','stderr']:
    b = (V / 'native_run_001' / (k + '.bin')).read_bytes()
    assert len(b) == native[k + '_bytes'] and sha(b) == native[k + '_sha256']
assert results['status'] == 'PASS_INDEPENDENT_COMPLETION_PACKET_STRUCTURAL_AND_LOCAL_CUSTODY'
assert len(results['checks']) == 350 and all(e['passed'] for e in results['checks'])
assert results['credentials_or_private_payload_hits'] == []
assert results['authenticated_input_files'] == 2372
assert results['original_native_captures'] == 377 and results['fresh_readonly_saved_captures'] == 84
assert json.loads((V / 'native_run_001/stdout.bin').read_bytes())['status'] == results['status']
planp = D / 'completion_preparation/CONTENT_PLAN.json'
assert pin(planp) == dict(bytes=70884,sha256='aa3f453d3bdb86d40228dfcca5f9ba6815665e17db1f9ea4f50b1a495230bad2',mode='0644')
plan = load(planp)
assert plan['target_count'] == len(plan['targets']) == 88
for e in plan['targets']:
    check(R / e['input']['path'], e['input'])
    if e['original_target'] is None:
        assert not (R / e['target']).exists() and not (R / e['target']).is_symlink()
    else:
        check(R / e['target'], e['original_target'])
before = load(P / 'inventory.json')
after = load(R / plan['targets'][0]['input']['path'])
assert [x['number'] for x,y in zip(before['items'],after['items']) if x != y] == [305]
assert before['completed_by_descending'] == 26 and after['completed_by_descending'] == 27
for k in ['claimed_solved_published_by_descending','claimed_solved_merged_by_descending']:
    assert after[k] == before[k] + [305] and len(after[k]) == len(set(after[k])) == 8
operator = D / 'root_checkpoint_pr305_publication_035.py'
assert pin(operator) == dict(bytes=9198,sha256='20417d15b340639e7a2a5e8a3e605795fdc0fb8bb8c9952ff9049ee1eb365ff5',mode='0644')
ast.parse(operator.read_bytes())
# The root has read the full report and operator. The independent reviewer did
# not review the routine checkpoint operator; these boundaries stay explicit.
sys.path.insert(0,str(D / 'publication_preparation'))
import submission_gate as g
g.current_clearance()
g.operational_clearance()
assert load(D / 'ROOT_PR305_POST_MERGE_CUSTODY.json')['status'] == 'PASS_ROOT_PR305_ACTUAL_MERGE_FULL_NATIVE_CUSTODY'
receipt = dict(status='PASS_ROOT_PR305_CLOSED_COMPLETION_PACKET_CUSTODY',
    UTC=datetime.now(timezone.utc).isoformat(), mandatory_unresolved_findings=0,
    optional_navigation_findings=2, exact_selected_bodies=88,
    closed_review_payloads=13, input_files_whole_body_mode_authenticated=2372,
    historical_own_criteria_mode_transition_explicit=True,
    actual_reviewer_native_PID=native['actual_PID'], actual_native_exit_code=0,
    actual_native_custody=pin(V / 'native_run_001/execution.json'),
    all350_independent_checks_authenticated=True, complete_report_read=True,
    exact_plan=pin(planp), original_merge_and_services_already_complete=True,
    selected_original_packet_unchanged=True, checkpoint_operator_root_read_only_review=pin(operator),
    independent_review_did_not_preapprove_checkpoint_operator=True,
    optional_manifest_navigation_addressed_by_exact_manifest_appendix=True,
    optional_readme_directional_word_accepted_as_nonblocking_navigation=True,
    no_new_mathematical_or_absolute_priority_or_human_review_claim=True,
    no_shared_or_service_mutation_or_writer_grant=True, persistent_goal_complete=False)
p = D / 'ROOT_PR305_COMPLETION_PACKET_CUSTODY.json'
assert not p.exists()
p.write_text(json.dumps(receipt,indent=2)+'\n')
evidence = {str(V / e['path']):pin(V / e['path']) for e in output['files']}
evidence[str(V / 'OUTPUT_INVENTORY.json')] = pin(V / 'OUTPUT_INVENTORY.json')
clear = dict(status='PASS_ROOT_PR305_CLOSED_COMPLETION_PACKET',
    UTC=receipt['UTC'], mandatory_unresolved_findings=0, content_plan=pin(planp),
    checkpoint_operator=pin(operator), root_custody=pin(p),
    closed_review_evidence=evidence, independent_content_review_closed=True,
    exact88_body_packet_only=True, checkpoint_operator_independent_review_claimed=False,
    future_actual_checkpoint_still_requires_fresh_scoped_lease=True,
    original_native_merge_and_service_writes_not_authorized=True)
q = D / 'ROOT_PR305_COMPLETION_PACKET_CLEARANCE.json'
assert not q.exists()
q.write_text(json.dumps(clear,indent=2)+'\n')
print(json.dumps(dict(custody=pin(p),clearance=pin(q),
    status=receipt['status'],mandatory_findings=0,input_files=2372,native_PID=76310),indent=2))

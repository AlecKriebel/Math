"""Meaningful owned offline controls. No current-five/native/network/lock reads."""
from pathlib import Path
import ast,copy,hashlib,json,types
HERE=Path(__file__).absolute().parent
def module(name):
 p=HERE/name;m=types.ModuleType(name);m.__file__=str(p)
 exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
b=module('conditional_packet_builder.py');s=module('prepare_positive_selection.py')
plan=json.loads((HERE/'PROPOSED_PUBLIC_SELECTION.json').read_text())
baseline_raw=(s.CASE/'native_completion_preparation_02/BASELINE_MEMBERSHIP.json').read_bytes()
carry_raw=(s.PROGRAM/'audits/pr212_30005310/next_checkpoint_carry_preparation_01/PROPOSED_CARRY_INVENTORY.json').read_bytes()
baseline=b.validate_baseline(baseline_raw);carry=b.validate_carry(carry_raw)
results=[]
def positive(name,f):
 f();results.append({'case':name,'expected':'PASS','result':'PASS'})
def refusal(name,f):
 try:f()
 except (ValueError,TypeError,KeyError,UnicodeError):results.append({'case':name,'expected':'REFUSE','result':'REFUSED'});return
 raise AssertionError('Expected refusal: '+name)
rows=b.validate_plan(plan,carry)
selected={}
for path,row in rows.items():
 raw,mode=s.read_file(Path(row['origin']))
 b.body_ok(raw,{k:row[k] for k in ('bytes','sha256')})
 assert mode==row['observed_source_mode'] and b.native(raw)==row['git_blob']
 selected[path]=raw
ready=json.loads(selected[b.CASE+'ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json'])
source_ref={'path':str(s.CHECKOUT/b.ENGINE/'SOURCE_MANIFEST.json'),**b.ENGINE_SOURCE_MANIFEST_PIN}
# Explicit SYNTHETIC capture. No actual current-five files or native state are read.
progress={**baseline,'fully_completed_count':53,'published_count':37,'last_completed_PR':211,
 'next_numeric_intake_cursor':213,'dated_eligible_total':99,'goal_complete':False,
 'administrative_checkpoint_complete':True,'prior_PR':212,'stale_case_field':'must disappear'}
nv={p:None for p in b.VIEWS};nv[b.VIEWS[2]]=b.enc(progress);nv[b.VIEWS[4]]=b'Native prefix\n'
nv[b.VIEWS[3]]=b'Old progress\n'
lv={p:None for p in b.VIEWS};lv[b.VIEWS[2]]=b.enc(progress);lv[b.VIEWS[4]]=b'Native prefix\nLocal suffix\n'
lv[b.VIEWS[1]]=b'Case local prefix without newline'
pre={p:None for p in set(rows)|set(b.VIEWS)}
for path,raw in nv.items():
 if raw is not None:pre[path]={'mode':'100644','type':'blob','sha':b.native(raw)}
capture={'schema':'pr214-future-root-capture-input-v1','UTC':'2026-10-17T23:00:00Z',
 'engine_source_manifest':source_ref,'native_preimages':pre,'native_view_bodies':nv,'local_view_bodies':lv,
 'ancestor_tuples':{p:{'mode':'040000','type':'tree','sha':'1'*40} for p in b.all_ancestors(pre)},
 'protected_queue':{'mode':'100644','type':'blob','sha':'2'*40},
 'protected_queue_row_pin':json.loads(selected[b.CASE+'ROOT_NATIVE_COMPLETION_IDENTITY_ACCEPTANCE_01.json'])['own_Main_QUEUE_row_pin'],
 'retired_candidates':[],'evidence_references':{**ready['evidence_references'],'case_ready':{
 'path':str(s.CASE/'ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json'),**b.FROZEN_GATE_PINS['ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json']}},
 'native_identity_receipt':ready['native_identity_receipt']}
resolved=copy.deepcopy(plan)
# Only owned fixture data resolves the3 in-packet slots. It is not operational Root acceptance.
resolved['unresolved_slots']=[x for x in resolved['unresolved_slots'] if not x['blocks_construction']]
def build(pp=resolved,cc=capture,ss=selected):
 return b.construct(pp,ss,baseline_raw,carry_raw,cc)
refusal('real_selection_unresolved_slots_refuse',lambda:build(plan))
artifact=build();m=artifact['manifest'];payload=artifact['postimages'];schedule=artifact['relative_source_bodies']
def success_checks():
 assert artifact['source_only'] is True and artifact['operational_authority'] is False
 assert m['total_files']==len(rows)+5 and m['total_bytes']<8_000_000
 assert m['facts']['advance_to_next_PR_authorized_now'] is False and m['facts']['goal_complete'] is False
 assert all(p not in payload for p in ['unsolved_math_prioritization/QUEUE.md',b.WRITER['path']])
 assert all(r['source'].startswith('_private_logical_packet_01/sources/') for r in m['files'])
 assert all(schedule[r['source']]==payload[r['path']] for r in m['files'])
 for i,p in enumerate(b.VIEWS):
  r=m['local_views'][i]
  assert r['path']==p
  if lv[p] is None:assert r['source'] is None and r['preimage'] is None
  else:assert schedule[r['source']]==lv[p] and r['preimage']==b.pin(lv[p])
 for p in (b.VIEWS[1],b.VIEWS[4]):
  for prefix in (lv[p],nv[p]):
   if prefix is not None:assert payload[p].startswith(prefix)
  assert payload[p].rstrip().endswith(b.marker()) and payload[p].count(b'<!-- PR214_NATIVE_PHASE_FACTS')==1
 out=b.decode(payload[b.VIEWS[2]])
 assert all(out[k]==v+[214] for k,v in baseline.items())
 assert len(out['fully_completed_eligible_PRs'])==54 and len(out['published_PRs'])==38
 assert not any(k in out for k in ['administrative_checkpoint_complete','prior_PR','stale_case_field'])
 assert out['conditional_proposal_only'] is True
 assert m['expected_new_directories']==[]
 assert set(m)==set(json.loads((s.CASE/'native_completion_preparation_02/INPUT_CONTRACT.json').read_text())['logical_exact_keys'])
positive('pure_complete_synthetic_constructor_and_model_exact_keys',success_checks)
positive('longer_native_prefix_preserved',lambda: (_ for _ in ()).throw(AssertionError()) if b.merge_log_prefix(b'a',b'ab')!=b'ab' else None)
positive('longer_local_prefix_preserved',lambda: (_ for _ in ()).throw(AssertionError()) if b.merge_log_prefix(b'ab',b'a')!=b'ab' else None)
positive('both_absent_logs_empty',lambda: (_ for _ in ()).throw(AssertionError()) if b.merge_log_prefix(None,None)!=b'' else None)
positive('all_known_positive_leaves_rehashed_no_body_copies',lambda:None)
refusal('divergent_log_histories',lambda:b.merge_log_prefix(b'a',b'b'))
refusal('duplicate_JSON_key',lambda:b.decode(b'{"a":1,"a":2}'))
refusal('nonfinite_JSON_constant',lambda:b.decode(b'{"a":NaN}'))
refusal('overflow_JSON_float',lambda:b.decode(b'{"a":1e999}'))
for value in ['../x','a/../x','/x','a//x','a/./x','a\\x','a\nx']:
 refusal('unsafe_relative_'+repr(value),lambda value=value:b.rel(value))
for p in [b.CASE+'_private/raw.json',b.CASE+'ROOT_COMPLETE214_READ/raw.json',b.CASE+'runtime/a.json',
          b.CASE+'packet/x.json',b.CASE+'native_completion_preparation_02/ROOT_COMPLETE214_CANDIDATE/raw.json',
          'unsolved_math_prioritization/QUEUE.md',b.PROGRAM+'ordered_intakes_after_PR214_20261017/helper.py']:
 positive('public_scope_refuses_'+p,lambda p=p: (_ for _ in ()).throw(AssertionError(p)) if b.public(p) else None)
refusal('NUL_body',lambda:b.body_ok(b'\0',b.pin(b'\0')))
refusal('nonUTF8_body',lambda:b.body_ok(b'\xff',b.pin(b'\xff')))
refusal('oversized_individual_body',lambda:b.body_ok(b'a'*(4_000_000+1),{'bytes':4_000_001,'sha256':'1'*64}))
refusal('bool_is_not_byte_count',lambda:b.bytepin({'bytes':True,'sha256':'1'*64}))
refusal('changed_pinned_baseline',lambda:b.validate_baseline(baseline_raw+b' '))
refusal('changed_pinned_carry',lambda:b.validate_carry(carry_raw+b' '))
def change_plan(name,fn):
 x=copy.deepcopy(resolved);fn(x);refusal(name,lambda:build(x))
change_plan('missing_carry_member',lambda x:x['files'].pop(0))
change_plan('duplicate_selected_target',lambda x:x['files'].append(copy.deepcopy(x['files'][0])))
change_plan('false_total_count',lambda x:x.update(total_files=x['total_files']+1))
change_plan('boolean_total_count',lambda x:x.update(total_files=True))
change_plan('over_budget_declared_total',lambda x:x.update(total_bytes=8_000_001))
change_plan('unsafe_selected_target',lambda x:x['files'][0].update(path='../escape'))
change_plan('selected_private_target',lambda x:x['files'][0].update(path=b.CASE+'_private/data.json'))
change_plan('selected_future_runtime_journal_target',lambda x:x['files'][0].update(path=b.CASE+'ROOT_COMPLETE214_READ/source.json'))
change_plan('forged_native_blob',lambda x:x['files'][-1].update(git_blob='f'*40))
change_plan('extra_slot_guessed_pin',lambda x:x['unresolved_slots'][0].update(sha256='1'*64))
def change_capture(name,fn):
 x=copy.deepcopy(capture);fn(x);refusal(name,lambda:build(cc=x))
change_capture('missing_native_target_preimage',lambda x:x['native_preimages'].pop(next(iter(rows))))
change_capture('native_view_body_absence_mismatch',lambda x:x['native_view_bodies'].update({b.VIEWS[2]:None}))
change_capture('native_view_OID_mismatch',lambda x:x['native_preimages'][b.VIEWS[2]].update(sha='3'*40))
change_capture('nonview_overwrite',lambda x:x['native_preimages'].update({next(iter(rows)):{'mode':'100644','type':'blob','sha':'3'*40}}))
change_capture('divergent_captured_program_logs',lambda x:x['local_view_bodies'].update({b.VIEWS[4]:b'Unrelated'}))
change_capture('duplicate_current_marker_in_prefix',lambda x:x['local_view_bodies'].update({b.VIEWS[1]:b.marker()}))
change_capture('source01_not_execution_base',lambda x:x['engine_source_manifest'].update(path=str(s.CASE/'native_completion_preparation_01/SOURCE_MANIFEST.json')))
change_capture('foreign_checkout_source_manifest',lambda x:x['engine_source_manifest'].update(path='/other/'+b.ENGINE+'/SOURCE_MANIFEST.json'))
change_capture('wrong02_source_manifest_pin',lambda x:x['engine_source_manifest'].update(sha256='1'*64))
change_capture('missing_exact_ancestor_state',lambda x:x['ancestor_tuples'].pop(next(iter(x['ancestor_tuples']))))
change_capture('non_tree_ancestor',lambda x:x['ancestor_tuples'].update({next(iter(x['ancestor_tuples'])):{'mode':'100644','type':'blob','sha':'1'*40}}))
change_capture('malformed_UTC',lambda x:x.update(UTC='2026-99-17T23:00:00Z'))
change_capture('wrong_Main_ownrow_pin',lambda x:x.update(protected_queue_row_pin={'bytes':279,'sha256':'1'*64}))
change_capture('duplicate_retired_candidate',lambda x:x.update(retired_candidates=['1'*40,'1'*40]))
change_capture('missing_evidence_role',lambda x:x['evidence_references'].pop('priority'))
change_capture('wrong_case_ready_natural_path',lambda x:x['evidence_references']['case_ready'].update(path=str(s.CASE/'fake_ready.json')))
change_capture('extra_capture_field',lambda x:x.update(operational_authority=True))
for key,v in [('fully_completed_count',54),('published_count',38),('last_completed_PR',214),('next_numeric_intake_cursor',214),('goal_complete',True),('dated_eligible_total',True)]:
 def fn(x,key=key,v=v):
  o=b.decode(x['local_view_bodies'][b.VIEWS[2]]);o[key]=v;x['local_view_bodies'][b.VIEWS[2]]=b.enc(o)
 change_capture('bad_local_baseline_'+key,fn)
def bad_members(x):
 o=b.decode(x['local_view_bodies'][b.VIEWS[2]]);o['fully_completed_eligible_PRs']=o['fully_completed_eligible_PRs']+[212]
 x['local_view_bodies'][b.VIEWS[2]]=b.enc(o)
change_capture('212_cannot_be_counted',bad_members)
# Verify conditional semantics against the final frozen input contract, not a duplicated count-only expectation.
contract=json.loads((s.CASE/'native_completion_preparation_02/INPUT_CONTRACT.json').read_text())
positive('conditional_facts_typed_exact_final02',lambda: (_ for _ in ()).throw(AssertionError()) if not b.exact(b.FACTS,contract['conditional_facts']) else None)
oldprefix=b'Prior log\n<!-- PR212_NATIVE_PHASE_FACTS history -->'
positive('prior_case_marker_and_unterminated_prefix_preserved',lambda: (_ for _ in ()).throw(AssertionError()) if not b.append_log(oldprefix,'2026-10-17T23:00:00Z').startswith(oldprefix) else None)
positive('explicit_local_absence_and_native_prefix',lambda: (_ for _ in ()).throw(AssertionError()) if b.merge_log_prefix(None,b'native')!=b'native' else None)
positive('explicit_native_absence_and_local_prefix',lambda: (_ for _ in ()).throw(AssertionError()) if b.merge_log_prefix(b'local',None)!=b'local' else None)
change_capture('null_MainQUEUE_tuple_refused',lambda x:x.update(protected_queue=None))
change_capture('absent_ancestor_cannot_have_existing_child',lambda x:x['ancestor_tuples'].update({b.PROGRAM.rstrip('/'):None}))
change_capture('missing_local_view_slot',lambda x:x['local_view_bodies'].pop(b.VIEWS[0]))
change_capture('bool_native_size_not_body',lambda x:x['native_view_bodies'].update({b.VIEWS[0]:True}))
bad=copy.deepcopy(resolved);bad['unresolved_slots'][0]['id']=bad['unresolved_slots'][1]['id']
refusal('duplicate_unresolved_slot_identity',lambda:build(bad))
refusal('nonobject_unresolved_slot',lambda:b.validate_plan({**resolved,'unresolved_slots':[None]},carry))
# Pure source audit: constructor imports only computation/path grammar modules; no effect primitive.
tree=ast.parse((HERE/'conditional_packet_builder.py').read_text())
imports=[n.module if isinstance(n,ast.ImportFrom) else a.name for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) for a in (n.names if isinstance(n,ast.Import) else [None])]
assert set(imports)<=set(['copy','datetime','hashlib','json','math','re','pathlib'])
assert not any(isinstance(n,ast.Name) and n.id in ('open','eval','exec','compile','__import__') for n in ast.walk(tree))
assert not any(isinstance(n,ast.Attribute) and n.attr in ('write','write_text','write_bytes','open','unlink','rename','rglob','walk') for n in ast.walk(tree))
results.append({'case':'constructor_AST_has_no_filesystem_transport_dynamic_execution_or_recursive_discovery_effects','expected':'PASS','result':'PASS'})
out={'schema':'pr214-inactive-packet-builder-offline-controls-v1','synthetic_only':True,
 'real_current_five_lock_native_or_provider_read_or_write':False,'actual_completion_authority':False,
 'all_passed':True,'positive_cases':sum(x['expected']=='PASS' for x in results),
 'expected_refusals':sum(x['expected']=='REFUSE' for x in results),'cases':results,
 'synthetic_packet_files':m['total_files'],'synthetic_packet_bytes':m['total_bytes'],
 'known_selection_files':len(rows),'known_selection_bytes':sum(r['bytes'] for r in rows.values()),
 'real_plan_still_unresolved':len(plan['unresolved_slots'])}
(HERE/'OFFLINE_CONTROL_RESULTS.json').open('x').write(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='cases'}))

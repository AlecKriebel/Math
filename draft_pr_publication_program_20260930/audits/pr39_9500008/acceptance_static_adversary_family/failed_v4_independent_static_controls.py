"""Independent data/AST reader and finite models. Never imports reviewed helpers.
Own outputs only; no Git, native, remote, helper execution, or mutation.
"""
from pathlib import Path, PurePosixPath
import ast, datetime as dt, difflib, hashlib, json, os, re
R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr39_9500008'
P=A/'acceptance_preparation_family'
O=A/'acceptance_static_adversary_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda t:(_ for _ in ()).throw(ValueError('nonfinite '+t)))
def enc(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
def read(p):
 p=Path(p)
 assert p.is_relative_to(R) and not p.is_symlink()
 for q in p.parents:
  if q==R.parent:break
  assert not q.is_symlink(),str(q)
 return p.read_bytes()
seen={}
def pin(row,base=R):
 q=PurePosixPath(row['path']);assert not q.is_absolute() and '..' not in q.parts and str(q)==row['path'] and '\\' not in str(q)
 b=read(base/str(q));n=row.get('bytes',row.get('size'));assert n==len(b) and sha(b)==row['sha256'],str(base/q)
 seen[str((base/q).relative_to(R))]={'bytes':len(b),'sha256':sha(b)}
 return b
def scan(base):
 fs=set();ds=set()
 for root,dirs,files in os.walk(base,followlinks=False):
  for n in dirs+files:
   p=Path(root)/n;assert not p.is_symlink() and (p.is_file() or p.is_dir()),str(p)
  ds.update(str((Path(root)/n).relative_to(base)) for n in dirs)
  fs.update(str((Path(root)/n).relative_to(base)) for n in files)
 return fs,ds
def parentdirs(paths):
 out=set()
 for s in paths:
  p=PurePosixPath(s).parent
  while str(p)!='.':out.add(str(p));p=p.parent
 return out
def closure(base,rows,selfname,extras=(),empty=(),exclude=()):
 assert len({x['path'] for x in rows})==len(rows)
 names={x['path'] for x in rows}|{selfname}|{x['path'] for x in extras}
 for row in rows+list(extras):pin(row,base)
 fs,ds=scan(base)
 def excluded(n):return any(n==t or n.startswith(t+'/') for t in exclude)
 fs={n for n in fs if not excluded(n)};ds={n for n in ds if not excluded(n)}
 assert fs==names,(str(base),sorted(fs-names),sorted(names-fs))
 wanted=parentdirs(names)|set(empty)|parentdirs(empty)
 assert ds==wanted,(str(base),sorted(ds-wanted),sorted(wanted-ds))
 for n in empty:assert not any((base/n).iterdir())
 return {'base':str(base.relative_to(R)),'authored':len(rows),'extra':len(extras),'excluded':list(exclude),'qualified_empty_directories':list(empty),'files_with_self_and_extras':len(fs),'directories':len(ds)}
# Original preparation and full adaptation byte reconstruction.
mraw=read(P/'PREPARATION_MANIFEST.json');assert sha(mraw)=='f66df61cb4b57ae63cc007fed3c4dabf9e67e027f1d428d4e0ffbc75a6332fca'
m=parse(mraw);assert m['files_count']==15 and m['helpers_imported_or_executed'] is False
prep=closure(P,m['files'],'PREPARATION_MANIFEST.json')
sb=parse(read(P/'SOURCE_BINDINGS.json'));patch=[];sources=[]
for z in sb['complete_sources']:
 before=pin(z['sealed_predecessor']);after=pin(z['new'])
 assert len(before.splitlines())==z['predecessor_lines'] and len(after.splitlines())==z['new_lines']
 ast.parse(after,filename=z['new']['path'])
 patch+=list(difflib.unified_diff(before.decode().splitlines(keepends=True),after.decode().splitlines(keepends=True),fromfile=z['sealed_predecessor']['path'],tofile=z['new']['path']))
 sources.append({'path':z['new']['path'],'sha256':sha(after),'lines':len(after.splitlines()),'full_literal_read':True,'AST_parsed_only':True})
assert ''.join(patch).encode()==pin(sb['patch'])
pin(sb['predecessor_manifest'])
ib=parse(read(P/'INPUT_BINDINGS.json'))
for k,v in ib['pins'].items():pin(v)
closures=[];json_n=0;jsonl_n=0;negative=[]
exceptions={z['path']:z for z in ib['qualified_JSON_negative_inputs']};assert len(exceptions)==14
for z in ib['closures']:
 mp=R/z['manifest']['path'];v=parse(pin(z['manifest']));rows=v[z['member_field']];rows=[{'path':k,**w} for k,w in rows.items()] if type(rows) is dict else rows
 assert len(rows)==z['authored_count']
 closures.append({'role':z['role'],**closure(mp.parent,rows,mp.name,z['qualified_extra_members'],z['qualified_empty_directories'],z['excluded_root_private_trees'])})
 for row in rows:
  p=mp.parent/row['path'];rel=str(p.relative_to(R));b=read(p)
  if rel in exceptions:
   x=exceptions[rel];pin(x)
   try:parse(b)
   except (ValueError,json.JSONDecodeError) as e:assert str(e)==x['parse_failure'];negative.append({'path':rel,'failure':str(e),'bytes':len(b),'sha256':sha(b)})
   else:raise AssertionError('negative parsed: '+rel)
  elif p.suffix=='.json':parse(b);json_n+=1
  elif p.suffix=='.jsonl':
   assert not b or b.endswith(b'\n')
   for line in b.splitlines():parse(line)
   jsonl_n+=1
assert set(x['path'] for x in negative)==set(exceptions)
cur=parse(read(A/'reviewed_candidate/MANIFEST.json'))
# Dependencies exact whole-byte rows independently checked.
deps=parse(read(A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json'));assert len(deps['files'])==2797
for row in deps['files']:pin(row,A)
current_exception_rows=ib['current_malformed_json_exceptions'];assert len(current_exception_rows)==6
for row in current_exception_rows:pin(row,A/'reviewed_candidate');assert str((A/'reviewed_candidate'/row['path']).relative_to(R)) in exceptions
# Full outer captures and typed child rows are read; no capture constructed.
outer=[];typed=[]
for z in ib['outer_typed_captures']:
 cap=parse(pin(z['capture']));base=(R/z['capture']['path']).parent
 closure(base,z['files'],z['capture']['path'].split('/')[-1]) # self is already in supplied rows: set union exact
 assert cap['pid']==z['expected_pid'] and cap['exit_code']==z['expected_exit_code'] and cap['actual_execution'] is True and cap['completed'] is True
 outer.append({'pid':cap['pid'],'exit_code':cap['exit_code'],'capture_sha256':sha(read(base/'CAPTURE.json'))})
for dirname in ['root_typed_entry_actual_capture','root_typed_entry_actual_capture_v2']:
 base=A/dirname
 v=parse(read(base/'TYPED_ENTRY_RECEIPT.json'));rows=v['actual_runs'];assert len(rows)==20
 assert rows==parse(read(base/'RUNS.json'))
 assert [q['exit_code'] for q in rows[1:18]]==[1]*17 and rows[0]['exit_code']==0 and rows[18]['exit_code']==0 and rows[19]['exit_code']==(1 if dirname=='root_typed_entry_actual_capture' else 0)
 for q in rows:
  assert q['actual_execution'] is True and q['completed'] is True and q['stdin_supplied'] is False
  for k in ['source','stdout','stderr']:pin(q[k],A)
 typed.append({'directory':dirname,'receipt':str((base/'TYPED_ENTRY_RECEIPT.json').relative_to(R)),'rows':len(rows),'negative_controls':17,'builder_exit':rows[-1]['exit_code']})
# Original dictionary attempts schema and scientific boundaries.
ledger=parse(read(A/'reviewed_candidate/turns.json'))
assert type(ledger) is dict and type(ledger['attempts']) is list and len(ledger['attempts'])==2 and [z['number'] for z in ledger['attempts']]==[1,2]
assert read(A/'reviewed_candidate/turns.json')==read(A/'reviewed_candidate/original_archive/turns.json')
draft=parse(read(P/'DRAFT_FINAL_PLAN.json'))
assert draft['full_problem_solved'] is False and draft['positive_novelty_claim'] is False and draft['original_substantive_attempts']==2 and draft['new_substantive_attempts']==0 and draft['audit_turns']==0
for k in ['current_model','current_reasoning_effort','current_deadline_utc','preparation_manifest_sha256']:assert draft[k] is None
for k in ['root_full_current_read_completed','root_full_whole_scope_read_completed','independent_whole_current_pass']:assert draft[k] is False
assert len(draft['immutable_evidence_references'])==33
for row in draft['immutable_evidence_references']:pin(row)
# Historical exactly-eight run1 exceptions; inspect all exact bodies too.
ex=parse(pin(ib['pins']['capability_exception']))
assert len(ex['files'])==8
for x in ex['files']:
 assert x['path'].endswith('.run1');b=pin(x,A/'root_closed_families_actual_reproduction_support')
 if x['path'].endswith('.json.run1'):parse(b)
# Source constructor fully read, preserving empty directory as historical evidence.
construct=read(A/'uniform_error_scaling_family/run_manifest_controls.py').decode()
assert "if name == 'missing':" in construct and "(d/'nested/b.txt').unlink()" in construct
assert not list((A/'uniform_error_scaling_family/manifest_control_fixtures/missing/nested').iterdir())
# Actual baseline and fresh read-only observation of the 13 archived input names.
previous=R/'draft_pr_publication_program_20260930/audits/pr38_2765/state_mirror_bindings.json'
assert sha(read(previous))=='82d2d2b1c598fd6c95f6de1ce3ba8cc1f468c6b6291aa859eae9d8b1cd636b3e'
prev=parse(read(previous));assert len(prev['entries'])==28
state=parse(read(R/'unsolved_math_prioritization/state.json'));hist=read(R/'unsolved_math_prioritization/history.jsonl');inventory=parse(read(R/'draft_pr_publication_program_20260930/inventory.json'))
assert len(state)==29 and sum(z['turns_used'] for z in state.values())==35 and '9500008' not in state
assert inventory['completed_count']==28
assert not any(str(parse(line).get('id',parse(line).get('problem_id',''))) == '9500008' for line in hist.splitlines())
assert read(R/'.git/HEAD').strip()==b'ref: refs/heads/main'
arch=parse(read(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'));assert len(arch['files'])==13
fresh=[]
for row in arch['files']:
 b=read(R/row['path']);fresh.append({'path':row['path'],'bytes':len(b),'sha256':sha(b),'matches_dated_archive':len(b)==row['size'] and sha(b)==row['sha256']})
# Independent finite semantic models; no reviewed function executed or imported.
# Exclusive absence check plus replacing publish admits another creator between them.
transitions=[('check_absent',None),('foreign_create','foreign-complete'),('publish_replace','our-complete')]
cell=None
for name,value in transitions:
 if name=='check_absent':assert cell is None
 else:cell=value
assert cell=='our-complete'
race={'schedule':[x[0] for x in transitions],'foreign_creation_overwritten':True,'atomic_link_publish_would_reject':True}
# Exact set equality loses channel cardinality. Inputs are abstract names, not receipts.
expected={'CAPTURE.json','prelaunch_source.py','stream.bin','stream.bin'}
actual={'CAPTURE.json','prelaunch_source.py','stream.bin'}
assert actual==expected and len(actual)==3
alias={'distinct_name_requirement':4,'set_validator_accepts':len(actual),'stdout_stderr_alias_admitted':True}
weak_clocks=[('banana','earlier'),('2026-10-02T14:00:00+00:00','2026-10-02T13:00:00+00:00'),('2026-10-02T13:00:00','2026-10-02T14:00:00')]
clocks=[]
for start,end in weak_clocks:
 weak=type(start) is str and bool(start) and type(end) is str and bool(end)
 try:
  s=dt.datetime.fromisoformat(start);e=dt.datetime.fromisoformat(end)
  strong=s.tzinfo is not None and e.tzinfo is not None and s.utcoffset()==dt.timedelta(0) and e.utcoffset()==dt.timedelta(0) and s<=e
 except ValueError:strong=False
 assert weak and not strong
 clocks.append({'start':start,'end':end,'existing_predicate_accepts':True,'aware_UTC_order_predicate_rejects':True})
# Static source locations substantiate modeled predicates and separate safe directory sealer.
guard=read(P/'pr39_guards.py').decode();sealer=read(P/'seal_final_evidence.py').decode()
assert 'os.replace(temporary, path)' in guard and 'if exclusive:' in guard
assert "exact_closure(cap_base, {paths['reconciliation_capture'].name, 'prelaunch_source.py', capture['stdout']['path'], capture['stderr']['path']})" in guard
assert "capture['started_utc'] and type(capture['finished_utc']) is str" in guard
assert 'RENAME_EXCL' in sealer
result={'schema':'independent-pr39-acceptance-static-controls/v1','status':'PASS_CONTROLS_WITH_ACTIONABLE_STATIC_GAPS','helpers_imported_or_executed':False,'science_reexecuted':False,'Git_shared_native_remote_writes':False,'preparation_manifest_sha256':sha(mraw),'preparation':prep,'complete_helper_source_coverage':sources,'exact_adaptation_patch_reconstructed':True,'closures':closures,'unique_bound_files':len(seen),'unique_bound_bytes':sum(v['bytes'] for v in seen.values()),'strict_JSON_valid_occurrences':json_n,'JSONL_files_occurrences':jsonl_n,'exact_qualified_negative_inputs':negative,'current_exact_malformed_count':6,'typed_outers':outer,'typed_child_receipts':typed,'ledger_original_dictionary_two_attempts':True,'draft_flags_false_null_zero':True,'whole_evidence_references':33,'exact_run1_exceptions':8,'empty_historical_missing_nested_constructor_qualified':True,'baseline':{'states':len(state),'consumed_substantive_turns':sum(z['turns_used'] for z in state.values()),'history_events':len(hist.splitlines()),'previous_entries':len(prev['entries']),'previous_mirror_sha256':sha(read(previous))},'fresh_readonly_static_observation_NOT_integration_gate':fresh,'finite_controls':{'exclusive_race':race,'capture_alias':alias,'invalid_or_reversed_or_naive_clocks':clocks},'limitations':['No prepared helper import/execution. This is a static acceptance audit, not an actual integration receipt.','Root must freshly bind/check/read all exact 13 input names before and after every actual phase, plus helper four shared gates and two foreign tracked logs. Dated archive remains untouched.','Mirror lock protects cooperative writers only; noncooperating shared file writers are outside that protocol.']}
(O/'STATIC_CONTROL_RESULTS.json').write_bytes(enc(result))
(O/'EXACT_BYTE_BINDINGS.json').write_bytes(enc({'files':seen,'count':len(seen)}))
print(json.dumps({'status':result['status'],'unique_bound_files':len(seen),'unique_bound_bytes':result['unique_bound_bytes'],'closure_count':len(closures),'negative_count':len(negative),'typed_child_receipts':typed,'baseline':result['baseline'],'static_defects':3},sort_keys=True))

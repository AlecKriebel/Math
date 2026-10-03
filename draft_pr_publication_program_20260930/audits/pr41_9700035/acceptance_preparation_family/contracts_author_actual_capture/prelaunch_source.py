#!/usr/bin/env python3
"""Own immutable-input/static author only. No prepared helper is imported/run."""
import ast
import datetime as dt
import hashlib
import json
import math
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;A=P.parent;R=A.parents[2];C=A/'reviewed_candidate'
NOW=dt.datetime.now(dt.timezone.utc).isoformat();READ={}
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
 def pairs(rr):
  o={}
  for k,v in rr:
   assert k not in o,'Duplicate JSON key';o[k]=v
  return o
 def floating(v):
  n=float(v);assert math.isfinite(n);return n
 return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def read(p):
 assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 b=p.read_bytes();READ[str(p.relative_to(R))]={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
 if p.suffix=='.json':parse(b)
 return b
def row(p):
 b=read(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(root,rr):
 assert len({z['path'] for z in rr})==len(rr)
 for z in rr:
  q=PurePosixPath(z['path']);assert not q.is_absolute() and not {'.','..','.git','__pycache__'}.intersection(q.parts) and q.as_posix()==z['path']
  b=read(root/z['path']);assert len(b)==z.get('bytes',z.get('size')) and sha(b)==z['sha256']
def exact(root,names):
 files=set();dirs=set()
 for p in root.rglob('*'):
  assert not p.is_symlink()
  if p.is_file():files.add(p.relative_to(root).as_posix())
  else:assert p.is_dir();dirs.add(p.relative_to(root).as_posix())
 assert files==set(names)
 assert dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'}
def put(name,obj):
 p=P/name;assert not p.exists();p.write_bytes(obj.encode() if isinstance(obj,str) else (json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())

prepared=parse(read(A/'current_preparation_family/INPUT_PINS.json'));closures=[]
for name,info in prepared['families'].items():
 m=info['manifest'];assert sha(read(A/name/m['path']))==m['sha256']
 authored,foreign=info['members'],info['foreign_members'];check(A/name,authored+foreign);exact(A/name,{z['path'] for z in authored+foreign}|{m['path']})
 closures.append({'directory':name,'manifest_name':m['path'],'manifest_sha256':m['sha256'],'members':authored,'foreign_members':foreign})
for label,info in prepared['root_support'].items():
 m=parse(read(A/info['directory']/'MANIFEST.json'));assert sha((A/info['directory']/'MANIFEST.json').read_bytes())==info['manifest_sha256']
 check(A/info['directory'],m['files']);exact(A/info['directory'],{z['path'] for z in m['files']}|{'MANIFEST.json'})
 closures.append({'directory':info['directory'],'manifest_name':'MANIFEST.json','manifest_sha256':info['manifest_sha256'],'members':m['files'],'foreign_members':[]})
oldprep=parse(read(A/'current_preparation_family/PREPARATION_MANIFEST.json'));check(A/'current_preparation_family',oldprep['files']);exact(A/'current_preparation_family',{z['path'] for z in oldprep['files']}|{'PREPARATION_MANIFEST.json'})
closures.append({'directory':'current_preparation_family','manifest_name':'PREPARATION_MANIFEST.json','manifest_sha256':sha((A/'current_preparation_family/PREPARATION_MANIFEST.json').read_bytes()),'members':oldprep['files'],'foreign_members':[]})
current=parse(read(C/'MANIFEST.json'));assert sha((C/'MANIFEST.json').read_bytes())=='3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa' and len(current['files'])==547
check(C,current['files']);exact(C,{z['path'] for z in current['files']}|{'MANIFEST.json'})
deps=parse(read(C/'CURRENT_PROOF_DEPENDENCIES.json'));assert sha((C/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes())=='ade2f6fe9890f1038810158a284f4a8924e34d6d2f95b3a07654d78fa6501ff6' and len(deps['files'])==469;check(A,deps['files'])
names=['snapshot_manifest.json','pr_input/diff.patch','pr_input/metadata.json','source_snapshot/PROOF.md','source_snapshot/source_record.json','source_snapshot/prior_report.json','source_snapshot/turns.json','source_snapshot/attempt.json',
       'primary_scope_family/SOURCE_PROOF_QUALIFICATIONS.md','ROOT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CLOSED_FAMILY_INSPECTION.json','ROOT_CURRENT_PACKET_INSPECTION.json',
       'root_current_freeze_actual_capture/CAPTURE.json','reviewed_candidate/MANIFEST.json','reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json']
names += [c['directory']+'/'+c['manifest_name'] for c in closures]
assert len(set(names))==len(names)
pins={name:row(A/name) for name in names}
freeze=parse(read(A/'root_current_freeze_actual_capture/CAPTURE.json'));assert freeze['pid']==36236 and type(freeze['pid']) is int and freeze['exit_code']==0 and type(freeze['exit_code']) is int
check(A/'root_current_freeze_actual_capture',[freeze['stdout'],freeze['stderr']]);exact(A/'root_current_freeze_actual_capture',{'CAPTURE.json','prelaunch_source.py',freeze['stdout']['path'],freeze['stderr']['path']})
capmembers=[{'path':p.relative_to(A/'root_current_freeze_actual_capture').as_posix(),'bytes':len(read(p)),'sha256':sha(p.read_bytes())} for p in sorted((A/'root_current_freeze_actual_capture').iterdir())]
closures.append({'directory':'root_current_freeze_actual_capture','manifest_name':'CAPTURE.json','manifest_sha256':sha((A/'root_current_freeze_actual_capture/CAPTURE.json').read_bytes()),'members':[z for z in capmembers if z['path']!='CAPTURE.json'],'foreign_members':[]})
whole=A/'whole_current_source_first_family';wm=parse(read(whole/'FIRST_PARTY_MANIFEST.json'));check(whole,wm['files']+wm['foreign_files']);exact(whole,{z['path'] for z in wm['files']+wm['foreign_files']}|{'FIRST_PARTY_MANIFEST.json'})
assert sha((whole/'FIRST_PARTY_MANIFEST.json').read_bytes())=='233867cfb7e18b910f1ec17c9a57a386eadd1793ff3a44328260e204d8304130'
assert len(wm['files'])==143 and len(wm['foreign_files'])==17
whole_observed={'path':(whole/'FIRST_PARTY_MANIFEST.json').relative_to(R).as_posix(),'bytes':len((whole/'FIRST_PARTY_MANIFEST.json').read_bytes()),'sha256':sha((whole/'FIRST_PARTY_MANIFEST.json').read_bytes()),'source_preparer_observation_not_ROOT_approval':True}
root_whole_observed=row(A/'ROOT_WHOLE_CURRENT_REVIEW.json')
assert root_whole_observed['sha256']=='28addc78a418ac5ad72a1e7f8cfacda16ec52ba5db52132b16c92602a3f4965e'
root_whole=parse((A/'ROOT_WHOLE_CURRENT_REVIEW.json').read_bytes())
assert root_whole['status']=='PASS' and root_whole['authored_members']==143 and root_whole['separately_bound_foreign_members']==17 and root_whole['independent_family_manifest_sha256']==whole_observed['sha256']
ledger=parse(read(A/'ROOT_PRIMARY_READ_LEDGER.json'))
scope={'schema':'pr41-proposed-accepted-scientific-scope/v1','id':'9700035','problem_number':'AMR-096-0035','literal_target_status':'UNSOLVED','full_problem_solved':False,'novelty_claimed':False,
       'functional':'Expected geometric length of union of every prescribed pair route, exterior included and overlaps counted once; not a Steiner minimum.',
       'unconditional':'Expected interior length/k tends to ell; full-length liminf/k at least ell.',
       'conditional':'Full expected-length law only with additional t^4 P(D>t)->0; finite fourth moment sufficient and not claimed necessary.',
       'weak_vs_full':'Finite major-road intensity p(1) is used for exterior control and is not automatic for weak SIRSN.',
       'indexed_vs_published':'Indexed Aldous2012 Problem35 is unconditional. Published2014 Problem9 asks which additional assumptions suffice.',
       'exact_remaining_gap':'Expected total exterior route-union length o(k) from ordinary SIRSN axioms, or an admissible full-SIRSN counterexample.',
       'generic_countercontrols':'Scalar tails, triangles and escaping random measures falsify generic inference rules, not the SIRSN target.',
       'qualified_imports':'Kahn joint-event rather than dependent time conditioning; T_n radius/indexing and shifted sums; geometric constant/inequality reconstruction; slow length equals speed times time. Credited q<gamma-1 survives; planar gamma>5 gives fourth moment, gamma=5 excluded; stronger conjectured moments not promoted.',
       'qualification_path':'SOURCE_PROOF_QUALIFICATIONS.md','qualification_sha256':'69196e84de0d627b31b6f2a20a3745ba33048969cb93efba92a886bfedf8bc7e',
       'root_primary_read_limits':ledger['primary_read_limits'],'external_foundations':'Continuum construction, existence/uniqueness and primary measurable framework are credited external inputs, not recursively recertified.',
       'present_summary_correction':'CURRENT_CONTEXT_PRESENT.md and CURRENT_AUDIT_SCOPE_PRESENT.md point to qualification and original_archive bodies. Frozen CURRENT_CONTEXT/CURRENT_AUDIT_SCOPE remain dated archival summaries; their appended-below/follows phrases do not promise embedded bodies.',
       'original16_and_PROOF_unchanged':True,'PRESENT_prior_archival_interpretation_corrected_separately':True,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,
       'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_DOI_or_tracker':False,'human_peer_review_asserted':False,
       'source_preparation_actual_acceptance_execution':'NOT_PERFORMED_IN_THIS_SOURCE_PREPARATION','source_preparation_does_not_certify_future_gates':True}
put('SCIENTIFIC_SCOPE.json',scope)
put('INPUT_BINDINGS.json',{'schema':'pr41-acceptance-source-fixed-input-bindings/v1','created_utc':NOW,'source_only':True,'pins':pins,'closures':closures,'whole_observed_only':whole_observed,'root_whole_observed':root_whole_observed,'root_whole_actual_read_record_observed':True,'future_ROOT_bindings_or_final_acceptance_asserted':False,'previous_PR40_mirror_SHA_invented':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0})
science={'full_problem_solved':False,'partial_valid':False,'novelty_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'verification_attempts_added':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'paper_or_new_doi_or_tracker':False}
put('DRAFT_FINAL_PLAN.json',{'schema':'pr41-root-reviewed-final-plan/v1','plan_status':'PENDING_ROOT_FULL_REVIEW_AND_ACTUAL_RECONCILIATION','pr':41,'problem_id':9700035,'original_head':'292b95ca601f166e6d246e609cf7ed5ca5653e25','original_base':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0','reviewed_candidate_manifest_sha256':'3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa','current_proof_dependencies_sha256':'ade2f6fe9890f1038810158a284f4a8924e34d6d2f95b3a07654d78fa6501ff6','whole_manifest_sha256':None,'preparation_manifest_sha256':None,'root_bindings':None,'root_bindings_sha256':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'independent_whole_current_pass':False,'mandatory_corrections':[],'science_reexecution_of_current':False,'historical_PASS_transferred':False,'immutable_evidence_references':[],'scientific_scope':scope,**science})
put('DRAFT_ROOT_IMMUTABLE_BINDINGS.json',{'schema':'pr41-root-approved-immutable-acceptance-bindings/v1','status':'PENDING_ROOT_ACTUAL_WHOLE_READING_APPROVAL','created_utc':None,'root_full_current_read_completed':False,'root_full_whole_read_completed':False,'independent_whole_current_pass':False,'mandatory_corrections':[],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'whole_manifest':None,'root_whole_inspection':None})
put('DRAFT_FUTURE_GATE_PINS.json',{'status':'SOURCE_ONLY_FUTURE_ACTUAL_INPUTS_NOT_SUPPLIED_OR_CERTIFIED_HERE','previous_mirror':None,'previous_mirror_sha256':None,'previous_post':None,'previous_post_sha256':None,'fresh_preimage':None,'fresh_preimage_sha256':None,'final_plan':None,'final_plan_sha256':None,'final_receipt':None,'final_receipt_sha256':None,'final_manifest':None,'final_manifest_sha256':None,'reconciliation_capture':None,'reconciliation_capture_sha256':None,'actual_execution':False})
helper_rows=[]
for name in ['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
 b=read(P/name);ast.parse(b);helper_rows.append(row(P/name))
 assert 'import pr40_guards' not in b.decode()
put('STATIC_READ_INSPECTION.json',{'status':'PASS_OWN_READ_STATIC_ONLY','utc':NOW,'files':sorted(READ.values(),key=lambda z:z['path']),'unique_files':len(READ),'whole_bytes':sum(z['bytes'] for z in READ.values()),'helper_sources':helper_rows,'prepared_helpers_imported_or_executed':False,'AST_only':True,'own_raw_SQL_reexecution_claimed':False,'ROOT_future_whole_approval_or_final_capture_claimed':False,'native_canonical_Git_remote_writes':False,'source_preparation_completion_estimate_percent':90,'unconditional_discovery_estimate_percent':0,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0})
print(json.dumps({'status':'SOURCE_ONLY_CONTRACT_INPUTS_STATICALLY_AUTHORED','files_read':len(READ),'bytes_read':sum(z['bytes'] for z in READ.values()),'current':547,'dependencies':469,'whole_observed_authored':143,'whole_observed_foreign':17,'ROOT_whole_approval_claimed':False,'prepared_helpers_imported_or_executed':False,'future_actual_gates':'PENDING'},indent=2))

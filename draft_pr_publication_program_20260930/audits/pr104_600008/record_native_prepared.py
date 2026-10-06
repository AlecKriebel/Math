from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(c,m):
 if not c:raise RuntimeError(m)
receipt=load(A/'native_prior_disposition_finalization_20261006/PREPARED_RECEIPT.json')
for pin in receipt['native_pins']:
 p=C/pin['path'];b=p.read_bytes();require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'prepared native pin changed')
require(receipt['other_native_targets_preserved'] and receipt['original_budget']=='1/5' and receipt['status']=='already_solved','native gate')
closed=load(A/'actual_closure_20261006/RECEIPT.json');require(closed['same_head_closed_without_merge'] and closed['comment_body_readback_exact'],'actual closure')
t=now();progress=load(P/'CURRENT_PROGRESS.json');require(progress['current_PR']==104 and progress['fully_completed_count']==14,'progress baseline')
progress.update(UTC=t,updated_UTC=t,current_PR_workflow_percent=95,current_workflow_estimate_percent=95,current_final_disposition_review_pending=False,
 current_final_disposition_review_authenticated=True,current_actual_closing_comment_url=closed['closing_comment_url'],current_actual_closed_without_merge=True,
 current_native_integration_complete=False,current_native_integration_prepared=True,current_native_prepared_record='audits/pr104_600008/native_prior_disposition_finalization_20261006/PREPARED_RECEIPT.json',
 current_priority_checkpoint='d3d6085c982fb82d50e21477aca5589e9e137313',current_priority_checkpoint_remote_verified=True,
 current_final_disposition_gate='audits/pr104_600008/ROOT_DISPOSITION_READY_20261006.json',advance_to_next_PR_authorized_now=False,
 current_new_central_proof_search_turns=0,current_original_budget='1/5',current_DOI=None,current_merge_commit=None,current_tracker_range=None,
 next_step='Commit and independently read back source-bound prior analytic disposition; then ordered eligible intake from105.',
 remaining_current_step='Native main checkpoint and actual final service/native/readback; no publication.',persistent_goal_complete=False,persistent_goal_status='active')
dump(P/'CURRENT_PROGRESS.json',progress)
record={'schema':'pr104-native-prepared-root-gate/v1','UTC':t,'actual_operator_PID':os.getpid(),'PR':104,
 'actual_closed_without_merge':True,'closing_comment_url':closed['closing_comment_url'],'native_prepared':True,'native_status':'already_solved',
 'scope':'literal analytic classification, verified prior reconstruction/classical corollary','original_budget':'1/5','new_central_proof_search_turns':0,
 'fresh_disposition_review_authenticated':True,'workflow_percent':95,'main_checkpoint_pending':True,'completed_program_count':14,
 'original_proof_preserved':True,'historical_assessment_preserved':True,'other_targets_not_reassessed':True,'DOI':None,'primary_checkout_mutated':False,
 'native_prepared_receipt':'native_prior_disposition_finalization_20261006/PREPARED_RECEIPT.json'}
dump(A/'ROOT_NATIVE_PREPARED_20261006.json',record)
line=t+' — PR104 actual same-head closure verified with exact comment readback. Fresh source-bound native assessment/status prepared in isolated backend; original1/5 imported, audit proof-search0. Canonical commands exposed48 preexisting unrelated stale catalog projections; scoped output rendering preserves those baseline rows and all other assessments/states/history prefixes. Source/math/bounded priority100%, disposition95% pending actual committed main/service readback; program14/99=14.14%. No merge, paper, DOI or tracker. Primary checkout/index unchanged.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+line)
paths=set(receipt['native_paths'])
for name in ['authenticate_final_disposition.py','close_pr104_prior_result.py','prepare_native_prior_disposition.py','finish_native_prior_disposition.py','record_native_prepared.py',
 'ROOT_DISPOSITION_READY_20261006.json','ROOT_NATIVE_PREPARED_20261006.json','NATIVE_REGENERATION_UNRELATED_DIFFERENCES_20261006.json','RESEARCH_LOG.md']:
 paths.add(str((A/name).relative_to(C)))
for dirname in ['actual_closure_20261006','native_prior_disposition_20261006','native_prior_disposition_finalization_20261006']:
 for f in (A/dirname).iterdir():
  if f.is_file():paths.add(str(f.relative_to(C)))
for f in (A/'native_prior_disposition_20261006_retry1').iterdir():
 if f.is_file():paths.add(str(f.relative_to(C)))
for f in (A/'final_disposition_adversary_20261006').iterdir():
 if f.is_file():paths.add(str(f.relative_to(C)))
for label in ['final_disposition_gate','actual_prior_closure','native_prior_disposition','refresh_main_before_native','reconcile_main_before_native','native_prior_disposition_retry1','native_prior_disposition_finalization','priority_release']:
 for f in (A/'actual_operations'/label).iterdir():
  if f.is_file():paths.add(str(f.relative_to(C)))
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:paths.add(str((A/'actual_checkpoints/priority_release'/name).relative_to(C)))
for f in [P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md']:paths.add(str(f.relative_to(C)))
selection={'schema':'pr104-explicit-native-checkpoint-selection/v1','UTC':t,'paths':sorted(paths),
 'private_backend_and_third_party_sources_excluded':True,'selection_bytes':sum((C/p).stat().st_size for p in paths)}
dump(A/'NATIVE_CHECKPOINT_SELECTION_20261006.json',selection)
print(json.dumps({'workflow_percent':95,'selection_paths':len(paths),'selection_bytes':selection['selection_bytes'],'actual_operator_PID':os.getpid()}))

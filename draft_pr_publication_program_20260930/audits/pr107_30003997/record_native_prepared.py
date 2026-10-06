from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(c,m):
 if not c:raise RuntimeError(m)
r=load(A/'native_prior_disposition_20261006/PREPARED_RECEIPT.json');closed=load(A/'actual_closure_20261006/RECEIPT.json');cp=load(A/'actual_checkpoints/priority_disposition_release/RECEIPT.json')
for row in r['native_pins']:
 p=C/row['path'];b=p.read_bytes();require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'prepared native pin drift')
require(r['original_budget']=='1/5' and r['other_native_targets_preserved'] and r['status']=='already_solved','prepared disposition gate')
require(closed['same_head_closed_without_merge'] and closed['comment_body_readback_exact'] and cp['remote_verified'],'actual closure/evidence release')
t=datetime.datetime.now(datetime.timezone.utc).isoformat();prog=load(P/'CURRENT_PROGRESS.json');require(prog['current_PR']==107 and prog['fully_completed_count']==15,'progress baseline')
prog.update(UTC=t,updated_UTC=t,current_PR_workflow_percent=95,current_workflow_estimate_percent=95,current_actual_closing_comment_url=closed['closing_comment_url'],current_actual_closed_without_merge=True,current_native_integration_prepared=True,current_native_integration_complete=False,current_native_prepared_record='audits/pr107_30003997/native_prior_disposition_20261006/PREPARED_RECEIPT.json',current_priority_checkpoint=cp['commit'],current_priority_checkpoint_remote_verified=True,current_final_disposition_gate='audits/pr107_30003997/ROOT_DISPOSITION_READY_20261006.json',advance_to_next_PR_authorized_now=False,next_step='Commit source-bound already_solved native assessment/status, then actual closure and committed remote readback.',remaining_current_step='Native main release and actual final readback; no paper/DOI/tracker.',persistent_goal_status='active',persistent_goal_complete=False)
dump(P/'CURRENT_PROGRESS.json',prog)
record={'UTC':t,'actual_operator_PID':os.getpid(),'PR':107,'actual_closed_without_merge':True,'closing_comment_url':closed['closing_comment_url'],'native_prepared':True,'native_status':'already_solved','scope':'complete advertised hardness bundle as published-construction corollary','original_budget':'1/5','new_central_proof_search_turns':0,'fresh_disposition_review_authenticated':True,'workflow_percent':95,'main_checkpoint_pending':True,'program_completed_count':15,'historical_assessment_preserved':True,'other_targets_not_reassessed':True,'DOI':None,'primary_checkout_mutated':False}
dump(A/'ROOT_NATIVE_PREPARED_20261006.json',record)
line=t+' — PR107 actual same-head CLOSED/unmerged with exact public explanation readback. Native fresh assess/status prepared in private backend, original1/5 imported, new proof turns0. Complete restricted theorem is prior2022 corollary, exact identity priority unresolved. Source/math/bounded priority100%, disposition95% pending committed native/service readback; goal active15/99. Other target assessments/states/campaign rows preserved; existing unrelated stale projections retained. No paper/DOI/tracker/merge.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+line)
paths=set(r['native_paths'])
for name in ['ROOT_NATIVE_PREPARED_20261006.json','record_native_prepared.py','prepare_native_prior_disposition.py','PRIOR_DISPOSITION_CHECKPOINT_SELECTION_20261006.json','RESEARCH_LOG.md']:paths.add(str((A/name).relative_to(C)))
for p in [P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md']:paths.add(str(p.relative_to(C)))
for folder in [A/'actual_closure_20261006',A/'native_prior_disposition_20261006']:
 paths.update(str(p.relative_to(C)) for p in folder.iterdir() if p.is_file())
for label in ['actual_prior_closure','native_prior_disposition','priority_disposition_release']:
 paths.update(str(p.relative_to(C)) for p in (A/'actual_operations'/label).iterdir() if p.is_file())
paths.update(str((A/'actual_checkpoints/priority_disposition_release'/n).relative_to(C)) for n in ['RECEIPT.json','PROCESS_JOURNAL.json'])
dump(A/'NATIVE_CHECKPOINT_SELECTION_20261006.json',{'paths':sorted(paths),'UTC':t,'private_backend_and_third_party_sources_excluded':True,'selection_bytes':sum((C/p).stat().st_size for p in paths)})
print(json.dumps({'workflow_percent':95,'selection_paths':len(paths),'actual_operator_PID':os.getpid()}))

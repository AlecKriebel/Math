"""Read-only final source/package/remote/queue/budget/history verification."""
from pathlib import Path
import argparse, datetime, hashlib, importlib.util, json, subprocess
R=Path(__file__).resolve().parents[3];B=R/'draft_pr_publication_program_20260930'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
ap=argparse.ArgumentParser();ap.add_argument('--pr',type=int,choices=[34,35],required=True);n=ap.parse_args().pr
identity='7000004' if n==34 else '2744';used=2 if n==34 else 1;A=B/'audits'/('pr'+str(n)+'_'+identity);K=R/'unsolved_math_prioritization/attempts'/identity;C=A/('reviewed_candidate_v2' if n==34 else 'reviewed_candidate')
acc=load(A/'acceptance.json');can=load(K/'acceptance.json');assert {k:v for k,v in acc.items() if k not in ['canonical_manifest_sha256','canonical_manifest_entries']}==can
assert sha((K/'MANIFEST.json').read_bytes())==acc['canonical_manifest_sha256']
m=load(K/'MANIFEST.json');assert len(m['files'])==m['files_count']==acc['canonical_manifest_entries']
assert {str(p.relative_to(K)) for p in K.rglob('*') if p.is_file() and p!=K/'MANIFEST.json'}=={z['path'] for z in m['files']}
for z in m['files']:
 b=(K/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
 if z['path'].endswith('.json'):json.loads(b)
 if z['path'].endswith('.jsonl'):
  for line in b.splitlines():json.loads(line)
admin={'README.md','pr_body.md','readiness.json','current_status.json','CURRENT_AUDIT_SCOPE.md','RESEARCH_LOG.md','CURRENT_SOURCE_CONTEXT.json','CURRENT_RESEARCH_LOG.md','PR_DRAFT.md','provenance.json'}
unchanged=0
for z in load(C/'MANIFEST.json')['files']:
 p=K/('reviewed_pending_administration' if z['path'] in admin else '')/z['path'];assert p.read_bytes()==(C/z['path']).read_bytes(),z['path'];unchanged+=1
for z in load(C/'CURRENT_PROOF_DEPENDENCIES.json')['files']:
 b=(A/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
remote=json.loads(subprocess.check_output(['gh','pr','view',str(n),'--json','number,url,state,isDraft,headRefOid,mergeCommit,mergedAt,body'],cwd=R))
assert {k:remote[k] for k in load(A/'remote_merge_receipt.json')}==load(A/'remote_merge_receipt.json') and remote['body']==(K/'pr_body.md').read_text()==(A/'accepted_pr_body.md').read_text()
merge=can['merge_commit'];assert subprocess.check_output(['git','show','-s','--format=%P',merge],cwd=R,text=True).strip().split()==can['merge_parents']
assert subprocess.run(['git','merge-base','--is-ancestor',merge,'HEAD'],cwd=R).returncode==0
qp=load(K/'ACCEPTED_QUEUE_PATCH.json');q=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();old=(A/'integration_queue_before.md').read_bytes()
assert sha(q)==qp['whole_after_sha256'] and sha(old)==qp['whole_before_sha256'] and old.replace(qp['row_before'].encode(),qp['row_after'].encode())==q
assert q.replace(qp['row_after'].encode(),qp['row_before'].encode())==old
pre=load(A/'integration_preflight.json');old_state=subprocess.check_output(['git','show',merge+':unsolved_math_prioritization/state.json'],cwd=R);assert sha(old_state)==pre['state_before_sha256']
state=load(R/'unsolved_math_prioritization/state.json');assert all(state[k]==v for k,v in json.loads(old_state).items()) and state[identity]['turns_used']==used
plan=load(A/'state_mirror_plan.json');hist=(R/'unsolved_math_prioritization/history.jsonl').read_bytes();tail=plan['history_append_bytes'].encode();assert hist.endswith(tail) and sha(hist[:-len(tail)])==pre['history_before_sha256']
assert state==plan['state_after'] and sha(hist)==plan['history_after_sha256']
spec=importlib.util.spec_from_file_location('mirror',B/'infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);orig=v.ledger_budget
def ledger(data,kind,amount,limit):
 if kind=='json_zero_source_triage':
  obj=json.loads(data);v.require(str(obj['problem_id'])=='30002145' and amount==obj['used']==0 and limit==obj['limit']==5 and obj['substantive_proof_attempts']==[] and obj['reason'],'Invalid zero-triage ledger')
 elif kind=='json_substantive_responses':
  obj=json.loads(data);v.require(obj['problem_id']==2744 and obj['problem_number']=='KP-1.85' and amount==obj['substantive_turns_used']==1 and limit==obj['turn_limit']==5 and obj['outcome']=='unsolved' and [z['turn'] for z in obj['responses']]==[1] and obj['responses'][0]['outcome']=='unsolved' and obj['responses'][0]['artifact']=='OBSTRUCTION.md','Invalid original response ledger')
 else:orig(data,kind,amount,limit)
v.ledger_budget=ledger;proposal=load(A/'state_mirror_bindings.json')
for name in ['inventory','queue']:proposal[name]={'path':proposal[name]['path'],'sha256':sha((R/proposal[name]['path']).read_bytes())}
fresh=v.build_plan(R,proposal);validation=v.validate_plan(R,fresh);assert not fresh['history_append'] and fresh['state_after']==state
inv=load(B/'inventory.json');count=sum(z.get('stage')=='complete' for z in inv['items']);assert inv['completed_count']==count==(24 if n==34 else 25) and inv['program_completion_estimate_percent']==count/180*100
for z in load(A/'snapshot_manifest.json')['files']:assert subprocess.check_output(['git','show',can['original_head']+':unsolved_math_prioritization/attempts/'+identity+'/'+z['path']],cwd=R)==(K/'original_archive'/z['path']).read_bytes()
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','pr':n,'exact_remote_merge_and_parents_verified':True,'canonical_manifest_sha256':acc['canonical_manifest_sha256'],'canonical_members':len(m['files']),'all_reviewed_science_or_archived_admin_members_exact':unchanged,'named_row_only_actual_queue_change':True,'current_read_only_mirror_validation':validation,'history_exact_single_current_acceptance_append':True,'all_prior_states_preserved':len(json.loads(old_state)),'attempts':str(used)+'/5','no_new_proof_turn_by_acceptance_or_mirror':True,'completed_primary_prs':count,'program_completion_estimate_percent':count/180*100,'science_raw_source_original_attempts_closed_reviews_unchanged':True,'paper_DOI_tracker':False,'scope':'Final actual read-only verification; current global inventory binding refreshed without rewriting historical mirror plan or event.'}
(A/'ROOT_POST_ACCEPTANCE_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','pr':n,'canonical_members':len(m['files']),'bindings':validation['bindings_verified'],'completed':count,'attempts':str(used)+'/5'}))

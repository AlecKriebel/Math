from pathlib import Path
import datetime, hashlib, json, os, subprocess
A = Path(__file__).resolve().parent
C = A.parents[2]
P = A.parents[1]
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(c, msg):
    if not c: raise RuntimeError(msg)
def pin(f):
    b=f.read_bytes()
    return {'file':str(f.relative_to(P)), 'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
snapshot = json.loads((A/'actual_operations/blocked_audit_PR95_native_snapshot/stdout.bin').read_text())
require(snapshot['head_sha']=='6534ad01e519c719628a18984b108e73cf2e8ead' and snapshot['state']=='open' and snapshot['draft'] and snapshot['merged_at'] is None, 'PR state changed; do not block from stale source')
argv=['git','show',snapshot['head_sha']+':unsolved_math_prioritization/QUEUE.md']
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
q=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=q.communicate()
require(q.returncode==0,'QUEUE read failed: '+err.decode('utf-8','replace'))
rows=[r for r in out.decode().splitlines() if '10400120' in r]
require(len(rows)==1 and 'claimed_solved' in rows[0], 'literal claimed_solved row changed')
prior=json.loads((A/'ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json').read_text())
disp=json.loads((A/'ROOT_PRIORITY_DISPOSITION_20261005.json').read_text())
require(prior['goal_blocked_audit']['consecutive_goal_turns_retaining_this_condition']==2,'turn count not established')
require(prior['bounded_followups_complete'] and not prior['priority_clearance'] and not prior['publication_clearance'],'priority state changed')
require(disp['mathematical_result_verified'] and not disp['priority_requirement_complete'] and not disp['may_advance_to_next_PR_now'],'gate changed')
for f in ['priority_later_version_followup_20261005/CLOSURE.json','priority_thesis_repository_followup_20261005/CLOSURE.json']:
    closed=json.loads((A/f).read_text())
    require(closed.get('closed',closed.get('bounded_audit_complete')) is True and not closed['priority_clearance'],'bounded source work not terminal')
actual=json.loads((A/'actual_operations/checkpoint_priority_followup/execution.json').read_text())
require(actual['exit_code']==0,'previous checkpoint did not finish')
for stream in ['stdout','stderr']:
    b=(A/'actual_operations/checkpoint_priority_followup'/actual[stream]['path']).read_bytes()
    require(len(b)==actual[stream]['bytes'] and hashlib.sha256(b).hexdigest()==actual[stream]['sha256'],'previous actual capture mismatch')
receipt=json.loads((A/'actual_checkpoints/closed_priority_followup/RECEIPT.json').read_text())
require(receipt['commit']=='5008d0b3d1f4e96d747ca395611450651cef0e0f' and receipt['remote_verified'],'previous authoritative push missing')
record={'schema':'PR95-persistent-goal-blocked-audit/v1','UTC':utc,'actual_operator_PID':os.getpid(),'PR':95,'source_head':snapshot['head_sha'],'native_current_snapshot':snapshot,'previous_goal_turn_classification':'progress','previous_goal_turn_evidence':'Independent later-version/adversarial and thesis/archive trails closed; new findings and exact custody records pushed as 5008d0b3d1f4e96d747ca395611450651cef0e0f.','consecutive_goal_turns_with_same_blocking_condition':3,'same_condition':'Priority clearance cannot be established without the complete, directly relevant Kuriya GP preprint or new primary evidence of its exact scope.','mathematics_verified':True,'priority_requirement_complete':False,'publication_clearance':False,'safe_ordered_advance_available':False,'all_current_bounded_source_families_closed':True,'current_agent_status_observation':'Actual collaboration.list_agents returned completed states for the later-version family and its fresh source adversary on this turn; no live source process or session is being awaited.','new_local_source_check':'Scoped Downloads filename search found no Kuriya/GP/LMO/lens-space paper; irrelevant substring hits discarded. This is not a full filesystem or content absence claim.','source_question_already_pending':True,'outreach_prepared_or_initiated':False,'publication_exception_applied':False,'PR50_exception_not_extended':True,'reason_no_further_safe_progress':'Further repetition of exhausted source routes supplies no new evidence. A novel-resolution paper, upload, merge or advance would bypass the unresolved priority requirement; the verified mathematics does not justify closing the PR as invalid.','needed_external_change':'Legitimate full text of Kuriya, The LMO invariant and the Guadagnini–Pilo conjecture for lens spaces (2003), or materially new primary theorem/hypothesis evidence resolving its finite-level ordinary SU(5) relevance.','blocked_audit_passed':True,'persistent_goal_status_update_pending':True,'PR95_workflow_estimate_percent':45,'mathematical_audit_percent':100,'priority_workflow_estimate_percent':85,'program_completed_dispositions':12,'dated_eligible_total':99,'program_workflow_estimate_percent':12/99*100,'new_central_proof_search_turns':0,'queue_read_actual':{'argv':argv,'child_PID':q.pid,'UTC_start':started,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':q.returncode,'full_stdout_bytes':len(out),'full_stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest(),'selected_row':rows[0]},'administrative_locator_failure':'Initial root QUEUE.md Git lookup failed because the file lives in unsolved_math_prioritization/QUEUE.md; tree locator and the actual successful read above corrected this without source modification.','inputs':[pin(A/f) for f in ['ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json','ROOT_PRIORITY_DISPOSITION_20261005.json','actual_checkpoints/closed_priority_followup/RECEIPT.json','actual_operations/checkpoint_priority_followup/execution.json','actual_operations/blocked_audit_PR95_native_snapshot/execution.json','actual_operations/blocked_audit_PR95_native_snapshot/stdout.bin']]}
(A/'ROOT_PERSISTENT_GOAL_BLOCKED_AUDIT_20261005.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['UTC','actual_operator_PID','PR','source_head','previous_goal_turn_classification','consecutive_goal_turns_with_same_blocking_condition','blocked_audit_passed','persistent_goal_status_update_pending']}))

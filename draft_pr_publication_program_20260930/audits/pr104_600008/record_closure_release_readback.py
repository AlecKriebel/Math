from pathlib import Path
import datetime,json,os
A=Path(__file__).resolve().parent;P=A.parents[1]
receipt=json.loads((A/'actual_checkpoints/closure_completion_release/RECEIPT.json').read_text())
operation=json.loads((A/'actual_operations/completion_metadata_release/execution.json').read_text())
if operation['exit_code']!=0 or operation['child_PID']!=receipt['actual_operator_PID'] or not receipt['remote_verified']:raise RuntimeError('Actual release not verified')
t=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'schema':'pr104-actual-closure-release-readback/v1','UTC':t,'operator_PID':os.getpid(),'PR':104,
 'commit':receipt['commit'],'parent':receipt['parent'],'actual_checkpoint_child_PID':operation['child_PID'],'exit_code':0,
 'remote_verified':True,'selected_files':len(receipt['pins']),'changed_paths':len(receipt['changed_paths']),
 'same_head_closed_without_merge':True,'native_already_solved_analytic_disposition_verified':True,'original_budget':'1/5',
 'extra_central_proof_search_turns':0,'DOI':None,'paper_unpublished':True,'human_PR104_disposition_resolved':True,
 'next_numeric_cursor':105,'workflow_percent':100,'program_completion_percent':15/99*100,'persistent_goal_complete':False,
 'late_receipt_pending_next_scoped_checkpoint':True}
with (A/'ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
p=P/'CURRENT_PROGRESS.json';progress=json.loads(p.read_text())
if progress['last_completed_PR']!=104 or progress['fully_completed_count']!=15:raise RuntimeError('Cursor/count changed')
progress.update(UTC=t,updated_UTC=t,last_completed_audit_checkpoint_push_pending=False,
 current_closure_release_checkpoint=receipt['commit'],current_closure_release_checkpoint_remote_verified=True,
 last_completed_metadata_checkpoint_commit=receipt['commit'],last_completed_final_completion_readback='audits/pr104_600008/ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json',
 completion_metadata_checkpoint_pending_at_snapshot=False,advance_to_next_PR_authorized_now=True,
 remaining_current_step='PR104 closure/native disposition and main release complete; fresh ordered intake after104.',
 next_step='Inspect draft-head literal status from105; process only claimed_solved.')
p.write_text(json.dumps(progress,indent=2)+'\n')
line=t+' — Actual PR104 completion checkpoint '+receipt['commit']+' pushed/read back as a strict child of '+receipt['parent']+'; source-bound already_solved analytic status and original1/5 preserved, same-head PR CLOSED/unmerged and exact comment readback. PR104workflow100%; program15/99=15.15%; goal active/incomplete. Next numeric intake105. Late receipts join the next scoped checkpoint.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+line)
print(json.dumps(result))

"""Save the actual completed release without a recursive self-commit claim."""
from pathlib import Path
import datetime,json,os
A=Path(__file__).resolve().parent
P=A.parents[1]
receipt=json.loads((A/'actual_checkpoints/closure_release/RECEIPT.json').read_text())
operation=json.loads((A/'actual_operations/checkpoint_pr97_closure_release/execution.json').read_text())
if operation['exit_code']!=0 or operation['child_PID']!=receipt['actual_operator_PID'] or not receipt['remote_verified']:
    raise RuntimeError('Actual release not verified')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'schema':'pr97-actual-closure-release-readback/v1','UTC':now,'operator_PID':os.getpid(),
        'PR':97,'commit':receipt['commit'],'parent':receipt['parent'],
        'actual_checkpoint_child_PID':operation['child_PID'],'exit_code':operation['exit_code'],
        'remote_verified':True,'selected_files':len(receipt['pins']),'changed_paths':len(receipt['changed_paths']),
        'same_head_closed_without_merge':True,'paper_unpublished':True,'DOI':None,
        'human_PR97_disposition_resolved':True,'next_numeric_cursor':98,
        'workflow_percent':100,'program_completion_percent':14/99*100,
        'late_receipt_pending_next_scoped_checkpoint':True}
with (A/'ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json').open('x') as stream:
    stream.write(json.dumps(result,indent=2)+'\n')
progress_path=P/'CURRENT_PROGRESS.json'
progress=json.loads(progress_path.read_text())
if progress['last_completed_PR']!=97:raise RuntimeError('Cursor changed')
progress.update({'UTC':now,'updated_UTC':now,'last_completed_audit_checkpoint_push_pending':False,
                 'current_closure_release_checkpoint':receipt['commit'],
                 'current_closure_release_checkpoint_remote_verified':True,
                 'last_completed_metadata_checkpoint_commit':receipt['commit'],
                 'last_completed_final_completion_readback':'audits/pr97_10300055/ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json',
                 'remaining_current_step':'PR97 closure and release complete; next ordered intake after97 on resumption.'})
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### '+now+' — closure release pushed and verified\n'
                 'Actual checkpoint91793exit0 committed'+str(len(receipt['changed_paths']))+' selected regular artifacts at'+receipt['commit']+', pushed and read back remote main as a strict child of'+receipt['parent']+'. Fresh GitHub readback again confirms PR97 CLOSED at original fb50facb, mergedAt null. All findings preserved; no publication, tracker update or global historical-status rewrite. The human disposition is resolved. Late actual checkpoint/readback metadata join the next scoped checkpoint without a recursive self-commit claim. PR97workflow100%;14/99=14.14%; next numeric intake98 on goal resumption.\n')
print(json.dumps(result))

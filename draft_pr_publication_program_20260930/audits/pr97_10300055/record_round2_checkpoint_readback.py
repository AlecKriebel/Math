"""Record completed audit checkpoint and the pending human disposition."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent
P=A.parents[1]
C=P.parent
receipt=json.loads((A/'actual_checkpoints/round2_adjudication_retry/RECEIPT.json').read_text())
operation=json.loads((A/'actual_operations/checkpoint_round2_adjudication_retry/execution.json').read_text())
if operation['exit_code'] != 0 or operation['child_PID'] != receipt['actual_operator_PID'] or not receipt['remote_verified']:
    raise RuntimeError('Actual checkpoint mismatch')
commit='250d2043167ac97adedef188edd3aa7a1e938f85'
if receipt['commit'] != commit or receipt['parent'] != '1f86990dcae793167b35c1cfff2e310758404886':
    raise RuntimeError('Checkpoint identity mismatch')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'schema':'pr97-round2-checkpoint-actual-readback/v1','UTC':now,'operator_PID':os.getpid(),
        'checkpoint':commit,'parent':receipt['parent'],'actual_child_PID':operation['child_PID'],
        'exit_code':operation['exit_code'],'selected_regular_files':len(receipt['pins']),
        'changed_paths':len(receipt['changed_paths']),'remote_verified_by_actual_checkpoint':True,
        'checkpoint_receipt_sha256':hashlib.sha256((A/'actual_checkpoints/round2_adjudication_retry/RECEIPT.json').read_bytes()).hexdigest(),
        'failed_pre_staging_checkpoint_and_reconciliation_preserved':True,
        'qualified_unpublished_package_accepted':True,'priority_clearance':False,
        'PR97_specific_disposition_requested':True,'human_answer_received':False,
        'question_choices':['Publish credited priority-unresolved note, merge and continue',
                            'Merge verified finding without paper and continue',
                            'Keep PR97 open for further priority evidence'],
        'reason':'Original novel-resolution publication requirement not satisfied by known construction and bounded unresolved priority.',
        'publication_authorization':False,'DOI':None,'native_acceptance':False,
        'workflow_estimate_percent':60,'program_completion_percent':13/99*100,
        'original_author_effort':'2/5','new_central_proof_search_turns':0,
        'late_record_pending_next_scoped_checkpoint':True}
with (A/'ROOT_ROUND2_CHECKPOINT_ACTUAL_READBACK_20261006.json').open('x') as stream:
    stream.write(json.dumps(result,indent=2)+'\n')
progress_path=P/'CURRENT_PROGRESS.json'
progress=json.loads(progress_path.read_text())
if progress['current_PR'] != 97 or progress['current_publication_authorization']:
    raise RuntimeError('Program disposition changed')
progress.update({'UTC':now,'updated_UTC':now,'current_human_disposition_question_pending':True,
                 'current_latest_completed_audit_checkpoint':commit,
                 'current_latest_completed_audit_checkpoint_remote_verified':True})
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### '+now+' — audit checkpoint verified; concrete disposition requested\n'
                 'Actual checkpoint63708exit0 committed406 selected regular bodies at250d2043, a strict child of concurrent1f86990d, pushed and verified remote main with empty isolated index. Both the stopped pre-staging attempt and actual reconciliation are included. The exact four-page qualified note was presented to the human, with a PR97-specific choice to publish with unresolved priority, accept without a paper, or hold for sources. Async question delivery was accepted; no answer or publication authorization is inferred. No Zenodo service/tracker/PR merge/native acceptance performed. This late readback and pending-question metadata join the next scoped checkpoint. PR97workflow60%; program13/99=13.13%; original2/5, extra proof-search0.\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'checkpoint':commit,
                  'human_disposition_pending':True,'publication_authorized':False}))

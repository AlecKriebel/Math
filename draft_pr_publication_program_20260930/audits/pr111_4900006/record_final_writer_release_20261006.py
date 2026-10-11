from pathlib import Path
import datetime,json,os
A=Path(__file__).resolve().parent
final=json.loads((A/'actual_final_completion_readback_20261006/RECEIPT.json').read_text())
if not final['actual_remote_main_verified'] or not final['index_empty_and_materialized_tracked_changes_empty']:raise ValueError('Actual final readback incomplete')
record={**final,'schema':'pr111-final-completion-writer-release/v1',
    'recorded_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_release_recorder_PID':os.getpid(),
    'release_message_destination':'01a0ff30-7e80-7053-abb4-4a9c45f2fd62',
    'actual_release_API_isError':False,'actual_release_API_returned_thread_id':'01a0ff30-7e80-7053-abb4-4a9c45f2fd62',
    'actual_release_API_accepted':True,'writer_release_pending':False,'writer_ownership_released':True,
    'completion_metadata_checkpoint_pending':False,'next_ordered_status_only_intake_authorized_now':True,
    'human_question_pending':False,'late_release_record_joins_next_checkpoint_without_self_commit_claim':True,
    'current_progress_committed_fields_are_pre_release_snapshot':True}
(A/'FINAL_COMPLETION_OWNER_RELEASE_20261006.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in {'status_scope'}},sort_keys=True))

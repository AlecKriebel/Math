"""Record observed API delivery after final readback; no self-commit claim."""
from pathlib import Path
import datetime, json, os, sys
A=Path(__file__).resolve().parent
readback=json.loads((A/'actual_final_completion_readback_20261006/RECEIPT.json').read_text())
response=json.loads(Path(sys.argv[1]).read_text())
if response.get('isError') is not False:raise ValueError('Actual release API not accepted')
text_blocks=[x['text'] for x in response.get('content',[]) if x.get('type')=='text']
delivery=json.loads(text_blocks[0])
if delivery.get('threadId')!='01a0ff30-7e80-7053-abb4-4a9c45f2fd62':raise ValueError('Wrong actual delivery thread')
out=A/'FINAL_COMPLETION_OWNER_RELEASE_20261006.json'
if out.exists():raise ValueError('Existing final release receipt')
record={**readback,'schema':'pr124-final-completion-writer-release/v1',
 'recorded_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_release_recorder_PID':os.getpid(),
 'actual_release_API_accepted':True,'actual_release_API_isError':False,
 'actual_release_API_returned_thread_id':delivery['threadId'],'writer_ownership_released':True,'writer_release_pending':False,
 'next_ordered_status_only_intake_authorized_now':True,'late_release_record_joins_next_checkpoint_without_self_commit_claim':True,
 'current_progress_committed_fields_are_pre_release_snapshot':True,'human_question_pending':False}
out.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps(record,sort_keys=True))

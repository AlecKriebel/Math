from pathlib import Path
import json,datetime,os
A=Path(__file__).resolve().parent
r=json.loads((A/'ACTUAL_INTAKE_RELEASE_API_RESPONSE_20261006.json').read_text())
q=json.loads((A/'actual_intake_root_checkpoint_20261006/RECEIPT.json').read_text())
if r.get('isError') is not False:raise RuntimeError('Actual API failed')
dest=json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))['threadId']
if dest!='01a0ff30-7e80-7053-abb4-4a9c45f2fd62':raise RuntimeError('Wrong destination')
if not q['all_changed_bodies_verified_in_index_commit_and_fetched_main']:raise RuntimeError('Readback gate')
out=A/'ACTUAL_INTAKE_WRITER_RELEASE_20261006.json'
if out.exists():raise RuntimeError('Already recorded')
record={'schema':'pr124-actual-intake-writer-release/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_recorder_PID':os.getpid(),'checkpoint_commit':q['commit'],'changed_body_count':q['changed_count'],'all_changed_bodies_verified_in_index_commit_and_fetched_main':True,'API_accepted':True,'API_isError':False,'returned_thread_id':dest,'writer_ownership_released':True,'writer_release_pending':False,'goal_active':True,'program_completed':20,'published':11,'current_PR':124,'native_PR_Zenodo_Sheet_mutations':False,'late_receipt_joins_next_checkpoint_without_self_commit_claim':True}
out.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');print(json.dumps(record))


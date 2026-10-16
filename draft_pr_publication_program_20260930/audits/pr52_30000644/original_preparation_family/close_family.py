"""ROOT-only SOURCE: execute only after complete personal read and preparer exit."""
import argparse,datetime,json,os,sys
from pathlib import Path
from closure_common import F,MF,digest,identity,inspect
p=argparse.ArgumentParser();p.add_argument('--expected-index-sha256',required=True);p.add_argument('--expected-ready-sha256',required=True);p.add_argument('--after-preparer-exit',action='store_true',required=True);a=p.parse_args()
assert a.after_preparer_exit and not MF.exists()
r=inspect(a.expected_index_sha256,a.expected_ready_sha256,False)
manifest={'schema':'pr52-original-source-self-closure/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closure_operator_pid':os.getpid(),'closure_operator_argv':sys.argv,'closure_operator_source':identity(Path(__file__).resolve()),'caller_supplied_after_preparer_exit':True,'closure_payload_verified':True,'process_completion_and_exit_must_be_captured_externally_after_return':True,'claimed_process_exit_code':None,'index_sha256':a.expected_index_sha256,'ready_sha256':a.expected_ready_sha256,'file_bindings':sorted(r['file_bindings'],key=lambda x:x['path']),'directories':r['directories'],'fixed_external_rows_checked':r['fixed_external_rows_checked'],'dated_mutable_rows_not_future_authority':r['dated_mutable_rows_not_future_authority'],'dated_derived_cache_rows_not_future_authority':r['dated_derived_cache_rows_not_future_authority'],'root_personal_read_attestation':False,'native_acceptance_authority':False,'remote_action_authority':False,'independent_new_mathematical_verdict':False,'merged':False,'preprint_created':False,'doi_created':False}
with MF.open('xb') as f:f.write((json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
MF.chmod(0o444);inspect(a.expected_index_sha256,a.expected_ready_sha256,True)
print(json.dumps({'status':'CLOSED_SOURCE_PREPARATION_ONLY','manifest_sha256':digest(MF.read_bytes()),'files_with_manifest':len(r['file_bindings'])+1,'native_and_remote_authority':False},sort_keys=True))

"""ROOT-only SOURCE: read closed preparation without writing any file."""
import argparse,json
from closure_common import F,MF,digest,identity,inspect,read_json
p=argparse.ArgumentParser();p.add_argument('--expected-index-sha256',required=True);p.add_argument('--expected-ready-sha256',required=True);p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args()
assert MF.exists() and digest(MF.read_bytes())==a.expected_manifest_sha256 and identity(MF)['mode']==0o444
r=inspect(a.expected_index_sha256,a.expected_ready_sha256,True);m=read_json(MF)
assert m['schema']=='pr52-original-source-self-closure/v1' and m['index_sha256']==a.expected_index_sha256 and m['ready_sha256']==a.expected_ready_sha256 and m['closure_payload_verified'] is True
assert m['file_bindings']==sorted(r['file_bindings'],key=lambda x:x['path']) and m['directories']==r['directories']
assert type(m['closure_operator_pid']) is int and m['closure_operator_pid']>0 and m['claimed_process_exit_code'] is None and m['process_completion_and_exit_must_be_captured_externally_after_return'] is True
assert m['closure_operator_source']==identity(F/'close_family.py')
assert all(m[k] is False for k in ['root_personal_read_attestation','native_acceptance_authority','remote_action_authority','independent_new_mathematical_verdict','merged','preprint_created','doi_created'])
print(json.dumps({'status':'READ_ONLY_CLOSED_SOURCE_PREPARATION_PASS','files_with_manifest':len(r['file_bindings'])+1,'manifest_sha256':a.expected_manifest_sha256,'fixed_external_rows_checked':r['fixed_external_rows_checked'],'dated_mutable_and_derived_rows_no_future_authority':r['dated_mutable_rows_not_future_authority']+r['dated_derived_cache_rows_not_future_authority'],'root_or_production_approval':False},sort_keys=True))

"""Own administrative report/READY author; no proposed rollback or ROOT closer import."""
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
if not __debug__: raise RuntimeError('Optimized Python refused')
H=Path(__file__).resolve().parent; A=H.parent; R=A.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def row(p,base=H):
    need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Regular bound source')
    b=p.read_bytes(); return {'path':p.relative_to(base).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def put(name,value):
    with (H/name).open('xb') as f:f.write((json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
need(not (H/'SELF_MANIFEST.json').exists() and not (H/'READY.json').exists(),'Absent final own outputs')
source=json.loads((H/'SOURCE_V2_CHECK.json').read_bytes())
need(source['status']=='PASS_READ_AST_AND_EXACT_QUEUE_SCOPE_CHECKS' and source['F1_F1a_F2_repair_personally_read'] is True,'Genuine final own control')
for p in H.rglob('*.py'): ast.parse(p.read_bytes())
verdict={'schema':'pr48-independent-selected-partial-rollback-SOURCE-verdict/v1','status':'PASS_SOURCE_REPAIR_VERIFIED_NO_REMAINING_MANDATORY_DEFECT','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_own_verdict_writer_pid':os.getpid(),'independence':'Initial mechanism and exact-footprint approach recorded before candidate or another reviewer verdict access; all original scope reconstructed personally','reviewed_corrected_SOURCE':source['received_SOURCE'],'reviewed_corrected_helper':source['received_helper'],'reviewed_corrected_plan':source['received_plan'],'actual_final_own_read_AST_capture':row(H/'actual_source_v2_capture/CAPTURE.json'),'actual_final_own_read_AST_result':row(H/'SOURCE_V2_CHECK.json'),'actual_final_own_inspector_pid':32685,'first_received_SOURCE_sha256':'595d61469762348ee143d1ed4ac3792439cc8bcd70271dacc3e324361e45ed28','mandatory_findings':[{'id':'F1','status':'REPAIRED','issue':'Persist full actual entry command evidence on pre-quarantine failures'},{'id':'F1a','status':'REPAIRED_AS_PART_OF_F1','issue':'Record raw-reversible stream bytes before strict interpretation'},{'id':'F2','status':'REPAIRED','issue':'Retain native-critical result before release and retain result on release/publication failure'}],'remaining_mandatory_findings':[],'fixed_current_mutation_footprint_count':11,'ADMIN_exact_original_blob_restoration_count':4,'inventory_exact_restoration_count':1,'quarantined_then_removed_new_receipts_count':6,'complete_canonical_preimage_count':1958,'complete_canonical_after_count':1955,'other_science_bodies_retained_count':1951,'other_science_full_mode_retained':0o444,'ADMIN_full_mode_deliberately_restored':0o644,'historical_all_modes_restored_claimed':False,'complete_outside_runtime_baseline_observed_inside_owned_lock':True,'fixed_current_QUEUE_refresh_exact_unrelated_status_delta_verified':True,'outside_mathematical_claims_accepted':False,'coordination_lock_Git_metadata_mutation_planned':True,'Git_index_body_ref_staging_mutation_planned':False,'proposed_helper_import_execution_or_runtime_simulation_by_reviewer':False,'native_Git_or_remote_mutation_by_reviewer':False,'ROOT_execution_approval_claimed':False,'actual_rollback_success_claimed':False,'V7_retry_authorized':False,'mathematical_review_credit':0,'acceptance_credit':0,'source_review_percent':100,'actual_recovery_percent':0,'limitations':['Static code/custody review and genuine own read-only/AST controls; no production or simulated rollback execution','Ordinary Git cooperation with index.lock assumed; source explicitly disclaims hostile atomic-unlink immunity','Storage errors can prevent evidence writes; absent files are not certified as retained','ROOT must personally read exact corrected SOURCE and inspect actual capture/receipt plus separate readback before later V7 work']}
put('VERDICT.json',verdict)
external=[]
for folder in [A/'partial_finalize_v6_rollback_preparation',A/'concurrent_finalize_failure_analysis/rollback_READY_candidate_v1_history',A/'concurrent_finalize_failure_analysis/source_binding_repaired_final_actual_capture',A/'concurrent_finalize_failure_analysis/source_binding_repaired_actual_capture']:
    for p in folder.rglob('*'):
        if p.is_file():external.append(row(p,R))
files=[]; dirs=[]
for p in H.rglob('*'):
    need(not p.is_symlink(),'No own source symlink')
    if p.is_file(): files.append(row(p))
    else:
        need(p.is_dir(),'No source special member'); dirs.append({'path':p.relative_to(H).as_posix(),'full_mode':stat.S_IMODE(p.stat().st_mode)})
files=sorted(files,key=lambda z:z['path']); dirs=sorted(dirs,key=lambda z:z['path'])
need(all(z['full_mode']==0o644 for z in files) and stat.S_IMODE(H.stat().st_mode)==0o755,'Prepared full source modes')
ready={'schema':'pr48-independent-selected-partial-rollback-review-SOURCE-ready/v1','status':'READY_SOURCE_REVIEW_ONLY_FOR_ROOT_CUSTODY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_own_READY_writer_pid':os.getpid(),'self_excluded':['READY.json'],'prepared_files_count_including_READY':len(files)+1,'files':files,'directories':dirs,'source_only':True,'ROOT_execution_approval_claimed':False,'ROOT_manifest_present':False,'future_ROOT_manifest':'SELF_MANIFEST.json','ROOT_only_closure_and_separate_readback_imported_or_executed':False,'ROOT_only_helper_AST_checked':True,'proposed_rollback_import_or_execution':False,'math_review_credit':0,'source_review_percent':100,'actual_recovery_percent':0,'external_received_SOURCE_and_history_bindings':sorted(external,key=lambda z:z['path']),'external_binding_role':'Fixed received source/historical evidence; no native runtime authority or foreign math acceptance','verdict':row(H/'VERDICT.json'),'closed_future_manifest_schema':'pr48-independent-rollback-SOURCE-review-closure/v1'}
put('READY.json',ready)
print(json.dumps({'status':ready['status'],'actual_writer_pid':os.getpid(),'utc':ready['utc'],'prepared_files_count':len(files)+1,'directories_count':len(dirs),'prepared_payload_bytes_excluding_READY':sum(z['bytes'] for z in files),'READY':row(H/'READY.json'),'VERDICT':row(H/'VERDICT.json'),'future_ROOT_manifest_absent':not (H/'SELF_MANIFEST.json').exists()}))

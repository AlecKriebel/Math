from pathlib import Path
import datetime, hashlib, json, os, stat
O=Path(__file__).resolve().parent
A=O.parent
C=O.parents[3]
D=A/'native_publication_integration_plan_20261006/corrected_v5'
Q=D/'candidate_dfe3e71993e3bd99'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def require(v,s):
 if not v:raise RuntimeError(s)
def write(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
require(not (O/'SEAL_RECEIPT.json').exists(),'already sealed')
normal=read(O/'normal_RECEIPT.json');optimized=read(O/'optimized_RECEIPT.json')
ne=read(O/'execution_normal_v5/execution.json');oe=read(O/'execution_optimized/execution.json')
require(ne['actual_child_PID']==normal['actual_operator_PID']==70473 and oe['actual_child_PID']==optimized['actual_operator_PID']==70935,'actual audit PID custody')
require(ne['exit_code']==oe['exit_code']==0 and ne['child_reaped'] is oe['child_reaped'] is True,'actual audit exit/reap')
require(normal['check_count']==optimized['check_count']==52385 and normal['checks_by_group']==optimized['checks_by_group'],'normal/optimized checks')
require(normal['negative_controls']==optimized['negative_controls'] and len(normal['negative_controls'])==13,'normal/optimized mutation controls')
require(normal['python_optimized'] is False and optimized['python_optimized'] is True,'actual optimization flags')
require(ne['source']==oe['source'] and ne['source']['sha256']==digest(O/'audit_actual_candidate.py'),'identical final source')
require(read(O/'normal_READ_PINS.json')==read(O/'optimized_READ_PINS.json'),'identical final concrete read pins')
for execution,folder in [(ne,'execution_normal_v5'),(oe,'execution_optimized')]:
 for name in ['stdout','stderr']:
  p=O/folder/execution[name]['path'];require(p.stat().st_size==execution[name]['bytes'] and digest(p)==execution[name]['sha256'],'retained actual audit stream')
 require(execution['stderr']['bytes']==0,'successful stderr empty')
for folder,source in [('execution_normal','audit_predicate_v2_before_hold_tally_correction.py'),('execution_normal_v3','audit_predicate_v3_before_README_wrapper_correction.py'),('execution_normal_v4','audit_predicate_v4_before_absolute_path_correction.py')]:
 x=read(O/folder/'execution.json');require(x['exit_code']==1 and x['source']['sha256']==digest(O/source),'failed reviewer predicate source custody')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n'+now+': Sealed independent actual-candidate review checkpoint, actual sealer PID '+str(os.getpid())+'. Review completion 100%; required and optional findings empty. Parent exact export/readbacks and merge remain outstanding.\n')
proposal=A/'ROOT_PROPOSED_NATIVE_EXPORT_PLAN_20261006.json'
verdict={'schema':'pr108-independent-actual-native-candidate-adversary/v1','UTC':now,'actual_sealer_PID':os.getpid(),'review_completion_percent':100,'required_findings':[],'optional_findings':[],'actual_candidate_data_and_execution_custody_review_clean':True,'exact_proposed_public_export_273_offers_plus_one_note_review_clean':True,'parent_may_export_reviewed_exact_bodies_after_immediate_unchanged_head_input_capacity_checks':True,'actual_export_acceptance_or_merge_complete':False,'actual_export_readback_and_merge_parents_tree_GitHub_status_still_required':True,'candidate_receipt_sha256':digest(Q/'CANDIDATE_RECEIPT.json'),'actual_config_sha256':digest(Q/'CONFIG.json'),'execution_inputs_sha256':normal['execution_inputs_sha256'],'main_parent':normal['main_parent'],'proposed_export_plan_sha256':digest(proposal),'operational_exclusions_note_sha256':digest(A/'PROPOSED_PUBLIC_NATIVE_OPERATIONAL_EXCLUSIONS_20261006.json'),'normal_actual_PID':70473,'optimized_actual_PID':70935,'independent_checks_per_mode':52385,'independent_negative_controls_per_mode':13,'concrete_read_pins_per_mode':631,'all_private_offers_verified':275,'proposed_public_offers':273,'added_public_metadata_only_note':1,'private_Sheet_body_export_exclusions':2,'nongate_captured_input_count':180,'unrelated_complete_catalog_rows':15457,'unrelated_physical_CSV_records':15457,'unrelated_state_and_assessment_maps_preserved':True,'ledger_exact_prefix_plus_one_target_event_each':True,'independently_derived_stale_projection_differences_preserved':48,'original_historical_files_preserved':15,'current_exact_effective_diagnostic_artifacts':9,'current_README_reviewed_wrapper_and_original_diagnostic_README_preserved':True,'published_logical_files_preserved':46,'published_support_ZIP_members_verified':47,'actual_outer_helper_PID':62139,'actual_native_worker_PID':62294,'actual_bounded_child_processes_verified':40,'worker_applied_CPU_soft_hard':[90,90],'worker_applied_FSIZE_soft_hard':[33554432,33554432],'worker_applied_NOFILE_soft_hard':[32,32],'Darwin_hard_memory_bound_claimed':False,'original_status':'claimed_solved','original_budget':'2/5','original_structured_ledger_present':False,'imported_prior_report_exact_empty_object':True,'new_central_proof_search_turns':0,'math_priority_paper_publication_tracker_source_review_repeated':False,'native_prepare_assess_SQL_queries_resource_application_service_calls_Git_mutations_export_install_commit_merge_by_auditor':0,'independent_readonly_Git_processes_per_mode':6,'all_writes_confined_to_new_review_folder':True,'private_runtime_configuration_or_credential_bodies_disclosed_or_copied':False,'new_subagents_spawned':0,'human_contact_or_outreach_prepared_or_made':False,'reviewer_predicate_corrections_and_failed_runs_preserved':True,'remaining_gap':'Root performs exact scoped export, exported-body readbacks, scoped main acceptance and remote confirmation, reviewed main-only merge, exact two-parent/tree checks and actual GitHub MERGED readback.'}
write(O/'VERDICT.json',verdict)
files=[]
for p in sorted(O.rglob('*')):
 require(not p.is_symlink(),'symlink in review output')
 if p.is_file() and p.name not in ['OUTPUT_MANIFEST.json','SEAL_RECEIPT.json']:
  files.append({'relative_path':p.relative_to(O).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')})
manifest={'schema':'pr108-independent-actual-candidate-review-output/v1','UTC':now,'actual_sealer_PID':os.getpid(),'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files),'files':files}
write(O/'OUTPUT_MANIFEST.json',manifest)
seal={'schema':'pr108-independent-actual-candidate-review-seal/v1','UTC':now,'actual_sealer_PID':os.getpid(),'sealed':True,'manifested_file_count':len(files),'allfiles_including_manifest_and_seal':len(files)+2,'manifested_bytes':sum(x['bytes'] for x in files),'output_manifest_sha256':digest(O/'OUTPUT_MANIFEST.json'),'REPORT_sha256':digest(O/'REPORT.md'),'VERDICT_sha256':digest(O/'VERDICT.json'),'execution_inputs_sha256':normal['execution_inputs_sha256'],'normal_actual_PID':70473,'optimized_actual_PID':70935,'required_findings':[],'optional_findings':[],'candidate_and_exact_export_proposal_review_completion_percent':100,'actual_export_acceptance_or_merge_claimed_complete':False}
write(O/'SEAL_RECEIPT.json',seal)
print(json.dumps(seal,indent=2))

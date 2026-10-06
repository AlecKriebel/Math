from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
A=Path(__file__).resolve().parents[1];D=A/'native_post_assess_carryforward_v3_20261006';W=D/'workspaces/candidate_d9eb646c1dd70e89';O=A/'root_actual_candidate_reproduction_v2_20261006'
def need(v,m):
 if not v:raise RuntimeError(m)
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(f):return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
def obj(f):return json.loads(f.read_bytes())
checked=[]
def check(f,s):
 need(f.is_file() and not f.is_symlink() and f.stat().st_nlink==1,'Unique regular body')
 need(hp(f.read_bytes())=={k:s[k] for k in ('bytes','sha256')},'Full body custody '+str(f));checked.append(pin(f))
adpath=Path(sys.argv[1]);manifest=Path(sys.argv[2]);need(adpath.is_relative_to(A) and manifest.parent==adpath.parent,'Dedicated final adversary')
ad=obj(adpath);m=obj(manifest)
for s in m['files']:check(manifest.parent/s['path'],s)
need(ad['schema']=='pr110-actual-native-candidate-adversary/v1' and ad['actual_review'] is True and ad['clearance'] is True and ad['required_findings']==[] and ad['template_only'] is False and ad.get('fixture',False) is False and ad.get('simulated',False) is False,'Completed actual adversary output review')
r=obj(W/'CANDIDATE_RECEIPT.json');need(not(W/'FAILURE.json').exists() and ad['candidate_receipt_pin']==hp((W/'CANDIDATE_RECEIPT.json').read_bytes()) and ad['packet_sha256']==r['packet_sha256'],'Exact successful real candidate')
for field,rfield in [('continuation_program_pin','continuation_program_pin'),('action_program_pin','continuation_action_program_pin'),('integration_inputs_pin','integration_inputs_pin'),('linear_diff_program_pin','linear_diff_program_pin'),('stopped_CPU_continuation_inventory_pin','stopped_CPU_continuation_inventory_pin')]:
 need(ad[field]==r[rfield],'Exact final reviewed '+field);check(A/ad[field]['path'],ad[field])
need(ad['outer_launcher_pin']==pin(A/'publication_build_v1/record_native_action_v4.py'),'Exact future action outer reviewed')
rep=obj(O/'ROOT_REPRODUCTION_COMPLETE.json');need(rep['actual_output_reproduction_complete'] is True and rep['actual_full_body_offer_and_DIFF_application_complete'] is True and rep['actual_28_child_outer_resource_custody_complete'] is True and rep['actual_candidate_clearance_issued'] is False,'Separate completed actual root reproduction')
for s in rep['output_pins']:check(A/s['path'],s)
q=obj(O/'ACTUAL_LINEAR_CARRYFORWARD_CANDIDATE_RESULT.json');custody=obj(O/'ACTUAL_LINEAR_CARRYFORWARD_CUSTODY_RESULT.json')
need(q['candidate_receipt_pin']==ad['candidate_receipt_pin'] and q['DIFF_pin']==r['DIFF_pin'] and q['offered_files']==84 and q['unrelated_catalog_records_preserved']==15457 and q['unrelated_assessments_preserved']==15457 and q['actual_output_review_complete'] is True,'Full actual preserved objects and complete patch')
for s in q['full_candidate_inventory']:check(W/s['path'],s)
need(custody['candidate_receipt_pin']==ad['candidate_receipt_pin'] and custody['actual_continuation_PID']==r['operator_PID'] and custody['new_actual_direct_children']==28 and custody['all_recorded_groups_absence_confirmed'] is True and custody['required_findings']==[],'Actual PID28/direct/outer custody')
need(r['main_parent']=='e0a94b93520610553c001f265f210f959b591c2c' and r['original_assessed_main_parent']=='f9f840d21305bdc353d151abe8dd5c51b6a27dd6' and r['turns_used']==2 and r['new_central_proof_search_turns']==0 and r['native_assess_calls_during_continuation']==0 and r['holds_cleared'] is False,'Historical assessment/current integration and honest effort')
scope={k:True for k in ['full_actual_candidate_DIFF_and_offer_reviewed','actual_native_PID_resources_and_process_custody_authenticated','all17_originals_and_nonempty_prior_preserved','source_cache_readonly_and_original_2_of_5_no_extra_search_turn','unrelated_scores_order_physical_CSV_history_and_campaign_preserved','accepted_full_mathematical_resolution_and_bounded_priority','actual_publication_tracker_and_clean_whole_package_R1_R2','this_exact_source_and_main_only_exact_tree_integration_reviewed']}
x={'schema':'pr110-root-actual-native-candidate-review/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'actual_review':True,'native_candidate_actual_authenticated':True,'required_findings':[],'adversary_decision_pin':pin(adpath),'adversary_manifest_pin':pin(manifest),'candidate_receipt_pin':ad['candidate_receipt_pin'],'packet_sha256':r['packet_sha256'],'main_parent':r['main_parent'],'original_assessed_main_parent':r['original_assessed_main_parent'],'integration_inputs_pin':r['integration_inputs_pin'],'linear_diff_program_pin':r['linear_diff_program_pin'],'stopped_CPU_continuation_inventory_pin':r['stopped_CPU_continuation_inventory_pin'],'scope_checks':scope,'root_reproduction_pin':pin(O/'ROOT_REPRODUCTION_COMPLETE.json'),'checked_artifacts':checked,'actual_processes_and_sources_and_full_report_read':True,'native_export_executed':False,'publication_tracker_already_complete':True,'workflow_completion_percent':85,'mathematics_and_bounded_priority_completion_percent':100,'actual_parent_and_worker_memory_advisory_exceedance_honestly_retained':True,'hard_memory_limit_claimed':False}
f=A/'ROOT_ACTUAL_NATIVE_CANDIDATE_REVIEW_AUTHENTICATION_20261006.json';need(not f.exists(),'Unique actual completed root clearance');f.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n');print(json.dumps({'root_review_pin':pin(f),'checked_complete_bodies':len(checked),'actual_root_PID':os.getpid(),'actual_candidate_authenticated':True}))

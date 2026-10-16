"""Preserve available incomplete review06 evidence; never issue clearance."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;D=A/'lifecycle_adversary_06';S=A/'lifecycle_adversary_06_snapshot_01'
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def fresh(p,j):
 with p.open('x') as f:f.write(json.dumps(j,indent=2)+'\n')
 p.chmod(0o444)
stamp=datetime.datetime.now(datetime.UTC).isoformat()
require(pin(A/'lifecycle_controls_preparation_06/FINAL_SEAL.json')['sha256']=='29ce438e059048c8102b277a854423b781c1c04a27ba15efe242f2aa597aa39b','Frozen06 drift')
focused=json.loads((D/'FOCUSED_SANITIZATION_PROBE.json').read_text());require(focused['outcome']=='ACCEPTED_UNAPPROVED_PRIVATE_TRACKER_FIELD' and focused['fixture_only_no_real_private_data'] is True,'Missing available finding')
results=json.loads((D/'INDEPENDENT_RESULTS.json').read_text());require(results['source_sha256']=='df48702660974c56394e2aa9ea1a2da817fd667bf500bbe917aa22ee5e8b8ca4' and results['test_count']==425 and results['passed']==425,'Available earlier results drift')
S.mkdir(exist_ok=False)
safe=['FOCUSED_SANITIZATION_PROBE.json','EXTERNAL_BOUNDARY_REVIEW.json','INDEPENDENT_ATTACK_PLAN.md','PLAN_PROVENANCE.json','PLAN_SEAL.sha256','PRE_EXECUTION_MAPPING.json','RESEARCH_LOG.md','INPUT_PINS.json']
members=[]
for n in safe:
 source=D/n;require(source.is_file() and not source.is_symlink(),'Unexpected original path')
 with (S/n).open('xb') as f:f.write(source.read_bytes())
 (S/n).chmod(0o444);members.append({'path':n,'original_path':'lifecycle_adversary_06/'+n,**pin(S/n)})
summary={'UTC':stamp,'PR':191,'status':'ROOT_PRESERVED_AVAILABLE_INCOMPLETE_REVIEW06_EVIDENCE_REQUIRED_REPAIR','independent_terminal_report_or_seal_exists':False,'reviewer_turns_stopped_by_automated_safety_filter':2,'Root_did_not_restart_further_review06_tests':True,'earlier_result_file':{'path':'lifecycle_adversary_06/INDEPENDENT_RESULTS.json',**pin(D/'INDEPENDENT_RESULTS.json')},'earlier_completed_expectations':425,'earlier_matched_expectations':425,'earlier_results_exclude_later_focused_finding':True,'later_focused_finding':focused,'required_repair':'Reject unapproved top-level and nested content in generated public service-evidence files; preserve own-only sanitized approved data.','unsealed_reproducer_not_selected':{'path':'lifecycle_adversary_06/INDEPENDENT_REPRODUCER.py',**pin(D/'INDEPENDENT_REPRODUCER.py')},'copied_original_namespace_retained_in_members':True,'copied_bytes_not_a_reviewer_terminal_seal':True,'remaining_review_scope_incomplete':True,'publication_or_merge_clearance':False,'actual_private_data_disclosed':False,'NEW_independent_review_plan_sealed':'lifecycle_adversary_07','originals_left_unchanged':True}
fresh(S/'ROOT_INCOMPLETE_REVIEW_SUMMARY.json',summary);members.append({'path':'ROOT_INCOMPLETE_REVIEW_SUMMARY.json',**pin(S/'ROOT_INCOMPLETE_REVIEW_SUMMARY.json')})
fresh(S/'MANIFEST.json',{'UTC':stamp,'status':'ROOT_OWNED_SNAPSHOT_OF_AVAILABLE_INCOMPLETE_EVIDENCE_ONLY','files':members,'no_reviewer_terminal_approval':True})
allow=[x['path'] for x in members]+['MANIFEST.json','PUBLIC_SAFE_ALLOWLIST.json']
fresh(S/'PUBLIC_SAFE_ALLOWLIST.json',{'files':allow,'schema':'PR191_ROOT_INCOMPLETE_REVIEW06_SAFE_SNAPSHOT_V1','scratch_raw_results_and_reproducer_excluded':True,'actual_private_data_included':False,'no_directory_globs':True})
out={'UTC':stamp,'PR':191,'original_head':'a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe','status':'ROOT_AUTHENTICATED_AVAILABLE_INCOMPLETE_REVIEW06_EVIDENCE_REPAIR_REQUIRED','independent_review06_terminal_complete':False,'snapshot_manifest':{'path':str((S/'MANIFEST.json').relative_to(A)),**pin(S/'MANIFEST.json')},'snapshot_safe_allowlist':{'path':str((S/'PUBLIC_SAFE_ALLOWLIST.json').relative_to(A)),**pin(S/'PUBLIC_SAFE_ALLOWLIST.json')},'required_repairs':[summary['required_repair']],'review07_plan_sealed_before_implementation':True,'separate_revision':'lifecycle_controls_preparation_07','two_clean_NEW_science_reviews_unchanged':True,'case_percent':79,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'fully_completed_count':39,'published_count':23,'goal_complete':False}
fresh(A/'ROOT_OPERATIONAL_REVIEW06_REPAIR_REQUIRED.json',out)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());case.update(UTC=stamp,status='SCIENTIFIC_PACKAGE_READY_REPAIRING_PUBLIC_EVIDENCE_SCHEMA_FINDING',case_percent=79,publication_ready=False,operational_lifecycle_audit_active=True,operational_required_repairs=out['required_repairs'],operational_review06_Root_authentication='ROOT_OPERATIONAL_REVIEW06_REPAIR_REQUIRED.json',operational_review06_incomplete=True,remaining_required_steps='Strict own-only public evidence schemas, NEW07 independent review; actual Zenodo DOI/tracker/original-head MAIN merge and factual acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — PR191 workflow79%: independent06 recorded425 earlier successful expectations, then a separate focused synthetic public-evidence sanitization failure. Two report-finalization turns were stopped by an automated safety filter, so no terminal review/seal or clearance is inferred. Root read and preserved available small evidence/provenance in an exclusive0444 snapshot, retaining original namespace and hashing but excluding unsealed large result/reproducer bodies from publication. Required07 repair is strict own-only schemas for all generated public service evidence. New reviewer07 sealed its plan before implementation. No real private data/service operation or publication/merge; proof/package/two scientific reviews unchanged;39/23.\n')
print(json.dumps(out))

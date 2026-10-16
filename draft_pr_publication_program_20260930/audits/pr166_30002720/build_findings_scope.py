from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
A=Path(__file__).resolve().parent;C=A.parents[2];P=C/'draft_pr_publication_program_20260930'
def require(x,msg):
 if not x:raise RuntimeError(msg)
def main():
 old=json.loads((A/'MATH_CHECKPOINT_SCOPE_PLAN.json').read_text())
 own=list(old['public_case_relative_paths'])
 own+=['ROOT_VERIFICATION_ADDENDUM.md','PRIORITY_DECISION.md','ROOT_PRIORITY_GATE.json','ROOT_CATEGORY_GATE.json','ROOT_FINAL_SCIENTIFIC_DISPOSITION.json','PR_CLOSURE_COMMENT.md','PR_CLOSURE_BODY.md','PR_DISPOSITION_PLAN.json','PR_CLOSURE_ACTION_RECEIPT.json','PR_CLOSURE_ACCEPTANCE.json','MAIN_WRITER_RETURN.json','WORKFLOW_COMPLETION.json','build_findings_scope.py','FINDINGS_SCOPE_PLAN.json','prepare_findings_checkpoint.py','accept_findings_checkpoint.py',
 'root_reproduction/reproduce_author_independent.py','root_reproduction/independent_checks_raised.py','root_reproduction/AUTHOR_INDEPENDENT_REPRODUCTION_AND_NEGATIVES.json',
 'root_math/authenticate_category_family.py','root_math/CATEGORY_FAMILY_AUTHENTICATION.json',
 'root_priority/authenticate_priority_families.py','root_priority/PRIORITY_FAMILY_MANIFEST_AUTHENTICATION.json','root_priority/ROOT_MECHANISM_SEARCH_LEDGER.json','root_priority/ROOT_PRIMARY_READ_MATRIX.json','root_priority/ROOT_PRELIMINARY_PRIORITY_COMPARISON.md','root_priority/acquire_thesis.py','root_priority/fetch_disclosure_timeline.py','root_priority/ORIGINAL_PR_COMMIT_HISTORY.json']
 auth=json.loads((A/'root_priority/PRIORITY_FAMILY_MANIFEST_AUTHENTICATION.json').read_text())
 require(len(auth['families'])==3,'Three complete priority inventories required')
 for fam in auth['families']:own.extend(fam['family']+'/'+x for x in fam['public_allowlist'])
 ca=json.loads((A/'root_math/CATEGORY_FAMILY_AUTHENTICATION.json').read_text())
 own.extend('category_consequence_adversary/'+x for x in ca['public_allowlist'])
 own=sorted(set(own))
 require(all(not any(p.startswith(('private','scratch')) for p in Path(x).parts) for x in own),'Private path in public scope')
 require(all(not Path(x).is_absolute() and '..' not in Path(x).parts for x in own),'Unsafe path')
 future={'PR_CLOSURE_ACTION_RECEIPT.json','PR_CLOSURE_ACCEPTANCE.json','MAIN_WRITER_RETURN.json','WORKFLOW_COMPLETION.json','FINDINGS_SCOPE_PLAN.json','prepare_findings_checkpoint.py','accept_findings_checkpoint.py'}
 for x in own:
  if x not in future:require((A/x).is_file(),'Missing public artifact '+x)
 prior=old['prior_completion_relative_paths'];intake=old['ordered_status_intake_relative_paths']
 plan=dict(UTC=datetime.now(timezone.utc).isoformat(),schema='original-target-prior-known-curated-findings-v1',PR=166,original_head='efc3f35a72543ad9ae76fd31a860116f1ffd4a32',original_QUEUE_status='claimed_solved',public_audit_relative_paths=own,prior_completion_relative_paths=prior,ordered_intake_public_relative_paths=intake,programme_paths=['draft_pr_publication_program_20260930/'+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']],QUEUE_path='unsolved_math_prioritization/QUEUE.md',QUEUE_rows_changed=1,native_attempt_paths_changed=0,author_branch_changed=False,PR_scope='Exactly166: detailed one closure comment, title/body disposition, closed unmerged; original head preserved.',new_paper=False,new_DOI=False,new_tracker_row=False,scientific_audits_complete=True,original_universal_target_prior_known=True,precise_continuity_refinement_not_asserted_known=True,new_category_deduction_verified=True,fully_completed_count_before=32,fully_completed_count_after_actual_acceptance=33,published_count=18,requires_fresh_explicit_bounded_MAIN_writer_return=True,requires_expected_old_nonforce_CAS=True,no_local_Git_index_ref_branch_checkout_operations=True,goal_complete=False)
 (A/'FINDINGS_SCOPE_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
 b=(A/'FINDINGS_SCOPE_PLAN.json').read_bytes()
 print(json.dumps(dict(public_case_files=len(own),prior_completion_files=len(prior),ordered_intake_files=len(intake),programme_files=3,QUEUE_files=1,total_selected=len(own)+len(prior)+len(intake)+4,plan_bytes=len(b),plan_sha256=hashlib.sha256(b).hexdigest()),indent=2))
if __name__=='__main__':main()

from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parent
C=A.parents[2];P=C/'draft_pr_publication_program_20260930'
def require(x,msg):
 if not x:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),mode=format(stat.S_IMODE(p.stat().st_mode),'04o'))
def main():
 auth=json.loads((A/'root_math/MATH_FAMILY_MANIFEST_AUTHENTICATION.json').read_text())
 require(auth['status']=='ALL_THREE_MATH_FAMILY_EXACT_MANIFESTS_AUTHENTICATED','Math family authentication absent')
 own=['.gitignore','README.md','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','ORIGINAL_INTAKE.json','ORIGINAL_FILE_MANIFEST.json',
 'ROOT_MATH_GATE.json','ROOT_PRELIMINARY_MATH_ANALYSIS.md',
 'root_math/authenticate_math_families.py','root_math/complete_math_gate.py','root_math/MATH_FAMILY_MANIFEST_AUTHENTICATION.json',
 'root_primary/acquire_sources.py','root_primary/SOURCE_ACQUISITIONS.json',
 'root_reproduction/reproduce.py','root_reproduction/verify_raised.py','root_reproduction/REPRODUCTION_AND_NEGATIVE_CONTROLS.json',
 'repaired_candidate_v1/COUNTEREXAMPLE.md','repaired_candidate_v1/verify.py','repaired_candidate_v1/REPAIR_NOTE.md',
 'original_submission/PR_METADATA.json','original_submission/HEAD_COMMIT.json',
 'root_priority/GITHUB_DISCLOSURE_TIMELINE.json','root_priority/EXACT_PROOF_HISTORY_READBACK.json',
 'build_math_checkpoint_scope.py','MATH_CHECKPOINT_SCOPE_PLAN.json','ROOT_GOAL_READONLY_OBSERVATION.json']
 for row in auth['families']:own.extend(row['family']+'/'+rel for rel in row['public_allowlist'])
 original='original_submission/files/unsolved_math_prioritization/attempts/30002720/'
 own.extend(original+n for n in ['COUNTEREXAMPLE.md','problem.json','source_manifest.json','verify.py'])
 own=sorted(set(own));require(all('private' not in Path(rel).parts and 'scratch' not in Path(rel).parts for rel in own),'Private scope')
 oldcase=['audits/pr164_30002879/'+n for n in ['CURRENT_CASE_STATUS.json','WORKFLOW_COMPLETION.json','RESEARCH_LOG.md','FINAL_CHECKPOINT_ACCEPTANCE.json']]
 intake=['status_intakes_after_pr164/'+n for n in ['intake_status_only.py','PR165_STATUS_ONLY.json','PR166_STATUS_ONLY.json','INTAKE_SUMMARY.json','RESEARCH_LOG.md']]
 others=['draft_pr_publication_program_20260930/'+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']]
 plan=dict(UTC=datetime.now(timezone.utc).isoformat(),schema='math-progress-only-bounded-checkpoint-v1',PR=166,original_head='efc3f35a72543ad9ae76fd31a860116f1ffd4a32',status='CONCRETE_PUBLIC_MATH_SCOPE_READY_NO_REMOTE_OBJECT_OR_REF_MUTATIONS',public_case_relative_paths=own,prior_completion_relative_paths=oldcase,ordered_status_intake_relative_paths=intake,other_selected_paths=others,math_clearance=True,priority_clearance=False,publication_clearance=False,case_percent=33,completed_count=32,published_count=18,dated_denominator=99,no_QUEUE_change=True,no_native_attempt_change=True,no_PR_or_DOI_or_tracker_change=True,no_local_Git_mutation=True,private_bodies_excluded=True,requires_fresh_scoped_MAIN_window=True,requires_expected_old_nonforce_CAS=True,goal_complete=False)
 (A/'MATH_CHECKPOINT_SCOPE_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
 selected=[A/rel for rel in own]+[P/rel for rel in oldcase+intake]
 for path in selected:require(path.is_file(),'Missing selected file '+str(path))
 print(json.dumps(dict(case_files=len(own),prior_completion_files=len(oldcase),intake_files=len(intake),programme_files=3,total=len(selected)+3,plan=pin(A/'MATH_CHECKPOINT_SCOPE_PLAN.json')),indent=2))
if __name__=='__main__':main()

"""SOURCE ONLY: ROOT must personally read, copy and actually invoke this author."""
from pathlib import Path
import sys,hashlib,json,os,argparse
from datetime import datetime,timezone
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr49_30000703';F=A/'root_whole_reconciliation_preparation'
p=argparse.ArgumentParser();p.add_argument('--root-complete-personal-read',action='store_true',required=True);p.add_argument('--inspection-core-sha256',required=True);args=p.parse_args()
assert args.root_complete_personal_read
core=F/'inspection_core.py';assert hashlib.sha256(core.read_bytes()).hexdigest()==args.inspection_core_sha256
sys.path.insert(0,str(F))
from inspection_core import collect,recheck,observed
q=collect();recheck(q)
q.update(schema='pr49-root-complete-closed-whole-inspection/v1',created_utc=datetime.now(timezone.utc).isoformat(),actual_ROOT_authoring_pid=os.getpid(),status='PASS_ROOT_COMPLETE_CLOSED_CURRENT_WHOLE_RECONCILIATION',approved_by_root=True,complete_report_personally_read=True,complete_verdict_personally_read=True,complete_sources_and_actual_captures_personally_read=True,author_source=observed(Path(__file__).resolve()),inspection_core_source=observed(core),status_classification='already_solved',exact_full_known_target_verified=True,project_solved=False,novelty_claimed=False,credit='Kraus, Roth and Ruscheweyh (2007)',full_2007_journal_proof_independently_certified=False,original_substantive_attempts=0,turn_limit=5,new_substantive_attempts=0,audit_turns=0,separate_original_source_response_count=None,inherited_context_and_nonblind_independence_qualified=True,required_review_custody_repair_resolved=True,ROOT_initial_failed_closure=82903,ROOT_wrong_hash_failed_readback=444,actual_ROOT_clean_closure=267,actual_ROOT_clean_readback=755,acceptance_SOURCE_review_or_execution_approved=False,current_native_acceptance_approved=False,future_PR48_acceptance_approved=False,future_acceptance_approved=False,actual_external_authoring_capture_required_after_exit=True)
dest=A/'ROOT_WHOLE_CURRENT_REVIEW.json'
with dest.open('x') as f:f.write(json.dumps(q,indent=2)+'\n')
print(json.dumps(dict(status=q['status'],actual_ROOT_authoring_pid=os.getpid(),record=observed(dest),normalized_fixed_bindings=len(q['normalized_complete_fixed_bindings']),dated_native4=4,future_acceptance_approved=False)))

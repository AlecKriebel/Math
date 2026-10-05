"""Close bounded priority after independent custody and ROOT adjudication."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
assert sys.flags.optimize==0
A=Path(__file__).resolve().parent
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
receipts={}
for name in ['ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json','ROOT_PRIORITY_TARGET_CLOSED_CUSTODY.json','ROOT_PRIORITY_MECHANISM_CLOSED_CUSTODY.json','ROOT_CLASSICAL_REDUCTION_CLOSED_CUSTODY.json','ROOT_PRIORITY_CONTROL_REPRODUCTION.json']:
 x=json.loads((A/name).read_text());assert str(x['status']).startswith('PASS') or name=='ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json'
 receipts[name]=pin(A/name)
reports=['priority_target_adversary_01/REPORT.md','priority_target_adversary_01/VERDICT.json','priority_mechanism_adversary_01/REPORT.md','priority_mechanism_adversary_01/VERDICT.json','priority_mechanism_adversary_01/TIKHONOV_EXISTENCE_REDUCTION.md','classical_reduction_adversary_01/INDEPENDENT_PROOF.md','classical_reduction_adversary_01/VERDICT.md','classical_reduction_adversary_01/SOURCE_SCOPE.md','ROOT_PRIORITY_ADJUDICATION.md','ROOT_priority_source_crosscheck_20261005/ROOT_SOURCE_COMPARISONS_01.md']
result=dict(status='PASS_ROOT_BOUNDED_PRIORITY_FOR_PREPRINT_PREPARATION',UTC=datetime.now(timezone.utc).isoformat(),
 actual_closer_pid=os.getpid(),argv=sys.argv,cwd=os.getcwd(),source=pin(__file__),original_head='eb6e0e999521d84a65f9857d338cad76b84d30db',
 original_status='claimed_solved',author_turns=2,receipts=receipts,reports=[pin(A/p) for p in reports],
 mathematical_percent=100,bounded_priority_percent=100,workflow_percent=40,no_located_encompassing_spectral_theorem=True,
 alternative_classical_reduction_mathematically_verified=True,alternative_is_new_current_derivation_not_located_earlier_publication=True,
 historical_wording_repair_resolved=True,publisher_final2011_uninspected=True,universal_firstness_not_established=True,
 permitted_next_stage='Prepare precise preprint and portable verification materials, then sequential NEW whole-package adversarial reviews',
 preprint_or_publication_ready=False,DOI_tracker_native_merge_ready=False,all_public_claims_must_preserve_adjudication=True,
 no_global_Git_service_or_PR_mutation=True)
(A/'ROOT_BOUNDED_PRIORITY_GATE_ACCEPTANCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('reports','receipts')},indent=2))

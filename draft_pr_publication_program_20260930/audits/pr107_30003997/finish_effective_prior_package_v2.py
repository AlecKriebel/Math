from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;R=A/'repaired_diagnostics_v2';D=A/'effective_prior_package_v2_validation_20261006'
def require(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((D/'VERDICT.json').read_text());require(v['status']=='PASS' and v['actual_runs']==8,'actual v2 validation')
require((D/'0.stdout.bin').read_bytes()==(D/'2.stdout.bin').read_bytes(),'author mode drift')
require((D/'4.stdout.bin').read_bytes()==(D/'6.stdout.bin').read_bytes(),'independent mode drift')
for name,n in [('verification.json',0),('independent_results.json',4)]:
 b=(D/(str(n)+'.stdout.bin')).read_bytes();json.loads(b);(R/name).write_bytes(b)
require(json.loads((R/'verification.json').read_text())['artifact_sha256']==sha(R/'PROOF.md'),'current proof pin')
for name in ['verify.py','independent_checks.py']:require((R/name).read_bytes()==(A/'repaired_diagnostics_v1'/name).read_bytes(),'code drift')
pins=[{'file':str(p.relative_to(A)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.iterdir()) if p.is_file()]
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'PR':107,'original_head':'cc2ae01897135b35bee135917819e782a220f2c1','current_effective_audit_package':'repaired_diagnostics_v2','dated_mathematical_snapshot':'repaired_diagnostics_v1','immutable_original':'original_source_authentication_20261006/original_attempt','metadata_only_update_since_cleared_math_gate':True,'advertised_hardness_bundle_prior_corollary':True,'exact_optimum_identity_priority':'unresolved; substantive novelty not established','no_new_publication_claim':True,'actual_normal_optimized_replays':8,'new_proof_search_turns':0,'pins':pins}
(A/'CURRENT_EFFECTIVE_ARTIFACTS_20261006.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'current_proof_sha256':sha(R/'PROOF.md'),'actual_operator_PID':os.getpid(),'pins':len(pins)}))

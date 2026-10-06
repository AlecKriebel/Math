"""Check and bind the completed audit outputs; writes only this audit folder."""
from pathlib import Path
import datetime
import hashlib
import json
import os

directory = Path(__file__).resolve().parent
normal = json.loads((directory/'EXACT_CONTROLS_NORMAL.json').read_bytes())
optimized = json.loads((directory/'EXACT_CONTROLS_OPTIMIZED.json').read_bytes())
left = {k:v for k,v in normal.items() if k not in ('UTC','actual_PID')}
right = {k:v for k,v in optimized.items() if k not in ('UTC','actual_PID')}
if left != right or not normal['all_checks_passed'] or normal['checks'] != 4076:
    raise RuntimeError('Final independent normal/optimized control disagreement')
pins = normal['source_pins']
summary = {
    'schema':'pr111-independent-global-flow-adversary/v1',
    'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_finalization_PID':os.getpid(),
    'PR':111, 'problem_id':4900006,
    'original_head':'8a7270989d7064a4b97badecaa4b311db5e6d49f',
    'original_status':'claimed_solved', 'original_effort':'2/5',
    'mathematical_candidate_clear':True, 'mathematical_audit_percent':100,
    'required_mathematical_fixes':[],
    'scope':'Literal unrestricted smooth dissipative complete flow with compact minimal global attractor; explicit nonnegative pointwise and finite-time KY plus separately fixed-global-index expression.',
    'repaired_counterexample_pin':pins[-1],
    'source_pins':pins,
    'exact_checks_per_execution':normal['checks'],
    'normal_actual_PID':normal['actual_PID'],
    'optimized_actual_PID':optimized['actual_PID'],
    'normal_optimized_results_identical_except_custody_fields':True,
    'verified_mechanisms':[
        'Global real-analytic Cartesian field and full forward/backward completeness',
        'Strict everywhere ambient volume contraction with exact positive-polynomial certificate',
        'All complete radial trajectories including 0/1/2 and interior/boundary strata',
        'Uniform attraction of every bounded set and minimal exact disk-product attractor',
        'Unique equilibrium and all four periodic circles, no double-active periodic orbit',
        'All singular-value spectra from exact diagonal corotating variational blocks',
        'All six pointwise and fixed-index dimensions, unique UU maximizer',
        'Finite-time strict comparison without exact supremum/infimum equality'],
    'priority_or_novelty_cleared':False,
    'primary_publication_wording_verified_by_this_agent':False,
    'historical_chaotic_generic_Lorenz_or_typical_systems_resolved':False,
    'new_central_proof_search_turns':0,
    'Git_PR_service_queue_cache_mutations':0,
    'original_author_verifier_or_original_review_used':False,
    'remaining_gate':'Independent historical-source framing and bounded priority; whole-publication review remains separate.',
}
(directory/'AUDIT_SUMMARY.json').write_text(json.dumps(summary, sort_keys=True, indent=2)+'\n')
members=[]
for name in ('REPORT.md','RESEARCH_LOG.md','verify_independently.py',
             'EXACT_CONTROLS_NORMAL.json','EXACT_CONTROLS_OPTIMIZED.json',
             'finalize_audit.py','AUDIT_SUMMARY.json'):
    body=(directory/name).read_bytes()
    members.append({'path':name,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
manifest={'schema':'pr111-independent-global-flow-output-manifest/v1',
          'UTC':summary['UTC'], 'members':members}
(directory/'OUTPUT_MANIFEST.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
print(json.dumps({'actual_PID':os.getpid(),'clear':True,
                  'checks_each':normal['checks'],'files_bound':len(members)}))

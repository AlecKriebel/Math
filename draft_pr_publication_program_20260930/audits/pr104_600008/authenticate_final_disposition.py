from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent;C=A.parents[2]
F=A/'final_disposition_adversary_20261006'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
M=json.loads((F/'MANIFEST.json').read_text());pins=[]
for group,base in [('inputs',A),('outputs',F),('external_policy_inputs',None)]:
    for rel,row in M[group].items():
        p=Path(rel) if base is None else base/rel
        b=p.read_bytes()
        if len(b)!=row['bytes'] or sha(p)!=row['sha256']:raise RuntimeError('changed review pin: '+str(p))
        pins.append({'path':str(p),'bytes':len(b),'sha256':row['sha256']})
V=json.loads((F/'VERDICT.json').read_text())
if V['required_corrections'] or V['unresolved_concerns_within_bounded_disposition']:
    raise RuntimeError('review not clean')
if V['substantive_new_contribution_established'] or V['recommended_native_classification']['status']!='already_solved':
    raise RuntimeError('wrong disposition')
S=json.loads((A/'original_source_authentication_20261006/original_attempt/status.json').read_text())
turns=[json.loads(s) for s in (A/'original_source_authentication_20261006/original_attempt/turns.jsonl').read_text().splitlines()]
if S['status']!='claimed_solved' or S['substantive_approaches']!=1 or [x['turn'] for x in turns]!=[1]:
    raise RuntimeError('incoming effort/status mismatch')
note=A/'PROPOSED_CLOSING_PRIORITY_NOTE_20261006.md'
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'schema':'pr104-final-analytic-disposition-ready/v1','UTC':UTC,'actual_operator_PID':os.getpid(),
 'PR':104,'original_head':'4d8ba8e9438c9c8a463721adc1102dee821b11df','original_literal_status':'claimed_solved',
 'original_budget':'1/5','extra_central_proof_search_turns':0,
 'fresh_final_disposition_review_authenticated':True,'review_manifest_sha256':sha(F/'MANIFEST.json'),
 'authenticated_pins':pins,'required_corrections':[],'unresolved_concerns_within_bounded_disposition':[],
 'no_substantive_new_contribution_established':True,'mathematics_verified':True,
 'verified_prior_analytic_criterion_recovered':True,'native_status_correction_supported':True,
 'supported_native_status':'already_solved','scope':'literal analytic classification, prior reconstruction/classical corollary',
 'exact_earlier_printing_or_earliest_priority_verified':False,'finite_algebraic_cayley_output_verified':False,
 'full_singular_flow_convergence_certified':False,
 'closing_comment_file':note.name,'closing_comment_sha256':sha(note),
 'global_queue_sha256_before':sha(C/'unsolved_math_prioritization/QUEUE.md'),
 'disposition':'close_without_merge_or_new_paper','closure_executed':False,'native_change_executed':False,
 'DOI':None,'workflow_estimate_percent':80}
(A/'ROOT_DISPOSITION_READY_20261006.json').write_text(json.dumps(record,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+UTC+' — Fresh final disposition review read in full and all input/output/policy pins authenticated. PASS: no required correction or concern within the analytic prior-result disposition. Source/math/priority-review100%, workflow80%; original1/5, extra central proof-turns0. Same-head closure and source-bound native correction remain to execute; no publication.\n')
print(json.dumps({k:v for k,v in record.items() if k!='authenticated_pins'}))

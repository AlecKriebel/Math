"""Record ROOT's adjudication of closed independent mathematics and guard repair."""
from pathlib import Path
import json,hashlib,datetime,os
A=Path(__file__).resolve().parent;P=A.parents[1];C=A.parents[2]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def dump(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
authentication=json.loads((A/'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json').read_text())
require(authentication['status']=='ALL_THREE_REVIEW_MANIFESTS_AUTHENTICATED' and len(authentication['records'])==3,'review authentication incomplete')
statuses=[r['verdict'].get('status',r['verdict'].get('verdict')) for r in authentication['records']]
require(statuses==['PASS_LITERAL_ANALYTIC_CRITERION','PASS_BOUNDED_MATHEMATICAL_AUDIT','PASS_PRECISE_ANALYTIC_CRITERION_WITH_ORIGINAL_CHECKER_OPTIMIZATION_DEFECT'],'review statuses')
repair=json.loads((A/'repaired_diagnostics_validation_20261006/VERDICT.json').read_text())
require(repair['status']=='PASS_REPAIRED_BOUNDED_DIAGNOSTICS' and repair['all_original_bodies_unchanged'],'repair validation')
require(authentication['records'][2]['verdict']['minimal_RuntimeError_guard_repair_sufficient'],'independent repair assessment')
gate={'schema':'pr104-root-mathematical-gate/v1','UTC':UTC,'actual_operator_PID':os.getpid(),
 'PR':104,'problem_id':600008,'source_head':'4d8ba8e9438c9c8a463721adc1102dee821b11df',
 'candidate_sha256':'608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae',
 'status':'PASS_COMPLETE_LITERAL_ANALYTIC_CRITERION_WITH_REPAIRED_DIAGNOSTICS',
 'domain':'all real a,b,c>0; positive actual-path lift; positive n,r; negative winding by orientation reversal; no nontrivial zero-winding closure',
 'verified_claim':'M=(2pi)^-1 integral_0^(2pi) sqrt((a sin²t+b cos²t)/(c+a sin²t+b cos²t))dt; rho=(1-M)/(2M); equator T^n closure with winding r iff M=n/(n+2r); literal full-arc closure additionally n even.',
 'least_period':'For rho=p/q reduced, folded period q and full-arc period lcm(2,q); iterated closures explicitly distinguished.',
 'written_proof_adjudication':'Global monotone-root coverage, smooth equator gluing, degenerate boundary homeomorphism, null geodesic and ordinary winding arguments, paired-cut contour identity and positive-axis parameter classification pass.',
 'fresh_review_families':authentication['records'],
 'repaired_diagnostics_folder':'repaired_diagnostics_v1','diagnostic_proof_bytes_unchanged':True,
 'normal_and_optimized_controls':{'author':2087,'independent':752,'four_false_controls_rejected':True},
 'independent_ambient_flow_diagnostics':'11 cases/17 initial trajectories/two tolerances; max normalized rotation defect6.257067729267415e-10; diagnostics without interval certification.',
 'required_mathematical_repairs_remaining':[],
 'publication_exposition_requirements':['Explicit even full-arc count and least/iterated distinction','Do not treat the equal-axis shrinking cut as a zero integral; continuity or direct evaluation','Do not advertise a finite algebraic Cayley determinant or ordinary division-polynomial criterion','Credit GKT invariant density/Poncelet theorem and distinguish imported third-kind differential error','Use corrected source URLs and keep previous reviews unchanged as dated records'],
 'blocked_imported_route':'Automatic ordinary elliptic-group translation inference from the real third-kind density; no alternative algebraic nonexistence claim.',
 'original_budget':'1/5','new_central_proof_search_turns':0,'mathematical_audit_percent':100,'PR_workflow_percent':25,
 'priority_clearance':False,'publication_clearance':False,'native_acceptance':False,
 'next_step':'Independent deep priority audit of the exact analytic formula and source problem; publication preparation follows only if priority clears.'}
dump(A/'ROOT_MATHEMATICAL_GATE_20261006.json',gate)
progress=json.loads((P/'CURRENT_PROGRESS.json').read_text())
require(progress['current_PR']==104,'active cursor')
progress.update({'UTC':UTC,'updated_UTC':UTC,'current_mathematical_audit_percent':100,'current_mathematical_clearance':True,
 'current_mathematical_gate':'audits/pr104_600008/ROOT_MATHEMATICAL_GATE_20261006.json',
 'current_math_family_evidence_readback_complete':True,'current_repaired_diagnostics':'audits/pr104_600008/repaired_diagnostics_v1',
 'current_PR_workflow_percent':25,'current_workflow_estimate_percent':25,
 'current_source_authentication_checkpoint':'e7aa71139e953a6f9b76b78f86a0f62067e20f04',
 'current_source_authentication_checkpoint_remote_verified':True,
 'remaining_current_step':'Conduct deep priority audit; no publication or native merge clearance yet.',
 'next_step':'Deep independent priority audit for104.'})
dump(P/'CURRENT_PROGRESS.json',progress)
entry=UTC+' — PR104 complete literal analytic criterion accepted after three fresh mathematical families, ROOT reconstruction, full2087/752 checker reproduction, independent ambient-flow diagnostics and a confirmed minimal optimization-guard repair. Original candidate proof unchanged; original1/5, extra proof-search0. Source100%, mathematics100%, priority0%, PR104workflow25%; overall14/99=14.14%. Algebraic Cayley formulation and historical novelty remain unestablished; deep priority audit next.\n'
for path in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with path.open('a') as f:f.write('\n'+entry)
selected=[P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'ROOT_RECONSTRUCTION_20261006.md',A/'ROOT_MATHEMATICAL_GATE_20261006.json',A/'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json',A/'authenticate_math_families.py',A/'record_math_gate.py',A/'repair_diagnostics.py',A/'validate_repaired_diagnostics.py',A/'INTAKE_CHECKPOINT_SELECTION_20261006.json']
for name in ['geometry_source_adversary_20261006','period_identity_adversary_20261006','independent_reproduction_20261006','repaired_diagnostics_v1','repaired_diagnostics_validation_20261006','actual_checkpoints/intake_release','actual_operations/intake_release','actual_operations/record_intake_checkpoint','actual_operations/repair_diagnostics','actual_operations/validate_repaired_diagnostics','actual_operations/authenticate_math_families','actual_operations/render_source2015','actual_operations/render_source2007_map','actual_operations/render_source2007_question']:
    selected.extend(p for p in (A/name).rglob('*') if p.is_file() and not p.is_symlink())
dump(A/'MATH_CHECKPOINT_SELECTION_20261006.json',{'UTC':UTC,'paths':sorted(set(str(p.relative_to(C)) for p in selected)),
 'expected_parent':'e7aa71139e953a6f9b76b78f86a0f62067e20f04','third_party_fulltexts_excluded':True,
 'mathematics_percent':100,'workflow_percent':25,'priority_clearance':False})
print(json.dumps({'UTC':UTC,'mathematical_gate':gate['status'],'selected_paths':len(selected),'original_budget':'1/5','extra_proof_search':0,'workflow_percent':25}))

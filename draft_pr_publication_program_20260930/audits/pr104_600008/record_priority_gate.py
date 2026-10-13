from pathlib import Path
import json, hashlib, datetime, os
A=Path(__file__).resolve().parent
P=A.parents[1];C=A.parents[2]
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
specs=[('priority_exact_formula_history_20261006',['local_inputs','outputs'],'family'),
       ('priority_garcia_wustholz_20261006',['input_pins','files'],'family'),
       ('priority_classical_mechanism_20261006',['artifacts'],'family'),
       ('prior_solution_claim_adversary_20261006',['input_pins','output_pins'],'effort')]
families=[];public=[]
for name,keys,relative in specs:
    F=A/name;M=json.loads((F/'MANIFEST.json').read_text());pins=[]
    for key in keys:
        for row in M[key]:
            base=A if relative=='effort' else F
            path=(base/row['path']).resolve()
            if not path.is_relative_to(A) or path.is_symlink():raise RuntimeError('scope: '+str(path))
            data=path.read_bytes()
            if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
                raise RuntimeError('changed pin: '+str(path))
            pins.append({'path':str(path.relative_to(A)),'bytes':len(data),'sha256':row['sha256']})
            private=('private_sources' in path.parts or row.get('private_third_party',False))
            if path.is_relative_to(F) and not private:public.append(str(path.relative_to(C)))
    public.append(str((F/'MANIFEST.json').relative_to(C)))
    families.append({'name':name,'manifest_sha256':hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),
                     'authenticated_pins':pins})
record={'schema':'pr104-priority-adjudication/v1','UTC':UTC,'actual_operator_PID':os.getpid(),
    'source_head':'4d8ba8e9438c9c8a463721adc1102dee821b11df','source_authentication_percent':100,
    'mathematics_percent':100,'bounded_priority_audit_percent':100,'workflow_estimate_percent':70,
    'novel_resolution_priority_clearance':False,'publication_clearance':False,
    'verified_prior_analytic_classification_recoverable':True,
    'recommended_disposition':'close_without_new_paper_analytic_prior_result_classical_corollary',
    'supported_label':'already_solved_analytic_via_verified_reconstruction',
    'exact_prior_printed_mean_formula_verified':False,'earliest_priority_exhaustively_established':False,
    'finite_algebraic_cayley_limit_verified':False,'complete_singular_flow_convergence_certified':False,
    'mathematical_repairs_complete':True,'required_novel_mathematical_increment_established':False,
    'source_of_prior_analytic_criterion':'DR1909.08154v1 Eq3.2 and Remark4.4, with checked scalar surface reconstruction',
    'classical_period_identity_source':'DLMF19.7.8',
    'adjudication_of_narrower_history_report':'The history family recovered the prior claim but did not verify its limit. Two separate families subsequently completed the scalar limit, count mapping and direct surface sufficiency; the difference is additional checked evidence, not an erased initial report.',
    'families':families,'final_fresh_disposition_review_pending':True,
    'global_queue_changed':False,'closure_executed':False,'native_integration_complete':False,
    'paper_created':False,'DOI':None,'original_budget':'1/5','extra_central_proof_search_turns':0}
(A/'ROOT_PRIORITY_GATE_20261006.json').write_text(json.dumps(record,indent=2)+'\n')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_text())
if progress['current_PR']!=104:raise RuntimeError('wrong effort')
progress.update({'UTC':UTC,'updated_UTC':UTC,'current_priority_audit_percent':100,
    'current_PR_workflow_percent':70,'current_workflow_estimate_percent':70,
    'current_priority_clearance':False,'current_analytic_prior_resolution_verified':True,
    'current_priority_gate':'audits/pr104_600008/ROOT_PRIORITY_GATE_20261006.json',
    'current_supported_disposition_label':record['supported_label'],
    'current_final_disposition_review_pending':True,
    'remaining_current_step':'Complete fresh final disposition adversary, then act on the precise prior-result classification.',
    'next_step':'Fresh final disposition review running for104; no novel-resolution publication.'})
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2,sort_keys=True)+'\n')
entry=f'{UTC} — PR104 deep priority audit closed:4 bounded families authenticated; prior explicit2019 solution claim and scalar analytic criterion reconstructed, independently checked necessary/sufficient with actual counts; metric and third-kind identity classical. No substantive new mathematical contribution established. Source100%, math100%, bounded priority audit100%, workflow70%; fresh disposition review pending; program14/99=14.14%. No exact-formula first printing, finite Cayley limit or complete singular-flow convergence certification. Original1/5, extra proof-search0. No service/native/publication action.\n'
for path in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with path.open('a') as f:f.write('\n'+entry)
public += [str((A/n).relative_to(C)) for n in ['ROOT_PRIORITY_ADJUDICATION_20261006.md','PROPOSED_CLOSING_PRIORITY_NOTE_20261006.md','ROOT_PRIORITY_GATE_20261006.json','record_priority_gate.py','ROOT_PRIORITY_INTERIM_20261006.md','ROOT_PRIORITY_INTERIM_RECEIPT_20261006.json','record_priority_interim.py','RESEARCH_LOG.md']]
public += [str((P/n).relative_to(C)) for n in ['CURRENT_PROGRESS.json','RESEARCH_LOG.md']]
for label in ['priority_live_pr_readback','priority_remote_main_readback','priority_interim']:
    public += [str(f.relative_to(C)) for f in (A/'actual_operations'/label).iterdir() if f.is_file()]
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:
    public.append(str((A/'actual_checkpoints/mathematics_release'/name).relative_to(C)))
public += [str(f.relative_to(C)) for f in (A/'actual_operations/mathematics_release').iterdir() if f.is_file()]
selection={'schema':'explicit-pr104-priority-checkpoint-selection/v1','UTC':UTC,'paths':sorted(set(public)),
    'private_fulltext_bodies_excluded':True,'further_final_review_files_not_yet_selected':True}
(A/'PRIORITY_CHECKPOINT_SELECTION_20261006.json').write_text(json.dumps(selection,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='families'}))

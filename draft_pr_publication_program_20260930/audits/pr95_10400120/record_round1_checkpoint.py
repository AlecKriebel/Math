from pathlib import Path
import datetime, json, os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];R=A/'whole_qualified_package_round1_20261005'
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
issues=json.loads((R/'ISSUES.json').read_text())
if issues['verdict']!='MATHEMATICS_PASS_PACKAGE_REPAIR_REQUIRED':raise RuntimeError('review disposition')
pr=P/'CURRENT_PROGRESS.json';p=json.loads(pr.read_text());p.update({'UTC':utc,'current_PR_workflow_percent':60,
    'current_whole_package_review_rounds_completed':1,'current_whole_package_round1_mathematics_pass':True,
    'current_whole_package_required_repairs':['R1: reject symlinked ancestor path components in payload guard'],
    'current_package_repair_target':'audits/pr95_10400120/qualified_publication_package_v2',
    'current_active_whole_package_reviewer':None,'current_publication_ready':False,
    'remaining_current_step':'Prepare v2 with component-wise linked-path rejection and fresh negative controls, preserving immutable v1; then new fresh whole-package review before qualified publication.'});dump(pr,p)
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n### '+utc+' — round1 closed, repair assigned; PR95 workflow60%, math100%, priority85% unresolved; program12/99 (12.12%)\nFirst fresh full-package adversary independently reconstructs the ordinary full SU(5) counterexample, authenticates primary formula/domain/topology/normalization, and passes fresh exact and false-target processes and all five PDF pages. Required low-severity R1: an unchanged ancestor-directory symlink can pass the payload guard despite the linked-path claim. ROOT read the report and independent derivation, authenticated997 closed files and assigned corrected v2 with explicit component rejection and normal/optimized hostile controls. Frozen v1 remains unchanged and is not relabeled clean. No publication, tracker append, PR merge, primary checkout/index or new proof-search turn occurred. Three root operational helpers are prepared and syntax checked but unexecuted.\n')
paths={str(pr.relative_to(C)),str((A/'RESEARCH_LOG.md').relative_to(C))}
for n in ['authenticate_whole_review.py','record_round1_checkpoint.py','prepare_native_acceptance.py','verify_public_deposit.py','append_verified_tracker.py','UNEXECUTED_ACCEPTANCE_HELPERS.json','ROOT_AUTHENTICATED_whole_qualified_package_round1_20261005.json']:
    paths.add(str((A/n).relative_to(C)))
d=json.loads((R/'CLOSED_MANIFEST.json').read_text())
for e in d['files']:paths.add(str((R/e['file']).relative_to(C)))
for n in ['CLOSED_MANIFEST.json','SHA256SUMS','CLOSURE.json']:
    if (R/n).is_file():paths.add(str((R/n).relative_to(C)))
for n in ['actual_operations/root_round1_closed_integrity','actual_operations/record_prepared_qualified_candidate',
    'actual_operations/checkpoint_prepared_qualified_candidate','actual_operations/round1_checkpoint_remote',
    'actual_checkpoints/prepared_qualified_candidate']:
    for f in (A/n).rglob('*'):
        if f.is_file() and not f.is_symlink():paths.add(str(f.relative_to(C)))
dump(A/'round1_checkpoint_selection.json',{'paths':sorted(paths)})
print(json.dumps({'UTC':utc,'PID':os.getpid(),'workflow_percent':60,'selected_paths':len(paths),'publication_ready':False}))

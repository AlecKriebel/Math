from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];Q=A/'qualified_publication_package_v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=json.loads((A/'root_portable_reproduction_python39_20261005/results.json').read_text())
if r['status']!='PASS_EXACT_SPECIALIZATION' or len(r['runs'])!=12:raise RuntimeError('fresh reproduction')
x={'schema':'pr95-root-prepared-candidate-checkpoint/v1','UTC':utc,'actual_operator_PID':os.getpid(),
   'preparation_complete':True,'whole_package_review_complete':False,'publication_ready':False,
   'priority_clearance':False,'qualified_publication_user_authorized':True,
   'frozen_manifest_sha256':sha(Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json'),
   'root_fresh_reproduction':{'file':'root_portable_reproduction_python39_20261005/results.json','sha256':sha(A/'root_portable_reproduction_python39_20261005/results.json'),'runtime':r['runtime'],'positive_processes':6,'actual_false_rejections':6},
   'root_pdf_visual_read_pages':[1,2,3,4,5],'root_final_visual_defects_found':0,
   'workflow_percent':55,'program_completion':'12/99 (12.12%)','new_central_proof_search_turns':0,
   'active_fresh_reviewer':'pr95_whole_qualified_package_round1_20261005'}
dump(A/'ROOT_PREPARED_QUALIFIED_CANDIDATE_20261005.json',x)
pr=P/'CURRENT_PROGRESS.json';p=json.loads(pr.read_text());p.update({'UTC':utc,'current_PR_workflow_percent':55,
    'current_package_preparation_percent':100,'current_prepared_candidate':'audits/pr95_10400120/ROOT_PREPARED_QUALIFIED_CANDIDATE_20261005.json',
    'current_publication_ready':False,'current_active_whole_package_reviewer':x['active_fresh_reviewer'],
    'remaining_current_step':'First fresh whole-package adversarial review is active; repair globally, then assign a new second reviewer before qualified publication, tracker and merge. Priority remains unresolved.'});dump(pr,p)
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n### '+utc+' — prepared candidate checkpoint; PR95 workflow55%, package preparation100%, priority85% unresolved; program12/99 (12.12%)\nROOT read the complete manuscript, public support, code and exact metadata, visually inspected all five final PDF pages, and authenticated 693 prepared files, 113 public bodies, 14 preparation inputs and all110 ZIP members. A separate actual CPython3.9.6/NumPy1.24.3 full reproduction passed six positives and rejected six false coefficient targets, with ordinary/optimized output agreement. First new whole-package adversary is active; fresh second review and all services remain pending. Qualified priority exception stays separate from priority clearance. Original effort2/5, zero new proof-search turns. No primary index, external outreach, editor tab or service write.\n')
paths={str(pr.relative_to(C)),str((A/'RESEARCH_LOG.md').relative_to(C))}
for rel in ['ROOT_PREPARED_QUALIFIED_CANDIDATE_20261005.json','NATIVE_ACCEPTANCE_PLAN_20261005.md','authenticate_qualified_candidate.py','record_qualified_candidate_checkpoint.py']:
    paths.add(str((A/rel).relative_to(C)))
manifest=json.loads((Q/'PREPARATION_MANIFEST.json').read_text())
for e in manifest['files']:paths.add(str((Q/e['file']).relative_to(C)))
paths.add(str((Q/'PREPARATION_MANIFEST.json').relative_to(C)))
for rel in ['root_qualified_candidate_authentication_20261005','root_portable_reproduction_python39_20261005',
   'actual_operations/root_qualified_candidate_authentication','actual_operations/root_python39_portable_reproduction',
   'actual_operations/pre_review_checkpoint_remote','actual_operations/tracker_tab_metadata','actual_operations/tracker_current_headers',
   'actual_operations/tracker_schema_get','actual_operations/tracker_schema_values_get','actual_operations/tracker_schema_append',
   'actual_operations/qualified_source_PR95_current','actual_checkpoints/qualified_note_authorization']:
    for f in (A/rel).rglob('*'):
        if f.is_file() and not f.is_symlink():paths.add(str(f.relative_to(C)))
dump(A/'qualified_candidate_checkpoint_selection.json',{'paths':sorted(paths)})
print(json.dumps({'UTC':utc,'PID':os.getpid(),'prepared_selected_paths':len(paths),'workflow_percent':55,'publication_ready':False}))

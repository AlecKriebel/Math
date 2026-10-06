"""Advance the live audit cursor without carrying prior-PR clearance fields."""
from pathlib import Path
import json,datetime,hashlib,os,shutil
A=Path(__file__).resolve().parent;P=A.parents[1];C=A.parents[2]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def dump(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
D=A/'original_source_authentication_20261006'
source=json.loads((D/'ORIGINAL_BLOB_MANIFEST.json').read_text())
pair=json.loads((D/'SOURCEPAIR_AUTHENTICATION.json').read_text())
retrieval=json.loads((A/'primary_sources_20261006/RETRIEVAL_MANIFEST.json').read_text())
require(source['source_head']=='4d8ba8e9438c9c8a463721adc1102dee821b11df' and pair['submitted_source_equals_raw_and_SQL'],'source authentication')
require(len(retrieval['records'])==3 and all(r.get('matches_submitted_pin') and r.get('extraction',{}).get('exit_code')==0 for r in retrieval['records']),'primary retrieval')
for pin in source['files']:
    body=Path(pin['preserved_path']).read_bytes()
    require(len(body)==pin['bytes'] and hashlib.sha256(body).hexdigest()==pin['sha256'],'original body changed')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_text())
require(progress['last_completed_PR']==97,'last completed identity')
progress={k:v for k,v in progress.items() if not k.startswith('current_')}
progress.update({'UTC':UTC,'updated_UTC':UTC,'persistent_goal_status':'active','persistent_goal_status_at_last_tool_read':'active',
 'persistent_goal_complete':False,'current_PR':104,'current_problem_id':600008,
 'current_original_head':source['source_head'],'current_original_literal_status':'claimed_solved','current_original_budget':'1/5',
 'current_new_central_proof_search_turns':0,'current_source_authentication_complete':True,'current_source_authentication_percent':100,
 'current_source_authentication_record':str((D/'ORIGINAL_BLOB_MANIFEST.json').relative_to(P)),
 'current_sourcepair_record':str((D/'SOURCEPAIR_AUTHENTICATION.json').relative_to(P)),
 'current_primary_sources_record':str((A/'primary_sources_20261006/RETRIEVAL_MANIFEST.json').relative_to(P)),
 'current_fresh_math_agents':['pr104_geometry_source_adversary_20261006','pr104_period_identity_adversary_20261006','pr104_independent_reproduction_20261006'],
 'current_mathematical_audit_percent':15,'current_mathematical_clearance':False,'current_priority_clearance':False,
 'current_priority_audit_percent':0,'current_publication_ready':False,'current_publication_percent':0,
 'current_native_integration_complete':False,'current_DOI':None,'current_tracker_range':None,'current_merge_commit':None,
 'current_PR_workflow_percent':10,'current_workflow_estimate_percent':10,
 'current_human_disposition_question_pending':False,
 'latest_ordered_intake_record':'ordered_intake_20261006/after_PR97/INTAKE_AFTER_PR97.json',
 'next_numeric_intake_cursor':105,'next_eligible_PR_after_current_completion':None,
 'skipped_since_last_completion':[{'PR':i,'literal_status':('already_solved' if i==99 else 'unsolved')} for i in range(98,104)],
 'remaining_current_step':'Close independent mathematical audit of PR104, then bounded priority audit if mathematics passes.',
 'next_step':'Independent source/geometry, period, and reproduction families running for104.',
 'completion_metadata_checkpoint_pending_at_snapshot':True})
dump(P/'CURRENT_PROGRESS.json',progress)
text=UTC+' — PR104 exact eligible head, all21 original native bodies, immutable source/prior pair and three public primary PDFs authenticated. Primary retrieval matches all three submitted SHA256 pins. Fresh independent geometry/source, period and reproduction families launched without shared conclusions; original1/5 and extra central proof-search0. Native/source100%, mathematics15%, priority0%, PR104workflow10%; program14/99=14.14%. No publication/merge clearance; no shared primary mutation.\n'
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+text)
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+text)
shutil.copyfile(P/'audits/pr97_10300055/scoped_checkpoint.py',A/'scoped_checkpoint.py')
paths=[P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'authenticate_original_source.py',A/'authenticate_source_pair.py',A/'retrieve_primary_sources.py',A/'record_cli.py',A/'record_intake_checkpoint.py',A/'scoped_checkpoint.py',A/'INITIAL_SHARED_RECORDER_CUSTODY_20261006.json',A/'primary_sources_20261006/RETRIEVAL_MANIFEST.json',P/'audits/pr97_10300055/ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json',P/'audits/pr97_10300055/record_closure_release_readback.py']
paths.extend(p for p in D.rglob('*') if p.is_file() and not p.is_symlink())
for folder in [A/'actual_operations/authenticate_pr104_source_initial_shared_recorder',A/'actual_operations/source_pair',A/'actual_operations/primary_sources',P/'ordered_intake_20261006/after_PR97']:
    paths.extend(p for p in folder.rglob('*') if p.is_file() and not p.is_symlink())
paths=sorted(set(str(p.relative_to(C)) for p in paths))
require(all((C/p).is_file() for p in paths),'selected artifact missing')
dump(A/'INTAKE_CHECKPOINT_SELECTION_20261006.json',{'UTC':UTC,'actual_operator_PID':os.getpid(),'paths':paths,'expected_main_parent':'6d0010f800248b0c136d723bd2b2f8c79f2892df','primary_fulltexts_excluded':True,'mathematical_and_priority_clearance':False})
print(json.dumps({'UTC':UTC,'selected_paths':len(paths),'current_PR':104,'source_percent':100,'math_percent':15,'workflow_percent':10,'program_percent':100*14/99}))

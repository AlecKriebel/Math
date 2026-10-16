"""Build an explicit publication/disposition allowlist from authenticated artifacts."""
from pathlib import Path
import datetime,hashlib,importlib.util,json
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('repair190',A/'run_review_repair_checkpoint_02.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def require(x,msg):
 if not x:raise RuntimeError(msg)
g=json.loads((A/'ROOT_PUBLICATION_GATE.json').read_text());z=json.loads((A/'ZENODO_PUBLICATION_READBACK.json').read_text());tr=json.loads((A/'TRACKER_ACCEPTANCE.json').read_text())
require(g['status']=='READY_FOR_AUTHORIZED_PUBLICATION' and z['state']=='published','Actual publication absent')
require(tr['status']=='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED' and tr['DOI']==z['doi'],'Actual tracker absent')
names=m.own_paths()
names+=['FINAL_MAIN_SCOPE.json','ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json','ROOT_WHOLE_REVIEW02_FINAL_AUTHENTICATION.json','ROOT_PUBLICATION_GATE.json','ROOT_V2_VISUAL_ACCEPTANCE.json','REPAIR_CHECKPOINT_ACCEPTANCE_02.json','PR_METADATA_REQUEST.json','PR_METADATA_ACCEPTANCE.json','ZENODO_LOCAL_CHECK.json','ZENODO_STAGE_READBACK.json','ZENODO_DRAFT_READBACK.json','ZENODO_PUBLICATION_READBACK.json','ZENODO_POSTPUBLICATION_INSPECTION.json','TRACKER_ACCEPTANCE.json','run_zenodo_step.py','record_tracker.py','prepare_native_final_01.py','prepare_final_scoped_merge.py','prepare_factual_completion.py','prepare_final_main_scope.py','ROOT_WHOLE_REVIEW_INPUT_02.json','integration_preparation/NATIVE_TEMPLATE_FINAL_01_MANIFEST.json']
names+=['campaign_aliases.py','ROOT_DISPOSITION_REPAIR_01.json','repair_disposition_safeguards_01.py','prepare_publication_gate.py','prepare_pr_metadata_request.py','prepare_publication_lifecycle_scripts_02.py','prepare_lifecycle_utilities_20261015.py']
support=json.loads((A/'disposition_script_audit/SAFE_AUTHORED_ALLOWLIST.json').read_text())
names+=['disposition_script_audit/'+n for n in support.get('files',support.get('key_files'))]
recheck=json.loads((A/'disposition_script_audit/targeted_recheck_01/RECHECK_SAFE_AUTHORED_ALLOWLIST.json').read_text())
names+=['disposition_script_audit/targeted_recheck_01/'+n for n in recheck['key_files']]
names+=['ROOT_DISPOSITION_REPAIR_ACCEPTANCE.json']
for d in ['whole_package_review_02']:
 j=json.loads((A/d/'SAFE_AUTHORED_ALLOWLIST.json').read_text());names += [d+'/'+n for n in j.get('files',j.get('key_files'))]
cur=json.loads((A/'integration_preparation/CURRENT_TEMPLATE.json').read_text());require(cur['current_template']=='native_template_final_01','Native final template absent')
names += ['integration_preparation/'+cur['current_template']+'/'+n for n in cur['files']]
for n in ['APPEND_REQUEST.json','APPEND_ATTEMPT_STARTED.json','APPEND_RESPONSE.stdout.json','APPEND_RESPONSE.stderr.txt','ROW_READBACK_1.stdout.json','ROW_READBACK_1.stderr.txt','ROW_READBACK_2.stdout.json','ROW_READBACK_2.stderr.txt']:
 require((A/'sheets_tracking'/n).is_file(),'Own tracker receipt absent '+n);names.append('sheets_tracking/'+n)
names=sorted(set(names))
for n in names:
 p=A/n;require((n=='FINAL_MAIN_SCOPE.json' or p.is_file()) and not p.is_symlink() and not any('private' in q.lower() or 'chrome' in q.lower() or q.startswith('.zenodo') for q in Path(n).parts),'Unsafe scope '+n)
prefix=m.CASE;native='unsolved_math_prioritization/attempts/5000007/'
selected=sorted([prefix+n for n in names]+[native+n for n in cur['files']]+[m.PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']]+['unsolved_math_prioritization/QUEUE.md'])
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'PR':190,'original_head':m.HEAD,'case_paths':names,'selected_MAIN_paths':selected,'DOI':z['doi'],'tracker_range':tr['range'],'historical_priority_clearance':False,'qualified_note_route_authorized':True,'case_percent':95,'completed_count_before_actual_acceptance':38,'published_count_before_actual_acceptance':22,'foreign_base_paths_preserved':True,'peer_pause_assumed':False,'factual_receipt_additional_allowed_paths':[prefix+n for n in ['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json']]}
(A/'FINAL_MAIN_SCOPE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'case_paths':len(names),'selected_MAIN_paths':len(selected),'scientific_packet':g['package_name'],'native_files':len(cur['files'])}))

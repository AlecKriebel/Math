"""Install exact independently accepted controls and issue Root's final authority.

No service, PR, Git/index/ref/checkout mutation. Refuses every pre-existing output.
Requires Root's separately authored, terminal independent07 PASS authentication.
"""
from pathlib import Path
import datetime,hashlib,importlib.util,json,stat,sys
A=Path(__file__).resolve().parent
def require(x,m):
 if not x:raise RuntimeError(m)
def read(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def match(p,x):require(pin(p)=={k:x[k] for k in ['bytes','sha256']},'Bound bytes drift '+str(p))
def binding(n):return {'path':n,**pin(A/n)}
def fresh(n,j):
 p=A/n
 with p.open('x') as f:f.write(json.dumps(j,indent=2)+'\n')
 p.chmod(0o444)
def main():
 require(sys.dont_write_bytecode,'Use -B');authname='ROOT_OPERATIONAL_REVIEW07_AUTHENTICATION.json';auth=read(A/authname)
 require(auth['status']=='ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW07_PASS' and auth['PR']==191 and auth['all_required_findings_globally_resolved'] is True and auth['outstanding_required_repairs']==[],'Root final independent07 acceptance absent')
 for role in ['report','seal']:
  require(auth[role]['path'].startswith('lifecycle_adversary_07/'),'Wrong independent review family');match(A/auth[role]['path'],auth[role])
 F=A/'lifecycle_controls_preparation_07';seal=read(F/'FINAL_SEAL.json');match(F/'FINAL_SEAL.json',auth['proposal_seal']);runtime=seal['runtime_pins']
 required={'lifecycle_common.py','campaign_aliases.py','run_zenodo_step.py','record_tracker.py','prepare_native_final_01.py','prepare_pr_metadata_request.py','prepare_final_main_scope.py','prepare_final_scoped_merge.py','prepare_factual_completion.py'}
 require(set(runtime)==required,'Exact nine accepted runtime files required')
 for n,x in runtime.items():match(F/n,x);require(not (A/n).exists(),'Canonical file exists; no overwrite '+n)
 for n in ['ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json','ROOT_LIFECYCLE_RUNTIME_INSTALLATION.json','ROOT_CASE_SCIENTIFIC_PROJECTION.json','ROOT_CASE_BASELINE.json','ROOT_CASE_LOG_BASELINE.md','ROOT_PUBLICATION_GATE.json']:require(not (A/n).exists(),'Existing authority; no overwrite '+n)
 g=read(A/'ROOT_PUBLICATION_GATE_DRAFT_01.json');require(g['status'].startswith('DRAFT_') and g['all_required_findings_globally_resolved'] is False,'Expected nonauthority source draft')
 seed=read(A/'IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS06_01.json');pins=dict(g['public_case_pins']);pins.update(seed['public_case_pins'])
 for n,x in pins.items():match(A/n,x)
 for family,allow,key in [('lifecycle_controls_preparation_07','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_controls_preparation_06','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_controls_preparation_05','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_controls_preparation_04','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_controls_preparation_03','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_adversary_02','PUBLIC_SAFE_ALLOWLIST.json','files'),('lifecycle_adversary_03','PUBLIC_SAFE_ALLOWLIST.json','files'),('lifecycle_adversary_04','PUBLIC_SAFE_ALLOWLIST.json','files'),('lifecycle_adversary_05','PUBLIC_SAFE_ALLOWLIST.json','files'),('lifecycle_adversary_06_snapshot_01','PUBLIC_SAFE_ALLOWLIST.json','files'),('lifecycle_adversary_07','PUBLIC_SAFE_ALLOWLIST.json','files')]:
  for n in read(A/family/allow)[key]:pins[family+'/'+n]=pin(A/family/n)
 extra=['OPERATIONS06_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS06_01.json','prepare_operations06_checkpoint.py','OPERATIONS05_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS05_01.json','prepare_operations05_checkpoint.py','OPERATIONS04_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS04_01.json','prepare_operations04_checkpoint.py','OPERATIONS_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS_01.json','OPERATIONS03_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS03_01.json','OPERATIONS03_REF_UPDATE_RECONCILIATION_01.json','OPERATIONS03_CHECKPOINT_STALE_c9da117f665ae2d941115a63cdb49d3b47df86d4.json','ROOT_OPERATIONAL_REVIEW02_REPAIR_REQUIRED.json','authenticate_operational_review02.py',authname,'prepare_root_publication_clearance_v6.py','prepare_root_publication_clearance_v5.py','ROOT_OPERATIONAL_REVIEW06_REPAIR_REQUIRED.json','authenticate_available_review06_evidence.py','ROOT_OPERATIONAL_PROPOSAL07_AUTHENTICATION.json','authenticate_operational_proposal07.py','prepare_root_publication_clearance_v4.py','ROOT_OPERATIONAL_REVIEW05_REPAIR_REQUIRED.json','authenticate_operational_review05.py','ROOT_OPERATIONAL_PROPOSAL06_AUTHENTICATION.json','authenticate_operational_proposal06.py','prepare_root_publication_clearance_v3.py','prepare_root_publication_clearance_v2.py','prepare_root_publication_clearance.py','ROOT_OPERATIONAL_PROPOSAL03_AUTHENTICATION.json','authenticate_operational_proposal03.py','ROOT_OPERATIONAL_REVIEW03_REPAIR_REQUIRED.json','authenticate_operational_review03.py','ROOT_OPERATIONAL_PROPOSAL04_AUTHENTICATION.json','authenticate_operational_proposal04.py','ROOT_OPERATIONAL_REVIEW04_REPAIR_REQUIRED.json','authenticate_operational_review04.py','ROOT_OPERATIONAL_PROPOSAL05_AUTHENTICATION.json','authenticate_operational_proposal05.py']
 for n in extra:pins[n]=pin(A/n)
 stamp=datetime.datetime.now(datetime.UTC).isoformat()
 for n in sorted(runtime):
  with (A/n).open('xb') as f:f.write((F/n).read_bytes())
  (A/n).chmod(0o444);match(A/n,runtime[n]);pins[n]=pin(A/n)
 spec=importlib.util.spec_from_file_location('root_prepublication_runtime_check',A/'lifecycle_common.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 fresh('ROOT_CASE_BASELINE.json',read(A/'CURRENT_CASE_STATUS.json'));pins['ROOT_CASE_BASELINE.json']=pin(A/'ROOT_CASE_BASELINE.json')
 with (A/'ROOT_CASE_LOG_BASELINE.md').open('xb') as f:f.write((A/'RESEARCH_LOG.md').read_bytes())
 (A/'ROOT_CASE_LOG_BASELINE.md').chmod(0o444);pins['ROOT_CASE_LOG_BASELINE.md']=pin(A/'ROOT_CASE_LOG_BASELINE.md')
 fresh('ROOT_CASE_SCIENTIFIC_PROJECTION.json',m.case_scientific_projection(read(A/'ROOT_CASE_BASELINE.json')));pins['ROOT_CASE_SCIENTIFIC_PROJECTION.json']=pin(A/'ROOT_CASE_SCIENTIFIC_PROJECTION.json')
 fresh('ROOT_LIFECYCLE_RUNTIME_INSTALLATION.json',{'UTC':stamp,'PR':191,'status':'EXACT_NINE_INDEPENDENTLY_ACCEPTED_RUNTIME_FILES_INSTALLED_WITHOUT_OVERWRITE','source':'lifecycle_controls_preparation_07','source_seal':pin(F/'FINAL_SEAL.json'),'runtime_pins':runtime,'Root_authentication':binding(authname),'actual_remote_actions_performed':False})
 fresh('ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json',{'UTC':stamp,'PR':191,'original_head':g['original_head'],'status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':runtime,'independent_adversary_review':{'disposition':'PASS','report':auth['report'],'seal':auth['seal'],'root_authentication':binding(authname)},'qualified_note_only':True,'two_scientific_whole_package_reviews_unchanged':True,'actual_publication':False,'actual_tracker_updated':False,'actual_original_PR_merged':False})
 for n in ['ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json','ROOT_LIFECYCLE_RUNTIME_INSTALLATION.json']:pins[n]=pin(A/n)
 g.update(UTC=stamp,status='READY_FOR_AUTHORIZED_PUBLICATION',all_required_findings_globally_resolved=True,operational_clearance=True,draft_only=False,public_case_pins=dict(sorted(pins.items())),public_case_paths=sorted(set(pins)|{'CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json'}),operational_clearance_receipt=binding('ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json'),actual_Zenodo_published=False,actual_DOI=None,actual_tracker_updated=False,actual_original_PR_merged=False)
 original_read=m.read
 def virtual_read(p):return g if Path(p)==A/'ROOT_PUBLICATION_GATE.json' else original_read(p)
 m.read=virtual_read;m.gate();m.read=original_read
 fresh('ROOT_PUBLICATION_GATE.json',g);m.gate()
 case=m.derive_case_ready(read(A/'ROOT_CASE_BASELINE.json'),g,pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'])
 (A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write(m.ready_case_log_suffix(stamp))
 print(json.dumps({'status':g['status'],'runtime_files':len(runtime),'immutable_public_case_pins':len(pins),'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'actual_publication':False}))
if __name__=='__main__':main()

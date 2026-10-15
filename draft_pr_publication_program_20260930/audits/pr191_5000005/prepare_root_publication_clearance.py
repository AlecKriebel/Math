"""Install exact independently accepted controls and issue Root's final authority.

No service, PR, Git/index/ref/checkout mutation. Refuses every pre-existing output.
Requires Root's separately authored, terminal independent03 PASS authentication.
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
 require(sys.dont_write_bytecode,'Use -B');authname='ROOT_OPERATIONAL_REVIEW03_AUTHENTICATION.json';auth=read(A/authname)
 require(auth['status']=='ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW03_PASS' and auth['PR']==191 and auth['all_required_findings_globally_resolved'] is True and auth['outstanding_required_repairs']==[],'Root final independent03 acceptance absent')
 for role in ['report','seal']:
  require(auth[role]['path'].startswith('lifecycle_adversary_03/'),'Wrong independent review family');match(A/auth[role]['path'],auth[role])
 F=A/'lifecycle_controls_preparation_03';seal=read(F/'FINAL_SEAL.json');match(F/'FINAL_SEAL.json',auth['proposal_seal']);runtime=seal['runtime_pins']
 required={'lifecycle_common.py','campaign_aliases.py','run_zenodo_step.py','record_tracker.py','prepare_native_final_01.py','prepare_pr_metadata_request.py','prepare_final_main_scope.py','prepare_final_scoped_merge.py','prepare_factual_completion.py'}
 require(set(runtime)==required,'Exact nine accepted runtime files required')
 for n,x in runtime.items():match(F/n,x);require(not (A/n).exists(),'Canonical file exists; no overwrite '+n)
 for n in ['ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json','ROOT_LIFECYCLE_RUNTIME_INSTALLATION.json','ROOT_PUBLICATION_GATE.json']:require(not (A/n).exists(),'Existing authority; no overwrite '+n)
 g=read(A/'ROOT_PUBLICATION_GATE_DRAFT_01.json');require(g['status'].startswith('DRAFT_') and g['all_required_findings_globally_resolved'] is False,'Expected nonauthority source draft')
 seed=read(A/'IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS_01.json');pins=dict(g['public_case_pins']);pins.update(seed['public_case_pins'])
 for n,x in pins.items():match(A/n,x)
 for family,allow,key in [('lifecycle_controls_preparation_03','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_adversary_02','PUBLIC_SAFE_ALLOWLIST.json','files'),('lifecycle_adversary_03','PUBLIC_SAFE_ALLOWLIST.json','files')]:
  for n in read(A/family/allow)[key]:pins[family+'/'+n]=pin(A/family/n)
 extra=['OPERATIONS_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS_01.json','ROOT_OPERATIONAL_REVIEW02_REPAIR_REQUIRED.json','authenticate_operational_review02.py',authname,'prepare_root_publication_clearance.py']
 for n in extra:pins[n]=pin(A/n)
 stamp=datetime.datetime.now(datetime.UTC).isoformat()
 for n in sorted(runtime):
  with (A/n).open('xb') as f:f.write((F/n).read_bytes())
  (A/n).chmod(0o444);match(A/n,runtime[n]);pins[n]=pin(A/n)
 fresh('ROOT_LIFECYCLE_RUNTIME_INSTALLATION.json',{'UTC':stamp,'PR':191,'status':'EXACT_NINE_INDEPENDENTLY_ACCEPTED_RUNTIME_FILES_INSTALLED_WITHOUT_OVERWRITE','source':'lifecycle_controls_preparation_03','source_seal':pin(F/'FINAL_SEAL.json'),'runtime_pins':runtime,'Root_authentication':binding(authname),'actual_remote_actions_performed':False})
 fresh('ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json',{'UTC':stamp,'PR':191,'original_head':g['original_head'],'status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':runtime,'independent_adversary_review':{'disposition':'PASS','report':auth['report'],'seal':auth['seal'],'root_authentication':binding(authname)},'qualified_note_only':True,'two_scientific_whole_package_reviews_unchanged':True,'actual_publication':False,'actual_tracker_updated':False,'actual_original_PR_merged':False})
 for n in ['ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json','ROOT_LIFECYCLE_RUNTIME_INSTALLATION.json']:pins[n]=pin(A/n)
 g.update(UTC=stamp,status='READY_FOR_AUTHORIZED_PUBLICATION',all_required_findings_globally_resolved=True,operational_clearance=True,draft_only=False,public_case_pins=dict(sorted(pins.items())),public_case_paths=sorted(set(pins)|{'CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json'}),operational_clearance_receipt=binding('ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json'),actual_Zenodo_published=False,actual_DOI=None,actual_tracker_updated=False,actual_original_PR_merged=False)
 spec=importlib.util.spec_from_file_location('root_prepublication_runtime_check',A/'lifecycle_common.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 original_read=m.read
 def virtual_read(p):return g if Path(p)==A/'ROOT_PUBLICATION_GATE.json' else original_read(p)
 m.read=virtual_read;m.gate();m.read=original_read
 fresh('ROOT_PUBLICATION_GATE.json',g);m.gate()
 case=read(A/'CURRENT_CASE_STATUS.json');case.setdefault('retired_operational_aliases_PR191',[]).append({'UTC':stamp,'operational_lifecycle_audit_active':case.get('operational_lifecycle_audit_active'),'operational_required_repairs':case.get('operational_required_repairs')});case.update(UTC=stamp,status='TWO_CLEAN_SCIENCE_REVIEWS_AND_FRESH_OPERATIONAL_REVIEW_COMPLETE_READY_FOR_AUTHORIZED_PUBLICATION',case_percent=90,publication_ready=True,operational_lifecycle_audit_active=False,operational_required_repairs=[],operational_clearance_receipt='ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json',publication_gate_SHA256=pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],remaining_required_steps='Actual exact-kit Zenodo publication and DOI, unique GWS row, original-head MAIN merge and full-scope factual acceptance before intake192.')
 (A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — PR191 workflow90%: two successive NEW clean whole mathematical/package reviews remain byte-identical. New independent03 operations review PASS; Root authenticated final code/evidence and global repairs; exact9 canonical controls installed without overwrite, final qualified-note publication gate issued and locally validated without service actions. No actual publication/DOI/tracker/PR metadata/ready/merge yet.39/23 unchanged; no192 intake until actual factual MAIN acceptance.\n')
 print(json.dumps({'status':g['status'],'runtime_files':len(runtime),'immutable_public_case_pins':len(pins),'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'actual_publication':False}))
if __name__=='__main__':main()

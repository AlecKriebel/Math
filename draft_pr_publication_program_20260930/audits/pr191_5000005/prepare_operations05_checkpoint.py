"""Release factual operational-review progress; preserve scientific packet and foreign MAIN."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('ready191',A/'prepare_ready_checkpoint.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
m=old.m;m.m.TREE_CACHE_PATH=A/'OPERATIONS05_CHECKPOINT_IMMUTABLE_TREE_CACHE.json'
api,require,save,body_at=m.api,m.require,m.save,m.body_at
PREFIX,CASE,HEAD=old.PREFIX,old.CASE,old.HEAD
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def paths():
 names=set(old.paths())|{'READY_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_READY_01.json','ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json','ROOT_OPERATIONAL_REVIEW01_REPAIR_REQUIRED.json','ROOT_OPERATIONAL_PROPOSAL02_AUTHENTICATION.json','authenticate_operational_proposal02.py','prepare_operations05_checkpoint.py'}
 names.update(['OPERATIONS_CHECKPOINT_ACCEPTANCE.json', 'IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS_01.json', 'prepare_operations_checkpoint.py', 'ROOT_OPERATIONAL_REVIEW02_REPAIR_REQUIRED.json', 'authenticate_operational_review02.py', 'ROOT_OPERATIONAL_PROPOSAL03_AUTHENTICATION.json', 'authenticate_operational_proposal03.py', 'ROOT_OPERATIONAL_REVIEW03_REPAIR_REQUIRED.json', 'authenticate_operational_review03.py', 'prepare_root_publication_clearance.py'])
 for family,allow,key in [('lifecycle_controls_preparation_01','PROPOSED_FILE_ALLOWLIST.json','key_files'),('lifecycle_controls_preparation_02','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_adversary_01','SAFE_ALLOWLIST.json','files'),('lifecycle_controls_preparation_03','PROPOSED_FILE_ALLOWLIST.json','files'),('lifecycle_adversary_02','PUBLIC_SAFE_ALLOWLIST.json','files'),('lifecycle_adversary_03','PUBLIC_SAFE_ALLOWLIST.json','files')]:
  names.update(family+'/'+n for n in json.loads((A/family/allow).read_text())[key])
 names.update(['prepare_operations03_checkpoint.py','OPERATIONS03_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS03_01.json','OPERATIONS03_REF_UPDATE_RECONCILIATION_01.json','OPERATIONS03_CHECKPOINT_STALE_c9da117f665ae2d941115a63cdb49d3b47df86d4.json','ROOT_OPERATIONAL_PROPOSAL04_AUTHENTICATION.json','authenticate_operational_proposal04.py','ROOT_OPERATIONAL_REVIEW04_REPAIR_REQUIRED.json','authenticate_operational_review04.py','prepare_root_publication_clearance_v2.py','prepare_root_publication_clearance_v3.py'])
 for family,allow in [('lifecycle_controls_preparation_04','PROPOSED_FILE_ALLOWLIST.json'),('lifecycle_adversary_04','PUBLIC_SAFE_ALLOWLIST.json')]:
  names.update(family+'/'+n for n in json.loads((A/family/allow).read_text())['files'])
 names.update(['prepare_operations04_checkpoint.py','OPERATIONS04_CHECKPOINT_ACCEPTANCE.json','IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS04_01.json','prepare_root_publication_clearance_v4.py','ROOT_OPERATIONAL_PROPOSAL05_AUTHENTICATION.json','authenticate_operational_proposal05.py','ROOT_OPERATIONAL_REVIEW05_REPAIR_REQUIRED.json','authenticate_operational_review05.py'])
 for family,allow in [('lifecycle_controls_preparation_05','PROPOSED_FILE_ALLOWLIST.json'),('lifecycle_adversary_05','PUBLIC_SAFE_ALLOWLIST.json')]:
  names.update(family+'/'+n for n in json.loads((A/family/allow).read_text())['files'])
 for n in names:require((A/n).is_file() and not (A/n).is_symlink(),'Missing reviewed public file '+n)
 return sorted(names)
def prepare(gen):
 require(gen.isalnum(),'Unsafe generation');old.old.old.open_original();names=paths();e=api('git/ref/heads/main')['object']['sha'];j=json.loads(body_at(PREFIX+'CURRENT_PROGRESS.json',e));require((j['fully_completed_count'],j['published_count'],j['last_completed_PR'],j['current_PR'])==(39,23,190,191),'Programme ownership changed')
 out=A/('operations05_preparation_'+gen);out.mkdir(exist_ok=False);stamp=now();case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());require(case['case_percent']==79 and not case['publication_ready'],'Unexpected operational state')
 note='\n\n'+stamp+' — PR191 workflow79%: two NEW clean scientific/package reviews unchanged. NEW independent operational05 report REPAIR_REQUIRED: current completion/intake aliases and new Root case-log claims require complete independently derived stage postimages. All24 safe05 audit files and18 frozen05 proposal files authenticated0444; separate06 full programme/case/log repairs and NEW06 independently presealed review plan. Frozen earlier failures and unused Root handoffs preserved. No actual runtime/clearance/gate, publication/DOI/tracker/metadata/ready/merge or192intake;39completed/23published unchanged.\n'
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write(note)
 j.update(UTC=stamp,updated_UTC=stamp,current_status=case['status'],current_PR_workflow_percent=79,current_workflow_estimate_percent=79,current_publication_ready=False,current_operational_lifecycle_audit_active=True,current_remaining_required_steps=case['remaining_required_steps'],remaining_current_step=case['remaining_required_steps'],next_step=case['remaining_required_steps'],next_numeric_intake_cursor=191,advance_to_next_PR_authorized_now=False,persistent_goal_complete=False,active_checkpoint_acceptance_receipt='audits/pr191_5000005/OPERATIONS05_CHECKPOINT_ACCEPTANCE.json',program_snapshot_authority_condition='Effective only after actual parent/full-scope and current-MAIN identity acceptance; no publication/disposition clearance.',program_snapshot_semantics='Two NEW clean scientific reviews; independent05 operations review requires two concrete repairs. Separate06 full stage derivations and fresh independent review pending;39completed/23published, no actual publication or merge.')
 save(out/'CURRENT_PROGRESS.json',j)
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:(out/n).write_bytes(body_at(PREFIX+n,e)+note.encode())
 overlay={CASE+n:A/n for n in names};overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']})
 r=old.old_prepare(e,overlay);r.update(UTC=stamp,generation=gen,case_percent=79)
 target=A/'OPERATIONS05_CHECKPOINT_PREPARATION.json'
 if target.exists():
  prior=json.loads(target.read_text());archive=A/('OPERATIONS05_CHECKPOINT_STALE_'+prior['commit']+'.json');require(not archive.exists(),'Stale receipt collision');save(archive,prior);archive.chmod(0o444)
 save(target,r);old.old.old.open_original();require(api('git/ref/heads/main')['object']['sha']==e,'MAIN advanced; preserve stale receipt and rebuild')
 print(json.dumps({'expected_main':e,'commit':r['commit'],'selected':len(r['selected_files']),'changed':len(r['changed_paths'])}))
def accept():
 r=json.loads((A/'OPERATIONS05_CHECKPOINT_PREPARATION.json').read_text());co=api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==[r['expected_main']],'Actual parent/tree drift');parent=api('git/commits/'+r['expected_main'])['tree']['sha'];require(parent==r['parent_tree'],'Receipt parent differs from actual parent');m.m.m.h.warm_selected_directories([parent,r['tree']],r['selected_files'])
 changed={n for n,x in r['selected_files'].items() if m.lookup(parent,n)!=('100644','blob',x['git_blob'])};require(set(r['changed_paths'])==changed==m.changed_leaves(parent,r['tree']),'Actual full-tree scope drift');actual=api('git/ref/heads/main')['object']['sha'];require(api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Checkpoint not on MAIN');t=m.require_selected_at_main(actual,r['selected_files'],r['tree'])
 for n in [PREFIX+'CURRENT_PROGRESS.json',CASE+'CURRENT_CASE_STATUS.json',CASE+'ROOT_OPERATIONAL_REVIEW01_REPAIR_REQUIRED.json',CASE+'ROOT_OPERATIONAL_PROPOSAL02_AUTHENTICATION.json',CASE+'ROOT_OPERATIONAL_REVIEW03_REPAIR_REQUIRED.json',CASE+'ROOT_OPERATIONAL_REVIEW04_REPAIR_REQUIRED.json',CASE+'ROOT_OPERATIONAL_REVIEW05_REPAIR_REQUIRED.json',CASE+'publication_package_v1/parallel_short_trajectories.pdf',CASE+'publication_package_v1/verification-package.zip']:
  b=body_at(n,actual);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh body drift '+n)
 old.old.old.open_original();out={'UTC':now(),'PR':191,'status':'ACTUAL_OPERATIONS_REPAIR_CHECKPOINT_PARENT_FULL_SCOPE_CURRENT_MAIN_ACCEPTED','checkpoint_commit':r['commit'],'main_observed':actual,'actual_tree':t,'selected_files':len(r['selected_files']),'every_selected_identity_checked_at_actual_observed_MAIN':True,'actual_original_parent_and_full_tree_scope_accepted':True,'foreign_MAIN_paths_preserved':True,'original_head':HEAD,'original_PR_open_draft_unmerged':True,'two_clean_NEW_science_reviews_unchanged':True,'operational_repair_active':True,'actual_published':False,'actual_tracker_updated':False,'case_percent':79,'fully_completed_count':39,'published_count':23,'goal_complete':False};save(A/'OPERATIONS05_CHECKPOINT_ACCEPTANCE.json',out);print(json.dumps(out))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare(sys.argv[2])
 elif sys.argv[1]=='accept':accept()
 else:raise RuntimeError('Unknown action')

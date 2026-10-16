"""PROPOSED post-factual PR191 receipt/status checkpoint. Import is inert.

Explicit prepare creates native tree/commit objects only; neither action moves
MAIN. Never calls the incompatible canonical publish route or any service write.
"""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;A=D.parent
REL='final_receipt_checkpoint_preparation_01/'
DOI='10.5281/zenodo.23389367';RANGE="'Math Puzzles'!A103:D103"
FINAL='ROOT_FINAL_FACTUAL_ACCEPTANCE.json'
MUTABLE=['CURRENT_CASE_STATUS.json','WORKFLOW_COMPLETION.json','RESEARCH_LOG.md']
PROGRAMME=['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']
def require(ok,message):
 if not ok:raise RuntimeError(message)
def read(p):return json.loads(Path(p).read_text())
def pin(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def json_bytes(j):return (json.dumps(j,indent=2)+'\n').encode()
def fresh(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 inputs=read(D/'SOURCE_INPUTS.json');require(pin(A/'lifecycle_common.py')==inputs['installed_common'] and pin(A/'ROOT_PUBLICATION_GATE.json')==inputs['gate'],'Installed runtime/gate changed')
 spec=importlib.util.spec_from_file_location('accepted_pr191_for_receipt_checkpoint',A/'lifecycle_common.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);return c

def context(c,current=True):
 """Verify the existing actual factual receipt; never issue/refresh one."""
 require((A/FINAL).is_file(),'Actual PR191 factual acceptance is required first')
 inputs=read(D/'SOURCE_INPUTS.json');require(pin(A/FINAL)==inputs['actual_factual_receipt'] and pin(A/'FINAL_FACTUAL_PREPARATION.json')==inputs['actual_factual_preparation'] and pin(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')==inputs['historical_merge_receipt'],'Pinned actual completion/merge receipts changed')
 g=c.gate();z=c.publication(g);tr=c.read(A/'TRACKER_ACCEPTANCE.json');row=c.validate_tracker(g,z,tr);c.observe_tracker(c.require_runtime()['tracker'],g,z,row,tr['range']);c.validate_metadata_documents(g,z,tr)
 require(z['doi']==DOI and tr['range']==RANGE,'Wrong actual own publication/tracker')
 h=c.helpers();m=c.read(A/'SCOPED_MERGE_PREPARATION.json');f=c.read(A/'FINAL_FACTUAL_PREPARATION.json');a=c.read(A/FINAL)
 c.verify_merge_scope(h,g,m,True);c.verify_prepared_native(h,g,z,tr,m,False);c.verify_stage_postimage(h,g,z,tr,m,95)
 c.verify_prepared(h,f,[f['expected_main']]);c.verify_prepared_native(h,g,z,tr,f,True);c.verify_stage_postimage(h,g,z,tr,f,100,m['commit'])
 require(set(f['selected_files'])==c.factual_paths(g),'Factual selected scope differs')
 combined={**m['selected_files'],**f['selected_files']}
 expected={'PR':191,'status':'ACTUAL_FACTUAL_COMPLETION_MAIN_PARENT_FULL_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED','factual_commit':f['commit'],'sole_parent':f['expected_main'],'combined_expected_current_identities_checked':len(combined),'every_selected_identity_checked_at_actual_observed_MAIN':True,'fully_completed_count':40,'published_count':24,'case_percent':100,'goal_complete':False,'next_original_status_intake':192,'next_numeric_intake_cursor_authorized_after_this_acceptance':192,'subsequent_status_only_intake_authorized':True,'live_programme_cursor_update_requires_next_own_checkpoint':True,'separate_selfreceipt_publication_required_at_next_own_checkpoint':True}
 require(set(a)==set(expected)|{'UTC','main_observed'} and all(type(a[k]) is type(v) and a[k]==v for k,v in expected.items()),'Actual factual acceptance receipt differs')
 require(c.valid_stamp(a['UTC'])<=c.valid_stamp(c.now()),'Factual acceptance time is in the future')
 require(h.api('compare/'+f['commit']+'...'+a['main_observed'])['status'] in ['identical','ahead'],'Receipt observation does not contain factual commit')
 main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+f['commit']+'...'+main)['status'] in ['identical','ahead'],'Accepted factual commit is not on current MAIN')
 p=h.api('pulls/191');require(p['merged'] and p['state']=='closed' and p['head']['sha']==c.HEAD,'Original PR completion changed')
 c.current_native(g,True,(z,tr))
 if current:c.selected_current(h,main,combined,f['tree']);core_readbacks(c,h,g,main,combined)
 return g,z,tr,h,m,f,a,combined,main

def core_readbacks(c,h,g,main,selected):
 names=[c.NATIVE+n for n in g['native_proof_paths']]+[c.CASE+g['current_proof']['path']]+[c.CASE+g['package_name']+'/'+n for n in g['paper_files'].values()]
 for n in names:require(c.byte_pin(h.body_at(n,main))==selected[n],'Fresh protected scientific body changed '+n)

def source_files(c):
 inputs=read(D/'SOURCE_INPUTS.json');out={}
 for n,x in inputs['extra_public_case_files'].items():
  p=c.inside(n);require(pin(p)==x,'Approved public source changed '+n);out[c.CASE+n]=p.read_bytes()
 for n in read(D/'PUBLIC_SAFE_ALLOWLIST.json')['files']:
  p=D/n;require(p.parent==D and p.is_file() and not p.is_symlink(),'Unsafe helper source');out[c.CASE+REL+n]=p.read_bytes()
 seal=read(D/'FINAL_SEAL.json')
 for x in seal['manifest']:require(pin(D/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Helper source seal drift')
 for n in [FINAL,'FINAL_FACTUAL_PREPARATION.json']:out[c.CASE+n]=(A/n).read_bytes()
 return out

def postimages(c,h,parent,stamp,a,z,tr):
 """Only declared current factual aliases/prose change; science/native do not."""
 c.valid_stamp(stamp);require(c.valid_stamp(a['UTC'])<=c.valid_stamp(stamp)<=c.valid_stamp(c.now()),'Completion recording date precedes acceptance or is future')
 receipt={'path':'audits/pr191_5000005/'+FINAL,**pin(A/FINAL)}
 note='\n'+stamp+' — PR191 actual factual MAIN acceptance '+a['factual_commit']+' is accepted;40completed/24published. Credited note '+z['doi_url']+'; own tracker '+tr['range']+' verified. Original claimed_solved2/5 and all scientific/native bytes retained. Actual completion receipt is recorded; numeric cursor192 is for a separate original-status-only intake, which this checkpoint does not perform. Broader goal remains active.\n'
 out={};case=json.loads(h.body_at(c.CASE+'CURRENT_CASE_STATUS.json',parent));prog=json.loads(h.body_at(c.PREFIX+'CURRENT_PROGRESS.json',parent));work=json.loads(h.body_at(c.CASE+'WORKFLOW_COMPLETION.json',parent))
 require((case['case_percent'],case['fully_completed_count'],case['published_count'],case['original_PR_merged'],case['PR_closed'])==(100,40,24,True,True),'Current case is not the accepted100 postimage')
 require((prog['current_PR'],prog['fully_completed_count'],prog['published_count'],prog['last_completed_PR'])==(191,40,24,191) and len(prog['fully_completed_eligible_PRs'])==40 and len(prog['published_PRs'])==24,'Actual40/24 census changed')
 protected={k:copy.deepcopy(case[k]) for k in c.CASE_PROTECTED_KEYS}
 oldkeys=['actual_factual_checkpoint_accepted','completion_metadata_checkpoint_pending_at_snapshot','last_completed_actual_final_receipt','conditional_last_completed_actual_final_receipt','conditional_next_numeric_intake_cursor','conditional_next_intake_requires_actual_factual_acceptance','remaining_required_steps','remaining_current_step','next_step','next_numeric_intake_cursor','advance_to_next_PR_authorized_now','program_snapshot_authority_condition','program_snapshot_semantics']
 for j in [case,prog]:
  j.setdefault('completion_receipt_history_PR191',[]).append({'UTC':stamp,'values':{k:copy.deepcopy(j[k]) for k in oldkeys if k in j}})
  for k in ['conditional_last_completed_actual_final_receipt','conditional_next_numeric_intake_cursor','conditional_next_intake_requires_actual_factual_acceptance']:j.pop(k,None)
  j.update(UTC=stamp,actual_factual_checkpoint_accepted=True,completion_metadata_checkpoint_pending_at_snapshot=False,last_completed_actual_final_receipt='audits/pr191_5000005/'+FINAL,actual_factual_acceptance_receipt=receipt,actual_factual_commit=a['factual_commit'],next_numeric_intake_cursor=192,advance_to_next_PR_authorized_now=True,next_intake_requires_actual_completion_receipt=True,next_status_only_intake_performed=False,completion_receipt_checkpoint_effective_after_actual_current_MAIN_acceptance=True)
 case.update(status='ACTUAL_FACTUAL_MAIN_COMPLETION_ACCEPTED_RECEIPT_RECORDED',case_completion_requires_actual_factual_postimage_acceptance=False,remaining_required_steps='PR191 complete; separate original-status-only intake192 follows after this checkpoint acceptance.')
 prog.update(updated_UTC=stamp,current_status='PR191_COMPLETE_ACTUAL_FACTUAL_ACCEPTANCE_RECORDED',current_PR_workflow_percent=100,current_workflow_estimate_percent=100,current_case_complete=True,current_remaining_required_steps=case['remaining_required_steps'],remaining_current_step=case['remaining_required_steps'],next_step='Separate original-status-only intake192; no intake performed by this checkpoint.',active_checkpoint_acceptance_receipt='audits/pr191_5000005/'+FINAL,program_snapshot_authority_condition='Actual PR191 factual acceptance exists; this receipt/status checkpoint is effective only after its own full-scope current-MAIN acceptance.',program_snapshot_semantics='Actual PR191 completion accepted:40completed/24published. Original-head merge, exact credited DOI and own tracker accepted; receipt recorded. Cursor192 authorizes only the separate next status-only intake. No intake performed; broader goal remains active.')
 require(all(case[k]==v for k,v in protected.items()),'Scientific case projection changed')
 work.update(UTC=stamp,status='ACTUAL_FACTUAL_MAIN_COMPLETION_ACCEPTED',actual_factual_acceptance_receipt=receipt,actual_factual_commit=a['factual_commit'],actual_factual_acceptance_UTC=a['UTC'])
 out[c.CASE+'CURRENT_CASE_STATUS.json']=json_bytes(case);out[c.CASE+'WORKFLOW_COMPLETION.json']=json_bytes(work);out[c.PREFIX+'CURRENT_PROGRESS.json']=json_bytes(prog)
 for n in [c.CASE+'RESEARCH_LOG.md',c.PREFIX+'CURRENT_PROGRESS.md',c.PREFIX+'RESEARCH_LOG.md']:out[n]=h.body_at(n,parent)+note.encode()
 return out

def message(a,digest):return 'Record actual PR191 factual completion receipt and40/24; separate status-only cursor192\n\n'+DOI+'; factual commit '+a['factual_commit']+'\nPR191 completion-checkpoint selected-map SHA256: '+digest

def verify_candidate(c,h,r,selected,a):
 co=h.api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==[r['expected_main']],'Checkpoint true parent/tree differs')
 parent=h.api('git/commits/'+r['expected_main'])['tree']['sha'];require(parent==r['parent_tree'],'Checkpoint parent tree differs')
 require(r['selected_files']==selected and r['selected_map_sha256']==c.selected_digest(selected) and co['message']==message(a,r['selected_map_sha256']),'Checkpoint exact selected map/message differs')
 h.m.m.h.warm_selected_directories([parent,r['tree']],selected)
 for n,x in selected.items():require(h.lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Prepared checkpoint selected identity changed '+n)
 changed={n for n,x in selected.items() if h.lookup(parent,n)!=('100644','blob',x['git_blob'])}
 require(changed==set(r['changed_paths'])==h.changed_leaves(parent,r['tree']) and changed<=set(r['overlay_paths']),'Checkpoint full-tree foreign/undeclared delta')

def prepare(c,gen):
 require(re.fullmatch('[a-z0-9_]{1,48}',gen),'Use a fresh lowercase generation');g,z,tr,h,m,f,a,combined,parent=context(c,True)
 dest=D/('checkpoint_'+gen);dest.mkdir(exist_ok=False);stamp=c.now();overlay=source_files(c);overlay.update(postimages(c,h,parent,stamp,a,z,tr));mutable={c.CASE+n for n in MUTABLE}|{c.PREFIX+n for n in PROGRAMME}
 for n,b in overlay.items():
  require(not n.startswith(c.NATIVE) and n!='unsolved_math_prioritization/QUEUE.md','Native/science/QUEUE overlay forbidden')
  if n in combined and n not in mutable:require(c.byte_pin(b)==combined[n],'Nonfactual selected source changed '+n)
 selected={**combined,**{n:c.byte_pin(b) for n,b in overlay.items()}};pt=h.api('git/commits/'+parent)['tree']['sha'];entries=[{'path':n,'mode':'100644','type':'blob','content':b.decode()} for n,b in sorted(overlay.items())]
 tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries});digest=c.selected_digest(selected);co=h.api('git/commits','POST',{'message':message(a,digest),'tree':tree['sha'],'parents':[parent]})
 h.m.m.h.warm_selected_directories([pt,tree['sha']],selected);changed=sorted(n for n,x in selected.items() if h.lookup(pt,n)!=('100644','blob',x['git_blob']))
 r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree['sha'],'commit':co['sha'],'selected_files':selected,'selected_map_sha256':digest,'changed_paths':changed,'overlay_paths':sorted(overlay),'factual_receipt':pin(A/FINAL),'factual_preparation':pin(A/'FINAL_FACTUAL_PREPARATION.json'),'original_preparation':pin(A/'SCOPED_MERGE_PREPARATION.json'),'MAIN_moved':False}
 fresh(dest/'CHECKPOINT_PREPARATION.json',json_bytes(r));verify_candidate(c,h,r,selected,a);require(h.api('git/ref/heads/main')['object']['sha']==parent,'MAIN advanced; preserve this generation and prepare a new one')
 print(json.dumps({'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected':len(selected),'changed':len(changed),'MAIN_moved':False}))

def accept(c,gen):
 require(re.fullmatch('[a-z0-9_]{1,48}',gen),'Unsafe generation');dest=D/('checkpoint_'+gen);r=read(dest/'CHECKPOINT_PREPARATION.json');g,z,tr,h,m,f,a,combined,main=context(c,False)
 require(r['factual_receipt']==pin(A/FINAL) and r['factual_preparation']==pin(A/'FINAL_FACTUAL_PREPARATION.json') and r['original_preparation']==pin(A/'SCOPED_MERGE_PREPARATION.json'),'Factual source receipt changed')
 c.selected_current(h,r['expected_main'],combined,f['tree']);overlay=source_files(c);overlay.update(postimages(c,h,r['expected_main'],r['UTC'],a,z,tr));selected={**combined,**{n:c.byte_pin(b) for n,b in overlay.items()}}
 require(r['overlay_paths']==sorted(overlay),'Checkpoint overlay scope changed');verify_candidate(c,h,r,selected,a);require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Receipt checkpoint is not on current MAIN');actual_tree=c.selected_current(h,main,selected,r['tree']);core_readbacks(c,h,g,main,selected)
 for n,b in overlay.items():require(h.body_at(n,main)==b,'Fresh completion/receipt body differs '+n)
 out={'UTC':c.now(),'PR':191,'status':'ACTUAL_PR191_FINAL_RECEIPT_CHECKPOINT_PARENT_FULL_DELTA_CURRENT_IDENTITIES_ACCEPTED','checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':actual_tree,'selected_files':len(selected),'every_selected_identity_checked_at_actual_observed_MAIN':True,'fully_completed_count':40,'published_count':24,'next_numeric_intake_cursor':192,'separate_status_only_intake_performed':False,'native100_QUEUE_scientific_bytes_unchanged':True,'goal_complete':False}
 fresh(dest/'CHECKPOINT_ACCEPTANCE.json',json_bytes(out));print(json.dumps(out))

if __name__=='__main__':
 require(sys.dont_write_bytecode,'Use Python -B');require(len(sys.argv)==3 and sys.argv[1] in ['prepare','accept'],'Usage: prepare_checkpoint.py prepare|accept fresh_generation');c=load();c.production_entrypoint(prepare if sys.argv[1]=='prepare' else accept,c,sys.argv[2])

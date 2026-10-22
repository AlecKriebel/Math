#!/usr/bin/env python3
"""Actual finalize/local reconciliation compiled at actual outer optimization.
All upstream publication/review/service boundaries are explicit inert fixtures.
Local JSON reads, validation, atomic writes/rename/fsync and retries are real.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,contextlib,copy,hashlib,io,json,os,stat,tempfile
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];CORE=P/'accept_pr952.py';BASE_SHA='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,m):
 if not ok:raise RuntimeError(m)
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
p=argparse.ArgumentParser();p.add_argument('--proposal-sha256',required=True);a=p.parse_args();base=(OWN/'BASE_accept_pr952.py').read_bytes();proposal=(OWN/'PROPOSED_accept_pr952.py').read_bytes()
need(sha(base)==BASE_SHA and sha(CORE.read_bytes())==BASE_SHA and sha(proposal)==a.proposal_sha256,'external/current source pins')
EVENTS=[];(OWN/'private_tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='finalize-',dir=OWN/'private_tmp') as td:
 root=Path(td);pr=root/'operations';audit=root/'audit';workflow=root/'workflow'
 for path in [pr,audit,workflow]:path.mkdir()
 for path in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']:path.write_text('UNRELATED LOG\n')
 cfg={};calls=[];n={};accepted={};freeze={};tracker={};native={};publication={};merge={}
 def rd(name):return json.loads((pr/name).read_bytes())
 def wr(name,value): (pr/name).write_bytes(enc(value))
 class PartialStream:
  def __init__(self,stream):self.stream=stream
  def __getattr__(self,name):return getattr(self.stream,name)
  def __enter__(self):self.stream.__enter__();return self
  def __exit__(self,*args):return self.stream.__exit__(*args)
  def write(self,data):
   self.stream.write(data[:max(1,len(data)//2)]);self.stream.flush();check('partial_temp_write')
   raise RuntimeError('partial-write injection did not fire')
 class OSProxy:
  def fdopen(self,*args,**kwargs):
   stream=os.fdopen(*args,**kwargs)
   return PartialStream(stream) if cfg.get('armed') and cfg.get('phase')=='partial_temp_write' and cfg.get('role')==cfg.get('active_role') else stream
  def __getattr__(self,name):return getattr(os,name)
  def fsync(self,fd):
   kind='directory' if stat.S_ISDIR(os.fstat(fd).st_mode) else 'file'
   check('before_'+kind+'_fsync');os.fsync(fd);check('after_'+kind+'_fsync')
  def replace(self,*args,**kwargs):
   check('before_replace');os.replace(*args,**kwargs);check('after_replace')
 def check(phase):
  if cfg.get('armed') and cfg.get('phase')==phase and cfg.get('role')==cfg.get('active_role'):
   cfg['armed']=False;raise RuntimeError('INERT_INTERRUPTION_'+cfg['role']+'_'+phase)
 def proof(name,result):
  def fn(*args,**kwargs):
   calls.append(name)
   if cfg.get('bad_boundary')==name:raise RuntimeError('INERT_REJECT_'+name)
   if name=='accepted_review_check' and cfg.get('concurrent_change'):
    which=cfg.pop('concurrent_change');value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)
   return copy.deepcopy(result)
  return fn
 def setup(body=proposal):
  global n,accepted,freeze,tracker,native,publication,merge
  for path in workflow.iterdir():
   if path.is_file():path.unlink()
  cfg.clear();calls.clear();n={'__name__':'_inert_actual_finalization_','__file__':str(CORE)}
  filename=OWN/('BASE_accept_pr952.py' if sha(body)==BASE_SHA else 'PROPOSED_accept_pr952.py')
  exec(compile(body,str(filename),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
  n.update(ROOT=root,P=pr,A=audit,W=workflow);n['utc_now']=lambda:cfg.get('now','2026-10-16T00:00:00+00:00')
  accepted={'freeze_sha256':'f'*64,'full_package_reviews':[{'manifest_sha256':'c'*64},{'manifest_sha256':'d'*64}]};freeze={'files':{}}
  tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['problem','','https://doi.org/10.5281/zenodo.17','fixture']};native={'commit':'e'*40}
  publication={'id':17,'doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'};merge={'mergeCommit':{'oid':'b'*40}}
  for name,value in [('TRACKER_RECEIPT.json',tracker),('NATIVE_PUBLICATION_RECEIPT.json',native)]:n['save'](workflow/name,value)
  n['accepted_package']=proof('accepted_package',(accepted,freeze));n['merged_gate']=proof('merged_gate',{'confirmed':True});n['publication_links']=proof('publication_links',(publication,merge));n['descriptor_check']=proof('descriptor_check',({},['exacttwofiles']));n['independent_public_verify']=proof('independent_public_verify',{'confirmed':True});n['native_verify']=proof('native_verify',{'confirmed':True});n['accepted_review_check']=proof('accepted_review_check',None);n['finalize_pr_metadata']=proof('finalize_pr_metadata_ALREADY_CORRECT_NO_EDIT',None)
  def gws(args):
   calls.append('gws_GET_ONLY');need(args[:4]==['sheets','spreadsheets','values','get'],'non-GET GWS action attempted');return {'range':tracker['updated_range'],'values':[tracker['row']]}
  n['gws']=gws
  n['gate_next']=proof('gate_next_METADATA_STATUS_ONLY',([{'pr':953,'action':'SKIP_STATUS_ONLY','math_source_read':False}],{'number':955,'problem_id':'later','headRefOid':'9'*40,'status':'claimed_solved','math_source_read':False}))
  def forbidden(*args,**kwargs):raise RuntimeError('FORBIDDEN REAL EXTERNAL ACTION')
  n['run']=forbidden;n['subprocess']=type('NoProcesses',(),{'run':staticmethod(forbidden)})
  target={'number':952,'headRefOid':n['HEAD'],'baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','entries':[{'id':n['KEY'],'original_note':'PRESERVE'}],'disposition':'pending_audit','target_custom':'PRESERVE'}
  inv=[{'number':904,'disposition':'accepted_merged_preprint_published','doi':'old','custom':'OLD OUTCOME'},target,{'number':955,'headRefOid':'9'*40,'entries':[{'id':'later'}],'custom':'LATER ITEM'}]
  state={'utc':'2026-10-15T00:00:00+00:00','eligible_prs':[904,952,955],'completed_prs':[904],'published_prs':[904],'completed_results':[{'pr':904,'outcome':'accepted_merged_preprint_published','doi':'old','custom':'OLD RECORD'}],'active_pr':952,'active_problem_id':n['KEY'],'next_pr':952,'active_original_head':n['HEAD'],'phase':'target952','active_pr_completion_estimate_percent':50,'shard_completion_estimate_percent':1/3*100,'custom':{'meaning':['KEEP',1]},'checkpoint':'PRESERVE'}
  wr('inventory.json',inv);wr('CURRENT_STATE.json',state)
  if 'local_atomic_json' in n:
   actual=n['local_atomic_json'];n['os']=OSProxy()
   def atomic(path,value,pin):
    cfg['active_role']='state' if path.name=='CURRENT_STATE.json' else 'inventory'
    try:
     check('before_call');result=actual(path,value,pin);check('after_call');return result
    finally:cfg.pop('active_role',None)
   n['local_atomic_json']=atomic
  return copy.deepcopy(state),copy.deepcopy(inv)
 def call():
  with contextlib.redirect_stdout(io.StringIO()):return n['finalize'](None,{'synthetic_authority':True})
 def consistent():
  state=rd('CURRENT_STATE.json');inventory=rd('inventory.json');matches=[x for x in state['completed_results'] if x['pr']==952];need(len(matches)==1 and state['completed_prs'].count(952)==1 and state['published_prs'].count(952)==1,'duplicate/missing local completion');item=[x for x in inventory if x['number']==952][0];record=matches[0]
  for ik,rk in [('doi','doi'),('tracker_range','tracker_range'),('merge_commit','merge_commit'),('native_ledger_commit','native_ledger_commit'),('accepted_freeze_sha256','accepted_freeze_sha256')]:need(item[ik]==record[rk],'local proof projection mismatch')
  need(item['disposition']==record['outcome'] and item['headRefOid']==n['HEAD'],'published inventory target outcome');return state,inventory
 # Independently reconstruct the reported legacy failure using the actual base.
 setup(base);actual_save=n['save']
 def fail_inventory(path,*args,**kwargs):
  if path==pr/'inventory.json' and cfg.get('armed'):
   cfg['armed']=False;raise RuntimeError('INERT_LEGACY_INVENTORY_SAVE_FAILURE')
  return actual_save(path,*args,**kwargs)
 n['save']=fail_inventory;cfg['armed']=True
 try:call()
 except RuntimeError as e:need(str(e)=='INERT_LEGACY_INVENTORY_SAVE_FAILURE','legacy failure not reached')
 else:raise RuntimeError('base did not interrupt')
 legacy_state=rd('CURRENT_STATE.json');legacy_inventory=rd('inventory.json');call()
 need(952 in rd('CURRENT_STATE.json')['completed_prs'] and rd('CURRENT_STATE.json')['active_pr']==955 and rd('inventory.json')[1]['disposition']=='pending_audit','base gap not reproduced')
 EVENTS.append({'test':'actual_base_retry_claims_complete_with_legacy_stale_inventory','status':'REPRODUCED_REQUIRED_GAP'})
 setup();wr('CURRENT_STATE.json',legacy_state);wr('inventory.json',legacy_inventory);before_state=(pr/'CURRENT_STATE.json').read_bytes();call();state,inv=consistent();need((pr/'CURRENT_STATE.json').read_bytes()==before_state and state['active_pr']==955,'legacy completed/later state regressed');EVENTS.append({'test':'legacy_state_complete_inventory_stale_repaired_only_inventory','status':'PASS'})
 # All meaningful boundaries of each real atomic local write and retry.
 for role in ['inventory','state']:
  for phase in ['before_call','after_call','partial_temp_write','before_file_fsync','after_file_fsync','before_replace','after_replace','before_directory_fsync','after_directory_fsync']:
   original_state,original_inv=setup();cfg.update(role=role,phase=phase,armed=True)
   try:call()
   except RuntimeError as e:need(str(e)=='INERT_INTERRUPTION_'+role+'_'+phase,'wrong boundary failure')
   else:raise RuntimeError('boundary not reached '+role+' '+phase)
   # Each target remains parseable; an interrupted temp write never truncates it.
   rd('CURRENT_STATE.json');rd('inventory.json');need(not list(pr.glob('.pr952-finalize-*.tmp')),'temporary atomic artifact leaked')
   cfg['now']='2026-10-16T00:10:00+00:00';call();state,inv=consistent()
   need(state['custom']==original_state['custom'] and state['checkpoint']==original_state['checkpoint'] and inv[0]==original_inv[0] and inv[2]==original_inv[2],'unrelated content changed')
   before=[(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']];calls.clear();call();need(before==[(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']],'consistent retry rewrote local state');need('gate_next_METADATA_STATUS_ONLY' not in calls,'completed retry restarted next gate')
   EVENTS.append({'test':'interrupted_'+role+'_'+phase+'_then_idempotent_retry','status':'PASS'})
 # Reverse window plus a genuinely later active program must not be regressed.
 setup();cfg.update(role='state',phase='before_call',armed=True)
 try:call()
 except RuntimeError:pass
 value=rd('CURRENT_STATE.json');value.update(active_pr=955,active_problem_id='later',next_pr=955,active_original_head='9'*40,phase='LATER_PHASE',priority_status={'later':'PRESERVE'},active_pr_completion_estimate_percent=71);wr('CURRENT_STATE.json',value);calls.clear();call();state,_=consistent()
 for key in ['active_pr','active_problem_id','next_pr','active_original_head','phase','priority_status','active_pr_completion_estimate_percent']:need(state[key]==value[key],'later active context regressed '+key)
 need('gate_next_METADATA_STATUS_ONLY' not in calls,'reverse recovery reselected later active program');EVENTS.append({'test':'inventory_first_reverse_window_preserves_later_active_context','status':'PASS'})
 setup();wr('CURRENT_STATE.json',legacy_state);wr('inventory.json',legacy_inventory);value=rd('CURRENT_STATE.json');value.update(active_pr=969,active_problem_id='newer',next_pr=969,phase='EVEN_LATER',active_original_head='8'*40);wr('CURRENT_STATE.json',value);before=(pr/'CURRENT_STATE.json').read_bytes();call();consistent();need((pr/'CURRENT_STATE.json').read_bytes()==before,'legacy repair regressed a still later state');EVENTS.append({'test':'legacy_complete_repair_preserves_even_later_active_state_bytes','status':'PASS'})
 # Legacy already-published inventory with only the original three fields is
 # upgraded from current independently verified authority, preserving its notes.
 setup();call();state,inv=consistent();item=inv[1]
 for key in ['merge_commit','native_ledger_commit','accepted_freeze_sha256','original_pr_head','problem_id','record_url']:item.pop(key)
 wr('inventory.json',inv);call();consistent();EVENTS.append({'test':'same_outcome_legacy_inventory_projection_upgrade','status':'PASS'})
 def reject(name,mutate,completed=False):
  setup()
  if completed:call()
  mutate();before=[(pr/f).read_bytes() for f in ['CURRENT_STATE.json','inventory.json']]
  try:call()
  except (RuntimeError,OSError,ValueError,TypeError,KeyError) as e:
   need(before==[(pr/f).read_bytes() for f in ['CURRENT_STATE.json','inventory.json']],'conflict case overwrote local data');EVENTS.append({'test':name,'status':'REJECTED_EXPECTED','guard':str(e)})
  else:raise RuntimeError('bad local finalization accepted '+name)
 def inv_mut(fn):
  inv=rd('inventory.json');fn(inv);wr('inventory.json',inv)
 def state_mut(fn):
  value=rd('CURRENT_STATE.json');fn(value);wr('CURRENT_STATE.json',value)
 for key,bad in [('headRefOid','1'*40),('baseRefName','other'),('url','https://github.com/other/repo/pull/952'),('disposition','rejected'),('disposition',None),('doi','10.5281/zenodo.99'),('merge_commit','1'*40),('native_ledger_commit','1'*40),('accepted_freeze_sha256','1'*64),('tracker_range',"'Math Puzzles'!A3:D3"),('problem_id','wrong')]:reject('inventory_conflicting_'+key+'_'+str(bad),lambda k=key,v=bad:inv_mut(lambda inv:inv[1].update({k:v})))
 reject('duplicate_inventory_target',lambda:inv_mut(lambda inv:inv.append(copy.deepcopy(inv[1]))))
 reject('missing_inventory_target',lambda:inv_mut(lambda inv:inv.pop(1)))
 reject('inventory_number_wrong_type',lambda:inv_mut(lambda inv:inv[1].update(number='952')))
 reject('inventory_problem_wrong_type',lambda:inv_mut(lambda inv:inv[1]['entries'][0].update(id=10400145)))
 reject('inventory_problem_extra_entry',lambda:inv_mut(lambda inv:inv[1]['entries'].append({'id':'other'})))
 reject('duplicate_completed_record',lambda:state_mut(lambda state:state['completed_results'].append(copy.deepcopy(state['completed_results'][-1]))),True)
 for key,bad in [('doi','wrong'),('merge_commit','1'*40),('native_ledger_commit','1'*40),('accepted_freeze_sha256','1'*64),('original_pr_head','1'*40)]:reject('completed_record_conflicting_'+key,lambda k=key,v=bad:state_mut(lambda state:state['completed_results'][-1].update({k:v})),True)
 reject('completed_pr_list_bool',lambda:state_mut(lambda state:state['completed_prs'].append(True)))
 reject('state_inconsistent_completed_ids',lambda:state_mut(lambda state:state['completed_prs'].append(952)))
 reject('state_inconsistent_published_ids',lambda:state_mut(lambda state:state['published_prs'].append(952)))
 reject('state_earlier_active_program',lambda:state_mut(lambda state:state.update(active_pr=940)))
 reject('state_active_bool',lambda:state_mut(lambda state:state.update(active_pr=True)))
 reject('accepted_whole_review_boundary_remains_required',lambda:cfg.update(bad_boundary='accepted_review_check'))
 # Compare-and-replan preserves a later write rather than replaying stale data.
 for which in ['CURRENT_STATE.json','inventory.json']:
  setup();cfg['concurrent_change']=which
  try:call()
  except RuntimeError as e:need('fingerprint' in str(e) or 'changed' in str(e) or 'nonregular or oversized file:' in str(e),'changed-input guard not reached')
  else:raise RuntimeError('stale observed input accepted')
  call();state,inv=consistent();need((state if which=='CURRENT_STATE.json' else inv[-1])['concurrent_marker']=='PRESERVE NEW WRITER','concurrent unrelated content lost');EVENTS.append({'test':'changed_input_rejected_then_fresh_merge_'+which,'status':'PASS'})
print(json.dumps({'schema':'pr952-proposed-finalization-recovery-controls-v1','utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_PROPOSAL_ONLY_NO_INSTALL_OR_REVIEW_CREDIT','base_sha256':BASE_SHA,'proposal_sha256':a.proposal_sha256,'outer_optimization':sys.flags.optimize,'core_compile_optimization':sys.flags.optimize,'event_count':len(EVENTS),'events':EVENTS,'actual_functions':['finalize','local_final_record','local_final_inventory','local_final_state','local_atomic_json','reconcile_local_finalization','save','read_regular'],'explicit_inert_upstream_trust_boundaries':['accepted_package','merged_gate','publication_links','descriptor_check','independent_public_verify','native_verify','accepted_review_check','finalize_pr_metadata_already_correct','gws_GET','gate_next_metadata_status_only'],'remote_merge_create_publish_append_push_or_PR_metadata_actions':0,'real_Git_or_service_calls':0,'current_adapter_state_inventory_workflow_edits':0,'accepted':False,'fresh_full_review_credit':False},sort_keys=True))

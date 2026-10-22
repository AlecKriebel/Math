#!/usr/bin/env python3
"""Actual finalize/local reconciliation compiled at actual outer optimization.
All upstream publication/review/service boundaries are explicit inert fixtures.
Local JSON/log byte reads, validation, atomic writes/rename/fsync and retries are real.
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
historical=(OWN/'HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py').read_bytes();need(sha(historical)=='07d1088bcbf8a81c71f15f5f096fcced98e4638244eb794df7efffcd0783688b','historical preinstall counterexample pin')
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
 class ShortStream(PartialStream):
  def write(self,data):return self.stream.write(data[:max(1,len(data)//2)])
 class OSProxy:
  def fdopen(self,*args,**kwargs):
   stream=os.fdopen(*args,**kwargs)
   if cfg.get('armed') and cfg.get('role')==cfg.get('active_role'):
    if cfg.get('phase')=='partial_temp_write':return PartialStream(stream)
    if cfg.get('phase')=='short_temp_write':cfg['armed']=False;return ShortStream(stream)
   return stream
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
   if name=='accepted_review_check' and cfg.get('interrupt_after_logs') and all(b'PR952-LOCAL-COMPLETION-V1 ' in p.read_bytes() for p in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']):
    cfg['interrupt_after_logs']=False;raise RuntimeError('INERT_AFTER_LOG_READBACK_BEFORE_CANONICAL_SUCCESS')
   if name=='accepted_review_check' and cfg.get('concurrent_change'):
    which=cfg.pop('concurrent_change');value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)
   return copy.deepcopy(result)
  return fn
 def setup(body=proposal):
  global n,accepted,freeze,tracker,native,publication,merge
  for path in workflow.iterdir():
   if path.is_file():path.unlink()
  for path in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']:path.write_bytes(b'UNRELATED LOG\n')
  cfg.clear();calls.clear();n={'__name__':'_inert_actual_finalization_','__file__':str(CORE)}
  filename=OWN/('BASE_accept_pr952.py' if sha(body)==BASE_SHA else 'HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py' if body==historical else 'PROPOSED_accept_pr952.py')
  exec(compile(body,str(filename),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
  n.update(ROOT=root,P=pr,A=audit,W=workflow);n['utc_now']=lambda:cfg.get('now',datetime.now(timezone.utc).isoformat())
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
  def role_for(path):
   return 'state' if path==pr/'CURRENT_STATE.json' else 'inventory' if path==pr/'inventory.json' else 'project_log' if path==pr/'RESEARCH_LOG.md' else 'audit_log' if path==audit/'RESEARCH_LOG.md' else 'OTHER'
  if 'local_atomic_bytes' in n or 'local_atomic_json' in n:
   helper='local_atomic_bytes' if 'local_atomic_bytes' in n else 'local_atomic_json';actual=n[helper];n['os']=OSProxy()
   def atomic(path,value,pin):
    cfg['active_role']=role_for(path)
    try:
     check('before_call');result=actual(path,value,pin);check('after_call');return result
    finally:cfg.pop('active_role',None)
   n[helper]=atomic
   actual_save=n['save']
   def saving(path,value,*args,**kwargs):
    if path!=workflow/'LOCAL_FINALIZATION_RECEIPT.json':return actual_save(path,value,*args,**kwargs)
    cfg['active_role']='receipt_confirmed' if value.get('confirmed') is True else 'receipt_progress'
    try:
     check('before_call');result=actual_save(path,value,*args,**kwargs);check('after_call');return result
    finally:cfg.pop('active_role',None)
   n['save']=saving
  return copy.deepcopy(state),copy.deepcopy(inv)
 def call():
  with contextlib.redirect_stdout(io.StringIO()):return n['finalize'](None,{'synthetic_authority':True})
 def consistent():
  state=rd('CURRENT_STATE.json');inventory=rd('inventory.json');matches=[x for x in state['completed_results'] if x['pr']==952];need(len(matches)==1 and state['completed_prs'].count(952)==1 and state['published_prs'].count(952)==1,'duplicate/missing local completion');item=[x for x in inventory if x['number']==952][0];record=matches[0]
  for ik,rk in [('doi','doi'),('tracker_range','tracker_range'),('merge_commit','merge_commit'),('native_ledger_commit','native_ledger_commit'),('accepted_freeze_sha256','accepted_freeze_sha256')]:need(item[ik]==record[rk],'local proof projection mismatch')
  need(item['disposition']==record['outcome'] and item['headRefOid']==n['HEAD'],'published inventory target outcome');return state,inventory
 def required_raw():return [path.read_bytes() for path in [pr/'CURRENT_STATE.json',pr/'inventory.json',pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']]
 def logs_consistent():
  record=rd('CURRENT_STATE.json')['completed_results'][-1]
  for path in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']:
   raw=path.read_bytes();desired,marker=n['local_final_log'](raw,record);need(desired==raw and raw.count(b'PR952-LOCAL-COMPLETION-V1 ')==1,'required independent log marker missing/duplicate');need(marker['workflow_completion_estimate_percent']==100,'completion percentage')
  receipt=json.loads((workflow/'LOCAL_FINALIZATION_RECEIPT.json').read_bytes());need(receipt['confirmed'] is True and receipt['both_research_logs_confirmed'] is True,'canonical success before both logs')
  for role,path in [('project_log',pr/'RESEARCH_LOG.md'),('audit_log',audit/'RESEARCH_LOG.md')]:need(receipt['after'][role]==n['fingerprint'](path.read_bytes()),'canonical log pin mismatch')
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
 # Reconstruct the parent preinstall counterexample independently with actual
 # authenticated old proposal finalize/reconcile and owned real filesystem.
 setup(historical);real_reconcile=n['reconcile_local_finalization']
 def interrupted_old_return(*args,**kwargs):
  result=real_reconcile(*args,**kwargs)
  if cfg.get('cut_return'):cfg['cut_return']=False;raise RuntimeError('INERT_OLD_AFTER_RECONCILE_RETURN')
  return result
 n['reconcile_local_finalization']=interrupted_old_return;cfg['cut_return']=True
 try:call()
 except RuntimeError as e:need(str(e)=='INERT_OLD_AFTER_RECONCILE_RETURN','historical gap boundary')
 else:raise RuntimeError('historical proposal failed to interrupt')
 old_state=rd('CURRENT_STATE.json');old_inventory=rd('inventory.json');old_record=json.loads((workflow/'PUBLICATION_RECORD.json').read_bytes());old_receipt=json.loads((workflow/'LOCAL_FINALIZATION_RECEIPT.json').read_bytes());call()
 need(all(path.read_bytes()==b'UNRELATED LOG\n' for path in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']) and old_receipt['confirmed'] is True,'historical omitted-log gap not reproduced')
 EVENTS.append({'test':'actual_authenticated_old_proposal_returns_success_with_both_logs_missing','status':'REPRODUCED_EXISTING_REQUIRED_FINDING_CLARIFICATION'})
 setup();wr('CURRENT_STATE.json',old_state);wr('inventory.json',old_inventory);n['save'](workflow/'PUBLICATION_RECORD.json',old_record);n['save'](workflow/'LOCAL_FINALIZATION_RECEIPT.json',old_receipt);before=required_raw()[:2];call();consistent();logs_consistent();need(required_raw()[:2]==before,'legacy confirmed-receipt log repair rewrote state/inventory');EVENTS.append({'test':'legacy_state_inventory_receipt_complete_both_logs_missing_repaired','status':'PASS'})
 # All meaningful boundaries of each real atomic local write and retry.
 for role in ['inventory','state','project_log','audit_log']:
  for phase in ['before_call','after_call','partial_temp_write','short_temp_write','before_file_fsync','after_file_fsync','before_replace','after_replace','before_directory_fsync','after_directory_fsync']:
   original_state,original_inv=setup();cfg.update(role=role,phase=phase,armed=True)
   try:call()
   except RuntimeError as e:need(str(e)==('local temporary short write' if phase=='short_temp_write' else 'INERT_INTERRUPTION_'+role+'_'+phase),'wrong boundary failure '+str(e))
   else:raise RuntimeError('boundary not reached '+role+' '+phase)
   # Each target remains parseable; an interrupted temp write never truncates it.
   rd('CURRENT_STATE.json');rd('inventory.json');need(not list(pr.glob('.pr952-finalize-*.tmp')) and not list(audit.glob('.pr952-finalize-*.tmp')),'temporary atomic artifact leaked')
   cfg['now']=datetime.now(timezone.utc).isoformat();call();state,inv=consistent();logs_consistent()
   need(state['custom']==original_state['custom'] and state['checkpoint']==original_state['checkpoint'] and inv[0]==original_inv[0] and inv[2]==original_inv[2],'unrelated content changed')
   before=required_raw();calls.clear();call();need(before==required_raw(),'consistent retry rewrote local state');need('gate_next_METADATA_STATUS_ONLY' not in calls,'completed retry restarted next gate')
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
 # Every canonical receipt save boundary is retryable. These receipts use
 # existing save (not rename); interrupted JSON may be partial, never trusted.
 for role in ['receipt_progress','receipt_confirmed']:
  for phase in ['before_call','after_call','partial_temp_write','before_file_fsync','after_file_fsync','before_directory_fsync','after_directory_fsync']:
   setup();cfg.update(role=role,phase=phase,armed=True)
   try:call()
   except RuntimeError as e:need(str(e)=='INERT_INTERRUPTION_'+role+'_'+phase,'receipt boundary '+str(e))
   else:raise RuntimeError('receipt interruption not reached')
   if role=='receipt_confirmed':need(all(b'PR952-LOCAL-COMPLETION-V1 ' in p.read_bytes() for p in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']),'confirmed save attempted before both logs')
   call();consistent();logs_consistent();before=required_raw();call();need(required_raw()==before,'receipt retry duplicated local outcomes');EVENTS.append({'test':'interrupted_'+role+'_'+phase+'_then_complete_retry','status':'PASS'})
 # Failure after both log readbacks but before canonical success leaves explicit
 # in-progress state; next actual finalize must independently confirm both logs.
 setup();cfg['interrupt_after_logs']=True
 try:call()
 except RuntimeError as e:need(str(e)=='INERT_AFTER_LOG_READBACK_BEFORE_CANONICAL_SUCCESS','after logs boundary')
 else:raise RuntimeError('missing after-logs interruption')
 need(json.loads((workflow/'LOCAL_FINALIZATION_RECEIPT.json').read_bytes())['confirmed'] is False,'early canonical success');before=required_raw();call();logs_consistent();need(before==required_raw(),'already-written logs duplicated');EVENTS.append({'test':'both_logs_written_before_confirmed_receipt_retry','status':'PASS'})
 # Failure after reconcile returns (the exact former omitted-log window) is safe.
 setup();real=n['reconcile_local_finalization']
 def interrupt_return(*args,**kwargs):
  result=real(*args,**kwargs)
  if cfg.get('cut_return'):cfg['cut_return']=False;raise RuntimeError('INERT_AFTER_ALL_REQUIRED_LOCAL_COMPLETION')
  return result
 n['reconcile_local_finalization']=interrupt_return;cfg['cut_return']=True
 try:call()
 except RuntimeError as e:need(str(e)=='INERT_AFTER_ALL_REQUIRED_LOCAL_COMPLETION','new after return boundary')
 else:raise RuntimeError('new return interruption missing')
 logs_consistent();before=required_raw();call();need(before==required_raw(),'post-return retry changed local outcomes');EVENTS.append({'test':'interruption_after_complete_reconcile_return_is_idempotent','status':'PASS'})
 # Each required log is checked independently on an already-completed outcome.
 for present in [(),('project',),('audit',),('project','audit')]:
  setup();call();state,inv=consistent();value=copy.deepcopy(state);value.update(active_pr=969,active_problem_id='later969',next_pr=969,phase='LATER_RESEARCH',priority_status={'do':'PRESERVE'},active_pr_completion_estimate_percent=83);wr('CURRENT_STATE.json',value)
  for role,path in [('project',pr/'RESEARCH_LOG.md'),('audit',audit/'RESEARCH_LOG.md')]:
   if role not in present:path.write_bytes(b'UNRELATED NONUTF8 \xff\r\nNO TRAILING NEWLINE')
  before=required_raw();record=json.loads((workflow/'PUBLICATION_RECORD.json').read_bytes());cfg['now']=datetime.now(timezone.utc).isoformat();call();logs_consistent();need(required_raw()[:2]==before[:2],'later active state/inventory changed during log-only repair')
  for i,(role,path) in enumerate([('project',pr/'RESEARCH_LOG.md'),('audit',audit/'RESEARCH_LOG.md')],start=2):
   raw=path.read_bytes();marker=n['local_final_log'](raw,record)[1]
   if role in present:need(raw==before[i],'existing same-outcome marker rewritten/backdated')
   else:need(raw.startswith(before[i]+b'\n') and marker['reconciled_utc']==cfg['now'] and marker['reconciled_utc']!=record['utc'],'missing log did not retain raw prefix/actual repair timestamp')
  calls.clear();before=required_raw();call();need(before==required_raw() and 'gate_next_METADATA_STATUS_ONLY' not in calls,'repeated log repair duplicated output/restarted next program');EVENTS.append({'test':'independent_log_repair_with_later_active_and_existing_'+('_'.join(present) or 'none'),'status':'PASS'})
 # Existing unmarked historical publication narrative is preserved; the new
 # entry explicitly records reconciliation and never rewrites publication time.
 setup();call();before=b'OLD UNMARKED PR952 PUBLICATION MILESTONE\r\nUNRELATED \xfe';(pr/'RESEARCH_LOG.md').write_bytes(before);call();logs_consistent();need((pr/'RESEARCH_LOG.md').read_bytes().startswith(before+b'\n'),'legacy log narrative changed');EVENTS.append({'test':'legacy_unmarked_milestone_and_nonutf8_bytes_preserved','status':'PASS'})
 def reject_log(name,mutator,role='project'):
  setup();call();path=(pr if role=='project' else audit)/'RESEARCH_LOG.md';raw=path.read_bytes();path.write_bytes(mutator(raw));before=required_raw()
  try:call()
  except (RuntimeError,OSError,ValueError,TypeError,KeyError) as e:need(before==required_raw(),'bad log overwrote local outcome');EVENTS.append({'test':name,'status':'REJECTED_EXPECTED','guard':str(e)})
  else:raise RuntimeError('malformed/conflicting marker accepted '+name)
 prefix=b'PR952-LOCAL-COMPLETION-V1 '
 def marker_mut(raw,fn):
  before,line=raw.split(prefix);marker=json.loads(line);fn(marker);return before+prefix+json.dumps(marker,sort_keys=True,separators=(',',':')).encode()+b'\n'
 for key,bad in [('doi','wrong'),('merge_commit','1'*40),('native_ledger_commit','1'*40),('accepted_freeze_sha256','1'*64),('original_pr_head','1'*40),('tracker_range','wrong'),('problem_id','wrong'),('clean_final_review_manifest_sha256','1'*64)]:reject_log('log_conflicting_'+key,lambda raw,k=key,v=bad:marker_mut(raw,lambda m:m['approved_outcome'].update({k:v})))
 for key,bad in [('reconciled_utc','2026-10-16T00:00:00'),('reconciled_utc',None),('workflow_completion_estimate_percent',True),('workflow_completion_estimate_percent',99),('schema','wrong'),('approved_sha256','1'*64),('approved_outcome',None)]:reject_log('log_malformed_'+key+'_'+str(bad),lambda raw,k=key,v=bad:marker_mut(raw,lambda m:m.update({k:v})),role='audit')
 reject_log('duplicate_same_outcome_markers',lambda raw:raw+raw[raw.index(prefix):])
 reject_log('truncated_marker_line',lambda raw:raw[:-7])
 reject_log('malformed_reserved_marker_framing',lambda raw:raw+b'PR952-LOCAL-COMPLETION BROKEN\n')
 reject_log('noncanonical_marker_json',lambda raw:raw.replace(b'{"approved_outcome"',b'{ "approved_outcome"'))
 reject_log('duplicate_marker_json_key',lambda raw:raw.replace(b'{"approved_outcome"',b'{"schema":"pr952-local-completion-v1","approved_outcome"'))
 # Log mode and symlink checks use actual nofollow regular-file boundaries.
 for role in ['project','audit']:
  setup();path=(pr if role=='project' else audit)/'RESEARCH_LOG.md';path.chmod(0o640);before=required_raw()
  try:call()
  except RuntimeError as e:need('mode' in str(e),'wrong unsupported-mode guard')
  else:raise RuntimeError('unsupported mode accepted')
  path.chmod(0o644);call();logs_consistent();EVENTS.append({'test':'log_unsupported_mode_rejected_then_repaired_'+role,'status':'PASS'})
 # Completion record and all four final bytes remain stable after repeated calls.
 setup();call();consistent();logs_consistent();before=required_raw();calls.clear();call();need(before==required_raw(),'completed outcome not byte-idempotent');need(all(name in ['accepted_package','merged_gate','publication_links','descriptor_check','independent_public_verify','native_verify','accepted_review_check','finalize_pr_metadata_ALREADY_CORRECT_NO_EDIT','gws_GET_ONLY'] for name in calls),'unexpected retry boundary/action');EVENTS.append({'test':'success_requires_four_exact_local_files_no_remote_mutation_retry','status':'PASS'})
print(json.dumps({'schema':'pr952-proposed-finalization-and-logs-recovery-controls-v2','utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_PROPOSAL_ONLY_NO_INSTALL_OR_REVIEW_CREDIT','base_sha256':BASE_SHA,'proposal_sha256':a.proposal_sha256,'outer_optimization':sys.flags.optimize,'core_compile_optimization':sys.flags.optimize,'event_count':len(EVENTS),'events':EVENTS,'actual_functions':['finalize','local_final_record','local_final_inventory','local_final_state','local_atomic_json','local_atomic_bytes','local_final_log','reconcile_local_finalization','save','read_regular'],'explicit_inert_upstream_trust_boundaries':['accepted_package','merged_gate','publication_links','descriptor_check','independent_public_verify','native_verify','accepted_review_check','finalize_pr_metadata_already_correct','gws_GET','gate_next_metadata_status_only'],'remote_merge_create_publish_append_push_or_PR_metadata_actions':0,'real_Git_or_service_calls':0,'current_adapter_state_inventory_workflow_edits':0,'accepted':False,'fresh_full_review_credit':False},sort_keys=True))

from pathlib import Path
OWN=Path(__file__).resolve().parent
s=(OWN/'test_finalization_recovery.py').read_text()
s=s.replace('Local JSON reads, validation, atomic writes/rename/fsync and retries are real.','Local JSON/log byte reads, validation, atomic writes/rename/fsync and retries are real.')
s=s.replace("p.add_argument('--proposal-sha256',required=True);a=p.parse_args();base=", "p.add_argument('--proposal-sha256',required=True);p.add_argument('--installed',action='store_true');a=p.parse_args();base=")
s=s.replace("proposal=(OWN/'PROPOSED_accept_pr952.py').read_bytes()", "proposal_copy=(OWN/'PROPOSED_accept_pr952.py').read_bytes();proposal=CORE.read_bytes() if a.installed else proposal_copy;need(proposal==proposal_copy,'installed/proposal exact source bytes')")
s=s.replace("sha(CORE.read_bytes())==BASE_SHA", "sha(CORE.read_bytes())==(a.proposal_sha256 if a.installed else BASE_SHA)")
s=s.replace("'current_adapter_state_inventory_workflow_edits':0", "'current_adapter_state_inventory_workflow_edits':0,'installed_actual_source_executed':a.installed")
s=s.replace("EVENTS=[];(OWN/'private_tmp')", "historical=(OWN/'HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py').read_bytes();need(sha(historical)=='07d1088bcbf8a81c71f15f5f096fcced98e4638244eb794df7efffcd0783688b','historical preinstall counterexample pin')\nEVENTS=[];(OWN/'private_tmp')")
s=s.replace(' class OSProxy:', ''' class ShortStream(PartialStream):
  def write(self,data):return self.stream.write(data[:max(1,len(data)//2)])
 class OSProxy:''')
s=s.replace("   return PartialStream(stream) if cfg.get('armed') and cfg.get('phase')=='partial_temp_write' and cfg.get('role')==cfg.get('active_role') else stream", "   if cfg.get('armed') and cfg.get('role')==cfg.get('active_role'):\n    if cfg.get('phase')=='partial_temp_write':return PartialStream(stream)\n    if cfg.get('phase')=='short_temp_write':cfg['armed']=False;return ShortStream(stream)\n   return stream")
s=s.replace("   if name=='accepted_review_check' and cfg.get('concurrent_change'):","   if name=='accepted_review_check' and cfg.get('interrupt_after_logs') and all(b'PR952-LOCAL-COMPLETION-V1 ' in p.read_bytes() for p in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']):\n    cfg['interrupt_after_logs']=False;raise RuntimeError('INERT_AFTER_LOG_READBACK_BEFORE_CANONICAL_SUCCESS')\n   if name=='accepted_review_check' and cfg.get('concurrent_change'):")
s=s.replace("  cfg.clear();calls.clear();n=", "  for path in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']:path.write_bytes(b'UNRELATED LOG\\n')\n  cfg.clear();calls.clear();n=")
s=s.replace("filename=OWN/('BASE_accept_pr952.py' if sha(body)==BASE_SHA else 'PROPOSED_accept_pr952.py')", "filename=CORE if a.installed and body==proposal else OWN/('BASE_accept_pr952.py' if sha(body)==BASE_SHA else 'HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py' if body==historical else 'PROPOSED_accept_pr952.py')")
s=s.replace("n['utc_now']=lambda:cfg.get('now','2026-10-16T00:00:00+00:00')", "n['utc_now']=lambda:cfg.get('now',datetime.now(timezone.utc).isoformat())")
a=s.index("  if 'local_atomic_json' in n:");b=s.index('  return copy.deepcopy(state)',a)
s=s[:a]+'''  def role_for(path):
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
''' +s[b:]
s=s.replace("for role in ['inventory','state']:","for role in ['inventory','state','project_log','audit_log']:")
s=s.replace("['before_call','after_call','partial_temp_write','before_file_fsync'", "['before_call','after_call','partial_temp_write','short_temp_write','before_file_fsync'")
s=s.replace("need(str(e)=='INERT_INTERRUPTION_'+role+'_'+phase,'wrong boundary failure')", "need(str(e)==('PR952 guard: local temporary short write' if phase=='short_temp_write' else 'INERT_INTERRUPTION_'+role+'_'+phase),'wrong boundary failure '+str(e))")
s=s.replace("need(not list(pr.glob('.pr952-finalize-*.tmp')),'temporary atomic artifact leaked')", "need(not list(pr.glob('.pr952-finalize-*.tmp')) and not list(audit.glob('.pr952-finalize-*.tmp')),'temporary atomic artifact leaked')")
s=s.replace("cfg['now']='2026-10-16T00:10:00+00:00';call();state,inv=consistent()", "cfg['now']=datetime.now(timezone.utc).isoformat();call();state,inv=consistent();logs_consistent()")
s=s.replace("before=[(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']];calls.clear();call();need(before==[(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']]", "before=required_raw();calls.clear();call();need(before==required_raw()")
s=s.replace("which=cfg.pop('concurrent_change');value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)", "which=cfg.pop('concurrent_change')\n    if which in ('project_log','audit_log'):\n     path=(pr if which=='project_log' else audit)/'RESEARCH_LOG.md';path.write_bytes(path.read_bytes()+b'CONCURRENT UNRELATED BYTES\\n')\n    else:\n     value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)")
pos=s.index(' # Independently reconstruct')
s=s[:pos]+''' def required_raw():return [path.read_bytes() for path in [pr/'CURRENT_STATE.json',pr/'inventory.json',pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']]
 def logs_consistent():
  record=rd('CURRENT_STATE.json')['completed_results'][-1]
  for path in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']:
   raw=path.read_bytes();desired,marker=n['local_final_log'](raw,record);need(desired==raw and raw.count(b'PR952-LOCAL-COMPLETION-V1 ')==1,'required independent log marker missing/duplicate');need(marker['workflow_completion_estimate_percent']==100,'completion percentage')
  receipt=json.loads((workflow/'LOCAL_FINALIZATION_RECEIPT.json').read_bytes());need(receipt['confirmed'] is True and receipt['both_research_logs_confirmed'] is True,'canonical success before both logs')
  for role,path in [('project_log',pr/'RESEARCH_LOG.md'),('audit_log',audit/'RESEARCH_LOG.md')]:need(receipt['after'][role]==n['fingerprint'](path.read_bytes()),'canonical log pin mismatch')
''' +s[pos:]
pos=s.index(' # All meaningful boundaries')
s=s[:pos]+''' # Reconstruct the parent preinstall counterexample independently with actual
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
 need(all(path.read_bytes()==b'UNRELATED LOG\\n' for path in [pr/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']) and old_receipt['confirmed'] is True,'historical omitted-log gap not reproduced')
 EVENTS.append({'test':'actual_authenticated_old_proposal_returns_success_with_both_logs_missing','status':'REPRODUCED_EXISTING_REQUIRED_FINDING_CLARIFICATION'})
 setup();wr('CURRENT_STATE.json',old_state);wr('inventory.json',old_inventory);n['save'](workflow/'PUBLICATION_RECORD.json',old_record);n['save'](workflow/'LOCAL_FINALIZATION_RECEIPT.json',old_receipt);before=required_raw()[:2];call();consistent();logs_consistent();need(required_raw()[:2]==before,'legacy confirmed-receipt log repair rewrote state/inventory');EVENTS.append({'test':'legacy_state_inventory_receipt_complete_both_logs_missing_repaired','status':'PASS'})
''' +s[pos:]
pos=s.index("print(json.dumps(")
extra=''' # Every canonical receipt save boundary is retryable. These receipts use
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
   if role not in present:path.write_bytes(b'UNRELATED NONUTF8 \\xff\\r\\nNO TRAILING NEWLINE')
  before=required_raw();record=json.loads((workflow/'PUBLICATION_RECORD.json').read_bytes());cfg['now']=datetime.now(timezone.utc).isoformat();call();logs_consistent();need(required_raw()[:2]==before[:2],'later active state/inventory changed during log-only repair')
  for i,(role,path) in enumerate([('project',pr/'RESEARCH_LOG.md'),('audit',audit/'RESEARCH_LOG.md')],start=2):
   raw=path.read_bytes();marker=n['local_final_log'](raw,record)[1]
   if role in present:need(raw==before[i],'existing same-outcome marker rewritten/backdated')
   else:need(raw.startswith(before[i]+b'\\n') and marker['reconciled_utc']==cfg['now'] and marker['reconciled_utc']!=record['utc'],'missing log did not retain raw prefix/actual repair timestamp')
  calls.clear();before=required_raw();call();need(before==required_raw() and 'gate_next_METADATA_STATUS_ONLY' not in calls,'repeated log repair duplicated output/restarted next program');EVENTS.append({'test':'independent_log_repair_with_later_active_and_existing_'+('_'.join(present) or 'none'),'status':'PASS'})
 # Existing unmarked historical publication narrative is preserved; the new
 # entry explicitly records reconciliation and never rewrites publication time.
 setup();call();before=b'OLD UNMARKED PR952 PUBLICATION MILESTONE\\r\\nUNRELATED \\xfe';(pr/'RESEARCH_LOG.md').write_bytes(before);call();logs_consistent();need((pr/'RESEARCH_LOG.md').read_bytes().startswith(before+b'\\n'),'legacy log narrative changed');EVENTS.append({'test':'legacy_unmarked_milestone_and_nonutf8_bytes_preserved','status':'PASS'})
 def reject_log(name,mutator,role='project'):
  setup();call();path=(pr if role=='project' else audit)/'RESEARCH_LOG.md';raw=path.read_bytes();path.write_bytes(mutator(raw));before=required_raw()
  try:call()
  except (RuntimeError,OSError,ValueError,TypeError,KeyError) as e:need(before==required_raw(),'bad log overwrote local outcome');EVENTS.append({'test':name,'status':'REJECTED_EXPECTED','guard':str(e)})
  else:raise RuntimeError('malformed/conflicting marker accepted '+name)
 prefix=b'PR952-LOCAL-COMPLETION-V1 '
 def marker_mut(raw,fn):
  before,line=raw.split(prefix);marker=json.loads(line);fn(marker);return before+prefix+json.dumps(marker,sort_keys=True,separators=(',',':')).encode()+b'\\n'
 for key,bad in [('doi','wrong'),('merge_commit','1'*40),('native_ledger_commit','1'*40),('accepted_freeze_sha256','1'*64),('original_pr_head','1'*40),('tracker_range','wrong'),('problem_id','wrong'),('clean_final_review_manifest_sha256','1'*64)]:reject_log('log_conflicting_'+key,lambda raw,k=key,v=bad:marker_mut(raw,lambda m:m['approved_outcome'].update({k:v})))
 for key,bad in [('reconciled_utc','2026-10-16T00:00:00'),('reconciled_utc',None),('workflow_completion_estimate_percent',True),('workflow_completion_estimate_percent',99),('schema','wrong'),('approved_sha256','1'*64),('approved_outcome',None)]:reject_log('log_malformed_'+key+'_'+str(bad),lambda raw,k=key,v=bad:marker_mut(raw,lambda m:m.update({k:v})),role='audit')
 reject_log('duplicate_same_outcome_markers',lambda raw:raw+raw[raw.index(prefix):])
 reject_log('truncated_marker_line',lambda raw:raw[:-7])
 reject_log('malformed_reserved_marker_framing',lambda raw:raw+b'PR952-LOCAL-COMPLETION BROKEN\\n')
 reject_log('noncanonical_marker_json',lambda raw:raw.replace(b'{"approved_outcome"',b'{ "approved_outcome"'))
 reject_log('duplicate_marker_json_key',lambda raw:raw.replace(b'{"approved_outcome"',b'{"schema":"pr952-local-completion-v1","approved_outcome"'))
 # Log mode and symlink checks use actual nofollow regular-file boundaries.
 for role in ['project','audit']:
  setup();path=(pr if role=='project' else audit)/'RESEARCH_LOG.md';path.chmod(0o640);before=required_raw()
  try:call()
  except RuntimeError as e:need('mode' in str(e),'wrong unsupported-mode guard')
  else:raise RuntimeError('unsupported mode accepted')
  path.chmod(0o644);call();logs_consistent();EVENTS.append({'test':'log_unsupported_mode_rejected_then_repaired_'+role,'status':'PASS'})
 # Fresh-input checks also protect both raw log prefixes from stale overwrite.
 for role in ['project_log','audit_log']:
  setup();cfg['concurrent_change']=role
  try:call()
  except RuntimeError as e:need(any(x in str(e) for x in ['fingerprint','changed','nonregular or oversized']),'wrong stale-log guard')
  else:raise RuntimeError('stale log snapshot accepted')
  path=(pr if role=='project_log' else audit)/'RESEARCH_LOG.md';before=path.read_bytes();need(b'CONCURRENT UNRELATED BYTES' in before,'owned log change absent');call();logs_consistent();need(path.read_bytes().startswith(before),'fresh retry lost concurrent unrelated bytes');EVENTS.append({'test':'stale_log_input_reject_then_fresh_prefix_preserved_'+role,'status':'PASS'})
 for role in ['project','audit']:
  for damage in ['missing','symlink','hardlink']:
   setup();path=(pr if role=='project' else audit)/'RESEARCH_LOG.md';unrelated=path.parent/'unrelated-log-anchor';unrelated.write_bytes(b'UNRELATED ANCHOR');path.unlink()
   if damage=='symlink':path.symlink_to(unrelated.name)
   if damage=='hardlink':os.link(unrelated,path)
   before=[(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']]
   try:call()
   except (RuntimeError,OSError) as e:
    need(unrelated.read_bytes()==b'UNRELATED ANCHOR','unrelated linked target overwritten')
    if damage in ('missing','symlink'):need([(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']]==before,'missing/symlink log changed state before validation')
   else:raise RuntimeError('unsafe/missing required log accepted')
   if path.exists() or path.is_symlink():path.unlink()
   path.write_bytes(b'UNRELATED LOG\\n');call();logs_consistent();unrelated.unlink();EVENTS.append({'test':'required_log_'+damage+'_reject_and_owned_repair_'+role,'status':'PASS'})
 # Completion record and all four final bytes remain stable after repeated calls.
 setup();call();consistent();logs_consistent();before=required_raw();calls.clear();call();need(before==required_raw(),'completed outcome not byte-idempotent');need(all(name in ['accepted_package','merged_gate','publication_links','descriptor_check','independent_public_verify','native_verify','accepted_review_check','finalize_pr_metadata_ALREADY_CORRECT_NO_EDIT','gws_GET_ONLY'] for name in calls),'unexpected retry boundary/action');EVENTS.append({'test':'success_requires_four_exact_local_files_no_remote_mutation_retry','status':'PASS'})
'''
s=s[:pos]+extra+s[pos:]
s=s.replace("pr952-proposed-finalization-recovery-controls-v1", "pr952-proposed-finalization-and-logs-recovery-controls-v2")
s=s.replace("'local_atomic_json','reconcile_local_finalization'", "'local_atomic_json','local_atomic_bytes','local_final_log','reconcile_local_finalization'")
(OWN/'test_finalization_logs_recovery.py').write_text(s)
compile(s,str(OWN/'test_finalization_logs_recovery.py'),'exec')

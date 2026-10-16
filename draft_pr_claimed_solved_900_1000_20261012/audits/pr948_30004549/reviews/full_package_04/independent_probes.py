import pathlib,json,copy,datetime,hashlib
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr948_30004549';D=A/'preprint';W=A/'publication/workflow';O=A/'reviews/full_package_04';core=P/'accept_pr948.py'
assert hashlib.sha256(core.read_bytes()).hexdigest()=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823'
N={'__name__':'_round04_inert_independent_','__file__':str(core)};exec(compile(core.read_bytes(),str(core),'exec',dont_inherit=True,optimize=0),N)
rows=[]
def check(name,fn):
 fn();rows.append({'name':name,'status':'PASS'})
def need(x):
 if not x:raise RuntimeError('probe expectation failed')
def reject(fn,part=None):
 try:fn()
 except (RuntimeError,ValueError,TypeError,KeyError,OSError) as e:
  if part:need(part in str(e))
  return
 raise RuntimeError('unsafe evidence accepted')
F=json.loads((D/'FREEZE.json').read_bytes());pins={'freeze':hashlib.sha256((D/'FREEZE.json').read_bytes()).hexdigest(),'manifest':F['package_manifest_sha256'],'pdf':F['files'][N['PDF']]['sha256']}
context=N['capture_inventory']('500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002')
B=D/'reviewed_candidates/candidate01';oldraw=(B/'FREEZE.json').read_bytes();oldpin=hashlib.sha256(oldraw).hexdigest();private=B/'evidence'/str((A/'source_record_private.txt').relative_to(R));realread=N['read_regular'];realprofile=N['frozen_profile'];calls=[]
for label in ('missing','tampered'):
 def fake(path,cap=N['MAX_FILE'],pin=None):
  if pathlib.Path(path)==private:
   if label=='missing':raise FileNotFoundError('owned simulated missing historical private snapshot')
   return realread(path,cap,pin={**pin,'sha256':'0'*64})
  return realread(path,cap,pin)
 N['read_regular']=fake;N['frozen_profile']=lambda *a,**k:calls.append(True)
 try:check('actual_old_private_'+label+'_rejects_before_profile',lambda:reject(lambda:N['freeze_check'](oldraw,oldpin,context,B,historical=True)));check('actual_old_private_'+label+'_no_profile_calls',lambda:need(calls==[]))
 finally:N['read_regular']=realread;N['frozen_profile']=realprofile
base=json.loads((A/'reviews/full_package_02/RESULT.json').read_bytes())
check('complete_clean_result_positive',lambda:need(N['result_schema'](base) is True))
for field in ('clean_context','entire_package_review','full_reproducer_completed'):
 bad=copy.deepcopy(base);bad[field]=False
 check('false_'+field+'_without_history_rejected',lambda bad=bad:reject(lambda:N['result_schema'](bad)))
bad=copy.deepcopy(base);bad['clean_context']=False;bad['clean_for_preprint']=False;bad['nonclean_history']={'status':'failed','explanation':'Actual hypothetical missing pre-intake check; later success cannot backdate it.','checks_not_passed':['before_intake_seventh_live_source']}
check('honest_nonclean_history_positive',lambda:need(N['result_schema'](bad) is False))
bad=copy.deepcopy(base);bad['optional_issues']=[{'id':'INERT-ONLY'}]
check('optional_issue_cannot_claim_clean',lambda:reject(lambda:N['result_schema'](bad)))
C=json.loads((O/'COLD_REPLAY.json').read_bytes())
check('actual_cold_positive_schema',lambda:need(N['review_cold'](C,pins,F,D)[0]))
for label,edit in [('one_field_changes',lambda c:c['modes'][0]['receipt'].update(limits='unreviewed')),('reversed_chronology',lambda c:c['modes'].reverse()),('wrong_env2_outer',lambda c:c['modes'][3].update(observed_outer_optimization=2)),('claimed_pass_mode_in_fail_receipt',lambda c:c['modes'][0].update(status='FAIL'))]:
 bad=copy.deepcopy(C);edit(bad);check('cold_'+label+'_rejected',lambda bad=bad:reject(lambda:N['review_cold'](bad,pins,F,D)))
realblob=N['blob']
for value in (None,{},False,0):
 N['blob']=lambda ref,path,value=value:json.dumps({N['KEY']:value}).encode() if path==N['STATE'] else b''
 try:check('native_present_'+repr(value)+'_is_not_absence',lambda:reject(lambda:N['native_safety']('inert')))
 finally:N['blob']=realblob
node={'baseRefName':'main','baseRef':{'name':'main','target':{'oid':'1'*40}}}
check('live_pointer_exact_positive',lambda:need(N['live_base_pointer'](node)=='1'*40))
for label,edit in [('name_mismatch',lambda n:n['baseRef'].update(name='other')),('upper_oid',lambda n:n['baseRef']['target'].update(oid='A'*40)),('null_target',lambda n:n['baseRef'].update(target=None))]:
 bad=copy.deepcopy(node);edit(bad);check('live_pointer_'+label+'_rejects',lambda bad=bad:reject(lambda:N['live_base_pointer'](bad)))
# Audit a surviving zero-byte failed engineering attempt as bytes, never JSON/PASS.
p=W/'LIVE_BASE_ATTEMPT_03.json';check('zero_byte_failed_attempt_preserved',lambda:need(p.read_bytes()==b''));check('zero_byte_is_not_json_receipt',lambda:reject(lambda:N['strict_json'](p.read_bytes())))
profile=json.loads((O/'profile/DEVELOPMENT_RESULTS.json').read_bytes());events=profile['events'];check('85_actual_profile_events_no_skips',lambda:need(len(events)==85 and not any('skip' in str(e.get('outcome','')).lower() for e in events)));check('reachable_ambient_poison_was_executed',lambda:need(any(e['test']=='ambient_import_poison_positive_control' and e['outcome']=='controlled_poison_executed_without_isolation' and e['exit_code']!=0 for e in events)))
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','passed':len(rows),'failed':0,'tests':rows,'actual_core_sha256':hashlib.sha256(core.read_bytes()).hexdigest(),'services':0,'production_action_functions_called':False,'scope':'Freshly reasoned direct inert evidence/provenance/schema controls; no mutation or independent design claim for inherited suites.'};p=O/'INDEPENDENT_PROBES.json';t=p.with_suffix('.json.tmp');t.write_text(json.dumps(obj,indent=2)+'\n');t.replace(p);print(json.dumps({'status':'PASS','passed':len(rows)}))

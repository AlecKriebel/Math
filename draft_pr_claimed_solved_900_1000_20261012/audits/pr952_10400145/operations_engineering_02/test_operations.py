#!/usr/bin/env python3
"""Inert PR952 adapter controls. Synthetic fixtures give no acceptance/review credit."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,copy,hashlib,json,os,tempfile
from pathlib import Path
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];CORE=P/'accept_pr952.py'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
p=argparse.ArgumentParser();p.add_argument('--core-sha256',required=True);a=p.parse_args()
raw=CORE.read_bytes()
if sha(raw)!=a.core_sha256:raise SystemExit('External core SHA mismatch')
n={'__name__':'_synthetic_inert_tests_','__file__':str(CORE)};exec(compile(raw,str(CORE),'exec',dont_inherit=True,optimize=0),n)
REAL_REMOTE_MAIN=n['remote_main'];EVENTS=[]
def yes(name,fn):
 v=fn();EVENTS.append({'test':name,'status':'PASS'});return v
def no(name,fn):
 try:fn()
 except (RuntimeError,ValueError,TypeError,KeyError,OSError):EVENTS.append({'test':name,'status':'REJECTED_EXPECTED'});return
 raise RuntimeError('ADVERSE CONTROL UNEXPECTEDLY ACCEPTED: '+name)
def boom(*a,**k):raise RuntimeError('REAL SERVICES/GIT DISABLED BY INERT HARNESS')
n['run']=boom;n['remote_main']=boom;n['pr_view']=boom;n['gws']=boom;n['bounded_public_get']=boom
(OWN/'private_tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='adapter-tests-',dir=OWN/'private_tmp') as td:
 root=Path(td);n.update(ROOT=root,A=root/'audit',D=root/'preprint',W=root/'workflow',P=root/'operations')
 for key in ['A','D','W','P']:n[key].mkdir()
 yes('strict_type_equality',lambda:n['need'](not n['exact'](1,True),'bool integer confusion'))
 no('duplicate_json_keys',lambda:n['strict_json'](b'{"a":1,"a":2}'))
 no('nonfinite_json',lambda:n['strict_json'](b'{"a":NaN}'))
 for bad in ['../a','/a','a//b','a/./b','a\\b','a/../b']:
  no('unsafe_path_'+repr(bad),lambda b=bad:n['need'](n['safe'](b),'unsafe path'))
 for pin in [{'bytes':True,'sha256':'a'*64},{'bytes':1.0,'sha256':'a'*64},{'bytes':1,'sha256':'A'*64}]:no('bad_pin_'+repr(pin),lambda p=pin:n['validate_pin'](p))
 normal=root/'normal';normal.write_bytes(b'x');yes('read_regular_exact',lambda:n['read_regular'](normal,pin=n['fingerprint'](b'x')))
 no('read_regular_changed',lambda:n['read_regular'](normal,pin=n['fingerprint'](b'y')))
 link=root/'symlink';link.symlink_to(normal);no('read_regular_symlink',lambda:n['read_regular'](link))
 (root/'fifo').mkfifo() if hasattr(Path,'mkfifo') else os.mkfifo(root/'fifo')
 no('read_regular_fifo_without_block',lambda:n['read_regular'](root/'fifo'))
 # Current absence differs from an explicit null. No historical zero inference.
 blobs={n['STATE']:b'{"other": {"x":1}}\n',n['HISTORY']:b'{"id":"other"}\n'}
 n['blob']=lambda ref,path:blobs[path]
 got=yes('native_absence_unknown',lambda:n['native_safety']('fixture'))
 n['need'](got['historical_native_turn_count']=='UNKNOWN' and got['target_state_absent'] is True,'honest absent schema')
 for body in [b'{"10400145":null}',b'{"10400145":{}}']:
  blobs[n['STATE']]=body;no('native_explicit_target_reject_'+body.decode(),lambda:n['native_safety']('fixture'))
 blobs[n['STATE']]=b'{}';blobs[n['HISTORY']]=b'{"id":"10400145","event":"candidate_turn"}\n';no('native_target_history',lambda:n['native_safety']('fixture'))
 # Literal unrelated state members and every old history byte survive.
 q=b'PREFIX\n| 10400145 / AMR-103-0145 | b | c | d | e | f | g | claimed_solved | 1/5 | j | note | link |\nSUFFIX\n'
 state=b'{\n  "x" : {"unicode": "\\u03b1", "array": [1,  2]}\n}\n';hist=b'{"id":"other", "literal":  1}'
 pub={'id':123,'doi':'10.5281/zenodo.123','record_url':'https://zenodo.org/records/123'}
 event=n['native_event']({'freeze_sha256':'f'*64},pub,{'mergeCommit':{'oid':'b'*40}},{'updated_range':"'Math Puzzles'!A2:D2"})
 r=yes('native_narrow_replacements',lambda:n['native_replacements'](q,state,hist,event))
 n['need'](n['queue_parts'](r[n['QUEUE']])[0]==n['queue_parts'](q)[0] and r[n['HISTORY']].startswith(hist) and b'"x" : {"unicode": "\\u03b1", "array": [1,  2]}' in r[n['STATE']],'byte preservation')
 n['need'](event['turns_used']==1 and event['original_declared_turns']=='1/5' and event['historical_native_turn_count']=='UNKNOWN' and 'candidate_turn' not in event,'honest imported turns')
 yes('imported_declaration_no_author_turn',lambda:event)
 no('claimed_wrong_turns',lambda:n['claimed_row'](q.replace(b'1/5',b'0/5')))
 # Dynamic computed status may change while stable authority remains fixed.
 before={'number':952,'state':'OPEN','isDraft':True,'headRefOid':n['HEAD'],'headRefName':'fixture','baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','title':'fixture','body':'fixture','baseRefOid':'0'*40,'currentBaseRefOid':'a'*40,'mergeable':'UNKNOWN','mergeStateStatus':'UNKNOWN'}
 after={**before,'mergeable':'MERGEABLE','mergeStateStatus':'CLEAN','baseRefOid':'1'*40,'currentBaseRefOid':'b'*40}
 bracket=yes('authority_computed_status_change_retained',lambda:n['observation_bracket'](before,after))
 n['need'](bracket['authority_equal'] and 'currentBaseRefOid' in bracket['observation_differences'],'stable authority/computed observation split')
 no('immutable_head_change',lambda:n['observation_bracket'](before,{**after,'headRefOid':'0'*40}))
 # Complete changed-file pagination uses actual baseRef.target; not associated base.
 page={k:v for k,v in before.items() if k not in ('title','body','mergeable','mergeStateStatus','currentBaseRefOid')};page['baseRef']={'name':'main','target':{'oid':'a'*40}};page['changedFiles']=2;page['files']={'nodes':[{'path':'unsolved_math_prioritization/QUEUE.md'},{'path':'unsolved_math_prioritization/attempts/10400145/README.md'}],'pageInfo':{'hasNextPage':False,'endCursor':None}}
 n['run']=lambda *a,**k:json.dumps({'data':{'repository':{'pullRequest':page}}})
 yes('complete_filenames_bound_live_base',lambda:n['complete_changed_paths'](before))
 page['baseRef']['target']['oid']='b'*40;no('filename_base_drift',lambda:n['complete_changed_paths'](before));page['baseRef']['target']['oid']='a'*40
 page['files']['nodes'].append(page['files']['nodes'][0]);no('filename_duplicate_excess',lambda:n['complete_changed_paths'](before));page['files']['nodes'].pop()
 page['changedFiles']=3;no('filename_incomplete_count',lambda:n['complete_changed_paths'](before));page['changedFiles']=2;n['run']=boom
 # Real orchestration accepts dynamic status and rejects a drifting live base.
 original_path='unsolved_math_prioritization/attempts/10400145/README.md'
 n['original_check']=lambda *a,**k:{original_path:{'fixture':True}}
 n['source_gate']=lambda parent:{'fixture_source_parent':parent}
 blobs[n['STATE']]=b'{}';blobs[n['HISTORY']]=b'';blobs[n['QUEUE']]=q
 n['blob']=lambda ref,path:blobs[path]
 n['remote_main']=lambda:'a'*40
 n['run']=lambda args,**kwargs:json.dumps({'data':{'repository':{'pullRequest':page}}}) if args[:3]==['gh','api','graphql'] else 'a'*40
 after_stable={**after,'currentBaseRefOid':'a'*40}
 seq=iter([before,after_stable]);n['pr_view']=lambda *a:next(seq)
 yes('premerge_real_guard_computed_drift_allowed',lambda:n['premerge_gate']({'pr_description_sha256':sha(b'fixture')},True))
 seq=iter([before,after,after]);n['pr_view']=lambda *a:next(seq)
 no('premerge_real_guard_live_base_drift_reject',lambda:n['premerge_gate']({'pr_description_sha256':sha(b'fixture')},True))
 n['run']=boom;n['pr_view']=boom;n['remote_main']=boom
 # Spreadsheet duplicate logic: exactly four strings, exact headers and exact row.
 row=n['tracker_row'](pub);headers=['Original Problem','Solution Chat URL','DOI','Notes']
 yes('tracker_absent',lambda:n['need'](n['duplicate_tracker']([headers],row) is None,'unexpected existing row'))
 yes('tracker_identical_reconciliation',lambda:n['need'](n['duplicate_tracker']([headers,row],row)==2,'identical row lost'))
 no('tracker_conflicting_same_problem',lambda:n['duplicate_tracker']([headers,[row[0],'',row[2],row[3]+' edited']],row))
 no('tracker_multiple_duplicates',lambda:n['duplicate_tracker']([headers,row,row],row))
 no('tracker_wrong_headers',lambda:n['duplicate_tracker']([['DOI'],row],row))
 no('tracker_range_multiple_rows',lambda:n['need'](n['valid_tracker_range']("'Math Puzzles'!A2:D3"),'bad range'))
 # Whole-review validation with actual sealed synthetic evidence; no accept() call.
 dirs=n['A']/'reviews';dirs.mkdir();orig={'original/FIXTURE':{'bytes':1,'sha256':'1'*64,'git_blob':'2'*40,'git_mode':'100644','disk_mode':'0644'}}
 n['original_check']=lambda *a,**k:orig
 inherited=n['inherited_findings'];n['inherited_findings']=lambda freeze:inherited(freeze,n['D'])
 helper={name:{'bytes':1,'sha256':str(i+1)*64} for i,name in enumerate(n['HELPERS'])}
 canonical={'schema':'SYNTHETIC_ONLY_NO_SCIENTIFIC_CREDIT','checks':['fixture']}
 f={'revision_candidate':1,'created_utc':'2026-10-16T00:00:00+00:00','future_helpers':helper,'files':{'package/verify_package.py':{'bytes':1,'sha256':'4'*64}},'package_manifest_sha256':'b'*64,'package_verifier':'verify_package.py','inherited_finding_ids':sorted(n['INHERITED_FINDING_IDS'])}
 dispositions=enc({'findings':[{'id':x} for x in sorted(n['INHERITED_FINDING_IDS'])]});(n['D']/'FINDING_DISPOSITIONS.json').write_bytes(dispositions);f['files']['FINDING_DISPOSITIONS.json']=n['fingerprint'](dispositions)
 for mode in ['normal','O','OO','env2']:(n['D']/('PACKAGE_REPLAY_'+mode+'.json')).write_bytes(enc({'receipt':canonical}))
 f['files'][n['PDF']]={'bytes':1,'sha256':'c'*64};freeze_pin='a'*64
 original_auth={path:{**pin,'archive_mode':'100644','disk_and_archive_match':True} for path,pin in orig.items()}
 bases=[];objects=[]
 def make_round(i,issue=None):
  b=dirs/('full_package_'+str(i).zfill(2));b.mkdir();bases.append(b)
  hour=str(i).zfill(2);start=f'2026-10-16T{hour}:00:00+00:00';end=f'2026-10-16T{hour}:30:00+00:00'
  result={'pr':952,'problem_id':n['KEY'],'original_pr_head':n['HEAD'],'reviewer_agent_id':'SYNTHETIC_REVIEWER_'+str(i),'clean_context':True,'full_reproducer_completed':True,'entire_package_review':True,'started_utc':start,'completed_utc':end,'candidate_revision':1,'candidate_pins':{'freeze':freeze_pin,'manifest':'b'*64,'pdf':'c'*64},'inspected_helper_hashes':helper,'required_issues':[],'optional_issues':[],'clean_for_preprint':issue is None,'strongest_verified_theorem':'SYNTHETIC FIXTURE; NO ACCEPTANCE OR SCIENTIFIC CREDIT','mathematical_remaining_gap_for_stated_theorem':None,'prior_issue_resolution':{'FIXTURE-OPTIONAL':{'verified':True,'evidence':'synthetic prior disposition'},'R952-OPS-ROOT-01':{'verified':True,'evidence':'synthetic root source-gate repair disposition'}},'inherited_finding_dispositions':{x:{'verified':True,'evidence':'synthetic separate disposition '+x} for x in n['INHERITED_FINDING_IDS']}}
  if issue:result['optional_issues']=[{'id':issue,'description':'synthetic adverse finding'}]
  attack=b'INERT FIRST ATTACK; NO SCIENTIFIC REVIEW\n'
  auth={'status':'PASS','utc':f'2026-10-16T{hour}:01:00+00:00','original_pr_head':n['HEAD'],'freeze_sha256':freeze_pin,'package_manifest_sha256':'b'*64,'future_helpers':helper,'candidate_files':copy.deepcopy(f['files']),'originals':copy.deepcopy(original_auth)}
  cold={'status':'PASS','utc':f'2026-10-16T{hour}:10:00+00:00','cold_extraction':True,'package_manifest_sha256':'b'*64,'externally_pinned_verifier_sha256':'4'*64,'normalized_fields_ignored':[],'modes':[{'mode':m,'observed_outer_optimization':o,'returncode':0,'receipt':canonical} for m,o in zip(['normal','O','OO','env2'],[0,1,2,0])]}
  docs={'RESULT.json':result,'FULL_AUDIT.md':b'SYNTHETIC ONLY\n','RESEARCH_LOG.md':b'SYNTHETIC ONLY\n','INITIAL_ATTACK.md':attack,'PRIOR_ASSESSMENT_INTAKE.json':{'status':'OWN_ATTACK_SAVED_BEFORE_PRIOR_ASSESSMENTS','initial_attack_sha256':sha(attack),'own_attack_completed_utc':f'2026-10-16T{hour}:02:00+00:00','prior_assessments_opened_utc':f'2026-10-16T{hour}:03:00+00:00'},'AUTHENTICATION_START.json':auth,'AUTHENTICATION_END.json':{**auth,'utc':f'2026-10-16T{hour}:20:00+00:00'},'COLD_REPLAY.json':cold};objects.append(docs);return docs
 def seals():
  specs=[]
  for i,(b,docs) in enumerate(zip(bases,objects),1):
   for name,v in docs.items():(b/name).write_bytes(v if type(v) is bytes else enc(v))
   manifest=enc({'files':{name:n['fingerprint']((b/name).read_bytes()) for name in docs},'explicit_public_allowlist':list(docs)})
   (b/'MANIFEST.json').write_bytes(manifest);specs.append(str(i).zfill(2)+':'+sha(manifest))
  return specs
 def check():return n['review_check'](seals(),f,freeze_pin,{})
 make_round(1,'FIXTURE-OPTIONAL');make_round(2);make_round(3)
 yes('history_adverse_then_two_current_clean',check)
 snap=copy.deepcopy(objects)
 def mutate(name,fn):
  fn();no(name,check);objects[:]=copy.deepcopy(snap)
 mutate('history_optional_must_be_verified',lambda:objects[2]['RESULT.json']['prior_issue_resolution'].clear())
 mutate('history_root_operational_finding_must_be_verified',lambda:objects[2]['RESULT.json']['prior_issue_resolution'].pop('R952-OPS-ROOT-01'))
 mutate('history_inherited_each_must_be_verified',lambda:objects[2]['RESULT.json']['inherited_finding_dispositions'].pop(sorted(n['INHERITED_FINDING_IDS'])[0]))
 mutate('history_distinct_reviewer',lambda:objects[2]['RESULT.json'].update(reviewer_agent_id=objects[1]['RESULT.json']['reviewer_agent_id']))
 mutate('history_overlapping_reviews',lambda:objects[2]['RESULT.json'].update(started_utc=objects[1]['RESULT.json']['started_utc']))
 mutate('history_false_entire_auth',lambda:objects[2]['AUTHENTICATION_END.json']['candidate_files'].clear())
 mutate('history_cold_optimization_bool',lambda:objects[2]['COLD_REPLAY.json']['modes'][1].update(observed_outer_optimization=True))
 mutate('history_cold_receipt_drift',lambda:objects[2]['COLD_REPLAY.json']['modes'][1].update(receipt={'fabricated':'not canonical'}))
 mutate('history_cold_missing_mode',lambda:objects[2]['COLD_REPLAY.json']['modes'].pop())
 mutate('history_own_attack_after_prior',lambda:objects[2]['PRIOR_ASSESSMENT_INTAKE.json'].update(own_attack_completed_utc=objects[2]['PRIOR_ASSESSMENT_INTAKE.json']['prior_assessments_opened_utc']))
 mutate('history_late_adverse_resets_clean',lambda:objects[2]['RESULT.json'].update(clean_for_preprint=False,optional_issues=[{'id':'LATE','description':'synthetic'}]))
 extra=dirs/'full_package_04';extra.mkdir();no('history_unfinished_directory_preserved',check);extra.rmdir()
 hidden=dirs/'.full_package_04';hidden.mkdir();no('history_hidden_unfinished_directory_preserved',check);hidden.rmdir()
 yes('history_honest_incomplete_schema',lambda:n['result_schema']({**objects[0]['RESULT.json'],'clean_context':False,'clean_for_preprint':False,'nonclean_history':{'status':'incomplete','explanation':'Synthetic interrupted observation','checks_not_passed':['not run']}}))
 no('history_incomplete_cannot_clean',lambda:n['result_schema']({**objects[0]['RESULT.json'],'clean_context':False,'clean_for_preprint':True}))
 # The observer skips Git fetch and cannot redirect authority paths.
 calls=[];n['run']=lambda args,**kwargs:(calls.append(args) or ('a'*40+' refs/heads/main\n'))
 n['READ_ONLY']=True;yes('readonly_remote_main_no_fetch',REAL_REMOTE_MAIN);n['need'](len(calls)==1 and calls[0][1]=='ls-remote','observer attempted Git fetch');n['READ_ONLY']=False;n['run']=boom
 # Durable POST intent and immediate returned-ID receipt, all calls inert.
 class Client:
  def __init__(self):self.creates=0;self.posts=0
  def create(self,metadata):self.creates+=1;return {'id':123,'submitted':False,'metadata':metadata,'files':[]}
  def get(self,ident):return {'id':ident,'submitted':False,'metadata':{'title':'fixture'},'files':[]}
  def publish(self,ident):self.posts+=1;raise RuntimeError('SYNTHETIC lost response')
 kit={'validate_record':lambda rec,ident:n['need'](rec['id']==ident,'ID mismatch'),'verify':lambda *a:[]};c=Client();g=n['GuardedZenodoClient'](c,kit,{'title':'fixture'},[],lambda:None,'stage')
 yes('zenodo_one_create',lambda:g.create({'title':'fixture'}));n['need']((n['W']/'ZENODO_CREATED_ID.json').exists(),'returned ID not durable')
 no('zenodo_second_create_same_client',lambda:g.create({'title':'fixture'}));g2=n['GuardedZenodoClient'](c,kit,{'title':'fixture'},[],lambda:None,'stage');no('zenodo_second_create_new_process_intent',lambda:g2.create({'title':'fixture'}));n['need'](c.creates==1,'second create reached client')
 gp=n['GuardedZenodoClient'](c,kit,{'title':'fixture'},[],lambda:None,'publish',123);no('zenodo_lost_publish_response',lambda:gp.publish(123));gp2=n['GuardedZenodoClient'](c,kit,{'title':'fixture'},[],lambda:None,'publish',123);no('zenodo_no_second_publish_after_uncertainty',lambda:gp2.publish(123));n['need'](c.posts==1,'second publish reached client')
 no('zenodo_other_ID_GET',lambda:gp.get(124));no('zenodo_notes_no_normalization',lambda:n['exact_remote_metadata']({'metadata':{'notes':'a&gt;b'}},{'notes':'a>b'}))
 n['need'](all(e['status'] in ('PASS','REJECTED_EXPECTED') for e in EVENTS),'test status')
print(json.dumps({'schema':'pr952-inert-operations-controls-v1','status':'PASS_INERT_CONTROLS','outer_optimization':sys.flags.optimize,'core_sha256':a.core_sha256,'events':EVENTS,'event_count':len(EVENTS),'real_service_calls':0,'real_Git_calls':0,'acceptance_authority':False,'scientific_review_credit':False},sort_keys=True))

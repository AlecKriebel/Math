#!/usr/bin/env python3
"""Proposed native-recovery actual-function tests; no real Git/services or acceptance.
Only accepted_package/accepted_review_check are explicit synthetic trust boundaries.
All publication links, source SQLite, native/raw commits and original33 checks run.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,copy,hashlib,json,sqlite3,subprocess,tempfile,types
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];A=P/'audits/pr952_10400145'
BASE_SHA='854a8694e3b4b46d3eff32f207729d2637c262b9714d8a7b052289450831e908'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,m):
 if not ok:raise RuntimeError(m)
def encode(x):return (json.dumps(x)+'\n').encode()
p=argparse.ArgumentParser();p.add_argument('--proposal-sha256',required=True);p.add_argument('--installed',action='store_true');a=p.parse_args()
base=(OWN/'BASE_accept_pr952.py').read_bytes();proposed=(OWN/'PROPOSED_accept_pr952.py').read_bytes()
need(sha(base)==BASE_SHA and sha(proposed)==a.proposal_sha256,'external base/proposal source pins')
need(sha((P/'accept_pr952.py').read_bytes())==(a.proposal_sha256 if a.installed else BASE_SHA),'current core changed outside authorized phase')
source=(A/'source_record_private.txt').read_bytes();records=(A/'ORIGINAL_FILE_RECORDS.json').read_bytes();originals=json.loads(records)['files']
source_doc=json.loads(source)
ORIGINAL_BYTES={name:(A/'original'/name).read_bytes() for name in originals}
EVENTS=[]
(OWN/'private_tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='native-proposal-',dir=OWN/'private_tmp') as td:
 root=Path(td);audit=root/'audit';workflow=root/'workflow';d=root/'preprint';cache=root/'unsolved_math_prioritization/cache'
 for path in [audit,workflow,d,cache]:path.mkdir(parents=True)
 (audit/'source_record_private.txt').write_bytes(source);(audit/'ORIGINAL_FILE_RECORDS.json').write_bytes(records)
 for name,body in ORIGINAL_BYTES.items():
  path=audit/'original'/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body);path.chmod(0o644)
 with sqlite3.connect(cache/'catalog.sqlite') as c:
  c.execute('CREATE TABLE records(key TEXT,payload TEXT,report TEXT)');c.execute('INSERT INTO records VALUES(?,?,?)',('10400145',json.dumps(source_doc['problem']),json.dumps(source_doc['prior_research'])))
 constants={'base':'a'*40,'merge':'b'*40,'parent':'c'*40,'commit':'d'*40,'main':'e'*40}
 n={};calls=[];cfg={};accepted={};freeze={};publication={};merge={};tracker={};blobs={};planned={};prepared={}
 def make_namespace(body):
  space={'__name__':'_inert_native_actual_functions_','__file__':str(P/'accept_pr952.py')};exec(compile(body,str(OWN/('BASE_accept_pr952.py' if sha(body)==BASE_SHA else 'PROPOSED_accept_pr952.py')),'exec',dont_inherit=True,optimize=0),space);return space
 def write(name,obj):
  path=workflow/name;path.write_bytes(encode(obj));return obj
 def blob(ref,path):
  calls.append(('blob',ref,path))
  if path in originals:
   if cfg.get('corrupt_original_ref')==ref and path==next(iter(originals)):return ORIGINAL_BYTES[path]+b'INERT CORRUPTION'
   return ORIGINAL_BYTES[path]
  if path in (n['CATALOG'],n['RELATED']):return blobs[path]
  native_ref=ref in (constants['commit'],constants['main'])
  if ref==constants['main'] and cfg.get('main_absent'):native_ref=False
  return blobs['native' if native_ref else 'parent'][path]
 def ancestor(older,newer):
  if older==constants['commit'] and newer in (constants['main'],constants['commit']):return not cfg.get('not_ancestor',False)
  return older==newer or (older==constants['merge'] and newer in (constants['parent'],constants['commit'],constants['main']))
 def run(args,raw=False,**kwargs):
  calls.append(('run',*args))
  if args[:3]==['git','merge-base','--is-ancestor']:
   if not ancestor(args[3],args[4]):raise subprocess.CalledProcessError(1,args)
   return ''
  if args[:4]==['git','show','-s','--format=%P']:
   if args[4]==constants['merge']:return constants['base']+' '+n['HEAD']
   if args[4]==constants['commit']:return cfg.get('actual_commit_parent',constants['parent'])
  if args[:3]==['git','diff','--name-only']:return '\n'.join(cfg.get('actual_paths',[n['QUEUE'],n['STATE'],n['HISTORY']]))+'\n'
  if args[:2]==['git','ls-tree']:
   name=args[-1];pin=originals[name];return '100644 blob '+pin['git_blob']+'\t'+name+'\n'
  raise RuntimeError('NO REAL COMMAND OR MUTATION: '+repr(args))
 def subprocess_run(args,**kwargs):
  calls.append(('subprocess',*args))
  if args[:3]==['git','merge-base','--is-ancestor']:return types.SimpleNamespace(returncode=0 if ancestor(args[3],args[4]) else 1)
  raise RuntimeError('NO REAL PUSH OR OTHER SUBPROCESS: '+repr(args))
 def accept_boundary(context):
  calls.append(('accepted_package_synthetic_boundary',))
  need(not cfg.get('bad_acceptance'),'synthetic acceptance rejected');return accepted,freeze
 def review_boundary(*args):
  calls.append(('accepted_review_synthetic_boundary',));need(not cfg.get('bad_reviews'),'synthetic review closure rejected')
 def setup(body=proposed):
  global n,accepted,freeze,publication,merge,tracker,blobs,planned,prepared
  for path in workflow.iterdir():
   if path.is_file():path.unlink()
  cfg.clear();calls.clear();n=make_namespace(body);n.update(ROOT=root,A=audit,D=d,W=workflow,READ_ONLY=True)
  n['utc_now']=lambda:'2026-10-16T00:00:00+00:00';n['run']=run;n['blob']=blob;n['subprocess']=types.SimpleNamespace(run=subprocess_run);n['remote_main']=lambda:constants['main'];n['accepted_package']=accept_boundary;n['accepted_review_check']=review_boundary
  accepted={'freeze_sha256':'f'*64,'operations_inventory_sha256':'e'*64}
  for name,body in [(n['PDF'],b'SYNTHETIC PDF ONLY'),(n['ZIP'],b'SYNTHETIC ZIP ONLY')]: (d/name).write_bytes(body)
  meta={'title':n['TITLE'],'version':'1.0','upload_type':'publication','publication_type':'preprint','license':'cc-by-4.0','creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'description':'SYNTHETIC AI unrefereed human formal novelty controls only'}
  descriptor={'metadata':meta,'files':[{'path':name,'name':name} for name in [n['PDF'],n['ZIP']]]};(d/'zenodo-deposit.json').write_bytes(encode(descriptor))
  freeze={'files':{name:n['fingerprint']((d/name).read_bytes()) for name in [n['PDF'],n['ZIP'],'zenodo-deposit.json']}}
  expected=[{'name':name,'size':freeze['files'][name]['bytes'],'sha256':freeze['files'][name]['sha256']} for name in [n['PDF'],n['ZIP']]]
  publication={'environment':'production','title':n['TITLE'],'files':expected,'id':17,'state':'published','doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17','accepted_freeze_sha256':accepted['freeze_sha256'],'operations_inventory_sha256':accepted['operations_inventory_sha256'],'merged_commit':constants['merge']}
  merge={'number':952,'state':'MERGED','isDraft':False,'headRefOid':n['HEAD'],'headRefName':'inert','baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','mergeCommit':{'oid':constants['merge']},'mergedAt':'2026-10-16T00:00:00+00:00','currentBaseRefOid':constants['main']}
  n['pr_view']=lambda *args:copy.deepcopy(merge)
  stage={**publication,'state':'ready_to_publish'}
  for name,obj in [('ZENODO_STAGE.json',stage),('ZENODO_PUBLISH.json',publication),('ZENODO_INSPECT.json',publication),('PR_MERGE_RECEIPT.json',merge)]:write(name,obj)
  write('ZENODO_PUBLISH_INTENT.json',{'accepted_freeze_sha256':accepted['freeze_sha256'],'operations_inventory_sha256':accepted['operations_inventory_sha256'],'descriptor_sha256':freeze['files']['zenodo-deposit.json']['sha256'],'merged_base':'main','merged_commit':constants['merge']})
  write('ZENODO_PUBLIC_VERIFICATION.json',{'confirmed':True,'id':17,'doi':publication['doi'],'no_API_token_sent':True,'files':expected})
  row=n['tracker_row'](publication);tracker={'confirmed':True,'readback_matches':True,'pr':952,'problem_id':n['KEY'],'original_pr_head':n['HEAD'],'merged_base':'main','merge_commit':constants['merge'],'accepted_freeze_sha256':accepted['freeze_sha256'],'zenodo_record_id':17,'doi':publication['doi'],'spreadsheet_id':n['SID'],'gid':1254632077,'tab_title':'Math Puzzles','updated_range':"'Math Puzzles'!A2:D2",'row':row}
  write('TRACKER_RECEIPT.json',tracker);write('TRACKER_READBACK.json',{'range':tracker['updated_range'],'values':[row]})
  event=n['native_event'](accepted,publication,merge,tracker);event['at']='2026-10-16T00:01:00+00:00'
  parent={n['QUEUE']:b'UNRELATED PREFIX\n| 10400145 / AMR-103-0145 | b | c | d | e | f | g | claimed_solved | 1/5 | j | original | link |\nUNRELATED SUFFIX\n',n['STATE']:b'{"OTHER": {"literal": [1,  2]}}\n',n['HISTORY']:b'{"id":"OTHER","event":"old"}'}
  native=n['native_replacements'](parent[n['QUEUE']],parent[n['STATE']],parent[n['HISTORY']],event)
  blobs={'parent':parent,'native':native,n['CATALOG']:encode([{'id':10400145,'present':True,'holds':[],'statement_hash':n['STATEMENT'],'review_hash':n['REVIEW']}]),n['RELATED']:b'{"groups":[]}'}
  planned={'utc':'2026-10-16T00:02:00+00:00','parent':constants['parent'],'published_event':event,'replacement_pins':{name:n['fingerprint'](body) for name,body in native.items()},'accepted_freeze_sha256':accepted['freeze_sha256'],'attempt':1,'blind_retry_permitted':False}
  prepared={'utc':'2026-10-16T00:03:00+00:00','parent':constants['parent'],'commit':constants['commit'],'paths':[n['QUEUE'],n['STATE'],n['HISTORY']],'published_event':copy.deepcopy(event),'source_gate':n['source_gate'](constants['parent']),'native_safety':n['native_safety'](constants['parent']),'accepted_freeze_sha256':accepted['freeze_sha256'],'attempt':1,'blind_retry_permitted':False}
  write('NATIVE_PUBLICATION_CAS_01_INTENT.json',planned);write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',prepared);calls.clear()
 def call():return n['native_write'](None,{'synthetic_boundary':True})
 def reject(name,mutate):
  setup();mutate()
  try:call()
  except (RuntimeError,OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError) as error:
   need(not (workflow/'NATIVE_PUBLICATION_RECEIPT.json').exists(),'bad recovery produced receipt')
   need(not any(c[:3]==('subprocess','git','push') for c in calls),'adverse case called push')
   need(not (workflow/'NATIVE_PUBLICATION_CAS_02_INTENT.json').exists(),'adverse uncertainty started second attempt')
   EVENTS.append({'test':name,'status':'REJECTED_EXPECTED','guard':str(error)})
  else:raise RuntimeError('Adverse case accepted: '+name)
 setup(base)
 try:call()
 except RuntimeError as error:
  need('current native target/history differs' in str(error),'base did not reproduce specific pre-recovery failure')
  need(not any(constants['commit'] in c for c in calls),'base reached exact prepared-commit recovery unexpectedly')
  EVENTS.append({'test':'authenticated_base_reproduces_early_merged_gate_recovery_block','status':'REPRODUCED_REQUIRED_GAP','guard':str(error)})
 else:raise RuntimeError('base unexpectedly recovered')
 setup();call();receipt=json.loads((workflow/'NATIVE_PUBLICATION_RECEIPT.json').read_bytes())
 need(receipt['commit']==constants['commit'] and receipt['parent']==constants['parent'] and receipt['push_confirmed'] is True and receipt['recovered_by_exact_commit_readback'] is True,'exact recovery missing')
 need(receipt['published_event']['turns_used']==1 and 'candidate_turn' not in receipt['published_event'],'fabricated proof turn')
 need(sum(c[0]=='accepted_review_synthetic_boundary' for c in calls)>=2,'review closure boundary omitted')
 need(not any(c[:3]==('subprocess','git','push') for c in calls),'recovery pushed again')
 EVENTS.append({'test':'proposed_real_native_write_exact_saved_commit_recovery','status':'PASS','original33_checks_executed':sum(c[:3]==('run','git','ls-tree') for c in calls),'push_calls':0})
 try:call()
 except RuntimeError:EVENTS.append({'test':'second_invocation_after_recovery_receipt_rejects','status':'REJECTED_EXPECTED'})
 else:raise RuntimeError('second invocation accepted')
 reject('wrong_planned_parent',lambda:write('NATIVE_PUBLICATION_CAS_01_INTENT.json',{**planned,'parent':'1'*40}))
 reject('wrong_actual_commit_parent',lambda:cfg.update(actual_commit_parent='1'*40))
 reject('wrong_prepared_event',lambda:write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',{**prepared,'published_event':{**prepared['published_event'],'doi':'10.5281/zenodo.18'}}))
 def both_event_wrong():
  bad={**planned['published_event'],'new_author_proof_responses':1};write('NATIVE_PUBLICATION_CAS_01_INTENT.json',{**planned,'published_event':bad});write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',{**prepared,'published_event':bad})
 reject('matching_pair_arbitrary_event_not_approved_template',both_event_wrong)
 reject('wrong_freeze',lambda:write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',{**prepared,'accepted_freeze_sha256':'0'*64}))
 reject('exact_commit_not_on_current_main',lambda:cfg.update(not_ancestor=True))
 reject('wrong_declared_paths',lambda:write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',{**prepared,'paths':[n['QUEUE'],n['STATE'],'unexpected']}))
 reject('wrong_actual_commit_paths',lambda:cfg.update(actual_paths=[n['QUEUE'],n['STATE'],'unexpected']))
 reject('wrong_replacement_pin',lambda:write('NATIVE_PUBLICATION_CAS_01_INTENT.json',{**planned,'replacement_pins':{**planned['replacement_pins'],n['STATE']:{'bytes':1,'sha256':'0'*64}}}))
 reject('missing_replacement_pin',lambda:write('NATIVE_PUBLICATION_CAS_01_INTENT.json',{**planned,'replacement_pins':{n['QUEUE']:planned['replacement_pins'][n['QUEUE']]}}))
 reject('missing_prepared',lambda:(workflow/'NATIVE_PUBLICATION_CAS_01_PREPARED.json').unlink())
 reject('orphan_prepared_without_intent',lambda:(workflow/'NATIVE_PUBLICATION_CAS_01_INTENT.json').unlink())
 reject('partial_prepared',lambda:write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',{'commit':constants['commit']}))
 reject('unmatched_saved_source_identity',lambda:write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',{**prepared,'source_gate':{**prepared['source_gate'],'private_record_sha256':'0'*64}}))
 reject('unmatched_baseline_history_pin',lambda:write('NATIVE_PUBLICATION_CAS_01_PREPARED.json',{**prepared,'native_safety':{**prepared['native_safety'],'history_sha256':'0'*64}}))
 reject('baseline_explicit_null_not_absence',lambda:blobs['parent'].update({n['STATE']:b'{"10400145":null}'}))
 reject('raw_replacement_unrelated_literal_changed',lambda:blobs['native'].update({n['STATE']:blobs['native'][n['STATE']].replace(b'[1,  2]',b'[1,2]')}))
 reject('corrupt_original_at_prepared_commit',lambda:cfg.update(corrupt_original_ref=constants['commit']))
 reject('corrupt_original_at_fresh_main',lambda:cfg.update(corrupt_original_ref=constants['main']))
 reject('current_native_event_removed',lambda:cfg.update(main_absent=True))
 reject('accepted_whole_package_boundary_failure',lambda:cfg.update(bad_acceptance=True))
 reject('accepted_whole_review_boundary_failure',lambda:cfg.update(bad_reviews=True))
 reject('publication_wrong_freeze_link',lambda:write('ZENODO_PUBLISH.json',{**publication,'accepted_freeze_sha256':'0'*64}))
 reject('tracker_wrong_merge_link',lambda:write('TRACKER_RECEIPT.json',{**tracker,'merge_commit':'1'*40}))
 reject('extra_unrecognized_attempt',lambda:write('NATIVE_PUBLICATION_CAS_07_INTENT.json',planned))
 def unresolved_later():
  write('NATIVE_PUBLICATION_CAS_02_INTENT.json',{**planned,'attempt':2});write('NATIVE_PUBLICATION_CAS_02_PREPARED.json',{**prepared,'attempt':2})
 reject('later_attempt_after_uncertain_first',unresolved_later)
 def race(action_rc=1,wrong_commit=False):
  write('NATIVE_PUBLICATION_CAS_01_ACTION.json',{'utc':'2026-10-16T00:04:00+00:00','returncode':action_rc,'stdout':'','stderr':'stale info'})
  write('NATIVE_PUBLICATION_CAS_01_DEFINITIVE_RACE.json',{'utc':'2026-10-16T00:05:00+00:00','not_pushed_commit':'1'*40 if wrong_commit else constants['commit'],'observed_remote_main':constants['main'],'repeat_requires_fresh_source_native_gate':True})
  cfg.update(not_ancestor=True,main_absent=True)
 reject('race_wrong_commit',lambda:race(wrong_commit=True))
 reject('race_action_success_cannot_waive_lease',lambda:race(action_rc=0))
 def race_contradiction():race();cfg['not_ancestor']=False
 reject('race_claim_contradicts_commit_on_main',race_contradiction)
 setup();race();n['explicit_tree']=lambda *args:(_ for _ in ()).throw(RuntimeError('INERT_STOP_AFTER_FRESH_GATE_BEFORE_NEW_GIT_OBJECTS'))
 try:call()
 except RuntimeError as error:
  need(str(error)=='INERT_STOP_AFTER_FRESH_GATE_BEFORE_NEW_GIT_OBJECTS','definitive race did not reach fresh strict gate')
  need((workflow/'NATIVE_PUBLICATION_CAS_02_INTENT.json').exists(),'proven race did not permit separately planned fresh parent')
  need(not any(c[:3]==('subprocess','git','push') for c in calls),'definitive-race test performed push')
  EVENTS.append({'test':'proven_definitive_race_reaches_new_strict_absence_gate_only','status':'PASS_INERT_STOP_BEFORE_OBJECT_OR_PUSH'})
 else:raise RuntimeError('inert boundary stop missing')
print(json.dumps({'schema':'pr952-proposed-native-recovery-inert-v1','utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_PROPOSAL_ONLY_NO_INSTALL_OR_REVIEW_CREDIT','base_sha256':BASE_SHA,'proposal_sha256':a.proposal_sha256,'outer_optimization':sys.flags.optimize,'event_count':len(EVENTS),'events':EVENTS,'real_Git_or_service_calls':0,'current_adapter_edits':0,'actual_functions':['native_write','native_attempt_inventory','native_prepared_pair','native_prepared_commit_proof','native_exact_recovery_gate','native_definitive_race','native_verify','native_safety','native_replacements','publication_links','descriptor_check','source_gate','original_check'],'explicit_synthetic_trust_boundaries':['accepted_package','accepted_review_check'],'private_fixture_bodies_retained':False,'fresh_full_review_credit':False,'accepted':False},sort_keys=True))

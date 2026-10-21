import sys
if not sys.flags.isolated:raise RuntimeError('Use -I')
from pathlib import Path
import contextlib,copy,hashlib,io,json,os,tempfile,types,datetime
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';O=A/'reviews/full_package_02'
b=(O/'private/authenticated'/P.relative_to(R)/'accept_pr946.py').read_bytes()
if hashlib.sha256(b).hexdigest()!='7d8d05fc3b05b249de51851db2eeb1e1d7adeecb774046183ecfb0fe08082e5a':raise RuntimeError('core pin')
N={'__name__':'_fresh_ops_adversary_','__file__':str(P/'accept_pr946.py')};exec(compile(b,N['__file__'],'exec'),N)
def fail(*a,**k):raise RuntimeError('Forbidden boundary')
N['run']=fail;N['blob']=fail;N['remote_main']=fail
out=[]
def record(name,f,expected_reject=False):
 try:r=f()
 except (RuntimeError,ValueError,TypeError,OSError) as e:
  if not expected_reject:raise
  out.append({'case':name,'rejected':True,'message':str(e)})
 else:
  if expected_reject:raise RuntimeError('Unexpected accepted '+name)
  out.append({'case':name,'accepted':True,'result':r})
with tempfile.TemporaryDirectory(dir=O/'private',prefix='own_fresh_fs_') as td:
 F=Path(td);N['ROOT']=F;N['A']=F/'effort/audits/pr946_6000001';rv=N['A']/'reviews';rv.mkdir(parents=True)
 specs=['01:'+'a'*64,'02:'+'b'*64]
 for n in ['full_package_01','full_package_02']:(rv/n).mkdir()
 record('actual_descriptor_anchored_exact_two_rounds',lambda:N['require_complete_review_history'](specs))
 for name,kind in [('full_package_03','pending'),('FULL_PACKAGE_03','case'),('full_package_bad','malformed'),('full_package_04','gap'),('full_package_03','link')]:
  p=rv/name
  if kind=='link':p.symlink_to(rv/'full_package_02',target_is_directory=True)
  else:p.mkdir()
  record('new_actual_fs_'+kind,lambda:N['require_complete_review_history'](specs),True)
  if p.is_symlink():p.unlink()
  else:p.rmdir()
 # Ancestor replacement, without following a symlink to the original review directory.
 rv.rename(rv.with_name('real_reviews'));rv.symlink_to(rv.with_name('real_reviews'),target_is_directory=True)
 record('review_ancestor_symlink',lambda:N['require_complete_review_history'](specs),True);rv.unlink();rv.with_name('real_reviews').rename(rv)
 # Real merge flow following acceptance: every external mutation boundary is fake.
 # Accepted package authentication is represented by a trusted existing acceptance; latest
 # proof review was valid when accepted. A new adverse/unfinished round is then present.
 (rv/'full_package_03').mkdir();(rv/'full_package_03/RESULT.json').write_text(json.dumps({'required_issues':[{'id':'NEW-ADVERSE'}]}))
 accepted={'accepted':True,'pr':946,'problem_id':'6000001','original_pr_head':N['HEAD'],'operations_inventory_sha256':'c'*64,'full_package_reviews':[{'round':1},{'round':2}],'all_prior_required_and_optional_findings_resolved':True,'proof_gap':None,'freeze_sha256':'d'*64,'files':{},'future_helpers':{}}
 freeze={'files':{},'future_helpers':{}};N['D']=N['A']/'preprint';N['D'].mkdir();(N['D']/'FREEZE.json').write_text('{}')
 N['load']=lambda p:copy.deepcopy(accepted) if p.name=='ACCEPTANCE.json' else fail(p)
 N['read_regular']=lambda *a,**k:b'{}';N['freeze_check']=lambda *a,**k:freeze;N['disposition_check']=lambda:{}
 live={'number':946,'state':'OPEN','baseRefName':'main','headRefOid':N['HEAD'],'isDraft':False,'mergeCommit':None};calls=[]
 def view():return copy.deepcopy(live)
 N['pr_view']=view;N['premerge_gate']=lambda *a,**k:(view(),'e'*40,{},{});N['save']=lambda p,v,**k:None;N['merged_gate']=lambda *a,**k:{}
 oldrun=N['subprocess'].run
 def fake_sub(args,**kwargs):
  if args[:4]!=['gh','pr','merge','946']:raise RuntimeError('Forbidden subprocess')
  calls.append(args);live.update(state='MERGED',mergeCommit={'oid':'e'*40});return types.SimpleNamespace(returncode=0,stdout='fake only',stderr='')
 N['subprocess'].run=fake_sub
 try:
  with contextlib.redirect_stdout(io.StringIO()):N['merge'](types.SimpleNamespace(),{'inventory_sha256':'c'*64})
 finally:N['subprocess'].run=oldrun
 out.append({'case':'postacceptance_new_adverse_round_merge_flow','new_round_present':(rv/'full_package_03').is_dir(),'mock_merge_mutations_dispatched':len(calls),'guard_rechecked':False,'finding_candidate':'FP02-OPS-001','all_external_actions_mocked':True})
 # A later adverse round appearing after the readiness action also reaches merge.
 shutil=__import__('shutil');shutil.rmtree(rv/'full_package_03');live.update(state='OPEN',isDraft=True,mergeCommit=None);calls.clear()
 def fake_ready_sub(args,**kwargs):
  if args[:4]==['gh','pr','ready','946']:
   calls.append(args);(rv/'full_package_03').mkdir();(rv/'full_package_03/RESULT.json').write_text('{"required_issues":[{"id":"AFTER-READY"}]}');live['isDraft']=False
  elif args[:4]==['gh','pr','merge','946']:
   calls.append(args);live.update(state='MERGED',mergeCommit={'oid':'e'*40})
  else:raise RuntimeError('Forbidden subprocess')
  return types.SimpleNamespace(returncode=0,stdout='fake only',stderr='')
 N['subprocess'].run=fake_ready_sub
 try:
  with contextlib.redirect_stdout(io.StringIO()):N['merge'](types.SimpleNamespace(),{'inventory_sha256':'c'*64})
 finally:N['subprocess'].run=oldrun
 out.append({'case':'adverse_round_created_after_ready_before_merge','mock_actions':[a[2] for a in calls],'new_round_present':(rv/'full_package_03').is_dir(),'guard_rechecked':False,'all_external_actions_mocked':True})
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'core_sha256':hashlib.sha256(b).hexdigest(),'external_mutations':0,'controls':out};(O/'INDEPENDENT_OPERATIONS_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

import sys
if not sys.flags.isolated:raise RuntimeError('use -I')
from pathlib import Path
import json,hashlib,shutil,copy,datetime,types,contextlib,io,ast
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint';O=A/'reviews/full_package_03';F=json.loads((D/'FREEZE.json').read_bytes());fp=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};enc=lambda j:(json.dumps(j,indent=2)+'\n').encode();FP=fp((D/'FREEZE.json').read_bytes())['sha256'];assert FP=='fdff50b3a1c77523b1b1b7c3da42b2dfdbb1bc17ada7b19abfcbfbbd40d4c505'
b=(P/'accept_pr946.py').read_bytes();assert fp(b)['sha256']=='f2695b6b7d5e7c6553280082b41987a7fbc7332bc980228502f7e10d8b7ded73';N={'__name__':'_independent_action_chain_','__file__':str(P/'accept_pr946.py')};exec(compile(b,N['__file__'],'exec'),N)
root=O/'private/action_chain'
if root.exists():shutil.rmtree(root)
root.mkdir();p=root/P.name;a=p/'audits/pr946_6000001';d=a/'preprint';d.mkdir(parents=True);(a/'reviews').mkdir()
def cp(src,dest):dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes());dest.chmod(0o644)
for name in ['FREEZE.json',*F['files']]:cp(D/name,d/name)
for name in F['evidence_files']:cp(R/name,root/name)
cp(A/'OPERATIONS_INVENTORY.json',a/'OPERATIONS_INVENTORY.json');op=json.loads((A/'OPERATIONS_INVENTORY.json').read_bytes())
for name in op['files']:cp(R/name,root/name)
for number,seal in [(1,'2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834'),(2,'e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6')]:
 w=A/'reviews'/f'full_package_{number:02d}';mb=(w/'MANIFEST.json').read_bytes();assert fp(mb)['sha256']==seal;m=json.loads(mb)
 for name,pin in m['files'].items():raw=(w/name).read_bytes();assert fp(raw)==pin;cp(w/name,a/'reviews'/w.name/name)
 cp(w/'MANIFEST.json',a/'reviews'/w.name/'MANIFEST.json')
 old=D/'reviewed_candidates'/f'candidate{number:02d}';of=json.loads((old/'FREEZE.json').read_bytes());dest=d/'reviewed_candidates'/old.name
 for name in ['FREEZE.json','OPERATIONS_INVENTORY.json',*of['files']]:cp(old/name,dest/name)
 oi=json.loads((old/'OPERATIONS_INVENTORY.json').read_bytes())
 for name in oi['files']:cp(old/'operations'/name,dest/'operations'/name)
S=json.loads((O/'AUTHENTICATION_START.json').read_bytes());originals=S['originals']
for name in originals:cp(A/'original'/name,a/'original'/name)
N.update(ROOT=root,P=p,A=a,D=d)
N['freeze_check'].__defaults__=(d,False);N['archive_check'].__defaults__=(d,)
# Every fake Git response is bound to an independently authenticated actual original blob/mode.
def forbidden(*args,**kw):raise RuntimeError('EXTERNAL BOUNDARY FORBIDDEN '+repr(args))
def orig_blob(ref,name):assert ref==N['HEAD'];return (a/'original'/name).read_bytes()
def orig_run(args,**kw):
 if args[:2]==['git','ls-tree']:
  name=args[-1];rec=originals[name];return '100644 blob '+rec['git_blob']+'\t'+name+'\n'
 return forbidden(args)
N['blob']=orig_blob;N['run']=orig_run;N['remote_main']=forbidden;N['subprocess']=types.SimpleNamespace(run=forbidden)
ctx=N['capture_inventory'](F['operations_inventory_sha256']);freeze=N['freeze_check']((d/'FREEZE.json').read_bytes(),FP,ctx);_,exp=N['original_check']();assert len(exp)==33
# The terminal round is SYNTHETIC contract evidence only; real01/02 seals and historical candidates are unchanged.
w=a/'reviews/full_package_03';w.mkdir();ts=['2026-10-15T14:00:0'+str(i)+'+00:00' for i in range(5)]
r=copy.deepcopy(json.loads((A/'reviews/full_package_02/RESULT.json').read_bytes()));prior=set(r['prior_issue_resolution'])|{x['id'] for x in r['required_issues']+r['optional_issues']};r.update(reviewer_agent_id='SYNTHETIC_ACTION_GUARD_TERMINAL',started_utc=ts[0],completed_utc=ts[4],candidate_revision=3,candidate_pins={'freeze':FP,'manifest':F['package_manifest_sha256'],'pdf':F['files']['research_note.pdf']['sha256']},inspected_helper_hashes=F['future_helpers'],required_issues=[],optional_issues=[],clean_for_preprint=True,strongest_verified_theorem='Synthetic terminal contract fixture only, no production acceptance.',prior_issue_resolution={k:{'verified':True,'fixture':True} for k in prior})
s=copy.deepcopy(S);s['utc']=ts[1];e=copy.deepcopy(S);e['utc']=ts[3];c=json.loads((O/'COLD_REPLAY.json').read_bytes());c['utc']=ts[2]
for name,j in [('RESULT.json',r),('AUTHENTICATION_START.json',s),('AUTHENTICATION_END.json',e),('COLD_REPLAY.json',c)]: (w/name).write_bytes(enc(j))
(w/'FULL_AUDIT.md').write_text('Synthetic contract fixture only.\n');(w/'RESEARCH_LOG.md').write_text('Synthetic contract fixture only.\n')
manifest=enc({'files':{q.name:fp(q.read_bytes()) for q in w.iterdir()},'explicit_public_allowlist':sorted(q.name for q in w.iterdir())});(w/'MANIFEST.json').write_bytes(manifest)
specs=['01:2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834','02:e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6','03:'+fp(manifest)['sha256']]
rows,latest=N['review_check'](specs,freeze,FP,ctx,exp)
accepted={'accepted':True,'pr':946,'problem_id':'6000001','original_pr_head':N['HEAD'],'operations_inventory_sha256':ctx['inventory_sha256'],'full_package_reviews':rows,'all_prior_required_and_optional_findings_resolved':True,'proof_gap':None,'freeze_sha256':FP,'files':F['files'],'future_helpers':F['future_helpers'],'exact_claim':r['strongest_verified_theorem']};(a/'ACCEPTANCE.json').write_bytes(enc(accepted));cases=[]
def ok(label,fn):
 with contextlib.redirect_stdout(io.StringIO()):v=fn()
 cases.append({'case':label,'passed':True});return v
def reject(label,fn,reason=None):
 try:
  with contextlib.redirect_stdout(io.StringIO()):fn()
 except (RuntimeError,OSError,KeyError,ValueError) as er:
  msg=str(er);assert 'EXTERNAL BOUNDARY FORBIDDEN' not in msg,msg
  if reason:assert reason in msg,msg
  cases.append({'case':label,'rejected':True,'reason':msg[:250]});return
 raise RuntimeError('accepted invalid case '+label)
ok('actual_complete_01_02_historical_and03_current_chain',lambda:N['accepted_package'](ctx))
extra=a/'reviews/full_package_04'
def adverse(kind='pending'):
 extra.mkdir()
 if kind=='adverse':(extra/'RESULT.json').write_bytes(enc({'required_issues':[{'id':'SYNTHETIC_NEW_ADVERSE'}]}))
def clear():
 if extra.exists():shutil.rmtree(extra)
 for n in ['PR_MERGE_INTENT.json','PR_READY_ACTION.json','TRACKER_APPEND_INTENT.json','PR_FINAL_METADATA_INTENT.json',*[f'NATIVE_PUBLICATION_CAS_{i:02d}_INTENT.json' for i in range(1,7)],*[f'NATIVE_PUBLICATION_CAS_{i:02d}_ACTION.json' for i in range(1,7)]]:
  (a/n).unlink(missing_ok=True)
 for action in ['STAGE','PUBLISH','INSPECT']:(d/('ZENODO_'+action+'_INTENT.json')).unlink(missing_ok=True)
for kind in ['pending','adverse']:
 adverse(kind)
 for action in ['merge','tracker_append','native_write','finalize']:
  reject(kind+'_blocks_'+action,lambda action=action:N[action](types.SimpleNamespace(),ctx),'supplied reviews must account')
 for action in ['stage','publish','inspect']:reject(kind+'_blocks_kit_'+action,lambda action=action:N['zenodo'](types.SimpleNamespace(action=action),ctx),'supplied reviews must account')
 clear()
for kind in ['payload','manifest','accepted_chain','theorem']:
 path=(w/('RESULT.json' if kind=='payload' else 'MANIFEST.json')) if kind in ['payload','manifest'] else a/'ACCEPTANCE.json';old=path.read_bytes()
 if kind in ['payload','manifest']:path.write_bytes(old+b' ')
 else:
  obj=json.loads(old)
  if kind=='accepted_chain':obj['full_package_reviews'][0]['completed_utc']='2001-01-01T00:00:00+00:00'
  else:obj['exact_claim']='changed theorem'
  path.write_bytes(enc(obj))
 reject('postacceptance_'+kind+'_drift',lambda:N['accepted_package'](ctx));path.write_bytes(old)
# Complete real guard + real merge flow; only transport and premerge source gate are fake.
current={'number':946,'state':'OPEN','isDraft':True,'baseRefName':'main','headRefOid':N['HEAD'],'body':'mock','mergeCommit':None};calls=[]
N['pr_view']=lambda:copy.deepcopy(current);N['premerge_gate']=lambda *args,**kw:(copy.deepcopy(current),'a'*40,{},exp);N['merged_gate']=lambda *args:{'merge_commit':'b'*40}
def ready(argv,**kw):
 assert argv[:3]==['gh','pr','ready'];calls.append('ready');current['isDraft']=False;adverse('adverse');return types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
N['subprocess'].run=ready;reject('newadverse_after_ready_prevents_merge',lambda:N['merge'](types.SimpleNamespace(),ctx),'supplied reviews must account');assert calls==['ready'];clear()
# Kit guards re-run after initial accepted_package and immediately before captured kit dispatch.
realcopy=N['runtime_upload_copy'];N['subprocess'].run=forbidden
for action in ['stage','publish','inspect']:
 descriptor,expected=N['descriptor_check'](F);(d/'ZENODO_STAGE.json').write_bytes(enc({'id':123,'state':'ready_to_publish','files':expected}))
 def latecopy(f):result=realcopy(f);adverse();return result
 N['runtime_upload_copy']=latecopy;reject('newpending_before_kit_'+action,lambda action=action:N['zenodo'](types.SimpleNamespace(action=action),ctx),'supplied reviews must account');clear()
N['runtime_upload_copy']=realcopy
# Tracker guard runs after preparing intent and before the only append request.
pub={'id':123,'doi':'10.5281/zenodo.123','record_url':'https://zenodo.org/records/123'};merge={'number':946,'state':'MERGED','isDraft':False,'baseRefName':'main','headRefOid':N['HEAD'],'mergeCommit':{'oid':'b'*40}};N['publication_links']=lambda *args:(pub,merge);tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['p','','d','note']};(a/'TRACKER_RECEIPT.json').write_bytes(enc(tracker));(a/'NATIVE_PUBLICATION_RECEIPT.json').unlink(missing_ok=True)
real_save=N['save']
def late_save(path,value,**kw):
 real_save(path,value,**kw)
 if Path(path).name in ['TRACKER_APPEND_INTENT.json','PR_FINAL_METADATA_INTENT.json'] or ('NATIVE_PUBLICATION_CAS_' in Path(path).name and 'INTENT' in Path(path).name):adverse()
N['save']=late_save
N['gws']=lambda args: {'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]} if args[1:3]==['spreadsheets','get'] else {'values':[['Original Problem','Solution Chat URL','DOI','Notes']]} if args[3]=='get' else forbidden(args)
reject('newpending_immediately_before_tracker_append',lambda:N['tracker_append'](types.SimpleNamespace(),ctx),'supplied reviews must account');clear()
# Native mutation is stopped at the real shared guard after an actual synthetic tree/intent.
N['pr_view']=lambda:copy.deepcopy(merge);N['remote_main']=lambda:'c'*40;parents=[];N['source_gate']=lambda parent:parents.append(parent) or {'fresh_parent':parent};queue=S['immutable_queue_row'].encode();N['blob']=lambda parent,name:orig_blob(parent,name) if name in originals else {N['QUEUE']:queue,N['STATE']:b'{"other" : {"keep": [1,2]}}\n',N['HISTORY']:b'{"old":"keep"}\n'}[name];N['explicit_tree']=lambda *args:'d'*40
N['run']=lambda argv,**kw: orig_run(argv,**kw) if argv[:2]==['git','ls-tree'] else '\n'.join([N['QUEUE'],N['STATE'],N['HISTORY']]) if argv[:3]==['git','diff','--name-only'] else 'e'*40 if argv[:2]==['git','commit-tree'] else '' if argv[:3]==['git','merge-base','--is-ancestor'] else forbidden(argv)
reject('newpending_immediately_before_native_push',lambda:N['native_write'](types.SimpleNamespace(),ctx),'supplied reviews must account');assert parents==['c'*40];clear()
# Explicit CAS rejection followed by new review prevents second push while refreshing each parent.
N['save']=real_save;parents.clear();pushes=[];seq=iter(['c'*40,'d'*40]);N['remote_main']=lambda:next(seq)
def fakepush(argv,**kw):pushes.append(argv);adverse();return types.SimpleNamespace(returncode=1,stdout='',stderr='rejected non-fast-forward')
N['subprocess'].run=fakepush;reject('newpending_after_first_CAS_rejection_prevents_second_push',lambda:N['native_write'](types.SimpleNamespace(),ctx),'supplied reviews must account');assert len(pushes)==1 and parents==['c'*40,'d'*40];clear()
# Final metadata edit guard after native/tracker verification and intent.
N['subprocess'].run=forbidden;N['save']=late_save;(a/'NATIVE_PUBLICATION_RECEIPT.json').write_bytes(enc({'commit':'e'*40}));N['native_verify']=lambda *args:{'status':'PASS','synthetic':True};N['gws']=lambda args:{'range':tracker['updated_range'],'values':[tracker['row']]};N['pr_view']=lambda:{**merge,'body':(D/'ORIGINAL_PR_DESCRIPTION.md').read_text(),'title':'old'}
reject('newpending_immediately_before_final_PR_edit',lambda:N['finalize'](types.SimpleNamespace(),ctx),'supplied reviews must account');clear()
# Adversarial final-state window: a new review appears during the status-only next gate,
# after the last existing chain guard and before CURRENT_STATE/inventory writes.
N['save']=real_save;N['subprocess'].run=lambda argv,**kw:types.SimpleNamespace(returncode=0,stdout='fake edit',stderr='');count=[0]
def finalview():
 count[0]+=1
 return {**merge,'body':(D/'ORIGINAL_PR_DESCRIPTION.md').read_text() if count[0]==1 else (a/'PR_PUBLISHED_BODY.md').read_text(),'title':'old' if count[0]==1 else '6000001: accepted global Hessian construction and published preprint'}
N['pr_view']=finalview
for q in [p/'README.md',p/'RESEARCH_LOG.md',a/'RESEARCH_LOG.md']:q.write_text('Synthetic final-state fixture.\n')
(p/'CURRENT_STATE.json').write_bytes(enc({'active_pr':946,'eligible_prs':[946,947],'completed_prs':[],'completed_results':[],'portable_release_tooling':'old'}));(p/'inventory.json').write_bytes(enc([{'number':946},{'number':947}]))
def late_next(inventory,state):
 adverse();return [],{'number':947,'problem_id':'synthetic947','headRefOid':'f'*40}
N['gate_next']=late_next
with contextlib.redirect_stdout(io.StringIO()):N['finalize'](types.SimpleNamespace(),ctx)
finalstate=json.loads((p/'CURRENT_STATE.json').read_bytes());assert finalstate['active_pr']==947 and 946 in finalstate['completed_prs'] and extra.exists()
cases.append({'case':'DEFECT_newpending_during_next_status_gate_allows_final_state_update','defect_reproduced':True,'pending_review':'full_package_04','active_pr_written':947,'completed_pr_written':946,'service_boundaries_fake':True,'shared_guard_and_finalization_flow_unmocked':True})
reject('same_newpending_is_rejected_by_guard_after_final_state_write',lambda:N['accepted_package'](ctx),'supplied reviews must account')
clear()
# Already-finalized recovery has the same post-guard read window.
N['pr_view']=lambda:{**merge,'body':(a/'PR_PUBLISHED_BODY.md').read_text(),'title':'6000001: accepted global Hessian construction and published preprint'}
real_load=N['load']
def late_state_load(path):
 result=real_load(path)
 if Path(path)==p/'CURRENT_STATE.json':adverse()
 return result
N['load']=late_state_load
with contextlib.redirect_stdout(io.StringIO()) as output:N['finalize'](types.SimpleNamespace(),ctx)
assert json.loads(output.getvalue())['already_finalized'] is True and extra.exists()
cases.append({'case':'DEFECT_newpending_during_state_read_allows_already_finalized_return','defect_reproduced':True,'pending_review':'full_package_04','already_finalized_acknowledged':True})
N['load']=real_load;reject('pending_after_early_return_is_rejected_by_shared_guard',lambda:N['accepted_package'](ctx),'supplied reviews must account');clear()
# No real Git/gh/gws/kit command was reachable from any fixture.
report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'core_sha256':fp(b)['sha256'],'cases':cases,'control_count':len(cases),'full_actual_chain_historical_freezes_archives_all33_and_current_candidate_authenticated':True,'earlier_manifest_pins':specs[:2],'synthetic_terminal_review_and_service_data_explicit':True,'shared_accepted_package_review_check_and_mergeflow_unmocked':True,'Git_transport_service_boundaries_mocked':True,'actual_external_actions':0,'new_proof_responses':0}
(O/'ACTION_CHAIN_CONTROLS.json').write_bytes(enc(report));print(json.dumps({'status':'PASS','controls':len(cases),'external_actions':0}))

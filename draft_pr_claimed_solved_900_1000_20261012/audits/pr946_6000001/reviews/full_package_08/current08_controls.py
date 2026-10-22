"""Independent actual candidate06 directory fixture. All service/Git calls fake.
The terminal review is synthetic contract data, never production approval.
The actual capture/freeze/original/archive/review/accepted-state guards execute.
"""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B at optimization zero')
import json,hashlib,copy,shutil,types,contextlib,io,datetime
from pathlib import Path
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint';O=A/'reviews/full_package_08'
fp=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};enc=lambda o:(json.dumps(o,indent=2)+'\n').encode()
F=json.loads((D/'FREEZE.json').read_bytes());FP=fp((D/'FREEZE.json').read_bytes())['sha256'];assert FP=='9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1'
raw=(P/'accept_pr946.py').read_bytes();assert fp(raw)['sha256']=='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7'
N={'__name__':'_full05_authenticated_subject_','__file__':str(P/'accept_pr946.py')};exec(compile(raw,N['__file__'],'exec'),N)
root=O/'private/current08_context'
if root.exists():shutil.rmtree(root)
p=root/P.name;a=p/'audits/pr946_6000001';d=a/'preprint';d.mkdir(parents=True);(a/'reviews').mkdir()
import ctypes,os
def cp(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if ctypes.CDLL(None,use_errno=True).clonefile(os.fsencode(src),os.fsencode(dst),0)!=0:dst.write_bytes(src.read_bytes())
 dst.chmod(0o644)
for name in ['FREEZE.json',*F['files']]:cp(D/name,d/name)
for name in F['evidence_files']:cp(R/name,root/name)
cp(A/'OPERATIONS_INVENTORY.json',a/'OPERATIONS_INVENTORY.json');I=json.loads((a/'OPERATIONS_INVENTORY.json').read_bytes())
for name in I['files']:cp(R/name,root/name)
seals=['2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834','e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6','28f08795caf265a412463b3b30880f29bcbc615eb84baf4b92010d1720326370','7fb99b465473a17ad54a363c4ee6f410023b3857343a5df2c356a705d50180d0','4d60602995d799a0850c4657b3401ad9c353460800f1fbd752c532b73b6963b2','1c75fc274754826a9d189a7e5e5ac206782deddd0a91dc75d0636d9aa787de71','eb55f996d2149104316d840103b641b104e60b371a7d6bef5202aa117406898d']
prior=set()
for num,seal in enumerate(seals,1):
 w=A/'reviews'/f'full_package_{num:02d}';mb=(w/'MANIFEST.json').read_bytes();assert fp(mb)['sha256']==seal;m=json.loads(mb)
 for name,pin in m['files'].items():assert fp((w/name).read_bytes())==pin;cp(w/name,a/'reviews'/w.name/name)
 cp(w/'MANIFEST.json',a/'reviews'/w.name/'MANIFEST.json')
 r=json.loads((w/'RESULT.json').read_bytes());prior.update(x['id'] for x in r['required_issues']+r['optional_issues']);prior.update(r['prior_issue_resolution'])
 if num>=6:continue
 old=D/'reviewed_candidates'/f'candidate{num:02d}';of=json.loads((old/'FREEZE.json').read_bytes());dest=d/'reviewed_candidates'/old.name
 for name in ['FREEZE.json','OPERATIONS_INVENTORY.json',*of['files']]:cp(old/name,dest/name)
 oi=json.loads((old/'OPERATIONS_INVENTORY.json').read_bytes())
 for name in oi['files']:cp(old/'operations'/name,dest/'operations'/name)
S=json.loads((O/'AUTHENTICATION_START.json').read_bytes());originals=S['originals']
for name in originals:cp(A/'original'/name,a/'original'/name)
N.update(ROOT=root,P=p,A=a,D=d);N['freeze_check'].__defaults__=(d,False);N['archive_check'].__defaults__=(d,)
def forbidden(*args,**kw):raise RuntimeError('FAKE TRANSPORT REJECTED '+repr(args))
def oblob(ref,name):
 assert ref==N['HEAD'],ref
 return (a/'original'/name).read_bytes()
def orun(argv,**kw):
 if argv[:2]==['git','ls-tree'] and argv[-1] in originals:return '100644 blob '+originals[argv[-1]]['git_blob']+'\t'+argv[-1]+'\n'
 return forbidden(argv)
N.update(blob=oblob,run=orun,remote_main=forbidden,subprocess=types.SimpleNamespace(run=forbidden))
ctx=N['capture_inventory'](F['operations_inventory_sha256']);freeze=N['freeze_check']((d/'FREEZE.json').read_bytes(),FP,ctx);_,exp=N['original_check']()
w=a/'reviews/full_package_08';w.mkdir();now=datetime.datetime.now(datetime.timezone.utc);ts=[(now+datetime.timedelta(microseconds=i)).isoformat() for i in range(5)]
claim='SYNTHETIC terminal contract theorem. Not production acceptance.'
r={'pr':946,'problem_id':'6000001','original_pr_head':N['HEAD'],'reviewer_agent_id':'SYNTHETIC_FULL08_CURRENT_CONTEXT','clean_context':True,'full_reproducer_completed':True,'started_utc':ts[0],'completed_utc':ts[4],'candidate_revision':6,'candidate_pins':{'freeze':FP,'manifest':F['package_manifest_sha256'],'pdf':F['files']['research_note.pdf']['sha256']},'inspected_helper_hashes':F['future_helpers'],'required_issues':[],'optional_issues':[],'clean_for_preprint':True,'mathematical_remaining_gap_for_stated_theorem':None,'strongest_verified_theorem':claim,'prior_issue_resolution':{k:{'verified':True,'resolution':'Synthetic contract only.'} for k in prior}}
s=copy.deepcopy(S);s['utc']=ts[1];e=copy.deepcopy(S);e['utc']=ts[3];c=json.loads((O/'COLD_REPLAY.json').read_bytes());c['utc']=ts[2]
for name,o in [('RESULT.json',r),('AUTHENTICATION_START.json',s),('AUTHENTICATION_END.json',e),('COLD_REPLAY.json',c)]: (w/name).write_bytes(enc(o))
(w/'FULL_AUDIT.md').write_text('Synthetic terminal fixture only.\n');(w/'RESEARCH_LOG.md').write_text('Synthetic terminal fixture only.\n')
def reseal():
 fs={q.name:fp(q.read_bytes()) for q in w.iterdir() if q.name!='MANIFEST.json'};mb=enc({'files':fs,'explicit_public_allowlist':sorted(fs)});(w/'MANIFEST.json').write_bytes(mb);return fp(mb)['sha256']
specs=[f'{num:02d}:'+seal for num,seal in enumerate(seals,1)]+['08:'+reseal()]
rows,latest=N['review_check'](specs,freeze,FP,ctx,exp)
accepted={'accepted':True,'pr':946,'problem_id':'6000001','original_pr_head':N['HEAD'],'operations_inventory_sha256':ctx['inventory_sha256'],'full_package_reviews':rows,'all_prior_required_and_optional_findings_resolved':True,'proof_gap':None,'freeze_sha256':FP,'files':F['files'],'future_helpers':F['future_helpers'],'exact_claim':claim}
(a/'ACCEPTANCE.json').write_bytes(enc(accepted));cases=[];findings=[]
def call(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def good(name,fn):call(fn);cases.append({'case':name,'pass':True})
def bad(name,fn,reason=None):
 try:call(fn)
 except (RuntimeError,OSError,ValueError,KeyError) as ex:
  msg=str(ex);assert 'FAKE TRANSPORT REJECTED' not in msg,(name,msg)
  if reason:assert reason in msg,(name,msg)
  cases.append({'case':name,'rejected':True,'reason':msg[:400]});return
 
 raise RuntimeError('INVALID ACCEPTED '+name)
good('current06_all_seven_actual_prior_seals_and_current_synthetic08',lambda:N['accepted_package'](ctx))
canonical={a/'ACCEPTANCE.json':(a/'ACCEPTANCE.json').read_bytes(),d/'FREEZE.json':(d/'FREEZE.json').read_bytes(),d/'research_note.tex':(d/'research_note.tex').read_bytes(),w/'FULL_AUDIT.md':(w/'FULL_AUDIT.md').read_bytes(),w/'MANIFEST.json':(w/'MANIFEST.json').read_bytes(),p/'accept_pr946.py':(p/'accept_pr946.py').read_bytes(),a/'OPERATIONS_INVENTORY.json':(a/'OPERATIONS_INVENTORY.json').read_bytes(),root/next(iter(F['evidence_files'])):(root/next(iter(F['evidence_files']))).read_bytes()}
extra=a/'reviews/full_package_09'
def inject(kind):
 if kind in ['pending','adverse']:
  extra.mkdir()
  if kind=='adverse':(extra/'RESULT.json').write_bytes(enc({'required_issues':[{'id':'SYNTHETIC_ADVERSE'}]}))
 elif kind in ['acceptance_revoked','theorem','review_record']:
  obj=json.loads(canonical[a/'ACCEPTANCE.json'])
  if kind=='acceptance_revoked':obj['accepted']=False
  elif kind=='theorem':obj['exact_claim']='WITHDRAWN'
  else:obj['full_package_reviews'][0]['public_files_authenticated']=0
  (a/'ACCEPTANCE.json').write_bytes(enc(obj))
 else:
  path={'tex':d/'research_note.tex','freeze':d/'FREEZE.json','payload':w/'FULL_AUDIT.md','seal':w/'MANIFEST.json','core':p/'accept_pr946.py','inventory':a/'OPERATIONS_INVENTORY.json','evidence':root/next(iter(F['evidence_files']))}[kind];path.write_bytes(canonical[path]+b'\n')
def restore():
 if extra.exists():shutil.rmtree(extra)
 for path,b in canonical.items():path.write_bytes(b)
 for path in list(a.glob('*INTENT.json'))+list(a.glob('PR_*ACTION*.json'))+list(d.glob('ZENODO_*INTENT.json')):path.unlink(missing_ok=True)
actual_original=N['original_check'];actual_review=N['review_check']
kinds=['pending','adverse','acceptance_revoked','theorem','review_record','tex','freeze','payload','seal','core','inventory','evidence']
for window in ['entry','after_original_read','after_full_review_read']:
 for kind in kinds:
  fired=[False]
  def hit():
   if not fired[0]:fired[0]=True;inject(kind)
  def original_hook(*args,**kw):
   result=actual_original(*args,**kw)
   if window=='after_original_read':hit()
   return result
  def review_hook(*args,**kw):
   result=actual_review(*args,**kw)
   if window=='after_full_review_read':hit()
   return result
  N['original_check']=original_hook;N['review_check']=review_hook
  if window=='entry':hit()
  bad(window+'_'+kind,lambda:N['accepted_review_check'](accepted,freeze,ctx));assert fired[0];restore()
N['original_check']=actual_original;N['review_check']=actual_review
good('guard_restored_after_all_source_history_read_injections',lambda:N['accepted_package'](ctx))
# Actual per-action control flow and shared guards, with fake source/service readbacks.
current={'number':946,'state':'OPEN','isDraft':True,'baseRefName':'main','headRefOid':N['HEAD'],'body':(D/'ORIGINAL_PR_DESCRIPTION.md').read_text(),'title':'original','mergeCommit':None};dispatch=[]
N['pr_view']=lambda:copy.deepcopy(current);N['premerge_gate']=lambda *args,**kw:(copy.deepcopy(current),'a'*40,{},exp);N['merged_gate']=lambda *args:{'merge_commit':'b'*40}
def fake_ready(argv,**kw):
 dispatch.append(argv[:3]);assert argv[:3]==['gh','pr','ready'];current['isDraft']=False;inject('acceptance_revoked');return types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
N['subprocess'].run=fake_ready;bad('revocation_after_ready_before_merge',lambda:N['merge'](types.SimpleNamespace(),ctx));assert dispatch==[['gh','pr','ready']];restore()
real_copy=N['runtime_upload_copy'];descriptor,expected=N['descriptor_check'](freeze)
for action in ['stage','publish','inspect']:
 for kind in ['pending','acceptance_revoked','tex','core']:
  (d/'ZENODO_STAGE.json').write_bytes(enc({'id':123,'state':'ready_to_publish','files':expected}))
  def latecopy(f):value=real_copy(f);inject(kind);return value
  N['runtime_upload_copy']=latecopy;N['subprocess'].run=forbidden;bad('before_kit_'+action+'_'+kind,lambda:N['zenodo'](types.SimpleNamespace(action=action),ctx));restore()
N['runtime_upload_copy']=real_copy
pub={'id':123,'doi':'10.5281/zenodo.123','record_url':'https://zenodo.org/records/123'};merge={**current,'state':'MERGED','isDraft':False,'mergeCommit':{'oid':'b'*40}};tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['p','','https://doi.org/10.5281/zenodo.123','note']}
N['publication_links']=lambda *args:(pub,merge);N['pr_view']=lambda:copy.deepcopy(merge);N['native_verify']=lambda *args:{'status':'PASS','synthetic':True};real_save=N['save'];real_load=N['load'];real_next=N['gate_next']
(a/'TRACKER_RECEIPT.json').write_bytes(enc(tracker));(a/'NATIVE_PUBLICATION_RECEIPT.json').write_bytes(enc({'commit':'e'*40}))
N['gws']=lambda argv:{'range':tracker['updated_range'],'values':[tracker['row']]}
base_state={'active_pr':946,'active_problem_id':'6000001','eligible_prs':[946,947],'completed_prs':[],'completed_results':[]}
for window in ['next_status_reads','already_finalized_state_read']:
 for kind in ['valid',*kinds]:
  restore();state=copy.deepcopy(base_state);recover=window=='already_finalized_state_read'
  if recover:state.update(active_pr=947,completed_prs=[946],completed_results=[{'pr':946,'outcome':'accepted_merged_preprint_published'}])
  (p/'CURRENT_STATE.json').write_bytes(enc(state));(p/'inventory.json').write_bytes(enc([{'number':946},{'number':947,'entries':[{'id':'SYNTHETIC947'}]}]))
  for path in [p/'README.md',p/'RESEARCH_LOG.md',a/'RESEARCH_LOG.md']:path.write_text('Synthetic local completion fixture.\n')
  def late_load(path):
   value=real_load(path)
   if Path(path)==p/'CURRENT_STATE.json' and recover and kind!='valid':inject(kind)
   return value
  def f_run(argv,**kw):
   if argv[:2]==['git','ls-tree']:return orun(argv,**kw)
   if argv[:4]==['gh','pr','view','947']:return json.dumps({'number':947,'state':'OPEN','isDraft':True,'headRefOid':'f'*40,'baseRefName':'main'})
   if argv[:2]==['gh','api']:return b'| 1 | SYNTHETIC947 / fixture | title | 0 | 0 | 0 | 0 | claimed_solved | 1/5 | | | |\n'
   return forbidden(argv)
  def late_next(inventory,state):
   value=real_next(inventory,state)
   if kind!='valid':inject(kind)
   return value
  N.update(load=late_load,run=f_run,gate_next=late_next);views=[0];dispatch=[]
  def view():
   views[0]+=1;final=recover or views[0]>1
   return {**merge,'body':(a/'PR_PUBLISHED_BODY.md').read_text() if final else (D/'ORIGINAL_PR_DESCRIPTION.md').read_text(),'title':'6000001: accepted global Hessian construction and published preprint' if final else 'original'}
  N['pr_view']=view;N['subprocess'].run=lambda argv,**kw:dispatch.append(argv[:3]) or types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
  if kind=='valid':good(window+'_valid_completion_or_recovery',lambda:N['finalize'](types.SimpleNamespace(),ctx))
  else:bad(window+'_'+kind,lambda:N['finalize'](types.SimpleNamespace(),ctx));assert json.loads((p/'CURRENT_STATE.json').read_bytes())==state
N.update(load=real_load,run=orun,gate_next=real_next);restore()
# Acceptance itself: drift during its final source reread must not silently approve stale bytes.
(a/'ACCEPTANCE.json').unlink();calls=[0]
def final_gate_drift(*args,**kw):
 calls[0]+=1
 if calls[0]==2:inject('tex')
 return copy.deepcopy(current),'a'*40,{},exp
N['premerge_gate']=final_gate_drift
error=None
try:call(lambda:N['accept'](types.SimpleNamespace(freeze=FP,review=specs),ctx))
except (RuntimeError,OSError,ValueError,KeyError) as ex:error=str(ex)
if error is None:
 assert (a/'ACCEPTANCE.json').exists();findings.append({'id':'FP05-OPS-001','case':'initial_acceptance_final_source_read_candidate_drift','acceptance_written':True,'current_tex_differs_from_frozen':True,'description':'accept() runs final premerge/source/original reads after full review and then writes ACCEPTANCE without refreshing current inventory/FREEZE/files. A deterministic current TeX change during this final read is approved as the old freeze. Later accepted_package rejects it, so external follow-on mutations remain blocked.'})
 cases.append({'case':'initial_acceptance_final_source_read_candidate_drift','defect_reproduced':True})
else:cases.append({'case':'initial_acceptance_final_source_read_candidate_drift','rejected':True,'reason':error})
restore();good('current06_positive_restored_complete_chain',lambda:N['accepted_package'](ctx))
out={'status':'FINDINGS_REPRODUCED' if findings else 'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'subject_candidate_revision':6,'subject_core_sha256':fp(raw)['sha256'],'fixture_current_inventory_sha256':ctx['inventory_sha256'],'actual_current06_context':True,'historical_actual_seals':seals,'terminal_review_explicitly_synthetic':True,'adapted_source_sha256':'84c13466620b91bd56468832da9443e7d1b28e24c14c12a37fc170412b7619c5','guards_unstubbed':['capture_inventory','freeze_check','archive_check','original_check','review_check','accepted_package','accepted_state_check','accepted_review_check'],'fake_boundaries':['Git transport','premerge source/service responses for action-flow tests','publication_links/native_verify for isolated completion tests','GWS','subprocess external dispatch'],'cases':cases,'case_count':len(cases),'findings':findings,'actual_external_mutations':0,'no_OS_atomicity_claim':True}
(O/'CURRENT08_CONTROLS.json').write_bytes(enc(out));print(json.dumps({'status':out['status'],'cases':len(cases),'findings':findings,'external_mutations':0}))

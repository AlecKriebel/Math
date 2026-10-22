from pathlib import Path
import copy,hashlib,importlib.util,json,shutil,sys,datetime,zipfile
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';C=R/'_local/controls'
def load(n):
 spec=importlib.util.spec_from_file_location('round2_'+n,P/(n+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
def update_case(name,change=None,receipt=True,expect_fail=True):
 case=C/name
 if case.exists():shutil.rmtree(case)
 root=case/'publication';root.mkdir(parents=True,exist_ok=True)
 m=load('update_pr_publication');m.ROOT=root
 for n in ['BUILD_RECEIPT.json','zenodo-deposit.json','Polynomial_Multipliers_Note_v1.0.pdf','Polynomial_Multipliers_Verification_v1.0.zip']:
  shutil.copyfile(P/n,root/n)
 with zipfile.ZipFile(P/'Polynomial_Multipliers_Verification_v1.0.zip') as z:
  (root.parent/'SUBMITTED_SNAPSHOT.json').write_bytes(z.read('provenance/SUBMITTED_SNAPSHOT.json'))
  for n in ['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']:
   q=root.parent/'current_edition'/n;q.parent.mkdir(exist_ok=True);q.write_bytes(z.read('current_edition/'+n))
 build=json.loads((root/'BUILD_RECEIPT.json').read_text());meta=json.loads((root/'zenodo-deposit.json').read_text())['metadata']
 pub={'state':'published','metadata_normalizations':[],'title':meta['title'],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','files':[{'name':build[k]['path'],'sha256':build[k]['sha256'],'size':build[k]['bytes']} for k in ['pdf','verification_zip']]}
 tracker={'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','gid':1254632077,'updatedRange':"'Math Puzzles'!A9:D9",'row':['30000921','','https://doi.org/10.5281/zenodo.123','intended note'],'readback_verified':True}
 public={'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_manifest_sha256':sha(root/'zenodo-deposit.json'),'doi':pub['doi'],'id':pub['id'],'files':[{'name':build[k]['path'],'bytes':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]}
 workflow=['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']
 for n in workflow:
  q=root/n;q.parent.mkdir(exist_ok=True);shutil.copyfile(P/n,q)
 gate={'status':'pass','pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':sha(root/'zenodo-deposit.json'),'workflow':{n:sha(root/n) for n in workflow}}
 for n,d in [('PUBLICATION_RECEIPT.json',pub),('tracker/TRACKER_RECEIPT.json',tracker),('PUBLIC_DOWNLOAD_VERIFICATION.json',public),('FINAL_REVIEW_GATE.json',gate)]:put(root/n,d)
 snapshot=json.loads((root.parent/'SUBMITTED_SNAPSHOT.json').read_text())
 files,publication,note=m.desired_files(build,pub,tracker,snapshot);wanted=m.expected_identity(pub,tracker,files)
 commit='a'*40;intent={**wanted,'commit':commit}
 put(root/'PR_BRANCH_INTENT.json',intent)
 if receipt:put(root/'PR_BRANCH_RECEIPT.json',{**intent,'remote_readback_verified':True})
 state={'mode':'valid','head':commit if receipt else m.ORIGINAL,'remote':commit if receipt else m.ORIGINAL,'body':'original','pushes':0,'files':files}
 # Hash matching the archived original body without needing its undistributed bytes.
 orig_digest=snapshot['body_sha256'];real_hash=m.hashlib.sha256
 class HashWrap:
  def __init__(self,data=b''):
   self.data=data;self.inner=real_hash(data)
  def hexdigest(self):return orig_digest if self.data==b'original' else self.inner.hexdigest()
  def digest(self):return self.inner.digest()
 m.hashlib=type('Hashes',(),{'sha256':staticmethod(HashWrap)})
 def git(*args,data=None):
  cmd=args[0]
  if cmd=='branch':return b'main\n'
  if cmd=='rev-list':return (commit+' '+('b'*40 if state['mode']=='parent' else m.ORIGINAL)+'\n').encode()
  if cmd=='diff-tree':return ('\n'.join(sorted(files)+(['foreign'] if state['mode']=='paths' else []))+'\n').encode()
  if cmd=='show':return b'wrong' if state['mode']=='treebytes' else files[args[1].split(':',1)[1]]
  if cmd=='ls-remote':return (state['remote']+'\trefs/heads/'+m.BRANCH+'\n').encode()
  if cmd=='push':state['pushes']+=1;state['remote']=commit;state['head']=commit;return b''
  raise RuntimeError('Unmocked Git operation '+str(args))
 m.git=git;m.pr=lambda:{'headRefOid':state['head'],'headRefName':m.BRANCH,'state':'OPEN','body':state['body']}
 if change:change(root,state)
 try:m.main();outcome='accepted';error=None
 except Exception as e:outcome='rejected';error=type(e).__name__+': '+str(e)
 results.append({'case':name,'outcome':outcome,'pushes':state['pushes'],'error':error,'expected_rejection':expect_fail,'unexpected':(outcome=='rejected')!=expect_fail})

def mutate_json(path,key,value):
 d=json.loads(path.read_text());d[key]=value;put(path,d)
update_case('valid_saved',expect_fail=False)
update_case('stale_intent_doi',lambda r,s:mutate_json(r/'PR_BRANCH_INTENT.json','doi','stale'))
update_case('missing_intent',lambda r,s:(r/'PR_BRANCH_INTENT.json').unlink())
update_case('bad_parent',lambda r,s:s.update(mode='parent'))
update_case('bad_tree_paths',lambda r,s:s.update(mode='paths'))
update_case('bad_tree_bytes',lambda r,s:s.update(mode='treebytes'))
update_case('bad_public_record_id',lambda r,s:mutate_json(r/'PUBLIC_DOWNLOAD_VERIFICATION.json','id',124))
update_case('bad_public_record_doi',lambda r,s:mutate_json(r/'PUBLIC_DOWNLOAD_VERIFICATION.json','doi','stale'))
update_case('missing_public_receipt',lambda r,s:(r/'PUBLIC_DOWNLOAD_VERIFICATION.json').unlink())
update_case('bad_source_snapshot',lambda r,s:(r.parent/'SUBMITTED_SNAPSHOT.json').write_text('{}'))
update_case('bad_current_source',lambda r,s:(r.parent/'current_edition/PROOF.md').write_text('wrong'))
update_case('workflow_drift',lambda r,s:(r/'append_tracker.py').write_text('wrong'))
update_case('bad_tracker_doi',lambda r,s:mutate_json(r/'tracker/TRACKER_RECEIPT.json','row',['30000921','','wrong','note']))
# These are deliberately stale/local record probes; saved identities are regenerated
# only where needed to isolate main's validation, just as a new initial intent would.
def reseal(r,s):
 m=load('update_pr_publication');m.ROOT=r
 b=json.loads((r/'BUILD_RECEIPT.json').read_text());p=json.loads((r/'PUBLICATION_RECEIPT.json').read_text());t=json.loads((r/'tracker/TRACKER_RECEIPT.json').read_text());sn=json.loads((r.parent/'SUBMITTED_SNAPSHOT.json').read_text())
 f,_,_=m.desired_files(b,p,t,sn);s['files'].clear();s['files'].update(f)
 it={**m.expected_identity(p,t,f),'commit':'a'*40};put(r/'PR_BRANCH_INTENT.json',it);put(r/'PR_BRANCH_RECEIPT.json',it)
def wrong_notes(r,s):
 t=json.loads((r/'tracker/TRACKER_RECEIPT.json').read_text());t['row'][3]='Unrelated false publication notes';put(r/'tracker/TRACKER_RECEIPT.json',t);reseal(r,s)
def wrong_urls(r,s):
 p=json.loads((r/'PUBLICATION_RECEIPT.json').read_text());p['doi_url']='https://doi.org/10.5281/zenodo.999';p['record_url']='https://zenodo.org/records/999';put(r/'PUBLICATION_RECEIPT.json',p)
 t=json.loads((r/'tracker/TRACKER_RECEIPT.json').read_text());t['row'][2]=p['doi_url'];put(r/'tracker/TRACKER_RECEIPT.json',t);reseal(r,s)
def missing_workflow(r,s):
 g=json.loads((r/'FINAL_REVIEW_GATE.json').read_text());g['workflow']={};put(r/'FINAL_REVIEW_GATE.json',g);(r/'append_tracker.py').write_text('changed workflow');reseal(r,s)
update_case('bad_tracker_notes_resealed',wrong_notes)
update_case('mismatched_doi_record_urls_resealed',wrong_urls)
update_case('missing_workflow_gate_resealed',missing_workflow)
update_case('successful_retry_original_body',receipt=False,expect_fail=False)
(R/'OFFLINE_GUARD_RECEIPT.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'limits':'All Git/gh mocked; no external action. Fixtures use exact reviewed package artifacts and current source bytes. Resealed probes isolate omissions in main validation rather than testing resistance to arbitrary forged trusted receipts.'},indent=2)+'\n')
print(json.dumps(results,indent=2))

"""Independent exact-source, synthetic-provider controls. NO RELEASE AUTHORITY.

Only module provider objects and native path globals are substituted. Candidate
functions, source text and AST are not rewritten. Every write is below this file.
"""
from pathlib import Path
import sys,json,hashlib,datetime,shutil,types,subprocess,base64,io,contextlib,traceback,zipfile,copy,http.client,os

D=Path(__file__).resolve().parent
C=D.parent
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
sys.path.insert(0,str(D))
import release_binding as B
import integrate_reviewed_pr as I
import verify_and_merge as M
import publish_preprint as P
import append_verified_tracker as A
import verify_published_readonly as V
REAL_RUN=subprocess.run
REAL_REQUEST=V.urllib.request.Request
RESULTS=[]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def js(p,x):put(p,(json.dumps(x,indent=2)+'\n').encode())
def pin(p,base):return dict(path=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
def check(name,f):
 start=utc()
 try:
  value=f();r=dict(name=name,start_utc=start,end_utc=utc(),PASS=True,result=value)
 except Exception as e:
  r=dict(name=name,start_utc=start,end_utc=utc(),PASS=False,error=repr(e),traceback=traceback.format_exc())
 RESULTS.append(r);js(D/'RESULTS.json',RESULTS);print(json.dumps(r),flush=True)
def rejects(f,contains=None):
 try:f()
 except Exception as e:
  if contains:assert contains in str(e),(contains,str(e))
  return dict(rejected=True,error=repr(e))
 raise AssertionError('Unexpected acceptance')

class Provider:
 def __init__(self,r,pub,intake,q,prior,large=False):
  self.r,self.pub,self.intake,self.q=r,pub,intake,q
  self.calls=[];self.blobs={};self.trees={};self.commits={};self.refs={};self.rules=[]
  self.values=[B.HEADER.copy()];self.zenstate='ready_to_publish';self.id=987654321
  self.bad_range=False;self.duplicates=False;self.lose_append=False;self.lose_publish=False;self.lose_stage=False
  self.bad_download=False;self.partial_download=False;self.partial_binary=None;self.mutate_on_live=None
  self.protected=False;self.drop_metadata=False;self.main_advance=False;self.main_unknown=False
  self.queue=[B.HEADER.copy()]
  src=I.frozen_source(r);original={I.PREFIX+x['native_path'][len(I.PREFIX):]:src['pr_update/5100015/history/original_submission_20261016/'+x['native_path'][len(I.PREFIX):]] for x in intake['original_source_files']}
  original[I.QUEUE]=q
  oldtree=self.make_tree(original);self.commits[I.OLD]=dict(sha=I.OLD,tree=dict(sha=oldtree),parents=[])
  mainfiles={I.QUEUE:q,'foreign/keep.txt':b'foreign main must survive\n'}
  mt=self.make_tree(mainfiles);self.refs['main']=self.commit(mt,[])
  self.refs[I.BRANCH]=I.OLD
  self.pr=dict(number=209,state='open',draft=True,merged=False,mergeable=True,node_id='SYNTHETIC_NODE',html_url='https://example.invalid/SYNTHETIC/209',title='old',body='old',head=dict(sha=I.OLD,ref=I.BRANCH,repo=dict(full_name='AlecKriebel/Math')),base=dict(ref='main',repo=dict(full_name='AlecKriebel/Math')))
  baseline=json.loads((pub/'PROGRESS_BASELINE.json').read_bytes());checkpoint=json.loads((pub.parent/baseline['previous_native_checkpoint_receipt']['path']).read_bytes())
  accept=(pub.parent/baseline['previous_case_acceptance']['path']).read_bytes()
  row=[x for x in checkpoint['owned_files'] if x.get('sha256')==sha(accept) and x.get('bytes')==len(accept)][0]
  pt=self.make_tree({row['path']:accept});self.commits[checkpoint['commit']]=dict(sha=checkpoint['commit'],tree=dict(sha=pt),parents=[])
 def make_tree(self,files):
  root={}
  for path,raw in files.items():
   parts=path.split('/');at=root
   for x in parts[:-1]:at=at.setdefault(x,{})
   at[parts[-1]]=raw
  def build(node):
   rows=[]
   for n,v in sorted(node.items()):
    if isinstance(v,dict):key=build(v);mode,kind='040000','tree'
    else:key=I.blob(v);self.blobs[key]=v;mode,kind='100644','blob'
    rows.append(dict(path=n,mode=mode,type=kind,sha=key))
   key=sha(json.dumps(rows,sort_keys=True).encode())[:40];self.trees[key]=rows;return key
  return build(root)
 def flat(self,tree,pre=''):
  out={}
  for row in self.trees[tree]:
   if row['type']=='tree':out.update(self.flat(row['sha'],pre+row['path']+'/'))
   else:out[pre+row['path']]=self.blobs[row['sha']]
  return out
 def commit(self,tree,parents):
  key=sha(json.dumps([tree,parents,len(self.commits)]).encode())[:40]
  self.commits[key]=dict(sha=key,tree=dict(sha=tree),parents=[dict(sha=x) for x in parents]);return key
 def summary(self,state=None):
  m=json.loads((self.r/'metadata.json').read_bytes())
  files=[dict(name=x['name'],size=(self.r/x['path']).stat().st_size,sha256=sha((self.r/x['path']).read_bytes())) for x in B.EXPECTED_DEPOSIT_FILES]
  out=dict(environment='production',title=m['title'],files=files,id=self.id,state=state or self.zenstate,metadata_normalizations=[])
  if out['state']=='published':
   doi='10.5281/zenodo.'+str(self.id);url='https://doi.org/'+doi;record='https://zenodo.org/records/'+str(self.id)
   out.update(doi=doi,doi_url=url,record_url=record,doi_resolution=dict(status='resolved',http_status=200,url=url,resolved_url=record))
  return out
 def api(self,method,path,payload=None):
  self.calls.append(dict(provider='github',method=method,path=path,payload=payload,intents=[p.name for p in self.pub.glob('*ATTEMPT.json')]+[p.name for p in self.pub.glob('*INTENT.json')],global_main_intent=(self.pub/'NATIVE_MERGE_REQUEST.json').exists()))
  if method=='GET':
   if path=='pulls/209':
    self.pr['head']['sha']=self.refs[I.BRANCH];return copy.deepcopy(self.pr)
   if path.startswith('git/ref/heads/'):return dict(object=dict(sha=self.refs[path.removeprefix('git/ref/heads/')]))
   if path.startswith('git/commits/'):return copy.deepcopy(self.commits[path.split('/')[-1]])
   if path.startswith('git/trees/'):return dict(sha=path.split('/')[-1],truncated=False,tree=copy.deepcopy(self.trees[path.split('/')[-1]]))
   if path.startswith('git/blobs/'):
    key=path.split('/')[-1];raw=self.blobs[key];return dict(encoding='base64',sha=key,size=len(raw),content=base64.b64encode(raw).decode())
   if path.startswith('branches/'):return dict(protected=self.protected)
   if path.startswith('rules/branches/') or path=='rulesets':return self.rules
   if path.startswith('compare/'):
    left,right=path.removeprefix('compare/').split('...');return dict(status='ahead',merge_base_commit=dict(sha=left),files=[])
   if path.startswith('contents/'):
    return dict(content=base64.b64encode(self.q).decode())
  if method=='PATCH' and path.startswith('git/refs/heads/'):
   name=path.removeprefix('git/refs/heads/');assert payload['force'] is False
   self.refs[name]=payload['sha']
   if name=='main':
    self.pr.update(state='closed',draft=False,merged=True,merge_commit_sha=payload['sha'])
    if self.main_unknown:raise subprocess.TimeoutExpired('SYNTHETIC_MAIN_PATCH',1,output=b'\x00\xffmain-partial',stderr=b'partial-err')
   return dict(object=dict(sha=self.refs[name]))
  if method=='PATCH' and path=='pulls/209':
   if not self.drop_metadata:self.pr.update(payload)
   return copy.deepcopy(self.pr)
  if method=='POST' and path=='graphql':self.pr['draft']=False;return dict(data=dict(markPullRequestReadyForReview=dict(pullRequest=dict(id='SYNTHETIC_NODE',isDraft=False))))
  if method=='POST' and path=='git/blobs':
   raw=base64.b64decode(payload['content']);key=I.blob(raw);self.blobs[key]=raw;return dict(sha=key)
  if method=='POST' and path=='git/trees':
   files=self.flat(payload['base_tree'])
   for row in payload['tree']:files[row['path']]=row['content'].encode() if 'content'in row else self.blobs[row['sha']]
   return dict(sha=self.make_tree(files))
  if method=='POST' and path=='git/commits':return dict(sha=self.commit(payload['tree'],payload['parents']))
  raise AssertionError((method,path))
 def run(self,cmd,**kw):
  binary=not kw.get('text',False);payload=None
  if '--input'in cmd:payload=json.loads(Path(cmd[cmd.index('--input')+1]).read_bytes())
  if 'gh'==Path(cmd[0]).name:
   method=cmd[cmd.index('--method')+1] if '--method'in cmd else 'GET';path=cmd[cmd.index('--method')+2] if '--method'in cmd else cmd[2]
   path=path.removeprefix(I.API);result=self.api(method,path,payload)
  elif Path(cmd[0]).name=='gws':
   params=json.loads(cmd[cmd.index('--params')+1]);self.calls.append(dict(provider='gws',args=cmd[1:],params=params))
   if cmd[3]=='get' and cmd[2]=='spreadsheets':result=dict(spreadsheetId=B.SHEET,sheets=[dict(properties=dict(sheetId=B.SHEET_ID,title='Math Puzzles'))])
   elif 'append'in cmd:
    row=json.loads(cmd[cmd.index('--json')+1])['values'][0];self.values.append(row)
    if self.duplicates:self.values.append(row.copy())
    if self.lose_append:raise subprocess.TimeoutExpired('SYNTHETIC_GWS_APPEND',1,output=b'partial-append\xff',stderr=b'err')
    result=dict(spreadsheetId=B.SHEET,tableRange="'Math Puzzles'!A1:D1",updates=dict(updatedRange="'Math Puzzles'!A2:D2",updatedRows=1,updatedColumns=4,updatedCells=4,updatedData=dict(range="'Math Puzzles'!A2:D2",majorDimension='ROWS',values=[row])))
   else:
    target=params['range'];values=self.values if target==B.FULL_RANGE else self.values[1:2]
    result=dict(range=("'Wrong tab'!Z999:AC999" if self.bad_range else target),majorDimension=('COLUMNS' if self.bad_range else 'ROWS'),values=copy.deepcopy(values))
  elif len(cmd)>2 and Path(cmd[2]).name=='zenodo.py':
   operation=cmd[3];self.calls.append(dict(provider='zenodo',operation=operation,stage_intent=(self.pub/'STAGE_ATTEMPT.json').exists(),publish_intent=(self.pub/'PUBLISH_ATTEMPT.json').exists()))
   if operation=='stage' and self.lose_stage:raise subprocess.TimeoutExpired('SYNTHETIC_STAGE',1,output=b'partial-stage\xff')
   if operation=='publish':
    self.zenstate='published'
    if self.lose_publish:raise subprocess.TimeoutExpired('SYNTHETIC_PUBLISH',1,output=b'partial-publish\xff')
   result=self.summary()
   if operation=='check':result={k:result[k] for k in ['environment','title','files']}
   if operation=='inspect' and self.mutate_on_live:
    fn=self.mutate_on_live;self.mutate_on_live=None;fn()
  else:raise AssertionError(('Forbidden subprocess',cmd))
  raw=json.dumps(result).encode();return subprocess.CompletedProcess(cmd,0,raw if binary else raw.decode(),b'' if binary else '')
 def open(self,req,timeout):
  name=req.full_url.split('/files/')[1].split('?')[0]
  row=next(x for x in B.EXPECTED_DEPOSIT_FILES if x['name']==name);raw=(self.r/row['path']).read_bytes()
  self.calls.append(dict(provider='public_download',url=req.full_url,bytes=len(raw)))
  if self.bad_download:raw=b'BAD'+raw
  parent=self
  class Response:
   def __enter__(self):return self
   def __exit__(self,*a):pass
   def read(self,*a):
    if parent.partial_download:
     parent.partial_binary=raw[:17]+b'\x00\xff';raise http.client.IncompleteRead(parent.partial_binary,100)
    return raw
  return Response()
 def install(self):
  for mod in [P,A,V,I]:mod.subprocess=types.SimpleNamespace(run=self.run)
  V.urllib=types.SimpleNamespace(request=types.SimpleNamespace(Request=REAL_REQUEST,urlopen=self.open))
  I.ROOT=M.ROOT=self.pub.parent.parent;I.PUB=M.PUB=self.pub;I.R=M.R=self.r
 def save(self,label):js(self.pub.parent/(label+'-PROVIDER_TRACE.json'),self.calls)

def make_case(name,large=False):
 case=D/'fixtures'/name;r=case/'preprint';pub=case/'publication'
 assert not case.exists();pub.mkdir(parents=True)
 source=json.loads((C/'preprint/SOURCE_MANIFEST.json').read_bytes())
 for rel in set(B.CORE)|{x['path'] for x in source['files']}|{'manuscript.log'}:put(r/rel,(C/'preprint'/rel).read_bytes())
 for rel in B.HELPERS:put(pub/rel,(D/rel).read_bytes())
 intake=json.loads((C/'initial_review_20261016/INTAKE.json').read_bytes())
 q=('SYNTHETIC QUEUE fixture\n| foreign | preserve all bytes |\n'+intake['queue_row']+'\n').encode()
 intake.update(Queue_blob=I.blob(q),Queue_sha256=sha(q),SYNTHETIC_NO_AUTHORITY=True)
 js(case/'initial_review_20261016/INTAKE.json',intake)
 baseline=json.loads((C/'publication/PROGRESS_BASELINE.json').read_bytes())
 for rel in ['publication/PROGRESS_BASELINE.json',baseline['previous_case_acceptance']['path'],baseline['previous_native_checkpoint_receipt']['path']]:put(case/rel,(C/rel).read_bytes())
 helpers=[pin(pub/x,pub) for x in B.HELPERS];core=B.current_core(r)
 def review(kind,n):
  folder=case/f'SYNTHETIC_{kind}_{n}';folder.mkdir();frozen=f'2026-10-15T0{n*2}:00:00+00:00';completed=f'2026-10-15T0{n*2+1}:00:00+00:00'
  assessment=dict(schema='pr209-'+('whole-package' if kind=='whole' else 'release-helper')+'-assessment-v1',completed_utc=completed,verdict='PASS',mandatory_findings=[],optional_findings=[],SYNTHETIC_NO_AUTHORITY=True)
  if kind=='whole':
   freeze=dict(frozen_utc=frozen,core=core);js(folder/'FROZEN.json',freeze)
   put(folder/'REPORT.md',b'SYNTHETIC control only. NO AUTHORITY.\n')
   assessment.update(review_id=f'SYNTHETIC_whole_{n}',review_completed=True,frozen_utc=frozen,frozen_bindings=core,evidence=dict(freeze=pin(folder/'FROZEN.json',folder),report=pin(folder/'REPORT.md',folder)))
  else:
   for x in B.HELPERS:put(folder/x,(D/x).read_bytes())
   freeze=dict(frozen_utc=frozen,rows=helpers);js(folder/'FROZEN.json',freeze);put(folder/'REPORT.md',b'SYNTHETIC control only. NO AUTHORITY.\n')
   assessment.update(reviewer=f'SYNTHETIC_helper_{n}',frozen_sources=helpers)
  js(folder/'ASSESSMENT.json',assessment)
  js(folder/'AUTHORED_MANIFEST.json',dict(files=[pin(x,folder) for x in sorted(folder.iterdir())]))
  entry=dict(assessment=pin(folder/'ASSESSMENT.json',case),authored_manifest=pin(folder/'AUTHORED_MANIFEST.json',case),supplements=[])
  if kind=='helper':entry['source_freeze']=pin(folder/'FROZEN.json',case)
  return entry
 whole=[review('whole',i) for i in [1,2]];helper=[review('helper',i) for i in [1,2]]
 if large:
  for n in range(101):put(case/f'additional_exports/evidence_{n:03d}.txt',f'SYNTHETIC additional finite export {n}\n'.encode())
 exports=[pin(x,case) for x in sorted(case.rglob('*')) if x.is_file()]
 js(pub/'PUBLIC_EXPORT_MANIFEST.json',dict(schema='pr209-public-export-manifest-v1',files=exports,SYNTHETIC_NO_AUTHORITY=True))
 package=json.loads((r/'PACKAGE_MANIFEST.json').read_bytes());metadata=json.loads((r/'metadata.json').read_bytes())
 clearance=dict(release_cleared=True,unresolved_mandatory_findings=[],unresolved_optional_findings=[],original_native_head=B.ORIGINAL_HEAD,package_manifest_sha256=B.digest(r/'PACKAGE_MANIFEST.json'),deposit_manifest_sha256=B.digest(r/'deposit.json'),publication_metadata_sha256=B.digest(r/'metadata.json'),release_helpers=helpers,submission_files=package['submission_files'],source_manifest=package['source_manifest'],manuscript_source=package['manuscript_source'],publication_metadata=metadata,whole_package_reviews=whole,release_helper_reviews=helper,fresh_manuscript_reviews=2,final_frozen_clean_reviews=2,public_export_manifest=pin(pub/'PUBLIC_EXPORT_MANIFEST.json',case),progress_baseline=pin(pub/'PROGRESS_BASELINE.json',case),SYNTHETIC_NO_AUTHORITY=True)
 js(r/'FINAL_CLEARANCE.json',clearance)
 provider=Provider(r,pub,intake,q,baseline,large);provider.install()
 return r,pub,provider

def stage_and_append(r,pub,p,bad_range=False):
 z=P.publish_once(r,pub,ROOT=pub.parent.parent)
 p.bad_range=bad_range;t=A.append_once(r,pub);p.save('publication_tracker')
 return z,t

def actual_chain():
 entries=[]
 for n in [1,2]:
  folder=C/f'whole_package_adversary_0{n}'
  e=dict(assessment=pin(folder/'ASSESSMENT.json',C),authored_manifest=pin(folder/'AUTHORED_MANIFEST.json',C),supplements=[])
  if n==1:e.update(resolution=pin(C/'initial_review_20261016/ROOT_REVIEW01_RESOLUTION.json',C),supplements=[pin(folder/'AUTHORED_MANIFEST_SUPPLEMENT_REPORT_CORRECTION.json',C)])
  entries.append(e)
 value=B.review_chain(C,entries,'whole-package',B.current_core(C/'preprint'));assert value==(2,1),value
 js(D/'ACTUAL_CHAIN_INPUTS.json',dict(entries=entries,current_core=B.current_core(C/'preprint'),result=value))
 return value

def baseline():
 r,pub,p=make_case('full_baseline',True);ctx=B.context(r)
 z,t=stage_and_append(r,pub,p)
 with contextlib.redirect_stdout(io.StringIO()) as output:I.main([])
 put(D/'native_prepare.stdout',output.getvalue().encode())
 with contextlib.redirect_stdout(io.StringIO()) as output:M.main([])
 put(D/'native_merge.stdout',output.getvalue().encode());p.save('full_baseline')
 receipt=json.loads((pub/'PR_MERGED.json').read_bytes());assert receipt['program_counts']==[45,22,22,0]
 prepared=json.loads((pub/'PR_PREPARED.json').read_bytes());assert len(prepared['included_owned_pins'])>300
 assert p.flat(p.commits[p.refs['main']]['tree']['sha'])['foreign/keep.txt']==b'foreign main must survive\n'
 assert sum(x.get('method')=='PATCH' and x.get('path')=='git/refs/heads/main' for x in p.calls)==1
 return dict(pins=len(prepared['included_owned_pins']),counts=receipt['program_counts'],fixture=str(pub.parent.relative_to(D)))

def range_mismatch():
 r,pub,p=make_case('wrong_get_range');z,t=stage_and_append(r,pub,p,True)
 assert t['verified'] and (pub/'TRACKER_VERIFIED_APPEND.json').exists()
 record=json.loads((r.parent/t['evidence']['target_readback']['path']).read_bytes())
 assert record['response']['range']=="'Wrong tab'!Z999:AC999" and record['response']['majorDimension']=='COLUMNS'
 return dict(defect_reproduced=True,verified=True,wrong_range=record['response']['range'],wrong_dimension=record['response']['majorDimension'])

def partial_http():
 r,pub,p=make_case('partial_http');z=P.publish_once(r,pub,ROOT=pub.parent.parent);p.partial_download=True
 folder=pub/'synthetic_http_failure';folder.mkdir();ctx=B.context(r)
 result=rejects(lambda:V.public_bytes(r,ctx,p.summary(),folder),'IncompleteRead')
 assert not list(folder.iterdir()),[x.name for x in folder.iterdir()]
 put(D/'EXPECTED_HTTP_PARTIAL.bin',p.partial_binary)
 p.save('partial_http');return dict(defect_reproduced=True,exception=result,retained_file_count=0,available_partial_bytes=len(p.partial_binary))

def decode_loss():
 folder=D/'fixtures/text_decode_loss';folder.mkdir(parents=True)
 def local_child(cmd,**kw):return REAL_RUN([PY,'-B','-c',"import os;os.write(1,b'prefix\\x00\\xffsuffix');os.write(2,b'error-stream')"],**kw)
 A.subprocess=types.SimpleNamespace(run=local_child)
 result=rejects(lambda:A.reader(folder)('bad-output',['SYNTHETIC_LOCAL_CHILD']))
 assert (folder/'bad-output-stdout.json').read_bytes()==b''
 assert (folder/'bad-output-stderr.txt').read_bytes()==b''
 put(D/'EXPECTED_CHILD_STDOUT.bin',b'prefix\x00\xffsuffix');put(D/'EXPECTED_CHILD_STDERR.bin',b'error-stream')
 return dict(defect_reproduced=True,exception=result,saved_stdout_bytes=0,saved_stderr_bytes=0,actual_stdout_bytes=14,actual_stderr_bytes=12)

def drift_completion():
 # Reuse a completed provider state held in this process; entry observation is
 # valid. The provider drifts specifically during the known lengthy live read.
 r,pub,p=DRIFT
 ctx=B.context(r);z=B.publication(r,pub,ctx);t=B.tracker(r,pub,ctx,z);api=I.NativeAPI(pub,'SYNTHETIC_completion_drift',readonly=True);trees=I.NativeTrees(api)
 pi,built,packet,row=M.prepared_authority(r,pub,ctx,z,t,api,trees);progress=M.progress_baseline(r,pub,ctx,api,trees)
 intake=json.loads((pub.parent/'initial_review_20261016/INTAKE.json').read_bytes());base=api('GET','git/commits/'+pi['main_parent']);casepre=pub.parent.relative_to(M.ROOT).as_posix()+'/'
 intent,objects,files,row=M.load_merge(pub,ctx,built,packet,intake,z,progress,api,trees,base,casepre)
 # No preexisting completion receipt, even though provider merge is complete.
 assert not (pub/'PR_MERGED.json').exists()
 def mutate():p.pr['body']='STALE FOCAL FIRST PROOF CLAIM DURING LIVE READ';p.refs['main']=p.commit(p.make_tree({I.QUEUE:b'foreign rewritten main\n'}),[])
 p.mutate_on_live=mutate
 receipt=M.complete_merge(r,pub,ctx,z,t,intent,objects,files,row,progress,api,trees);p.save('completion_drift')
 assert receipt['case_completion_percent']==100 and p.pr['body'].startswith('STALE') and p.refs['main']!=objects['head']
 return dict(defect_reproduced=True,completion=100,actual_main=p.refs['main'],verified_merge=objects['head'],actual_body=p.pr['body'])

def make_drift():
 r,pub,p=make_case('completion_drift');stage_and_append(r,pub,p)
 with contextlib.redirect_stdout(io.StringIO()):I.main([])
 # Stop exact merge workflow after main PATCH using an unknown response; all
 # durable ancestry exists and actual in-memory provider merge did happen.
 p.main_unknown=True;rejects(lambda:M.main([]),'unknown');p.main_unknown=False
 assert not (pub/'PR_MERGED.json').exists();return r,pub,p

def negatives():
 r,pub,p=make_case('binding_negatives');ctx=B.context(r);clearpath=r/'FINAL_CLEARANCE.json';original=clearpath.read_bytes();out={}
 for key,value in [('fresh_manuscript_reviews',True),('whole_package_reviews',[]),('release_helper_reviews',[]),('unresolved_optional_findings',[dict(id='x')]),('original_native_head','0'*40)]:
  c=json.loads(original);c[key]=value;js(clearpath,c);out[key]=rejects(lambda:B.context(r))
 put(clearpath,original)
 h=pub/B.HELPERS[0];old=h.read_bytes();put(h,old+b'\n');out['helper_drift']=rejects(lambda:B.context(r));put(h,old)
 out['unsafe_export']=rejects(lambda:I.safe_name('private_data/file'))
 out['bad_queue_year']=rejects(lambda:I.patch_queue(p.q.replace(b' 2021 ',b' 2020 '),p.intake,dict(doi_url='https://doi.org/SYNTHETIC')))
 altered=p.q+b'| foreign untouched |\r\n';patched,row=I.patch_queue(altered,p.intake,dict(doi_url='https://doi.org/SYNTHETIC'));assert b'| foreign untouched |\r\n'in patched
 out['target_only_queue_preserved_foreign_crlf']=True
 lock=B.acquire(pub)
 try:out['concurrent_lock']=rejects(lambda:B.acquire(pub))
 finally:lock.close()
 raw=(r/'manuscript.log').read_bytes();put(r/'unexpected.bin',b'bad');out['unexpected_top_file']=rejects(lambda:B.context(r));(r/'unexpected.bin').unlink()
 return out

def duplicate_unknown():
 r,pub,p=make_case('append_duplicate');P.publish_once(r,pub,ROOT=pub.parent.parent);p.duplicates=True
 result=rejects(lambda:A.append_once(r,pub),'uniqueness');assert not (pub/'TRACKER_VERIFIED_APPEND.json').exists()
 writes=sum(x.get('provider')=='gws' and 'append'in x.get('args',[]) for x in p.calls)
 result2=rejects(lambda:A.append_once(r,pub));assert writes==sum(x.get('provider')=='gws' and 'append'in x.get('args',[]) for x in p.calls)==1
 p.save('duplicate');return dict(first=result,second=result2,append_calls=1)

def unknown_append_recovery():
 r,pub,p=make_case('append_unknown');P.publish_once(r,pub,ROOT=pub.parent.parent);p.lose_append=True
 rejects(lambda:A.append_once(r,pub));p.lose_append=False;t=A.append_once(r,pub)
 assert t['append_count']==0 and t['reconciled_existing_attempt'] is True
 assert sum(x.get('provider')=='gws' and 'append'in x.get('args',[]) for x in p.calls)==1
 p.save('unknown_append');return dict(recovered_with_zero_additional_writes=True)

def unknown_publication_recovery():
 r,pub,p=make_case('publish_unknown');p.lose_publish=True
 rejects(lambda:P.publish_once(r,pub,ROOT=pub.parent.parent));rejects(lambda:P.publish_once(r,pub,ROOT=pub.parent.parent),'Prior stage')
 p.lose_publish=False;z=V.verify_existing(r,pub,B.context(r));assert z['submitted'] is True
 assert sum(x.get('provider')=='zenodo' and x.get('operation')=='publish' for x in p.calls)==1
 p.save('unknown_publish');return dict(recovered_with_one_publish=True)

def rule_metadata_controls():
 r,pub,p=make_case('native_metadata_rejected');stage_and_append(r,pub,p);p.drop_metadata=True
 rejects(lambda:I.main([]),'title/body');assert not (pub/'PR_PREPARED.json').exists()
 assert (pub/'NATIVE_METADATA_ATTEMPT.json').exists();before=len([x for x in p.calls if x.get('method') in ['POST','PATCH']]);rejects(lambda:I.main([]),'Prior native')
 after=len([x for x in p.calls if x.get('method') in ['POST','PATCH']]);assert before==after
 p.pr.update(I.expected_pr_metadata(B.publication(r,pub),B.tracker(r,pub)))
 with contextlib.redirect_stdout(io.StringIO()):I.main(['--reconcile'])
 p.protected=True;rejects(lambda:M.main([]),'rules compliance');assert not (pub/'NATIVE_MERGE_REQUEST.json').exists()
 p.save('metadata_rules');return dict(stale_metadata_rejected=True,reconcile_readonly=True,protected_main_rejected=True)

def run():
 global DRIFT
 for row in json.loads((D/'FROZEN_SOURCES.json').read_bytes())['rows']:
  assert pin(D/row['path'],D)=={k:row[k] for k in ['path','bytes','sha256']}
 check('actual_whole_sealed_chain_compatibility',actual_chain)
 check('full_exact_workflow_300plus_native_paths',baseline)
 check('binding_queue_export_lock_negatives',negatives)
 check('tracker_wrong_response_range_and_dimension',range_mismatch)
 check('public_partial_http_stream_loss',partial_http)
 check('real_local_binary_decode_stream_loss',decode_loss)
 check('post_append_duplicate_no_second_write',duplicate_unknown)
 check('unknown_append_readonly_recovery',unknown_append_recovery)
 check('unknown_publish_readonly_recovery',unknown_publication_recovery)
 check('native_metadata_rules_and_readonly_recovery',rule_metadata_controls)
 check('completion_drift_setup',lambda:setup_drift())
 if 'DRIFT'in globals():check('completion_drift_after_long_public_readback',drift_completion)
 js(D/'RUN_SUMMARY.json',dict(utc=utc(),groups=len(RESULTS),passed=sum(x['PASS'] for x in RESULTS),synthetic_only=True,no_release_authority=True))
 return all(x['PASS'] for x in RESULTS)
def setup_drift():
 global DRIFT
 DRIFT=make_drift();return dict(fixture='completion_drift',actual_synthetic_merge=True,receipt_pending=True)
if __name__=='__main__':sys.exit(0 if run() else 1)

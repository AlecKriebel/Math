"""Independent offline whole-main probes. Every external adapter is a local mock."""
from pathlib import Path
import copy,contextlib,datetime,hashlib,importlib.util,io,json,shutil,types,zipfile
H=Path(__file__).resolve().parent; SOURCE=H/'_local/copy'; LAB=H/'_local/probes';LAB.mkdir(exist_ok=True)
RESULT=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def runcheck(name,fn):
 try:detail=fn();RESULT.append({'name':name,'status':'PASS','detail':detail})
 except Exception as e:RESULT.append({'name':name,'status':'FAIL','error':repr(e)})
def reject(fn,contains=None):
 try:fn()
 except (RuntimeError,ValueError,FileNotFoundError,KeyError) as e:
  if contains and contains not in str(e):raise RuntimeError('wrong guard: '+str(e))
  return str(e)
 raise RuntimeError('mutation unexpectedly accepted')
def silent(fn):
 with contextlib.redirect_stdout(io.StringIO()) as out:fn()
 return out.getvalue()
def case(name):
 root=LAB/name
 if root.exists():shutil.rmtree(root)
 shutil.copytree(SOURCE,root);return root

def artifact_and_nested():
 root=case('bindings');p=root/'publication';b=load(p/'build_package.py','binding_build');v=load(p/'verification/verify.py','binding_verify');good=b.document_bindings();bad=[]
 for name in ['manuscript/main.tex','output/pdf/main.pdf','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:
  f=p/name;old=f.read_bytes();f.write_bytes(old+b'\nCORRUPT');bad.append([name,reject(b.document_bindings)]);f.write_bytes(old)
 for key,value in [('page_indices_inspected',[1,2,3,4,5]),('all_pages_visually_inspected',False),('status','pending'),('pages',5)]:
  f=p/'LAYOUT_VERIFICATION.json';old=f.read_bytes();d=json.loads(old);d[key]=value;save(f,d);bad.append([key,reject(b.document_bindings)]);f.write_bytes(old)
 # Corruption hidden by updating outer inventory must still fail immutable family anchors.
 archive=p/'verification';manifest=json.loads((archive/'MANIFEST.json').read_text());context=json.loads((archive/'provenance/CURRENT_PR1241_CONTEXT.json').read_text())
 schemas=[]
 for reg in context['authored_freezes']:
  f=archive/reg['path'];d=json.loads(f.read_text());entry=d[reg['entries_key']][0];target=archive/reg['base']/entry[reg['path_key']];old=target.read_bytes();target.write_bytes(old+b'\nmodified after seal');new=target.read_bytes()
  for item in manifest['files']:
   if item['path']==target.relative_to(archive).as_posix():item['bytes']=len(new);item['sha256']=sha(new)
  save(archive/'MANIFEST.json',manifest)
  schemas.append({'manifest':reg['path'],'schema':[reg['entries_key'],reg['path_key']],'rejection':reject(lambda:v.authenticate_nested_manifests(archive))});target.write_bytes(old)
 return {'document_mutations':bad,'all_seven_actual_nested_schemas':schemas,'baseline_document_bindings':good}

class GitModel:
 """Local Git object/remote model; executes no Git or networking command."""
 def __init__(self,u,root):
  self.u=u;self.blobs={};self.trees={};self.commits={};self.calls=[];self.pushes=0;self.edits=0;self.created=0;self.lostpush=False;self.lostbody=False;self.apilag=False;self.bodyoutside=False
  self.state={'headRefName':u.BRANCH,'headRefOid':u.ORIGINAL,'state':'OPEN','isDraft':True,'body':'placeholder'};self.remote=u.ORIGINAL
  snap=json.loads((root/'SUBMITTED_SNAPSHOT.json').read_text());self.state['body']='original fixture body';self.originalbody=self.state['body'];snap['body_sha256']=sha(self.originalbody.encode());save(root/'SUBMITTED_SNAPSHOT.json',snap)
  # Keep immutable reviewed snapshot instead: body must match actual snapshot hash.
  self.snapshot=snap
 def original(self,root):
  # The original body is not present in the snapshot; retrieve it from frozen preflight context.
  d=json.loads((SOURCE/'LIVE_PR_PREFLIGHT.json').read_text());
  return d
 def hashblob(self,b):
  oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();self.blobs[oid]=b;return oid
 def tree(self,entries):
  raw=b''.join(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid) for name,(mode,kind,oid) in sorted(entries.items()));oid=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest();self.trees[oid]=dict(entries);return oid
 def buildtree(self,files):
  def go(d):return self.tree({n:('040000','tree',go(v)) if isinstance(v,dict) else ('100644','blob',self.hashblob(v)) for n,v in d.items()})
  tree={}
  for path,b in files.items():
   at=tree;parts=path.split('/')
   for q in parts[:-1]:at=at.setdefault(q,{})
   at[parts[-1]]=b
  return go(tree)
 def flatten(self,oid,prefix=''):
  out={}
  for name,(mode,kind,c) in self.trees[oid].items():
   if kind=='tree':out.update(self.flatten(c,prefix+name+'/'))
   else:out[prefix+name]=self.blobs[c]
  return out
 def pr(self):
  x=copy.deepcopy(self.state);x['headRefOid']=self.u.ORIGINAL if self.apilag and self.remote!=self.u.ORIGINAL else self.remote
  if self.bodyoutside and self.remote!=self.u.ORIGINAL:x['body']='outside body change'
  return x
 def git(self,*args,data=None):
  self.calls.append(args);a=args[0];u=self.u
  if a=='branch':return b'main\n'
  if a=='rev-parse':
   c,path=args[1].split(':',1);return (self.hashblob(self.flatten(self.commits[c]['tree'])[path])+'\n').encode()
  if a=='hash-object':return (self.hashblob(data)+'\n').encode()
  if a=='ls-tree':return b'\0'.join(f'{mode} {kind} {oid}\t{name}'.encode() for name,(mode,kind,oid) in sorted(self.trees[self.commits.get(args[-1],{}).get('tree',args[-1])].items()))+b'\0'
  if a=='mktree':
   entries={}
   for q in data.rstrip(b'\0').split(b'\0'):
    header,name=q.split(b'\t');mode,kind,oid=header.decode().split();entries[name.decode()]=(mode,kind,oid)
   return (self.tree(entries)+'\n').encode()
  if a=='commit-tree':
   self.created+=1;oid=hashlib.sha1(('commit-'+str(self.created)+args[1]).encode()).hexdigest();self.commits[oid]={'tree':args[1],'parent':args[3]};return (oid+'\n').encode()
  if a=='update-ref':return b''
  if a=='rev-list':
   c=args[-1];return (c+' '+self.commits[c]['parent']+'\n').encode()
  if a=='diff-tree':
   c=args[-1];o=self.flatten(self.commits[self.commits[c]['parent']]['tree']);n=self.flatten(self.commits[c]['tree']);return ('\n'.join(sorted(x for x in set(o)|set(n) if o.get(x)!=n.get(x)))+'\n').encode()
  if a=='show':
   c,path=args[1].split(':',1);return self.flatten(self.commits[c]['tree'])[path]
  if a=='ls-remote':return (self.remote+' refs/heads/'+u.BRANCH+'\n').encode()
  if a=='push':
   if args[1]!='origin' or len(args)!=3 or '--force' in repr(args):raise RuntimeError('not a pinned nonforce push')
   c,ref=args[2].split(':',1)
   if ref!='refs/heads/'+u.BRANCH or self.commits[c]['parent']!=self.remote:raise RuntimeError('push would not fast forward pinned branch')
   self.remote=c;self.pushes+=1
   if self.lostpush:self.lostpush=False;raise RuntimeError('simulated lost push response')
   return b''
  raise RuntimeError('Forbidden Git model call '+repr(args))
 def edit(self,args,**kw):
  if args[:3]!=['gh','pr','edit'] or args[3]!=self.u.NUMBER:raise RuntimeError('Forbidden app command')
  self.edits+=1;self.state['body']=Path(args[-1]).read_text()
  bad=self.lostbody;self.lostbody=False
  return types.SimpleNamespace(returncode=1 if bad else 0,stderr='simulated lost body response' if bad else '',stdout='')

def updater_fixture(name):
 root=case(name);p=root/'publication';u=load(p/'update_pr_publication.py','up_'+name);t=load(p/'append_tracker.py','track_'+name)
 # Frozen original body is embedded in the root context capture.
 ctx=json.loads((SOURCE/'LIVE_PR_PREFLIGHT.json').read_text());snap=json.loads((SOURCE/'SUBMITTED_SNAPSHOT.json').read_text())
 # Discover the captured full original PR body from frozen JSON objects.
 target=snap['body_sha256'];bodies=[]
 def walk(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if isinstance(v,str) and sha(v.encode())==target:bodies.append(v)
    walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 for n in ['LIVE_PR_PREFLIGHT.json','CURRENT_PR1241_CONTEXT.json','ROOT_GITHUB_HISTORY_RECEIPT.json']:walk(json.loads((SOURCE/n).read_text()))
 if not bodies:raise RuntimeError('Exact frozen original body unavailable; cannot test initial main honestly')
 model=GitModel(u,root);save(root/'SUBMITTED_SNAPSHOT.json',snap);model.state['body']=bodies[0];model.originalbody=bodies[0]
 originalfiles={e['path']:(root/'submitted'/Path(e['path']).name).read_bytes() for e in snap['files']};model.commits[u.ORIGINAL]={'tree':model.buildtree(originalfiles),'parent':None}
 build=json.loads((p/'BUILD_RECEIPT.json').read_text());meta=json.loads((p/'zenodo-deposit.json').read_text())['metadata'];pub={'environment':'production','state':'published','metadata_normalizations':[],'id':321,'doi':'10.5281/zenodo.321','doi_url':'https://doi.org/10.5281/zenodo.321','record_url':'https://zenodo.org/records/321','url':'https://doi.org/10.5281/zenodo.321','title':meta['title'],'files':[{'name':build[k]['path'],'size':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]}
 save(p/'PUBLICATION_RECEIPT.json',pub)
 tracker={'spreadsheetId':t.SID,'gid':t.GID,'row':t.expected_row(pub,meta['title']),'updatedRange':"'Math Puzzles'!A321:D321",'readback_verified':True};save(p/'tracker/TRACKER_RECEIPT.json',tracker)
 review=root/'reviews/final';save(review/'VERDICT.json',{'status':'CLEAN'});(review/'REPORT.md').write_text('Explicit offline CLEAN fixture, no review claim.\n')
 gate={'schema':'math-preprint-final-review-gate-v1','pr':1241,'problem_id':11000082,'original_head':u.ORIGINAL,'status':'pass','pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':sha((p/'zenodo-deposit.json').read_bytes()),'workflow':{n:sha((p/n).read_bytes()) for n in u.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/final/REPORT.md','report_sha256':sha((review/'REPORT.md').read_bytes()),'verdict':'../reviews/final/VERDICT.json','verdict_sha256':sha((review/'VERDICT.json').read_bytes())}};save(p/'FINAL_REVIEW_GATE.json',gate)
 public={'id':pub['id'],'doi':pub['doi'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_manifest_sha256':gate['metadata_sha256'],'metadata_fields_verified':sorted(meta),'files':[{'name':build[k]['path'],'bytes':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]};save(p/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
 u.git=model.git;u.pr=model.pr;u.subprocess=types.SimpleNamespace(run=model.edit);return root,p,u,model

def updater_flow(kind):
 root,p,u,m=updater_fixture('updater_'+kind)
 if kind=='api_lag':m.apilag=True;message=reject(lambda:silent(u.main),'not yet the intended commit');assert m.pushes==1 and m.edits==0 and not (p/'PR_BRANCH_RECEIPT.json').exists();m.apilag=False
 elif kind=='lost_push':m.lostpush=True;message=reject(lambda:silent(u.main),'lost push');assert m.pushes==1 and m.edits==0
 elif kind=='lost_body':m.lostbody=True;message=reject(lambda:silent(u.main),'outcome needs');assert m.pushes==1 and m.edits==1 and not (p/'PR_BRANCH_RECEIPT.json').exists()
 elif kind=='outside_body':
  m.bodyoutside=True;message=reject(lambda:silent(u.main),'outside original/intended');assert m.edits==0 and not (p/'PR_BRANCH_RECEIPT.json').exists();return {'stopped':message,'pushes':m.pushes,'body_edits':m.edits}
 elif kind=='wrong_branch':
  m.state['headRefName']='outside-branch';message=reject(lambda:silent(u.main),'Unexpected PR');assert m.created==m.pushes==m.edits==0;return {'stopped':message,'external_mutations':0}
 else:message='normal initial completion'
 silent(u.main);silent(u.main)
 receipt=json.loads((p/'PR_BRANCH_RECEIPT.json').read_text());files,_,_=u.desired_files(json.loads((p/'BUILD_RECEIPT.json').read_text()),json.loads((p/'PUBLICATION_RECEIPT.json').read_text()),json.loads((p/'tracker/TRACKER_RECEIPT.json').read_text()),json.loads((root/'SUBMITTED_SNAPSHOT.json').read_text()));c=receipt['commit']
 assert len(files)==13 and all(m.git('show',c+':'+n)==b for n,b in files.items()) and m.commits[c]['parent']==u.ORIGINAL
 assert m.pushes==1 and m.edits==1 and m.created==1 and receipt['body_readback_verified'] and receipt['remote_readback_verified']
 # Mutate actual synthetic object bytes, leaving all saved identity JSON intact.
 tree=m.commits[c]['tree'];badpath=sorted(files)[0];savedoid=m.hashblob(files[badpath]);old=m.blobs[savedoid];m.blobs[savedoid]=old+b'changed object'
 drift=reject(lambda:silent(u.main),'bytes differ');m.blobs[savedoid]=old
 return {'initial_outcome':message,'single_commit':m.created,'single_nonforce_pinned_push':m.pushes,'single_body_edit':m.edits,'actual_13_blobs_verified':True,'saved_retry_object_corruption_refused':drift,'model_limit':'Real production main and put/identity/body code, in-memory Git object and remote/API adapters. No Git or application command executed.'}

def main():
 for k in ['normal','api_lag','lost_push','lost_body','outside_body','wrong_branch']:runcheck('full_updater_'+k,lambda k=k:updater_flow(k))
 runcheck('bindings_and_actual_nested_schema_mutations',artifact_and_nested)
 save(H/'INDEPENDENT_WORKFLOW_RESULTS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':RESULT,'all_pass':all(x['status']=='PASS' for x in RESULT),'scope':'Offline copies and mocks only; no live GitHub/Zenodo/GWS integration or publication claim.'})
 print(json.dumps(RESULT,indent=2))

if __name__=='__main__':main()

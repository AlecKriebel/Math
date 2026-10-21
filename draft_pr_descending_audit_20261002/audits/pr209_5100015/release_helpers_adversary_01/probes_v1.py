"""Exact frozen-source negative controls. No provider, Git, or outside writes.

Every candidate is compiled without text/AST changes. Imports of subprocess and
urllib.request are replaced with in-memory providers. Only the literal workspace
Path is remapped to an owned synthetic root; __file__ is the synthetic publication
path. The pure binding module is itself compiled from the exact frozen bytes.
"""
from pathlib import Path
import base64,builtins,hashlib,json,os,shutil,subprocess,sys,types,zipfile

HERE=Path(__file__).resolve().parent
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
NAMES=['append_verified_tracker.py','integrate_reviewed_pr.py','publish_preprint.py','release_binding.py','verify_and_merge.py','verify_published_readonly.py']
SOURCE={n:(HERE/n).read_bytes() for n in NAMES}
OLD='fd09a95b479f376234835a4494693bb1316c85ec'
PREFIX='unsolved_math_prioritization/attempts/5100015/'
ROW='| 222 | 5100015 / AMR-050-0015 | Elliptic-billiard invariant k_{303,b} | 0.1905 | 5.0 | 3 | 2021 | claimed_solved | 1/5 |  |  |  |'
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
RESULTS=[]

def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def dump(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def pin(p,base):return dict(path=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))

class Fixture:
 def __init__(self,label):
  self.base=HERE/'probe_runs'/label
  if self.base.exists():raise RuntimeError('Preserve previous probe output; choose a new label')
  self.root=self.base/'workspace';self.c=self.root/'case';self.pub=self.c/'publication';self.r=self.c/'preprint';self.d=self.c/'initial_review_20261016'
  for p in [self.pub,self.r,self.d]:p.mkdir(parents=True)
  for name,raw in SOURCE.items():(self.pub/name).write_bytes(raw)
  self.u=self.r/'pr_update/5100015';self.u.mkdir(parents=True)
  for n in ['STATUS.md','README.md','RESEARCH_LOG.md','PROOF.md']:(self.u/n).write_text('synthetic reviewed '+n+'\n')
  dump(self.u/'readiness.json',{'scope':'synthetic reviewed'})
  original=[]
  for k in range(23):
   n=f'original_{k:02d}.txt';p=self.u/'history/original_submission_20261016'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(f'original {k}\n')
   original.append(dict(native_path=PREFIX+n,bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
  self.queue=(ROW+'\n| foreign | preserved |\n').encode()
  dump(self.d/'INTAKE.json',dict(Queue_blob=blob(self.queue),Queue_sha256=sha(self.queue),queue_row=ROW,original_source_files=original))
  for n in ['submitted','root_reproduction_01','root_reproduction_02','root_reproduction_03','priority_public_chronology_01']:(self.d/n).mkdir()
  families=['source_domain_adversary_01','physical_geometry_adversary_01','meromorphic_divisor_adversary_01','priority_author_updates_01','priority_classical_general_01']
  for n in families:
   folder=self.d/n;dump(folder/'AUTHORED_MANIFEST.json',{'files':[]})
   if n=='priority_author_updates_01':dump(folder/'AUTHORED_MANIFEST_SUPPLEMENT_TIMESTAMP_CORRECTION.json',dict(original_manifest=pin(folder/'AUTHORED_MANIFEST.json',folder),original_payloads_unchanged=[],supplemental_payloads=[]))
  (self.r/'manuscript.pdf').write_bytes(b'%PDF synthetic reviewed\n')
  (self.r/'manuscript.tex').write_text('synthetic reviewed theorem\n')
  (self.r/'data.txt').write_text('synthetic referenced input\n')
  dump(self.r/'SOURCE_MANIFEST.json',{'files':[pin(self.r/'data.txt',self.r)]})
  with zipfile.ZipFile(self.r/'k303b-source-verification.zip','w') as z:
   for p in sorted(self.u.rglob('*')):
    if p.is_file():z.write(p,'k303b_outer_center_pedal_product/pr_update/5100015/'+p.relative_to(self.u).as_posix())
  self.metadata={'title':'The outer center-pedal area product in elliptic billiards','version':'1.0'}
  dump(self.r/'metadata.json',self.metadata)
  self.mappings=[{'path':'manuscript.pdf','name':'k303b-outer-center-pedal-areas.pdf'},{'path':'k303b-source-verification.zip','name':'k303b-source-verification.zip'}]
  dump(self.r/'deposit.json',dict(metadata=self.metadata,files=self.mappings))
  package=dict(submission_files=[pin(self.r/x['path'],self.r) for x in self.mappings],source_manifest=pin(self.r/'SOURCE_MANIFEST.json',self.r),manuscript_source=pin(self.r/'manuscript.tex',self.r),metadata=pin(self.r/'metadata.json',self.r))
  dump(self.r/'PACKAGE_MANIFEST.json',package)
  self.clear=dict(release_cleared=True,fresh_manuscript_reviews=2,final_frozen_clean_reviews=1,unresolved_mandatory_findings=[],unresolved_optional_findings=[],original_native_head=OLD,package_manifest_sha256=sha((self.r/'PACKAGE_MANIFEST.json').read_bytes()),deposit_manifest_sha256=sha((self.r/'deposit.json').read_bytes()),publication_metadata_sha256=sha((self.r/'metadata.json').read_bytes()),release_helpers=[pin(self.pub/n,self.pub) for n in NAMES],submission_files=package['submission_files'],source_manifest=package['source_manifest'],manuscript_source=package['manuscript_source'],publication_metadata=self.metadata)
  dump(self.r/'FINAL_CLEARANCE.json',self.clear)
  self.calls=[];self.mutations=[];self.nodes={};self.commits={};self.files_by_tree={};self.pr=self.identity(OLD)
  self.rb=self.module('release_binding.py')
  self.ctx=self.rb.context(self.r)
  self.z=dict(submitted=True,metadata_and_files_verified=True,exact_reviewed_frozen_files_published=True,release_binding=self.rb.binding(self.ctx),metadata=self.metadata,files=self.ctx['expected_files'],additional_public_readback_error=None,additional_actual_public_file_downloads=[dict(file=f['name'],bytes=f['size'],sha256=f['sha256'],actual_public_download_byte_hash_match=True) for f in self.ctx['expected_files']],id=12345,doi='10.5281/zenodo.12345',doi_url='https://doi.org/10.5281/zenodo.12345',record_url='https://zenodo.org/records/12345',doi_resolution=dict(status='resolved',http_status=200,url='https://doi.org/10.5281/zenodo.12345',resolved_url='https://zenodo.org/records/12345'))
  dump(self.pub/'ZENODO_VERIFIED_PUBLICATION.json',self.z)
  self.t=dict(verified=True,exact_all_four_cells_readback=True,release_binding=self.rb.binding(self.ctx),publication_receipt_sha256=sha((self.pub/'ZENODO_VERIFIED_PUBLICATION.json').read_bytes()),doi_url=self.z['doi_url'],spreadsheet_id=SHEET,sheet_id=1254632077,values=['https://arxiv.org/abs/2004.12497v11','',self.z['doi_url'],self.metadata['title']+' 5100015'],updated_range="'Math Puzzles'!A2:D2",append_count=1)
  dump(self.pub/'TRACKER_VERIFIED_APPEND.json',self.t)
  self.main='main-synthetic';self.mainfiles={'unsolved_math_prioritization/QUEUE.md':self.queue,'foreign-preserved.txt':b'foreign main bytes\n'}
  self.commits[self.main]=dict(tree={'sha':self.tree(self.mainfiles)},parents=[])
  self.sheet=[['Original Problem','Solution Chat URL','DOI','Notes']]
  self.duplicate_during_append=False;self.ignore_body_patch=False;self.fail_body_patch=False;self.compare_cap=False
 def identity(self,head):return dict(number=209,state='open',head=dict(sha=head,ref='dot/math-5100015',repo={'full_name':'AlecKriebel/Math'}),base=dict(ref='main',repo={'full_name':'AlecKriebel/Math'}),draft=True,merged=False,mergeable=True,node_id='PR209',html_url='https://github.com/AlecKriebel/Math/pull/209',title='stale title',body='stale focal theorem; first proof claim')
 def imp(self,name,globals=None,locals=None,fromlist=(),level=0):
  if name=='release_binding':return self.rb
  if name=='subprocess':return types.SimpleNamespace(run=self.run)
  if name=='pathlib':return types.SimpleNamespace(Path=lambda *args: self.root if args==('/Users/alec/Documents/Math',) else Path(*args))
  if name=='urllib.request':return types.SimpleNamespace(request=types.SimpleNamespace(Request=lambda *a,**k:a[0],urlopen=self.urlopen))
  if name=='verify_published_readonly':return self.module(name+'.py')
  if name=='time':return types.SimpleNamespace(sleep=lambda x:None)
  return builtins.__import__(name,globals,locals,fromlist,level)
 def module(self,name,main=False):
  m=types.ModuleType('__main__' if main else name.removesuffix('.py'));m.__file__=str(self.pub/name)
  m.__dict__['__builtins__']={**vars(builtins),'__import__':self.imp}
  exec(compile(SOURCE[name],str(HERE/name),'exec'),m.__dict__)
  return m
 def tree(self,files):
  nested={}
  for path,raw in files.items():
   cur=nested;parts=path.split('/')
   for part in parts[:-1]:cur=cur.setdefault(part,{})
   cur[parts[-1]]=raw
  def rec(d):
   rows=[]
   for name,v in sorted(d.items()):
    if isinstance(v,dict):rows.append(dict(path=name,type='tree',mode='040000',sha=rec(v)))
    else:
     s=blob(v);self.nodes[s]=v;rows.append(dict(path=name,type='blob',mode='100644',sha=s))
   key='tree-'+sha(json.dumps(rows,sort_keys=True).encode());self.nodes[key]=dict(truncated=False,tree=rows);return key
  t=rec(nested);self.files_by_tree[t]=dict(files);return t
 def native(self,method,path,payload):
  self.calls.append(dict(provider='github',method=method,path=path,payload=payload))
  if method!='GET':self.mutations.append(dict(method=method,path=path,prepare_intent_exists=(self.pub/'NATIVE_PREPARE_ATTEMPT.json').exists(),ready_intent_exists=(self.pub/'NATIVE_READY_ATTEMPT.json').exists(),merge_intent_exists=(self.pub/'NATIVE_MERGE_REQUEST.json').exists()))
  if method=='GET' and path=='pulls/209':return dict(self.pr)
  if method=='GET' and path.startswith('git/ref/heads/'):
   return {'object':{'sha':self.main if path.endswith('/main') else self.pr['head']['sha']}}
  if method=='GET' and path.startswith('git/commits/'):return self.commits[path.removeprefix('git/commits/')]
  if method=='GET' and path.startswith('git/trees/'):return self.nodes[path.removeprefix('git/trees/')]
  if method=='GET' and path.startswith('git/blobs/'):
   raw=self.nodes[path.removeprefix('git/blobs/')];return dict(content=base64.b64encode(raw).decode(),encoding='base64')
  if method=='GET' and path.startswith('contents/'):
   path,ref=path.removeprefix('contents/').split('?ref=')
   if ref==OLD:raw=self.queue
   else:raw=self.files_by_tree[self.commits[ref]['tree']['sha']][path]
   return dict(sha=blob(raw),content=base64.b64encode(raw).decode(),encoding='base64')
  if method=='POST' and path=='git/blobs':
   raw=base64.b64decode(payload['content']);s=blob(raw);self.nodes[s]=raw;return {'sha':s}
  if method=='POST' and path=='git/trees':
   files=dict(self.files_by_tree[payload['base_tree']])
   for e in payload['tree']:files[e['path']]=e['content'].encode() if 'content' in e else self.nodes[e['sha']]
   return {'sha':self.tree(files)}
  if method=='POST' and path=='git/commits':
   head='prepared-'+sha(json.dumps(payload,sort_keys=True).encode());self.commits[head]=dict(tree={'sha':payload['tree']},parents=[{'sha':s} for s in payload['parents']]);return {'sha':head}
  if method=='PATCH' and path=='git/refs/heads/dot/math-5100015':self.pr['head']=dict(self.pr['head'],sha=payload['sha']);return {'object':{'sha':payload['sha']}}
  if method=='PATCH' and path=='pulls/209':
   if self.fail_body_patch:raise RuntimeError('synthetic unknown body-PATCH outcome')
   if not self.ignore_body_patch:self.pr.update(payload)
   return dict(self.pr)
  if method=='GET' and path.startswith('compare/'):
   before,after=path.removeprefix('compare/').split('...');a=self.files_by_tree[self.commits[before]['tree']['sha']];b=self.files_by_tree[self.commits[after]['tree']['sha']]
   rows=[dict(filename=p,status='removed' if p not in b else 'added' if p not in a else 'modified') for p in sorted(a.keys()|b.keys()) if a.get(p)!=b.get(p)]
   return {'files':rows[:300] if self.compare_cap else rows}
  if method=='POST' and path=='graphql':self.pr['draft']=False;return dict(data={'markPullRequestReadyForReview':{'pullRequest':{'id':'PR209','isDraft':False}}})
  if method=='PUT' and path=='pulls/209/merge':self.pr.update(merged=True,state='closed',merge_commit_sha='synthetic-merge');return {'merged':True,'sha':'synthetic-merge'}
  raise RuntimeError('Unsupported synthetic GitHub request '+repr((method,path,payload)))
 def run(self,args,**kw):
  if 'gh' in Path(args[0]).name:
   method=args[args.index('--method')+1] if '--method' in args else 'GET';target=args[args.index('--method')+2] if '--method' in args else args[2]
   payload=json.loads(Path(args[args.index('--input')+1]).read_text()) if '--input' in args else None
   result=self.native(method,target.removeprefix('repos/AlecKriebel/Math/'),payload)
  elif args[0].endswith('/gws'):
   params=json.loads(args[args.index('--params')+1]);operation=args[4] if args[1:4]==['sheets','spreadsheets','values'] else 'properties'
   self.calls.append(dict(provider='gws',operation=operation,params=params))
   if operation=='properties':result={'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
   elif operation=='append':
    row=json.loads(args[args.index('--json')+1])['values'][0];self.sheet.append(row)
    if self.duplicate_during_append:self.sheet.append(row)
    result={'updates':dict(updatedRows=1,updatedCells=4,updatedData={'values':[row]},updatedRange="'Math Puzzles'!A2:D2")}
   else:result={'values':self.sheet if params['range'].endswith('A:D') else [self.sheet[1]]}
  else:
   operation=args[3];self.calls.append(dict(provider='zenodo-kit',operation=operation))
   result=dict(environment='production',files=self.ctx['expected_files'],id=12345,state='ready_to_publish')
   if operation in ['publish','inspect']:result.update(self.z,state='published' if operation=='publish' or (self.pub/'PUBLISH_ATTEMPT.json').exists() else 'ready_to_publish')
  raw=json.dumps(result)
  return types.SimpleNamespace(returncode=0,stdout=raw if kw.get('text') else raw.encode(),stderr='' if kw.get('text') else b'')
 def urlopen(self,url,**kw):
  name=url.split('/files/')[1].split('?')[0];mapping=next(m for m in self.mappings if m['name']==name);raw=(self.r/mapping['path']).read_bytes()
  class Response:
   def __enter__(self):return self
   def __exit__(self,*a):return None
   def read(self):return raw
  return Response()
 def execute(self,name):
  old=sys.stdout;sys.stdout=types.SimpleNamespace(write=lambda s:None,flush=lambda:None)
  try:self.module(name,main=True)
  finally:sys.stdout=old
 def save(self):dump(self.base/'PROVIDER_TRACE.json',dict(calls=self.calls,mutations=self.mutations,final_pr=self.pr,final_sheet=self.sheet))

def check(label,fn):
 try:detail=fn();RESULTS.append(dict(label=label,status='PASS',detail=detail))
 except Exception as e:RESULTS.append(dict(label=label,status='PROBE_ERROR',error=type(e).__name__+': '+str(e)))
 dump(HERE/'PROBE_RESULTS.json',RESULTS)
 print(json.dumps(RESULTS[-1]))

def rejection(fn):
 try:fn()
 except Exception as e:return type(e).__name__+': '+str(e)
 raise AssertionError('Negative control unexpectedly accepted')

def baseline():
 f=Fixture('baseline');f.execute('integrate_reviewed_pr.py');f.execute('verify_and_merge.py');f.save()
 assert f.pr['merged'];return {'prepared_and_merged':True,'mutation_count':len(f.mutations)}

def counter_only_clearance():
 f=Fixture('counter_only_clearance');ctx=f.rb.context(f.r)
 assert set(ctx['clear'])==set(f.clear)
 return {'accepted_without_any_review_record':True,'new_sequential_whole_package_proof_fields':[],'review_count':ctx['clear']['fresh_manuscript_reviews']}

def all_basic_guards():
 f=Fixture('basic_guards');cases={};p=f.r/'FINAL_CLEARANCE.json';original=p.read_bytes()
 for key,value in [('unresolved_mandatory_findings',['M1']),('unresolved_optional_findings',['O1']),('original_native_head','wrong'),('fresh_manuscript_reviews',1),('fresh_manuscript_reviews',True),('final_frozen_clean_reviews',0)]:
  c=json.loads(original);c[key]=value;dump(p,c);cases[key+repr(value)]=rejection(lambda:f.rb.context(f.r));p.write_bytes(original)
 for target in [f.r/'manuscript.pdf',f.r/'metadata.json',f.pub/'publish_preprint.py']:
  raw=target.read_bytes();target.write_bytes(raw+b'changed');cases[str(target.relative_to(f.base))]=rejection(lambda:f.rb.context(f.r));target.write_bytes(raw)
 f.z['doi_resolution']['resolved_url']='https://zenodo.org/records/999';dump(f.pub/'ZENODO_VERIFIED_PUBLICATION.json',f.z);cases['wrong_DOI_record']=rejection(lambda:f.rb.publication(f.r,f.pub,f.ctx))
 return cases

def tracker_unbound_intent():
 f=Fixture('tracker_unbound_intent');f.t.update(append_count=9,updated_range='Other sheet!Z999',reconciled_existing_attempt=False);dump(f.pub/'TRACKER_VERIFIED_APPEND.json',f.t)
 accepted=f.rb.tracker(f.r,f.pub,f.ctx,f.z)
 return {'accepted_append_count':accepted['append_count'],'accepted_range':accepted['updated_range'],'append_intent_exists':(f.pub/'private_transport/tracker/APPEND_ATTEMPT.json').exists()}

def duplicate_race():
 f=Fixture('duplicate_race');(f.pub/'TRACKER_VERIFIED_APPEND.json').unlink();f.duplicate_during_append=True;f.execute('append_verified_tracker.py');f.save()
 receipt=json.loads((f.pub/'TRACKER_VERIFIED_APPEND.json').read_text());assert receipt['verified'] and len(f.sheet)==3
 return {'verified':True,'problem_rows_after_append':len(f.sheet)-1,'actual_append_calls':sum(c.get('operation')=='append' for c in f.calls),'full_sheet_reads_after_append':0}

def unreviewed_payload():
 f=Fixture('unreviewed_payload');(f.pub/'.env').write_text('SYNTHETIC_PRIVATE_PAYLOAD=must-not-upload\n');(f.r/'UNREVIEWED.txt').write_text('synthetic unsealed addition\n');f.execute('integrate_reviewed_pr.py');f.save()
 p=json.loads((f.pub/'PR_PREPARED.json').read_text());paths={r['path'] for r in p['included_owned_pins']}
 leaked=[x for x in paths if x.endswith('/.env') or x.endswith('/UNREVIEWED.txt')];assert len(leaked)==2
 return {'uploaded_unsealed_paths':sorted(leaked),'first_provider_mutation':f.mutations[0]}

def body_ignored():
 f=Fixture('body_ignored');f.ignore_body_patch=True;f.execute('integrate_reviewed_pr.py');f.execute('verify_and_merge.py');f.save();assert f.pr['merged'] and 'first proof' in f.pr['body']
 return {'merged':True,'actual_body':f.pr['body'],'actual_title':f.pr['title']}

def body_patch_unknown():
 f=Fixture('body_patch_unknown');f.fail_body_patch=True;error=rejection(lambda:f.execute('integrate_reviewed_pr.py'));assert (f.pub/'PR_PREPARED.json').exists();f.execute('verify_and_merge.py');f.save();assert f.pr['merged']
 return {'prepare_error':error,'prepared_receipt_written_before_failed_body_patch':True,'subsequent_merge_succeeded':True,'actual_body':f.pr['body']}

def forged_prepared_no_science():
 f=Fixture('forged_prepared_no_science');head='forged-head';target=ROW.replace('|  |  |  |','|  | audited | '+f.z['doi_url']+' |');q=(target+'\n| foreign | preserved |\n').encode()
 files=dict(f.mainfiles);files['unsolved_math_prioritization/QUEUE.md']=q
 for row in f.clear['submission_files']:files[(f.r/row['path']).relative_to(f.root).as_posix()]=(f.r/row['path']).read_bytes()
 files['foreign-owned-by-someone-else.txt']=b'UNREVIEWED foreign addition\n'
 tree=f.tree(files);f.commits[head]=dict(tree={'sha':tree},parents=[{'sha':OLD},{'sha':f.main}]);f.pr['head']['sha']=head
 pins=[dict(path=path,bytes=len(raw),sha256=sha(raw),git_blob_sha1=blob(raw)) for path,raw in files.items() if f.mainfiles.get(path)!=raw]
 p=dict(prepared_head=head,tree=tree,main_parent=f.main,target_queue_row=target,included_owned_pins=pins,release_binding=f.rb.binding(f.ctx),publication_receipt_sha256=sha((f.pub/'ZENODO_VERIFIED_PUBLICATION.json').read_bytes()),tracker_receipt_sha256=sha((f.pub/'TRACKER_VERIFIED_APPEND.json').read_bytes()))
 dump(f.pub/'PR_PREPARED.json',p);f.execute('verify_and_merge.py');f.save();assert f.pr['merged']
 return {'merged':True,'prepare_intent_exists':(f.pub/'NATIVE_PREPARE_ATTEMPT.json').exists(),'native_current_source_exists':(f.pub/'native_current_source').exists(),'original_archive_files_in_native_tree':0,'unreviewed_foreign_addition_merged':True}

def compare_limit():
 f=Fixture('compare_limit');f.compare_cap=True
 for k in range(310):(f.r/f'extra_{k:03d}.txt').write_text('synthetic reviewed-count-boundary\n')
 f.execute('integrate_reviewed_pr.py');error=rejection(lambda:f.execute('verify_and_merge.py'));f.save()
 return {'error':error,'prepared_pin_count':len(json.loads((f.pub/'PR_PREPARED.json').read_text())['included_owned_pins']),'merge_requested':any(m['method']=='PUT' for m in f.mutations)}

def optimized_guards():
 rows=[]
 for n in NAMES:
  r=subprocess.run([PY,'-B','-O',str(HERE/n)],capture_output=True,text=True,timeout=20)
  assert r.returncode!=0 and ('optimized' in r.stderr.lower() or 'Optimized' in r.stderr)
  rows.append(dict(path=n,returncode=r.returncode,stderr=r.stderr))
 dump(HERE/'OPTIMIZED_GUARD_RESULTS.json',rows);return {'all_six_rejected':True}

def intent_parent_durability():
 f=Fixture('intent_parent_durability');events=[];real=f.rb.sync_directory
 def sync(p):events.append(str(Path(p).relative_to(f.base)));real(p)
 f.rb.sync_directory=sync;p=f.pub/'one/two/intent.json';f.rb.durable_mkdir(p.parent);f.rb.exclusive_json(p,{'intent':'synthetic'})
 assert events[-1]=='workspace/case/publication/one/two'
 return {'sync_directory_order':events,'intent_readback':json.loads(p.read_text())}

if __name__=='__main__':
 for label,fn in [('baseline_actual_callers',baseline),('counter_only_clearance',counter_only_clearance),('basic_rejections',all_basic_guards),('tracker_unbound_intent',tracker_unbound_intent),('duplicate_race',duplicate_race),('unreviewed_payload',unreviewed_payload),('stale_body',body_ignored),('body_patch_unknown',body_patch_unknown),('forged_prepared_no_science',forged_prepared_no_science),('compare_limit',compare_limit),('optimized_guards',optimized_guards),('intent_parent_durability',intent_parent_durability)]:check(label,fn)

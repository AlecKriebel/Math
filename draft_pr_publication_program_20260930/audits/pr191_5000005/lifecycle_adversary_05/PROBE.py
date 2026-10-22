#!/usr/bin/env python3
"""Independent PR191 adversary05, offline disposable fixtures only; no author tests."""
import ast,base64,copy,datetime,hashlib,importlib.util,json,os,re,shutil,socket,stat,subprocess,sys,types
from pathlib import Path
SCRIPT_ROOT=Path(__file__).resolve().parent
CASE_ROOT=SCRIPT_ROOT.parent
HERE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else SCRIPT_ROOT
assert HERE.is_relative_to(SCRIPT_ROOT), 'All probe outputs must remain under adversary05'
if len(sys.argv)>1:
 assert not HERE.exists(), 'Reproduction output directory must be new'
 HERE.mkdir(parents=True)
SOURCE=CASE_ROOT/'lifecycle_controls_preparation_05'
SOURCE_SHA='dc883dcad2120b21e134070a5dc44f78f860ffd7cd711b89db8423f2da00a97f'
RESULTS=[]
FIXTURES=HERE/'scratch_fixtures'
FIXTURES.mkdir(exist_ok=True)

def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,indent=2)+'\n').encode()
def digest(b):return {'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def pin(p):return digest(Path(p).read_bytes())
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():p.chmod(0o644)
 p.write_bytes(v if isinstance(v,bytes) else enc(v))
def bind(root,n):return {'path':n,**{k:v for k,v in pin(root/n).items() if k!='git_blob'}}
def expect(label,fun,reject=False,detail=None):
 try:
  result=fun();ok=not reject;error=None
 except Exception as e:
  result=None;ok=reject;error=type(e).__name__+': '+str(e)
 row={'test':label,'expectation':'reject' if reject else 'accept','passed':ok,'observed':'reject' if error else 'accept'}
 if error:row['error']=error
 if detail:row['detail']=detail
 RESULTS.append(row)
 return result

def load():
 assert sha((SOURCE/'lifecycle_common.py').read_bytes())==SOURCE_SHA
 spec=importlib.util.spec_from_file_location('independent05_reviewed_runtime',SOURCE/'lifecycle_common.py')
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class Service:
 def __init__(self,f):self.f=f;self.rows=[copy.deepcopy(f.m.HEADER),['FOREIGN_CANARY_ALPHA','secret-note','10.9999/foreign-A','FOREIGN_CANARY_PRIVATE'],['FOREIGN_CANARY_BETA','','','retain']];self.calls=[];self.record=None;self.stage_calls=0;self.publish_calls=0;self.append_calls=0;self.fail_publish=False;self.fail_append=False;self.inspect_hook=None;self.track_hook=None
 def tracker(self,resource,method,params,body=None):
  self.calls.append({'service':'tracker','resource':resource,'method':method,'params':copy.deepcopy(params),'body':copy.deepcopy(body)})
  if self.track_hook:
   answer=self.track_hook(resource,method,params,body)
   if answer is not None:return answer
  m=self.f.m
  if resource=='spreadsheet':return {'spreadsheetId':m.SID,'sheets':[{'properties':{'sheetId':m.GID,'title':m.TAB}}]}
  rng=params['range']
  if method=='append':
   assert params['valueInputOption']=='RAW' and body=={'majorDimension':'ROWS','values':[m.tracker_row(self.f.g,self.f.z)]}
   self.append_calls+=1;self.rows+=copy.deepcopy(body['values']);i=len(self.rows)
   if self.fail_append:raise TimeoutError('independent injected append-after-commit response loss')
   return {'updates':{'updatedRange':f"'Math Puzzles'!A{i}:D{i}",'updatedRows':1,'updatedColumns':4}}
  if rng=="'Math Puzzles'!A1:D1":return {'values':[copy.deepcopy(self.rows[0])]}
  if rng=="'Math Puzzles'!A:D":return {'values':copy.deepcopy(self.rows)}
  i=m.own_range(rng);return {'values':[copy.deepcopy(self.rows[i-1])] if i<=len(self.rows) else []}
 def runner(self,args,**kwargs):
  self.calls.append({'service':'kit','args':list(args),'kwargs':{k:str(v) for k,v in kwargs.items()}})
  action=args[6]
  if action=='stage':
   self.stage_calls+=1;self.record=copy.deepcopy(self.f.z);self.record['state']='draft'
  elif action=='publish':
   self.publish_calls+=1;self.record=copy.deepcopy(self.f.z)
   if self.fail_publish:raise TimeoutError('independent injected publish-after-commit response loss')
  elif action=='check':return types.SimpleNamespace(returncode=0,stdout=enc({'environment':'production','state':'checked'}),stderr=b'')
  elif action=='inspect':
   if self.inspect_hook:
    answer=self.inspect_hook()
    if answer is not None:return types.SimpleNamespace(returncode=0,stdout=enc(answer),stderr=b'')
   if self.record is None:raise RuntimeError('No service record')
  else:raise AssertionError(('unexpected kit action',args))
  answer={k:v for k,v in self.record.items() if k!='gate_sha256'}
  return types.SimpleNamespace(returncode=0,stdout=enc(answer),stderr=b'')
 def inspect(self,g):return self.f.m.observe_publication(g,self.runner)

class Native:
 """Native tree/object API implemented in memory; has no Git/process/service calls."""
 def __init__(self,f):
  self.f=f;self.commits={};self.trees={};self.blobs={};self.calls=[];self.seq=0;self.main='b'*40;self.pr={'head':{'sha':f.m.HEAD},'state':'open','merged':False,'draft':True,'title':'','body':''};self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *a:None)))
 def tree(self,files):
  entries={}
  for n,b in files.items():
   p=digest(b);self.blobs[p['git_blob']]=b;entries[n]=('100644','blob',p['git_blob'])
  tid=sha(enc(entries))[:40];self.trees[tid]=entries;return tid
 def seed(self,name,files,parents=None):
  tid=self.tree(files);self.commits[name]={'sha':name,'tree':{'sha':tid},'parents':[{'sha':p} for p in parents or []],'message':'Independent fixture parent'};return name
 def body_at(self,n,commit):return self.blobs[self.trees[self.commits[commit]['tree']['sha']][n][2]]
 def lookup(self,tree,n):return self.trees[tree].get(n)
 def changed_leaves(self,before,after):return {n for n in set(self.trees[before])|set(self.trees[after]) if self.trees[before].get(n)!=self.trees[after].get(n)}
 def ancestor(self,ancestor,child):return ancestor==child or any(self.ancestor(ancestor,p['sha']) for p in self.commits[child]['parents'])
 def api(self,path,method='GET',body=None):
  self.calls.append({'path':path,'method':method})
  if path=='pulls/191':return copy.deepcopy(self.pr)
  if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
  if path.startswith('git/commits/'):return copy.deepcopy(self.commits[path.split('/')[-1]])
  if path.startswith('compare/'):
   a,b=path[8:].split('...');return {'status':'identical' if a==b else 'ahead' if self.ancestor(a,b) else 'diverged'}
  if path=='git/blobs' and method=='POST':
   b=base64.b64decode(body['content']);k=digest(b)['git_blob'];self.blobs[k]=b;return {'sha':k}
  if path=='git/trees' and method=='POST':
   entries=copy.deepcopy(self.trees[body['base_tree']])
   for e in body['tree']:
    if 'content' in e:
     b=e['content'].encode();k=digest(b)['git_blob'];self.blobs[k]=b
    else:k=e['sha']
    entries[e['path']]=(e['mode'],e['type'],k)
   tid=sha(enc(entries))[:40];self.trees[tid]=entries;return {'sha':tid}
  if path=='git/commits' and method=='POST':
   self.seq+=1;cid=sha(enc(body)+str(self.seq).encode())[:40];co={'sha':cid,'tree':{'sha':body['tree']},'parents':[{'sha':p} for p in body['parents']],'message':body['message']};self.commits[cid]=co;return copy.deepcopy(co)
  raise AssertionError(('Unhandled native API',path,method))
 def coherent_commit_change(self,r,n,b):
  """Recompute body, selected map, tree and exact operative message coherently."""
  r=copy.deepcopy(r);old=self.commits[r['commit']];tree=copy.deepcopy(self.trees[r['tree']]);x=digest(b);self.blobs[x['git_blob']]=b;tree[n]=('100644','blob',x['git_blob']);tid=sha(enc(tree))[:40];self.trees[tid]=tree;r['tree']=tid;r['selected_files'][n]=x;r['selected_map_sha256']=self.f.m.selected_digest(r['selected_files']);r['changed_paths']=sorted(self.changed_leaves(r['parent_tree'],tid));parents=[v['sha'] for v in old['parents']];co=self.api('git/commits','POST',{'tree':tid,'parents':parents,'message':self.f.m.operative_message(self.f.z,parents,r['selected_map_sha256'])});r['commit']=co['sha'];return r
 def descendant(self,n,b):
  old=self.main;entries={path:self.body_at(path,old) for path in self.trees[self.commits[old]['tree']['sha']]};entries[n]=b;cid=sha((old+n+sha(b)).encode())[:40];self.seed(cid,entries,[old]);self.main=cid;return cid

class Fixture:
 def __init__(self,name):
  self.root=FIXTURES/name
  if self.root.exists():shutil.rmtree(self.root)
  self.root.mkdir();self.m=load();m=self.m;m.A=self.root;m.R=self.root/'NO_REAL_REPOSITORY';self.clock=datetime.datetime(2026,10,15,7,0,0,tzinfo=datetime.timezone.utc)
  def tick():
   self.clock+=datetime.timedelta(microseconds=1);return self.clock.isoformat()
  m.now=tick
  self.g={'schema':'PR191_LIFECYCLE_GATE_V1','status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':191,'original_head':m.HEAD,'qualified_note_route_authorized':True,'historical_priority_clearance':False,'all_required_findings_globally_resolved':True,'whole_package_reviews':[],'last_review_required_repairs':0,'package_name':'package_fixture','paper_files':{'pdf':'note.pdf','source':'note.tex','support':'support.zip','metadata':'metadata.json'},'payloads':{},'native_pending_template':'native_template_pending_05','native_final_template':'native_template_final_05','native_complete_template':'native_template_complete_05','native_proof_paths':['PROOF.md'],'native_json_status_paths':sorted(m.JSON_FACTS),'native_text_status_replacements':{n:'Pending factual status at original fixture snapshot.' for n in m.TEXT_FACTS},'public_case_paths':['CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json'],'public_case_pins':{}}
  g=self.g
  for i in [1,2]:
   for role in ['report','seal','root_authentication']:save(self.root/f'science_review_{i}_{role}.json',{'fixture':True,'id':i,'role':role})
   g['whole_package_reviews'].append({'reviewer_id':f'independent-science-{i}','disposition':'PASS','authoritative':True,**{role:bind(self.root,f'science_review_{i}_{role}.json') for role in ['report','seal','root_authentication']}})
  proof=b'Independent synthetic fixture proof, not an actual scientific package.\n'
  save(self.root/'CURRENT_PROOF.md',proof);g['current_proof']=bind(self.root,'CURRENT_PROOF.md')
  native={n:enc({'scientific_protected':{'claim':'DO NOT CHANGE','nested':[1,2,3]},'UTC':'2026-09-01T00:00:00+00:00','case_percent':0,'actual_DOI':None,'actual_Zenodo_published':False,'actual_original_PR_merged':False}) for n in m.JSON_FACTS}
  native.update({n:b'Protected scientific prose\nPending factual status at original fixture snapshot.\nProtected end.\n' for n in m.TEXT_FACTS});native['RESEARCH_LOG.md']=b'Dated immutable scientific history\n';native['PROOF.md']=proof
  original=[]
  for i in range(16):
   n=f'original_{i:02}.txt';b=f'Original artifact {i}: exact bytes\n'.encode();native['ORIGINAL_SUBMISSION/'+n]=b;original.append({'path':m.NATIVE+n,**digest(b)})
  for i in range(50-len(native)):native[f'science_aux/{i:02}.txt']=f'Protected auxiliary {i}\n'.encode()
  assert len(native)==50
  for n,b in native.items():save(self.root/'integration_preparation'/g['native_pending_template']/n,b)
  save(self.root/'ORIGINAL_FILE_MANIFEST.json',{'original_head':m.HEAD,'files':original})
  manifest={'current_template':g['native_pending_template'],'files':{n:digest(b) for n,b in native.items()}}
  save(self.root/'integration_preparation/PENDING_MANIFEST.json',manifest);g['native_pending_manifest']=bind(self.root,'integration_preparation/PENDING_MANIFEST.json')
  save(self.root/'integration_preparation/CURRENT_TEMPLATE.json',manifest)
  save(self.root/'package_fixture/note.pdf',b'%PDF-1.4 synthetic fixture\n');save(self.root/'package_fixture/note.tex',b'Synthetic note source.\n');save(self.root/'package_fixture/support.zip',b'PK synthetic support\n')
  metadata={'title':'Synthetic credited qualified note','files':[{'path':g['paper_files'][k],'name':g['paper_files'][k]} for k in ['pdf','source','support']]}
  save(self.root/'package_fixture/metadata.json',metadata)
  for n in g['paper_files'].values():g['payloads'][n]={k:v for k,v in pin(self.root/'package_fixture'/n).items() if k!='git_blob'}
  for key,n,v in [('pr_metadata_proposal','METADATA_PROPOSAL.json',{'title':'Credited qualified synthetic fixture','body_before_publication':'Prior mechanisms credited. No novelty.'}),('tracker_row_proposal','TRACKER_PROPOSAL.json',{'original_problem':'Synthetic fixture problem5000005','solution_chat_url':'','notes':'Synthetic test only; credited qualified note.'}),('review_input','REVIEW_INPUT.json',{'synthetic_fixture':True})]:save(self.root/n,v);g[key]=bind(self.root,n)
  save(self.root/'INTAKE_CHECKPOINT_ACCEPTANCE.json',{'PR':191,'original_head':m.HEAD,'checkpoint_commit':'a'*40})
  save(self.root/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json',{'synthetic_fixture':True,'original_head':m.HEAD,'original_base':m.ORIGINAL_BASE})
  save(self.root/'RESEARCH_LOG.md',b'Trusted dated Root history, preserved.\n')
  case={k:('Synthetic trusted '+k) for k in m.CASE_PROTECTED_KEYS};case.update(PR=191,problem_id=5000005,original_head=m.HEAD,original_QUEUE_status='claimed_solved',original_effort='2/5',mathematical_clearance=True,priority_clearance=False,goal_complete=False,bounded_priority_audit_complete=True,current_primary_overlap_verified=True,novelty_clearance=False,qualified_credited_note_route_authorized=True,current_proof='CURRENT_PROOF.md',current_proof_SHA256=g['current_proof']['sha256'],scientific_package_ready=True,UTC='2026-10-15T06:59:00+00:00',status='ROOT_AUTHORIZED_PENDING')
  save(self.root/'CURRENT_CASE_STATUS.json',case);save(self.root/m.CASE_PROJECTION,m.case_scientific_projection(case));g['public_case_pins'][m.CASE_PROJECTION]={k:v for k,v in pin(self.root/m.CASE_PROJECTION).items() if k!='git_blob'}
  for n in m.CONTROL_FILES:
   save(self.root/n,(SOURCE/n).read_bytes())
  for role in ['report','seal','root_authentication']:save(self.root/f'operations_{role}.json',{'synthetic_fixture':True,'role':role})
  op={'UTC':'2026-10-15T06:59:00+00:00','status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','PR':191,'original_head':m.HEAD,'all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':{n:{k:v for k,v in pin(self.root/n).items() if k!='git_blob'} for n in m.CONTROL_FILES},'independent_adversary_review':{'disposition':'PASS',**{role:bind(self.root,f'operations_{role}.json') for role in ['report','seal','root_authentication']}}}
  save(self.root/m.OP_CLEARANCE,op);g['public_case_pins'][m.OP_CLEARANCE]={k:v for k,v in pin(self.root/m.OP_CLEARANCE).items() if k!='git_blob'}
  save(self.root/'IMMUTABLE_SUPPORT.txt',b'Root reviewed exact content\n');g['public_case_pins']['IMMUTABLE_SUPPORT.txt']={k:v for k,v in pin(self.root/'IMMUTABLE_SUPPORT.txt').items() if k!='git_blob'}
  save(self.root/'ROOT_PUBLICATION_GATE.json',g)
  self.z={'environment':'production','id':777777777,'state':'published','doi':'10.9999/independent-fixture05','doi_url':'https://doi.org/10.9999/independent-fixture05','record_url':'https://zenodo.org/records/777777777','files':[{'name':g['paper_files'][k],'size':g['payloads'][g['paper_files'][k]]['bytes'],'sha256':g['payloads'][g['paper_files'][k]]['sha256']} for k in ['pdf','source','support']],'metadata_normalizations':[],'doi_resolution':{'status':'resolved'},'receipt_saved':True,'verified_utc':'2026-10-15T06:59:59+00:00','gate_sha256':pin(self.root/'ROOT_PUBLICATION_GATE.json')['sha256']}
  self.service=Service(self);self.native=Native(self);m._helpers=self.native;m._runtime={'runner':self.service.runner,'inspect':self.service.inspect,'tracker':self.service.tracker}
  before={'UTC':'2026-09-01T00:00:00+00:00','updated_UTC':'2026-09-01T00:00:00+00:00','current_PR':191,'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'last_published_PR':190,'dated_eligible_total':99,'fully_completed_eligible_PRs':list(range(100,138))+[190],'published_PRs':list(range(100,122))+[190],'skipped_since_last_completion':[],'next_intake_requires_actual_completion_receipt':True,'completion_metadata_checkpoint_pending_at_snapshot':True}
  self.before=before
  row='| 5000005 / synthetic | one | two | three | four | five | six | claimed_solved | 2/5 | https://github.com/AlecKriebel/Math/pull/191 | original comment | old doi |'
  assert len(row.split('|'))==14
  queue='Immutable QUEUE header\n| FOREIGN_ROW_CANARY | exact unaltered bytes |\n'+row+'\n| FOREIGN_ROW_TAIL | keep |\n';self.queue=queue
  files={m.PREFIX+'CURRENT_PROGRESS.json':enc(before),m.PREFIX+'CURRENT_PROGRESS.md':b'Trusted dated programme history\n',m.PREFIX+'RESEARCH_LOG.md':b'Trusted programme log history\n','unsolved_math_prioritization/QUEUE.md':queue.encode(),'FOREIGN_REPO_CANARY.txt':b'exact foreign bytes'}
  self.native.seed(self.native.main,files);self.native.seed(m.HEAD,{'unsolved_math_prioritization/QUEUE.md':queue.encode()});self.native.seed(m.ORIGINAL_BASE,{'unsolved_math_prioritization/QUEUE.md':queue.encode()})
 def publish_and_track(self):
  m=self.m;m.run_zenodo('check');m.run_zenodo('stage');m.run_zenodo('inspect');m.run_zenodo('publish',str(self.z['id']));m.run_zenodo('inspect-published');self.tr=m.record_tracker(self.service.tracker);return self.tr
 def through95(self):
  self.publish_and_track();m=self.m;m.prepare_native(False);request=m.metadata_request();self.native.pr.update(draft=False,title=request['request']['title'],body=request['request']['body']);save(self.root/'PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':m.HEAD,'gate_sha256':self.z['gate_sha256'],'request_sha256':pin(self.root/'PR_METADATA_REQUEST.json')['sha256']});m.final_scope();self.merge=m.integration_prepare('merge_preparation_independent05');return self.merge
 def adopt95(self,r=None):
  if r is not None:self.merge=r;save(self.root/'SCOPED_MERGE_PREPARATION.json',r)
  self.native.main=self.merge['commit'];self.native.pr.update(merged=True,state='closed');self.accepted95=self.m.integration_accept();return self.accepted95
 def through100(self):
  self.through95();self.adopt95();self.factual=self.m.factual_prepare('factual_preparation_independent05');return self.factual
 def adopt100(self,r=None):
  if r is not None:self.factual=r;save(self.root/'FINAL_FACTUAL_PREPARATION.json',r)
  self.native.main=self.factual['commit'];self.accepted100=self.m.factual_accept();return self.accepted100

# Independent pre-execution probe inventory. Not derived from author tests.
INVENTORY={'families':['inert imports and explicit runtime','valid full 50/16 native lifecycle','exact gate/science/runtime identities','publication service mismatch and uncertain writes','single RAW append, private baseline, fresh target/own/full observations','full native science and companion preservation','original head/metadata/ready','true parent/full tree/selected content/message','coherent QUEUE historical/foreign attacks','both programme dates at95/100 inclusive bounds/order','complete factual postimages and no early cursor advance','immutable stale-MAIN retry','Root handoff static authenticated installation boundary']}

def main():
 save(HERE/'PROBE_INVENTORY.json',INVENTORY)
 f=Fixture('full_positive')
 expect('01 gate positive complete synthetic fixture50 original16',f.m.gate)
 expect('02 valid full flow publication-to-actual-factual-acceptance',lambda:(f.through100(),f.adopt100()))
 if not hasattr(f,'accepted100'):
  save(HERE/'RESULTS.json',{'tests':RESULTS});return
 expect('03 programme live cursor remains191 even factual commit',lambda:assert_(json.loads(f.native.body_at(f.m.PREFIX+'CURRENT_PROGRESS.json',f.factual['commit']))['next_numeric_intake_cursor']==191))
 expect('04 factual receipt alone authorizes subsequent intake',lambda:assert_(f.accepted100['next_numeric_intake_cursor_authorized_after_this_acceptance']==192))
 expect('05 service exactly one stage publish RAW append',lambda:assert_((f.service.stage_calls,f.service.publish_calls,f.service.append_calls)==(1,1,1)))
 run_attacks(f)
 summary={'total':len(RESULTS),'passed':sum(x['passed'] for x in RESULTS),'required_failures':[x for x in RESULTS if not x['passed']]}
 print(json.dumps(summary,indent=2))
 save(HERE/'RESULTS.json',{'summary':summary,'tests':RESULTS})

def run_attacks(f):
 m=f.m;h=f.native;g=f.g;z=f.z;tr=f.tr
 # Every coherent candidate has a new complete selected map, valid exact message,
 # true parent, correct full-tree delta and matching native object identities.
 original_merge=copy.deepcopy(f.merge);original_fact=copy.deepcopy(f.factual)
 accepted95=(f.root/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').read_bytes()
 def accept95(r):
  oldmain=h.main;oldpr=copy.deepcopy(h.pr);oldprep=(f.root/'SCOPED_MERGE_PREPARATION.json').read_bytes()
  try:
   save(f.root/'SCOPED_MERGE_PREPARATION.json',r);h.main=r['commit'];h.pr.update(merged=True,state='closed');return m.integration_accept()
  finally:
   h.main=oldmain;h.pr=oldpr;save(f.root/'SCOPED_MERGE_PREPARATION.json',oldprep);save(f.root/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted95)
 def accept100(r):
  oldmain=h.main;oldprep=(f.root/'FINAL_FACTUAL_PREPARATION.json').read_bytes()
  try:save(f.root/'FINAL_FACTUAL_PREPARATION.json',r);h.main=r['commit'];return m.factual_accept()
  finally:h.main=oldmain;save(f.root/'FINAL_FACTUAL_PREPARATION.json',oldprep)
 def changed(r,n,mut):
  b=h.body_at(n,r['commit']);return h.coherent_commit_change(r,n,mut(b))
 def jsonchange(r,n,key,value):
  def mutate(b):j=json.loads(b);j[key]=value;return enc(j)
  return changed(r,n,mutate)
 # No-effects imports: sentinel real process/network calls and import each adapter.
 def imports():
  oldrun=subprocess.run;oldconnect=socket.socket.connect;oldalias=sys.modules.get('lifecycle_common')
  def forbidden(*a,**k):raise AssertionError('Import attempted process or network')
  subprocess.run=forbidden;socket.socket.connect=forbidden;sys.modules['lifecycle_common']=m
  before={str(p.relative_to(f.root)):sha(p.read_bytes()) for p in f.root.rglob('*') if p.is_file()}
  try:
   for n in [*m.CONTROL_FILES[1:],'protect_canonical_outputs.py']:
    spec=importlib.util.spec_from_file_location('independent_inert_'+n[:-3],SOURCE/n);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
   after={str(p.relative_to(f.root)):sha(p.read_bytes()) for p in f.root.rglob('*') if p.is_file()};assert before==after
  finally:
   subprocess.run=oldrun;socket.socket.connect=oldconnect
   if oldalias is None:sys.modules.pop('lifecycle_common',None)
   else:sys.modules['lifecycle_common']=oldalias
 expect('06 inert imports all adapters no process/network/fixture mutation',imports)
 oldruntime=m._runtime;m._runtime=None
 expect('07 direct publication consumption without runtime rejects',lambda:m.publication(g),True)
 m._runtime=oldruntime
 # Gate alterations use one independent authority variable at a time.
 gatepath=f.root/'ROOT_PUBLICATION_GATE.json';gatebytes=gatepath.read_bytes()
 def gate_mutate(mut):
  j=copy.deepcopy(g);mut(j);save(gatepath,j)
  try:return m.gate()
  finally:save(gatepath,gatebytes)
 for label,mut in [
 ('draft gate',lambda j:j.update(status='DRAFT_READY_FOR_AUTHORIZED_PUBLICATION')),
 ('wrong original head',lambda j:j.update(original_head='d'*40)),
 ('unresolved repairs',lambda j:j.update(all_required_findings_globally_resolved=False)),
 ('duplicate science identity',lambda j:j['whole_package_reviews'][1].update(reviewer_id=j['whole_package_reviews'][0]['reviewer_id'])),
 ('duplicated scientific evidence',lambda j:j['whole_package_reviews'][1].update(report=j['whole_package_reviews'][0]['report'])),
 ('latest science review unfinished',lambda j:j['whole_package_reviews'][-1].update(disposition='REPAIR_REQUIRED')),
 ('missing exact runtime clearance',lambda j:j['public_case_pins'].pop(m.OP_CLEARANCE)),
 ('missing scientific projection',lambda j:j['public_case_pins'].pop(m.CASE_PROJECTION))]:expect('08 gate '+label,lambda mut=mut:gate_mutate(mut),True)
 runtimepath=f.root/'record_tracker.py';runtimebytes=runtimepath.read_bytes();save(runtimepath,runtimebytes+b'\n# unauthorized drift\n');expect('09 installed runtime drift',lambda:m.gate(),True);save(runtimepath,runtimebytes)
 # Publication receipts bind all exact output and fresh observations.
 for key,val in [('environment','sandbox'),('id',True),('state','draft'),('doi_url','https://doi.org/10.9999/wrong'),('gate_sha256','f'*64),('verified_utc','2099-01-01T00:00:00+00:00'),('files',z['files'][:-1])]:
  j=copy.deepcopy(z);j[key]=val;expect('10 publication rejects '+key,lambda j=j:m.validate_publication(g,j),True)
 observed=copy.deepcopy(f.service.record);f.service.record['files'][0]['sha256']='f'*64;expect('11 fresh consumer rejects service file drift',lambda:m.published_tracked(),True);f.service.record=copy.deepcopy(observed)
 f.service.record['doi']='10.9999/wrong';f.service.record['doi_url']='https://doi.org/10.9999/wrong';expect('12 fresh consumer rejects changed assigned DOI',lambda:m.published_tracked(),True);f.service.record=copy.deepcopy(observed)
 # Tracker exact targets, baseline, row and DOI uniqueness at later consumers.
 rows=copy.deepcopy(f.service.rows)
 f.service.rows[1][-1]='CHANGED_FOREIGN_CANARY';expect('13 fresh consumer rejects foreign row edit',lambda:m.published_tracked(),True);f.service.rows=copy.deepcopy(rows)
 f.service.rows+=copy.deepcopy([rows[-1]]);expect('14 fresh consumer rejects duplicate DOI row',lambda:m.published_tracked(),True);f.service.rows=copy.deepcopy(rows)
 f.service.rows[-1][3]='unapproved notes';expect('15 fresh consumer rejects own four-cell drift',lambda:m.published_tracked(),True);f.service.rows=copy.deepcopy(rows)
 f.service.track_hook=lambda resource,method,params,body: {'spreadsheetId':m.SID,'sheets':[{'properties':{'sheetId':m.GID,'title':'Wrong tab'}}]} if resource=='spreadsheet' else None
 expect('16 fresh consumer rejects target gid/tab drift',lambda:m.published_tracked(),True);f.service.track_hook=None
 f.service.rows.append(['NEW_FOREIGN','addition','','']);expect('17 fresh consumer permits ordered unrelated tracker addition',lambda:m.published_tracked());f.service.rows=copy.deepcopy(rows)
 def no_leak():
  for p in [f.root/'TRACKER_ACCEPTANCE.json',*sorted((f.root/'sheets_tracking').glob('*.json'))]:
   b=p.read_bytes();assert b'FOREIGN_CANARY' not in b and b'secret-note' not in b,p.name
 expect('18 sanitized public tracker receipts omit foreign rows',no_leak)
 # Exact full native bytes, not self-consistent receipt hashes.
 pointer=f.root/'integration_preparation/CURRENT_TEMPLATE.json';cur=json.loads(pointer.read_bytes());manifest=f.root/'integration_preparation'/(cur['current_template']+'_MANIFEST.json');pointerbytes=pointer.read_bytes();manifestbytes=manifest.read_bytes();nativepath=f.root/'integration_preparation'/cur['current_template']/'CURRENT_RESULT.json';old=nativepath.read_bytes();j=json.loads(old);j['scientific_protected']['nested'][0]=999;save(nativepath,j);poisoned=copy.deepcopy(cur);poisoned['files']['CURRENT_RESULT.json']=pin(nativepath);save(pointer,poisoned);save(manifest,poisoned)
 expect('19 native scientific JSON drift with rehashed pointer+manifest',lambda:m.current_native(g,True,(z,tr)),True);save(nativepath,old);save(pointer,pointerbytes);save(manifest,manifestbytes)
 save(manifest,manifestbytes+b' ');expect('20 native companion exact bytes',lambda:m.current_native(g,True,(z,tr)),True);save(manifest,manifestbytes)
 originalpath=f.root/'integration_preparation'/cur['current_template']/'ORIGINAL_SUBMISSION/original_00.txt';old=originalpath.read_bytes();save(originalpath,old+b'changed');expect('21 original16 preserved byte-exact',lambda:m.current_native(g,True,(z,tr)),True);save(originalpath,old)
 # Coherent QUEUE attacks must survive basic producer receipts to reach actual stage defense.
 q='unsolved_math_prioritization/QUEUE.md'
 for label,mut in [('foreign row',lambda b:b.replace(b'FOREIGN_ROW_CANARY',b'FOREIGN_ROW_CORRUPTED')),('historical status',lambda b:b.replace(b'| claimed_solved | 2/5 |',b'| solved | 5/5 |')),('actual DOI',lambda b:b.replace(z['doi'].encode(),b'10.9999/fabricated'))]:
  r=changed(original_merge,q,mut);expect('22 coherent QUEUE '+label+' map/tree/message internally valid',lambda r=r:m.verify_prepared(h,r,[r['expected_main'],m.HEAD]));expect('23 actual merge rejects coherent QUEUE '+label,lambda r=r:accept95(r),True)
 # Programme dates: BOTH fields, stage95 and100, lower/upper/order and inclusive bounds.
 for phase,r in [(95,original_merge),(100,original_fact)]:
  n=m.PREFIX+'CURRENT_PROGRESS.json';lower=max(m.valid_stamp(z['verified_utc']),m.valid_stamp(tr['UTC']))
  if phase==100:lower=max(lower,m.valid_stamp(json.loads(accepted95)['UTC']))
  upper=f.clock
  for key in ['UTC','updated_UTC']:
   for value,kind in [((lower-datetime.timedelta(microseconds=1)).isoformat(),'before evidence'),('2099-01-01T00:00:00+00:00','future'),('2026-02-30T00:00:00+00:00','invalid date'),('2026-10-15T00:00:00-07:00','non UTC')]:
    attack=jsonchange(r,n,key,value);expect(f'24 phase{phase} {key} {kind}',lambda attack=attack,phase=phase:m.verify_stage_postimage(h,g,z,tr,attack,phase,original_merge['commit'] if phase==100 else None),True)
  def dated(b):j=json.loads(b);j['UTC']=lower.isoformat();j['updated_UTC']=lower.isoformat();return enc(j)
  same=changed(r,n,dated);expect(f'25 phase{phase} inclusive evidence lower bound both dates',lambda same=same,phase=phase:m.verify_stage_postimage(h,g,z,tr,same,phase,original_merge['commit'] if phase==100 else None))
  def reversed_dates(b):j=json.loads(b);j['UTC']=(lower+datetime.timedelta(microseconds=2)).isoformat();j['updated_UTC']=(lower+datetime.timedelta(microseconds=1)).isoformat();return enc(j)
  attack=changed(r,n,reversed_dates);expect(f'26 phase{phase} dates reversed within allowed interval',lambda attack=attack,phase=phase:m.verify_stage_postimage(h,g,z,tr,attack,phase,original_merge['commit'] if phase==100 else None),True)
 # Approved static payload/source contents, complete tree delta, exact operative message.
 for n in [m.CASE+'IMMUTABLE_SUPPORT.txt',m.CASE+'package_fixture/note.tex',m.CASE+'lifecycle_common.py']:
  r=changed(original_merge,n,lambda b:b+b'UNAPPROVED_CONTENT\n');expect('27 coherent unapproved content rejected '+n,lambda r=r:accept95(r),True)
 r=copy.deepcopy(original_merge);h.commits[r['commit']]['message']+='\nNew unsupported novelty claim';expect('28 exact immutable operative message forbids suffix',lambda:accept95(r),True);h.commits[r['commit']]['message']=m.operative_message(z,[r['expected_main'],m.HEAD],r['selected_map_sha256'])
 r=copy.deepcopy(original_merge);r['parent_tree']='f'*40;expect('29 true parent tree mismatch',lambda:accept95(r),True)
 # Coherent partial-fact and mutable case-log attacks: expected rejection.
 n=m.PREFIX+'CURRENT_PROGRESS.json'
 for key,value in [('advance_to_next_PR_authorized_now',True),('next_numeric_intake_cursor',192),('fully_completed_eligible_PRs',[*f.before['fully_completed_eligible_PRs'][:-1],191]),('current_priority_clearance',True)]:
  r=jsonchange(original_merge,n,key,value);expect('30 exact programme facts reject '+key,lambda r=r:accept95(r),True)
 # Target current factual aliases which the honest generator sets or retires.
 for key,value in [('next_intake_requires_actual_completion_receipt',False),('actual_factual_checkpoint_accepted',True),('last_completed_actual_final_receipt','audits/pr191_5000005/ROOT_FINAL_FACTUAL_ACCEPTANCE.json'),('completion_metadata_checkpoint_pending_at_snapshot',False)]:
  r=jsonchange(original_merge,n,key,value);out=expect('31 current programme factual alias must reject '+key,lambda r=r:accept95(r),True)
  if out is not None:save(HERE/('COUNTEREXAMPLE_programme_'+key+'.json'),{'field':key,'value':value,'phase':95,'candidate':r,'actual_acceptance':out})
 # Modify only the newly generated factual case log, retaining all trusted history/science.
 n=m.CASE+'RESEARCH_LOG.md'
 def false_log(b):return b+('\n'+m.now()+' — PR191 actual factual MAIN acceptance complete; PR192 intake is already authorized and complete.\n').encode()
 r=changed(original_merge,n,false_log);out=expect('32 false current Root case log factual acceptance/PR192 claim rejected',lambda:accept95(r),True)
 if out is not None:save(HERE/'COUNTEREXAMPLE_case_log.json',{'phase':95,'candidate':r,'actual_acceptance':out,'changed_path':n,'original_body_sha256':sha(h.body_at(n,original_merge['commit'])),'false_body':h.body_at(n,r['commit']).decode()})
 # Repeat programme gap at the final combined factual consumer.
 n=m.PREFIX+'CURRENT_PROGRESS.json'
 for key,value in [('next_intake_requires_actual_completion_receipt',False),('actual_factual_checkpoint_accepted',True),('completion_metadata_checkpoint_pending_at_snapshot',True),('last_completed_actual_final_receipt','audits/pr190_5000007/ROOT_FINAL_FACTUAL_ACCEPTANCE.json')]:
  r=jsonchange(original_fact,n,key,value);out=expect('32b factual100 current programme alias must reject '+key,lambda r=r:accept100(r),True)
  if out is not None:save(HERE/('COUNTEREXAMPLE_factual100_'+key+'.json'),{'field':key,'value':value,'phase':100,'candidate':r,'actual_acceptance':out})
 n=m.CASE+'RESEARCH_LOG.md';r=changed(original_fact,n,false_log);out=expect('32c factual100 false current Root log PR192 intake claim rejected',lambda r=r:accept100(r),True)
 if out is not None:save(HERE/'COUNTEREXAMPLE_factual100_case_log.json',{'phase':100,'candidate':r,'actual_acceptance':out,'changed_path':n,'original_body_sha256':sha(h.body_at(n,original_fact['commit'])),'false_body':h.body_at(n,r['commit']).decode()})
 # Exact inclusive upper boundaries at both stages, using a frozen validation clock.
 for phase,r in [(95,original_merge),(100,original_fact)]:
  n=m.PREFIX+'CURRENT_PROGRESS.json';upper=f.clock.isoformat()
  def upper_dates(b):j=json.loads(b);j['UTC']=upper;j['updated_UTC']=upper;return enc(j)
  attack=changed(r,n,upper_dates);oldnow=m.now;m.now=lambda:upper
  try:expect(f'32d phase{phase} inclusive current-clock upper bound both dates',lambda attack=attack,phase=phase:m.verify_stage_postimage(h,g,z,tr,attack,phase,original_merge['commit'] if phase==100 else None))
  finally:m.now=oldnow
 # Factual100 postimage facts and independently approved protected case.
 n=m.CASE+'CURRENT_CASE_STATUS.json'
 for key,value in [('goal_complete',True),('original_effort','5/5'),('actual_original_PR_merged',False),('case_completion_requires_actual_factual_postimage_acceptance',False)]:
  r=jsonchange(original_fact,n,key,value);expect('33 factual100 case rejects '+key,lambda r=r:accept100(r),True)
 n=m.CASE+'WORKFLOW_COMPLETION.json';r=jsonchange(original_fact,n,'status','ACTUAL_FACTUAL_COMPLETION_ACCEPTED');expect('34 factual100 exact workflow prevents premature effective status',lambda:accept100(r),True)
 # Actual-current identity checks must reject drift in selected paths but permit foreign descendants.
 oldmain=h.main;h.main=original_fact['commit'];h.descendant('FOREIGN_ADDITION.txt',b'unrelated descendant bytes');expect('35 factual acceptance permits unrelated descendant',m.factual_accept)
 h.descendant(m.CASE+'IMMUTABLE_SUPPORT.txt',b'unauthorized actual MAIN drift');expect('36 combined actual MAIN selected identities reject support drift',m.factual_accept,True);h.main=oldmain
 # Explicit unsure-write probes: native service can commit then lose response.
 u=Fixture('uncertain_publish');u.m.run_zenodo('stage');u.service.fail_publish=True;expect('37 uncertain publication first POST committed but response lost',lambda:u.m.run_zenodo('publish',str(u.z['id'])),True);u.service.fail_publish=False;expect('38 uncertain publication retry reconciles read-only published record',lambda:u.m.run_zenodo('publish',str(u.z['id'])));expect('39 no duplicate publication POST after response loss',lambda:assert_(u.service.publish_calls==1))
 u=Fixture('uncertain_append');u.m.run_zenodo('stage');u.m.run_zenodo('publish',str(u.z['id']));u.service.fail_append=True;expect('40 uncertain tracker append committed but response lost',lambda:u.m.record_tracker(u.service.tracker),True);u.service.fail_append=False;expect('41 retry accepts exact existing row after two new reads',lambda:u.m.record_tracker(u.service.tracker));expect('42 no duplicate RAW append after response loss',lambda:assert_(u.service.append_calls==1))
 # Unknown absent outcome cannot issue another append.
 u=Fixture('unknown_absent_append');u.m.run_zenodo('stage');u.m.run_zenodo('publish',str(u.z['id']));save(u.root/'sheets_tracking/APPEND_ATTEMPT_STARTED.json',{'unknown':True});expect('43 unknown earlier append with absent row forbids blind retry',lambda:u.m.record_tracker(u.service.tracker),True);expect('44 unknown absent append issued zero writes',lambda:assert_(u.service.append_calls==0))
 # Stale MAIN retry: preserve exact generated100 bytes across unrelated current MAIN change.
 u=Fixture('stale_retry');u.through95();u.adopt95();prior=u.m.factual_prepare('factual_preparation_first');nativebefore={str(p.relative_to(u.root/'integration_preparation'/u.g['native_complete_template'])):sha(p.read_bytes()) for p in (u.root/'integration_preparation'/u.g['native_complete_template']).rglob('*') if p.is_file()};pointerbefore=(u.root/'integration_preparation/CURRENT_TEMPLATE.json').read_bytes();u.native.descendant('UNRELATED_MAIN_AFTER_PREPARE.txt',b'foreign current MAIN addition');retry=expect('45 stale MAIN fresh preparation reuses immutable100 generation',lambda:u.m.factual_prepare('factual_preparation_retry'))
 expect('46 stale retry retains pointer and every native byte',lambda:assert_(pointerbefore==(u.root/'integration_preparation/CURRENT_TEMPLATE.json').read_bytes() and nativebefore=={str(p.relative_to(u.root/'integration_preparation'/u.g['native_complete_template'])):sha(p.read_bytes()) for p in (u.root/'integration_preparation'/u.g['native_complete_template']).rglob('*') if p.is_file()}))
 if retry:expect('47 unchanged-generation stale retry actual full acceptance',lambda:u.adopt100(retry))
 # Self-consistent mutation may not change any scientific bytes in reviewed full generation.
 expect('48 protected fifty-file full derivation after all attacks',lambda:m.current_native(g,True,(z,tr)))
 # Remaining explicit metadata/original-head/native-time/full-tree boundaries.
 oldpr=copy.deepcopy(h.pr);h.pr.update(state='open',merged=False,draft=False)
 expect('49 valid original head metadata ready guards',lambda:(m.original_ready(False),m.require_metadata(g,z,tr,h.pr)))
 for key,value in [('title','unapproved but plausible metadata'),('body','Unsupported novelty claim')]:
  p=copy.deepcopy(h.pr);p[key]=value;expect('50 metadata exact approved '+key,lambda p=p:m.require_metadata(g,z,tr,p),True)
 h.pr['head']['sha']='d'*40;expect('51 original PR head drift',lambda:m.original_ready(False),True);h.pr=copy.deepcopy(oldpr);h.pr.update(state='open',merged=False,draft=True);expect('52 original PR readiness guard',lambda:m.original_ready(False),True);h.pr=oldpr
 expect('53 explicit production entrypoint refuses existing injected context',lambda:m.production_entrypoint(lambda:None),True)
 def bad_native_time(key,value):
  j=copy.deepcopy(cur);j['factual_timestamps'][key]=value;expected=m.derive_native(g,z,tr,m.pending_native_bytes(g),j['factual_timestamps'],True);j['files']={n:digest(b) for n,b in expected.items()};return m.expected_native_receipt(j,g,z,tr,True)
 expect('54 native future generation even coherent reconstructed bytes',lambda:bad_native_time('merged','2099-01-01T00:00:00+00:00'),True)
 stamp=(m.valid_stamp(json.loads(accepted95)['UTC'])-datetime.timedelta(microseconds=1)).isoformat();expect('55 native merged generation before actual accepted merge',lambda:bad_native_time('merged',stamp),True)
 # A foreign tree write omitted from the producer selected map cannot hide in delta.
 r=copy.deepcopy(original_merge);tree=copy.deepcopy(h.trees[r['tree']]);b=b'coherent foreign extra tree change';x=digest(b);h.blobs[x['git_blob']]=b;tree['HIDDEN_FOREIGN_WRITE.txt']=('100644','blob',x['git_blob']);tid=sha(enc(tree))[:40];h.trees[tid]=tree;co=h.api('git/commits','POST',{'tree':tid,'parents':[r['expected_main'],m.HEAD],'message':m.operative_message(z,[r['expected_main'],m.HEAD],r['selected_map_sha256'])});r.update(commit=co['sha'],tree=tid);expect('56 unselected foreign full-tree mutation',lambda:accept95(r),True)
 # Handoff is inspected as source and AST only. No main or installer executes.
 handoff=CASE_ROOT/'prepare_root_publication_clearance_v4.py';hb=handoff.read_bytes()
 expect('57 Root handoff exact frozen v4 content',lambda:assert_(len(hb)==8358 and sha(hb)=='c4f8f2c122e1954d3f3d5cf03d70cd0fe8a243e368efa166171c4aca97f4b548' and stat.S_IMODE(handoff.stat().st_mode)==0o444))
 tree=ast.parse(hb);mainnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');maintext=ast.get_source_segment(hb.decode(),mainnode)
 def handoff_order():
  ordered=["auth=read(A/authname)","auth['status']=='ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW05_PASS'","match(F/'FINAL_SEAL.json',auth['proposal_seal'])","for n,x in runtime.items():match(F/n,x);require(not (A/n).exists()","for n,x in pins.items():match(A/n,x)","with (A/n).open('xb')", "fresh('ROOT_CASE_SCIENTIFIC_PROJECTION.json'", "fresh('ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json'", "m.read=virtual_read;m.gate()", "fresh('ROOT_PUBLICATION_GATE.json',g);m.gate()"]
  offsets=[maintext.index(x) for x in ordered];assert offsets==sorted(offsets)
 expect('58 Root handoff auth+input hashes precede exclusive install and authority',handoff_order)
 def handoff_static():
  assert "for n in ['ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json','ROOT_LIFECYCLE_RUNTIME_INSTALLATION.json','ROOT_CASE_SCIENTIFIC_PROJECTION.json','ROOT_PUBLICATION_GATE.json']:require(not (A/n).exists()" in maintext
  assert "required={'lifecycle_common.py','campaign_aliases.py','run_zenodo_step.py','record_tracker.py','prepare_native_final_01.py','prepare_pr_metadata_request.py','prepare_final_main_scope.py','prepare_final_scoped_merge.py','prepare_factual_completion.py'}" in maintext
  assert "require(set(runtime)==required" in maintext and "all_required_findings_globally_resolved'] is True" in maintext and "outstanding_required_repairs']==[]" in maintext
  imported=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))];assert all('subprocess' not in ast.unparse(n) and 'requests' not in ast.unparse(n) and 'socket' not in ast.unparse(n) for n in imported)
  assert "'actual_publication':False" in maintext and "actual_Zenodo_published=False" in maintext
 expect('59 Root handoff exact9/no-overwrite/no-service/factual authority checks static',handoff_static)
 seed=CASE_ROOT/'IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS04_01.json';sb=seed.read_bytes();sj=json.loads(sb)
 expect('60 dated556 seed exact content and number of immutable pins',lambda:assert_(len(sb)==101959 and sha(sb)=='93a6aae3e4fb11e897495f0ab0955c33c540e9d2cbdaf4bab7331eae3bcce89b' and len(sj['public_case_pins'])==556))
 # Store sanitized traces from synthetic services only (all rows are fabricated canaries).
 save(HERE/'INDEPENDENT_CALL_TRACES.json',{'full_flow_service':f.service.calls,'full_flow_native':f.native.calls,'stale_retry_service':u.service.calls,'stale_retry_native':u.native.calls,'all_services':'offline native/service stubs; no actual production, network, Git, or native helper calls'})

def assert_(v):
 if not v:raise AssertionError('independent assertion failed')

if __name__=='__main__':
 assert sys.dont_write_bytecode, 'Run python3 -B PROBE.py'
 main()

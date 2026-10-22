"""Independent terminal07 validation. Offline synthetic own data only.
Run with python3 -B reproduce_07.py. Writes only beneath this script's folder.
No production subprocess/helper/service, Git command, or Root handoff is run.
"""
from pathlib import Path
from types import SimpleNamespace
import base64, copy, datetime, hashlib, importlib.util, json, shutil, sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'lifecycle_controls_preparation_07'
SOURCE_SHA='c5a15c7b1c4e05b11c60fef73bd0c791d4b0cc46537778f65e1fa58c6f085479'
RESULTS=[]
CANARY='SYNTHETIC_OWN_DIAGNOSTIC_ONLY'

def enc(x):return (json.dumps(x,indent=2)+'\n').encode()
def bp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def pp(b):return {k:v for k,v in bp(b).items() if k!='git_blob'}
def put(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():p.chmod(0o644)
 p.write_bytes(x if isinstance(x,bytes) else enc(x))
def get(p):return json.loads(Path(p).read_bytes())
def outcome(name,fn,expected='REJECT',family='field-validation'):
 try:fn();observed='ACCEPT';error=None
 except Exception as e:observed='REJECT';error=type(e).__name__+': '+str(e)
 ok=(observed==expected)
 RESULTS.append({'case':name,'family':family,'expected':expected,'observed':observed,'met_expectation':ok,'error':error})
 return ok

class Repo:
 def __init__(self,m):
  self.m0=m;self.blobs={};self.trees={};self.commits={};self.main='';self.journal=[]
  self.m=SimpleNamespace(m=SimpleNamespace(h=SimpleNamespace(warm_selected_directories=self.warm)))
  self.pr={'head':{'sha':m.HEAD},'state':'open','merged':False,'draft':False,'title':'','body':''}
 def warm(self,*args):self.journal.append(('warm',len(args[1])))
 def blob(self,b):s=bp(b)['git_blob'];self.blobs[s]=b;return s
 def tree(self,files):
  v={n:('100644','blob',self.blob(b)) for n,b in files.items()}
  return self.tree_values(v)
 def tree_values(self,v):
  s=hashlib.sha1(json.dumps(v,sort_keys=True).encode()).hexdigest();self.trees[s]=copy.deepcopy(v);return s
 def commit(self,files,parents=(),message='Synthetic own fixture',name=None):
  tree=self.tree(files);s=name or hashlib.sha1(enc({'tree':tree,'parents':list(parents),'message':message})).hexdigest()
  self.commits[s]={'sha':s,'tree':{'sha':tree},'parents':[{'sha':x} for x in parents],'message':message};return s
 def files(self,c):return {n:self.blobs[x[2]] for n,x in self.trees[self.commits[c]['tree']['sha']].items()}
 def descends(self,a,b):return b==a or any(self.descends(a,p['sha']) for p in self.commits[b]['parents'])
 def api(self,path,method='GET',data=None):
  self.journal.append((method,path))
  if path=='pulls/191':return copy.deepcopy(self.pr)
  if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
  if path.startswith('git/commits/') and method=='GET':return copy.deepcopy(self.commits[path.split('/')[-1]])
  if path=='git/blobs' and method=='POST':return {'sha':self.blob(base64.b64decode(data['content']))}
  if path=='git/trees' and method=='POST':
   v=copy.deepcopy(self.trees[data['base_tree']])
   for x in data['tree']:v[x['path']]=(x['mode'],x['type'],x.get('sha') or self.blob(x['content'].encode()))
   return {'sha':self.tree_values(v)}
  if path=='git/commits' and method=='POST':
   s=hashlib.sha1(enc(data)).hexdigest();self.commits[s]={'sha':s,'tree':{'sha':data['tree']},'parents':[{'sha':p} for p in data['parents']],'message':data['message']};return copy.deepcopy(self.commits[s])
  if path.startswith('compare/'):
   a,b=path[8:].split('...');return {'status':'identical' if a==b else 'ahead' if self.descends(a,b) else 'diverged'}
  raise AssertionError('Unexpected synthetic repository interface '+method+' '+path)
 def lookup(self,t,n):return self.trees[t].get(n)
 def changed_leaves(self,a,b):return {n for n in set(self.trees[a])|set(self.trees[b]) if self.lookup(a,n)!=self.lookup(b,n)}
 def body_at(self,n,c):self.journal.append(('body',c,n));return self.blobs[self.trees[self.commits[c]['tree']['sha']][n][2]]
 def advance_foreign(self):
  files=self.files(self.main);files['synthetic_unrelated/own_fixture.txt']=b'An unrelated descendant fixture edit.\n';self.main=self.commit(files,[self.main]);return self.main

class World:
 serial=0
 def __init__(self,label):
  World.serial+=1;self.path=HERE/'offline_work'/('%03d_'%World.serial+label)
  if self.path.exists():shutil.rmtree(self.path)
  self.path.mkdir(parents=True)
  assert hashlib.sha256((SOURCE/'lifecycle_common.py').read_bytes()).hexdigest()==SOURCE_SHA
  spec=importlib.util.spec_from_file_location('independent_terminal07_'+str(World.serial),SOURCE/'lifecycle_common.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
  m=self.m;m.A=self.path;m.R=self.path/'synthetic_repository';m.PY='SYNTHETIC_PYTHON';m.GWS='SYNTHETIC_GWS'
  def forbidden(*a,**k):raise AssertionError('Production process use forbidden')
  m.subprocess=SimpleNamespace(run=forbidden);self.ticks=0;m.now=self.clock
  for n in m.CONTROL_FILES:put(self.path/n,(SOURCE/n).read_bytes())
  self.h=Repo(m);m._helpers=self.h
  self.service={'state':'absent','id':7000191,'stage_creations':0,'publish_writes':0,'append_writes':0,'runner_calls':[],'sheet_calls':[],'rows':[copy.deepcopy(m.HEADER)],'fault':None}
  self.build_authority()
  m._runtime={'runner':self.runner,'inspect':lambda g:m.observe_publication(g,self.runner),'tracker':self.sheet}
 def clock(self):
  self.ticks+=1
  return (datetime.datetime(2026,10,1,tzinfo=datetime.UTC)+datetime.timedelta(seconds=self.ticks)).isoformat()
 def pathpin(self,n):return pp((self.path/n).read_bytes())
 def binding(self,n):return {'path':n,**self.pathpin(n)}
 def build_authority(self):
  m=self.m;A=self.path
  proof=b'Synthetic approved mathematical identity; no real theorem is asserted.\n'
  put(A/'CURRENT_PROOF.md',proof)
  names=['paper.pdf','paper.tex','support.zip'];payload={names[0]:b'Synthetic own PDF fixture bytes',names[1]:b'Synthetic own source fixture bytes',names[2]:b'Synthetic own support fixture bytes'}
  payload['deposit.json']=enc({'files':[{'path':n,'name':n} for n in names]})
  for n,b in payload.items():put(A/'package'/n,b)
  native={'ORIGINAL_SUBMISSION/original_%02d.txt'%i:('Original own fixture %02d\n'%i).encode() for i in range(16)}
  originals=[{'path':m.NATIVE+'original_%02d.txt'%i,**pp(native['ORIGINAL_SUBMISSION/original_%02d.txt'%i])} for i in range(16)]
  native.update({'CANDIDATE.md':proof,'PROOF_V4.md':proof,'README.md':b'Synthetic independent fixture. Pending own publication.\n','review/REVIEW.md':b'Synthetic independent review. Pending own review.\n','RESEARCH_LOG.md':b'Own dated native history.\n'})
  facts={'UTC':'2026-09-30T00:00:00+00:00','whole_package_reviews_complete':False,'publication_ready':False,'actual_Zenodo_published':False,'actual_published':False,'actual_DOI':None,'actual_tracker_updated':False,'actual_tracker_range':None,'actual_original_PR_merged':False,'case_percent':50,'snapshot_semantics':'Synthetic pending','whole_package_reviews_pending':True,'successive_NEW_whole_package_reviews_complete':False,'publication_clearance':False,'publication_and_tracker_actions_not_yet_performed':True,'not_an_approval':True,'completed_new_whole_package_reviews':0,'scientific_unchanged':{'marker':'APPROVED_OWN_SCIENCE','novelty':False}}
  native.update({n:enc(facts) for n in sorted(m.JSON_FACTS)})
  for i in range(50-len(native)):native['support/retained_%02d.txt'%i]=('Unchanged approved own support %02d\n'%i).encode()
  assert len(native)==50
  for n,b in native.items():put(A/'integration_preparation/native_template_pending_own'/n,b)
  put(A/'pending_manifest.json',{'current_template':'native_template_pending_own','files':{n:pp(b) for n,b in native.items()}})
  put(A/'ORIGINAL_FILE_MANIFEST.json',{'original_head':m.HEAD,'files':originals})
  put(A/'pr_proposal.json',{'title':'Synthetic own credited note','body_before_publication':'Approved own note; no priority or independence assertion.'})
  put(A/'tracker_proposal.json',{'original_problem':'OWN_SYNTHETIC_5000005','solution_chat_url':'','notes':'Approved own synthetic note.'})
  put(A/'review_input.json',{'synthetic_own_input':True})
  put(A/'INTAKE_CHECKPOINT_ACCEPTANCE.json',{'PR':191,'original_head':m.HEAD,'checkpoint_commit':'1'*40})
  put(A/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json',{'original_head':m.HEAD,'original_proof_parent':m.ORIGINAL_BASE,'original_queue':'claimed_solved','original_effort':'2/5'})
  reviews=[]
  for i in [1,2]:
   bs={}
   for role in ['report','seal','root_authentication']:
    n='science_review_%d_%s.json'%(i,role);put(A/n,{'synthetic_own':role,'round':i});bs[role]=self.binding(n)
   reviews.append({'reviewer_id':'OWN_SCIENCE_REVIEW_'+str(i),'authoritative':True,'disposition':'PASS',**bs})
  baseline={k:'Synthetic protected own value '+k for k in m.CASE_PROTECTED_KEYS}
  baseline.update(PR=191,problem_id=5000005,original_head=m.HEAD,original_QUEUE_status='claimed_solved',original_effort='2/5',current_proof='CURRENT_PROOF.md',current_proof_SHA256=pp(proof)['sha256'],mathematical_clearance=True,priority_clearance=False,goal_complete=False,novelty_clearance=False,qualified_credited_note_route_authorized=True,bounded_priority_audit_complete=True,current_primary_overlap_verified=True,scientific_package_ready=True,operational_lifecycle_audit_active=True,operational_required_repairs=['OWN_HISTORICAL_REPAIR'],whole_package_review_active=True,old_history={'kept':'own exact history'})
  put(A/m.CASE_BASELINE,baseline);put(A/m.CASE_LOG_BASELINE,b'Synthetic own trusted case history.\n');put(A/m.CASE_PROJECTION,m.case_scientific_projection(baseline))
  bs={}
  for role in ['report','seal','root_authentication']:
   n='own_operational_'+role+'.json';put(A/n,{'synthetic_own_authority':role});bs[role]=self.binding(n)
  put(A/m.OP_CLEARANCE,{'UTC':'2026-09-30T00:00:00+00:00','PR':191,'original_head':m.HEAD,'status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':{n:self.pathpin(n) for n in m.CONTROL_FILES},'independent_adversary_review':{'disposition':'PASS',**bs}})
  pinned=[m.CASE_BASELINE,m.CASE_LOG_BASELINE,m.CASE_PROJECTION,m.OP_CLEARANCE]
  g={'UTC':'2026-09-30T00:00:00+00:00','schema':'PR191_LIFECYCLE_GATE_V1','status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':191,'original_head':m.HEAD,'qualified_note_route_authorized':True,'historical_priority_clearance':False,'all_required_findings_globally_resolved':True,'last_review_required_repairs':0,'whole_package_reviews':reviews,'review_input':self.binding('review_input.json'),'package_name':'package','payloads':{n:pp(b) for n,b in payload.items()},'paper_files':dict(zip(['pdf','source','support','metadata'],names+['deposit.json'])),'current_proof':self.binding('CURRENT_PROOF.md'),'native_proof_paths':['CANDIDATE.md','PROOF_V4.md'],'native_pending_template':'native_template_pending_own','native_pending_manifest':self.binding('pending_manifest.json'),'native_final_template':'native_template_final_own','native_complete_template':'native_template_complete_own','native_json_status_paths':sorted(m.JSON_FACTS),'native_text_status_replacements':{'README.md':'Pending own publication.','review/REVIEW.md':'Pending own review.'},'pr_metadata_proposal':self.binding('pr_proposal.json'),'tracker_row_proposal':self.binding('tracker_proposal.json'),'public_case_pins':{n:self.pathpin(n) for n in pinned},'public_case_paths':pinned}
  put(A/'ROOT_PUBLICATION_GATE.json',g);self.g=g;self.baseline=baseline;self.native_pending=native
  put(A/'CURRENT_CASE_STATUS.json',m.derive_case_ready(baseline,g,self.pathpin('ROOT_PUBLICATION_GATE.json')['sha256']))
  put(A/'RESEARCH_LOG.md',(A/m.CASE_LOG_BASELINE).read_bytes()+m.ready_case_log_suffix(g['UTC']).encode())
  programme={'fully_completed_eligible_PRs':list(range(1,39))+[190],'published_PRs':list(range(1,23))+[190],'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'last_published_PR':190,'current_PR':191,'dated_eligible_total':99,'last_completed_actual_final_receipt':'audits/pr190_5000007/ROOT_FINAL_FACTUAL_ACCEPTANCE.json','last_completed_DOI':'10.5281/own_previous190','current_operational_lifecycle_audit_active':True,'current_operational_required_repairs':['OWN_HISTORICAL_REPAIR'],'actual_factual_checkpoint_accepted':True,'history_own_marker':{'unchanged':True}}
  def q(status,effort):
   c=['',' 5000005 / synthetic own ',' c2 ',' c3 ',' c4 ',' c5 ',' c6 ',' c7 ',' '+status+' ',' '+effort+' ',' original own link ',' old own note ',' old own doi ',''];return 'Own queue header\n'+'|'.join(c)+'\nOwn unrelated queue line.\n'
  base=q('unsolved','0/5').encode();original=q('claimed_solved','2/5').encode();queue='unsolved_math_prioritization/QUEUE.md'
  self.h.commit({queue:base},name=m.ORIGINAL_BASE);self.h.commit({queue:original},[m.ORIGINAL_BASE],name=m.HEAD)
  files={queue:base,m.PREFIX+'CURRENT_PROGRESS.json':enc(programme),m.PREFIX+'CURRENT_PROGRESS.md':b'Own programme prose history.\n',m.PREFIX+'RESEARCH_LOG.md':b'Own programme log history.\n','synthetic_unrelated/keep.txt':b'Own unchanged unrelated bytes\n'}
  self.h.main=self.h.commit(files,[m.ORIGINAL_BASE]);self.programme_before=programme;self.queue_base=base
 def raw_receipt(self):
  m=self.m;g=self.g;files=[{'name':g['paper_files'][k],'size':g['payloads'][g['paper_files'][k]]['bytes'],'sha256':g['payloads'][g['paper_files'][k]]['sha256'],'own_raw_extra':CANARY} for k in ['pdf','source','support']]
  j={'environment':'production','files':files,'own_raw_extra':CANARY}
  if self.service['state']!='absent':j.update(id=self.service['id'],state=self.service['state'],metadata_normalizations=[{'field':'description','kind':'plain_text_html_entities','own_raw_extra':CANARY},{'field':'creators','kind':'omitted_creator_affiliation_to_null','own_raw_extra':CANARY}])
  if self.service['state']=='published':j.update(doi='10.5281/zenodo.7000191',doi_url='https://doi.org/10.5281/zenodo.7000191',record_url='https://zenodo.org/records/7000191',receipt_saved=True,verified_utc=self.clock(),doi_resolution={'status':'resolved','own_raw_extra':CANARY})
  return j
 def runner(self,args,**kwargs):
  cmd=args[6];self.service['runner_calls'].append(cmd)
  if cmd=='stage' and self.service['state']=='absent':self.service['state']='ready_to_publish';self.service['stage_creations']+=1
  if cmd=='publish':self.service['state']='published';self.service['publish_writes']+=1
  if cmd=='inspect' and self.service['state']=='absent':return SimpleNamespace(returncode=1,stdout=enc({'synthetic_no_existing_record':True}),stderr=b'Synthetic inspect reports no existing record')
  j=self.raw_receipt()
  if cmd=='check':j={k:v for k,v in j.items() if k in ['environment','files','own_raw_extra']}
  fault=self.service['fault']
  if fault and fault[0]==cmd:
   self.service['fault']=None
   if fault[1]=='absent':
    if cmd=='stage':self.service['state']='absent';self.service['stage_creations']-=1
    if cmd=='publish':self.service['state']='ready_to_publish';self.service['publish_writes']-=1
   return SimpleNamespace(returncode=1,stdout=enc({'synthetic_unknown':True}),stderr=b'Synthetic own lost response')
  return SimpleNamespace(returncode=0,stdout=enc(j),stderr=b'')
 def sheet(self,resource,method,params,body=None):
  m=self.m;s=self.service;s['sheet_calls'].append((resource,method,params['spreadsheetId'],params.get('range')))
  if resource=='spreadsheet':return {'spreadsheetId':m.SID,'sheets':[{'properties':{'sheetId':m.GID,'title':m.TAB}}],'own_raw_extra':CANARY}
  rng=params['range']
  if method=='append':
   s['append_writes']+=1;s['rows'].extend(copy.deepcopy(body['values']));i=len(s['rows']);r={'updates':{'updatedRange':"'Math Puzzles'!A%d:D%d"%(i,i),'updatedRows':1,'updatedColumns':4,'own_raw_extra':CANARY},'own_raw_extra':CANARY}
   if s['fault'] and s['fault'][0]=='append':
    fault=s['fault'];s['fault']=None
    if fault[1]=='absent':s['rows'].pop();s['append_writes']-=1
    raise RuntimeError('Synthetic own unknown append outcome')
   return r
  if rng=="'Math Puzzles'!A1:D1":return {'values':[copy.deepcopy(m.HEADER)],'own_raw_extra':CANARY}
  if rng=="'Math Puzzles'!A:D":return {'values':copy.deepcopy(s['rows']),'own_raw_extra':CANARY}
  import re
  i=int(re.search(r'!A([0-9]+)',rng)[1]);return {'values':copy.deepcopy(s['rows'][i-1:i]),'own_raw_extra':CANARY}
 def services_ready(self):
  m=self.m;m.gate();m.run_zenodo('check');m.run_zenodo('stage');m.run_zenodo('inspect');m.run_zenodo('publish',self.service['id']);m.run_zenodo('inspect-published');m.record_tracker(self.sheet)
 def merge_ready(self):
  m=self.m;self.services_ready();m.prepare_native(False);req=m.metadata_request();put(self.path/'PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':m.HEAD,'gate_sha256':req['gate_sha256'],'request_sha256':self.pathpin('PR_METADATA_REQUEST.json')['sha256']})
  self.h.pr.update(title=req['request']['title'],body=req['request']['body']);m.final_scope();r=m.integration_prepare('merge_preparation_own');self.merge=r;self.h.main=r['commit'];self.h.pr.update(state='closed',merged=True);m.integration_accept();return r
 def full_flow(self,retry=True):
  m=self.m;self.merge_ready();r=m.factual_prepare('factual_preparation_first');cur=(self.path/'integration_preparation/CURRENT_TEMPLATE.json').read_bytes();native={n:(self.path/'integration_preparation/native_template_complete_own'/n).read_bytes() for n in self.native_pending}
  if retry:
   self.h.advance_foreign();r=m.factual_prepare('factual_preparation_fresh_parent')
   assert (self.path/'integration_preparation/CURRENT_TEMPLATE.json').read_bytes()==cur
   assert all((self.path/'integration_preparation/native_template_complete_own'/n).read_bytes()==b for n,b in native.items())
  self.h.main=r['commit'];self.factual=r;accept=m.factual_accept()
  assert accept['fully_completed_count']==40 and accept['published_count']==24 and accept['next_numeric_intake_cursor_authorized_after_this_acceptance']==192
  case=get(self.path/'CURRENT_CASE_STATUS.json');prog=json.loads(self.h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',r['commit']))
  assert all(case[k]==self.baseline[k] for k in m.CASE_PROTECTED_KEYS)
  assert case['historical_case_baseline_PR191']['values']==self.baseline
  for j in [case,prog]:assert j['actual_factual_checkpoint_accepted'] is False and j['advance_to_next_PR_authorized_now'] is False and j['next_numeric_intake_cursor']==191
  assert prog['history_own_marker']==self.programme_before['history_own_marker']
  for n,b in self.native_pending.items():
   if n.startswith('ORIGINAL_SUBMISSION/') or n not in m.JSON_FACTS|m.TEXT_FACTS|{'RESEARCH_LOG.md'}:assert native[n]==b
   if n in m.JSON_FACTS:assert json.loads(native[n])['scientific_unchanged']==json.loads(b)['scientific_unchanged']
  assert self.service['stage_creations']==1 and self.service['publish_writes']==1 and self.service['append_writes']==1
  assert len(m.inventory(self.path/'integration_preparation/native_template_complete_own'))==50
  assert m.CASE+'lifecycle_private/TRACKER_FOREIGN_BASELINE.json' not in r['selected_files']
  assert all(CANARY.encode() not in self.h.body_at(n,r['commit']) for n in r['selected_files'])
  return accept

# Every mutation is restored; trusted synthetic historical authorities stay fixed.
def local_case(w,name,file,edit,validator,relink=None,expected='REJECT',family='field-validation'):
 touched={p:p.read_bytes() for p in w.path.rglob('*') if p.is_file()}
 try:
  j=get(w.path/file);edit(j);put(w.path/file,j)
  if relink:relink()
  return outcome(name,validator,expected,family)
 finally:
  for p,b in touched.items():
   if not p.exists() or p.read_bytes()!=b:put(p,b)
  for p in list(w.path.rglob('*')):
   if p.is_file() and p not in touched:p.unlink()

def dict_nodes(x,path=()):
 if isinstance(x,dict):
  yield path
  for k,v in x.items():yield from dict_nodes(v,path+(k,))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from dict_nodes(v,path+(i,))
def at(x,path):
 for k in path:x=x[k]
 return x

def field_suite(w):
 m=w.m;g=w.g;z=get(w.path/'ZENODO_PUBLICATION_READBACK.json');tr=get(w.path/'TRACKER_ACCEPTANCE.json')
 def relink_tracker():
  j=get(w.path/'TRACKER_ACCEPTANCE.json')
  for n in j['evidence']:j['evidence'][n]=w.binding('sheets_tracking/'+n)
  put(w.path/'TRACKER_ACCEPTANCE.json',j)
 def relink_pub():
  e=get(w.path/'ZENODO_PUBLICATION_EVIDENCE.json');e['receipt']=w.binding('ZENODO_PUBLICATION_READBACK.json');e['published_output']=get(w.path/'ZENODO_PUBLICATION_READBACK.json');put(w.path/'ZENODO_PUBLICATION_EVIDENCE.json',e)
 records={
 'ZENODO_LOCAL_CHECK.json':lambda:m.publication(g),'ZENODO_STAGE_READBACK.json':lambda:m.publication(g),'ZENODO_DRAFT_READBACK.json':lambda:m.publication(g),'ZENODO_PUBLICATION_READBACK.json':lambda:m.publication(g),'ZENODO_POSTPUBLICATION_INSPECTION.json':lambda:m.publication(g),'ZENODO_PUBLICATION_EVIDENCE.json':lambda:m.publication(g),
 'TRACKER_ACCEPTANCE.json':lambda:m.validate_tracker(g,z,get(w.path/'TRACKER_ACCEPTANCE.json')),
 'PR_METADATA_REQUEST.json':lambda:m.validate_metadata_documents(g,z,tr),'PR_METADATA_ACCEPTANCE.json':lambda:m.validate_metadata_documents(g,z,tr),
 'FINAL_MAIN_SCOPE.json':lambda:m.validate_scope_schema(get(w.path/'FINAL_MAIN_SCOPE.json'),g),
 'SCOPED_MERGE_PREPARATION.json':lambda:m.verify_prepared(w.h,get(w.path/'SCOPED_MERGE_PREPARATION.json'),[w.merge['expected_main'],m.HEAD]),
 'FINAL_FACTUAL_PREPARATION.json':lambda:m.verify_prepared(w.h,get(w.path/'FINAL_FACTUAL_PREPARATION.json'),[w.factual['expected_main']]),
 'ROOT_ACTUAL_MERGE_ACCEPTANCE.json':lambda:m.verify_merge_scope(w.h,g,w.merge,True),
 'WORKFLOW_COMPLETION.json':lambda:m.validate_dynamic_control_shapes(g,z,tr),
 'integration_preparation/CURRENT_TEMPLATE.json':lambda:m.current_native(g,True,(z,tr)),
 }
 for n in ['TARGET_VALIDATION.json','ROW_READBACK_1.json','ROW_READBACK_2.json','POSTAPPEND_UNIQUENESS_1.json','POSTAPPEND_UNIQUENESS_2.json','APPEND_REQUEST.json','APPEND_RESPONSE.json','APPEND_ATTEMPT_STARTED.json']:records['sheets_tracking/'+n]=lambda:m.validate_tracker(g,z,get(w.path/'TRACKER_ACCEPTANCE.json'))
 for file,validator in records.items():
  original=get(w.path/file)
  for path in dict_nodes(original):
   def edit(j,p=path):at(j,p)['unexpected_own_field']={'synthetic_own':CANARY}
   local_case(w,'extra-field:'+file+':'+str(path),file,edit,validator,relink_tracker if file.startswith('sheets_tracking/') else relink_pub if file=='ZENODO_PUBLICATION_READBACK.json' else None)
 # Wrong approved scalar values and types, with evidence rebindings where needed.
 simple=[('ZENODO_PUBLICATION_READBACK.json','id',True),('ZENODO_PUBLICATION_READBACK.json','doi','10.5281/wrong_own'),('ZENODO_PUBLICATION_READBACK.json','verified_utc','2099-01-01T00:00:00+00:00'),('ZENODO_PUBLICATION_READBACK.json','receipt_saved',CANARY),('TRACKER_ACCEPTANCE.json','actual_fresh_reads',True),('TRACKER_ACCEPTANCE.json','row',[CANARY]),('PR_METADATA_ACCEPTANCE.json','request_sha256','f'*64),('FINAL_MAIN_SCOPE.json','native_files',49),('SCOPED_MERGE_PREPARATION.json','UTC','not a date'),('WORKFLOW_COMPLETION.json','case_percent',True)]
 for file,key,value in simple:local_case(w,'wrong-approved:'+file+':'+key,file,lambda j,k=key,v=value:j.__setitem__(k,v),records[file],relink_pub if file=='ZENODO_PUBLICATION_READBACK.json' else None)
 # This allowed key must also have its exact intended value and scalar type.
 for value,label in [('10.5281/wrong_own','wrong-DOI'),({'unexpected_own_field':CANARY},'nested-object-in-DOI')]:local_case(w,'merge-acceptance:'+label,'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',lambda j,v=value:j.__setitem__('DOI',v),records['ROOT_ACTUAL_MERGE_ACCEPTANCE.json'],family='merge-current-record')
 local_case(w,'merge-acceptance:wrong-selected-count','ROOT_ACTUAL_MERGE_ACCEPTANCE.json',lambda j:j.__setitem__('selected_files',999999),records['ROOT_ACTUAL_MERGE_ACCEPTANCE.json'],family='merge-current-record')


def recovery_suite():
 for action in ['stage','publish']:
  for durable in ['durable','absent']:
   w=World('unknown_'+action+'_'+durable);m=w.m;m.run_zenodo('check')
   if action=='publish':m.run_zenodo('stage')
   w.service['fault']=(action,durable)
   outcome('unknown-'+action+'-'+durable+':first',lambda:m.run_zenodo(action,w.service['id'] if action=='publish' else None),family='unknown-write')
   expected='ACCEPT' if durable=='durable' else 'REJECT'
   outcome('unknown-'+action+'-'+durable+':retry',lambda:m.run_zenodo(action,w.service['id'] if action=='publish' else None),expected,'unknown-write')
   assert w.service['stage_creations']<=1 and w.service['publish_writes']<=1
 for durable in ['durable','absent']:
  w=World('unknown_append_'+durable);m=w.m
  for a in ['check','stage','inspect']:m.run_zenodo(a)
  m.run_zenodo('publish',w.service['id']);w.service['fault']=('append',durable)
  outcome('unknown-append-'+durable+':first',lambda:m.record_tracker(w.sheet),family='unknown-write')
  outcome('unknown-append-'+durable+':retry',lambda:m.record_tracker(w.sheet),'ACCEPT' if durable=='durable' else 'REJECT','unknown-write')
  assert w.service['append_writes']<=1


def freshness_suite(w):
 m=w.m
 old=copy.deepcopy(w.service)
 try:
  w.service['rows'].append(copy.deepcopy(w.service['rows'][1]));outcome('fresh-duplicate-DOI',m.published_tracked,family='fresh-consumer')
  w.service=copy.deepcopy(old);w.service['rows'][1][3]='Changed own note';outcome('fresh-own-row-changed',m.published_tracked,family='fresh-consumer')
  w.service=copy.deepcopy(old);w.service['id']+=1;outcome('fresh-publication-id-changed',m.published_tracked,family='fresh-consumer')
 finally:w.service=old
 # Allowed unrelated addition after all owned rows; no foreign private data involved.
 w.service['rows'].append(['Own synthetic unrelated addition','','','Own fixture'])
 outcome('fresh-unrelated-addition-permitted',m.published_tracked,'ACCEPT','fresh-consumer')
 w.service=old


def coherent_case_suite():
 # Actual prepared-commit bodies and all selected hashes/messages change together.
 for kind in ['case-alias','programme-alias','programme-time','case-log','queue-foreign','native-science','true-parent-tree','full-tree-extra','scope-omission']:
  w=World('coherent_'+kind);w.merge_ready();m=w.m;r=copy.deepcopy(w.merge);h=w.h;files=h.files(r['commit'])
  if kind=='case-alias':
   n=m.CASE+'CURRENT_CASE_STATUS.json';j=json.loads(files[n]);j['advance_to_next_PR_authorized_now']=True;files[n]=enc(j)
  elif kind=='programme-alias':
   n=m.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(files[n]);j['extra_current_completion_authority']=True;files[n]=enc(j)
  elif kind=='programme-time':
   n=m.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(files[n]);j['updated_UTC']='2099-01-01T00:00:00+00:00';files[n]=enc(j)
  elif kind=='case-log':n=m.CASE+'RESEARCH_LOG.md';files[n]+=b'Own unsupported current intake192 claim.\n'
  elif kind=='queue-foreign':n='unsolved_math_prioritization/QUEUE.md';files[n]=files[n].replace(b'Own unrelated queue line.',b'Altered unrelated own fixture line.')
  elif kind=='native-science':
   n=m.NATIVE+'CURRENT_RESULT.json';j=json.loads(files[n]);j['scientific_unchanged']['marker']='WRONG_OWN_SCIENCE';files[n]=enc(j)
  elif kind=='true-parent-tree':r['parent_tree']='0'*40
  elif kind=='full-tree-extra':files['synthetic_unrelated/hidden_edit.txt']=b'Unexpected unrelated own fixture edit'
  elif kind=='scope-omission':
   n=m.CASE+'FINAL_MAIN_SCOPE.json';j=json.loads(files[n]);j['selected_MAIN_paths'].remove(m.CASE+'CURRENT_PROOF.md');files[n]=enc(j);put(w.path/'FINAL_MAIN_SCOPE.json',j)
  if kind!='true-parent-tree':
   for n in r['selected_files']:r['selected_files'][n]=bp(files[n])
   r['selected_map_sha256']=hashlib.sha256(json.dumps(r['selected_files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
   r['tree']=h.tree(files);r['commit']=h.commit(files,[r['expected_main'],m.HEAD],m.operative_message(get(w.path/'ZENODO_PUBLICATION_READBACK.json'),[r['expected_main'],m.HEAD],r['selected_map_sha256']))
   parent_tree=h.commits[r['expected_main']]['tree']['sha'];r['changed_paths']=sorted(n for n,x in r['selected_files'].items() if h.lookup(parent_tree,n)!=('100644','blob',x['git_blob']))
  put(w.path/'SCOPED_MERGE_PREPARATION.json',r);h.main=r['commit']
  outcome('coherent-'+kind,m.integration_accept,family='coherent-postimage')


def end_to_end_merge_record_case():
 # Separate actual late-consumer reproductions: no combined-mutation ambiguity.
 for label,value,count in [('wrong-scalar-DOI','10.5281/wrong_own',None),('nested-DOI',{'unexpected_own_field':CANARY},None),('wrong-selected-count',None,999999)]:
  w=World('merge_receipt_end_to_end_'+label);w.merge_ready();m=w.m
  a=get(w.path/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')
  if value is not None:a['DOI']=value
  if count is not None:a['selected_files']=count
  put(w.path/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',a)
  def consume():
   r=m.factual_prepare('factual_preparation_current_record');w.h.main=r['commit'];m.factual_accept()
   published=json.loads(w.h.body_at(m.CASE+'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',r['commit']))
   assert published['DOI']==a['DOI'] and published['selected_files']==a['selected_files']
  outcome('actual-factual-consumers:'+label+'-reaches-selected-output',consume,family='required-repair-reproduction')


def main():
 assert sys.dont_write_bytecode,'Invoke this independent harness with -B'
 w=World('positive_complete_flow')
 outcome('full-positive-workflow-plus-unchanged-native100-fresh-parent-retry',lambda:w.full_flow(True),'ACCEPT','positive-complete-workflow')
 if not RESULTS[-1]['met_expectation']:
  put(HERE/'results_07.json',{'schema':'independent-terminal07-results-v1','source_sha256':SOURCE_SHA,'results':RESULTS});print(json.dumps(RESULTS[-1]));return
 field_suite(w);freshness_suite(w);recovery_suite();coherent_case_suite();end_to_end_merge_record_case()
 summary={'cases':len(RESULTS),'met_expectation':sum(x['met_expectation'] for x in RESULTS),'unexpected_acceptances':[x['case'] for x in RESULTS if not x['met_expectation'] and x['observed']=='ACCEPT'],'unexpected_rejections':[x['case'] for x in RESULTS if not x['met_expectation'] and x['observed']=='REJECT']}
 put(HERE/'results_07.json',{'schema':'independent-terminal07-results-v1','source_sha256':SOURCE_SHA,'synthetic_own_only':True,'production_calls':0,'git_commands':0,'handoff_executed':False,'prior_author_harness_or_results_read':False,'summary':summary,'results':RESULTS})
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

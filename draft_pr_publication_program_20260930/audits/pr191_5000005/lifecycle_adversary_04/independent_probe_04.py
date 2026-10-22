"""Independent frozen04 probes. Offline objects/services only; no production helpers.
Fixture mechanisms were sealed in independent_fixtures_preinspection_04.py before
reading the implementation, and are adapted here to its frozen public interface.
"""
import ast, copy, datetime, hashlib, importlib.util, json, os, pathlib, shutil, sys, types
from independent_fixtures_preinspection_04 import commit as native_commit, flat_tree, blob, PRIVATE_SENTINEL
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=HERE.parent/'lifecycle_controls_preparation_04'
NOW='2026-10-15T05:00:00+00:00'
OLD='2026-10-14T05:00:00+00:00'
FUTURE='2026-10-16T05:00:00+00:00'
RESULTS=[]
def enc(x): return (json.dumps(x,indent=2)+'\n').encode()
def bp(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def p2(b): return {k:v for k,v in bp(b).items() if k!='git_blob'}
def check(name,fn,expect='accept'):
 try:
  detail=fn()
  passed=expect=='accept'
  RESULTS.append({'name':name,'expected':expect,'observed':'accept','passed':passed,'detail':detail})
 except Exception as e:
  RESULTS.append({'name':name,'expected':expect,'observed':'reject','passed':expect=='reject','exception':type(e).__name__,'reason':str(e)})
def reject(name,fn): check(name,fn,'reject')

class NativeAPI:
 def __init__(self,m):
  self.mdl=m;self.commits={};self.trees={};self.blobs={};self.calls=[]
  self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *x:None)))
  self.pr={'head':{'sha':m.HEAD},'state':'open','merged':False,'draft':True,'title':'','body':''}
  self.main=self.seed({'unrelated/foreign.txt':b'preserve foreign bytes\n'},[],'true parent')
 def seed(self,files,parents,message):
  c=native_commit(files,parents,message);self.commits[c['oid']]=c;self.trees[c['tree']['oid']]=copy.deepcopy(files)
  for b in files.values():self.blobs[bp(b)['git_blob']]=b
  return c['oid']
 def api(self,path,method='GET',body=None):
  self.calls.append((path,method))
  if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
  if path=='pulls/191':return copy.deepcopy(self.pr)
  if path.startswith('git/commits/'):
   c=self.commits[path.split('/')[-1]];return {'tree':{'sha':c['tree']['oid']},'parents':[{'sha':p} for p in c['parents']],'message':c['message']}
  if path=='git/blobs' and method=='POST':
   import base64
   b=base64.b64decode(body['content']);oid=bp(b)['git_blob'];self.blobs[oid]=b;return {'sha':oid}
  if path=='git/trees' and method=='POST':
   files=copy.deepcopy(self.trees[body['base_tree']])
   for e in body['tree']:
    assert e['mode']=='100644' and e['type']=='blob'
    b=e['content'].encode() if 'content' in e else self.blobs[e['sha']]
    files[e['path']]=b;self.blobs[bp(b)['git_blob']]=b
   t=flat_tree(files);self.trees[t['oid']]=files;return {'sha':t['oid']}
  if path=='git/commits' and method=='POST':
   return {'sha':self.seed(self.trees[body['tree']],body['parents'],body['message'])}
  if path.startswith('compare/'):
   before,after=path[len('compare/'):].split('...')
   def ancestor(a,b,seen=None):
    if a==b:return True
    if b not in self.commits:return False
    return any(ancestor(a,p) for p in self.commits[b]['parents'])
   return {'status':'identical' if before==after else 'ahead' if ancestor(before,after) else 'diverged'}
  raise AssertionError('Unexpected synthetic API '+path+' '+method)
 def body_at(self,path,ref):return self.commits[ref]['files'][path]
 def lookup(self,tree,path):
  b=self.trees[tree].get(path)
  return None if b is None else ('100644','blob',bp(b)['git_blob'])
 def changed_leaves(self,a,b):
  x,y=self.trees[a],self.trees[b]
  return {k for k in set(x)|set(y) if x.get(k)!=y.get(k)}

class Tracker:
 def __init__(self,m):self.m=m;self.rows=[m.HEADER[:],[PRIVATE_SENTINEL,'foreign private value','','']];self.calls=[];self.append_calls=0;self.timeout=False;self.mutate=None
 def __call__(self,resource,method,params,body=None):
  self.calls.append((resource,method,copy.deepcopy(params),copy.deepcopy(body)))
  if params.get('spreadsheetId')!=self.m.SID:raise AssertionError('Wrong tracker target')
  if self.mutate:self.mutate(self,resource,method,params)
  if resource=='spreadsheet':return {'spreadsheetId':self.m.SID,'sheets':[{'properties':{'sheetId':self.m.GID,'title':self.m.TAB}}]}
  if method=='append':
   self.append_calls+=1
   assert params['valueInputOption']=='RAW' and params['insertDataOption']=='INSERT_ROWS' and body['majorDimension']=='ROWS' and len(body['values'])==1 and len(body['values'][0])==4
   self.rows.append(copy.deepcopy(body['values'][0]));i=len(self.rows)
   if self.timeout:raise TimeoutError('synthetic unknown append outcome')
   return {'updates':{'updatedRange':f"'Math Puzzles'!A{i}:D{i}",'updatedRows':1,'updatedColumns':4}}
  rng=params['range']
  if rng=="'Math Puzzles'!A1:D1":return {'values':[copy.deepcopy(self.rows[0])]}
  if rng=="'Math Puzzles'!A:D":return {'values':copy.deepcopy(self.rows)}
  import re
  q=re.fullmatch(r"'?Math Puzzles'?!A([0-9]+):D([0-9]+)",rng);assert q
  return {'values':[copy.deepcopy(self.rows[int(q[1])-1])]}

class Kit:
 def __init__(self,m,g):self.m=m;self.g=g;self.state='absent';self.calls=[];self.creations=0;self.publications=0;self.fail=None;self.tamper=None
 def result(self):
  g=self.g;m=self.m
  j={'environment':'production','id':9000005,'state':'published' if self.state=='published' else 'draft','doi':'10.5281/zenodo.9000005','doi_url':'https://doi.org/10.5281/zenodo.9000005','record_url':'https://zenodo.org/records/9000005','files':[{'name':g['paper_files'][k],'size':g['payloads'][g['paper_files'][k]]['bytes'],'sha256':g['payloads'][g['paper_files'][k]]['sha256']} for k in ['pdf','source','support']],'metadata_normalizations':[],'doi_resolution':{'status':'resolved'},'receipt_saved':False,'verified_utc':NOW}
  if self.tamper:self.tamper(j)
  return j
 def __call__(self,args,**kw):
  assert args[:5]==[self.m.PY,'-E','-S','-B','-P'] and args[5].endswith('/zenodo_deposit_tool/zenodo.py')
  command=args[6];self.calls.append((command,args[:]))
  if command=='stage':
   if self.state=='absent':self.creations+=1;self.state='draft'
  if command=='publish':
   assert '--check-doi' in args and args[args.index('--confirm-id')+1]=='9000005'
   assert self.state=='draft';self.state='published';self.publications+=1
  if self.fail==command:self.fail=None;raise TimeoutError('synthetic unknown '+command+' outcome')
  return types.SimpleNamespace(stdout=json.dumps(self.result()).encode(),stderr=b'',returncode=0)

class Fixture:
 def __init__(self,name):
  self.root=HERE/'work'/name
  if self.root.exists():shutil.rmtree(self.root)
  self.root.mkdir(parents=True)
  spec=importlib.util.spec_from_file_location('pr191_independent04_'+name,SOURCE/'lifecycle_common.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
  m=self.m;m.A=self.root;m.now=lambda:NOW
  self.h=NativeAPI(m);m._helpers=self.h
  def put(n,b):
   p=self.root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b if isinstance(b,bytes) else enc(b));return p2(p.read_bytes())
  self.put=put
  def binding(n):return {'path':n,**p2((self.root/n).read_bytes())}
  self.binding=binding
  for n in m.CONTROL_FILES:put(n,(SOURCE/n).read_bytes())
  proof=b'Qualified proof: literal conjunction false n>=5; K_PS law/existence n>=3. Ferudun exact theorem/mechanisms credited. No novelty/firstness/independence/current-openness certification. Extensive AI; unrefereed.\n'
  put('CURRENT_PROOF_V4.md',proof)
  native={}
  for i in range(16):native[f'ORIGINAL_SUBMISSION/o{i:02}.txt']=f'original artifact {i}\n'.encode()
  native['CANDIDATE.md']=proof;native['PROOF_V4.md']=proof
  for n in sorted(m.JSON_FACTS):
   native[n]=enc({'UTC':OLD,'scientific_claim':'parity-selected all n>=3; bare conjunction false all n>=5','priority_clearance':False,'extensive_AI':True,'Ferudun_exact_theorem_credited':True,'historical_effort':'2/5','whole_package_reviews_complete':False,'publication_ready':False,'actual_Zenodo_published':False,'actual_published':False,'actual_DOI':None,'actual_tracker_updated':False,'actual_tracker_range':None,'actual_original_PR_merged':False,'case_percent':90,'snapshot_semantics':'pending','whole_package_reviews_pending':True,'successive_NEW_whole_package_reviews_complete':False,'publication_clearance':False,'publication_and_tracker_actions_not_yet_performed':True,'not_an_approval':True,'completed_new_whole_package_reviews':0})
  self.needles={'README.md':'PUBLICATION.json contains dated assembly-time publication facts, pending until actual publication and repository acceptance.','review/REVIEW.md':'Those are pending at this dated assembly snapshot.'}
  for n,t in self.needles.items():native[n]=('Scientific/priority/AI history fixed. '+t+'\n').encode()
  native['RESEARCH_LOG.md']=b'Prior dated history fixed.\n'
  for i in range(21):native[f'support/s{i:02}.txt']=f'approved support {i}\n'.encode()
  assert len(native)==50;self.native=copy.deepcopy(native)
  for n,b in native.items():put('integration_preparation/native_template_pending_test/'+n,b)
  put('PENDING_MANIFEST.json',{'current_template':'native_template_pending_test','files':{n:p2(b) for n,b in native.items()}})
  put('ORIGINAL_FILE_MANIFEST.json',{'original_head':m.HEAD,'files':[{'path':m.NATIVE+f'o{i:02}.txt',**p2(native[f'ORIGINAL_SUBMISSION/o{i:02}.txt'])} for i in range(16)]})
  roles={'pdf':'paper.pdf','source':'paper.tex','support':'support.zip','metadata':'deposit.json'}
  payloads={'paper.pdf':b'%PDF-independent approved fixture\n','paper.tex':proof,'support.zip':b'PK independent approved fixture\n','deposit.json':enc({'files':[{'path':roles[k],'name':roles[k]} for k in ['pdf','source','support']],'metadata':{'title':'credited note','description':'qualified proof extensive AI'}})}
  for n,b in payloads.items():put('package_test/'+n,b)
  put('INPUT.json',{'complete_package':'independent fixture only','proof_sha256':p2(proof)['sha256']})
  put('PR_PROPOSAL.json',{'title':'Credited K_PS note and literal counterexamples','body_before_publication':proof.decode()})
  put('TRACKER_PROPOSAL.json',{'original_problem':'original problem 5000005','solution_chat_url':'','notes':'Credited note; original effort2/5 retained.'})
  reviews=[]
  for i in [1,2]:
   for role in ['report','seal','root_authentication']:put(f'science{i}/{role}.json',{'synthetic':True,'role':role,'reviewer':i,'qualified_claims':proof.decode()})
   reviews.append({'reviewer_id':f'fresh-independent-science-{i}','authoritative':True,'disposition':'PASS',**{role:binding(f'science{i}/{role}.json') for role in ['report','seal','root_authentication']}})
  for role in ['report','seal','root_authentication']:put(f'operations04/{role}.json',{'synthetic':True,'role':role,'status':'PASS'})
  case={k:'trusted Root scientific value '+k for k in sorted(m.CASE_PROTECTED_KEYS)}
  case.update(PR=191,problem_id=5000005,original_head=m.HEAD,original_QUEUE_status='claimed_solved',original_effort='2/5',mathematical_clearance=True,priority_clearance=False,goal_complete=False,bounded_priority_audit_complete=True,current_primary_overlap_verified=True,novelty_clearance=False,qualified_credited_note_route_authorized=True,current_proof='CURRENT_PROOF_V4.md',current_proof_SHA256=p2(proof)['sha256'],scientific_package_ready=True,UTC=OLD,status='ready pending actual actions',case_percent=90,root_dated_history='Root-authored qualified status history',operational_lifecycle_audit_active=True,operational_required_repairs=['historical review'])
  put('CURRENT_CASE_STATUS.json',case);put('ROOT_CASE_SCIENTIFIC_PROJECTION.json',m.case_scientific_projection(case));put('RESEARCH_LOG.md',b'Root prior dated factual history.\n')
  put('ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json',{'status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','PR':191,'original_head':m.HEAD,'UTC':OLD,'all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':{n:p2((self.root/n).read_bytes()) for n in m.CONTROL_FILES},'independent_adversary_review':{'disposition':'PASS',**{role:binding(f'operations04/{role}.json') for role in ['report','seal','root_authentication']}}})
  for kind in ['control','support','case-proof','review','gate']:put('protected/'+kind+'.txt',('approved immutable '+kind+'\n').encode())
  put('INTAKE_CHECKPOINT_ACCEPTANCE.json',{'PR':191,'original_head':m.HEAD,'checkpoint_commit':'1'*40})
  put('ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json',{'PR':191,'original_head':m.HEAD,'proof_parent':m.ORIGINAL_BASE})
  g={'schema':'PR191_LIFECYCLE_GATE_V1','status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':191,'original_head':m.HEAD,'qualified_note_route_authorized':True,'historical_priority_clearance':False,'all_required_findings_globally_resolved':True,'last_review_required_repairs':0,'whole_package_reviews':reviews,'package_name':'package_test','payloads':{n:p2(b) for n,b in payloads.items()},'paper_files':roles,'current_proof':binding('CURRENT_PROOF_V4.md'),'native_proof_paths':['CANDIDATE.md','PROOF_V4.md'],'native_pending_template':'native_template_pending_test','native_pending_manifest':binding('PENDING_MANIFEST.json'),'native_final_template':'native_template_final_test','native_complete_template':'native_template_complete_test','native_json_status_paths':sorted(m.JSON_FACTS),'native_text_status_replacements':self.needles,'pr_metadata_proposal':binding('PR_PROPOSAL.json'),'tracker_row_proposal':binding('TRACKER_PROPOSAL.json'),'review_input':binding('INPUT.json')}
  immutable=['ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json','ROOT_CASE_SCIENTIFIC_PROJECTION.json']+[f'protected/{k}.txt' for k in ['control','support','case-proof','review','gate']]
  g['public_case_pins']={n:p2((self.root/n).read_bytes()) for n in immutable};g['public_case_paths']=immutable+['CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json']
  self.put('ROOT_PUBLICATION_GATE.json',g);self.g=g;self.kit=Kit(m,g);self.tracker=Tracker(m)
  m._runtime={'runner':self.kit,'inspect':lambda g:m.observe_publication(g,self.kit),'tracker':self.tracker}
  self.base_program={'current_PR':191,'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'fully_completed_eligible_PRs':list(range(1,40)),'published_PRs':list(range(1,24)),'dated_eligible_total':99,'current_operational_lifecycle_audit_active':True,'current_operational_required_repairs':['historical negative review']}
  own='| 5000005 / original | a | b | c | d | e | f | claimed_solved | 2/5 | old PR | old note | old DOI |'
  self.queue='QUEUE header\n| foreign / row | keep | cells | exactly |\n'+own+'\n'
  # Original HEAD and proof parent are represented as fixed in-memory identities only.
  for identity in [m.HEAD,m.ORIGINAL_BASE]:
   seed=self.h.seed({'unsolved_math_prioritization/QUEUE.md':self.queue.encode()},[],'original snapshot');self.h.commits[identity]=self.h.commits[seed]
  files={m.PREFIX+'CURRENT_PROGRESS.json':enc(self.base_program),m.PREFIX+'CURRENT_PROGRESS.md':b'Programme dated prior status.\n',m.PREFIX+'RESEARCH_LOG.md':b'Programme dated prior log.\n','unsolved_math_prioritization/QUEUE.md':self.queue.encode(),'unrelated/foreign.txt':b'preserve foreign bytes\n'}
  self.h.main=self.h.seed(files,[],'actual main fixture')
 def publish(self):
  m=self.m;m.run_zenodo('check',runner=self.kit);m.run_zenodo('stage',runner=self.kit);m.run_zenodo('inspect',runner=self.kit);m.run_zenodo('publish',9000005,runner=self.kit);m.run_zenodo('inspect-published',runner=self.kit);return m.publication()
 def track(self):return self.m.record_tracker(self.tracker)
 def native95(self):return self.m.prepare_native(False)
 def ready(self):
  m=self.m;r=m.metadata_request();self.h.pr.update(title=r['request']['title'],body=r['request']['body'],draft=False)
  self.put('PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':m.HEAD,'gate_sha256':r['gate_sha256'],'request_sha256':p2((self.root/'PR_METADATA_REQUEST.json').read_bytes())['sha256']})
 def prep95(self):
  self.publish();self.track();self.native95();self.ready();self.m.final_scope();return self.m.integration_prepare('merge_preparation_independent04')
 def adopt95(self):
  r=self.prep95();self.h.main=r['commit'];self.h.pr.update(merged=True,state='closed');return self.m.integration_accept()
 def prep100(self):self.adopt95();return self.m.factual_prepare('factual_preparation_independent04')
 def adopt100(self):r=self.prep100();self.h.main=r['commit'];return self.m.factual_accept()
 def reforge(self,r,changes,message=None,parents=None):
  m=self.m;files=copy.deepcopy(self.h.commits[r['commit']]['files']);files.update(changes);selected=copy.deepcopy(r['selected_files'])
  for n,b in changes.items():
   if n in selected:selected[n]=bp(b)
  digest=m.selected_digest(selected);parents=parents or self.h.commits[r['commit']]['parents']
  if message is None:message=m.operative_message(self.kit.result(),parents,digest)
  c=self.h.seed(files,parents,message);out=copy.deepcopy(r);out.update(commit=c,tree=self.h.commits[c]['tree']['oid'],selected_files=selected,selected_map_sha256=digest,changed_paths=sorted(self.h.changed_leaves(r['parent_tree'],self.h.commits[c]['tree']['oid'])))
  return out

# Fixed-input check and import-time effects. No author harness/results are used.
def source_pins():
 expected={'lifecycle_common.py':'82c40f48f9aabc6780a13b36db895d8ba437aa7817c17f14430444fd27ed8b78','FINAL_SEAL.json':'3c9f2386caabaeb53fcacdce97625386c64b67866d9b958be29264a372b3605b','GATE_CONTRACT.md':'7d89a96c09ccd88515132b57074d8f9f3ddfc229daf9a9ea68552f5740e046dd'}
 assert all(hashlib.sha256((SOURCE/n).read_bytes()).hexdigest()==v for n,v in expected.items())
 s=json.loads((SOURCE/'FINAL_SEAL.json').read_text());a=json.loads((SOURCE/'PROPOSED_FILE_ALLOWLIST.json').read_text())
 assert set(a['files'])=={x['path'] for x in s['manifest']}|{'FINAL_SEAL.json'} and len(a['files'])==18
 for x in s['manifest']:assert p2((SOURCE/x['path']).read_bytes())=={'bytes':x['bytes'],'sha256':x['sha256']} and ((SOURCE/x['path']).stat().st_mode&0o777)==0o444
 return {'frozen_files':18,'hashes_sizes_modes':'exact'}
def import_inert():
 # Compile source first; trap operational APIs only during module execution.
 import socket,subprocess,builtins
 code=compile((SOURCE/'lifecycle_common.py').read_bytes(),str(SOURCE/'lifecycle_common.py'),'exec');oldopen=builtins.open;oldrun=subprocess.run;oldconnect=socket.socket.connect
 def forbidden(*a,**k):raise AssertionError('Import-time external effect')
 builtins.open=forbidden;subprocess.run=forbidden;socket.socket.connect=forbidden
 try:
  ns={'__file__':str(SOURCE/'lifecycle_common.py'),'__name__':'independent_import_only'};exec(code,ns)
  assert ns['_runtime'] is None and ns['_helpers'] is None
 finally:builtins.open=oldopen;subprocess.run=oldrun;socket.socket.connect=oldconnect
 return 'No open, subprocess.run, socket connect, helper load, or authority creation.'

check('frozen_source_identity_and_modes',source_pins)
check('inert_import_with_effect_traps',import_inert)
f=Fixture('baseline')
check('full_real_gate_consumer_synthetic_authority',lambda: {'PR':f.m.gate()['PR'],'native_count':len(f.native)})
# Gate mutations do not issue changed authority; they test exact enforcement with synthetic Root inputs.
for label,mut in [('duplicate_science_reviewer',lambda g:g['whole_package_reviews'][1].update(reviewer_id=g['whole_package_reviews'][0]['reviewer_id'])),('missing_operational_pin',lambda g:g['public_case_pins'].pop('ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json')),('missing_case_projection',lambda g:g['public_case_pins'].pop('ROOT_CASE_SCIENTIFIC_PROJECTION.json')),('latest_review_negative',lambda g:g['whole_package_reviews'][-1].update(disposition='REPAIR_REQUIRED')),('wrong_original_head',lambda g:g.update(original_head='f'*40)),('wrong_json_alias_set',lambda g:g.update(native_json_status_paths=[]))]:
 def attack(mut=mut):
  g=copy.deepcopy(f.g);mut(g);f.put('ROOT_PUBLICATION_GATE.json',g)
  try:return f.m.gate()
  finally:f.put('ROOT_PUBLICATION_GATE.json',f.g)
 reject('gate_'+label,attack)
# Direct production actions need explicit runtime context; not tested against production.
f.m._runtime=None
reject('default_entrypoint_rejects_uninjected_services',lambda:f.m.publication())
f.m._runtime={'runner':f.kit,'inspect':lambda g:f.m.observe_publication(g,f.kit),'tracker':f.tracker}
check('exact_kit_stage_inspect_publish_consumption',lambda:{'state':f.publish()['state'],'creations':f.kit.creations,'publications':f.kit.publications})
for label,mut in [('sandbox',lambda j:j.update(environment='sandbox')),('wrong_record_id',lambda j:j.update(id=9000006)),('wrong_DOI_URL',lambda j:j.update(doi_url='https://doi.org/10.0000/wrong')),('wrong_file_bytes',lambda j:j['files'][0].update(sha256='f'*64)),('future_verified_utc',lambda j:j.update(verified_utc=FUTURE))]:
 def attack(mut=mut):
  f.kit.tamper=mut
  try:return f.m.publication()
  finally:f.kit.tamper=None
 reject('publication_fresh_'+label,attack)
check('one_RAW_append_two_own_and_full_reads',lambda:{'status':f.track()['status'],'append_count':f.tracker.append_calls})
check('later_tracker_consumer_reobserves_both_own_full',lambda:{'PR':f.m.published_tracked()[0]['PR'],'tracker_calls':len(f.tracker.calls)})
for label,mut in [('foreign_row_changed',lambda t:t.rows[1].__setitem__(1,'mutated foreign')),('duplicate_own_DOI',lambda t:t.rows.append(copy.deepcopy(t.rows[-1]))),('header_drift',lambda t:t.rows[0].__setitem__(0,'wrong')),('own_cell_drift',lambda t:t.rows[-1].__setitem__(3,'wrong'))]:
 def attack(mut=mut):
  old=copy.deepcopy(f.tracker.rows);mut(f.tracker)
  try:return f.m.published_tracked()
  finally:f.tracker.rows=old
 reject('tracker_later_'+label,attack)

def uncertain_publication():
 q=Fixture('unknown_publication');q.m.run_zenodo('stage',runner=q.kit);q.kit.fail='publish'
 try:q.m.run_zenodo('publish',9000005,runner=q.kit)
 except TimeoutError:pass
 else:raise AssertionError('Expected timeout')
 out=q.m.run_zenodo('publish',9000005,runner=q.kit)
 assert out['state']=='published' and q.kit.publications==1
 return {'write_count':q.kit.publications,'reconciled_from':'fresh inspect'}
check('unknown_publication_no_second_POST',uncertain_publication)
def uncertain_tracker():
 q=Fixture('unknown_tracker');q.publish();q.tracker.timeout=True
 try:q.track()
 except TimeoutError:pass
 else:raise AssertionError('Expected timeout')
 q.tracker.timeout=False;out=q.track();assert q.tracker.append_calls==1
 return {'append_count':q.tracker.append_calls,'status':out['status']}
check('unknown_tracker_no_second_append',uncertain_tracker)
# Native and factual baseline, followed by independently predicted preservation attacks.
check('native95_full_generation',lambda:{'files':len(f.native95()['files'])})
for n in ['CANDIDATE.md','support/s00.txt','ORIGINAL_SUBMISSION/o00.txt','CURRENT_RESULT.json','README.md','RESEARCH_LOG.md']:
 def attack(n=n):
  root=f.root/'integration_preparation/native_template_final_test';p=root/n;old=p.read_bytes();cur=f.m.read(f.root/'integration_preparation/CURRENT_TEMPLATE.json');oldcur=copy.deepcopy(cur)
  changed=old+b'UNAPPROVED SCIENTIFIC OR HISTORICAL CHANGE\n';p.chmod(0o644);p.write_bytes(changed);cur['files'][n]=bp(changed);f.put('integration_preparation/CURRENT_TEMPLATE.json',cur);f.put('integration_preparation/native_template_final_test_MANIFEST.json',cur)
  try:return f.m.current_native(f.g,False)
  finally:p.write_bytes(old);p.chmod(0o444);f.put('integration_preparation/CURRENT_TEMPLATE.json',oldcur);f.put('integration_preparation/native_template_final_test_MANIFEST.json',oldcur)
 reject('native_rehashed_unapproved_'+n.replace('/','_'),attack)
# Complete path through actual acceptance entrypoints with synthetic object/service adapters.
q=Fixture('full_flow')
merge=None;factual=None
try:
 merge=q.prep95();check('native_two_parent_preparation_real_consumers',lambda:{'selected_count':len(merge['selected_files']),'parents':len(q.h.commits[merge['commit']]['parents'])})
 q.h.main=merge['commit'];q.h.pr.update(merged=True,state='closed')
 check('actual_entrypoint_merge_acceptance_fixture',lambda:{'status':q.m.integration_accept()['status']})
 factual=q.m.factual_prepare('factual_preparation_independent04');check('native_factual_preparation_real_consumers',lambda:{'selected_count':len(factual['selected_files'])})
 q.h.main=factual['commit'];check('actual_entrypoint_combined_factual_acceptance_fixture',lambda:{'status':q.m.factual_accept()['status']})
except Exception as e:RESULTS.append({'name':'full_flow_setup','expected':'accept','observed':'reject','passed':False,'exception':type(e).__name__,'reason':str(e)})
# Each new attack uses an intact independently created merge and coherent native objects.
r=Fixture('merge_attack');mr=r.prep95();r.h.pr.update(merged=True,state='closed')

def accept_merge_changes(changes,message=None,receipt_mut=None):
 rr=r.reforge(mr,changes,message);r.put('SCOPED_MERGE_PREPARATION.json',rr);r.h.main=rr['commit']
 if receipt_mut:receipt_mut(rr)
 return r.m.integration_accept()
# This is within a selected shared file, leaving all path-level, native, gate and programme checks valid.
wrong_queue=r.h.body_at('unsolved_math_prioritization/QUEUE.md',mr['commit']).replace(b'| foreign / row | keep | cells | exactly |',b'| foreign / row | ALTERED | cells | exactly |')
reject('coherent_refingerprinted_foreign_QUEUE_row_change',lambda:accept_merge_changes({'unsolved_math_prioritization/QUEUE.md':wrong_queue}))
wrong_own=r.h.body_at('unsolved_math_prioritization/QUEUE.md',mr['commit']).replace(b'| claimed_solved | 2/5 |',b'| solved | 5/5 |')
reject('coherent_refingerprinted_own_QUEUE_status_effort_change',lambda:accept_merge_changes({'unsolved_math_prioritization/QUEUE.md':wrong_own}))
for field,value in [('UTC',FUTURE),('updated_UTC',FUTURE),('UTC',OLD),('updated_UTC',OLD)]:
 def attack(field=field,value=value):
  p=r.m.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(r.h.body_at(p,mr['commit']));j[field]=value
  return accept_merge_changes({p:enc(j)})
 reject('programme_date_'+field+'_'+('future' if value==FUTURE else 'predates_evidence'),attack)
for role,path in [('protected','protected/support.txt'),('paper','package_test/paper.tex'),('proof','CURRENT_PROOF_V4.md'),('science_review','science1/report.json'),('control','campaign_aliases.py'),('gate','ROOT_PUBLICATION_GATE.json')]:
 reject('coherent_refingerprinted_immutable_'+role,lambda path=path:accept_merge_changes({r.m.CASE+path:b'forged protected bytes\n'}))
reject('coherent_refingerprinted_wrong_operative_message',lambda:accept_merge_changes({},message='novel original first theorem\n\nPR191 selected-map SHA256: '+mr['selected_map_sha256']))
for key,value in [('novelty_clearance',True),('original_effort','5/5'),('actual_Zenodo_published',False),('case_percent',100)]:
 def attack(key=key,value=value):
  p=r.m.CASE+'CURRENT_CASE_STATUS.json';j=json.loads(r.h.body_at(p,mr['commit']));j[key]=value;return accept_merge_changes({p:enc(j)})
 reject('case_postimage_'+key,attack)
# Full tree delta catches changes outside the selected map even with a coherent fingerprint.
reject('hidden_full_tree_extra_path',lambda:accept_merge_changes({'foreign/unselected.txt':b'bad\n'}))
# Immutable-generation content attack on combined-current factual acceptance.
if factual is not None:
 for path in ['protected/support.txt','package_test/paper.tex']:
  def attack(path=path):
   full=q.m.CASE+path;files=copy.deepcopy(q.h.commits[factual['commit']]['files']);files[full]=b'altered at actual descendant MAIN\n';old=q.h.main;q.h.main=q.h.seed(files,[factual['commit']],'unrelated descendant plus protected corruption')
   try:return q.m.factual_accept()
   finally:q.h.main=old
  reject('combined_current_identity_'+path.replace('/','_'),attack)
 # Change immutable original-merge receipt after factual preparation; both factual boundaries must revalidate it.
 def original_merge_drift():
  old=(q.root/'SCOPED_MERGE_PREPARATION.json').read_bytes();rr=json.loads(old);rr['selected_map_sha256']='f'*64;q.put('SCOPED_MERGE_PREPARATION.json',rr)
  try:return q.m.factual_accept()
  finally:q.put('SCOPED_MERGE_PREPARATION.json',old)
 reject('factual_accept_revalidates_original_merge',original_merge_drift)
# Verify actual programme cursor remains 191 in the factual postimage, 192 only authorized by receipt.
if factual is not None:
 j=json.loads(q.h.body_at(q.m.PREFIX+'CURRENT_PROGRESS.json',factual['commit']))
 check('factual_postimage_cursor_and_counts',lambda:{'asserted':j['next_numeric_intake_cursor']==191 and j['advance_to_next_PR_authorized_now'] is False and (j['fully_completed_count'],j['published_count'])==(40,24)})
# Public material excludes private rows: scan only selected/public outputs, never private service bodies.
def privacy():
 for root in [f,r,q]:
  for p in root.root.rglob('*.json'):
   if 'lifecycle_private' not in p.parts:
    assert PRIVATE_SENTINEL not in p.read_text(),'private row leaked in '+p.name
 return 'No private foreign-row sentinel in public JSON outputs.'
check('public_receipt_privacy',privacy)


# Additional final-boundary tests and independent full-native oracle.
def independent_native_expected(fixture,merged):
 m=fixture.m;g=fixture.g;z=m.read(fixture.root/'ZENODO_PUBLICATION_READBACK.json');tr=m.read(fixture.root/'TRACKER_ACCEPTANCE.json');files=copy.deepcopy(fixture.native)
 for accepted in ([False,True] if merged else [False]):
  common={'UTC':NOW,'whole_package_reviews_complete':True,'publication_ready':True,'actual_Zenodo_published':True,'actual_published':True,'actual_DOI':z['doi'],'actual_tracker_updated':True,'actual_tracker_range':tr['range'],'actual_original_PR_merged':accepted,'case_percent':100 if accepted else 95,'snapshot_semantics':'Actual publication/tracker facts; original-head merge '+('accepted' if accepted else 'pending at this preparation')+'; factual MAIN adoption requires separate actual acceptance.'}
  flags={'whole_package_reviews_pending':False,'successive_NEW_whole_package_reviews_complete':True,'publication_clearance':True,'publication_and_tracker_actions_not_yet_performed':False,'not_an_approval':False,'completed_new_whole_package_reviews':2}
  for name in sorted(g['native_json_status_paths']):
   value=json.loads(files[name]);value.update({k:v for k,v in {**common,**flags}.items() if k in value})
   if name=='PUBLICATION.json':value.update(UTC=NOW,kind='ACTUAL_PUBLISHED_TRACKED_CREDITED_NOTE',package='package_test',paper='paper.pdf',source='paper.tex',support='support.zip',metadata='deposit.json',actual_DOI=z['doi'],actual_Zenodo_published=True,actual_tracker_range=tr['range'],actual_original_PR_merged=accepted,whole_package_review_status='Successive NEW whole-package reviews completed; final clean',gate_sha256=z['gate_sha256'])
   if name=='PUBLICATION_PACKAGE_PLAN.json':value.update(package_case_relative=m.CASE+'package_test/',planned_files=['paper.pdf','paper.tex','support.zip'],actual_published=True,actual_DOI=z['doi'],publication_ready=True)
   if name=='review/WHOLE_PACKAGE_REVIEW_STATUS.json':value.update(status='SUCCESSIVE_NEW_COMPLETE_PACKAGE_REVIEWS_FINAL_CLEAN',not_an_approval=False,completed_new_whole_package_reviews=2,paper_science_and_current_native_template_require_review=False)
   files[name]=enc(value)
  sentence='The successive NEW whole-package review loop is complete and final clean. Exact note '+z['doi_url']+' is actually published and tracker '+tr['range']+' was verified twice. Original-head merge '+('was actually accepted; final factual MAIN acceptance follows separately.' if accepted else 'remains pending at this preparation.')+' Extensive AI; unrefereed.'
  for name,original in fixture.needles.items():
   old=oldsentence if accepted else original;assert files[name].count(old.encode())==1;files[name]=files[name].replace(old.encode(),sentence.encode())
  files['RESEARCH_LOG.md']+=('\n'+NOW+' — '+sentence+' Original effort2/5 retained. '+('40/24 factual postimage requires actual MAIN acceptance.' if accepted else '39completed/23published until actual factual acceptance.')+'\n').encode()
  oldsentence=sentence
 return files

def oracle_check(fixture,merged):
 expected=independent_native_expected(fixture,merged);name=fixture.g['native_complete_template'] if merged else fixture.g['native_final_template'];actual={n:(fixture.root/'integration_preparation'/name/n).read_bytes() for n in expected}
 assert actual==expected and len(actual)==50
 assert all(actual[f'ORIGINAL_SUBMISSION/o{i:02}.txt']==fixture.native[f'ORIGINAL_SUBMISSION/o{i:02}.txt'] for i in range(16))
 return {'native_bytes_independently_equal':50,'originals_byte_identical':16,'stage':100 if merged else 95}
check('independent_full_native95_oracle',lambda:oracle_check(q,False))
check('independent_full_native100_oracle',lambda:oracle_check(q,True))

def uninjected_context_after_receipts():
 old=f.m._runtime;f.m._runtime=None
 try:return f.m.publication()
 finally:f.m._runtime=old
reject('existing_receipts_still_require_explicit_service_context',uninjected_context_after_receipts)

def adapters_import_inert():
 old=sys.modules.get('lifecycle_common');sys.modules['lifecycle_common']=f.m
 try:
  for n in f.m.CONTROL_FILES[1:]:exec(compile((SOURCE/n).read_bytes(),str(SOURCE/n),'exec'),{'__name__':'independent_adapter_import','__file__':str(SOURCE/n)})
 finally:
  if old is None:sys.modules.pop('lifecycle_common',None)
  else:sys.modules['lifecycle_common']=old
 return {'adapters_imported_without_execution':8}
check('eight_adapter_imports_inert',adapters_import_inert)

# Both generated programme date fields must be bounded at phase100 too.
if factual is not None:
 for field,value in [('UTC',FUTURE),('updated_UTC',FUTURE),('UTC',OLD),('updated_UTC',OLD),('UTC','not-a-timestamp')]:
  def attack(field=field,value=value):
   path=q.m.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(q.h.body_at(path,factual['commit']));j[field]=value;rr=q.reforge(factual,{path:enc(j)});q.put('FINAL_FACTUAL_PREPARATION.json',rr);q.h.main=rr['commit']
   try:return q.m.factual_accept()
   finally:q.put('FINAL_FACTUAL_PREPARATION.json',factual);q.h.main=factual['commit']
  reject('factual_programme_date_'+field+'_'+('future' if value==FUTURE else 'predates_evidence' if value==OLD else 'malformed'),attack)
 # Selected native companion pointer is independently checked at acceptance.
 def companion_attack():
  path=q.m.CASE+'integration_preparation/native_template_complete_test_MANIFEST.json';j=json.loads(q.h.body_at(path,factual['commit']));j['actual_DOI']='10.0000/unapproved';rr=q.reforge(factual,{path:enc(j)});q.put('FINAL_FACTUAL_PREPARATION.json',rr);q.h.main=rr['commit']
  try:return q.m.factual_accept()
  finally:q.put('FINAL_FACTUAL_PREPARATION.json',factual);q.h.main=factual['commit']
 reject('factual_companion_manifest_coherent_rehash_rejected',companion_attack)
 # The same corrupt QUEUE accepted at merge also survives both factual boundaries.
 def queue_through_factual():
  t=Fixture('queue_entire_flow');rr=t.prep95();path='unsolved_math_prioritization/QUEUE.md';wrong=t.h.body_at(path,rr['commit']).replace(b'| foreign / row | keep |',b'| foreign / row | CORRUPTED |');rr=t.reforge(rr,{path:wrong});t.put('SCOPED_MERGE_PREPARATION.json',rr);t.h.main=rr['commit'];t.h.pr.update(merged=True,state='closed');t.m.integration_accept();fr=t.m.factual_prepare('factual_preparation_corrupt_queue');t.h.main=fr['commit'];accepted=t.m.factual_accept();assert b'CORRUPTED' in t.h.body_at(path,t.h.main);return {'factual_status':accepted['status'],'foreign_queue_corruption_survived':True}
 reject('foreign_QUEUE_corruption_survives_both_factual_boundaries',queue_through_factual)

# Missing or extra selected paths and true-parent changes fail even with a new message.
def wrong_parent():
 rr=copy.deepcopy(mr);rr['parent_tree']='f'*40;r.put('SCOPED_MERGE_PREPARATION.json',rr);r.h.main=mr['commit'];return r.m.integration_accept()
reject('actual_true_parent_tree_binding',wrong_parent)

def missing_selected():
 rr=copy.deepcopy(mr);rr['selected_files'].pop('unsolved_math_prioritization/QUEUE.md');rr['selected_map_sha256']=r.m.selected_digest(rr['selected_files']);files=copy.deepcopy(r.h.commits[mr['commit']]['files']);message=r.m.operative_message(r.kit.result(),[mr['expected_main'],r.m.HEAD],rr['selected_map_sha256']);rr['commit']=r.h.seed(files,[mr['expected_main'],r.m.HEAD],message);r.put('SCOPED_MERGE_PREPARATION.json',rr);r.h.main=rr['commit'];return r.m.integration_accept()
reject('missing_selected_QUEUE_path',missing_selected)

# Stale MAIN retry leaves the existing 100-byte generation unchanged.
def stale_retry():
 t=Fixture('stale_retry');a=t.adopt95();before_main=t.h.main;fr=t.m.factual_prepare('factual_preparation_first');first={p.relative_to(t.root).as_posix():p.read_bytes() for p in (t.root/'integration_preparation/native_template_complete_test').rglob('*') if p.is_file()};files=copy.deepcopy(t.h.commits[before_main]['files']);files['unrelated/added.txt']=b'concurrent unrelated addition\n';t.h.main=t.h.seed(files,[before_main],'unrelated concurrent MAIN');fr2=t.m.factual_prepare('factual_preparation_retry');second={p.relative_to(t.root).as_posix():p.read_bytes() for p in (t.root/'integration_preparation/native_template_complete_test').rglob('*') if p.is_file()};assert first==second and fr['selected_files']==fr2['selected_files'];t.h.main=fr2['commit'];return {'status':t.m.factual_accept()['status'],'same_immutable_selected_map':True}
check('stale_MAIN_retry_same_generation_exact_bytes',stale_retry)

# Respect explicit prohibition on actual Root main execution. Inspect current handoff
# AST and exercise only its pure pin matcher and exclusive fresh writer in own sandbox.
def handoff_static_and_exclusive():
 path=HERE.parent/'prepare_root_publication_clearance_v2.py';raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()=='6df49335d56f411836ca1206e2cfca04817bf84c6c5cf5e9d47750818c50aac5' and (path.stat().st_mode&0o777)==0o444
 tree=ast.parse(raw);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');source=ast.get_source_segment(raw.decode(),main)
 assert "ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW04_PASS" in source and source.index("Root final independent04 acceptance absent")<source.index("with (A/n).open('xb')")
 expected=set(f.m.CONTROL_FILES);required=next(n.value for n in main.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='required' for x in n.targets));assert ast.literal_eval(required)==expected and len(expected)==9
 assert "not (A/n).exists()" in source and "with (A/n).open('xb')" in source and "m.case_scientific_projection" in source and "m.gate();m.read=original_read" in source
 ns={'__file__':str(path),'__name__':'independent_handoff_no_main'};exec(compile(raw,str(path),'exec'),ns);ns['A']=HERE/'work/handoff_helpers'
 if ns['A'].exists():shutil.rmtree(ns['A'])
 ns['A'].mkdir(exist_ok=True)
 ns['fresh']('new.json',{'synthetic':True});before=(ns['A']/'new.json').read_bytes()
 try:ns['fresh']('new.json',{'overwritten':True})
 except FileExistsError:pass
 else:raise AssertionError('handoff fresh overwrote')
 assert before==(ns['A']/'new.json').read_bytes() and ((ns['A']/'new.json').stat().st_mode&0o777)==0o444
 return {'root_main_executed':False,'exact_runtime_set':9,'exclusive_writer_rejects_existing':True,'auth_before_install':'statically verified','full_handoff_live_execution':'prohibited and unperformed'}
check('Root_v2_handoff_pins_static_order_and_exclusive_writer',handoff_static_and_exclusive)



def unknown_publication_before_write():
 t=Fixture('unknown_publish_before');t.m.run_zenodo('stage',runner=t.kit);attempts=[]
 def fail_publish(args,**kw):
  if args[6]=='publish':attempts.append(1);raise TimeoutError('unknown before server write')
  return t.kit(args,**kw)
 try:t.m.run_zenodo('publish',9000005,runner=fail_publish)
 except TimeoutError:pass
 else:raise AssertionError('expected uncertain outcome')
 try:t.m.run_zenodo('publish',9000005,runner=fail_publish)
 except RuntimeError as e:assert 'no second POST' in str(e)
 else:raise AssertionError('blind repeat was allowed')
 assert len(attempts)==1 and t.kit.publications==0
 return {'publication_attempts':1,'automatic_retry_writes':0}
check('unknown_publication_without_observed_commit_no_blind_retry',unknown_publication_before_write)

def unknown_tracker_before_write():
 t=Fixture('unknown_tracker_before');t.publish();attempts=[]
 def fail_append(resource,method,params,body=None):
  if method=='append':attempts.append(1);raise TimeoutError('unknown before server append')
  return t.tracker(resource,method,params,body)
 try:t.m.record_tracker(fail_append)
 except TimeoutError:pass
 else:raise AssertionError('expected uncertain outcome')
 try:t.m.record_tracker(fail_append)
 except RuntimeError as e:assert 'no automatic second write' in str(e)
 else:raise AssertionError('blind repeat was allowed')
 assert len(attempts)==1 and t.tracker.append_calls==0
 return {'append_attempts':1,'automatic_retry_writes':0}
check('unknown_tracker_without_observed_commit_no_blind_retry',unknown_tracker_before_write)

# Native receipt times are bound to accepted facts, unlike the demonstrated
# programme JSON gap. No live clock expiry is added to immutable generations.
for key,value in [('published',OLD),('published',FUTURE)]:
 def attack(key=key,value=value):
  cur=q.m.read(q.root/'integration_preparation/native_template_final_test_MANIFEST.json');cur['factual_timestamps'][key]=value
  return q.m.expected_native_receipt(cur,q.g,q.m.read(q.root/'ZENODO_PUBLICATION_READBACK.json'),q.m.read(q.root/'TRACKER_ACCEPTANCE.json'),False)
 reject('native_timestamp_'+('future' if value==FUTURE else 'predates_evidence'),attack)

def current_seed_identity_only():
 p=HERE.parent/'IMMUTABLE_CARRY_FORWARD_FROM_OPERATIONS03_01.json';raw=p.read_bytes();j=json.loads(raw)
 assert hashlib.sha256(raw).hexdigest()=='e8f578e61b8942a912e20b9025edfc756022c385a265029bf055730d7a1d86eb' and len(j['public_case_pins'])==513
 return {'seed_members':513,'dated_seed_is_not_current_MAIN_or_authority':True}
check('Root_seed513_exact_announced_identity',current_seed_identity_only)

def main():
 out={'schema':'PR191_INDEPENDENT_ADVERSARY04_RESULTS_V1','UTC':datetime.datetime.now(datetime.UTC).isoformat(),'scope':'offline frozen04 proposal; no live action certification','fixture_source':'independent_fixtures_preinspection_04.py','author_harness_or_results_used':False,'production_helper_imports':0,'external_calls':0,'results':RESULTS,'summary':{'total':len(RESULTS),'passed':sum(x['passed'] for x in RESULTS),'failed':sum(not x['passed'] for x in RESULTS)}}
 result_name=sys.argv[sys.argv.index('--results')+1] if '--results' in sys.argv else 'PROBE_RESULTS_04.json'
 target=HERE/result_name
 assert target.resolve().is_relative_to(HERE.resolve()),'Replay results must stay in own directory'
 target.write_bytes(enc(out))
 print(json.dumps({'summary':out['summary'],'failures':[x['name'] for x in RESULTS if not x['passed']]} ,indent=2))
if __name__=='__main__':main()

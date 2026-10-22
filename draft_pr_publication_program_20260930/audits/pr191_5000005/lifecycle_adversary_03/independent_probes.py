"""Independent terminal03 offline probes. Never calls production services/helpers.
Derived from the separately sealed acceptance_plan.md, without author harness.
All fixture writes are within this reviewer-owned directory. Gate and clearance
exist only as in-memory synthetic authorities; no real Root authority is made.
"""
from pathlib import Path
from types import SimpleNamespace, ModuleType
from datetime import datetime, timezone
import copy, hashlib, json, sys, shutil

OWN=Path(__file__).resolve().parent
BASE=OWN.parent
SRC=BASE/'lifecycle_controls_preparation_03'
FIX=OWN/'offline_fixture'
FIX.mkdir(exist_ok=True)
RESULTS=[]
EXPECTED_INPUTS={
 'lifecycle_controls_preparation_03/FINAL_SEAL.json':'93d882058e6696b71db930f152cb6ef18dbf77784e7189a29cfaefd8a0d89896',
 'lifecycle_controls_preparation_03/lifecycle_common.py':'f55b3590debf98cf69b061c2f1488e2323e71325766e2a3d34bebf4c0db9a32e',
 'prepare_root_publication_clearance.py':'01b6a878354d2c6271e98cdfa1e69817894ec8c61b4248fd1bccf4cd4792e670',
 'ROOT_PUBLICATION_GATE_DRAFT_01.json':'5ee37c8a196f86ded963e48b6d9361d35ac0a025b1a1dec8f6b6d81f1f5fd199'}
for n,digest in EXPECTED_INPUTS.items():
 assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==digest, 'Pinned input changed: '+n
source_seal=json.loads((SRC/'FINAL_SEAL.json').read_text())
for x in source_seal['manifest']:
 data=(SRC/x['path']).read_bytes()
 assert len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256'], 'Frozen proposal manifest drift'

def bp(b):
 return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(n,b):
 p=FIX/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b if isinstance(b,bytes) else enc(b));return p

def result(name,ok,detail=''):
 RESULTS.append({'id':name,'expected_invariant_met':bool(ok),'detail':detail})
def reject(name,call):
 try:call()
 except (RuntimeError,KeyError,ValueError,TypeError,FileNotFoundError) as e:result(name,True,type(e).__name__+': '+str(e).replace(str(FIX),'<fixture>'))
 else:result(name,False,'Invalid candidate accepted')

def raw_import(path, module_name='reviewed_runtime'):
 m=ModuleType(module_name);m.__file__=str(FIX/path.name);sys.modules[module_name]=m
 exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__)
 return m

# Gate fixtures derive from exact Root DRAFT; all ready authority is in memory.
draft=json.loads((BASE/'ROOT_PUBLICATION_GATE_DRAFT_01.json').read_text())
g=copy.deepcopy(draft)
copy_names=set(g['public_case_pins'])
copy_names.update(x['path'] for r in g['whole_package_reviews'] for x in [r['report'],r['seal'],r['root_authentication']])
copy_names.update(g[k]['path'] for k in ['review_input','current_proof','native_pending_manifest','pr_metadata_proposal','tracker_row_proposal'])
copy_names.add('ORIGINAL_FILE_MANIFEST.json')
copy_names.update(g['package_name']+'/'+n for n in g['payloads'])
pending_manifest=json.loads((BASE/g['native_pending_manifest']['path']).read_text())
copy_names.update('integration_preparation/'+g['native_pending_template']+'/'+n for n in pending_manifest['files'])
for n in sorted(copy_names):
 p=BASE/n
 if p.is_file():save(n,p.read_bytes())
for n in ['lifecycle_common.py','campaign_aliases.py','run_zenodo_step.py','record_tracker.py','prepare_native_final_01.py','prepare_pr_metadata_request.py','prepare_final_main_scope.py','prepare_final_scoped_merge.py','prepare_factual_completion.py']:
 save(n,(SRC/n).read_bytes())

# Check actual common/adapters import is inert; __main__ is never used.
before={str(p.relative_to(FIX)):bp(p.read_bytes()) for p in FIX.rglob('*') if p.is_file()}
m=raw_import(SRC/'lifecycle_common.py','lifecycle_common')
m.A=FIX
for p in sorted(SRC.glob('*.py')):
 if p.name in ['SELFTEST.py','lifecycle_common.py']:continue
 raw_import(p,'isolated_'+p.stem)
after={str(p.relative_to(FIX)):bp(p.read_bytes()) for p in FIX.rglob('*') if p.is_file()}
result('I01_import_file_inert',before==after and m._runtime is None and m._helpers is None)

# Deny any future accidental real process/helper use; all tests inject models.
def forbidden(*a,**k):raise AssertionError('Forbidden production action')
m.subprocess.run=forbidden
m.importlib.util.spec_from_file_location=forbidden
virtual={}
oldread=m.read;oldpin=m.pin
m.read=lambda p:copy.deepcopy(json.loads(virtual[str(Path(p))])) if str(Path(p)) in virtual else oldread(p)
m.pin=lambda p:bp(virtual[str(Path(p))]) if str(Path(p)) in virtual else oldpin(p)
def syncgate():virtual[str(FIX/'ROOT_PUBLICATION_GATE.json')]=enc(g)
def syncclear(j):virtual[str(FIX/m.OP_CLEARANCE)]=enc(j)
for role in ['report','seal','authentication']:
 save('synthetic_authority/'+role+'.json',{'synthetic':True,'role':role})
def binding(n):return {'path':n,**{k:v for k,v in bp((FIX/n).read_bytes()).items() if k!='git_blob'}}
op={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','PR':191,'original_head':m.HEAD,'all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':{n:{k:v for k,v in bp((SRC/n).read_bytes()).items() if k!='git_blob'} for n in m.CONTROL_FILES},'independent_adversary_review':{'disposition':'PASS','report':binding('synthetic_authority/report.json'),'seal':binding('synthetic_authority/seal.json'),'root_authentication':binding('synthetic_authority/authentication.json')}}
syncclear(op)
g.update(status='READY_FOR_AUTHORIZED_PUBLICATION',all_required_findings_globally_resolved=True,draft_only=False)
g['public_case_pins'][m.OP_CLEARANCE]={k:v for k,v in bp(enc(op)).items() if k!='git_blob'}
for n in m.CONTROL_FILES:g['public_case_pins'][n]={k:v for k,v in bp((SRC/n).read_bytes()).items() if k!='git_blob'}
syncgate()
result('G01_full_ready_clone_accepts',m.gate()['original_head']==m.HEAD)
validg=copy.deepcopy(g)
for name,key,value in [('G02_draft_rejected','status',draft['status']),('G03_head_rejected','original_head','0'*40),('G04_unresolved_rejected','all_required_findings_globally_resolved',False)]:
 g[key]=value;syncgate();reject(name,m.gate);g=copy.deepcopy(validg);syncgate()
g['whole_package_reviews'][1]['reviewer_id']=g['whole_package_reviews'][0]['reviewer_id'];syncgate();reject('G05_duplicate_science_reviewer',m.gate);g=copy.deepcopy(validg);syncgate()
oldop=copy.deepcopy(op)
for name,mut in [('G06_clearance_notpass',lambda j:j['independent_adversary_review'].update(disposition='REPAIR_REQUIRED')),('G07_clearance_wrong_runtime',lambda j:j['runtime_pins']['lifecycle_common.py'].update(sha256='0'*64)),('G08_clearance_unresolved',lambda j:j.update(outstanding_required_repairs=['synthetic repair']))]:
 j=copy.deepcopy(oldop);mut(j);syncclear(j);g['public_case_pins'][m.OP_CLEARANCE]={k:v for k,v in bp(enc(j)).items() if k!='git_blob'};syncgate();reject(name,m.gate)
 op=copy.deepcopy(oldop);syncclear(op);g=copy.deepcopy(validg);syncgate()
proof=FIX/g['current_proof']['path'];b=proof.read_bytes();proof.write_bytes(b+b'\n');reject('G09_approved_proof_byte_drift',m.gate);proof.write_bytes(b)
reject('G10_no_default_runtime',lambda:m.require_runtime())

# Exact publication receipt fixture; actual remote calls are injected.
gatehash=m.pin(FIX/'ROOT_PUBLICATION_GATE.json')['sha256']
z={'environment':'production','id':987654321,'state':'published','doi':'10.5281/zenodo.987654321','doi_url':'https://doi.org/10.5281/zenodo.987654321','record_url':'https://zenodo.org/records/987654321','files':[{'name':g['paper_files'][k],'size':g['payloads'][g['paper_files'][k]]['bytes'],'sha256':g['payloads'][g['paper_files'][k]]['sha256']} for k in ['pdf','source','support']],'metadata_normalizations':[],'doi_resolution':{'status':'resolved'},'receipt_saved':True,'verified_utc':datetime.now(timezone.utc).isoformat(),'gate_sha256':gatehash}
result('Z01_publication_shape_valid',m.validate_publication(g,z)==z)
for name,mut in [('Z02_wrong_environment',lambda j:j.update(environment='sandbox')),('Z03_uploaded_bytes',lambda j:j['files'][0].update(sha256='f'*64)),('Z04_wrong_gate',lambda j:j.update(gate_sha256='f'*64)),('Z05_missing_uploaded',lambda j:j['files'].pop()),('Z06_wrong_DOI',lambda j:j.update(doi_url='https://doi.org/10.0/wrong'))]:
 j=copy.deepcopy(z);mut(j);reject(name,lambda:m.validate_publication(g,j))
save('ZENODO_STAGE_READBACK.json',{'id':z['id'],'gate_sha256':gatehash})
save('ZENODO_PUBLICATION_READBACK.json',z)
save('ZENODO_PUBLICATION_EVIDENCE.json',{'source':'EXACT_KIT_PUBLISHED_OUTPUT','command':'inspect','gate_sha256':gatehash,'receipt':binding('ZENODO_PUBLICATION_READBACK.json'),'manifest':g['payloads'][g['paper_files']['metadata']],'published_output':z})
m._runtime={'inspect':lambda _:copy.deepcopy(z)}
result('Z07_fresh_injected_observation',m.publication(g)==z)
zbad=copy.deepcopy(z);zbad['files'][0]['sha256']='f'*64;m._runtime['inspect']=lambda _:zbad
reject('Z08_fresh_remote_mismatch',lambda:m.publication(g));m._runtime['inspect']=lambda _:copy.deepcopy(z)

# A sheet model with synthetic foreign rows only. Results never contain row data.
class Sheet:
 def __init__(self):self.rows=[copy.deepcopy(m.HEADER),['SYNTHETIC_FOREIGN_A','','','SYNTHETIC_CONTEXT']];self.appends=0;self.fullreads=0;self.mode=None
 def call(self,resource,method,params,body=None):
  if resource=='spreadsheet':return {'spreadsheetId':m.SID,'sheets':[{'properties':{'sheetId':m.GID,'title':m.TAB}}]}
  if method=='append':
   assert params['valueInputOption']=='RAW';self.appends+=1;self.rows.append(copy.deepcopy(body['values'][0]));n=len(self.rows)
   if self.mode=='timeout_after_append':raise RuntimeError('Synthetic lost append response')
   return {'updates':{'updatedRange':f"'Math Puzzles'!A{n}:D{n}",'updatedRows':1,'updatedColumns':4}}
  rng=params['range']
  if rng.endswith('A1:D1'):return {'values':[copy.deepcopy(m.HEADER)]}
  if rng.endswith('A:D'):
   self.fullreads+=1
   if self.mode=='duplicate_after' and self.fullreads>=2 and len(self.rows)==3:self.rows.append(copy.deepcopy(self.rows[-1]))
   if self.mode=='foreign_change' and self.fullreads>=2:self.rows[1][3]='SYNTHETIC_CHANGED'
   return {'values':copy.deepcopy(self.rows)}
  n=m.own_range(rng);return {'values':[copy.deepcopy(self.rows[n-1])]}
def resettracker():
 for n in ['sheets_tracking','lifecycle_private']:
  if (FIX/n).exists():shutil.rmtree(FIX/n)
 p=FIX/'TRACKER_ACCEPTANCE.json'
 if p.exists():p.unlink()
for ident,mode in [('T01_clean_single_RAW','clean'),('T02_duplicate_postappend','duplicate_after'),('T03_foreign_preservation','foreign_change')]:
 resettracker();s=Sheet();s.mode=mode
 if mode=='clean':
  tr=m.record_tracker(s.call);result(ident,s.appends==1 and tr['actual_fresh_reads']==2);m._runtime['tracker']=s.call;result('T04_trust_boundary_rereads',m.published_tracked()[2]['row']==tr['row'])
  s.rows.append(copy.deepcopy(s.rows[-1]));reject('T05_later_duplicate_rejected',m.published_tracked)
 else:reject(ident,lambda:m.record_tracker(s.call))
resettracker();s=Sheet();s.mode='timeout_after_append';reject('T06_unknown_append_raises',lambda:m.record_tracker(s.call));s.mode='clean';m.record_tracker(s.call);result('T07_unknown_append_no_second_RAW',s.appends==1)
tr=m.read(FIX/'TRACKER_ACCEPTANCE.json');m._runtime['tracker']=s.call
public_tracker=[(FIX/'TRACKER_ACCEPTANCE.json').read_text()]+[p.read_text() for p in (FIX/'sheets_tracking').glob('*.json')]
result('T08_public_tracker_sanitized',not any('SYNTHETIC_FOREIGN' in b or 'SYNTHETIC_CONTEXT' in b for b in public_tracker))

# Independent native oracle: approved baseline plus exact declared fact fields.
baseline={n:(FIX/'integration_preparation'/g['native_pending_template']/n).read_bytes() for n in pending_manifest['files']}
def native_oracle(times,merged=False):
 out=dict(baseline)
 for accepted in ([False,True] if merged else [False]):
  stamp=times['merged' if accepted else 'published']
  sentence='The successive NEW whole-package review loop is complete and final clean. Exact note '+z['doi_url']+' is actually published and tracker '+tr['range']+' was verified twice. Original-head merge '+('was actually accepted; final factual MAIN acceptance follows separately.' if accepted else 'remains pending at this preparation.')+' Extensive AI; unrefereed.'
  common={'UTC':stamp,'whole_package_reviews_complete':True,'publication_ready':True,'actual_Zenodo_published':True,'actual_published':True,'actual_DOI':z['doi'],'actual_tracker_updated':True,'actual_tracker_range':tr['range'],'actual_original_PR_merged':accepted,'case_percent':100 if accepted else 95,'snapshot_semantics':'Actual publication/tracker facts; original-head merge '+('accepted' if accepted else 'pending at this preparation')+'; factual MAIN adoption requires separate actual acceptance.'}
  other={'whole_package_reviews_pending':False,'successive_NEW_whole_package_reviews_complete':True,'publication_clearance':True,'publication_and_tracker_actions_not_yet_performed':False,'not_an_approval':False,'completed_new_whole_package_reviews':len(g['whole_package_reviews'])}
  for n in g['native_json_status_paths']:
   j=json.loads(out[n]);j.update({k:v for k,v in {**common,**other}.items() if k in j})
   if n=='PUBLICATION.json':j.update(UTC=stamp,kind='ACTUAL_PUBLISHED_TRACKED_CREDITED_NOTE',package=g['package_name'],paper=g['paper_files']['pdf'],source=g['paper_files']['source'],support=g['paper_files']['support'],metadata=g['paper_files']['metadata'],actual_DOI=z['doi'],actual_Zenodo_published=True,actual_tracker_range=tr['range'],actual_original_PR_merged=accepted,whole_package_review_status='Successive NEW whole-package reviews completed; final clean',gate_sha256=z['gate_sha256'])
   if n=='PUBLICATION_PACKAGE_PLAN.json':j.update(package_case_relative=m.CASE+g['package_name']+'/',planned_files=[g['paper_files'][k] for k in ['pdf','source','support']],actual_published=True,actual_DOI=z['doi'],publication_ready=True)
   if n=='review/WHOLE_PACKAGE_REVIEW_STATUS.json':j.update(status='SUCCESSIVE_NEW_COMPLETE_PACKAGE_REVIEWS_FINAL_CLEAN',not_an_approval=False,completed_new_whole_package_reviews=len(g['whole_package_reviews']),paper_science_and_current_native_template_require_review=False)
   out[n]=enc(j)
  for n,pending in g['native_text_status_replacements'].items():
   old=('The successive NEW whole-package review loop is complete and final clean. Exact note '+z['doi_url']+' is actually published and tracker '+tr['range']+' was verified twice. Original-head merge remains pending at this preparation. Extensive AI; unrefereed.') if accepted else pending
   assert out[n].count(old.encode())==1;out[n]=out[n].replace(old.encode(),sentence.encode())
  out['RESEARCH_LOG.md']+=('\n'+stamp+' — '+sentence+' Original effort2/5 retained. '+('40/24 factual postimage requires actual MAIN acceptance.' if accepted else '39completed/23published until actual factual acceptance.')+'\n').encode()
 return out
stamp=datetime.now(timezone.utc).isoformat();times={'published':stamp}
expected=native_oracle(times)
result('N01_independent_full50_oracle',len(expected)==50 and m.derive_native(g,z,tr,baseline,times)==expected)
result('N02_original16_unchanged',sum(n.startswith('ORIGINAL_SUBMISSION/') for n in expected)==16 and all(v==baseline[n] for n,v in expected.items() if n.startswith('ORIGINAL_SUBMISSION/')))
sciencekeys=['novelty_clearance','historical_priority_clearance','independent_simultaneous_discovery_certified','source_author_authenticated_erratum','unique_printed_source_intent_certified','AI_used_extensively','unrefereed','conventional_human_peer_review_claimed']
result('N03_science_policy_preserved',all(json.loads(expected[n])[k]==json.loads(baseline[n])[k] for n in ['CURRENT_RESULT.json','readiness.json'] for k in sciencekeys))
def native_receipt(files,ts,merged=False):
 return {'UTC':max(ts.values()),'current_template':g['native_complete_template'] if merged else g['native_final_template'],'files':{n:bp(b) for n,b in files.items()},'original_head':m.HEAD,'gate_sha256':gatehash,'actual_DOI':z['doi'],'actual_tracker_range':tr['range'],'factual_timestamps':ts,'reviewed_scientific_bytes_preserved':True,'only_declared_factual_paths_changed':sorted(set(g['native_json_status_paths'])|set(g['native_text_status_replacements'])|{'RESEARCH_LOG.md'}),'actual_original_PR_merged':merged,'MAIN_updated_by_preparation':False}
cur=native_receipt(expected,times)
result('N04_valid_receipt_accepts',m.expected_native_receipt(cur,g,z,tr,False)==expected)
bad=copy.deepcopy(cur);key='CURRENT_RESULT.json';changed=json.loads(expected[key]);changed['novelty_clearance']=True;bad['files'][key]=bp(enc(changed));reject('N05_rehashed_science_change',lambda:m.expected_native_receipt(bad,g,z,tr,False))
future={'published':'2099-01-01T00:00:00+00:00'};futurefiles=native_oracle(future);futurecur=native_receipt(futurefiles,future)
try:m.expected_native_receipt(futurecur,g,z,tr,False)
except RuntimeError:result('N06_future_factual_timestamp_rejected',True)
else:result('N06_future_factual_timestamp_rejected',False,'Receipt and all50 native pins accepted with publication factual timestamp 2099; actual publication/tracker observations remain current.')
for n,b in expected.items():save('integration_preparation/'+g['native_final_template']+'/'+n,b)
save('integration_preparation/CURRENT_TEMPLATE.json',cur)

# In-memory native Git model. No Git CLI or real API is imported/called.
class Git:
 def __init__(self):
  self.trees={};self.commits={};self.bodies={};self.current='';self.m=SimpleNamespace(m=SimpleNamespace(h=SimpleNamespace(warm_selected_directories=lambda *a:None)))
 def addtree(self,bodymap):
  ident=hashlib.sha1(enc({n:bp(b) for n,b in sorted(bodymap.items())})).hexdigest();self.trees[ident]={n:bp(b)['git_blob'] for n,b in bodymap.items()};self.bodies[ident]=dict(bodymap);return ident
 def addcommit(self,tree,parents,message):
  ident=hashlib.sha1(enc([tree,parents,message])).hexdigest();self.commits[ident]={'sha':ident,'tree':{'sha':tree},'parents':[{'sha':p} for p in parents],'message':message};return ident
 def api(self,path,*a):
  if path.startswith('git/commits/'):return self.commits[path.split('/')[-1]]
  if path=='git/ref/heads/main':return {'object':{'sha':self.current}}
  if path=='pulls/191':return {'merged':True,'state':'closed','head':{'sha':m.HEAD},'draft':False}
  if path.startswith('compare/'):return {'status':'identical' if path.split('...')[-1]==path.split('compare/')[-1].split('...')[0] else 'ahead'}
  raise AssertionError('Unexpected model API '+path)
 def lookup(self,tree,n):return ('100644','blob',self.trees[tree][n]) if n in self.trees[tree] else None
 def changed_leaves(self,a,b):return {n for n in set(self.trees[a])|set(self.trees[b]) if self.lookup(a,n)!=self.lookup(b,n)}
 def body_at(self,n,commit):return self.bodies[self.commits[commit]['tree']['sha']][n]

# Build the full approved path set independently from contract requirements.
fixed={'ROOT_PUBLICATION_GATE.json','PR_METADATA_REQUEST.json','PR_METADATA_ACCEPTANCE.json','ZENODO_LOCAL_CHECK.json','ZENODO_STAGE_READBACK.json','ZENODO_DRAFT_READBACK.json','ZENODO_PUBLICATION_READBACK.json','ZENODO_PUBLICATION_EVIDENCE.json','ZENODO_POSTPUBLICATION_INSPECTION.json','TRACKER_ACCEPTANCE.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','FINAL_MAIN_SCOPE.json','ORIGINAL_FILE_MANIFEST.json','INTAKE_CHECKPOINT_ACCEPTANCE.json','ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+g['native_final_template']+'_MANIFEST.json'}
names=set(g['public_case_paths'])|set(g['public_case_pins'])|set(m.CONTROL_FILES)|fixed
names.update(g[k]['path'] for k in ['current_proof','native_pending_manifest','review_input','pr_metadata_proposal','tracker_row_proposal'])
names.update(x['path'] for r in g['whole_package_reviews'] for x in [r['report'],r['seal'],r['root_authentication']])
names.update(op['independent_adversary_review'][k]['path'] for k in ['report','seal','root_authentication'])
names.update(g['package_name']+'/'+n for n in g['payloads'])
names.update('integration_preparation/'+g['native_final_template']+'/'+n for n in baseline)
names.update('sheets_tracking/'+n for n in ['TARGET_VALIDATION.json','ROW_READBACK_1.json','ROW_READBACK_2.json','POSTAPPEND_UNIQUENESS_1.json','POSTAPPEND_UNIQUENESS_2.json'])
result('M00_independent_scope_oracle',names==m.scope_names(g))
paths={m.CASE+n for n in names}|{m.NATIVE+n for n in baseline}|{m.PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}|{'unsolved_math_prioritization/QUEUE.md'}
scope={'PR':191,'original_head':m.HEAD,'gate_sha256':gatehash,'case_paths':sorted(names),'selected_MAIN_paths':sorted(paths)}
save('FINAL_MAIN_SCOPE.json',scope)
bodymap={}
for n in names:
 p=FIX/n
 bodymap[m.CASE+n]=virtual[str(p)] if str(p) in virtual else p.read_bytes() if p.is_file() else b'SYNTHETIC_FACTUAL_PLACEHOLDER\n'
bodymap.update({m.NATIVE+n:b for n,b in expected.items()})
for n in paths-bodymap.keys():bodymap[n]=b'SYNTHETIC_PROGRAMME_OR_QUEUE\n'
h=Git();parenttree=h.addtree({'foreign/retained.txt':b'UNRELATED_OWNED_MODEL_CONTENT\n'});parent=h.addcommit(parenttree,[],'synthetic parent')
preparedtree=h.addtree({**h.bodies[parenttree],**bodymap})
def receipt(tree,message=None):
 selected={n:bp(h.bodies[tree][n]) for n in paths};digest=hashlib.sha256(json.dumps(selected,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 message=message or 'Merge PR191: credited parity-selected signed-angle law and literal counterexamples; '+z['doi_url']
 commit=h.addcommit(tree,[parent,m.HEAD],message+'\n\nPR191 selected-map SHA256: '+digest)
 return {'UTC':stamp,'expected_main':parent,'parent_tree':parenttree,'tree':tree,'commit':commit,'original_head':m.HEAD,'gate_sha256':gatehash,'selected_files':selected,'selected_map_sha256':digest,'changed_paths':sorted(paths)}
r=receipt(preparedtree);h.current=r['commit'];save('SCOPED_MERGE_PREPARATION.json',r)
m._helpers=h
# Retain real gate/publication/tracker validation; only actual API observations are injected.
result('M00b_real_gate_still_valid',m.gate()['original_head']==m.HEAD)
result('M01_full_integration_accept_control',m.integration_accept()['PR_merged'] is True)
# Alter actual approved scientific packet in Git only; local gate/files stay exact.
evilbody=dict(h.bodies[preparedtree]);packetpath=m.CASE+g['package_name']+'/'+g['paper_files']['source'];evilbody[packetpath]=b'UNAPPROVED SCIENTIFIC SOURCE BODY\n';eviltree=h.addtree(evilbody);evil=receipt(eviltree);h.current=evil['commit'];save('SCOPED_MERGE_PREPARATION.json',evil)
try:m.integration_accept()
except RuntimeError as e:result('M02_unapproved_packet_in_prepared_commit_rejected',True,str(e))
else:result('M02_unapproved_packet_in_prepared_commit_rejected',False,'Full integration_accept accepted a native Git commit whose packet TeX is unapproved; local trusted gate/payload bytes unchanged. Only prepared commit and untrusted preparation receipt were changed coherently.')
# Alter a gate-pinned case control/proof similarly while retaining native proof.
evilbody=dict(h.bodies[preparedtree]);caseproof=m.CASE+g['current_proof']['path'];evilbody[caseproof]=b'UNAPPROVED CASE PROOF BODY\n';eviltree=h.addtree(evilbody);evil=receipt(eviltree);h.current=evil['commit'];save('SCOPED_MERGE_PREPARATION.json',evil)
try:m.integration_accept()
except RuntimeError as e:result('M03_unapproved_case_proof_in_commit_rejected',True,str(e))
else:result('M03_unapproved_case_proof_in_commit_rejected',False,'Full integration_accept accepted altered gate-pinned CASE proof while approved local proof and native proof stayed exact.')
# Commit message must bind approved meaning, not merely contain a digest line.
evil=receipt(preparedtree,'PR191: FIRST NOVEL COMPLETE SOLUTION; human-refereed; priority certified');h.current=evil['commit'];save('SCOPED_MERGE_PREPARATION.json',evil)
try:m.integration_accept()
except RuntimeError as e:result('M04_unapproved_commit_message_rejected',True,str(e))
else:result('M04_unapproved_commit_message_rejected',False,'Full integration_accept accepted a contradictory scientific/priority commit message with the valid selected-map marker.')
# Positive negative controls for true parent and full foreign scope.
bad=copy.deepcopy(r);bad['parent_tree']='0'*40;reject('M05_wrong_actual_parent_tree',lambda:m.verify_prepared(h,bad,[parent,m.HEAD]))
foreignbody=dict(h.bodies[preparedtree]);foreignbody['foreign/retained.txt']=b'CHANGED_FOREIGN\n';foreigntree=h.addtree(foreignbody);foreignr=receipt(foreigntree);reject('M06_fulltree_foreign_delta',lambda:m.verify_prepared(h,foreignr,[parent,m.HEAD]))
h.current=r['commit'];m.selected_current(h,h.current,r['selected_files'],r['tree']);result('M07_current_selected_control',True)
advanced=dict(h.bodies[preparedtree]);advanced[caseproof]=b'CONCURRENT_SELECTED_DRIFT\n';advtree=h.addtree(advanced);adv=h.addcommit(advtree,[r['commit']],'synthetic concurrent descendant');reject('M08_concurrent_selected_drift',lambda:m.selected_current(h,adv,r['selected_files'],r['tree']))
advanced=dict(h.bodies[preparedtree]);advanced['foreign/addition.txt']=b'CONCURRENT_UNRELATED\n';advtree=h.addtree(advanced);adv=h.addcommit(advtree,[r['commit']],'synthetic unrelated descendant');m.selected_current(h,adv,r['selected_files'],r['tree']);result('M09_concurrent_foreign_addition_allowed',True)


# Factual acceptance independently checks native100, but must also check actual
# programme/case/workflow semantics against the exact authorized postimage.
# Restore the legitimate merge first, so this probe changes no approved packet.
h.current=r['commit'];save('SCOPED_MERGE_PREPARATION.json',r);m.integration_accept()
mergeaccept=m.read(FIX/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')
mergedtimes={**times,'merged':datetime.now(timezone.utc).isoformat()}
completed=native_oracle(mergedtimes,True);completecur=native_receipt(completed,mergedtimes,True)
factualnames={'SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+g['native_complete_template']+'_MANIFEST.json'}
factualnames.update('integration_preparation/'+g['native_complete_template']+'/'+n for n in baseline)
factualpaths={m.CASE+n for n in factualnames}|{m.NATIVE+n for n in baseline}|{m.PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
result('F00_independent_factual_scope_oracle',factualpaths==m.factual_paths(g))
factualbody=dict(h.bodies[preparedtree])
for n in factualnames:factualbody[m.CASE+n]=b'SYNTHETIC_FACTUAL_DECLARATION\n'
factualbody[m.CASE+'SCOPED_MERGE_PREPARATION.json']=enc(r)
factualbody[m.CASE+'ROOT_ACTUAL_MERGE_ACCEPTANCE.json']=enc(mergeaccept)
factualbody[m.CASE+'integration_preparation/CURRENT_TEMPLATE.json']=enc(completecur)
factualbody[m.CASE+'integration_preparation/'+g['native_complete_template']+'_MANIFEST.json']=enc(completecur)
for n,b in completed.items():
 factualbody[m.NATIVE+n]=b;factualbody[m.CASE+'integration_preparation/'+g['native_complete_template']+'/'+n]=b
# This is deliberately an invalid factual postimage: old39/23 counts and live
# 192 authority, which must not become actual acceptance simply via own pins.
factualbody[m.PREFIX+'CURRENT_PROGRESS.json']=enc({'current_PR':191,'fully_completed_count':39,'published_count':23,'next_numeric_intake_cursor':192,'advance_to_next_PR_authorized_now':True})
factualbody[m.CASE+'CURRENT_CASE_STATUS.json']=enc({'PR':191,'case_percent':95,'actual_original_PR_merged':False})
factualbody[m.CASE+'WORKFLOW_COMPLETION.json']=enc({'fully_completed_count':39,'published_count':23,'status':'NOT_COMPLETE'})
ftree=h.addtree(factualbody);fselected={n:bp(factualbody[n]) for n in factualpaths};fdigest=hashlib.sha256(json.dumps(fselected,sort_keys=True,separators=(',',':')).encode()).hexdigest()
fcommit=h.addcommit(ftree,[r['commit']],'Record PR191 factual40/24 completion; actual acceptance required before192\n\nPR191 selected-map SHA256: '+fdigest)
fr={'UTC':datetime.now(timezone.utc).isoformat(),'expected_main':r['commit'],'parent_tree':preparedtree,'tree':ftree,'commit':fcommit,'original_head':m.HEAD,'gate_sha256':gatehash,'selected_files':fselected,'selected_map_sha256':fdigest,'changed_paths':sorted(n for n in factualpaths if h.lookup(preparedtree,n)!=h.lookup(ftree,n))}
save('FINAL_FACTUAL_PREPARATION.json',fr);h.current=fcommit
try:m.factual_accept()
except RuntimeError as e:result('F01_invalid_factual_counts_cursor_rejected',True,str(e))
else:result('F01_invalid_factual_counts_cursor_rejected',False,'Full factual_accept issued40/24 and next192 acceptance while actual model MAIN programme contained39/23 with prematurely live192, case95/unmerged, and workflow NOT_COMPLETE; exact native100, actual parent/delta/maps/current identities and original approved merge remained valid.')

# Direct helper-free import of Root preparator: main is never invoked.
before={str(p.relative_to(FIX)):bp(p.read_bytes()) for p in FIX.rglob('*') if p.is_file()}
rootmodule=raw_import(BASE/'prepare_root_publication_clearance.py','isolated_root_preparator')
after={str(p.relative_to(FIX)):bp(p.read_bytes()) for p in FIX.rglob('*') if p.is_file()}
result('H01_root_preparator_import_inert',before==after and callable(rootmodule.main))

# Explicit injected uploader runner models lost publish response and recovery.
class OpenPR:
 def api(self,path,*a):
  assert path=='pulls/191';return {'head':{'sha':m.HEAD},'state':'open','merged':False,'draft':False}
m._helpers=OpenPR()
class KitRunner:
 def __init__(self):self.commands=[];self.published=False
 def __call__(self,args,**kw):
  command=args[6];self.commands.append(command)
  assert args[1:5]==['-E','-S','-B','-P']
  if command=='publish':self.published=True;return SimpleNamespace(returncode=1,stdout=b'',stderr=b'SYNTHETIC_LOST_RESPONSE')
  output=copy.deepcopy(z) if self.published else {'environment':'production','id':z['id'],'state':'ready_to_publish','files':z['files'],'metadata_normalizations':[]}
  return SimpleNamespace(returncode=0,stdout=enc(output),stderr=b'')
runner=KitRunner();save('ZENODO_STAGE_READBACK.json',{'id':z['id'],'gate_sha256':gatehash})
reject('Z09_wrong_confirmed_stage_id',lambda:m.run_zenodo('publish',z['id']+1,runner));result('Z10_wrong_id_no_external_call',runner.commands==[])
reject('Z11_uncertain_publish_blocks',lambda:m.run_zenodo('publish',z['id'],runner))
recovered=m.run_zenodo('publish',z['id'],runner)
result('Z12_uncertain_publish_one_POST',runner.commands.count('publish')==1 and recovered['state']=='published')


# Full native current-byte consumer also accepts the impossible future time;
# this does not rely solely on the lower-level pure derivation check.
for n,b in futurefiles.items():save('integration_preparation/'+g['native_final_template']+'/'+n,b)
save('integration_preparation/CURRENT_TEMPLATE.json',futurecur)
try:m.current_native(g,False,(z,tr))
except RuntimeError as e:result('N07_current_native_future_facts_rejected',True,str(e))
else:result('N07_current_native_future_facts_rejected',False,'current_native accepted all50 exact rederived files and receipt with publication timestamp2099 while unchanged actual publication/tracker observations are dated2026.')
for n,b in expected.items():save('integration_preparation/'+g['native_final_template']+'/'+n,b)
save('integration_preparation/CURRENT_TEMPLATE.json',cur)
for phase,counts in [(95,(39,23,190)),(100,(40,24,191))]:
 j={'current_PR':191,'fully_completed_count':counts[0],'published_count':counts[1],'last_completed_PR':counts[2],'dated_eligible_total':99,'next_numeric_intake_cursor':192,'advance_to_next_PR_authorized_now':True,'current_operational_lifecycle_audit_active':True,'current_operational_required_repairs':['SYNTHETIC_RESOLVED_HISTORY']}
 normalized=m.normalize(j,phase)
 result('A01_normalize_phase'+str(phase),normalized['next_numeric_intake_cursor']==191 and normalized['advance_to_next_PR_authorized_now'] is False and normalized['current_operational_lifecycle_audit_active'] is False and normalized['current_operational_required_repairs']==[] and normalized['current_historical_firstness_or_guaranteed_novelty_certified'] is False and bool(normalized['retired_operational_aliases_PR191']))
out={'schema':'PR191_LIFECYCLE_ADVERSARY03_INDEPENDENT_PROBES_V1','UTC':datetime.now(timezone.utc).isoformat(),'production_calls':0,'production_helpers_imported':0,'real_Root_gate_or_clearance_written':False,'author_harness_inspected_or_executed':False,'author_harness_hashed_only_for_input_integrity':True,'fixture_scientific_files':50,'tests':RESULTS,'total':len(RESULTS),'invariants_met':sum(x['expected_invariant_met'] for x in RESULTS),'mandatory_counterexamples':[x['id'] for x in RESULTS if not x['expected_invariant_met']]}
(OWN/'independent_results.json').write_bytes(enc(out))
print(json.dumps({k:v for k,v in out.items() if k!='tests'},indent=2))

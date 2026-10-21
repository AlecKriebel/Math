#!/usr/bin/env python3
"""Offline independent tests of actual PR399 helpers. No provider calls/mutations."""
import sys,pathlib,json,copy,tempfile,hashlib,re,datetime,io,zipfile,urllib.parse
sys.dont_write_bytecode=True
Q=pathlib.Path(__file__).resolve().parent;A=Q.parents[1];P=A.parents[1]/'private/pr0399_package_adversary_02';sys.path.insert(0,str(A))
import ops_binding as o,prepublication_check as p,publication_live_gates as g,record_publication_ledger as l,repository_integration as ri,publication_lifecycle as lc,verify_published_files as vf
from contextlib import contextmanager
@contextmanager
def patch(module,**values):
 old={k:getattr(module,k) for k in values}
 for k,v in values.items():setattr(module,k,v)
 try:yield
 finally:
  for k,v in old.items():setattr(module,k,v)

def need(value,label):
 if not value:raise RuntimeError(label)

def rejected(label,fn):
 try:fn()
 except (RuntimeError,ValueError,OSError,KeyError,TypeError,o.zenodo.DepositError) as e:return {'label':label,'rejected':True,'diagnostic':str(e)[:160]}
 raise RuntimeError('Unexpected acceptance: '+label)

metadata,selected=o.manifest();release=o.release();results=[];identifier=29999991;head='a'*40
variants={'canonical':'https://doi.org/10.5281/zenodo.'+str(identifier),'uppercase':'https://doi.org/10.5281/ZENODO.'+str(identifier),'mixed_notes':'Reference https://doi.org/10.5281/ZeNoDo.'+str(identifier),'encoded_period':'https://doi.org/10.5281/zenodo%2E'+str(identifier),'encoded_slash':'https://doi.org/10.5281%2Fzenodo.'+str(identifier)}
variants.update({n+'_exempt':variants[n] for n in ['canonical','uppercase','encoded_slash']})
for label,text in variants.items():
 with tempfile.TemporaryDirectory(dir=P) as name:
  root=pathlib.Path(name);audit=root/'audit';audit.mkdir();priv=root/'private';repo=root/'repo';(repo/'.zenodo-state').mkdir(parents=True);(root/'raw/pr0399').mkdir(parents=True)
  rows=[o.HEADERS,['Other problem','','',text]]
  (root/'raw/pr0399/ledger_live.json').write_text(json.dumps({'values':[o.HEADERS]}))
  recon={'pr':399,'root_identity_reconciliation_complete':True,'unresolved_leads':[],'release_manifest_sha256':o.RELEASE_SHA,'account_leads':[],'ledger_leads':[],'unrelated_local_state_exemptions':[]}
  if label.endswith('_exempt'):recon['ledger_leads']=[{'values_sha256':o.digest(rows[1]),'disposition':'distinct_non_target'}]
  (audit/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').write_text(json.dumps(recon))
  positive={'id':23174283,'metadata':{'title':'Fibonacci'},'files':[]};target={'id':identifier,'metadata':{'title':o.TITLE},'files':[]}
  class Client:
   base='https://offline.invalid'
   def __init__(self,*args):pass
   def request(self,method,url):
    need(method=='GET'and url.startswith(self.base),'no network')
    query=urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get('q',[''])[0]
    records=[positive] if query=='Fibonacci' else [positive,target] if not query else [target]
    return {'hits':{'total':len(records),'hits':copy.deepcopy(records)},'links':{}}
  pr={'number':399,'head':{'sha':head,'ref':o.BRANCH,'repo':{'full_name':'AlecKriebel/Math'}},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}},'state':'closed','merged':True,'draft':False}
  def read_cmd(args):
   if args[0]=='gws':return {'values':copy.deepcopy(rows)}
   if args[-1].endswith('pulls/399'):return copy.deepcopy(pr)
   return {'object':{'sha':'b'*40}}
  calls=[]
  def fake_gws(action,params,body=None):
   if action=='get':return {'values':copy.deepcopy(rows)}
   need(action=='append','offline provider mock permits only tested append')
   calls.append(copy.deepcopy(body));rows.extend(copy.deepcopy(body['values']))
   return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':body['values']}}}
  def public(i):
   need(i==identifier,'mock public identifier')
   v={'record':i,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':o.RELEASE_SHA}
   (audit/'ZENODO_PUBLIC_FILE_VERIFICATION.json').write_text(json.dumps(v));return v
  def collect(phase,expected_head,expected_id=None,allow_target_row=False):
   gate=p.gather(phase,expected_head,expected_id)
   return gate,g.reconcile(gate,phase,expected_head,expected_id,allow_target_row)
  with patch(p,ROOT=root,REPO=repo,PRIVATE=priv,read_command=read_cmd,verify_destination=lambda:None),patch(p.zenodo,ZenodoClient=Client,token_for=lambda x:'OFFLINE_DUMMY'),patch(g,AUDIT=audit),patch(l,AUDIT=audit,PRIVATE=priv,verify_live=public,collect=collect,gws=fake_gws,require_release_clearance=lambda:None):
   gate=p.gather('before_ledger',head,identifier)
   gate_accepted=False;append_verified=False;diagnostic=None
   try:
    g.reconcile(gate,'before_ledger',head,identifier,True);gate_accepted=True
    receipt=l.append_verified(head,identifier);append_verified=receipt['unique_target_and_DOI'] is True
   except RuntimeError as e:diagnostic=str(e)
   semantic=sum(('10.5281/zenodo.'+str(identifier))in urllib.parse.unquote(' '.join(row)).lower() for row in rows[1:])
   if label in {'canonical','encoded_slash','canonical_exempt'}:need(not gate_accepted and not calls,'recognized DOI must block wrong row')
   else:need(gate_accepted and append_verified and len(calls)==1 and semantic==2,'expected case/encoding counterexample '+repr((label,gate_accepted,append_verified,len(calls),semantic,diagnostic)))
   results.append({'label':label,'root_digest_exemption':label.endswith('_exempt'),'collector_match_rows':[r['row']for r in gate['ledger_matches']],'reconciliation_accepted':gate_accepted,'append_calls':len(calls),'append_claimed_unique':append_verified,'actual_normalized_same_DOI_rows':semantic,'diagnostic':diagnostic})
# Full account paginator, schema, freshness and binding controls use actual implementations.
controls=[]
class Pages:
 base='https://offline.invalid'
 def __init__(self,pages):self.pages=iter(pages)
 def request(self,m,u):need(m=='GET','GET only');return next(self.pages)
def record(i):return {'id':i,'metadata':{},'files':[]}
def page(records,total,next=None):return {'hits':{'hits':records,'total':total},'links':{'next':next}if next else{}}
c=p.account_search(Pages([page([record(1)],2,'https://offline.invalid/p2'),page([record(2)],2)]),'')
need(c['total']==2 and c['pages']==2,'actual pagination positive');controls.append({'label':'full_two_page_account','accepted':True})
for label,pages in [('duplicate_id',[page([record(1)],2,'https://offline.invalid/p2'),page([record(1)],2)]),('incomplete',[page([record(1)],2)]),('external_next',[page([record(1)],2,'https://evil.invalid/p2')]),('boolean_id',[page([record(True)],1)]),('inexact_total',[page([record(1)],{'value':1,'relation':'gte'})]),('missing_files',[page([{'id':1,'metadata':{}}],1)])]:controls.append(rejected(label,lambda pages=pages:p.account_search(Pages(pages),'')))
for label,rows in [('extra_column',[o.HEADERS,['a','','','','x']]),('wrong_header',[['A','B','C','D']]),('nonstring',[o.HEADERS,[1]])]:controls.append(rejected(label,lambda rows=rows:o.schema_rows({'values':rows})))
for label,when in [('expired',(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=181)).isoformat()),('future',(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=20)).isoformat()),('naive','2026-10-21T00:00:00')]:controls.append(rejected(label,lambda when=when:o.fresh(when)))
controls.append(rejected('missing_affirmative_root_clearance',o.require_release_clearance))
with tempfile.TemporaryDirectory(dir=P) as name:
 root=pathlib.Path(name);f=root/'x';f.write_bytes(b'ok');entry={'path':'x','bytes':2,'sha256':o.sha(b'ok')};need(o.verify_entries(root,[entry])=={'x'},'entry baseline')
 for label,e in [('bool_byte',{**entry,'bytes':True}),('escape_path',{**entry,'path':'../x'}),('wrong_sha',{**entry,'sha256':'0'*64})]:controls.append(rejected(label,lambda e=e:o.verify_entries(root,[e])))
 intent=root/'intent.json';o.intent_json(intent,{'a':1});controls.append(rejected('durable_intent_no_overwrite',lambda:o.intent_json(intent,{'a':2})))
 # Exercise the full integrated-tree verifier with an unlisted empty directory.
 originals=ri.originals();added={**originals,**{n:('100644','blob',ri.blob_sha(d))for n,d in ri.selection().items()}}
 base_commit='b'*40;new_commit='c'*40
 extra_empty={'mode':'040000','type':'tree','sha':'4b825dc642cb6eb9a060e54bf8d69288fbee4904'}
 def tree_fixture(commit,path,recursive=True):
  if path==o.PROBLEM:
   if commit==base_commit:return {}
   entries={n:dict(mode=sig[0],type=sig[1],sha=sig[2])for n,sig in added.items()}
   entries['preprint']={'mode':'040000','type':'tree','sha':'d'*40}
   entries['independent_reviews']={'mode':'040000','type':'tree','sha':'e'*40}
   entries['hidden_empty']=extra_empty
   return entries
  if path=='':return {'unsolved_math_prioritization':{'mode':'040000','type':'tree','sha':commit},'other':{'mode':'100644','type':'blob','sha':'f'*40}}
  if path=='unsolved_math_prioritization':return {'attempts':{'mode':'040000','type':'tree','sha':commit},'QUEUE.md':{'mode':'100644','type':'blob','sha':commit},'other':{'mode':'040000','type':'tree','sha':'f'*40}}
  if path=='unsolved_math_prioritization/attempts':return {'30001179':{'mode':'040000','type':'tree','sha':commit},'sibling':{'mode':'040000','type':'tree','sha':'f'*40}}
  raise RuntimeError('unexpected fixture subtree '+path)
 def blob_fixture(commit,path):return ri.BASELINE_ROW if commit in {base_commit,o.ORIGINAL_PARENT}else ri.DESIRED_ROW
 with patch(ri,subtree=tree_fixture,blob=blob_fixture,api=lambda endpoint:{'parents':[{'sha':o.ORIGINAL_PARENT}]}):
  tree_acceptance=ri.verify_integrated_tree(base_commit,new_commit,o.ORIGINAL)
 need(tree_acceptance['original_files']==11 and tree_acceptance['publication_files']==5,'full exact-overlay verifier accepted hidden empty tree')
 controls.append({'label':'full_verify_integrated_tree_accepts_unlisted_selected_empty_tree','observed':True,'unexpected_tree':o.PROBLEM+'/hidden_empty','tree_sha':extra_empty['sha'],'actual_verifier_receipt':tree_acceptance,'scope':'Full actual verify_integrated_tree with synthetic read-only Git tree/blob API boundaries, actual11 snapshot and5 frozen files. Leaves match while tree-entry inventory differs. No physical Git object/index/ref mutation.'})
# Independently exercise actual lifecycle per-mutation gates and actual public bytes/metadata verifier.
events=[]
class Delegate:
 def create(self,m):events.append('create');return {'id':999}
 def get(self,i):events.append('get');return {'id':i}
 def upload(self,b,e):events.append('upload');return {}
 def update(self,i,m):events.append('update');return {}
 def publish(self,i):events.append('publish');return {}
def life_gate(phase,h,i):events.append(('gate',phase,i));return {'started_utc':o.stamp()},{}
with patch(lc,require_release_clearance=lambda:None,collect=life_gate):
 c=lc.GuardedLifecycleClient('stage',head,delegate=Delegate());c.create(metadata);c.upload('offline',selected[0]);c.update(999,metadata)
 need([e for e in events if isinstance(e,tuple)]==[('gate','before_stage',None),('gate','before_stage',999),('gate','before_stage',999)],'fresh gate for each stage mutation')
 controls.append({'label':'independent_lifecycle_each_stage_mutation_gated','accepted':True})
 controls.append(rejected('lifecycle_second_allocation',lambda:c.create(metadata)))
 controls.append(rejected('stage_cannot_publish',lambda:c.publish(999)))
 d=lc.GuardedLifecycleClient('publish',head,999,delegate=Delegate());controls.append(rejected('publish_wrong_id',lambda:d.publish(998)));controls.append(rejected('publish_cannot_edit',lambda:d.update(999,metadata)));d.publish(999)
 need(events[-2:]==[('gate','before_publish',999),'publish'],'fresh publish gate before mutation');controls.append({'label':'independent_publish_gate_precedes_delegate','accepted':True})
with tempfile.TemporaryDirectory(dir=P) as name:
 root=pathlib.Path(name);(root/'PR_MERGE_VERIFIED.json').write_text(json.dumps({'merged':False}))
 with patch(lc,AUDIT=root,require_release_clearance=lambda:None,verify_destination=lambda:None):controls.append(rejected('lifecycle_requires_actual_merged_preservation',lambda:lc.run_action('stage',head)))
public_metadata=copy.deepcopy(metadata);public_metadata.pop('upload_type');public_metadata.pop('publication_type');public_metadata['resource_type']={'type':'publication','subtype':'preprint','title':'Preprint'};public_metadata['license']={'id':'cc-by-4.0'}
public_record={'id':identifier,'doi':'10.5281/zenodo.'+str(identifier),'metadata':public_metadata,'files':[{'key':e['name'],'size':e['size'],'checksum':'md5:'+e['md5']}for e in selected]}
inspection={'id':identifier,'state':'published','doi':public_record['doi'],'doi_url':'https://doi.org/'+public_record['doi'],'doi_resolution':{'http_status':200,'resolved_url':'https://zenodo.org/records/'+str(identifier)}}
downloads={e['name']:(e['path'].read_bytes(),200,'https://offline.invalid/'+e['name'])for e in selected}
need(vf.verify_public_record(identifier,metadata,selected,inspection,public_record,downloads,200)['all_public_file_bytes_match_reviewed'],'public verifier exact positive')
controls.append({'label':'independent_public_metadata_download_pdf_zip81_positive','accepted':True})
for key in metadata:
 mutant=copy.deepcopy(public_record)
 if key in {'upload_type','publication_type'}:mutant['metadata']['resource_type']['type'if key=='upload_type'else'subtype']='changed'
 elif key=='license':mutant['metadata']['license']['id']='changed'
 else:mutant['metadata'].pop(key)
 controls.append(rejected('public_missing_or_changed_intended_metadata_'+key,lambda mutant=mutant:vf.verify_public_record(identifier,metadata,selected,inspection,mutant,downloads,200)))
wrong=copy.deepcopy(downloads);n=selected[0]['name'];data,code,url=wrong[n];wrong[n]=(b'!'+data[1:],code,url)
controls.append(rejected('public_download_same_length_byte_change',lambda:vf.verify_public_record(identifier,metadata,selected,inspection,public_record,wrong,200)))
bad_inspection=copy.deepcopy(inspection);bad_inspection['doi_resolution']['http_status']=404
controls.append(rejected('public_requires_DOI200',lambda:vf.verify_public_record(identifier,metadata,selected,bad_inspection,public_record,downloads,200)))
(Q/('OPERATIONS_CONTROLS.optimized.json'if not __debug__ else 'OPERATIONS_CONTROLS.normal.json')).write_text(json.dumps({'scope':'Actual399 functions, all external boundaries replaced with offline fixtures; root clearance deliberately bypassed only for downstream append test; no real provider mutations.','doi_duplicate_counterexamples':results,'guard_controls':controls},indent=2)+'\n')
print(json.dumps({'status':'CONFIRMED_REPAIR_REQUIRED','doi_variants_tested':len(results),'duplicate_append_variants':sum(r['append_claimed_unique'] for r in results),'guard_controls':len(controls)}))

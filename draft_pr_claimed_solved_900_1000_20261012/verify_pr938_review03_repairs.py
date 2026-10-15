#!/usr/bin/env python3
"""Offline R6 regressions: synthetic fixtures, actual bounded logic, no service writes."""
import ast,copy,hashlib,importlib.util,json,os,re,shutil,sys,tempfile,types
from pathlib import Path
P=Path(__file__).resolve().parent;A=P/'audits/pr938_30003634';D=A/'publication';HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b';COMMIT='b'*40;REMOTE='c'*40
HELPERS=['accept_pr938.py','merge_pr938.py','run_pr938_zenodo.py','append_pr938_tracker.py','update_pr938_publication_ledger.py','finalize_pr938_and_gate_next.py']
def need(ok,label):
 if not ok:raise RuntimeError(label)
def load(p):return json.loads(p.read_text())
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def fp(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def mod(name):
 path=P/(name+'.py');m=types.ModuleType(name);m.__file__=str(path)
 if name=='update_pr938_publication_ledger' and sys.flags.optimize:
  # Verbatim pure definitions/constants only; never optimized operational use.
  tree=ast.parse(path.read_text());nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))];exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),m.__dict__)
 else:
  spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 return m
class StopBeforeWrite(Exception):pass
rows=[]
def rejected(label,call,fragment):
 try:call()
 except RuntimeError as error:
  need(fragment in str(error),label+' rejected for unrelated reason: '+str(error));rows.append({'case':label,'rejected':True,'reason':str(error)});return
 raise RuntimeError(label+' accepted adverse fixture')
def main():
 seal=A/'reviews/full_package_03/MANIFEST.json';need(fp(seal)['sha256']=='caa5253f9c0212cfbde804cc92b8705e59d59e0705d17cba7d8ac92a63ac1d13','Settled review03 seal')
 ac=mod('accept_pr938');ac.authenticate_review_records(seal.parent,load(seal));old=D/'reviewed_candidates/candidate03';ac.validate_review_evidence(seal.parent,load(seal.parent/'RESULT.json'),load(old/'PREPUBLICATION_FREEZE.json'),old)
 need(ac.HELPERS==HELPERS,'Six reviewed helper inventory')
 scratch=A/'private/review03_repairs';scratch.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(dir=scratch) as td:
  T=Path(td);Q=T/'publication';Q.mkdir();freeze=copy.deepcopy(load(D/'PREPUBLICATION_FREEZE.json'))
  for name in freeze['files']:
   dest=Q/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(D/name,dest)
  freeze['files']={n:fp(Q/n) for n in freeze['files']};freeze['future_helpers']={n:fp(P/n) for n in HELPERS};save(Q/'PREPUBLICATION_FREEZE.json',freeze);pin=fp(Q/'PREPUBLICATION_FREEZE.json')['sha256']
  acc={'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':pin,'files':freeze['files'],'future_helpers':freeze['future_helpers']};save(T/'ACCEPTANCE.json',acc)
  for name in ['PUBLICATION_DISPOSITION.json','ORIGINAL_SNAPSHOT.json','TARGET_IDENTITY_PREFLIGHT.json']:shutil.copyfile(A/name,T/name)
  source=load(A/'TARGET_IDENTITY_PREFLIGHT.json');catalog={'id':'30003634','present':True,'holds':[],'statement_hash':source['statement_hash'],'review_hash':source['review_hash']};snap=load(A/'ORIGINAL_SNAPSHOT.json');queue=(A/'GATED_QUEUE_ROW.md').read_text();body=(A/'PR_DESCRIPTION_CORRECTED.md').read_text()
  def actual_blob(ref,name):
   if name.endswith('catalog.json'):return json.dumps([catalog]).encode()
   if name.endswith('QUEUE.md'):return queue.encode()
   return (A/'original'/name).read_bytes()
  def merge_case(label,base,phase):
   m=mod('merge_pr938');m.A=T;calls=[];saves=[];view_count=[0]
   def pr(merged,base_):
    out={'number':938,'state':'MERGED' if merged else 'OPEN','isDraft':not merged,'headRefOid':HEAD,'body':body,'mergeCommit':{'oid':COMMIT}}
    if base_!='MISSING':out['baseRefName']=base_
    return out
   def fake_run(args):
    calls.append(args)
    if args[:3]==['gh','pr','view']:
     need('baseRefName' in args[-1],'Actual merge view omits baseRefName');view_count[0]+=1
     return json.dumps(pr(phase=='already' or view_count[0]>1,base if phase!='post' or view_count[0]>1 else 'main'))
    if args[:3]==['gh','api','repos/AlecKriebel/Math/pulls/938/files']:return '\n'.join(snap['files'])
    if args[:2]==['gh','api']:return queue
    if args[:2]==['git','ls-remote']:return REMOTE+' refs/heads/main\n'
    if args[:2]==['git','show']:return REMOTE+' '+HEAD+'\n'
    if args[:2]==['git','fetch'] or args[:2]==['git','merge-base'] or args[:3]==['gh','pr','ready']:return ''
    raise RuntimeError('Unmocked read '+repr(args))
   def fake_save(name,value):
    saves.append(name)
    if phase=='pre' or name=='PR_MERGE_RECEIPT.json':raise StopBeforeWrite(name)
   m.run=fake_run;m.rawblob=actual_blob;m.save=fake_save
   def fake_action(args,**kwargs):
    need(args[:3]==['gh','pr','merge'],'Only mocked merge action allowed');calls.append(args);return types.SimpleNamespace(returncode=0,stdout='',stderr='')
   m.subprocess=types.SimpleNamespace(run=fake_action)
   try:m.main()
   except StopBeforeWrite:
    need(base=='main',label+' reached write with wrong/missing destination');rows.append({'case':label,'positive_reaches_expected_local_boundary':True,'all_calls_mocked':True});return
   except RuntimeError as error:
    need(base!='main' and 'destination must remain exactly main' in str(error),label+' unrelated failure: '+str(error))
    if phase!='post':need(not saves and len(calls)==1,label+' adverse initial base reached save/action')
    else:need('PR_MERGE_RECEIPT.json' not in saves,label+' adverse postaction base accepted')
    rows.append({'case':label,'rejected':True,'all_calls_mocked':True,'final_merge_receipt_written':False});return
   raise RuntimeError(label+' did not stop at bounded boundary')
  for phase in ['pre','already','post']:
   for base in ['main','unreviewed-other-branch','MISSING',None,'']:merge_case('actual_merge_'+phase+'_'+str(base),base,phase)
  merged={'number':938,'state':'MERGED','headRefOid':HEAD,'baseRefName':'main','mergeCommit':{'oid':COMMIT}}
  z=mod('run_pr938_zenodo')
  for base in ['unreviewed-other-branch','MISSING',None,'']:
   record=copy.deepcopy(merged)
   if base=='MISSING':record.pop('baseRefName')
   else:record['baseRefName']=base
   rejected('publish_receipt_'+str(base),lambda record=record:z.require_main_merged_record(record,HEAD),'destination must be exactly main')
  z.require_main_merged_record(merged,HEAD,COMMIT);rows.append({'case':'publish_main_receipt_positive','passed':True})
  for bad in ['other',None,'MISSING']:
   fresh=copy.deepcopy(merged)
   if bad=='MISSING':fresh.pop('baseRefName')
   else:fresh['baseRefName']=bad
   def mocked_process(args,**kwargs):return types.SimpleNamespace(stdout=json.dumps(fresh))
   z.subprocess=types.SimpleNamespace(run=mocked_process)
   rejected('publish_actual_fresh_readback_'+str(bad),lambda:z.confirm_main_destination(merged,HEAD),'destination must be exactly main')
  for field,value in [('headRefOid','0'*40),('mergeCommit',{'oid':'0'*40}),('state','OPEN')]:
   fresh=copy.deepcopy(merged);fresh[field]=value;z.subprocess=types.SimpleNamespace(run=lambda *args,**kwargs:types.SimpleNamespace(stdout=json.dumps(fresh)))
   rejected('publish_fresh_'+field,lambda:z.confirm_main_destination(merged,HEAD),{'headRefOid':'accepted head','mergeCommit':'different merge commit','state':'destination must be exactly main'}[field])
  calls=[]
  def all_good_process(args,**kwargs):
   calls.append(args)
   if args[0]=='gh':return types.SimpleNamespace(stdout=json.dumps(merged))
   if args[:2]==['git','ls-remote']:return types.SimpleNamespace(stdout=REMOTE+' refs/heads/main\n')
   return types.SimpleNamespace(stdout='')
  z.subprocess=types.SimpleNamespace(run=all_good_process);destination=z.confirm_main_destination(merged,HEAD);need(calls[-1]==['git','merge-base','--is-ancestor',COMMIT,REMOTE],'Actual ancestry check absent');rows.append({'case':'publish_fresh_main_actual_readback_and_ancestry_mocked','passed':True})
  def failed_ancestry(args,**kwargs):
   if args[:2]==['git','merge-base']:raise RuntimeError('main ancestry rejected')
   return all_good_process(args,**kwargs)
  z.subprocess=types.SimpleNamespace(run=failed_ancestry);rejected('publish_merged_commit_not_on_main',lambda:z.confirm_main_destination(merged,HEAD),'main ancestry rejected')
  # Full actual receipt validators, including native evidence, not just a range function.
  desc=load(Q/'zenodo-deposit.json');files=[{'name':x['name'],'size':freeze['files'][x['path']]['bytes'],'sha256':freeze['files'][x['path']]['sha256']} for x in desc['files']];pub={'id':123,'state':'published','doi':'10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','files':files}
  intent={'action':'publish','pr':938,'accepted_freeze_sha256':pin,'merged_commit':COMMIT,'merged_base':'main','descriptor_sha256':fp(Q/'zenodo-deposit.json')['sha256'],'destination_readback':destination};save(Q/'ZENODO_PUBLISH_INTENT.json',intent);save(Q/'ZENODO_STAGE.json',pub);save(Q/'ZENODO_INSPECT.json',pub)
  tracker={'confirmed':True,'readback_matches':True,'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'merged_head':HEAD,'merged_base':'main','merge_commit':COMMIT,'accepted_freeze_sha256':pin,'doi':pub['doi'],'zenodo_record_id':123,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','gid':1254632077,'tab_title':'Math Puzzles','updated_range':"'Math Puzzles'!A10:D10",'row':['primary','','https://doi.org/'+pub['doi'],'SYNTHETIC fixture, never uploaded']};save(T/'TRACKER_READBACK.json',{'range':tracker['updated_range'],'values':[tracker['row']]})
  native={'push_confirmed':True,'published_event':{'id':'30003634','pr':938,'doi':pub['doi'],'original_pr_head':HEAD,'accepted_freeze_sha256':pin,'merged_commit':COMMIT,'merged_base':'main','zenodo_record_id':123,'evidence':{'tracker_range':tracker['updated_range']}}}
  for name in ['append_pr938_tracker','update_pr938_publication_ledger']:
   m=mod(name);m.verify_receipt_links(T,pub,merged,acc,tracker,native);rows.append({'case':name+'_complete_main_chain_positive','passed':True})
   for which in ['merge','intent','destination','fresh','tracker','native']:
    for base in ['other','MISSING']:
     mg=copy.deepcopy(merged);it=copy.deepcopy(intent);tr=copy.deepcopy(tracker);nt=copy.deepcopy(native)
     object_,key={'merge':(mg,'baseRefName'),'intent':(it,'merged_base'),'destination':(it['destination_readback'],'baseRefName'),'fresh':(it['destination_readback']['actual_PR_readback'],'baseRefName'),'tracker':(tr,'merged_base'),'native':(nt['published_event'],'merged_base')}[which]
     if base=='MISSING':object_.pop(key)
     else:object_[key]=base
     save(Q/'ZENODO_PUBLISH_INTENT.json',it)
     rejected(name+'_'+which+'_'+base,lambda m=m,mg=mg,tr=tr,nt=nt:m.verify_receipt_links(T,pub,mg,acc,tr,nt),'PR938 receipt linkage:')
   save(Q/'ZENODO_PUBLISH_INTENT.json',intent)
   for field,value in [('merge_commit','0'*40),('merge_commit_is_ancestor_of_observed_main',False),('observed_remote_main','bad')]:
    it=copy.deepcopy(intent);it['destination_readback'][field]=value;save(Q/'ZENODO_PUBLISH_INTENT.json',it);rejected(name+'_destination_'+field,lambda m=m:m.verify_receipt_links(T,pub,merged,acc,tracker,native),'ancestry linkage')
   save(Q/'ZENODO_PUBLISH_INTENT.json',intent)
  # Execute only actual native preflight statements up to (not including) catalog read.
  # This tests the current-main ancestry boundary without an operational writer.
  save(Q/'ZENODO_PUBLISH.json',pub);save(T/'TRACKER_RECEIPT.json',tracker);save(T/'PR_MERGE_RECEIPT.json',merged)
  native_tree=ast.parse((P/'update_pr938_publication_ledger.py').read_text());native_fn=next(n for n in native_tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');bounded=[]
  for node in native_fn.body:
   if isinstance(node,ast.For):
    for child in node.body:
     if isinstance(child,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='catalogue' for t in child.targets):break
     bounded.append(child)
    break
   bounded.append(node)
  code=compile(ast.fix_missing_locations(ast.Module(body=bounded,type_ignores=[])),'actual_bounded_native_destination_preflight','exec')
  for permitted in [True,False]:
   m=mod('update_pr938_publication_ledger');seen=[]
   def native_read(args):
    seen.append(args)
    if args[:2]==['git','ls-remote']:return REMOTE+' refs/heads/main\n'
    if args[:2]==['git','fetch']:return ''
    if args==['git','merge-base','--is-ancestor',COMMIT,REMOTE]:
     if not permitted:raise RuntimeError('current main ancestry rejected')
     return ''
    raise RuntimeError('Unmocked native call '+repr(args))
   ns=dict(m.__dict__,AUDIT=T,run=native_read)
   if permitted:
    exec(code,ns);need(seen[-1]==['git','merge-base','--is-ancestor',COMMIT,REMOTE],'Actual native ancestry guard missing');rows.append({'case':'native_actual_bounded_current_main_positive','passed':True})
   else:rejected('native_actual_bounded_current_main_not_ancestor',lambda:exec(code,ns),'current main ancestry rejected')
  f=mod('finalize_pr938_and_gate_next');raw=b'{"first" : {"nested":[1,{"x":"}"}]}, "30003634": {"turns_used":1}, "last": 7}\n';values=f.raw_json_values(raw);need(set(values)=={'first','30003634','last'} and values['first']=='"first" : {"nested":[1,{"x":"}"}]}','Finalizer literal nested parsing');rows.append({'case':'finalizer_raw_other_member_preservation_parser','passed':True})
 print(json.dumps({'status':'PASS','actual_parent_optimization':sys.flags.optimize,'cases':len(rows),'rows':rows,'synthetic_fixture_records_only':True,'all_service_Git_action_calls_mocked':True,'no_real_operational_actions':True,'review03_original_seal_unchanged':fp(seal)['sha256'],'six_helper_inventory':HELPERS,'new_proof_search_responses':0},indent=2))
if __name__=='__main__':main()

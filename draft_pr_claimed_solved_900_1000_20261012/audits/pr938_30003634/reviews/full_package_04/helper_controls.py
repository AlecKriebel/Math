"""Review04 independent pure and bounded actual-code controls; no operational mains."""
import ast,copy,hashlib,importlib.util,json,os,shutil,sys,types
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[3];A=R.parents[1];D=A/'publication';T=R/'private'/('controls_'+str(sys.flags.optimize)+'_'+os.environ.get('REVIEW_MODE','normal'));T.mkdir(parents=True,exist_ok=False);sys.dont_write_bytecode=True
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b';COMMIT='b'*40;REMOTE='c'*40
rows=[]
def need(x,s):
 if not x:raise RuntimeError(s)
def load(p):return json.loads(p.read_bytes())
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def fp(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(name):
 path=P/(name+'.py');m=types.ModuleType(name);m.__file__=str(path)
 if name=='update_pr938_publication_ledger' and sys.flags.optimize:
  tree=ast.parse(path.read_text());nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))];exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),m.__dict__)
 else:
  spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 return m
def positive(label,call):call();rows.append({'case':label,'passed':True})
def negative(label,call,fragment=None):
 try:call()
 except (RuntimeError,KeyError,ValueError,TypeError) as e:
  need(fragment is None or fragment in str(e),label+' unrelated rejection '+str(e));rows.append({'case':label,'rejected':True,'reason':str(e)});return
 raise RuntimeError(label+' was accepted')
ac=module('accept_pr938')
for n in [2,3,4]:positive('R1_R4_canonical_history_'+str(n),lambda n=n:ac.validate_review_sequence([f'{i:02d}:'+str(i)*64 for i in range(1,n+1)]))
for numbers in [['01'],['01','03'],['02','01'],['01','01'],['02','03'],['001','002'],['1','2'],['+1','02'],['01','002'],['01','02','04']]:negative('R1_R4_reject_'+repr(numbers),lambda numbers=numbers:ac.validate_review_sequence([i+':'+('a'*64) for i in numbers]))
for n in ['01','02','03']:
 folder=A/'reviews'/('full_package_'+n);positive('R2_genuine_sealed_'+n,lambda folder=folder:ac.authenticate_review_records(folder,load(folder/'MANIFEST.json')))
 old=D/'reviewed_candidates'/('candidate'+n);positive('R5_genuine_full_evidence_'+n,lambda folder=folder,old=old:ac.validate_review_evidence(folder,load(folder/'RESULT.json'),load(old/'PREPUBLICATION_FREEZE.json'),old))
manifest=load(A/'reviews/full_package_03/MANIFEST.json')
negative('R2_empty_inventory',lambda:ac.validate_review_inventory({'files':{},'explicit_public_allowlist':[]}))
for absent in ['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json']:
 bad=copy.deepcopy(manifest);bad['files'].pop(absent);bad['explicit_public_allowlist'].remove(absent);negative('R2_missing_'+absent,lambda bad=bad:ac.validate_review_inventory(bad))
F=T/'evidence';F.mkdir()
for n in ['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json']:shutil.copyfile(A/'reviews/full_package_03'/n,F/n)
minimal={'files':{n:fp(F/n) for n in [x.name for x in F.iterdir()]},'explicit_public_allowlist':sorted(x.name for x in F.iterdir())}
positive('R2_minimal_six_nonempty',lambda:ac.authenticate_review_records(F,minimal))
raw=(F/'RESULT.json').read_bytes();(F/'RESULT.json').write_text('{"clean_for_preprint":true}');negative('R2_unsealed_result_mutation',lambda:ac.authenticate_review_records(F,minimal));(F/'RESULT.json').write_bytes(raw)
for n in ['FULL_AUDIT.md','AUTHENTICATION_START.json','COLD_REPLAY.json']:
 raw=(F/n).read_bytes();(F/n).write_text('  \n');bad=copy.deepcopy(minimal);bad['files'][n]=fp(F/n);negative('R5_rebound_empty_'+n,lambda bad=bad:ac.authenticate_review_records(F,bad));(F/n).write_bytes(raw)
old=D/'reviewed_candidates/candidate03';result=load(F/'RESULT.json');oldfreeze=load(old/'PREPUBLICATION_FREEZE.json')
for name,path,value in [('start_head',['original_pr_head'],'0'*40),('start_freeze',['freeze_sha256'],'0'*64),('start_manifest',['package_manifest_sha256'],'0'*64),('start_count',['archive_members'],True),('start_payloads',['payloads'],0),('start_helper',['future_helpers','accept_pr938.py','sha256'],'0'*64),('start_original_size',['originals',next(iter(load(F/'AUTHENTICATION_START.json')['originals'])),'bytes'],True),('start_status',['status'],'FAIL'),('start_time',['utc'],'1900-01-01T00:00:00+00:00'),('end_mode',['originals',next(iter(load(F/'AUTHENTICATION_END.json')['originals'])),'disk_mode'],'0755'),('end_archive_mode',['originals',next(iter(load(F/'AUTHENTICATION_END.json')['originals'])),'archive_mode'],'100755'),('cold_mode',['modes',3,'observed_outer_optimization'],0),('cold_extraction',['cold_extraction'],False),('cold_verifier',['externally_pinned_verifier_sha256'],'0'*64),('cold_status',['status'],'FAIL'),('cold_receipt',['modes',0,'receipt','original_files_unchanged'],True)]:
 file='AUTHENTICATION_END.json' if name.startswith('end') else 'COLD_REPLAY.json' if name.startswith('cold') else 'AUTHENTICATION_START.json';raw=(F/file).read_bytes();data=load(F/file);obj=data
 for k in path[:-1]:obj=obj[k]
 obj[path[-1]]=value;save(F/file,data);negative('R5_'+name,lambda:ac.validate_review_evidence(F,result,oldfreeze,old));(F/file).write_bytes(raw)
for raw in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}']:negative('R5_strict_json_'+raw,lambda raw=raw:ac.strict_json(raw))
# Actual author worker comparator and call site.
spec=importlib.util.spec_from_file_location('review04_package',D/'verify_package.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
worker=ast.parse((D/'verify_package.py').read_text());need(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='equivalent' and len(n.args)>1 and isinstance(n.args[0],ast.Name) and n.args[0].id=='author' for n in ast.walk(worker)),'O1 actual worker call absent')
positive('O1_exact_author_summary',lambda:v.equivalent({'n':1,'m':3,'inertia':[23,25,0]},{'n':1,'m':3,'inertia':[23,25,0]}))
for val in [True,1.0]:negative('O1_wrong_n_type_'+repr(val),lambda val=val:v.equivalent({'n':val},{'n':1}))
negative('O1_nested_false_nullity',lambda:v.equivalent([23,25,False],[23,25,0]))
# Synthetic linked publication chain, exercising both complete validators.
Q=T/'publication';Q.mkdir();freeze=load(D/'PREPUBLICATION_FREEZE.json');shutil.copyfile(D/'PREPUBLICATION_FREEZE.json',Q/'PREPUBLICATION_FREEZE.json');pin=fp(Q/'PREPUBLICATION_FREEZE.json')['sha256']
for name in ['zenodo-deposit.json','deep-derived-pure-braids-source-verification-v1.0.zip','output/pdf/note.pdf']:
 dst=Q/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(D/name,dst)
acc={'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{}, {}, {}, {}],'freeze_sha256':pin,'files':freeze['files'],'future_helpers':freeze['future_helpers'],'proof_gap':None,'all_prior_required_and_optional_findings_resolved':True};save(T/'ACCEPTANCE.json',acc)
merged={'number':938,'state':'MERGED','headRefOid':HEAD,'baseRefName':'main','mergeCommit':{'oid':COMMIT}}
files=[{'name':i['name'],'size':freeze['files'][i['path']]['bytes'],'sha256':freeze['files'][i['path']]['sha256']} for i in load(Q/'zenodo-deposit.json')['files']]
pub={'id':123,'state':'published','doi':'10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','files':files}
destination={'baseRefName':'main','merge_commit':COMMIT,'observed_remote_main':REMOTE,'merge_commit_is_ancestor_of_observed_main':True,'actual_PR_readback':merged}
intent={'action':'publish','pr':938,'accepted_freeze_sha256':pin,'merged_commit':COMMIT,'merged_base':'main','descriptor_sha256':fp(Q/'zenodo-deposit.json')['sha256'],'destination_readback':destination}
tracker={'confirmed':True,'readback_matches':True,'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'merged_head':HEAD,'merged_base':'main','merge_commit':COMMIT,'accepted_freeze_sha256':pin,'doi':pub['doi'],'zenodo_record_id':123,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','gid':1254632077,'tab_title':'Math Puzzles','updated_range':"'Math Puzzles'!A10:D10",'row':['primary','','https://doi.org/'+pub['doi'],'SYNTHETIC private fixture only']}
native={'push_confirmed':True,'published_event':{'id':'30003634','pr':938,'doi':pub['doi'],'original_pr_head':HEAD,'accepted_freeze_sha256':pin,'merged_commit':COMMIT,'merged_base':'main','zenodo_record_id':123,'evidence':{'tracker_range':tracker['updated_range']}}}
for name,data in [('ZENODO_PUBLISH_INTENT.json',intent),('ZENODO_STAGE.json',pub),('ZENODO_INSPECT.json',pub),('ZENODO_PUBLISH.json',pub)]:save(Q/name,data)
save(T/'TRACKER_READBACK.json',{'range':tracker['updated_range'],'values':[tracker['row']]})
for module_name in ['append_pr938_tracker','update_pr938_publication_ledger']:
 m=module(module_name);positive('O2_R6_full_link_positive_'+module_name,lambda m=m:m.verify_receipt_links(T,pub,merged,acc,tracker,native))
 for badrange in ["'Other tab'!A10:D10","'Math Puzzles'!B10:E10","'Math Puzzles'!A10:D11","'Math Puzzles'!A1:D1","'Math Puzzles'!A0:D0","Math Puzzles!A10:D10","'Math Puzzles'!A010:D010"]:
  tr=copy.deepcopy(tracker);tr['updated_range']=badrange;negative('O2_range_'+module_name+'_'+badrange,lambda m=m,tr=tr:m.verify_receipt_links(T,pub,merged,acc,tr,native),'tracker')
 save(T/'TRACKER_READBACK.json',{'range':"'Math Puzzles'!A11:D11",'values':[tracker['row']]});negative('O2_actual_returned_readback_mismatch_'+module_name,lambda m=m:m.verify_receipt_links(T,pub,merged,acc,tracker,native),'range');save(T/'TRACKER_READBACK.json',{'range':tracker['updated_range'],'values':[tracker['row']]})
 for target in ['merged','intent','destination','actual','tracker','native']:
  for value in [None,'other']:
   mg=copy.deepcopy(merged);it=copy.deepcopy(intent);tr=copy.deepcopy(tracker);nt=copy.deepcopy(native);obj,key={'merged':(mg,'baseRefName'),'intent':(it,'merged_base'),'destination':(it['destination_readback'],'baseRefName'),'actual':(it['destination_readback']['actual_PR_readback'],'baseRefName'),'tracker':(tr,'merged_base'),'native':(nt['published_event'],'merged_base')}[target]
   if value is None:obj.pop(key)
   else:obj[key]=value
   save(Q/'ZENODO_PUBLISH_INTENT.json',it);negative('R6_'+module_name+'_'+target+'_'+str(value),lambda m=m,mg=mg,tr=tr,nt=nt:m.verify_receipt_links(T,pub,mg,acc,tr,nt),'PR938 receipt linkage:')
 save(Q/'ZENODO_PUBLISH_INTENT.json',intent)
 for target in ['doi','files','id','record_url']:
  bad=copy.deepcopy(pub);bad[target]={'doi':'10.5281/zenodo.999','files':files[::-1],'id':True,'record_url':'https://example.invalid'}[target];negative('complete_link_'+module_name+'_'+target,lambda m=m,bad=bad:m.verify_receipt_links(T,bad,merged,acc,tracker,native),'PR938 receipt linkage:')
# Bounded actual merge preflight, ending BEFORE intent/save/ready/action.
mm=module('merge_pr938');mm.A=T
for name in freeze['files']:
 dst=Q/name
 if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(D/name,dst)
for name in ['PUBLICATION_DISPOSITION.json','ORIGINAL_SNAPSHOT.json','TARGET_IDENTITY_PREFLIGHT.json']:shutil.copyfile(A/name,T/name)
body=(A/'PR_DESCRIPTION_CORRECTED.md').read_text();queue=(A/'GATED_QUEUE_ROW.md').read_text();snap=load(T/'ORIGINAL_SNAPSHOT.json');source=load(T/'TARGET_IDENTITY_PREFLIGHT.json')
fn=next(n for n in ast.parse((P/'merge_pr938.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main');prefix=[]
for node in fn.body:
 if isinstance(node,ast.If) and ast.unparse(node.test)=="pr['state'] != 'MERGED'":
  for child in node.body:
   if isinstance(child,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='intent' for t in child.targets):break
   prefix.append(child)
  break
 prefix.append(node)
code=compile(ast.fix_missing_locations(ast.Module(body=prefix,type_ignores=[])),'review04_actual_premerge_prefix','exec')
for base in ['main',None,'other']:
 for changed_body in [False,True]:
  pr={'number':938,'state':'OPEN','isDraft':True,'headRefOid':HEAD,'baseRefName':base,'body':body+'changed' if changed_body else body}
  calls=[]
  def read(args):
   calls.append(args)
   if args[:3]==['gh','pr','view']:
    need('body' in args[-1] and 'baseRefName' in args[-1],'actual requested fields');return json.dumps(pr)
   if args[:3]==['gh','api','repos/AlecKriebel/Math/pulls/938/files']:return '\n'.join(snap['files'])
   if args[:2]==['gh','api']:return queue
   if args[:2]==['git','fetch']:return ''
   if args[:2]==['git','ls-remote']:return REMOTE+' refs/heads/main\n'
   raise RuntimeError('Unmocked call '+repr(args))
  def raw(ref,name):
   if name.endswith('catalog.json'):return json.dumps([{'id':'30003634','present':True,'holds':[],'statement_hash':source['statement_hash'],'review_hash':source['review_hash']}]).encode()
   return (A/'original'/name).read_bytes()
  mm.run=read;mm.rawblob=raw;ns=dict(mm.__dict__)
  if base=='main' and not changed_body:positive('R3_R6_actual_premerge_valid',lambda:exec(code,ns))
  else:negative('R3_R6_actual_premerge_'+str(base)+'_'+str(changed_body),lambda:exec(code,ns),'destination' if base!='main' else 'description')
# Actual post-action interpretation statements, no ready/merge operation.
branch=next(n for n in fn.body if isinstance(n,ast.If) and ast.unparse(n.test)=="pr['state'] != 'MERGED'");post=[];collect=False
for node in branch.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='pr' for t in node.targets) and isinstance(node.value,ast.Call):collect=True
 if collect:post.append(node)
postcode=compile(ast.fix_missing_locations(ast.Module(body=post,type_ignores=[])),'review04_actual_post_merge_interpretation','exec')
for base in ['main',None,'other']:
 pr={'state':'MERGED','headRefOid':HEAD,'baseRefName':base};saved=[];ns=dict(mm.__dict__,view=lambda pr=pr:pr,save=lambda name,value:saved.append(name),expected_head=HEAD)
 if base=='main':positive('R6_actual_postaction_main',lambda:exec(postcode,ns))
 else:negative('R6_actual_postaction_'+str(base),lambda:exec(postcode,ns),'destination')
# Actual upload fresh readback/ancestry path, all subprocess calls intercepted.
z=module('run_pr938_zenodo')
for badfield,value in [('baseRefName','other'),('baseRefName',None),('headRefOid','0'*40),('mergeCommit',{'oid':'0'*40}),('state','OPEN')]:
 fresh=copy.deepcopy(merged);fresh[badfield]=value;z.subprocess=types.SimpleNamespace(run=lambda *a,**k:types.SimpleNamespace(stdout=json.dumps(fresh)))
 negative('R6_actual_upload_fresh_'+badfield+'_'+str(value),lambda:z.confirm_main_destination(merged,HEAD))
seen=[]
def upload_read(args,**kwargs):
 seen.append(args)
 if args[0]=='gh':return types.SimpleNamespace(stdout=json.dumps(merged))
 if args[:2]==['git','ls-remote']:return types.SimpleNamespace(stdout=REMOTE+' refs/heads/main')
 return types.SimpleNamespace(stdout='')
z.subprocess=types.SimpleNamespace(run=upload_read);positive('R6_actual_upload_main_and_ancestry',lambda:z.confirm_main_destination(merged,HEAD));need(seen[-1]==['git','merge-base','--is-ancestor',COMMIT,REMOTE],'upload ancestry')
def no_ancestor(args,**kwargs):
 if args[:2]==['git','merge-base']:raise RuntimeError('Mocked ancestry rejection')
 return upload_read(args,**kwargs)
z.subprocess=types.SimpleNamespace(run=no_ancestor);negative('R6_upload_nonancestor',lambda:z.confirm_main_destination(merged,HEAD),'Mocked ancestry rejection')
# Native non-index state replacement and exact three-path declaration.
lm=module('update_pr938_publication_ledger');raw='{ "other" : {"a": [1,2]}, "30003634" : {"x":1}, "last": false}\n';changed=lm.replace_entry(raw,'30003634',{'x':2});need('"other" : {"a": [1,2]}' in changed and '"last": false' in changed,'literal other state preservation');rows.append({'case':'native_exact_other_state_bytes','passed':True})
negative('native_tree_wrong_declared_paths',lambda:lm.explicit_tree(REMOTE,{'unrelated':'x'}),'replacement set')
# Current CAS parent ancestry: actual main prefix through the first loop guard only.
lfn=next(n for n in ast.parse((P/'update_pr938_publication_ledger.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main');bounded=[]
for n in lfn.body:
 if isinstance(n,ast.For):
  for child in n.body:
   if isinstance(child,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='catalogue' for t in child.targets):break
   bounded.append(child)
  break
 bounded.append(n)
for name,data in [('PR_MERGE_RECEIPT.json',merged),('TRACKER_RECEIPT.json',tracker)]:save(T/name,data)
lns=dict(lm.__dict__,AUDIT=T);lcode=compile(ast.fix_missing_locations(ast.Module(body=bounded,type_ignores=[])),'review04_actual_native_cas_prefix','exec')
for ancestral in [True,False]:
 seen=[]
 def nread(args):
  seen.append(args)
  if args[:2]==['git','ls-remote']:return REMOTE+' refs/heads/main'
  if args[:2]==['git','fetch']:return ''
  if args==['git','merge-base','--is-ancestor',COMMIT,REMOTE]:
   if not ancestral:raise RuntimeError('Mocked current parent lacks reviewed merge')
   return ''
  raise RuntimeError('Unmocked native operation')
 lns['run']=nread
 if ancestral:positive('R6_actual_current_CAS_parent_ancestry',lambda:exec(lcode,lns))
 else:negative('R6_actual_current_CAS_parent_nonancestor',lambda:exec(lcode,lns),'lacks reviewed merge')
result={'status':'PASS','actual_parent_optimization':sys.flags.optimize,'mode':os.environ.get('REVIEW_MODE'),'cases':len(rows),'rows':rows,'operational_mains_called':False,'service_and_Git_calls_mocked':True,'all_writes_in_review_private':True,'prior_nine_findings_independently_challenged':True}
print(json.dumps(result,indent=2))

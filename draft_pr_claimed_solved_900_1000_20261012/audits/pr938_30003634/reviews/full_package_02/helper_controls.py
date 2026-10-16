#!/usr/bin/env python3
"""Independent bounded offline gates. Never call an operational main."""
import ast,copy,datetime,hashlib,importlib.util,json,os,re,sys,tempfile,types
from pathlib import Path
O=Path(__file__).resolve().parent;A=O.parents[1];P=A.parents[1];D=A/'publication';HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b';PIN='75180bee0473fa3eaed6a8fdcf72695fea6646b49341979e753ccd4425ba5147'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def module(p):
 spec=importlib.util.spec_from_file_location('offline_'+p.stem,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def pure(p,names):
 tree=ast.parse(p.read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];need(len(nodes)==len(names),'missing functions');ns={'json':json,'hashlib':hashlib,'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns);return ns

def bounded(m,start,stop,args):
 tree=ast.parse(Path(m.__file__).read_text());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
 def isassign(n,name):return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)
 i=next(i for i,n in enumerate(main.body) if isassign(n,start));j=next(i for i,n in enumerate(main.body) if isassign(n,stop))
 nodes=copy.deepcopy(main.body[i:j]);nodes.append(ast.Return(ast.Call(ast.Name('locals',ast.Load()),[],[])))
 fn=ast.FunctionDef(name='bounded_gate',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=x) for x in args],kwonlyargs=[],kw_defaults=[],defaults=[]),body=nodes,decorator_list=[])
 ns=m.__dict__.copy();exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),m.__file__,'exec'),ns);return ns['bounded_gate'],ns

def reject(fn,*args):
 try:fn(*args)
 except (RuntimeError,ValueError,KeyError,TypeError):return True
 return False

accept=module(P/'accept_pr938.py');merge=module(P/'merge_pr938.py');verify=module(D/'verify_package.py');freeze=json.loads((D/'PREPUBLICATION_FREEZE.json').read_bytes())
root=O/'private/helper_fixtures';root.mkdir(parents=True,exist_ok=True)
# Authenticate adverse01 independently against external anchor, all16 leaves.
first=A/'reviews/full_package_01';raw=(first/'MANIFEST.json').read_bytes();need(sha(raw)=='37feff8cb31bbef2b7f41b98d8f34571923e7a89cb4c8f53226ccd2adf388a91','review01 seal');mapping=json.loads(raw);accept.authenticate_review_records(first,mapping)
validspec=lambda ns:[f'{n:02d}:'+('a'*64) for n in ns]
sequence={'canonical_valid':[],'rejected':[],'noncanonical_accepted':[]}
for ns in [[1,2],[1,2,3]]:accept.validate_review_sequence(validspec(ns));sequence['canonical_valid'].append(ns)
for ns in [[1,3],[2,1],[1,1],[1,2,4],[1]]:need(reject(accept.validate_review_sequence,validspec(ns)),'skipped review accepted');sequence['rejected'].append(ns)
for specs in [['001:'+('a'*64),'002:'+('a'*64)],['1:'+('a'*64),'002:'+('a'*64)]]:
 need(not reject(accept.validate_review_sequence,specs),'unexpected alias rejection');sequence['noncanonical_accepted'].append(specs)
# Execute precisely the actual review-only block with no external operations.
gate,ns=bounded(accept,'reviews','disposition',['args','freeze']);fixture=root/'reviews';ns['A']=fixture;ns['D']=fixture/'publication'
mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json'}
def make(label,index,issues=(),empty=False):
 folder=fixture/'reviews'/('full_package_'+label);folder.mkdir(parents=True,exist_ok=True)
 result={'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'clean_context':True,'candidate_revision':2,'full_reproducer_completed':True,'started_utc':f'2026-10-15T09:{index:02d}:00+00:00','completed_utc':f'2026-10-15T09:{index:02d}:30+00:00','candidate_pins':{'freeze':PIN,'manifest':freeze['package_manifest_sha256'],'pdf':freeze['files']['output/pdf/note.pdf']['sha256']},'inspected_helper_hashes':freeze['future_helpers'],'required_issues':list(issues),'optional_issues':[],'prior_issue_resolution':{'HIDDEN':{'verified':True}},'clean_for_preprint':not bool(issues),'mathematical_remaining_gap_for_stated_theorem':None}
 dump(folder/'RESULT.json',result)
 for name in mandatory-{'RESULT.json'}:(folder/name).write_text('' if empty else 'Offline fixture supporting record; not an actual review.\n')
 rec={name:accept.fp(folder/name) for name in sorted(mandatory)};dump(folder/'MANIFEST.json',{'files':rec,'explicit_public_allowlist':list(rec)})
 return label+':'+sha((folder/'MANIFEST.json').read_bytes())
def invoke(specs):
 accept.validate_review_sequence(specs);return gate(types.SimpleNamespace(review=specs,freeze=PIN),freeze)
canonical=[make('01',1),make('02',2)];need(len(invoke(canonical)['reviews'])==2,'valid full review chain')
canonical3=make('03',3);need(len(invoke(canonical+[canonical3])['reviews'])==3,'valid three chain')
# Previous R1 omission fails before the block; missing/unsealed R2 fails.
need(reject(invoke,[canonical[0],canonical3]),'earlier R1')
missing=copy.deepcopy(mapping);missing['files'].pop('RESULT.json');missing['explicit_public_allowlist'].remove('RESULT.json');need(reject(accept.validate_review_inventory,missing),'earlier R2 missing')
need(reject(accept.validate_review_inventory,{'files':{},'explicit_public_allowlist':[]}),'earlier R2 empty')
copydir=root/'tampered';copydir.mkdir(exist_ok=True)
for name in mapping['files']:
 q=copydir/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((first/name).read_bytes())
accept.authenticate_review_records(copydir,mapping);r=json.loads((copydir/'RESULT.json').read_bytes());r.update(clean_for_preprint=True,required_issues=[],optional_issues=[]);dump(copydir/'RESULT.json',r);need(reject(accept.authenticate_review_records,copydir,mapping),'earlier R2 tampering')
# New R4: actual canonical01 has unresolved HIDDEN. Alternate leading-zero
# directories are selected by zfill(2), bypassing the genuine canonical round.
make('01',1,[{'id':'HIDDEN','title':'Unresolved canonical issue'}]);make('02',2,[{'id':'HIDDEN','title':'Unresolved canonical issue'}]);aliases=[make('001',1),make('002',2)];bypass=invoke(aliases);need(bypass['prior_ids']==set() and bypass['latest']['clean_for_preprint'] is True,'alias counterexample')
# New R5: all mandatory names can be present while all five evidence files are empty.
empty=[make('01',1,empty=True),make('02',2,empty=True)];emptyresult=invoke(empty);need(emptyresult['latest']['clean_for_preprint'] is True,'empty evidence counterexample')
# Earlier R3 actual extracted preflight checks body in OPEN and MERGED states.
preflight,mns=bounded(merge,'decision','snapshot',[]);mfix=root/'merge';mns['A']=mfix
fb={'files':{},'pr_description_sha256':sha(b'reviewed body')};dump(mfix/'publication/PREPUBLICATION_FREEZE.json',fb);dump(mfix/'PUBLICATION_DISPOSITION.json',{'decision':'PREPARE_ALL_FINITE_DERIVED_DEPTH_RESEARCH_NOTE'});dump(mfix/'ACCEPTANCE.json',{'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':sha((mfix/'publication/PREPUBLICATION_FREEZE.json').read_bytes())})
bodyrows=[]
for state in ['OPEN','MERGED']:
 for body,expected in [('reviewed body',True),('changed',False),(None,False)]:
  mns['view']=lambda state=state,body=body:{'headRefOid':HEAD,'state':state,'isDraft':state=='OPEN','body':body}
  ok=not reject(preflight);need(ok is expected,'body gate');bodyrows.append({'state':state,'valid_body':expected,'accepted':ok})
fields=[];merge.run=lambda x:(fields.append(x[-1]) or '{}');merge.view();need('body' in fields[0].split(','),'actual view lacks body')
# Earlier O1 invoke actual recursive comparator and check worker calls it.
e={'n':1,'m':3,'goeritz_inertia':[23,25,0]};verify.equivalent(e,e)
for k,v in [('n',True),('m',3.0),('goeritz_inertia',[23,25,False])]:
 c=copy.deepcopy(e);c[k]=v;need(c==e and reject(verify.equivalent,c,e),'scalar confusion')
tree=ast.parse((D/'verify_package.py').read_text());need(any(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='equivalent' and len(x.args)>2 and isinstance(x.args[2],ast.Constant) and x.args[2].value=='original_author' for x in ast.walk(tree)),'worker not connected')
# Earlier O2 both actual pure functions and full duplicated receipt validators.
receipts=root/'receipts';pub=receipts/'publication';pub.mkdir(parents=True,exist_ok=True);files=[];f={'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'files':{}}
for name,b in [('note.pdf',b'fixturepaper'),('bundle.zip',b'fixturearchive')]:
 (pub/name).write_bytes(b);f['files'][name]={'bytes':len(b),'sha256':sha(b)};files.append({'name':name,'size':len(b),'sha256':sha(b)})
desc={'files':[{'path':n,'name':n} for n in ['note.pdf','bundle.zip']]};dump(pub/'zenodo-deposit.json',desc);f['files']['zenodo-deposit.json']={'bytes':(pub/'zenodo-deposit.json').stat().st_size,'sha256':sha((pub/'zenodo-deposit.json').read_bytes())};dump(pub/'PREPUBLICATION_FREEZE.json',f);fp=sha((pub/'PREPUBLICATION_FREEZE.json').read_bytes())
ac={'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':fp,'files':f['files']};me={'number':938,'state':'MERGED','headRefOid':HEAD,'mergeCommit':{'oid':'1'*40}};pu={'id':12345,'state':'published','doi':'10.5281/zenodo.12345','record_url':'https://zenodo.org/records/12345','files':files}
dump(pub/'ZENODO_PUBLISH_INTENT.json',{'action':'publish','pr':938,'accepted_freeze_sha256':fp,'merged_commit':'1'*40,'descriptor_sha256':f['files']['zenodo-deposit.json']['sha256']});dump(pub/'ZENODO_STAGE.json',{'id':12345,'files':files});dump(pub/'ZENODO_INSPECT.json',pu)
tr={'confirmed':True,'readback_matches':True,'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'merged_head':HEAD,'merge_commit':'1'*40,'accepted_freeze_sha256':fp,'doi':pu['doi'],'zenodo_record_id':12345,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','gid':1254632077,'tab_title':'Math Puzzles','row':['source','','https://doi.org/'+pu['doi'],'notes'],'updated_range':"'Math Puzzles'!A10:D10"}
range_rows=[]
for name in ['append_pr938_tracker.py','update_pr938_publication_ledger.py']:
 funcs=pure(P/name,{'valid_tracker_range','verify_receipt_links'});v=funcs['valid_tracker_range'];link=funcs['verify_receipt_links'];need(v(tr['updated_range']),'valid range');dump(receipts/'TRACKER_READBACK.json',{'range':tr['updated_range'],'values':[tr['row']]});link(receipts,pu,me,ac,tr)
 for bad in ["'Other tab'!A10:D10","'Math Puzzles'!B10:E10","'Math Puzzles'!A10:D11","'Math Puzzles'!A1:D1","'Math Puzzles'!A0:D0",None]:
  c=copy.deepcopy(tr);c['updated_range']=bad;need(not v(bad) and reject(link,receipts,pu,me,ac,c),'wrongrange accepted')
 dump(receipts/'TRACKER_READBACK.json',{'range':"'Math Puzzles'!A11:D11",'values':[tr['row']]});need(reject(link,receipts,pu,me,ac,tr),'readback range mismatch')
 range_rows.append({'helper':name,'valid_control':True,'wrong_ranges_rejected':6,'exact_readback_range_mismatch_rejected':True})
# Inspect the actual append/recovery bounded block without calling main or gws.
append=module(P/'append_pr938_tracker.py');ag,ans=bounded(append,'hits','receipt',['existing','row','doi','table']);saved=[];ans['save']=lambda *args:saved.append(args)
for mode in ['append','recovery']:
 row=['source','','https://doi.org/10.5281/zenodo.12345','notes'];existing={'values':[['Original Problem','Solution Chat URL','DOI','Notes']]+([row] if mode=='recovery' else [])}
 for rangebad in [False,True]:
  requests=[]
  def gws(args):
   requests.append(args);params=json.loads(args[args.index('--params')+1])
   if 'append' in args:return {'updates':{'updatedRange':"'Other tab'!A2:D2" if rangebad else "'Math Puzzles'!A2:D2",'updatedRows':1,'updatedCells':4}}
   return {'range':"'Other tab'!A2:D2" if rangebad else params['range'],'values':[row]}
  ans['gws']=gws;ok=not reject(ag,existing,row,'10.5281/zenodo.12345',"'Math Puzzles'!A:D");need(ok is (not rangebad),'append/recovery range failure')
# Selected-entry replacement preserves unrelated byte slices.
fn=pure(P/'update_pr938_publication_ledger.py',{'replace_entry'})['replace_entry'];raw='{\n "other" : {"spacing": 3},\n "30003634": {"turns_used": 1},\n "tail": [1,2]\n}\n';new=fn(raw,'30003634',{'turns_used':2});need(raw.split('"30003634"')[0]==new.split('"30003634"')[0] and raw[raw.index(',\n "tail"'):]==new[new.index(',\n "tail"'):],'state outside bytes changed')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_parent_optimization':sys.flags.optimize,'operational_mains_called':False,'mutations_private_only':True,'prior_R1_sequence':sequence,'prior_R2':{'missing_or_empty_inventory_rejected':True,'sealed_result_mutation_rejected':True,'review01_payloads_authenticated':len(mapping['files'])},'prior_R3':{'actual_view_requests_body':True,'preflight_cases':bodyrows},'prior_O1':{'valid_exact_control':True,'bool_float_nested_zero_controls_rejected':3,'actual_worker_uses_type_exact_comparator':True},'prior_O2':{'both_receipt_validators':range_rows,'actual_append_and_recovery_bounded_blocks_valid_and_negative_controls_pass':True},'new_R4':{'noncanonical_001_002_rounds_accepted':True,'unresolved_canonical_01_02_omitted':True,'selected_directories':['full_package_001','full_package_002'],'prior_ids_seen':sorted(bypass['prior_ids'])},'new_R5':{'all_six_names_authenticated':True,'five_mandatory_supporting_files_zero_bytes':True,'review_gate_accepts_clean_verdict':True},'selected_state_unrelated_bytes_preserved':True}
print(json.dumps(result,indent=2))

"""Synthetic private-fixture controls only; no provider/real journals/current views.
Modules are executed from exact copied sources; no function, module, or transport
is monkeypatched. The native observer is the model's ordinary injected interface.
"""
from pathlib import Path
import ast,base64,copy,hashlib,json,os,sys,tempfile,types
BASE=Path(__file__).absolute().parent
SOURCE=BASE.parent/"native_adoption_preparation_02"

def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def load(path):
 m=types.ModuleType(path.stem);m.__file__=str(path)
 exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m

def run():
 checks=[]
 def yes(value,label):
  if not value:raise RuntimeError(label)
  checks.append(label)
 def no(call,label):
  try:call()
  except (RuntimeError,ValueError,TypeError,KeyError,OSError):checks.append(label)
  else:raise RuntimeError('Expected refusal: '+label)
 with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as name:
  root=Path(name)/'checkout';program=root/'draft_pr_publication_program_20260930';case=program/'audits/pr210_5100033';d=case/'native_adoption_preparation_02';d.mkdir(parents=True)
  def write(path,raw):
   path.parent.mkdir(parents=True,exist_ok=True)
   if path.exists():path.chmod(0o644)
   path.write_bytes(raw);path.chmod(0o444)
  def enc(value):return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
  for filename in ('native210_model.py','native210_future_executor.py','native_trees_readonly.py','BASELINE_MEMBERSHIP.json','PROTECTED_NATIVE_REFERENCE.json'):
   write(d/filename,(SOURCE/filename).read_bytes())
  h=load(d/'native210_model.py');c=h.core();e=load(d/'native210_future_executor.py')
  baseline=json.loads((d/'BASELINE_MEMBERSHIP.json').read_bytes())
  post=h.phase_facts('adoption100');oldfacts=h.baseline_facts()
  yes(post['fully_completed_count']==52 and post['published_count']==36 and post['last_completed_PR']==210 and post['next_numeric_intake_cursor']==211 and post['goal_complete'] is False,'single_terminal52_36_210_211_goalFalse')
  review=json.loads((BASE.parent/'review_candidate_01/PUBLIC_REVIEW_MANIFEST.json').read_bytes())
  yes(all(h.public_payload_path(h.CASE+r['path']) for r in review['files']),'all127_exact_current_public_candidate_paths_supported')
  yes(len(h.PUBLIC_PINNED_EXCEPTIONS)==11,'only_eleven_fixed_path_and_body_exceptions')
  no(lambda:h.need(h.public_payload_path(h.CASE+'native_custody_01/archive/native_commits/'+('0'*40)+'.commit'),'unlisted'),'unlisted_native_commit_exception_refused')
  no(lambda:h.phase_facts('merge95'),'old_merge95_phase_refused')
  no(lambda:h.phase_facts('completion100'),'old_completion100_phase_refused')
  marker=h.phase_marker('adoption100')
  history=b'<!-- PR209_NATIVE_PHASE_FACTS historical95 -->\n<!-- PR209_NATIVE_PHASE_FACTS historical100 -->\n'
  h.markdown_current(history+marker+b'\n','adoption100',True);yes(True,'prior_PR209_markers_history_new_PR210_terminal_allowed')
  for raw,label in ((marker+b'\n'+marker+b'\n','duplicate'),(marker+b'\nafter\n','nonterminal'),(b'inline '+marker+b'\n','midline'),(b'<!-- PR210_NATIVE_PHASE_FACTS\t{} -->\n'+marker+b'\n','malformed_namespace')):
   no(lambda raw=raw:h.markdown_current(raw,'adoption100',True),'marker_'+label+'_refused')
  yes(not h.exact({'n':51},{'n':51.0}),'deep_JSON_numeric_type_guard')
  publicpaths=[h.CASE+'ROOT_SYNTHETIC_'+role+'.json' for role in ('scientific','priority','whole_package_one','whole_package_two','existing_publication','existing_tracker','custody','actual_prior209_completion','PR210_status_intake')]
  roles=dict(zip(('scientific','priority','whole_package_one','whole_package_two','existing_publication','existing_tracker','custody','actual_prior209_completion','PR210_status_intake'),publicpaths))
  bodies={p:enc({'synthetic_fixture_only':True,'role':role}) for role,p in roles.items()}
  case_native=b'synthetic native case log\n';case_local=case_native+b'synthetic current local45 note\n';prog_native=history+b'synthetic accepted209 program log\n'
  oldprogress={**oldfacts,'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs'],'published_PRs':baseline['published_PRs'],'dated_eligible_total':99}
  newprogress={**post,'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[210],'published_PRs':baseline['published_PRs']+[210],'dated_eligible_total':99}
  before_views={h.VIEWS[0]:enc({'synthetic_case45':True}),h.VIEWS[1]:case_native,h.VIEWS[2]:enc(oldprogress),h.VIEWS[3]:b'prior current synthetic document\n',h.VIEWS[4]:prog_native}
  bodies.update({h.VIEWS[0]:enc(post),h.VIEWS[1]:case_local+b'actual terminal proposal synthetic\n'+marker+b'\n',h.VIEWS[2]:enc(newprogress),h.VIEWS[3]:marker+b'\n',h.VIEWS[4]:prog_native+b'actual terminal proposal synthetic\n'+marker+b'\n'})
  objects={};blobs={};requests=[];overrides={};ref=[h.ANCHOR]
  def blob(raw):
   oid=c.native('blob',raw);blobs[oid]=raw;return oid
  def tree(rows):
   rows=sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''));oid=c.tree_hash(rows)
   objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':mode,'type':kind,'sha':sha} for n,mode,kind,sha in rows]};return oid
  def root_tree(leaves):
   trie={}
   for path,value in leaves.items():
    node=trie
    for part in path.split('/')[:-1]:node=node.setdefault(part,{})
    node[path.split('/')[-1]]=value
   def descend(node):return tree([(k,'040000','tree',descend(v)) if type(v) is dict else (k,*v) for k,v in node.items()])
   return descend(trie)
  queue=('100644','blob',blob(b'synthetic wholeQUEUE opaque\n'))
  leaves={p:('100644','blob',blob(raw)) for p,raw in before_views.items()}
  leaves.update({h.ATTEMPT[:-1]:('040000','tree',h.ATTEMPT_TREE),h.SHARED:('040000','tree',h.SHARED_TREE),h.QUEUE:queue,
   'foreign/empty':('040000','tree',tree([])),'foreign/executable':('100755','blob',blob(b'exec\n')),'foreign/symlink':('120000','blob',blob(b'target')),'foreign/gitlink':('160000','commit','9'*40)})
  parent_tree=root_tree(leaves)
  commitmeta={
   h.ORIGINAL:{'sha':h.ORIGINAL,'tree':{'sha':h.ORIGINAL_TREE},'parents':[{'sha':'462ac1846ea0abc36cb0e617d05c120351d943a0'}]},
   h.PREPARED:{'sha':h.PREPARED,'tree':{'sha':h.PREPARED_TREE},'parents':[{'sha':h.ORIGINAL},{'sha':h.MERGE_FIRST_PARENT}]},
   h.MERGED:{'sha':h.MERGED,'tree':{'sha':h.PREPARED_TREE},'parents':[{'sha':h.MERGE_FIRST_PARENT},{'sha':h.PREPARED}]},
   h.ANCHOR:{'sha':h.ANCHOR,'tree':{'sha':parent_tree},'parents':[{'sha':'8'*40}]}}
  pr={'number':210,'head':{'sha':h.PREPARED},'base':{'ref':'main'},'draft':False,'state':'closed','merged':True,'merge_commit_sha':h.MERGED,'merged_at':h.MERGED_AT}
  def observer(method,path,body=None):
   if method!='GET' or body is not None:raise RuntimeError('Synthetic GET-only observer')
   requests.append(path)
   if path in overrides:return copy.deepcopy(overrides[path])
   if path=='git/ref/heads/main':return {'object':{'sha':ref[0]}}
   if path=='pulls/210':return copy.deepcopy(pr)
   if path.startswith('compare/'):
    base=path.split('/')[1].split('...')[0];return {'status':'ahead','merge_base_commit':{'sha':base}}
   oid=path.rsplit('/',1)[-1]
   if path.startswith('git/trees/'):return copy.deepcopy(objects[oid])
   if path.startswith('git/commits/'):return copy.deepcopy(commitmeta[oid])
   if path.startswith('git/blobs/'):
    raw=blobs[oid];return {'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
   raise RuntimeError('Unexpected synthetic route')
  m={'schema':'pr210-native-adoption-inputs-v1','PR':210,'problem_id':'5100033','phase':'adoption100','helper_pin':pin((d/'native210_model.py').read_bytes()),'executor_pin':pin((d/'native210_future_executor.py').read_bytes()),'core_pin':h.CORE_PIN,'expected_parent':h.ANCHOR,'expected_parent_tree':parent_tree,'facts':post,'public_allowlist':sorted(publicpaths),'protected_queue':dict(zip(('mode','type','sha'),queue)),'reused_blobs':[],'reused_trees':[{'path':h.ATTEMPT[:-1],'mode':'040000','type':'tree','sha':h.ATTEMPT_TREE},{'path':h.SHARED,'mode':'040000','type':'tree','sha':h.SHARED_TREE}],'baseline_pin':h.BASELINE_PIN,'protected_reference_pin':h.PROTECTED_REFERENCE_PIN,'writer_lock':h.WRITER_LOCK_REFERENCE,'candidate_journal':'SYNTHETIC_NEVER_EXECUTED_CANDIDATE','commit_message':'Synthetic adoption test only\n','commit_author':{'name':'Synthetic','email':'synthetic@example.invalid','date':'2026-10-17T04:00:00Z'},'commit_committer':{'name':'Synthetic','email':'synthetic@example.invalid','date':'2026-10-17T04:00:00Z'}}
  m['files']=[]
  for i,(path,raw) in enumerate(sorted(bodies.items())):
   source='synthetic/selected'+str(i)+'.data';write(d/source,raw)
   before=leaves.get(path);m['files'].append({'path':path,'source':source,**pin(raw),'git_blob':blob(raw),'preimage':dict(zip(('mode','type','sha'),before)) if before else None})
  m['total_files']=len(bodies);m['total_bytes']=sum(map(len,bodies.values()));m['local_views']=[]
  for i,path in enumerate(h.VIEWS):
   raw=case_local if path==h.VIEWS[1] else before_views[path];source='synthetic/local'+str(i)+'.data';write(d/source,raw)
   m['local_views'].append({'path':path,'preimage':pin(raw),'source':source})
  for i in (1,2):write(d/('synthetic/audit'+str(i)+'.json'),enc({'synthetic_only':True,'reviewer':i}))
  def gate(mm,mp):
   return {'schema':'pr210-root-native-adoption-model-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','synthetic_fixture_only_not_authority':True,'PR':210,'phase':'adoption100','accepted':True,'manifest_pin':mp,'helper_pin':mm['helper_pin'],'executor_pin':mm['executor_pin'],'core_pin':h.CORE_PIN,'facts':post,'scientific_accepted':True,'priority_accepted':True,'whole_package_reviews_accepted':True,'existing_publication_verified':True,'existing_tracker_verified':True,'native_custody_accepted':True,'no_new_publication_or_tracker_action':True,'public_selection_reviewed':True,'original_PR_already_merged':True,'original_merge_commit':h.MERGED,'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,'prepared_tree':h.PREPARED_TREE,'native_audits':[{'path':'synthetic/audit'+str(i)+'.json',**pin((d/('synthetic/audit'+str(i)+'.json')).read_bytes()),'Root_accepted':True,'helper_pin':mm['helper_pin'],'executor_pin':mm['executor_pin'],'manifest_pin':mp} for i in (1,2)],'receipts':{role:{'path':path,**pin(bodies[path])} for role,path in roles.items()}}
  def loaded(mm=None,gg=None):
   mm=copy.deepcopy(m if mm is None else mm);raw=enc(mm);mp=pin(raw);write(d/'synthetic/inputs.json',raw)
   g=gate(mm,mp) if gg is None else gg;gr=enc(g);write(d/'synthetic/gate.json',gr)
   return h.load_inputs('synthetic/inputs.json',mp,'synthetic/gate.json',pin(gr))
  # Reviewed fixture declarations above are reused. These focused repair tests
  # are independently authored; exact source modules are never monkeypatched.
  import subprocess,fcntl
  observations=[]
  v1=ast.parse((SOURCE.parent/'native_adoption_preparation_01/native210_future_executor.py').read_bytes())
  v2=ast.parse((SOURCE/'native210_future_executor.py').read_bytes())
  oldnodes={n.name:n for n in v1.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
  newnodes={n.name:n for n in v2.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
  for node in oldnodes:
   if node not in ('API','candidate'):yes(ast.dump(oldnodes[node])==ast.dump(newnodes[node]),'unchanged_V1_AST_'+node)
  newcandidate=copy.deepcopy(newnodes['candidate'])
  yes(len(newcandidate.body)==2 and isinstance(newcandidate.body[1],ast.With),'candidate_entire_body_held_lock_scope')
  yes(ast.unparse(newcandidate.body[1].items[0].context_expr)=="WriterLock(m['writer_lock'])",'candidate_uses_manifest_pinned_original_WriterLock')
  guard=next(n for n in ast.walk(newcandidate) if isinstance(n,ast.FunctionDef) and n.name=='effect_guard')
  yes(ast.unparse(guard.body[0])=='lock.check()' and ast.unparse(guard.body[-1])=='lock.check()','guard_live_lock_check_entry_and_last_statement')
  newcandidate.body=newcandidate.body[:1]+newcandidate.body[1].body
  class StripOnlyLockChecks(ast.NodeTransformer):
   def visit_Expr(self,node):
    return None if isinstance(node.value,ast.Call) and ast.unparse(node.value.func)=='lock.check' else self.generic_visit(node)
  newcandidate=StripOnlyLockChecks().visit(newcandidate)
  yes(ast.dump(newcandidate)==ast.dump(oldnodes['candidate']),'candidate_AST_equals_V1_after_only_scope_checks_removed')
  api=copy.deepcopy(newnodes['API']);newcall=next(n for n in api.body if isinstance(n,ast.FunctionDef) and n.name=='__call__');oldcall=next(n for n in oldnodes['API'].body if isinstance(n,ast.FunctionDef) and n.name=='__call__')
  def argv_index(node):return next(i for i,n in enumerate(node.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='argv' for t in n.targets))
  ni,oi=argv_index(newcall),argv_index(oldcall);newcall.body[ni:ni+1]=copy.deepcopy(oldcall.body[oi:oi+2])
  yes(ast.dump(api)==ast.dump(oldnodes['API']),'API_AST_equals_V1_after_only_argv_replacement_removed')
  yes((SOURCE/'native210_model.py').read_bytes()==(SOURCE.parent/'native_adoption_preparation_01/native210_model.py').read_bytes(),'model_bytes_unchanged')
  yes((SOURCE/'native_trees_readonly.py').read_bytes()==(SOURCE.parent/'native_adoption_preparation_01/native_trees_readonly.py').read_bytes(),'core_bytes_unchanged')
  priorhost=os.environ.get('GH_HOST');os.environ['GH_HOST']='hostile.example.invalid'
  try:
   routes=[('GET','git/ref/heads/main',False),('GET','pulls/210',False),('GET','git/commits/'+'1'*40,False),('GET','git/trees/'+'1'*40,False),('GET','git/blobs/'+'1'*40,False),('GET','compare/'+'1'*40+'...'+'2'*40,False),('POST','git/blobs',True),('POST','git/trees',True),('POST','git/commits',True)]
   for method,path,hasbody in routes:
    expected=[e.GH,'api','--hostname','github.com','--method',method,'repos/AlecKriebel/Math/'+path]+(['--input','-'] if hasbody else [])
    yes(e.api_argv(method,path,hasbody)==expected,'canonical_host_exact_argv_'+method+'_'+path)
  finally:
   if priorhost is None:os.environ.pop('GH_HOST',None)
   else:os.environ['GH_HOST']=priorhost
  # One selected public receipt is a real serialized binary fixture, so the
  # candidate exercises blob, tree and commit effect guards without transport.
  binarypath=roles['scientific'];binaryraw=b'\0owned synthetic binary\xff'
  binaryraw=bytes([0])+b'owned synthetic binary'+bytes([255])
  bodies[binarypath]=binaryraw;row=next(r for r in m['files'] if r['path']==binarypath);write(d/row['source'],binaryraw);row.update(**pin(binaryraw),git_blob=blob(binaryraw));m['total_bytes']=sum(map(len,bodies.values()))
  cc,mm,overlay,pre,reused=loaded();yes(overlay[binarypath]==binaryraw,'actual_serialized_model_load_accepts_exact_binary_public_fixture')
  for row in mm['local_views']:write(root/row['path'],(d/row['source']).read_bytes())
  lockpath=program/'ROOT_GLOBAL_FIVE_WRITER.lock'
  def probe(path):
   code='import os,sys,fcntl; fd=os.open(sys.argv[1],os.O_RDONLY);\ntry: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)\nexcept BlockingIOError: sys.exit(7)\nelse: sys.exit(0)'
   code=code.replace('\\n','\n')
   return subprocess.run([sys.executable,'-E','-S','-B','-P','-c',code,str(path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False).returncode
  class StopBeforeRealCommit(RuntimeError):pass
  modes={'absent':0,'competing':0,'replace_at_last_guard_read':0,'modify_at_last_guard_read':0,'replace_after_blob':1,'modify_after_blob':1,'replace_after_tree':2,'held_through_commit_boundary':3}
  for mode,expectedposts in modes.items():
   write(lockpath,e.LOCK_BYTES);st=lockpath.stat();fixturelock={'path':h.WRITER_LOCK_REFERENCE['path'],'device':st.st_dev,'inode':st.st_ino,**pin(e.LOCK_BYTES)}
   bad=copy.deepcopy(m);bad['writer_lock']=fixturelock
   no(lambda bad=bad:loaded(bad),'production_model_rejects_fixture_lock_substitution_'+mode)
   # Restore exact serialized fixture; only the ordinary behavioral loader below
   # substitutes the owned disposable lock identity. Production sources unchanged.
   cc,mm,overlay,pre,reused=loaded()
   fixture_m={**mm,'writer_lock':fixturelock,'candidate_journal':'OWNED_V2_'+mode.upper()};journal=e.journal_new(fixture_m['candidate_journal'])
   alias=program/('original_'+mode+'.lock');os.link(lockpath,alias)
   loads=[0];posts=[];mainreads=[0];competitor=None
   def fixture_load():
    loads[0]+=1
    return cc,fixture_m,overlay,pre,reused
   def mutate(which):
    if which=='replace':lockpath.unlink();write(lockpath,e.LOCK_BYTES)
    else:write(lockpath,b'owned fixture corrupt payload')
   def injected_api(method,path,body=None,expected_oid=None):
    if method=='POST':
     posts.append(path)
     yes(probe(alias)==7,'original_inode_OS_flock_held_'+mode+'_POST'+str(len(posts)))
     yes(loads[0]>=3,'fresh_loads_before_POST_'+mode+'_'+str(len(posts)))
     yes(path==('git/blobs' if len(posts)==1 else 'git/trees' if len(posts)==2 else 'git/commits'),'expected_effect_sequence_'+mode+'_'+str(len(posts)))
     if path=='git/commits':raise StopBeforeRealCommit('Stop before any provider transport')
     if mode in ('replace_after_blob','modify_after_blob') and path=='git/blobs':mutate('replace' if mode.startswith('replace') else 'modify')
     if mode=='replace_after_tree' and path=='git/trees':mutate('replace')
     return {'sha':expected_oid}
    answer=observer(method,path,body)
    if path=='git/ref/heads/main':
     mainreads[0]+=1
     if mainreads[0]==4 and mode in ('replace_at_last_guard_read','modify_at_last_guard_read'):mutate('replace' if mode.startswith('replace') else 'modify')
    return answer
   if mode=='absent':lockpath.unlink()
   if mode=='competing':competitor=os.open(alias,os.O_RDONLY);fcntl.flock(competitor,fcntl.LOCK_EX|fcntl.LOCK_NB)
   caught=None
   try:e.candidate(h,fixture_load,injected_api,journal)
   except (RuntimeError,OSError) as error:caught={'type':type(error).__name__,'message':str(error)}
   else:raise RuntimeError('Unexpected candidate completion')
   finally:
    if competitor is not None:fcntl.flock(competitor,fcntl.LOCK_UN);os.close(competitor)
   yes(len(posts)==expectedposts,'failclosed_exact_POST_count_'+mode)
   if mode=='held_through_commit_boundary':yes(caught['type']=='StopBeforeRealCommit','held_through_commit_stopped_before_real_transport')
   if mode not in ('held_through_commit_boundary','absent','competing'):yes('Pinned stable lock inode/payload changed' in caught['message'],'actual_lock_guard_exception_'+mode)
   yes(probe(alias)==0,'original_inode_OS_flock_released_on_exit_'+mode)
   observations.append({'mode':mode,'injected_POST_boundaries':posts,'all_provider_requests_intercepted_without_dispatch':True,'exception':caught,'original_inode_release_probed_by_retained_hardlink':True})
  # No API instance is allowed to reach run_bounded. API's exact new argv call is
  # established by the AST delta and pure-helper tests above. All sources exact.
 return {'schema':'pr210-native-adversary02-v2-repair-controls-v1','status':'PASS_SOURCE_REPAIR_CONTROLS_ONLY','checks':checks,'check_count':len(checks),'inherited_fixture_setup_checks':12,'new_independent_check_count':len(checks)-12,'observations':observations,'source_pins':{n:pin((SOURCE/n).read_bytes()) for n in ('native210_model.py','native210_future_executor.py','native_trees_readonly.py')},'fixture_declarations_adapted_from_reviewed_preparation_fixture':True,'no_source_function_module_or_transport_monkeypatches':True,'provider_calls':0,'real_objects_refs_live_locks_current_views_Root_gates_or_target_sources_modified':False,'temporary_owned_fixtures_deleted':True,'actual_acceptance_inferred':False}
if __name__=='__main__':
 if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Use python3 -E -S -B -P')
 print(json.dumps(run(),sort_keys=True,indent=2))

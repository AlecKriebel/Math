"""Independent bounded PR211 operational-source controls, not an operational gate.
Run with python3 -E -S -B -P. Only this directory's TemporaryDirectory is written.
External immutable dependencies are read/pinned; ten private bodies stay in memory.
The preparation's offline_selftest.py is inspected and hashed but never executed.
No live transport, Git, original writer lock or current-five operation is used.
"""
from pathlib import Path
import ast,base64,copy,difflib,hashlib,json,os,stat,subprocess,sys,tempfile,types
from datetime import datetime,timezone
HERE=Path(__file__).absolute().parent
SOURCE=HERE.parent/'native_adoption_preparation_01'
OLD=HERE.parent.parent/'pr210_5100033/native_adoption_preparation_02'
CUSTODY=HERE.parent/'native_custody_01'
CHECKS=[]
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(x):return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def yes(x,label):
 if type(x) is not bool or not x:raise RuntimeError(label)
 CHECKS.append(label)
def no(call,label):
 try:call()
 except (RuntimeError,ValueError,TypeError,KeyError,OSError):CHECKS.append(label)
 else:raise RuntimeError('Unexpected acceptance: '+label)
def module(p):
 m=types.ModuleType(p.stem);m.__file__=str(p)
 exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def write(p,raw):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():p.chmod(0o644)
 p.write_bytes(raw);p.chmod(0o444)
def run():
 source_manifest={'bytes':3249,'sha256':'fb63e96b9c8f3874b0c171a73ff94455a325a954dd6cb6a68e2cbff4397f1c9e'}
 yes(pin((SOURCE/'SOURCE_MANIFEST.json').read_bytes())==source_manifest,'exact_frozen_source_manifest')
 sm=json.loads((SOURCE/'SOURCE_MANIFEST.json').read_bytes())
 yes(sm['file_count']==17 and sm['total_bytes']==169973 and len(sm['files'])==17,'finite17_source_closure')
 for r in sm['files']:
  p=SOURCE/r['path'];s=p.lstat()
  yes(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and pin(p.read_bytes())=={k:r[k] for k in ('bytes','sha256')},'source_pin_'+r['path'])
 provenance=json.loads((SOURCE/'AUDITED_SOURCE_PROVENANCE.json').read_bytes())
 for r in provenance['inherited_source_inputs']:
  p=HERE.parents[2]/r['path']
  yes(pin(p.read_bytes())=={k:r[k] for k in ('bytes','sha256')},'provenance_pin_'+r['path'])
 for stem,delta in (('model','ADAPTATION_MODEL_DELTA.patch'),('future_executor','ADAPTATION_EXECUTOR_DELTA.patch')):
  old=(OLD/('native210_'+stem+'.py')).read_text();new=(SOURCE/('native211_'+stem+'.py')).read_text()
  actual=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='accepted210v2/native210_'+stem+'.py',tofile='PR211/native211_'+stem+'.py'))
  yes(actual==(SOURCE/delta).read_text(),'recomputed_exact_'+delta)
 yes((OLD/'native_trees_readonly.py').read_bytes()==(SOURCE/'native_trees_readonly.py').read_bytes(),'canonical_core_byte_identical')
 class Normalize(ast.NodeTransformer):
  def visit_Constant(self,n):
   if type(n.value) is str:n.value=n.value.replace('PR210','PR211').replace('pr210','pr211').replace('pulls/210','pulls/211').replace('native210','native211')
   elif type(n.value) is int and n.value==210:n.value=211
   return n
  def visit_Assign(self,n):
   return None if any(isinstance(t,ast.Name) and t.id=='MODEL_PIN' for t in n.targets) else self.generic_visit(n)
 yes(ast.dump(Normalize().visit(ast.parse((OLD/'native210_future_executor.py').read_bytes())))==ast.dump(Normalize().visit(ast.parse((SOURCE/'native211_future_executor.py').read_bytes()))),'whole_executor_AST_equal_under_declared_normalization_only')
 # All executed sources are exact copies under this directory; production paths stay readonly.
 with tempfile.TemporaryDirectory(prefix='_owned_fixture_',dir=HERE) as tmp:
  checkout=Path(tmp)/'checkout';d=checkout/'draft_pr_publication_program_20260930/audits/pr211_5100063/native_adoption_preparation_01'
  for n in ('native211_model.py','native211_future_executor.py','native_trees_readonly.py','BASELINE_MEMBERSHIP.json','PROTECTED_NATIVE_REFERENCE.json'):
   write(d/n,(SOURCE/n).read_bytes())
  h=module(d/'native211_model.py');c=h.core();e=module(d/'native211_future_executor.py')
  yes(e.MODEL_PIN==pin((SOURCE/'native211_model.py').read_bytes()),'executor_model_crosspin_exact')
  ref=json.loads((d/'PROTECTED_NATIVE_REFERENCE.json').read_bytes())
  trees=json.loads((CUSTODY/'FINAL_NATIVE_TREES_SUPPLEMENT.json').read_bytes())
  yes(len(trees)==65 and all(c.tree_hash([(k,v['mode'],v['type'],v['sha']) for k,v in rows.items()])==oid for oid,rows in trees.items()),'all65_authenticated_custody_trees_canonical')
  snap=json.loads((CUSTODY/'NATIVE_SNAPSHOTS.json').read_bytes())
  for key,oid,treeoid,parents in (
   ('original',h.ORIGINAL,h.ORIGINAL_TREE,['a3bdcb55173cb41866a58aded968b68d6a14d1a4']),
   ('revised',h.PREPARED,h.PREPARED_TREE,[h.ORIGINAL,h.PREPARED_SECOND_PARENT]),
   ('merge',h.MERGED,h.MERGED_TREE,[h.MERGE_FIRST_PARENT,h.PREPARED])):
   z=snap['commits'][key]
   yes(z['sha']==oid and z['tree']['sha']==treeoid and [x['sha'] for x in z['parents']]==parents,'custody_native_root_ordered_parents_'+key)
  for path,pp in json.loads((SOURCE/'PUBLIC_CUSTODY_PINNED_EXCEPTIONS.json').read_bytes()).items():
   raw=(HERE.parent/path).read_bytes()
   yes(pin(raw)==pp and h.native('commit',raw)==Path(path).stem,'fixed_raw_commit_'+Path(path).stem)
  for tr in ref['authenticated_tree_path_trace']:
   yes(trees[tr['tree']][tr['name']]=={k:tr[k] for k in ('mode','type','sha')},'authenticated_reference_trace_'+tr['name'])
  def lookup(oid,path):
   value=None
   for part in path.split('/'):
    value=trees[oid][part];oid=value['sha']
   return value
  yes(lookup(ref['observed_custody_tree'],h.ATTEMPT[:-1])['sha']==h.ATTEMPT_TREE,'current44_whole_tree_reference')
  yes(lookup(ref['observed_custody_tree'],h.SHARED)['sha']==h.SHARED_TREE,'current633_old_audit_whole_tree_reference')
  old=trees[ref['merge_preprint_tree']];cur=trees[ref['current_preprint_tree']]
  yes(ref['prepared_preprint_tree']==ref['merge_preprint_tree'] and ref['whole_preprint_tree_stability'] is False and [k for k in sorted(set(old)|set(cur)) if old.get(k)!=cur.get(k)]==['RESEARCH_LOG.md'],'qualified_prepared_merge_preprint_equal_current_log_drift_only')
  fixture=json.loads((SOURCE/'SELFTEST_FIXTURE_INPUTS.json').read_bytes())
  private={}
  for r in fixture['files']:
   raw=(CUSTODY/r['path']).read_bytes()
   yes(pin(raw)=={k:r[k] for k in ('bytes','sha256')},'private_fixture_pin_'+Path(r['path']).name)
   private[r['path']]=raw
  for r in ref['critical_blobs']:
   raw=private['private_reading/current_MAIN_preprint/'+r['path']]
   yes(pin(raw)=={k:r[k] for k in ('bytes','sha256')} and h.native('blob',raw)==r['sha'] and lookup(ref['observed_custody_tree'],r['path'])=={k:r[k] for k in ('mode','type','sha')},'ten_path_and_full_body_binding_'+Path(r['path']).name)
  base=json.loads((d/'BASELINE_MEMBERSHIP.json').read_bytes());facts=h.phase_facts('adoption100')
  yes(len(base['fully_completed_eligible_PRs'])==52 and len(base['published_PRs'])==36 and all(211 not in base[k] for k in ('fully_completed_eligible_PRs','published_PRs')),'exact_current52_36_memberships_exclude211')
  yes(facts=={'active_PR':211,'case_workflow_estimate_percent':100,'fully_completed_count':53,'published_count':37,'last_completed_PR':211,'next_numeric_intake_cursor':212,'advance_to_next_PR_authorized_now':True,'completed':True,'publication_ready':True,'goal_complete':False},'prospective53_37_211_212_goalFalse_only')
  for phase in ('merge95','completion100','planned100','adoption99'):no(lambda phase=phase:h.phase_facts(phase),'unsupported_phase_'+phase)
  role_names=('scientific','priority','whole_package_one','whole_package_two','existing_publication','existing_tracker','custody','actual_prior210_completion','PR211_status_intake')
  role_paths={r:h.CASE+'ROOT_SYNTHETIC_'+r+'.json' for r in role_names}
  bodies={p:enc({'synthetic_only_never_authority':r}) for r,p in role_paths.items()}
  marker=h.phase_marker('adoption100');history=b'<!-- PR210_NATIVE_PHASE_FACTS historical95 -->\n<!-- PR210_NATIVE_PHASE_FACTS historical100 -->\n'
  oldprogress={**h.baseline_facts(),**base}
  before={h.VIEWS[0]:enc({'synthetic_case40':True}),h.VIEWS[1]:b'native case log\n',h.VIEWS[2]:enc(oldprogress),h.VIEWS[3]:b'old current markdown\n',h.VIEWS[4]:history+b'native program log\n'}
  localbefore={**before,h.VIEWS[1]:before[h.VIEWS[1]]+b'separate local case40 history\n'}
  bodies.update({h.VIEWS[0]:enc(facts),h.VIEWS[1]:localbefore[h.VIEWS[1]]+marker+b'\n',h.VIEWS[2]:enc({**facts,'dated_eligible_total':99,'fully_completed_eligible_PRs':base['fully_completed_eligible_PRs']+[211],'published_PRs':base['published_PRs']+[211],'fully_completed_fraction_percent':5300/99}),h.VIEWS[3]:marker+b'\n',h.VIEWS[4]:before[h.VIEWS[4]]+marker+b'\n'})
  objects={};blobs={};requests=[];overrides={};main=[h.ANCHOR]
  def blob(raw):
   oid=h.native('blob',raw);blobs[oid]=raw;return oid
  def tree(rows):
   rows=sorted(rows,key=lambda x:x[0].encode()+(b'/' if x[1]=='040000' else b''))
   oid=c.tree_hash(rows);objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':m,'type':t,'sha':s} for n,m,t,s in rows]};return oid
  def root_tree(leaves):
   trie={}
   for p,v in leaves.items():
    node=trie
    for part in p.split('/')[:-1]:node=node.setdefault(part,{})
    node[p.split('/')[-1]]=v
   def build(node):return tree([(k,'040000','tree',build(v)) if type(v) is dict else (k,*v) for k,v in node.items()])
   return build(trie)
  for oid in (h.SHARED_TREE,ref['current_preprint_tree']):tree([(k,v['mode'],v['type'],v['sha']) for k,v in trees[oid].items()])
  for r in ref['critical_blobs']:blob(private['private_reading/current_MAIN_preprint/'+r['path']])
  queue=('100644','blob',blob(b'whole QUEUE including opaque foreign content\n'))
  leaves={p:('100644','blob',blob(raw)) for p,raw in before.items()}
  leaves.update({h.ATTEMPT[:-1]:('040000','tree',h.ATTEMPT_TREE),h.SHARED:('040000','tree',h.SHARED_TREE),h.QUEUE:queue,'foreign/empty':('040000','tree',tree([])),'foreign/executable':('100755','blob',blob(b'exec')),'foreign/symlink':('120000','blob',blob(b'target')),'foreign/gitlink':('160000','commit','9'*40)})
  parent_tree=root_tree(leaves)
  commits={v['sha']:copy.deepcopy(v) for v in snap['commits'].values()}
  commits[h.ANCHOR]={'sha':h.ANCHOR,'tree':{'sha':parent_tree},'parents':[{'sha':'8'*40}]}
  pr=copy.deepcopy(snap['PR'])
  def observer(method,path,body=None):
   if method!='GET' or body is not None:raise RuntimeError('Only injected GET observer permitted')
   requests.append(path)
   if path in overrides:return copy.deepcopy(overrides[path])
   if path=='git/ref/heads/main':return {'object':{'sha':main[0]}}
   if path=='pulls/211':return copy.deepcopy(pr)
   if path.startswith('compare/'):return {'status':'ahead','merge_base_commit':{'sha':path.split('/')[1].split('...')[0]}}
   oid=path.rsplit('/',1)[-1]
   if path.startswith('git/trees/'):return copy.deepcopy(objects[oid])
   if path.startswith('git/commits/'):return copy.deepcopy(commits[oid])
   if path.startswith('git/blobs/'):
    raw=blobs[oid];return {'sha':oid,'size':len(raw),'encoding':'base64','content':base64.b64encode(raw).decode()}
   raise RuntimeError('Unexpected injected route')
  m={'schema':'pr211-native-adoption-inputs-v1','PR':211,'problem_id':'5100063','phase':'adoption100','helper_pin':pin((d/'native211_model.py').read_bytes()),'executor_pin':pin((d/'native211_future_executor.py').read_bytes()),'core_pin':h.CORE_PIN,'baseline_pin':h.BASELINE_PIN,'protected_reference_pin':h.PROTECTED_REFERENCE_PIN,'expected_parent':h.ANCHOR,'expected_parent_tree':parent_tree,'facts':facts,'public_allowlist':sorted(role_paths.values()),'protected_queue':dict(zip(('mode','type','sha'),queue)),'reused_trees':[{'path':h.ATTEMPT[:-1],'mode':'040000','type':'tree','sha':h.ATTEMPT_TREE},{'path':h.SHARED,'mode':'040000','type':'tree','sha':h.SHARED_TREE}],'reused_blobs':ref['critical_blobs'],'writer_lock':h.WRITER_LOCK_REFERENCE,'candidate_journal':'SYNTHETIC_ONLY_NO_EFFECT','commit_message':'Independent synthetic PR211 check only\n','commit_author':{'name':'Synthetic','email':'synthetic@example.invalid','date':'2026-10-17T05:00:00Z'},'commit_committer':{'name':'Synthetic','email':'synthetic@example.invalid','date':'2026-10-17T05:00:00Z'}}
  m['files']=[]
  for i,(p,raw) in enumerate(sorted(bodies.items())):
   source='fixtures/selected'+str(i)+'.data';write(d/source,raw);v=leaves.get(p)
   m['files'].append({'path':p,'source':source,**pin(raw),'git_blob':blob(raw),'preimage':dict(zip(('mode','type','sha'),v)) if v else None})
  m['total_files']=len(bodies);m['total_bytes']=sum(map(len,bodies.values()));m['local_views']=[]
  for i,p in enumerate(h.VIEWS):
   source='fixtures/local'+str(i)+'.data';write(d/source,localbefore[p])
   m['local_views'].append({'path':p,'preimage':pin(localbefore[p]),'source':source});write(checkout/p,localbefore[p])
  for i in (1,2):write(d/('fixtures/audit'+str(i)+'.json'),enc({'synthetic_only':i}))
  def make_gate(mm,mp):
   return {'schema':'pr211-root-native-adoption-model-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','synthetic_only_never_authority':True,'PR':211,'phase':'adoption100','accepted':True,'manifest_pin':mp,'helper_pin':mm['helper_pin'],'executor_pin':mm['executor_pin'],'core_pin':h.CORE_PIN,'facts':facts,'scientific_accepted':True,'priority_accepted':True,'whole_package_reviews_accepted':True,'existing_publication_verified':True,'existing_tracker_verified':True,'native_custody_accepted':True,'no_new_publication_or_tracker_action':True,'public_selection_reviewed':True,'original_PR_already_merged':True,'original_merge_commit':h.MERGED,'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,'prepared_tree':h.PREPARED_TREE,'native_audits':[{'path':'fixtures/audit'+str(i)+'.json',**pin((d/('fixtures/audit'+str(i)+'.json')).read_bytes()),'Root_accepted':True,'helper_pin':mm['helper_pin'],'executor_pin':mm['executor_pin'],'manifest_pin':mp} for i in (1,2)],'receipts':{role:{'path':path,**pin(bodies[path])} for role,path in role_paths.items()}}
  def prepare(mm=None,gg=None):
   mm=copy.deepcopy(m if mm is None else mm);raw=enc(mm);mp=pin(raw)
   write(d/'fixtures/inputs.json',raw);g=make_gate(mm,mp) if gg is None else gg;rawgate=enc(g);gp=pin(rawgate);write(d/'fixtures/gate.json',rawgate)
   return lambda:h.load_inputs('fixtures/inputs.json',mp,'fixtures/gate.json',gp)
  load=prepare();cc,mm,overlay,pre,reused=load()
  yes(len(overlay)==14 and len(reused)==10,'exact_copied_production_loader_accepts_only_synthetic14_and_ten_protections')
  no(lambda:h.load_inputs('absent.json',pin(b'x'),'none.json',pin(b'x')),'actual_input_absence_refused')
  for field,value in (('schema','pr210-native-adoption-inputs-v1'),('PR',210),('facts',{**facts,'goal_complete':True}),('facts',{**facts,'fully_completed_count':53.0}),('reused_blobs',[]),('reused_trees',list(reversed(m['reused_trees']))),('writer_lock',{**m['writer_lock'],'inode':m['writer_lock']['inode']+1}),('candidate_journal','../escape')):
   bad=copy.deepcopy(m);bad[field]=value;no(prepare(bad),'adapted_input_refused_'+field+'_'+str(value)[:50])
  for i in range(10):
   bad=copy.deepcopy(m);bad['reused_blobs'][i]['bytes']+=1;no(prepare(bad),'critical_reference_pin_mutation_'+str(i))
  for path in (h.QUEUE,h.ATTEMPT+'PROOF.md',h.SHARED+'/preprint/manuscript.tex',h.CASE+'_private/a.json',h.CASE+'packet100/a.json',h.CASE+'paper.pdf',h.CASE+'paper.zip',h.CASE+'native_custody_01/public/native_commits/'+('0'*40)+'.commit'):
   bad=copy.deepcopy(m);bad['public_allowlist'][0]=path;bad['public_allowlist'].sort();no(prepare(bad),'positive_scope_refuses_'+path)
  g=make_gate(m,pin(enc(m)))
  for key,value in (('schema','pr211-review-only-spec'),('evidence_scope','PLANNED_ROOT_RECEIPT'),('accepted',False),('scientific_accepted',False),('priority_accepted',False),('whole_package_reviews_accepted',False),('facts',{**facts,'goal_complete':0}),('prepared_tree',h.MERGED_TREE)):
   bad=copy.deepcopy(g);bad[key]=value;no(prepare(gg=bad),'actual_Root_authority_guard_'+key)
  for role in role_names:
   bad=copy.deepcopy(g);bad['receipts'][role]['sha256']='0'*64;no(prepare(gg=bad),'all_nine_role_body_bindings_'+role)
  bad=copy.deepcopy(g);bad['receipts']['whole_package_two']=bad['receipts']['whole_package_one'];no(prepare(gg=bad),'same_whole_review_path_refused')
  for change in ('single','duplicate','wrongmanifest','unaccepted'):
   bad=copy.deepcopy(g)
   if change=='single':bad['native_audits']=bad['native_audits'][:1]
   if change=='duplicate':bad['native_audits'][1]=bad['native_audits'][0]
   if change=='wrongmanifest':bad['native_audits'][1]['manifest_pin']=pin(b'other')
   if change=='unaccepted':bad['native_audits'][1]['Root_accepted']=False
   no(prepare(gg=bad),'two_distinct_Root_native_audits_'+change)
  load=prepare();cc,mm,overlay,pre,reused=load();s=h.state(cc,mm,overlay,pre,reused,observer)
  yes(s['parents']==[h.ANCHOR],'one_fresh_MAIN_parent_not_original_merge_parents')
  after=root_tree({**leaves,**{p:('100644','blob',blob(raw)) for p,raw in overlay.items()}})
  yes(s['wanted']==after,'computed_overlay_tree_preserves_all_opaque_foreign_tuples')
  req,oid=h.commit_request(mm,after,[h.ANCHOR]);commits[oid]={'sha':oid,'tree':{'sha':after},'parents':[{'sha':h.ANCHOR}],**{k:req[k] for k in ('author','committer','message')}}
  requests.clear();result=h.verify(cc,mm,overlay,pre,reused,observer,oid)
  yes(result['full_scope_verified'] and len(result['selected_files'])==14 and len(result['protected_existing_scientific_bodies_verified'])==10,'independent_full_candidate_verifier14_new_ten_existing_bodies')
  yes('git/trees/'+h.ATTEMPT_TREE not in requests and 'git/blobs/'+queue[2] not in requests,'whole_own44_and_QUEUE_stay_opaque')
  for key in (h.PREPARED,h.MERGED):
   saved=copy.deepcopy(commits[key])
   for field,value,label in (('tree',{'sha':h.MERGED_TREE if key==h.PREPARED else h.PREPARED_TREE},'false_root_equality'),('parents',list(reversed(saved['parents'])),'reversed_parents'),('parents',saved['parents'][:1],'missing_second_parent')):
    commits[key][field]=value;no(lambda:h.state(cc,mm,overlay,pre,reused,observer),label+'_'+key);commits[key]=copy.deepcopy(saved)
  for r in ref['critical_blobs']:
   bad=b'changed private protected body';overrides['git/blobs/'+r['sha']]={'sha':r['sha'],'size':len(bad),'encoding':'base64','content':base64.b64encode(bad).decode()}
   no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid),'full_existing_body_tamper_refused_'+Path(r['path']).name);overrides.clear()
  commits[oid]['message']=req['message'][:-1];yes(h.verify(cc,mm,overlay,pre,reused,observer,oid)['commit_message_readback']['terminal_LFs_omitted']==1,'only_one_terminalLF_metadata_omission_allowed')
  commits[oid]['message']=req['message']+'\n';no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid),'extra_message_LF_refused');commits[oid]['message']=req['message']
  main[0]=oid;yes(h.verify(cc,mm,overlay,pre,reused,observer,oid,after_ref=True)['actual_MAIN_observed']==oid,'after_ref_full_GET_candidate_readback')
  main[0]='0'*40;no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid,after_ref=True),'after_ref_wrong_MAIN_refused');main[0]=h.ANCHOR
  # Actual executor routes are rejected before run_bounded; no transport is reached.
  api=e.API(h,d,mutate=True)
  for method,path in (('PATCH','git/refs/heads/main'),('POST','git/refs'),('POST','pulls/211/merge'),('POST','zenodo/publish'),('GET','pulls/210')):
   no(lambda method=method,path=path:api(method,path,{} if method!='GET' else None,expected_oid='0'*40),'forbidden_executor_route_'+method+'_'+path)
  previous=os.environ.get('GH_HOST');os.environ['GH_HOST']='hostile.invalid'
  try:
   for method,path,body in (('GET','git/ref/heads/main',False),('POST','git/trees',True)):
    argv=e.api_argv(method,path,body);yes(argv[:5]==[e.GH,'api','--hostname','github.com','--method'] and argv[5]==method,'explicit_host_despite_GH_HOST_'+method)
  finally:
   if previous is None:os.environ.pop('GH_HOST',None)
   else:os.environ['GH_HOST']=previous
  j=e.journal_new('ONE_USE_ONLY');no(lambda:e.journal_new('ONE_USE_ONLY'),'one_use_journal_reuse_refused')
  lockpath=checkout/h.WRITER_LOCK_REFERENCE['path'];write(lockpath,e.LOCK_BYTES)
  class SyntheticStop(RuntimeError):pass
  def probe():
   code='import os,sys,fcntl;fd=os.open(sys.argv[1],os.O_RDONLY);\ntry:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)\nexcept BlockingIOError:sys.exit(7)\nelse:sys.exit(0)'
   return subprocess.run([sys.executable,'-E','-S','-B','-P','-c',code,str(lockpath)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False).returncode
  for scenario in ('held','absent','replace_before_tree','replace_after_tree','payload_after_tree','Main_before_tree','gate_before_tree'):
   if not lockpath.exists():write(lockpath,e.LOCK_BYTES)
   else:write(lockpath,e.LOCK_BYTES)
   st=lockpath.stat();ownlock={'path':h.WRITER_LOCK_REFERENCE['path'],'device':st.st_dev,'inode':st.st_ino,**pin(e.LOCK_BYTES)}
   synthetic_m={**mm,'writer_lock':ownlock,'candidate_journal':'ONLY_SYNTHETIC_'+scenario};journal=e.journal_new(synthetic_m['candidate_journal'])
   loads=[0];posts=[0];reads=[0]
   def checked_load():
    loads[0]+=1
    value=load() # Actual exact copied production loader rechecks sealed fixture inputs/gate.
    if scenario=='gate_before_tree' and loads[0]>=2:raise RuntimeError('Injected stale Root gate')
    return value[0],synthetic_m,*value[2:]
   def candidate_api(method,path,body=None,expected_oid=None):
    if method=='POST':
     posts[0]+=1
     yes(probe()==7 and loads[0]>=3,'candidate_POST_requires_held_lock_and_fresh_gate_'+scenario)
     if scenario=='replace_after_tree':
      temp=lockpath.with_name('OWN_REPLACEMENT');write(temp,e.LOCK_BYTES);os.replace(temp,lockpath);return {'sha':expected_oid}
     if scenario=='payload_after_tree':write(lockpath,b'changed owned payload');return {'sha':expected_oid}
     raise SyntheticStop('Intercepted before transport')
    answer=observer(method,path,body)
    if path=='git/ref/heads/main':
     reads[0]+=1
     if reads[0]==2:
      if scenario=='replace_before_tree':
       temp=lockpath.with_name('OWN_REPLACEMENT');write(temp,e.LOCK_BYTES);os.replace(temp,lockpath)
      if scenario=='Main_before_tree':main[0]='0'*40
    return answer
   if scenario=='absent':lockpath.unlink()
   try:e.candidate(h,checked_load,candidate_api,journal)
   except SyntheticStop:yes(scenario=='held' and posts[0]==1,'held_lock_positive_stopped_before_transport')
   except (RuntimeError,OSError):yes(scenario!='held' and posts[0]==(1 if scenario in ('replace_after_tree','payload_after_tree') else 0),'candidate_boundary_stops_'+scenario)
   else:raise RuntimeError('Expected synthetic candidate stop')
   main[0]=h.ANCHOR
   if lockpath.exists():yes(probe()==0,'lock_released_after_stop_'+scenario)
  # Separate actual CAS receipt parser: only synthetic owned files; no sync invoked.
  actual={'schema':'pr211-root-native-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':211,'phase':mm['phase'],'accepted':True,'manifest_pin':pin(enc(mm)),'helper_pin':mm['helper_pin'],'executor_pin':mm['executor_pin'],'core_pin':h.CORE_PIN,'facts':facts,'parent':mm['expected_parent'],'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,'original_merge_commit':h.MERGED,'original_PR_already_merged':True,'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,'candidate':oid,'tree':after,'actual_MAIN_observed':oid,'Root_ref_update':{'expected_sha':h.ANCHOR,'sha':oid,'force':False,'success_confirmed_by_actual_native_readback':True}}
  def actual_load(a):
   raw=enc(a);write(d/'fixtures/actual.json',raw);return e.actual_acceptance(h,mm,pin(enc(mm)),'fixtures/actual.json',pin(raw))
  yes(actual_load(actual)['candidate']==oid,'separate_actualCAS_parser_synthetic_positive')
  for key,value in (('evidence_scope','PLANNED_ROOT_RECEIPT'),('actual_MAIN_observed',h.ANCHOR),('Root_ref_update',{**actual['Root_ref_update'],'force':True}),('Root_ref_update',{**actual['Root_ref_update'],'expected_sha':'0'*40}),('Root_ref_update',{**actual['Root_ref_update'],'success_confirmed_by_actual_native_readback':False})):
   bad=copy.deepcopy(actual);bad[key]=value;no(lambda bad=bad:actual_load(bad),'actualCAS_refuses_'+key+'_'+str(value)[:50])
 # Rehash production closure after all owned-fixture controls and cleanup.
 yes(pin((SOURCE/'SOURCE_MANIFEST.json').read_bytes())==source_manifest and all(pin((SOURCE/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')} for r in sm['files']),'frozen17_source_closure_unchanged_after_controls')
 return {'schema':'pr211-independent-operational-source-controls-v1','UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':CHECKS,'check_count':len(CHECKS),'source_manifest':source_manifest,'preparer_selftest_executed':False,'private_dependencies':fixture,'synthetic_candidate_POST_interceptions_only':True,'production_or_network_transport_calls':0,'production_current_five_original_lock_Git_ref_provider_PR_tracker_mutations':0,'actual_acceptance_or_case_readiness_inferred':False,'fixture_removed':True}
if __name__=='__main__':
 if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Require -E -S -B -P')
 result=run()
 if sys.argv[1:]==['--stdout-only']:print(enc(result).decode(),end='')
 elif not sys.argv[1:]:
  output=HERE/'CONTROL_RESULT.json';output.write_bytes(enc(result));print(json.dumps({'status':result['status'],'checks':result['check_count'],'result':pin(output.read_bytes())}))
 else:raise RuntimeError('Only --stdout-only replay mode supported')


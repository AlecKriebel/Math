"""Synthetic private-fixture controls only; no provider/real journals/current views.
Modules are executed from exact copied sources; no function, module, or transport
is monkeypatched. The native observer is the model's ordinary injected interface.
"""
from pathlib import Path
import ast,base64,copy,hashlib,json,os,subprocess,sys,tempfile,types
BASE=Path(__file__).absolute().parent

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
  root=Path(name)/'checkout';program=root/'draft_pr_publication_program_20260930';case=program/'audits/pr211_5100063';d=case/'native_adoption_preparation_01';d.mkdir(parents=True)
  def write(path,raw):
   path.parent.mkdir(parents=True,exist_ok=True)
   if path.exists():path.chmod(0o644)
   path.write_bytes(raw);path.chmod(0o444)
  def enc(value):return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
  for filename in ('native211_model.py','native211_future_executor.py','native_trees_readonly.py','BASELINE_MEMBERSHIP.json','PROTECTED_NATIVE_REFERENCE.json'):
   write(d/filename,(BASE/filename).read_bytes())
  h=load(d/'native211_model.py');c=h.core();e=load(d/'native211_future_executor.py')
  baseline=json.loads((d/'BASELINE_MEMBERSHIP.json').read_bytes())
  post=h.phase_facts('adoption100');oldfacts=h.baseline_facts()
  yes(post['fully_completed_count']==53 and post['published_count']==37 and post['last_completed_PR']==211 and post['next_numeric_intake_cursor']==212 and post['goal_complete'] is False,'single_terminal53_37_211_212_goalFalse')
  yes(len(h.PUBLIC_PINNED_EXCEPTIONS)==8,'only_eight_fixed_public_native_commit_exceptions')
  no(lambda:h.need(h.public_payload_path(h.CASE+'native_custody_01/archive/native_commits/'+('0'*40)+'.commit'),'unlisted'),'unlisted_native_commit_exception_refused')
  no(lambda:h.phase_facts('merge95'),'old_merge95_phase_refused')
  no(lambda:h.phase_facts('completion100'),'old_completion100_phase_refused')
  marker=h.phase_marker('adoption100')
  history=b'<!-- PR210_NATIVE_PHASE_FACTS historical95 -->\n<!-- PR210_NATIVE_PHASE_FACTS historical100 -->\n'
  h.markdown_current(history+marker+b'\n','adoption100',True);yes(True,'prior_PR210_markers_history_new_PR211_terminal_allowed')
  for raw,label in ((marker+b'\n'+marker+b'\n','duplicate'),(marker+b'\nafter\n','nonterminal'),(b'inline '+marker+b'\n','midline'),(b'<!-- PR211_NATIVE_PHASE_FACTS\t{} -->\n'+marker+b'\n','malformed_namespace')):
   no(lambda raw=raw:h.markdown_current(raw,'adoption100',True),'marker_'+label+'_refused')
  yes(not h.exact({'n':51},{'n':51.0}),'deep_JSON_numeric_type_guard')
  publicpaths=[h.CASE+'ROOT_SYNTHETIC_'+role+'.json' for role in ('scientific','priority','whole_package_one','whole_package_two','existing_publication','existing_tracker','custody','actual_prior210_completion','PR211_status_intake')]
  roles=dict(zip(('scientific','priority','whole_package_one','whole_package_two','existing_publication','existing_tracker','custody','actual_prior210_completion','PR211_status_intake'),publicpaths))
  bodies={p:enc({'synthetic_fixture_only':True,'role':role}) for role,p in roles.items()}
  case_native=b'synthetic native case log\n';case_local=case_native+b'synthetic current local40 note\n';prog_native=history+b'synthetic accepted210 program log\n'
  oldprogress={**oldfacts,'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs'],'published_PRs':baseline['published_PRs'],'dated_eligible_total':99}
  newprogress={**post,'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[211],'published_PRs':baseline['published_PRs']+[211],'dated_eligible_total':99}
  before_views={h.VIEWS[0]:enc({'synthetic_case40':True}),h.VIEWS[1]:case_native,h.VIEWS[2]:enc(oldprogress),h.VIEWS[3]:b'prior current synthetic document\n',h.VIEWS[4]:prog_native}
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
  fixture_spec=json.loads((BASE/'SELFTEST_FIXTURE_INPUTS.json').read_bytes())
  fixture_root=BASE.parent/'native_custody_01'
  fixture_data={}
  for row in fixture_spec['files']:
   raw=(fixture_root/row['path']).read_bytes();yes(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'finite_existing_fixture_pin_'+row['path'])
   fixture_data[row['path']]=raw
  native_trees=json.loads(fixture_data['FINAL_NATIVE_TREES_SUPPLEMENT.json'])
  for oid0 in (h.SHARED_TREE,'6103bc250915076cca7cfde6607f89e173294723'):
   entries=native_trees[oid0];rows0=[(k,v['mode'],v['type'],v['sha']) for k,v in entries.items()]
   yes(c.tree_hash(rows0)==oid0,'authenticated_actual_opaque_fixture_tree_'+oid0)
   tree(rows0)
  for row in json.loads(fixture_data['CURRENT_MAIN_TO_FROZEN_V1_BODY_IDENTITIES.json'])['records']:
   info=row['native_current_MAIN'];yes(blob(fixture_data[info['reading_copy']])==info['sha'],'ten_actual_existing_fixture_native_blob_'+row['file'])
  parent_tree=root_tree(leaves)
  commitmeta={
   h.ORIGINAL:{'sha':h.ORIGINAL,'tree':{'sha':h.ORIGINAL_TREE},'parents':[{'sha':'a3bdcb55173cb41866a58aded968b68d6a14d1a4'}]},
   h.PREPARED:{'sha':h.PREPARED,'tree':{'sha':h.PREPARED_TREE},'parents':[{'sha':h.ORIGINAL},{'sha':h.PREPARED_SECOND_PARENT}]},
   h.MERGED:{'sha':h.MERGED,'tree':{'sha':h.MERGED_TREE},'parents':[{'sha':h.MERGE_FIRST_PARENT},{'sha':h.PREPARED}]},
   h.ANCHOR:{'sha':h.ANCHOR,'tree':{'sha':parent_tree},'parents':[{'sha':'8'*40}]}}
  pr={'number':211,'head':{'sha':h.PREPARED},'base':{'ref':'main'},'draft':False,'state':'closed','merged':True,'merge_commit_sha':h.MERGED,'merged_at':h.MERGED_AT}
  def observer(method,path,body=None):
   if method!='GET' or body is not None:raise RuntimeError('Synthetic GET-only observer')
   requests.append(path)
   if path in overrides:return copy.deepcopy(overrides[path])
   if path=='git/ref/heads/main':return {'object':{'sha':ref[0]}}
   if path=='pulls/211':return copy.deepcopy(pr)
   if path.startswith('compare/'):
    base=path.split('/')[1].split('...')[0];return {'status':'ahead','merge_base_commit':{'sha':base}}
   oid=path.rsplit('/',1)[-1]
   if path.startswith('git/trees/'):return copy.deepcopy(objects[oid])
   if path.startswith('git/commits/'):return copy.deepcopy(commitmeta[oid])
   if path.startswith('git/blobs/'):
    raw=blobs[oid];return {'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
   raise RuntimeError('Unexpected synthetic route')
  m={'schema':'pr211-native-adoption-inputs-v1','PR':211,'problem_id':'5100063','phase':'adoption100','helper_pin':pin((d/'native211_model.py').read_bytes()),'executor_pin':pin((d/'native211_future_executor.py').read_bytes()),'core_pin':h.CORE_PIN,'expected_parent':h.ANCHOR,'expected_parent_tree':parent_tree,'facts':post,'public_allowlist':sorted(publicpaths),'protected_queue':dict(zip(('mode','type','sha'),queue)),'reused_blobs':json.loads((d/'PROTECTED_NATIVE_REFERENCE.json').read_bytes())['critical_blobs'],'reused_trees':[{'path':h.ATTEMPT[:-1],'mode':'040000','type':'tree','sha':h.ATTEMPT_TREE},{'path':h.SHARED,'mode':'040000','type':'tree','sha':h.SHARED_TREE}],'baseline_pin':h.BASELINE_PIN,'protected_reference_pin':h.PROTECTED_REFERENCE_PIN,'writer_lock':h.WRITER_LOCK_REFERENCE,'candidate_journal':'SYNTHETIC_NEVER_EXECUTED_CANDIDATE','commit_message':'Synthetic adoption test only\n','commit_author':{'name':'Synthetic','email':'synthetic@example.invalid','date':'2026-10-17T04:00:00Z'},'commit_committer':{'name':'Synthetic','email':'synthetic@example.invalid','date':'2026-10-17T04:00:00Z'}}
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
   return {'schema':'pr211-root-native-adoption-model-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','synthetic_fixture_only_not_authority':True,'PR':211,'phase':'adoption100','accepted':True,'manifest_pin':mp,'helper_pin':mm['helper_pin'],'executor_pin':mm['executor_pin'],'core_pin':h.CORE_PIN,'facts':post,'scientific_accepted':True,'priority_accepted':True,'whole_package_reviews_accepted':True,'existing_publication_verified':True,'existing_tracker_verified':True,'native_custody_accepted':True,'no_new_publication_or_tracker_action':True,'public_selection_reviewed':True,'original_PR_already_merged':True,'original_merge_commit':h.MERGED,'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,'prepared_tree':h.PREPARED_TREE,'native_audits':[{'path':'synthetic/audit'+str(i)+'.json',**pin((d/('synthetic/audit'+str(i)+'.json')).read_bytes()),'Root_accepted':True,'helper_pin':mm['helper_pin'],'executor_pin':mm['executor_pin'],'manifest_pin':mp} for i in (1,2)],'receipts':{role:{'path':path,**pin(bodies[path])} for role,path in roles.items()}}
  def loaded(mm=None,gg=None):
   mm=copy.deepcopy(m if mm is None else mm);raw=enc(mm);mp=pin(raw);write(d/'synthetic/inputs.json',raw)
   g=gate(mm,mp) if gg is None else gg;gr=enc(g);write(d/'synthetic/gate.json',gr)
   return h.load_inputs('synthetic/inputs.json',mp,'synthetic/gate.json',pin(gr))
  cc,mm,overlay,pre,reused=loaded();yes(len(overlay)==14 and len(reused)==10,'full_synthetic_input_gate_load_exact14_selected_ten_protected_existing_bodies')
  no(lambda:h.load_inputs('missing.json',{'bytes':1,'sha256':'0'*64},'none.json',{'bytes':1,'sha256':'0'*64}),'absent_actual_inputs_fail_closed')
  for key,value,label in [('phase','merge95','merge_phase'),('protected_queue',None,'missing_queue'),('reused_blobs',[{}],'redundant_science'),('facts',{**post,'published_count':37.0},'floating_fact'),('writer_lock',{**m['writer_lock'],'inode':float(m['writer_lock']['inode'])},'floating_lock')]:
   bad=copy.deepcopy(m);bad[key]=value;no(lambda bad=bad:loaded(bad),'input_'+label+'_refused')
  for path,label in [(h.QUEUE,'whole_queue'),(h.ATTEMPT+'PROOF.md','own_attempt'),(h.SHARED+'/preprint/metadata.json','shared_audit'),(h.CASE+'_private/secret.json','private'),(h.CASE+'packet100/inputs.json','working_packet'),(h.CASE+'paper.pdf','PDF'),(h.CASE+'root_reproduction_preparation_01/extracted/data.json','extraction')]:
   bad=copy.deepcopy(m);bad['public_allowlist'][0]=path;bad['public_allowlist'].sort();no(lambda bad=bad:loaded(bad),'scope_'+label+'_refused')
  bad=copy.deepcopy(m);next(r for r in bad['files'] if r['path'] not in h.VIEWS)['preimage']={'mode':'100644','type':'blob','sha':'0'*40};no(lambda:loaded(bad),'existing_public_archive_replacement_refused')
  bad=copy.deepcopy(m);bad['public_allowlist'].append(bad['public_allowlist'][0]);no(lambda:loaded(bad),'duplicate_public_allowlist_refused')
  bad=copy.deepcopy(m);row=next(r for r in bad['files'] if r['path']==h.VIEWS[2]);raw=enc({**newprogress,'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[211.0]});write(d/'synthetic/floatprogress.data',raw);row.update(source='synthetic/floatprogress.data',**pin(raw),git_blob=blob(raw));no(lambda:loaded(bad),'floating_ascending_membership_refused')
  bad=copy.deepcopy(m);bad['local_views'][1]['preimage']=pin(b'changed historical prefix');write(d/'synthetic/wrongprefix.data',b'changed historical prefix');bad['local_views'][1]['source']='synthetic/wrongprefix.data';no(lambda:loaded(bad),'separate_local_log_preimage_prefix_refused')
  duplicate=gate(m,pin(enc(m)));duplicate['receipts']['whole_package_two']=duplicate['receipts']['whole_package_one'];no(lambda:loaded(gg=duplicate),'duplicate_new_whole_review_receipt_refused')
  cc,mm,overlay,pre,reused=loaded();s=h.state(cc,mm,overlay,pre,reused,observer);yes(s['parents']==[h.ANCHOR],'adoption_has_single_fresh_MAIN_parent')
  after_leaves={**leaves,**{p:('100644','blob',blob(raw)) for p,raw in overlay.items()}};wanted=root_tree(after_leaves);yes(wanted==s['wanted'],'native_expected_tree_exact')
  request,oid=h.commit_request(mm,wanted,[h.ANCHOR]);commitmeta[oid]={'sha':oid,'tree':{'sha':wanted},'parents':[{'sha':h.ANCHOR}],'author':request['author'],'committer':request['committer'],'message':request['message']}
  result=h.verify(cc,mm,overlay,pre,reused,observer,oid);yes(result['full_scope_verified'] and result['all_selected_native_bodies_verified'],'full_real_verifier_exact_scope_and_all_new_bodies')
  yes(not any(p in requests for p in ('git/trees/'+h.ATTEMPT_TREE,'git/blobs/'+queue[2])),'own44_whole_QUEUE_opaque_no_body_fetch')
  yes(result['own44_tree_preserved']==h.ATTEMPT_TREE and result['shared_tree_preserved']==h.SHARED_TREE,'protected_trees_exact')
  commitmeta[oid]['message']=request['message'][:-1];result=h.verify(cc,mm,overlay,pre,reused,observer,oid);yes(result['commit_message_readback']['terminal_LFs_omitted']==1,'one_terminalLF_metadata_representation_only')
  for message,label in [(request['message']+'\n','extra_LF'),(request['message'][:-1]+' ','space'),(request['message'][:-1]+'\r\n','CRLF')]:
   commitmeta[oid]['message']=message;no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid),'message_'+label+'_refused')
  commitmeta[oid]['message']=request['message']
  for key,value,label in [('sha','0'*40,'response_SHA'),('tree',{'sha':'0'*40},'tree'),('parents',[{'sha':'0'*40}],'ordered_parent'),('author',{**request['author'],'email':'changed@example.invalid'},'author_identity'),('committer',{**request['committer'],'date':'2026-10-17T04:00:01Z'},'committer_identity')]:
   saved=commitmeta[oid][key];commitmeta[oid][key]=value;no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid),'canonical_metadata_'+label+'_refused');commitmeta[oid][key]=saved
  no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,'0'*40),'wrong_deterministic_canonical_candidate_refused')
  for key,value,label in [('state','open','open'),('merged',False,'unmerged'),('head',{'sha':'0'*40},'head'),('merge_commit_sha','0'*40,'actual_merge')]:
   original=pr[key];pr[key]=value;no(lambda:h.state(cc,mm,overlay,pre,reused,observer),'PR_'+label+'_refused');pr[key]=original
  route='compare/'+h.MERGED+'...'+h.ANCHOR;overrides[route]={'status':'diverged','merge_base_commit':{'sha':'0'*40}};no(lambda:h.state(cc,mm,overlay,pre,reused,observer),'original_merge_ancestry_refused');del overrides[route]
  badprogress_raw=enc({**oldprogress,'fully_completed_count':53});badprogress_oid=blob(badprogress_raw)
  moved_tree=root_tree({**leaves,h.VIEWS[2]:('100644','blob',badprogress_oid)});moved=copy.deepcopy(mm);moved['expected_parent_tree']=moved_tree;moved_pre={**pre,h.VIEWS[2]:('100644','blob',badprogress_oid)};commitmeta[h.ANCHOR]['tree']['sha']=moved_tree
  try:h.state(cc,moved,overlay,moved_pre,reused,observer)
  except RuntimeError as error:yes('Refuse overwriting an intervening ascending checkpoint' in str(error),'valid_native_body_intervening_ascending_checkpoint_refused')
  else:raise RuntimeError('Intervening checkpoint accepted')
  commitmeta[h.ANCHOR]['tree']['sha']=parent_tree
  progress_oid=pre[h.VIEWS[2]][2];badraw=enc({**oldprogress,'fully_completed_count':53});overrides['git/blobs/'+progress_oid]={'sha':progress_oid,'encoding':'base64','size':len(badraw),'content':base64.b64encode(badraw).decode()};no(lambda:h.state(cc,mm,overlay,pre,reused,observer),'intervening_native_progress_or_body_refused');overrides.clear()
  selected_oid=h.native('blob',next(iter(overlay.values())));badraw=b'tampered selected';overrides['git/blobs/'+selected_oid]={'sha':selected_oid,'encoding':'base64','size':len(badraw),'content':base64.b64encode(badraw).decode()};no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid),'selected_native_body_tamper_refused');overrides.clear()
  science_row=next(iter(reused.values()));science_oid=science_row['sha'];badraw=b'altered existing frozen body';overrides['git/blobs/'+science_oid]={'sha':science_oid,'encoding':'base64','size':len(badraw),'content':base64.b64encode(badraw).decode()};no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid),'protected_existing_science_full_body_tamper_refused');overrides.clear()
  yes(len(result['protected_existing_scientific_bodies_verified'])==10,'all_ten_existing_scientific_full_bodies_verified_separate_from_overlay')
  yes(h.PREPARED_TREE!=h.MERGED_TREE and h.PREPARED_SECOND_PARENT!=h.MERGE_FIRST_PARENT,'prepared_and_actual_merge_roots_and_parents_distinct')
  saved_tree=commitmeta[h.MERGED]['tree'];commitmeta[h.MERGED]['tree']={'sha':h.PREPARED_TREE};no(lambda:h.state(cc,mm,overlay,pre,reused,observer),'false_prepared_actual_merge_whole_root_equality_refused');commitmeta[h.MERGED]['tree']=saved_tree
  ref[0]=oid;yes(h.verify(cc,mm,overlay,pre,reused,observer,oid,after_ref=True)['actual_MAIN_observed']==oid,'after_CAS_full_readonly_verify_mode')
  ref[0]='0'*40;no(lambda:h.verify(cc,mm,overlay,pre,reused,observer,oid,after_ref=True),'after_CAS_wrong_MAIN_refused');ref[0]=h.ANCHOR
  api=e.API(h,d,mutate=True)
  for method,path in [('POST','git/refs'),('PATCH','git/refs/heads/main'),('POST','pulls/211/merge'),('GET','pulls/210')]:no(lambda method=method,path=path:api(method,path,{} if method!='GET' else None,expected_oid='0'*40),'executor_forbidden_route_'+method+'_'+path)
  lockpath=program/'ROOT_GLOBAL_FIVE_WRITER.lock';write(lockpath,e.LOCK_BYTES);st=lockpath.stat();lock={'path':h.WRITER_LOCK_REFERENCE['path'],'device':st.st_dev,'inode':st.st_ino,**pin(e.LOCK_BYTES)}
  with e.WriterLock(lock):yes(True,'fixture_stable_inode_lock_positive')
  replacement=lockpath.with_name('FIXTURE_REPLACEMENT.tmp');write(replacement,e.LOCK_BYTES);os.replace(replacement,lockpath);no(lambda:e.WriterLock(lock).__enter__(),'fixture_same_payload_new_inode_lock_refused')
  e.journal_new('SYNTHETIC_UNIQUE');no(lambda:e.journal_new('SYNTHETIC_UNIQUE'),'fixture_journal_reuse_refused')
  prior_host=os.environ.get('GH_HOST');os.environ['GH_HOST']='hostile.invalid'
  try:
   getargv=e.api_argv('GET','git/ref/heads/main',False);postargv=e.api_argv('POST','git/trees',True)
   yes(getargv==[e.GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/git/ref/heads/main'],'explicit_canonical_host_ignores_hostile_GH_HOST_GET')
   yes(postargv==[e.GH,'api','--hostname','github.com','--method','POST','repos/AlecKriebel/Math/git/trees','--input','-'],'explicit_canonical_host_ignores_hostile_GH_HOST_POST')
  finally:
   if prior_host is None:os.environ.pop('GH_HOST',None)
   else:os.environ['GH_HOST']=prior_host
  # Full real candidate entry uses the ordinary trusted loader/API interfaces.
  # Only this fixture's lock identity differs from production's immutable pin;
  # production load_inputs still rejects that substitution. No module is patched.
  for row in mm['local_views']:write(root/row['path'],(d/row['source']).read_bytes())
  class SyntheticPostStop(RuntimeError):pass
  def lock_probe():
   code='import os,sys,fcntl; fd=os.open(sys.argv[1],os.O_RDONLY);\ntry: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)\nexcept BlockingIOError: sys.exit(7)\nelse: sys.exit(0)'
   return subprocess.run([sys.executable,'-E','-S','-B','-P','-c',code,str(lockpath)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False).returncode
  for mode in ('held','absent','replaced','replaced_after_tree','modified_after_tree'):
   if not lockpath.exists():write(lockpath,e.LOCK_BYTES)
   st=lockpath.stat();expected_lock={'path':h.WRITER_LOCK_REFERENCE['path'],'device':st.st_dev,'inode':st.st_ino,**pin(e.LOCK_BYTES)}
   fixture_m={**mm,'writer_lock':expected_lock,'candidate_journal':'SYNTHETIC_LOCK_'+mode.upper()};fixture_journal=e.journal_new(fixture_m['candidate_journal'])
   load_calls=[0];posts=[0];main_reads=[0]
   def fixture_load():
    load_calls[0]+=1
    return cc,fixture_m,overlay,pre,reused
   def candidate_api(method,path,body=None,expected_oid=None):
    if method=='POST':
     posts[0]+=1
     yes(mode in ('held','replaced_after_tree','modified_after_tree') and posts[0]==1 and lock_probe()==7 and load_calls[0]>=3,'real_candidate_'+mode+'_first_POST_requires_held_fixture_lock_and_fresh_loads')
     if mode=='replaced_after_tree':
      replacement=lockpath.with_name('FIXTURE_REPLACEMENT.tmp');write(replacement,e.LOCK_BYTES);os.replace(replacement,lockpath);return {'sha':expected_oid}
     if mode=='modified_after_tree':
      write(lockpath,b'changed fixture payload');return {'sha':expected_oid}
     raise SyntheticPostStop('Synthetic injected API stops before any transport')
    answer=observer(method,path,body)
    if path=='git/ref/heads/main':
     main_reads[0]+=1
     if mode=='replaced' and main_reads[0]==2:
      replacement=lockpath.with_name('FIXTURE_REPLACEMENT.tmp');write(replacement,e.LOCK_BYTES);os.replace(replacement,lockpath)
    return answer
   if mode=='absent':lockpath.unlink()
   try:e.candidate(h,fixture_load,candidate_api,fixture_journal)
   except SyntheticPostStop:yes(mode=='held' and posts[0]==1,'candidate_held_lock_control_stopped_before_transport')
   except (RuntimeError,OSError):yes(mode!='held' and posts[0]==(1 if mode.endswith('_after_tree') else 0),'candidate_'+mode+'_fixture_lock_refused_before_next_POST')
   else:raise RuntimeError('Candidate fixture should stop')
   if lockpath.exists():yes(lock_probe()==0,'candidate_'+mode+'_fixture_lock_released_on_stop')
  old_source=BASE.parents[1]/'pr210_5100033/native_adoption_preparation_02/native210_future_executor.py'
  original_ast=ast.parse(old_source.read_bytes());current_ast=ast.parse((BASE/'native211_future_executor.py').read_bytes())
  class NormalizeAccepted210(ast.NodeTransformer):
   def visit_Constant(self,node):
    if type(node.value) is str:node.value=node.value.replace('PR210','PR211').replace('pr210','pr211').replace('pulls/210','pulls/211').replace('native210','native211')
    elif type(node.value) is int and node.value==210:node.value=211
    return node
   def visit_Assign(self,node):
    return None if any(isinstance(t,ast.Name) and t.id=='MODEL_PIN' for t in node.targets) else self.generic_visit(node)
  yes(ast.dump(NormalizeAccepted210().visit(original_ast))==ast.dump(NormalizeAccepted210().visit(current_ast)),'entire_accepted210v2_executor_AST_unchanged_after_exact_case_literal_and_crosspin_normalization')
  current_candidate=next(n for n in current_ast.body if isinstance(n,ast.FunctionDef) and n.name=='candidate')
  guard=next(n for n in ast.walk(current_candidate) if isinstance(n,ast.FunctionDef) and n.name=='effect_guard')
  yes(ast.unparse(guard.body[0])=='lock.check()' and ast.unparse(guard.body[-1])=='lock.check()','effect_guard_checks_lock_at_entry_and_immediately_before_POST')
  # No live transport, real immutable object, local-five sync or pointer executed.
 return {'schema':'pr211-native-adoption-synthetic-controls-v2','status':'PASS','checks':checks,'check_count':len(checks),'source_pins':{p:pin((BASE/p).read_bytes()) for p in ('native211_model.py','native211_future_executor.py','native_trees_readonly.py','offline_selftest.py')},'synthetic_only':True,'no_model_or_module_monkeypatches':True,'provider_calls':0,'live_objects_refs_locks_five_views_gates_or_pointers_modified':False,'actual_acceptance_inferred':False}
if __name__=='__main__':
 if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Use python3 -E -S -B -P')
 print(json.dumps(run(),sort_keys=True,indent=2))

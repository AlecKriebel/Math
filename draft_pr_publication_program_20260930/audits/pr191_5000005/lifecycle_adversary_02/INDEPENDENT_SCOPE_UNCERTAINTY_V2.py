"""Second independent offline family. Synthetic immutable object API and uncertain uploader.
No author harness read, production imports, network, Git processes, or shared mutation.
"""
from pathlib import Path
import base64,copy,hashlib,importlib.util,json,sys,types,datetime
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent;S=O.parent/'lifecycle_controls_preparation_02'
spec=importlib.util.spec_from_file_location('independent_scope_runtime02',S/'lifecycle_common.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
F=O/'fixtures/scope_and_factual_v2';F.mkdir(parents=True,exist_ok=False);m.A=F
results=[]
def put(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2)+'\n')
def check(name,fn,reject=False):
 try:fn();observed='accept';detail=None
 except Exception as e:observed='reject';detail=str(e)
 expected='reject' if reject else 'accept';results.append({'name':name,'expected':expected,'observed':observed,'passed':expected==observed,'detail':detail})
def blob(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def binding(name):return {'path':name,'bytes':1,'sha256':'1'*64}
g={'package_name':'package','payloads':{n:{'bytes':1,'sha256':'1'*64} for n in ['a.pdf','a.tex','a.zip','meta.json']},'paper_files':{'pdf':'a.pdf','source':'a.tex','support':'a.zip','metadata':'meta.json'},'native_pending_manifest':binding('pending_manifest.json'),'native_pending_template':'pending','native_final_template':'native_template_final_test','native_complete_template':'native_template_complete_test','public_case_paths':['extra_support.md'],'public_case_pins':{},'current_proof':binding('proof.md'),'review_input':binding('review_input.json'),'pr_metadata_proposal':binding('metadata_proposal.json'),'tracker_row_proposal':binding('tracker_proposal.json'),'whole_package_reviews':[{'report':binding('report1.md'),'seal':binding('seal1.json'),'root_authentication':binding('auth1.json')},{'report':binding('report2.md'),'seal':binding('seal2.json'),'root_authentication':binding('auth2.json')}],'native_proof_paths':['CANDIDATE.md']}
put(F/'ROOT_PUBLICATION_GATE.json',{'test_gate':'inert-synthetic'})
put(F/'pending_manifest.json',{'files':{'CANDIDATE.md':{},'CURRENT_RESULT.json':{}}});g['native_pending_manifest']=dict(path='pending_manifest.json',**m.pin(F/'pending_manifest.json'))
m.gate=lambda:copy.deepcopy(g)
gh=m.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'];z={'doi':'10.5281/zenodo.9919191','doi_url':'https://doi.org/10.5281/zenodo.9919191','gate_sha256':gh};tr={'range':"'Math Puzzles'!A3:D3"}
m.published_tracked=lambda:(copy.deepcopy(g),copy.deepcopy(z),copy.deepcopy(tr))
names=m.scope_names(g);native={'CANDIDATE.md','CURRENT_RESULT.json'}
selected={m.CASE+n for n in names}|{m.NATIVE+n for n in native}|{m.PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}|{'unsolved_math_prioritization/QUEUE.md'}
scope={'PR':191,'original_head':m.HEAD,'gate_sha256':gh,'case_paths':sorted(names),'selected_MAIN_paths':sorted(selected)}
put(F/'FINAL_MAIN_SCOPE.json',scope)
bodies={p:('exact frozen bytes for '+p+'\n').encode() for p in selected};bodies[m.CASE+'FINAL_MAIN_SCOPE.json']=(F/'FINAL_MAIN_SCOPE.json').read_bytes()
mergepins={p:blob(b) for p,b in bodies.items()}
def receipt(commit,parent,parenttree,tree,pins,changed):return {'commit':commit,'expected_main':parent,'parent_tree':parenttree,'tree':tree,'original_head':m.HEAD,'gate_sha256':gh,'selected_files':copy.deepcopy(pins),'selected_map_sha256':m.selected_digest(pins),'changed_paths':sorted(changed)}
merged=receipt('merge','base','tree_base','tree_merge',mergepins,set(mergepins));put(F/'SCOPED_MERGE_PREPARATION.json',merged)
factualnames=m.factual_paths(g);fbodies={p:('truthful factual body for '+p+'\n').encode() for p in factualnames};fpins={p:blob(b) for p,b in fbodies.items()}
final=receipt('factual','merge','tree_merge','tree_factual',fpins,{p for p in fpins if p not in mergepins or fpins[p]['git_blob']!=mergepins[p]['git_blob']});put(F/'FINAL_FACTUAL_PREPARATION.json',final)
accepted={'PR_merged':True,'every_selected_identity_checked_at_actual_observed_MAIN':True,'original_head':m.HEAD,'gate_sha256':gh,'merge_commit':'merge','merge_tree':'tree_merge','selected_map_sha256':merged['selected_map_sha256'],'scope_sha256':hashlib.sha256(bodies[m.CASE+'FINAL_MAIN_SCOPE.json']).hexdigest()};put(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted)
class Objects:
 def __init__(self):
  self.trees={'tree_base':{},'tree_merge':copy.deepcopy(mergepins),'tree_factual':{**copy.deepcopy(mergepins),**copy.deepcopy(fpins)}};self.current='factual'
  self.commits={'base':{'tree':{'sha':'tree_base'},'parents':[]},'merge':{'tree':{'sha':'tree_merge'},'parents':[{'sha':'base'},{'sha':m.HEAD}],'message':'Merge\nPR191 selected-map SHA256: '+merged['selected_map_sha256']},'factual':{'tree':{'sha':'tree_factual'},'parents':[{'sha':'merge'}],'message':'Facts\nPR191 selected-map SHA256: '+final['selected_map_sha256']}}
  self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *a:None)))
 def api(self,path,*args):
  if path.startswith('git/commits/'):return copy.deepcopy(self.commits[path.removeprefix('git/commits/')])
  if path=='git/ref/heads/main':return {'object':{'sha':self.current}}
  if path.startswith('compare/'):return {'status':'identical' if path.removeprefix('compare/').split('...')[0]==self.current else 'ahead'}
  if path=='pulls/191':return {'merged':True,'state':'closed','head':{'sha':m.HEAD}}
  raise AssertionError('Unexpected API '+path)
 def lookup(self,tree,p):
  x=self.trees[tree].get(p);return ('100644','blob',x['git_blob']) if x else None
 def changed_leaves(self,a,b):return {p for p in set(self.trees[a])|set(self.trees[b]) if self.lookup(a,p)!=self.lookup(b,p)}
 def body_at(self,p,commit):
  if commit=='merge':return bodies[p]
  if commit in ['factual','descendant']:return fbodies[p] if p in fbodies else bodies[p]
  raise AssertionError((p,commit))
h=Objects();m.helpers=lambda:h
check('merge_scope_full_exact_positive',lambda:m.verify_merge_scope(h,g,merged))
for label,path in [('control',m.CASE+'lifecycle_common.py'),('packet',m.CASE+'package/a.tex'),('native',m.NATIVE+'CANDIDATE.md'),('queue_guard',m.CASE+'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json')]:
 r=copy.deepcopy(merged);r['selected_files'].pop(path);r['changed_paths'].remove(path);r['selected_map_sha256']=m.selected_digest(r['selected_files'])
 saved=h.commits['merge']['message'];saved_entry=h.trees['tree_merge'].pop(path);h.commits['merge']['message']='mutant\nPR191 selected-map SHA256: '+r['selected_map_sha256']
 check('merge_selected_'+label+'_omission',lambda:m.verify_merge_scope(h,g,r),True);h.commits['merge']['message']=saved;h.trees['tree_merge'][path]=saved_entry
check('factual_combined_current_positive',m.factual_accept)
# Unrelated descendant changes are allowed, while original selected/current factual identities remain exact.
h.trees['tree_current']=copy.deepcopy(h.trees['tree_factual']);h.trees['tree_current']['unrelated/new.txt']=blob(b'concurrent foreign change');h.commits['descendant']={'tree':{'sha':'tree_current'},'parents':[{'sha':'factual'}]};h.current='descendant'
check('factual_unrelated_descendant_allowed',m.factual_accept)
for label,path in [('original_packet',m.CASE+'package/a.tex'),('original_control',m.CASE+'lifecycle_common.py'),('factual_current_native',m.NATIVE+'CURRENT_RESULT.json')]:
 saved=copy.deepcopy(h.trees['tree_current'][path]);h.trees['tree_current'][path]=blob(b'adversarial selected drift')
 check('factual_current_'+label+'_drift',m.factual_accept,True);h.trees['tree_current'][path]=saved
# Factual preparation must stop before writing a generation if parent original scope drifted.
h.current='descendant';target=m.CASE+'package/a.tex';saved=h.trees['tree_current'][target];h.trees['tree_current'][target]=blob(b'drift at factual parent')
check('factual_prepare_original_scope_drift_at_parent',lambda:m.factual_prepare('factual_preparation_audit'),True);h.trees['tree_current'][target]=saved;h.current='descendant'
# Stage/publish uncertainty exercise wrapper only; runner is an offline command recorder.
F2=O/'fixtures/zenodo_uncertainty_v2';F2.mkdir(parents=True,exist_ok=False);m.A=F2;put(F2/'ROOT_PUBLICATION_GATE.json',{'test':'inert'});m.original_ready=lambda *a:None
ug={'package_name':'package','paper_files':{'metadata':'meta.json'}};m.gate=lambda:ug
calls=[]
def runner(args,**kwargs):
 command=args[6];calls.append(command)
 # argv [python,-E,-S,-B,-P,kit,cmd,manifest]
 if command=='stage':raise RuntimeError('synthetic uncertain creation outcome')
 return types.SimpleNamespace(returncode=1,stdout=b'',stderr=b'synthetic unknown state')
check('zenodo_uncertain_stage_first',lambda:m.run_zenodo('stage',runner=runner),True)
check('zenodo_uncertain_stage_no_second_creation',lambda:m.run_zenodo('stage',runner=runner),True)
results.append({'name':'zenodo_uncertain_stage_calls','expected':['stage','inspect'],'observed':calls[:],'passed':calls==['stage','inspect'],'detail':None})
gatehash=m.pin(F2/'ROOT_PUBLICATION_GATE.json')['sha256'];put(F2/'ZENODO_STAGE_READBACK.json',{'id':123,'gate_sha256':gatehash})
calls=[]
def publish_runner(args,**kwargs):
 command=args[6];calls.append(command)
 if command=='publish':raise RuntimeError('synthetic uncertain publish POST outcome')
 return types.SimpleNamespace(returncode=0,stdout=json.dumps({'environment':'production','state':'ready_to_publish','id':123}).encode(),stderr=b'')
check('zenodo_uncertain_publish_first',lambda:m.run_zenodo('publish',123,publish_runner),True)
check('zenodo_uncertain_publish_no_second_POST',lambda:m.run_zenodo('publish',123,publish_runner),True)
results.append({'name':'zenodo_uncertain_publish_POST_calls','expected':['inspect','publish','inspect'],'observed':calls[:],'passed':calls==['inspect','publish','inspect'],'detail':None})
# Reconcile an already published result with no new publication POST.
def already_published(args,**kwargs):
 command=args[6];calls.append(command)
 return types.SimpleNamespace(returncode=0,stdout=json.dumps({'environment':'production','state':'published','id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123'}).encode(),stderr=b'')
calls=[];check('zenodo_unknown_publish_resolved_by_inspect',lambda:m.run_zenodo('publish',123,already_published));results.append({'name':'zenodo_existing_published_no_POST','expected':['inspect'],'observed':calls,'passed':calls==['inspect'],'detail':None})
summary={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256((S/'lifecycle_common.py').read_bytes()).hexdigest(),'author_harness_read_or_run':False,'tests':results,'count':len(results),'satisfied_expectations':sum(x['passed'] for x in results),'unexpected':[x for x in results if not x['passed']]}
put(O/'INDEPENDENT_SCOPE_UNCERTAINTY_V2_RESULTS.json',summary);print(json.dumps({k:v for k,v in summary.items() if k!='tests'},indent=2))

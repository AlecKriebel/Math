"""Owned pure capture-source controls. Never calls run/main/API/Seed/Runtime/lock."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,os,sys,tempfile,types
HERE=Path(__file__).absolute().parent
SOURCE=HERE.parent/'logical_capture_source_preparation_02'
ENGINE=HERE.parent/'native_completion_preparation_01'
RESULTS=[]
def need(x,m):
 if type(x) is not bool or not x:raise RuntimeError(m)
def yes(x,n):need(x,n);RESULTS.append({'name':n,'kind':'positive','passed':True})
def no(f,n):
 try:f()
 except (RuntimeError,ValueError,TypeError,KeyError,OSError,AttributeError):RESULTS.append({'name':n,'kind':'refusal','passed':True});return
 raise RuntimeError('Expected refusal: '+n)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:need(f.write(b)==len(b),'Complete owned write')
 p.chmod(0o444)
def module(p,n):
 m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 def deny(event,args):
  if event in ('subprocess.Popen','os.system','os.exec','socket.connect','socket.connect_ex','socket.bind'):raise RuntimeError('No transport or subprocess allowed')
 sys.addaudithook(deny)
 bound=json.loads((HERE/'REVIEWED_SOURCE_BINDINGS.json').read_text())
 yes(pin((SOURCE/'SOURCE_MANIFEST.json').read_bytes())==bound['capture_manifest_pin'],'exact_frozen_capture_manifest')
 with tempfile.TemporaryDirectory(prefix='_synthetic_controls_',dir=HERE) as temporary:
  checkout=Path(temporary)/'checkout';case=checkout/'draft_pr_publication_program_20260930/audits/pr218_30006020';B=case/'native_completion_preparation_01';C=case/'logical_capture_source_preparation_02'
  eraw=(ENGINE/'SOURCE_MANIFEST.json').read_bytes();em=json.loads(eraw)
  for row in em['files']:
   raw=(ENGINE/row['path']).read_bytes();yes(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'engine_'+row['path']);put(B/row['path'],raw)
  put(B/'SOURCE_MANIFEST.json',eraw)
  context_row=bound['context_reference'];context_raw=Path(context_row['path']).read_bytes();yes(pin(context_raw)=={k:context_row[k] for k in ('bytes','sha256')},'exact_raw_commit_context_reference')
  context_path=case/'native_source_custody_preparation_02/capture_native_custody.py';put(context_path,context_raw)
  for row in bound['capture_payloads']:
   raw=(SOURCE/row['path']).read_bytes();yes(pin(raw)=={k:row[k] for k in ('bytes','sha256')},'capture_'+row['path']);put(C/row['path'],raw)
  h=module(B/'native218_model.py','owned_h');cap=module(C/'capture_logical_packet.py','owned_capture')
  context=module(context_path,'owned_context_raw_commit_only')
  yes(h.CHECKOUT==cap.CHECKOUT==checkout,'all_paths_only_owned_checkout')
  commit_payload='tree '+'a'*40+'\nparent '+'b'*40+'\nauthor X <x@x> 1 +0000\ncommitter X <x@x> 1 +0000\n\nmessage\n';signature='SIG\nfold\n';head,body=commit_payload.encode().split(b'\n\n',1);signed=head+b'\ngpgsig '+b'\n '.join(signature.encode().split(b'\n'))+b'\n\n'+body
  metadata={'sha':context.native('commit',signed),'tree':{'sha':'a'*40},'parents':[{'sha':'b'*40}],'verification':{'payload':commit_payload,'signature':signature}}
  yes(context.raw_commit(metadata)==signed,'pinned_raw_commit_helper_signed_empty_fold_exact')
  no(lambda:context.raw_commit({**metadata,'tree':{'sha':'c'*40}}),'raw_commit_root_mismatch')
  no(lambda:context.raw_commit({**metadata,'parents':[{'sha':'c'*40}]}),'raw_commit_parent_mismatch')
  own=cap.read_regular(C/'capture_logical_packet.py')[0];yes(pin(own)==bound['capture_source_pin'],'real_nofollow_source_read')
  origin=case/'public_fixture.md';put(origin,b'owned public fixture\n')
  path=h.CASE+'public_fixture.md';base_row={'path':path,'origin':str(origin),**pin(origin.read_bytes()),'git_blob':h.native('blob',origin.read_bytes()),'observed_source_mode':292,'role':'owned-fixture','selection_basis':'owned synthetic source test'}
  value={'schema':'pr218-root-positive-public-selection-v1','PR':218,'operational_authority':False,'files':[base_row],'total_files':1,'total_bytes':base_row['bytes']}
  yes(cap.selection(h,value,{})[path]==base_row,'exact_six_header_eight_row_mode292_selection')
  for k,bad in (('schema','pr218-root-positive-public-selection-preparation-v1'),('PR',218.0),('operational_authority',True),('total_files',True),('total_bytes',base_row['bytes']+1)):
   no(lambda k=k,bad=bad:cap.selection(h,{**value,k:bad},{}),'selection_header_'+k)
  no(lambda:cap.selection(h,{**value,'pending':'unaccepted preliminary'},{}),'extra_pending_header_refused')
  no(lambda:cap.selection(h,{k:v for k,v in value.items() if k!='total_files'},{}),'missing_header_refused')
  for k,bad in (('observed_source_mode','0444'),('observed_source_mode',True),('observed_source_mode',292.0),('observed_source_mode',420),('bytes',True),('git_blob','f'*39),('origin','relative/path'),('role',''),('selection_basis','')):
   row={**base_row,k:bad};v={**value,'files':[row]}
   no(lambda v=v:cap.selection(h,v,{}),'row_'+k+'_'+str(bad))
  for p in (h.VIEWS[0],h.QUEUE,h.ATTEMPT+'/science.tex',h.CASE+'ROOT_COMPLETE214_READ_X/raw.json',h.CASE+'private_capture218_x/report.json',h.CASE+'hidden/.gitignore'):
   no(lambda p=p:cap.selection(h,{**value,'files':[{**base_row,'path':p}]},{}),'reserved_or_private_or_ancillary_'+p)
  no(lambda:cap.selection(h,{**value,'files':[base_row,base_row],'total_files':2,'total_bytes':2*base_row['bytes']},{}),'duplicate_selection_target')
  carry={h.PRIOR_TERMINAL_PATH:h.PRIOR_TERMINAL_PIN}
  no(lambda:cap.selection(h,value,carry),'required_exact_carry_absent')
  cr={**base_row,'path':h.PRIOR_TERMINAL_PATH,**h.PRIOR_TERMINAL_PIN};cv={**value,'files':[cr],'total_bytes':cr['bytes']}
  yes(cap.selection(h,cv,carry)[cr['path']]==cr,'exact_carry_exception_positive')
  no(lambda:cap.selection(h,{**cv,'files':[{**cr,'sha256':'f'*64}]},carry),'carry_pin_drift')
  baseline={**h.baseline_facts(),**h.source_baseline(),'dated_eligible_total':99,'active_publication_DOI':'10.5281/zenodo.23390551','active_tracker_range':"'Math Puzzles'!A105:D105",'stale_unknown_publication_field':'remove me'}
  native={p:None for p in h.VIEWS};local=dict(native);native[h.VIEWS[2]]=enc(baseline);local[h.VIEWS[2]]=enc(baseline)
  native[h.VIEWS[1]]=b'case prefix\n';local[h.VIEWS[1]]=b'case prefix\nlocal extension\n';native[h.VIEWS[4]]=b'program prefix\n<!-- PR214_NATIVE_PHASE_FACTS history -->\n';local[h.VIEWS[4]]=b'program prefix\n'
  views=cap.postimages(h,{'scientific_disposition':'explicit synthetic accepted disposition'},native,local,'2026-10-18T01:35:00Z')
  progress=h.decode(views[h.VIEWS[2]]);casepost=h.decode(views[h.VIEWS[0]])
  yes(progress['fully_completed_count']==55 and progress['published_count']==39 and progress['next_numeric_intake_cursor']==219 and progress['advance_to_next_PR_authorized_now'] is False,'postimages_conditional55_39_219_only')
  yes(progress['active_publication_DOI']==h.EXISTING_DOI and progress['active_tracker_range']==h.EXISTING_TRACKER and 'stale_unknown_publication_field' not in progress,'whitelist_replaces214_publication_fields')
  yes(casepost['PR']==218 and casepost['problem_id']=='30006020','casepost_exact_case_identity')
  yes(all(h.exact(progress[k],v+[218]) for k,v in h.source_baseline().items()),'memberships_exact_baseline_plus218')
  yes(views[h.VIEWS[1]].startswith(local[h.VIEWS[1]]) and views[h.VIEWS[4]].startswith(native[h.VIEWS[4]]),'both_longer_native_local_log_prefixes_preserved')
  for p in (h.VIEWS[1],h.VIEWS[3],h.VIEWS[4]):h.markdown_current(views[p],'completion100',p!=h.VIEWS[3])
  yes(True,'all_postimage_markers_real_validator')
  for left,right in ((b'a',b'b'),(1,b'a')):no(lambda left=left,right=right:cap.merge_prefix(left,right),'divergent_or_nonbyte_prefix_'+str(left))
  for state in ('native','local'):
   wrong=copy.deepcopy(native if state=='native' else local);wrong[h.VIEWS[2]]=enc({**baseline,'fully_completed_count':55})
   no(lambda wrong=wrong,state=state:cap.postimages(h,{'scientific_disposition':'synthetic'},wrong if state=='native' else native,wrong if state=='local' else local,'2026-10-18T01:35:00Z'),'independent_'+state+'_baseline_change')
  wrong=copy.deepcopy(local);wrong[h.VIEWS[1]]=h.phase_marker()+b'\n'
  no(lambda:cap.postimages(h,{'scientific_disposition':'synthetic'},native,wrong,'2026-10-18T01:35:00Z'),'existing218_marker_refused')
  tree_node={'mode':'040000','type':'tree','sha':'a'*40};yes(h.preserved_tuple(tree_node,tree_only=True)==('040000','tree','a'*40),'correct_opaque_tree_validator_positive');no(lambda:h.tuple_pin(tree_node),'blob_tuple_helper_cannot_accept_tree')
  c=h.core();root=c.tree_hash([])
  def observer(method,route,body=None):
   need(method=='GET' and route=='git/trees/'+root and body is None,'Owned local empty native tree only');return {'sha':root,'truncated':False,'tree':[]}
  trees=c.NativeTrees(observer);payload={**views,path:b'owned public fixture\n'};pre={p:None for p in payload};identity={'_capture_queue':{'mode':'100644','type':'blob','sha':'b'*40},'own_Main_QUEUE_row_pin':pin(b'own\n'),'protected_nodes':{},'protected_bodies':[],'current_PR_opaque_body_pin':pin(b'opaque')}
  fixture_ref={'path':str(origin),**pin(origin.read_bytes())};manifest,sources=cap.materialize_manifest(h,payload,pre,local,'private_packet218_test',identity,{},fixture_ref,fixture_ref,{},[],trees,root)
  yes(manifest['total_files']==6 and manifest['facts']['advance_to_next_PR_authorized_now'] is False and all(n.startswith('private_packet218_test/') for n in sources),'pure_manifest_sixviews_private_staging_only')
  yes([r['path'] for r in manifest['local_views']]==list(h.VIEWS) and len(manifest['expected_changed_paths'])==6,'separate_ordered_local_preimages_and_exact_native_changes')
  empty_manifest,empty_sources=cap.materialize_manifest(h,{**payload,path:b''},pre,local,'private_packet218_empty',identity,{},fixture_ref,fixture_ref,{},[],trees,root)
  yes(any(r['path']==path and r['bytes']==0 for r in empty_manifest['files']) and all(len(views[p])>0 for p in h.VIEWS),'legitimate_empty_public_nonview_with_nonempty_five')
  badpre={**pre,path:('100644','blob','f'*40)};no(lambda:cap.materialize_manifest(h,payload,badpre,local,'private_packet218_test',identity,{},fixture_ref,fixture_ref,{},[],trees,root),'nonview_native_overwrite_refused')
  for bad,label in ((b'bad\0body','NUL'),(b'\xff','nonUTF8')):
   no(lambda bad=bad:cap.materialize_manifest(h,{**payload,path:bad},pre,local,'private_packet218_test',identity,{},fixture_ref,fixture_ref,{},[],trees,root),'selected_'+label)
  readonly=case/'readonly.md';put(readonly,b'fixture\n');yes(cap.read_regular(readonly)[0]==b'fixture\n','readonly0444_positive');readonly.chmod(0o644);no(lambda:cap.read_regular(readonly),'mutable_mode_refused');readonly.chmod(0o444)
  link=case/'symlink.md';link.symlink_to(readonly);no(lambda:cap.read_regular(link),'symlink_refused')
  yes(cap.read_regular(case/'absent.md',absent=True)==(None,None),'explicit_absent_local_preimage')
  probe=C/'inert_probe.py';put(probe,b'VALUE=7\n');yes(cap.load('owned_inert_probe',probe,pin(probe.read_bytes())).VALUE==7,'exact_pinned_inert_module_loader');no(lambda:cap.load('bad_pin_probe',probe,{'bytes':8,'sha256':'f'*64}),'changed_module_pin_refused')
  class OwnedAPI:
   """Explicit local envelope/cache dependency, never the real primitive API."""
   def __init__(self,model,journal,mutate):
    need(mutate is False,'Only readonly fixture dependency');self.journal=journal;self.number=0;self.actual_GET_origins={};self.kind='valid';self.origin_pin=None
   def __call__(self,method,route,body=None):
    self.number+=1;name=str(self.number).zfill(5);value={'sha':'a'*40,'fixture':True}
    if self.number>1 and self.kind=='valid':
     put(self.journal/(name+'.IMMUTABLE_GET_CACHE_HIT.json'),enc({'method':'GET','path':route,'request_pin':None,'canonical_cache_pin':pin(enc(value)),'actual_response_origin':{'receipt':'00001.API_RECEIPT.json','actual_stdout_pin':self.origin_pin}}));return value
    if self.kind=='missing':return value
    stdout=enc(value if self.kind!='wrong_raw' else {'sha':'a'*40,'fixture':False});stderr=b'warning' if self.kind=='stderr' else b''
    op=self.journal/(name+'.RAW_STDOUT.json');ep=self.journal/(name+'.RAW_STDERR.txt');put(op,stdout);put(ep,stderr);self.origin_pin=pin(stdout)
    receipt={'method':'GET','path':route,'request_pin':None,'exit':0,'stdout_pin':pin(stdout),'stderr_pin':pin(stderr),'raw_stdout':{'path':str(op),**pin(stdout)},'raw_stderr':{'path':str(ep),**pin(stderr)}}
    put(self.journal/(name+'.API_RECEIPT.json'),enc(receipt));return value
  dependency=types.SimpleNamespace(API=OwnedAPI,enc=enc);journal=C/'_synthetic_GET_valid';journal.mkdir();guards=[];api=cap.GET(h,dependency,journal,lambda:guards.append('source'))
  route='git/trees/'+'a'*40;first=api('GET',route);wire=api.wire;second=api('GET',route)
  yes(first==second and api.calls==2 and wire==len(enc(first)) and api.wire==wire and len(api.seen_receipts)==1 and guards==['source','source'],'real_GET_wrapper_retained_origin_and_cache_count_once')
  no(lambda:api('POST',route,{}),'GET_wrapper_POST_refused')
  for kind,route2 in (('missing','git/ref/heads/main'),('wrong_raw',route),('stderr',route)):
   journal2=C/('_synthetic_GET_'+kind);journal2.mkdir();subject=cap.GET(h,dependency,journal2,lambda:None);subject.inner.kind=kind
   no(lambda subject=subject,route2=route2:subject('GET',route2),'wrapper_refuses_'+kind)
   yes(subject.failed is True,'wrapper_failure_poisoned_'+kind);calls=subject.inner.number;no(lambda subject=subject,route2=route2:subject('GET',route2),'wrapper_no_retry_'+kind);yes(subject.inner.number==calls,'no_second_dispatch_'+kind)
  api.calls=cap.MAX_GETS;no(lambda:api('GET',route),'GET_wrapper_call_bound')
  for kind in ('wire_cap','deadline','source_revoked'):
   j=C/('_synthetic_GET_bound_'+kind);j.mkdir()
   def revoked():raise RuntimeError('Owned source gate revoked')
   subject=cap.GET(h,dependency,j,revoked if kind=='source_revoked' else lambda:None)
   if kind=='wire_cap':subject.wire=cap.MAX_WIRE
   if kind=='deadline':subject.deadline=0
   no(lambda subject=subject:subject('GET',route),'GET_wrapper_'+kind)
   yes(subject.inner.number==(1 if kind=='wire_cap' else 0),'GET_bound_dispatch_count_'+kind)
  parsed=ast.parse(own);calls=[n for n in ast.walk(parsed) if isinstance(n,ast.Call)]
  yes(not any(isinstance(n.func,ast.Attribute) and n.func.attr in ('Seed','Runtime','WriterLock') for n in calls),'no_Seed_Runtime_or_lock_invocation_in_source')
  yes(any(isinstance(n.func,ast.Attribute) and n.func.attr=='preserved_tuple' and any(k.arg=='tree_only' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords) for n in calls),'actual_source_opaque_tree_uses_tree_only_validator')
  gate_calls=[n for n in calls if isinstance(n.func,ast.Attribute) and n.func.attr=='matches' and n.args and isinstance(n.args[0],ast.Name) and n.args[0].id=='acceptance']
  yes(len(gate_calls)==1 and isinstance(gate_calls[0].args[1],ast.Dict),'single_actual_capture_gate_contract')
  expression=ast.Expression(copy.deepcopy(gate_calls[0].args[1]));ast.fix_missing_locations(expression)
  environment={'source_pin':bound['capture_source_pin'],'own_manifest_ref':{'path':'owned-manifest',**bound['capture_manifest_pin']},'selected_ref':fixture_ref,'ENGINE_MANIFEST_PIN':cap.ENGINE_MANIFEST_PIN}
  expected=eval(compile(expression,'owned_actual_capture_gate_contract','eval'),environment)
  yes(h.exact(expected.get('selection_reference'),fixture_ref),'actual_gate_binds_exact_selected_reference')
  h.matches(copy.deepcopy(expected),expected,'Owned synthetic typed capture gate');yes(True,'actual_gate_contract_positive_without_capture_run')
  wrong=copy.deepcopy(expected);wrong['selection_reference']={**fixture_ref,'sha256':'f'*64};no(lambda:h.matches(wrong,expected,'Owned synthetic wrong selection'),'capture_gate_other_plan_pin_refused')
  missing=copy.deepcopy(expected);missing.pop('selection_reference');no(lambda:h.matches(missing,expected,'Owned missing selected ref'),'capture_gate_missing_selection_refused')
 yes(pin((SOURCE/'SOURCE_MANIFEST.json').read_bytes())==bound['capture_manifest_pin'],'frozen_capture_subject_unchanged')
 return {'schema':'pr218-independent-logical-capture-source-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'PURE_OWNED_COMPONENTS_ONLY_NO_CAPTURE_ENTRYPOINT','checks':len(RESULTS),'positive':sum(r['kind']=='positive' for r in RESULTS),'expected_refusals':sum(r['kind']=='refusal' for r in RESULTS),'all_passed':True,'results':RESULTS,'actual_capture_API_Seed_Runtime_original_lock_global_five_or_any_native_effect':False,'limitations':['No capture run/main or GET transport invoked.','Pure composition and readonly descriptor controls run against exact owned copies; full actual packet and current native/local observations remain separate.']}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))

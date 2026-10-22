"""Independent PR214 focused actual-source controls. Owned fixtures only.
No production CLI/transport/global-five/original-lock/native/provider/ref/PR actions.
Full local publisher is exercised via explicit local_ops/callback seams; other
controls exercise real pure gates, protected/native body paths and source reader.
This is not a full actual Runtime/admission/CAS/inspect roundtrip.
"""
from pathlib import Path
import copy,datetime,hashlib,json,os,socket,subprocess,sys,tempfile,types
D=Path(__file__).absolute().parent
S=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/native_completion_preparation_02")
CHECKS=[]
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(o):return (json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def yes(v,n):
    if type(v)is not bool or not v:raise AssertionError(n)
    CHECKS.append({'test':n,'outcome':'PASS'})
def no(fn,n):
    try:fn()
    except (RuntimeError,ValueError,TypeError,KeyError,OSError)as e:CHECKS.append({'test':n,'outcome':'EXPECTED_REFUSAL','exception':type(e).__name__,'reason':str(e)[:220]});return e
    raise AssertionError('Unexpected acceptance '+n)
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb')as f:f.write(b)
    p.chmod(0o444);return {'path':str(p),**pin(b)}
def module(p):
    m=types.ModuleType('own_'+p.stem);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def deny(*a,**k):raise AssertionError('Actual process/network forbidden')
def fixture(root):
    b=root/'draft_pr_publication_program_20260930/audits/pr214_30005244/native_completion_preparation_02';b.mkdir(parents=True)
    m=json.loads((S/'SOURCE_MANIFEST.json').read_bytes())
    for n in [r['path']for r in m['files']]+['SOURCE_MANIFEST.json','SOURCE_EXTERNAL_SEAL.json']:write(b/n,(S/n).read_bytes())
    return b,module(b/'native214_model.py'),module(b/'completion_checkpoint.py'),module(b/'native214_primitives.py'),module(b/'ROOT_TERMINAL_INSPECTION.py'),module(b/'concurrent_get_extension.py')

def scope_and_gate(b,h,q,e,t,x):
    a=t.source_closure()
    yes(a[0]==pin((b/'ROOT_TERMINAL_INSPECTION.py').read_bytes())and a[1]==pin((b/'SOURCE_MANIFEST.json').read_bytes()),'complete_shared18_source_closure_reader')
    for prefix in ['ROOT_COMPLETE214_CANDIDATE_X','ROOT_COMPLETE214_READ_X','ROOT_COMPLETE214_SYNC_X','ROOT_COMPLETE214_FAST_READ_X','ROOT_COMPLETE214_FAST_WORK_abc_0','ROOT_COMPLETE214_READ_ROOT_TERMINAL_X','ROOT_ADMIN214_READ_X']:
        for p in [prefix,prefix.lower(),prefix.swapcase()]:
            yes(h.public_path(h.CASE+'native_completion_preparation_02/outer/'+p+'/00001.RAW_STDOUT.json')is False,'raw_operational_scope_refused_'+p)
    yes(h.public_path(h.CASE+'native_completion_preparation_02/native214_model.py')is True,'legitimate_public_source_allowed')
    for path in [h.ATTEMPT+'/science.txt',h.SHARED+'/science.json',h.QUEUE]:
        yes(h.public_path(path)is False,'protected_or_QUEUE_not_public_overlay_'+path)
    refs={k:{'path':str(b.parent/(k+'.json')),'bytes':2,'sha256':pin(b'{}')['sha256']}for k in ['math','custody','priority','adoption']}
    native={'path':str(b.parent/'NATIVE.json'),'bytes':2,'sha256':pin(b'{}')['sha256']}
    ready={'schema':'pr214-root-case-ready-adoption-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':214,'accepted':True,
      'mathematical_review_accepted':True,'priority_review_accepted':True,'existing_publication_adoption_accepted':True,
      'two_sequential_fresh_whole_package_reviews_accepted':True,'original_and_current_claimed_solved_eligibility_preserved':True,
      'already_merged_original_PR_verified':True,'existing_DOI_and_unique_tracker_row_reused':True,
      'no_new_provider_publication_or_tracker_append':True,'existing_scientific_package_frozen':True,'prior_PR213_status_only_skip_accepted':True,
      'native_identity_receipt':native,'current_head':h.CURRENT,'original_merge_commit':h.MERGED,
      'existing_publication_DOI':h.EXISTING_DOI,'existing_tracker_range':h.EXISTING_TRACKER,'evidence_references':refs,'numeric_advance_authorized_by_this_file':False}
    h.validate_ready_value({'native_identity_receipt':native},refs,ready);yes(True,'complete_synthetic_case_ready_leaf')
    for key,val in list(ready.items()):
        if val is not True:continue
        for alt in [None,False,1,1.0]:
            bad=copy.deepcopy(ready)
            if alt is None:bad.pop(key)
            else:bad[key]=alt
            no(lambda bad=bad:h.validate_ready_value({'native_identity_receipt':native},refs,bad),'ready_required_'+key+'_'+repr(alt))
    for key,val in [('PR',214.0),('current_head',h.ORIGINAL),('original_merge_commit',h.CURRENT),('existing_publication_DOI','10.1/other'),('existing_tracker_range',h.EXISTING_TRACKER+'x'),('numeric_advance_authorized_by_this_file',True),('numeric_advance_authorized_by_this_file',0)]:
        no(lambda key=key,val=val:h.validate_ready_value({'native_identity_receipt':native},refs,{**ready,key:val}),'ready_identity_or_false_alias_'+key+'_'+repr(val))
    policy=t.transport_policy({'extension_source':None,'extension_acceptance':None})
    gate={'schema':t.SOURCE_SCHEMA,'evidence_scope':'ACTUAL_ROOT_RECEIPT_SOURCE_ONLY','PR':214,'accepted':True,
      'terminal_source_pin':a[0],'terminal_source_manifest_pin':a[1],'approved_driver_pin':t.DRIVER_PIN,'receipt_schema':t.RECEIPT_SCHEMA,
      'Root_full_source_read':True,'independent_source_review_accepted':True,'transport_policy':policy,'source_acceptance_is_not_actual_terminal_or_numeric_authority':True}
    t.check_source_acceptance(gate,*a,policy);yes(True,'terminal_source_gate_full_typed_positive')
    for key in gate:
        bad=copy.deepcopy(gate);bad.pop(key)
        no(lambda bad=bad:t.check_source_acceptance(bad,*a,policy),'terminal_source_gate_missing_'+key)
    for key,val in [('accepted',1),('PR',214.0),('evidence_scope','ACTUAL_ROOT_RECEIPT'),('source_acceptance_is_not_actual_terminal_or_numeric_authority',False)]:
        no(lambda key=key,val=val:t.check_source_acceptance({**gate,key:val},*a,policy),'source_gate_alias_'+key)
    source=b/'native214_model.py';old=source.read_bytes();source.chmod(0o644)
    no(t.source_closure,'shared_source_writable_mode_refused');source.chmod(0o444)
    source.chmod(0o644);source.write_bytes(old+b' ');source.chmod(0o444)
    no(t.source_closure,'shared_source_body_drift_refused');source.chmod(0o644);source.write_bytes(old);source.chmod(0o444)

def signed_and_counts(b,h,q,e,t,x):
    raw=b'tree '+b'a'*40+b'\nparent '+b'b'*40+b'\nparent '+b'c'*40+b'\nauthor A <a@a> 1 +0000\ncommitter A <a@a> 1 +0000\ngpgsig signed\n body\n \n\nmessage\n'
    ref=write(b/'own_signed_raw.txt',raw);row={'sha':h.native('commit',raw),'tree':'a'*40,'parents':['b'*40,'c'*40],'raw_commit':ref}
    h.authenticated_commit(row);yes(True,'verbatim_signed_raw_two_ordered_parents')
    for k,v in [('parents',list(reversed(row['parents']))),('tree','d'*40),('sha','e'*40)]:
        no(lambda k=k,v=v:h.authenticated_commit({**row,k:v}),'signed_association_'+k)
    altered=write(b/'own_refolded_raw.txt',raw.replace(b'\n \n\n',b'\n\n'))
    no(lambda:h.authenticated_commit({**row,'raw_commit':altered}),'same_declared_SHA_refolded_empty_signature_line_refused')
    baseline=h.source_baseline();facts=h.phase_facts();case={**facts,'conditional_proposal_only':True};progress={**case,**h.completion_memberships(),'dated_eligible_total':99}
    t.accounting(h,{'facts':facts},case,progress,baseline);yes(True,'strict_adoption_accounting54_38_baseline_plus214')
    for k,v in [('fully_completed_count',54.0),('published_count',38.0),('workflow_percent',100.0),('completed',1),('numeric_advance_conditional_on_actual_Root_terminal',False),('advance_to_next_PR_authorized_now',True)]:
        no(lambda k=k,v=v:t.accounting(h,{'facts':facts},{**case,k:v},progress,baseline),'five_proposal_alias_or_false_authority_'+k)
    for key in baseline:
        for values in [baseline[key],baseline[key]+[212,214],baseline[key]+[213,214],baseline[key]+[214,214]]:
            no(lambda key=key,values=values:t.accounting(h,{'facts':facts},case,{**progress,key:values},baseline),'membership_exact_'+key+'_'+str(len(values)))

class Observer:
    def __init__(self,b,h,data):
        self.b,self.h,self.data=b,h,data;self.actual_GET_origins={};self.calls=[];self.missing=False
    def __call__(self,method,path,body=None):
        if method!='GET'or body is not None or not path.startswith('git/blobs/'):raise AssertionError('Unexpected synthetic observer route')
        oid=path.rsplit('/',1)[1];raw=self.data[oid];self.calls.append(oid)
        import base64
        value={'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
        prefix=str(len(self.calls));out=write(self.b/(prefix+'.RAW.json'),enc(value));err=write(self.b/(prefix+'.ERR.txt'),b'')
        receipt={'method':'GET','path':path,'exit':0,'raw_stdout':out,'raw_stderr':err}
        r=write(self.b/(prefix+'.RECEIPT.json'),enc(receipt))
        if not self.missing:self.actual_GET_origins[path]={'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math','route':path,
          'raw_response':out,'raw_stderr':err,'receipt':r['path'],'receipt_pin':{k:r[k]for k in ['bytes','sha256']}}
        return value

def protected_bodies(b,h,q,e,t,x):
    cells=[b'',b'214',b'30005244 / OWR-11101924-008',b'a',b'b',b'c',b'd',b'e',b'claimed_solved',b'2/5',b'f',b'g',b'h',b'']
    row=b'|'.join(cells)+b'\n';queue=b'# owned synthetic QUEUE\n'+row;science=b'owned existing scientific body\n';post=b'owned positive audit artifact\n'
    qo,so,po=[h.native('blob',v)for v in [queue,science,post]];path=h.ATTEMPT+'/science.txt';out=h.CASE+'AUDIT.md'
    data={qo:queue,so:science,po:post}
    m={'protected_nodes':{h.ATTEMPT:{'mode':'040000','type':'tree','sha':'a'*40},h.SHARED:None},
      'protected_bodies':[{'path':path,'mode':'100644','type':'blob','sha':so,**pin(science)}],
      'protected_queue':{'mode':'100644','type':'blob','sha':qo},'protected_queue_row_pin':pin(row)}
    mapping={h.ATTEMPT:('040000','tree','a'*40),path:('100644','blob',so),h.QUEUE:('100644','blob',qo),out:('100644','blob',po)}
    trees=types.SimpleNamespace(lookup=lambda root,p:mapping.get(p))
    rt=types.SimpleNamespace(h=h,m=m,overlay={out:post},pre={out:None},pool=h.NativeBodyProofs())
    api=Observer(b/'native_good',h,data)
    selected,qu=q.body_associations(rt,api,trees,'b'*40,True)
    yes(len(selected)==1 and so in api.calls and po in api.calls and qo in api.calls,'new_scientific_protected_body_loop_uses_full_retained_native_GET_origins')
    yes(rt.pool.origin(api,so)['route']=='git/blobs/'+so,'science_path_SHA_body_origin_association')
    mapping[path]=('100755','blob',so)
    no(lambda:q.body_associations(rt,api,trees,'b'*40,True),'protected_science_mode_drift_refused');mapping[path]=('100644','blob',so)
    mapping[h.ATTEMPT]=('040000','tree','c'*40)
    no(lambda:q.body_associations(rt,api,trees,'b'*40,True),'opaque_science_tree_drift_refused');mapping[h.ATTEMPT]=('040000','tree','a'*40)
    m['protected_bodies'][0]['sha256']='0'*64;rt.pool=h.NativeBodyProofs()
    no(lambda:q.body_associations(rt,Observer(b/'bad_science_pin',h,data),trees,'b'*40,True),'same_native_science_wrong_expected_SHA256_refused')
    m['protected_bodies'][0].update(pin(science));rt.pool=h.NativeBodyProofs();ap=Observer(b/'missing_origin',h,data);ap.missing=True
    no(lambda:q.body_associations(rt,ap,trees,'b'*40,True),'source_bytes_without_retained_actual_shaped_origin_refused')

def publication(root):
    for case in ['success','pending_file_fsync','pending_directory_fsync','mutable_guard','link_before','link_after','published_directory_fsync','identity_first','cleanup_directory_fsync','identity_second','racing_existing']:
        b,h,q,e,t,x=fixture(root/case);path=t.A/'ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json';calls=[];fs=[0];ident=[0];links=[0]
        class Ops:
            def fsync(self,fd):
                fs[0]+=1
                target={'pending_file_fsync':1,'pending_directory_fsync':2,'published_directory_fsync':3,'cleanup_directory_fsync':4}.get(case)
                if target==fs[0]:raise OSError('owned fsync '+case)
                return os.fsync(fd)
            def link(self,*a,**kw):
                links[0]+=1
                if case=='link_before':raise OSError('owned link before syscall')
                if case=='racing_existing':write(path,b'owned concurrent other final\n')
                os.link(*a,**kw)
                if case=='link_after':raise OSError('owned link result uncertainty after syscall')
            def unlink(self,*a,**kw):return os.unlink(*a,**kw)
        def mutable():
            calls.append('mutable')
            if case=='mutable_guard':raise RuntimeError('owned changed mutable prerequisite')
        def identity():
            calls.append('identity');ident[0]+=1;t.source_closure()
            if case=='identity_first'and ident[0]==1:raise RuntimeError('owned source/lock identity fault1')
            if case=='identity_second'and ident[0]==2:raise RuntimeError('owned source/lock identity fault2')
        if case=='success':
            result=t.exclusive_root_receipt(e,path,b'owned fixture publication only\n',mutable,identity,local_ops=Ops())
            yes(result['exclusive_atomic_publication']is True and calls==['mutable','identity','identity'],'entire_local_publisher_exact_success_guard_order')
            no(lambda:t.exclusive_root_receipt(e,path,b'other\n',mutable,identity),'existing_fixed_terminal_never_overwritten')
        else:
            error=no(lambda:t.exclusive_root_receipt(e,path,b'owned fixture publication only\n',mutable,identity,local_ops=Ops()),'publisher_failure_'+case)
            post=case in ['link_before','link_after','published_directory_fsync','identity_first','cleanup_directory_fsync','identity_second','racing_existing']
            yes(isinstance(error,t.TerminalPublicationUncertain)==post,'publication_uncertainty_class_'+case)
            expected=post and case!='link_before'
            yes(path.exists()==expected,'final_presence_truthful_'+case)
            if post:yes(error.details['automatic_retry_overwrite_or_unlink_final_forbidden']is True,'no_automatic_retry_or_unlink_'+case)
            if expected:
                old=path.read_bytes()
                no(lambda:t.exclusive_root_receipt(e,path,b'new\n',mutable,identity),'uncertain_existing_final_refuses_retry_'+case)
                yes(path.read_bytes()==old,'uncertain_final_bytes_preserved_'+case)
            else:yes(links[0]==(1 if case=='link_before'else 0),'prepublication_failure_no_final_link_'+case)

def run():
    expected={'bytes':3105,'sha256':'a1f2fd7a1749af748add130a6ad2e3961e476a7ea48f069c9e927a2f035b5ad3'}
    yes(pin((S/'SOURCE_MANIFEST.json').read_bytes())==expected,'Root_exact_final02_manifest')
    m=json.loads((S/'SOURCE_MANIFEST.json').read_bytes());yes(len(m['files'])==18 and sum(r['bytes']for r in m['files'])==233728,'final18_payload_scope')
    for r in m['files']:yes(pin((S/r['path']).read_bytes())=={k:r[k]for k in ['bytes','sha256']},'final02_payload_'+r['path'])
    socket.socket=deny;socket.create_connection=deny;subprocess.Popen=deny
    with tempfile.TemporaryDirectory(prefix='_owned_pr214_',dir=D)as tmp:
        root=Path(tmp);parts=fixture(root/'predicates')
        scope_and_gate(*parts);signed_and_counts(*parts);protected_bodies(*parts)
        publication(root/'publication')
    from collections import Counter
    return {'schema':'pr214-independent-focused-actual-source-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
      'source_manifest_pin':expected,'checks':CHECKS,'check_count':len(CHECKS),'outcome_counts':dict(Counter(r['outcome']for r in CHECKS)),
      'whole_local_exclusive_publisher_effect_path_exercised':True,'production_immutable_case_gates_and_full_Runtime_inspect_roundtrip_exercised':False,
      'adaptations':['owned_source_checkout','explicit_publisher_local_ops_and_callbacks','retained_raw_synthetic_observer'],
      'no_production_source_module_global_monkeypatches':True,'actual_network_Git_native_original_lock_currentfive_ref_PR_provider_intake_effects':False,
      'limits':'Full frozen source/deltas/AST read; focused real predicate/native body/source reader/local publisher execution with explicit synthetic prerequisites. No actual logical packet/admission/CAS, full inspect, original-lock or five sync evidence; separate full-inspect integration remains a Root acceptance prerequisite.'}
if __name__=='__main__':
    if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Use -E -S -B -P')
    print(json.dumps(run(),indent=2,sort_keys=True))


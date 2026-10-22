"""Independent actual-source concurrent GET controls; own isolated fixtures only.
Final binding file must pin the complete reviewed producer closure before execution.
Fixture adaptations: original deterministic transport and owned lock-inode adapter,
controlled clocks/events, and explicitly named scoped fault-injection hooks.
No new actual network, Git, original lock, native object, ref or global-five effects.
"""
from pathlib import Path
import ast,base64,copy,datetime,hashlib,json,os,socket,subprocess,sys,tempfile,threading,time,types
X=Path(__file__).absolute().parent
A=X.parent
Y=A/'root_concurrent_get_source_01'
OLD=A/'native_source_adversary_01'/'independent_source_controls.py'
CHECKS=[];FIXTURE_ERRORS=[]
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def need(ok,label):
    if type(ok)is not bool or not ok:raise AssertionError(label)
def yes(ok,label):need(ok,label);need(not FIXTURE_ERRORS,str(FIXTURE_ERRORS));CHECKS.append({'test':label,'outcome':'PASS'})
def no(fn,label,text=None):
    try:fn()
    except (RuntimeError,ValueError,TypeError,KeyError,OSError)as e:
        need(not FIXTURE_ERRORS,str(FIXTURE_ERRORS))
        if text is not None:need(text in str(e),'Wrong refusal for '+label+': '+str(e))
        CHECKS.append({'test':label,'outcome':'EXPECTED_REFUSAL','exception':type(e).__name__,'reason':str(e)[:220]})
    else:raise AssertionError('Unexpected acceptance: '+label)
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():p.chmod(0o644)
    p.write_bytes(b);p.chmod(0o444)
def module(p):
    m=types.ModuleType('owned_'+p.stem);m.__file__=str(p)
    exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def deny(*a,**k):raise AssertionError('Real process/network action forbidden')
def support():
    need(pin(OLD.read_bytes())=={'bytes':38836,'sha256':'00422b06b36aa9c29899e98ef0ee0e52e71b5a77edfe72b5262c6c1f1d55d078'},'Frozen prior own fixture support')
    return module(OLD)
S=None
class F:
    def __init__(self,root,workers=8,extra=False):
        self.f=S.F(root,extra=extra);f=self.f
        self.d=f.case/'root_concurrent_get_source_01';self.d.mkdir()
        manifest=json.loads((Y/'SOURCE_MANIFEST.json').read_bytes())
        for n in [r['path']for r in manifest['files']]+['SOURCE_MANIFEST.json']:
            write(self.d/n,(Y/n).read_bytes())
        self.x=module(self.d/'concurrent_get_extension.py')
        self.aux=[]
        oids={f.logical['protected_queue']['sha'],f.h.CURRENT_QUEUE}
        for p in [f.h.VIEWS[2],f.h.VIEWS[1],f.h.VIEWS[4]]:
            if f.pre[p]is not None:oids.add(f.pre[p][2])
        for oid in sorted(oids):self.aux.append({'oid':oid,**pin(f.blobs[oid])})
        self.aux_ref=f.record('auxiliary.json',{'schema':'pr212-concurrent-GET-auxiliary-blob-pins-v1','PR':212,'files':self.aux},annotate=False)
        self.gate={'schema':'pr212-root-concurrent-GET-extension-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
          'PR':212,'accepted':True,'extension_pin':pin((self.d/'concurrent_get_extension.py').read_bytes()),
          'extension_source_manifest_pin':pin((self.d/'SOURCE_MANIFEST.json').read_bytes()),
          'protocol_pin':self.x.PROTOCOL_PIN,'protocol_source_manifest_pin':self.x.PROTOCOL_MANIFEST_PIN,
          'logical_manifest_pin':f.seed.manifest_pin,'logical_gate_pin':f.seed.logical_gate_pin,
          'admission_pin':f.rt.admission_pin,'admission_gate_pin':f.rt.gate_pin,'Root_full_source_read':True,
          'independent_source_adversarial_review_accepted':True,'fresh_actual_parameter_bindings_accepted':True,
          'old_logical_packet_and_source_identity_unchanged':True,'actual_native_GET_transport_extension_explicitly_accepted':True,
          'only_existing_inherited_per_admission_effect_authority':True,'no_ref_PR_or_global_five_authority_added':True,
          'original_driver_CLI_execution_claimed':False,'old_sync_and_hold_CAS_invoked_unchanged':True,
          'candidate_two_POST_orchestration_delta_reviewed':True,'allowed_operations':['candidate','hold-CAS','sync','terminal','verify'],
          'workers':workers,'auxiliary_blob_pins':self.aux_ref}
        self.set_gate()
        rawtransport=f.e.run_bounded
        def checked_transport(argv,request):
            try:return rawtransport(argv,request)
            except AssertionError as e:FIXTURE_ERRORS.append(str(e));raise
        f.e.run_bounded=checked_transport;self.transport=checked_transport
    def set_gate(self):
        self.gref=self.f.record('extension_gate.json',self.gate)
    def guard(self,op='verify'):
        return self.x.bind_runtime(self.f.v,self.f.rt,self.gref,op)
    def api(self,label,op='verify'):
        g=self.guard(op);j=self.f.e.journal_new('ROOT_ADMIN212_FAST_READ_'+label)
        return g,self.x.make_readonly_api(self.f.v,g,j)

def gate_tests(o):
    f,x=o.f,o.x;g=o.guard()
    yes(g.worker_count==o.gate['workers'] and len(g.specs)>=len({f.h.native('blob',b)for b in f.overlay.values()}),'full_guarded_runtime_binds_original_dynamic_packet')
    original=copy.deepcopy(o.gate)
    for k,v in [('workers',0),('workers',9),('workers',True),('workers',1.0),('workers','8'),
      ('accepted',False),('PR',True),('original_driver_CLI_execution_claimed',True),
      ('Root_full_source_read',False),('old_logical_packet_and_source_identity_unchanged',False),
      ('independent_source_adversarial_review_accepted',False),
      ('only_existing_inherited_per_admission_effect_authority',False),
      ('candidate_two_POST_orchestration_delta_reviewed',False)]:
        o.gate=copy.deepcopy(original);o.gate[k]=v;o.set_gate()
        no(lambda:o.guard('candidate'),'repinned_new_gate_'+k+'_'+str(v))
    for k in ['extension_pin','extension_source_manifest_pin','protocol_pin','protocol_source_manifest_pin',
      'logical_manifest_pin','logical_gate_pin','admission_pin','admission_gate_pin']:
        o.gate=copy.deepcopy(original);o.gate[k]['sha256']='0'*64;o.set_gate()
        no(o.guard,'repinned_wrong_binding_'+k)
    for ops in [[],['verify','verify'],['verify','candidate'],['verify','POST'],['candidate']]:
        o.gate=copy.deepcopy(original);o.gate['allowed_operations']=ops;o.set_gate()
        no(o.guard,'wrong_operation_set_'+str(ops))
    o.gate=original;o.set_gate()

def full_tests(o):
    f,x=o.f,o.x
    g,api=o.api('FULL')
    proof=f.v.verify_immutable(g,api)
    yes(proof['selected_count']==len(f.overlay) and proof['full_scope_verified']and proof['all_selected_native_bodies_verified'],'full_original_verify_immutable_uses_concurrent_actual_origins')
    yes(proof['mutable_Main_observed_or_spoofed']is False and f.ref_reads==0,'immutable_pool_does_not_observe_or_spoof_Main')
    yes(len(api.workers)==o.gate['workers'] and len({str(w.journal)for w in api.workers})==len(api.workers),'distinct_original_worker_API_journals')
    yes(all(type(w)is f.e.API and not w.mutate for w in api.workers),'each_worker_is_original_GETonly_API')
    origins={oid:copy.deepcopy(api.actual_GET_origins.get('git/blobs/'+oid))for oid in g.specs}
    yes(all(v is not None and Path(v['receipt']).parent in {w.journal for w in api.workers}for v in origins.values()),'aggregate_origins_are_actual_current_worker_receipts')
    before=sum(w.number for w in api.workers)
    oid=next(iter(g.specs));v1=api('GET','git/blobs/'+oid);v1['sha']='0'*40
    v2=api('GET','git/blobs/'+oid)
    yes(v2['sha']==oid and before==sum(w.number for w in api.workers),'same_invocation_immutable_reuse_returns_fresh_decode_without_fake_GET')
    g2,api2=o.api('SECOND')
    yes(all(api2.actual_GET_origins.get('git/blobs/'+oid)['receipt']!=v['receipt']for oid,v in origins.items()),'new_invocation_gets_fresh_original_worker_origins')
    child=f.descendant(queue=f.main_queue+f.foreign_row+b'\n',label=b'newforeignQUEUE')
    f.ref=child;closure=f.v.main_closure(g,api)
    yes(closure['actual_MAIN_observed']==child and closure['Main_QUEUE_observation']['observed_QUEUE_oid']!=closure['Main_QUEUE_observation']['parent_QUEUE_oid'],'dynamic_foreign_QUEUE_descendant_full_original_closure')
    yes(closure['Main_QUEUE_observation']['actual_native_body_origin']['receipt'].startswith(str(api.workers[0].journal)+'/'),'new_R_QUEUE_uses_fresh_sequential_worker0_actual_origin')
    hostile=f.descendant(queue=f.head_row+f.foreign_row,label=b'hostileOwnRow');f.ref=hostile
    no(lambda:f.v.main_closure(g,api),'old_native_owned_row_guard_rejects_hostile_descendant_through_new_factory')
    f.ref=f.parent;ref_before=f.ref_reads
    for unused in range(2):api('GET','git/ref/heads/main')
    yes(f.ref_reads==ref_before+2,'mutable_Main_is_fetched_each_time')
    for route,method,body in [('git/ref/heads/main','POST',None),('git/refs/heads/main','GET',None),('https://bad.invalid','GET',None),('pulls/1','GET',None),('git/blobs/'+oid,'GET',{})]:
        g3,ap=o.api('FIREWALL_'+str(len(CHECKS)))
        no(lambda:ap(method,route,body),'actual_composite_route_firewall_'+route+'_'+method)
    no(lambda:x.make_readonly_api(f.v,g, f.b/'OTHER_JOURNAL'),'wrong_main_journal_prefix')
    return proof

def origin_and_failure_tests(o):
    f,x=o.f,o.x
    for kind in ['no_origin','wrong_route','wrong_raw_body','bool_size','wrong_receipt_pin']:
        original_call=f.e.API.__call__
        hit=[False]
        def fault(worker,method,path,body=None,expected_oid=None):
            value=original_call(worker,method,path,body,expected_oid)
            if path.startswith('git/blobs/') and not hit[0]:
                hit[0]=True
                if kind=='no_origin':worker.actual_GET_origins.pop(path,None)
                elif kind=='wrong_route':worker.actual_GET_origins[path]['route']='git/blobs/'+'0'*40
                elif kind=='wrong_raw_body':value['content']=base64.b64encode(b'incorrect native bytes').decode()
                elif kind=='bool_size':value['size']=True
                else:worker.actual_GET_origins[path]['receipt_pin']['sha256']='0'*64
            return value
        f.e.API.__call__=fault
        try:no(lambda:o.api('BAD_'+kind),'actual_original_worker_fault_'+kind)
        finally:f.e.API.__call__=original_call
        yes(hit[0],'owned_worker_fault_reached_'+kind)
    g,api=o.api('ORIGIN_AFTER_POOL')
    oid=next(iter(g.specs));r=api.actual_GET_origins.get('git/blobs/'+oid)
    raw=Path(r['raw_response']['path']);saved=raw.read_bytes()
    write(raw,saved+b' ')
    try:no(lambda:f.v.verify_immutable(g,api),'unchanged_NativeBodyProofs_rechecks_retained_origin_after_pool')
    finally:write(raw,saved)
    # Public proof consumption returns decode copies, not mutable origin dicts.
    g2,api2=o.api('ORIGIN_COPY')
    first=api2.actual_GET_origins.get('git/blobs/'+oid);first['route']='tampered'
    yes(api2.actual_GET_origins.get('git/blobs/'+oid)['route']=='git/blobs/'+oid,'aggregate_origin_mapping_returns_fresh_decode')
    errors=[]
    def other_owner():
        try:api2('GET','git/blobs/'+oid)
        except RuntimeError as e:errors.append(str(e))
    t=threading.Thread(target=other_owner);t.start();t.join(5)
    yes(not t.is_alive()and bool(errors),'aggregate_only_original_owner_consumes_after_join')
    no(lambda:api2('GET','git/blobs/'+oid),'failed_aggregate_never_retries')

def candidate_fault(root,kind):
    o=F(root,workers=4);f,x=o.f,o.x
    if kind=='between_POSTs':
        f.ref_hook=lambda n:f.parent if n<5 else 'f'*40
    elif kind=='after_both_POSTs':
        original=f.e.run_bounded
        def fault(argv,request):
            if len(f.posts)==2 and argv[5]=='GET'and argv[6].startswith('repos/AlecKriebel/Math/git/blobs/'):
                return types.SimpleNamespace(returncode=1,stdout=b'{}\n',stderr=b'owned synthetic read failure')
            return original(argv,request)
        f.e.run_bounded=fault
    else:raise AssertionError(kind)
    no(lambda:x.candidate(f.v,o.guard('candidate')),'actual_candidate_failure_'+kind)
    journal=f.b/f.admission['candidate_journal']
    known=[json.loads(p.read_bytes())for p in journal.glob('*.OBJECT_RESULT.json')]
    wanted=1 if kind=='between_POSTs'else 2
    yes(len(f.posts)==wanted and len(known)==wanted,'truthful_known_immutable_POST_count_'+kind)
    yes(not (journal/'IMMUTABLE_CANDIDATE_VERIFIED.json').exists(),'no_successful_candidate_proof_after_'+kind)
    need((f.b/'_private_candidate_oid_ledger'/(f.target+'.json')).exists(),'Permanent original canonicalOID ledger')
    # Even an accepted new admission/journal cannot redispatch the same OID.
    f.ref_hook=None;f.ref=f.parent
    f.admission={**f.admission,'candidate_journal':'ROOT_ADMIN212_CANDIDATE_NEW_ACCEPTED_JOURNAL'}
    f.ar=f.record('new_admission.json',f.admission,annotate=False)
    f.ag={**f.ag,'admission_pin':pin(enc(f.admission))}
    f.gr=f.record('new_old_gate.json',f.ag);f.rt=f.v.Runtime(f.seed,f.ar,f.gr)
    o.gate['admission_pin']=f.rt.admission_pin;o.gate['admission_gate_pin']=f.rt.gate_pin;o.set_gate()
    no(lambda:x.candidate(f.v,o.guard('candidate')),'new_wrapper_same_OID_new_admission_and_journal_refused_'+kind)
    yes(len(f.posts)==wanted,'same_candidate_no_additional_POST_'+kind)

def unit_workers(o,n,label):
    return [o.f.e.API(o.f.h,o.f.e.journal_new('ROOT_ADMIN212_FAST_WORK_UNIT_'+label+'_'+str(i)),mutate=False)for i in range(n)]
def unit_specs(o,n):
    return {o.f.blob(('owned tiny body '+str(i)).encode()):pin(('owned tiny body '+str(i)).encode())for i in range(n)}

def resource_and_deadline_tests(o):
    f,x=o.f,o.x;specs=unit_specs(o,12);original=f.e.run_bounded;cap=x.MAX_CANONICAL
    def padded(argv,request):
        r=original(argv,request);v=f.h.decode(r.stdout);v['extra_untrusted_metadata']='x'*18000
        return types.SimpleNamespace(returncode=r.returncode,stdout=enc(v),stderr=r.stderr)
    f.e.run_bounded=padded;x.MAX_CANONICAL=25000
    workers=unit_workers(o,1,'EARLY_BUDGET');before=len(f.calls)
    try:no(lambda:x.collect_workers(f.h,workers,specs,lambda:None,clock=lambda:0),'online_shared_budget_rejects_before_all_serial_GETs')
    finally:f.e.run_bounded=original;x.MAX_CANONICAL=cap
    yes(len(f.calls)-before==2,'serial_budget_stops_after_second_valid_large_metadata_envelope')
    # Force eight valid response envelopes in flight together; observe actual guard
    # admissions while forwarding unchanged strict need semantics.
    barrier=threading.Barrier(8);counts={'accepted':0,'refused':0};raw_need=x.need
    def observe_need(ok,message):
        if message=='Shared aggregate canonical/origin budget exceeded before retention':
            counts['accepted'if ok else'refused']+=1
        return raw_need(ok,message)
    def concurrent_padded(argv,request):
        barrier.wait(5);return padded(argv,request)
    f.e.run_bounded=concurrent_padded;x.MAX_CANONICAL=25000;x.need=observe_need
    try:no(lambda:x.collect_workers(f.h,unit_workers(o,8,'RACE_BUDGET'),specs,lambda:None,clock=lambda:0),'concurrent_budget_admission_race_fails_closed')
    finally:f.e.run_bounded=original;x.MAX_CANONICAL=cap;x.need=raw_need
    yes(counts['accepted']==1 and counts['refused']>=1,'shared_locked_budget_admits_only_one_large_envelope')
    for value in [0,121,True,1.0,'120']:
        no(lambda:x.collect_workers(f.h,unit_workers(o,1,'BAD_DEADLINE_'+str(len(CHECKS))),specs,lambda:None,clock=lambda:0,deadline_seconds=value),'strict_dispatch_deadline_'+str(value))
    for boundary in ['before_source','after_source','after_transport']:
        now=[0];before=len(f.calls);clock=lambda:now[0]
        def check():
            if boundary=='after_source':now[0]=121
        def timed(argv,request):
            r=original(argv,request)
            if boundary=='after_transport':now[0]=121
            return r
        if boundary=='before_source':
            clock_calls=[0]
            def clock():
                clock_calls[0]+=1
                return 0 if clock_calls[0]==1 else 121
        f.e.run_bounded=timed
        try:no(lambda:x.collect_workers(f.h,unit_workers(o,1,'TIME_'+boundary),specs,check,clock=clock),'controlled_monotonic_expiry_'+boundary)
        finally:f.e.run_bounded=original
        yes(len(f.calls)-before==(1 if boundary=='after_transport'else 0),'deadline_dispatch_count_'+boundary)

def shutdown_join_test(o):
    f,x=o.f,o.x;specs=unit_specs(o,2);oids=sorted(specs)
    waiting=threading.Event();failed=threading.Event();release=threading.Event();done=threading.Event();errors=[];active=[0];mu=threading.Lock();old=f.e.run_bounded
    def delayed(argv,request):
        route=argv[6].rsplit('/',1)[-1]
        with mu:active[0]+=1
        try:
            if route==oids[0]:
                if not waiting.wait(5):FIXTURE_ERRORS.append('Delayed peer never started')
                failed.set();raise RuntimeError('Owned worker transport failure')
            waiting.set()
            if not release.wait(5):FIXTURE_ERRORS.append('Owned delayed peer release timed out')
            return old(argv,request)
        finally:
            with mu:active[0]-=1
    f.e.run_bounded=delayed
    def runner():
        try:x.collect_workers(f.h,unit_workers(o,2,'JOIN'),specs,lambda:None,clock=lambda:0)
        except RuntimeError as e:errors.append(str(e))
        finally:done.set()
    t=threading.Thread(target=runner);t.start()
    try:
        need(failed.wait(5),'Controlled worker failure reached')
        yes(not done.wait(.03) and active[0]>=1,'failed_pool_does_not_return_with_live_delayed_worker')
    finally:
        release.set();t.join(5);f.e.run_bounded=old
    yes(not t.is_alive() and done.is_set() and active[0]==0 and len(errors)==1,'failed_pool_joins_all_original_API_workers_before_return')
    yes(not FIXTURE_ERRORS,'join_fixture_errors_absent')

def active_concurrency_test(o):
    f,x=o.f,o.x;barrier=threading.Barrier(8);mu=threading.Lock();active=[0];maximum=[0];calls=[0];original=f.e.run_bounded
    def counted(argv,request):
        with mu:active[0]+=1;maximum[0]=max(maximum[0],active[0]);calls[0]+=1;n=calls[0]
        try:
            if n<=8:barrier.wait(5)
            return original(argv,request)
        finally:
            with mu:active[0]-=1
    f.e.run_bounded=counted
    try:g,api=o.api('ACTIVE_EIGHT')
    finally:f.e.run_bounded=original
    yes(maximum[0]==8 and active[0]==0 and len(api.workers)==8,'actual_original_API_peak_exactly_eight_and_all_joined')

def source_and_aux_tests(o):
    f,x=o.f,o.x;original=copy.deepcopy(o.gate)
    aux={'schema':'pr212-concurrent-GET-auxiliary-blob-pins-v1','PR':212,'files':copy.deepcopy(o.aux)}
    for change,label in [
      (lambda z:z['files'].pop(),'missing_required'),
      (lambda z:z['files'].append(copy.deepcopy(z['files'][0])),'duplicate_oid'),
      (lambda z:z['files'][0].update(oid='0'*40),'unknown_oid'),
      (lambda z:z['files'][0].update(bytes=True),'bool_length'),
      (lambda z:z['files'][0].update(sha256='0'*64),'repinned_wrong_expected_SHA256')]:
        z=copy.deepcopy(aux);change(z)
        # Wrong expected body SHA is permitted as a pin descriptor and refused by
        # actual native fetching, not a detached descriptor predicate.
        o.gate=copy.deepcopy(original);o.gate['auxiliary_blob_pins']=f.record('aux_bad_'+label+'.json',z,annotate=False);o.set_gate()
        if label=='repinned_wrong_expected_SHA256':no(lambda:o.api('AUX_WRONG_SHA'),'aux_actual_GET_rejects_wrong_expected_SHA256')
        else:no(o.guard,'aux_descriptor_'+label)
    o.gate=original;o.set_gate()
    g,api=o.api('DISJOINT')
    before=len(f.calls)
    no(lambda:x.make_readonly_api(f.v,g,api.journal),'same_operation_main_journal_cannot_allocate_duplicate_workers')
    yes(len(f.calls)==before,'worker_namespace_collision_precedes_actual_transport')
    code=o.d/'concurrent_get_extension.py';saved=code.read_bytes()
    code.chmod(0o644)
    try:no(g.refresh,'writable_extension_source_refused')
    finally:code.chmod(0o444)
    copyfile=o.d/'same_source_copy.py';write(copyfile,saved)
    code.unlink();code.symlink_to(copyfile)
    try:no(g.refresh,'symlinked_extension_source_same_bytes_refused')
    finally:code.unlink();write(code,saved)
    # Change an exact new acceptance body while keeping the established reference.
    gp=Path(o.gref['path']);saved=gp.read_bytes();write(gp,saved+b' ')
    try:no(g.refresh,'changed_new_gate_same_fields_different_bytes_refused')
    finally:write(gp,saved)

def candidate_extension_guard_fault(root,what):
    o=F(root,workers=4);f,x=o.f,o.x;original=f.e.run_bounded
    gatepath=Path(o.gref['path']);code=o.d/'concurrent_get_extension.py';target=gatepath if what=='gate'else code
    saved=target.read_bytes();hit=[False]
    def fault(argv,request):
        result=original(argv,request)
        if argv[5]=='POST'and argv[6].endswith('/git/trees')and not hit[0]:
            hit[0]=True;write(target,saved+b' ')
        return result
    f.e.run_bounded=fault
    try:no(lambda:x.candidate(f.v,o.guard('candidate')),'new_extension_'+what+'_change_after_tree_stops_commit')
    finally:f.e.run_bounded=original;write(target,saved)
    journal=f.b/f.admission['candidate_journal']
    yes(hit[0]and len(f.posts)==1 and len(list(journal.glob('*.OBJECT_RESULT.json')))==1,'exact_one_known_tree_before_'+what+'_guard_refusal')
    yes(not (journal/'IMMUTABLE_CANDIDATE_VERIFIED.json').exists(),'no_promoted_candidate_after_'+what+'_change')

def candidate_positive(root):
    o=F(root,workers=8);f,x=o.f,o.x
    result=x.candidate(f.v,o.guard('candidate'))
    journal=f.b/f.admission['candidate_journal'];proof=json.loads((journal/'IMMUTABLE_CANDIDATE_VERIFIED.json').read_bytes())
    yes(len(f.posts)==2 and result['this_action_immutable_POST_dispatches']==2,'full_new_candidate_exact_original_two_POSTs')
    yes(proof['selected_count']==len(f.overlay) and proof['all_selected_native_bodies_verified']and proof['transport_extension']['worker_count']==8,'full_new_candidate_complete_original_native_proof_with_fresh_reader')
    yes(result['actual_CAS_or_completion_inferred']is False,'new_candidate_adds_no_CAS_or_completion_authority')

def provenance_AST_tests():
    old=ast.parse((A/'native_administrative_preparation_01'/'administrative_checkpoint.py').read_bytes())
    new=ast.parse((Y/'concurrent_get_extension.py').read_bytes())
    om={r.name:r for r in old.body if isinstance(r,(ast.ClassDef,ast.FunctionDef))}
    nm={r.name:r for r in new.body if isinstance(r,(ast.ClassDef,ast.FunctionDef))}
    for name in ['need','pin','enc','read_regular']:
        yes(ast.dump(om[name],include_attributes=False)==ast.dump(nm[name],include_attributes=False),'independent_shared_AST_'+name)
    class Normalize(ast.NodeTransformer):
        def visit_Attribute(self,n):
            n=self.generic_visit(n)
            if isinstance(n.value,ast.Name)and n.value.id=='driver'and n.attr in ['lease_guard','reserve_candidate_oid']:
                return ast.copy_location(ast.Name(id=n.attr,ctx=ast.Load()),n)
            return n
    def guarded_prefix(fn):
        w=next(n for n in fn.body if isinstance(n,ast.With));rows=[]
        for n in w.body:
            rows.append(n)
            if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call):
                c=n.value
                if isinstance(c.func,ast.Name)and c.func.id=='api'and len(c.args)>1 and isinstance(c.args[0],ast.Constant)and c.args[0].value=='POST'and isinstance(c.args[1],ast.Constant)and c.args[1].value=='git/commits':break
        return ast.dump(Normalize().visit(ast.Module(body=copy.deepcopy(rows),type_ignores=[])),include_attributes=False)
    yes(guarded_prefix(om['candidate'])==guarded_prefix(nm['candidate']),'exact_original_guarded_mutation_sequence_AST_through_commit_POST')

def run():
    global S
    expected={'bytes':1604,'sha256':'a8fe591970cd85e1325d38a0bdb2fededf39d4f023bc0b66218fd91b285b6a18'}
    code={'bytes':24985,'sha256':'ef746eb08622c919dffe08b037fc2ce18dfcc6629d44182aacb9d8b2e156f5f0'}
    need(pin((Y/'SOURCE_MANIFEST.json').read_bytes())==expected,'Exact Root final producer closure')
    need(pin((Y/'concurrent_get_extension.py').read_bytes())==code,'Exact Root final code')
    manifest=json.loads((Y/'SOURCE_MANIFEST.json').read_bytes())
    need(len(manifest['files'])==7 and sum(r['bytes']for r in manifest['files'])==64322,'Final finite seven payloads')
    for r in manifest['files']:yes(pin((Y/r['path']).read_bytes())=={k:r[k]for k in ['bytes','sha256']},'final_payload_'+r['path'])
    S=support();socket.socket=deny;socket.create_connection=deny;subprocess.Popen=deny
    provenance_AST_tests()
    with tempfile.TemporaryDirectory(prefix='_owned_actual_concurrent_',dir=X)as temp:
        root=Path(temp)
        o=F(root/'main_checkout',workers=8)
        gate_tests(o);full_tests(o);origin_and_failure_tests(o);source_and_aux_tests(o)
        active_concurrency_test(o);resource_and_deadline_tests(o);shutdown_join_test(o)
        candidate_positive(root/'positive_candidate')
        candidate_fault(root/'failure_between','between_POSTs')
        candidate_fault(root/'failure_after','after_both_POSTs')
        candidate_extension_guard_fault(root/'new_gate_fault','gate')
        candidate_extension_guard_fault(root/'new_source_fault','source')
        p=F(root/'one_worker_dynamic11',workers=1,extra=True);g,api=p.api('ONE_WORKER')
        proof=p.f.v.verify_immutable(g,api)
        yes(proof['selected_count']==11 and len(api.workers)==1,'dynamic_eleven_scope_one_original_worker_full_verifier')
    need(not FIXTURE_ERRORS,str(FIXTURE_ERRORS))
    from collections import Counter
    return {'schema':'pr212-independent-concurrent-GET-actual-source-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'status':'PASS','final_source_manifest_pin':expected,'final_code_pin':code,'checks':CHECKS,'check_count':len(CHECKS),
      'outcome_counts':dict(Counter(r['outcome']for r in CHECKS)),
      'full_original_Seed_Runtime_refresh_native_proofs_and_original_API_receipts_executed':True,
      'fixture_adapters':['prior_own_support_deterministic_transport','owned_lock_inode_mapping'],
      'owned_fault_and_observation_hooks':['original_API.__call__','original_run_bounded_transport','wrapper_need_budget_observation',
        'controlled_collect_workers_clock','threading_events_and_barriers','owned_gate_source_and_retained_raw_file_mutations'],
      'all_hook_implementations_in_this_checker_visible':True,'production_source_or_logical271_changed':False,
      'actual_native_network_Git_real_original_lock_globalfive_ref_PR_provider_CAS_sync_terminal_intake_effects':False,
      'no_authority':'Source review controls and synthetic Root-shaped records only; no actual Root gate/admission/candidate/ref/CAS/sync/terminal/publication/cursor authority.',
      'limits':'Bounded own fixtures, low overridden cache-budget constants, clocks/events and transparent fault/observation hooks. No live transport, external race, crash, OS scheduling or whole-process memory proof. Existing unchanged hold/sync/framing/descriptor algorithms are source/AST reviewed rather than exhaustively rerun.'}
if __name__=='__main__':
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Use -E -S -B -P')
    print(json.dumps(run(),sort_keys=True,indent=2))






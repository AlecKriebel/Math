"""Owned offline controls. No production factory/CLI/network/lock/native effects."""
import ast,base64,concurrent.futures,copy,hashlib,json,os,sys,tempfile,threading,time,types
from pathlib import Path
BASE=Path(__file__).absolute().parent

def module(path,raw):
    out=types.ModuleType(path.stem);out.__file__=str(path);exec(compile(raw,str(path),'exec'),out.__dict__);return out

def run():
    checks=[]
    def yes(value,label):
        if not value:raise RuntimeError(label)
        checks.append(label)
    def no(call,label):
        try:call()
        except (RuntimeError,ValueError,TypeError,KeyError,OSError):checks.append(label)
        else:raise RuntimeError('Expected refusal '+label)
    source=(BASE/'concurrent_get_extension.py').read_bytes();x=module(BASE/'concurrent_get_extension.py',source)
    oldpath=BASE.parent/'native_administrative_preparation_01/native212_model.py'
    old=oldpath.read_bytes()
    with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as tmp:
        root=Path(tmp)/'checkout';case=root/'draft_pr_publication_program_20260930/audits/pr212_30005310'
        oldbase=case/'native_administrative_preparation_01';oldbase.mkdir(parents=True)
        h=module(oldbase/'native212_model.py',old)
        def write(path,raw):
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);path.chmod(0o444)
        def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
        class Tracker:
            def __init__(self):
                self.lock=threading.Lock();self.active=0;self.peak=0;self.calls=0
            def enter(self):
                with self.lock:self.active+=1;self.calls+=1;self.peak=max(self.peak,self.active)
            def leave(self):
                with self.lock:self.active-=1
        class Worker:
            def __init__(self,name,data,tracker,barrier=None,extra=0,bad=None,delay=0):
                self.journal=case/name;self.journal.mkdir();self.data=data;self.tracker=tracker;self.barrier=barrier
                self.extra=extra;self.bad=bad;self.delay=delay;self.number=0;self.actual_GET_origins={}
                self.busy=False;self.lock=threading.Lock();self.main='a'*40;self.thread_ids=[]
            def __call__(self,method,path,body=None):
                if method!='GET' or body is not None:raise RuntimeError('Synthetic GET only')
                with self.lock:
                    if self.busy:raise RuntimeError('Worker used concurrently')
                    self.busy=True
                self.tracker.enter();self.thread_ids.append(threading.get_ident())
                try:
                    self.number+=1
                    if self.barrier is not None and self.number==1:self.barrier.wait(timeout=5)
                    if self.delay:threading.Event().wait(self.delay)
                    if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
                    if path.startswith('git/trees/'):return {'sha':path.rsplit('/',1)[1],'tree':[]}
                    if not path.startswith('git/blobs/'):raise RuntimeError('Unexpected synthetic route')
                    oid=path.rsplit('/',1)[1];raw=self.data[oid]
                    value={'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
                    if self.extra:value['extra_metadata']='x'*self.extra
                    if self.bad=='size':value['size']=5_000_001
                    if self.bad=='base64':value['content']='!bad!'
                    if self.bad=='oid':value['sha']='0'*40
                    out=self.journal/(str(self.number)+'.stdout.json');err=self.journal/(str(self.number)+'.stderr.txt')
                    receipt=self.journal/(str(self.number)+'.receipt.json')
                    wire=enc(value);write(out,wire);write(err,b'')
                    response={'path':str(out),**h.pin(wire)};stderr={'path':str(err),**h.pin(b'')}
                    record={'method':'GET','path':path,'exit':0,'raw_stdout':response,'raw_stderr':stderr}
                    write(receipt,enc(record))
                    self.actual_GET_origins[path]={'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math',
                        'route':path,'receipt':str(receipt),'receipt_pin':h.pin(enc(record)),
                        'raw_response':response,'raw_stderr':stderr}
                    return value
                finally:
                    self.tracker.leave()
                    with self.lock:self.busy=False
        data={h.native('blob',('fixture '+str(i)).encode()):('fixture '+str(i)).encode() for i in range(24)}
        specs={oid:h.pin(body) for oid,body in data.items()}
        class Guard:
            def __init__(self,specs):
                self.h=h;self.specs=specs;self.operation='verify';self.source_pin=h.pin(source)
                self.source_manifest_pin={'bytes':1,'sha256':'1'*64};self.acceptance_ref={'path':'synthetic','bytes':1,'sha256':'2'*64}
                self.checks=0
            def check_sources(self):self.checks+=1
        tracker=Tracker();barrier=threading.Barrier(8)
        workers=[Worker('positive_'+str(i),data,tracker,barrier=barrier) for i in range(8)]
        guard=Guard(specs);api=x.FastAPI(guard,case/'main',workers)
        yes(tracker.peak==8 and tracker.active==0,'eight_workers_overlap_and_all_join_before_return')
        yes(all(len(set(w.thread_ids))==1 for w in workers),'each_prefetch_worker_single_thread')
        yes(tracker.calls==len(specs),'one_fresh_synthetic_GET_per_unique_prefetched_OID')
        pool=h.NativeBodyProofs()
        for oid,raw in data.items():
            yes(pool.get(api,oid,h.pin(raw))==raw,'old_NativeBodyProofs_revalidates_composite_origin_'+oid[:7])
        yes(tracker.calls==len(specs),'original_proof_reuses_only_same_invocation_authenticated_blob_envelopes')
        oid=next(iter(data));value=api('GET','git/blobs/'+oid);value['content']='modified'
        yes(api('GET','git/blobs/'+oid)['content']==base64.b64encode(data[oid]).decode(),'fresh_decoded_copy_prevents_alias_mutation')
        origin=api.actual_GET_origins.get('git/blobs/'+oid);origin['method']='POST'
        yes(api.actual_GET_origins.get('git/blobs/'+oid)['method']=='GET','origin_view_returns_sealed_fresh_copy')
        yes(api('GET','git/ref/heads/main')['object']['sha']=='a'*40,'first_mutable_ref_observation')
        workers[0].main='b'*40
        yes(api('GET','git/ref/heads/main')['object']['sha']=='b'*40,'mutable_ref_not_cached')
        dynamic=b'new foreign QUEUE bytes';dynamic_oid=h.native('blob',dynamic);data[dynamic_oid]=dynamic
        yes(pool.get(api,dynamic_oid,h.pin(dynamic))==dynamic,'dynamic_delegated_blob_has_actual_raw_origin_and_oldproof_association')
        yes(api.actual_GET_origins.get('git/blobs/'+dynamic_oid)['route']=='git/blobs/'+dynamic_oid,'dynamic_origin_mirrored')
        tracker2=Tracker();workers2=[Worker('separate_'+str(i),data,tracker2) for i in range(2)]
        api2=x.FastAPI(Guard(specs),case/'main2',workers2)
        yes(tracker2.calls==len(specs),'second_composite_performs_new_GETs_no_cross_observer_cache')
        yes(pool.get(api2,oid,h.pin(data[oid]))==data[oid] and api2.actual_GET_origins.get('git/blobs/'+oid)!=api.actual_GET_origins.get('git/blobs/'+oid),
            'separate_oldproof_origin_association_per_composite_observer')
        path=Path(api2.actual_GET_origins.get('git/blobs/'+oid)['raw_response']['path'])
        path.chmod(0o644);path.write_bytes(b'{}');path.chmod(0o444)
        no(lambda:h.NativeBodyProofs().get(api2,oid,h.pin(data[oid])),'retained_raw_response_tamper_refused_by_original_proof')
        no(lambda:api('POST','git/trees',{}),'composite_POST_refused')
        no(lambda:api('GET','git/ref/heads/main'),'failed_composite_cannot_fallback_or_retry')
        for kind in ('size','base64','oid'):
            t=Tracker();w=Worker('bad_'+kind,data,t,bad=kind);badapi=x.FastAPI.__new__(x.FastAPI)
            no(lambda w=w,badapi=badapi:x.FastAPI.__init__(badapi,Guard({oid:specs[oid]}),case/'badmain',[w]),
               'malformed_'+kind+'_immediate_refusal')
            yes(badapi.failed and not badapi._cache and t.active==0,'malformed_'+kind+'_observer_poisoned_and_joined')
        wrong={oid:{**specs[oid],'sha256':'f'*64}};t=Tracker();w=Worker('wrongpin',data,t)
        no(lambda:x.collect_workers(h,[w],wrong,lambda:None),'expected_length_SHA256_mismatch_refused')
        no(lambda:x.collect_workers(h,[w]*9,{oid:specs[oid]},lambda:None),'worker_count_nine_refused_before_dispatch')
        no(lambda:x.collect_workers(h,[w],{'z':{'bytes':32_000_001,'sha256':'0'*64}},lambda:None),'decoded_pool_bound_refused_before_dispatch')
        # Each envelope is valid with tiny exact native body and oversized
        # extra JSON metadata. A locked budget must reject before all24 collect.
        t=Tracker();bigworkers=[Worker('extra_'+str(i),data,t,extra=5_900_000) for i in range(8)]
        badapi=x.FastAPI.__new__(x.FastAPI)
        no(lambda:x.FastAPI.__init__(badapi,Guard(specs),case/'bigmain',bigworkers),'oversized_extra_metadata_shared_aggregate_budget_refused_early')
        count=t.calls
        yes(badapi.failed and not badapi._cache and t.active==0 and count<len(specs),
            'overflow_discards_partial_cache_and_joins_before_return')
        threading.Event().wait(0.02)
        yes(t.calls==count and t.active==0,'overflow_no_late_worker_activity')
        class Clock:
            def __init__(self):self.value=0;self.lock=threading.Lock()
            def __call__(self):
                with self.lock:return self.value
            def advance(self,n):
                with self.lock:self.value+=n
        clock=Clock();t=Tracker()
        class DelayedWorker(Worker):
            def __call__(self,*args,**kwargs):
                value=super().__call__(*args,**kwargs);clock.advance(121);return value
        w=DelayedWorker('deadline',data,t,delay=0.01)
        no(lambda:x.collect_workers(h,[w],specs,lambda:None,clock=clock),'overall_deadline_delayed_response_refused_before_acceptance')
        yes(t.calls==1 and t.active==0,'deadline_stops_new_jobs_and_joins_delayed_worker')
        clock2=Clock();t2=Tracker();w2=Worker('deadline_dispatch',data,t2)
        no(lambda:x.collect_workers(h,[w2],specs,lambda:clock2.advance(121),clock=clock2),'deadline_rechecked_immediately_before_dispatch')
        yes(t2.calls==0,'deadline_sourcecheck_delay_never_dispatches')
        no(lambda:x.collect_workers(h,[w2],specs,lambda:None,deadline_seconds=121),'overall_deadline_cannot_be_relaxed')
    tree=ast.parse(source)
    fns={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    cand=fns['candidate']
    posts=[n.args[1].value for n in ast.walk(cand) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
           and n.func.id=='api' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value=='POST']
    yes(posts==['git/trees','git/commits'],'candidate_exact_two_sequential_original_immutable_POST_sites')
    yes('driver.lease_guard(rt, api, lock)' in ast.unparse(cand) and 'driver.reserve_candidate_oid(rt)' in ast.unparse(cand),
        'candidate_original_per_effect_lease_and_oneuse_OID_reservation_retained')
    text=ast.unparse(fns['main'])
    yes('q.hold_CAS(rt, api, journal' in text and 'q.sync(rt, api, journal' in text,
        'old_hold_CAS_and_sync_called_without_reimplementation')
    yes("rt.refresh()" in ast.unparse(fns['candidate']) and 'self.base.refresh()' in ast.unparse(fns['GuardedRuntime']),
        'wrapped_runtime_adds_source_gate_refresh_without_monkeypatch')
    yes('driver.Runtime' in ast.unparse(fns['GuardedRuntime']) and 'type(runtime) is GuardedRuntime' in ast.unparse(fns['make_readonly_api']),
        'public_factory_requires_explicit_approved_runtime_binding')
    yes('NativeBodyProofs' not in ast.unparse(fns['collect_workers']),'original_global_bodyproof_pool_never_used_concurrently')
    yes("git/ref/heads/main" not in ast.unparse(fns['collect_workers']),'no_mutable_prefetch')
    return {'schema':'pr212-concurrent-GET-offline-controls-v1','status':'PASS','checks':checks,'check_count':len(checks),
        'source_pin':x.pin(source),'metrics':{'peak_concurrent_workers':tracker.peak,'overflow_worker_calls':count,'requested_prefetch_bodies':len(specs),'deadline_delayed_calls':t.calls,'deadline_before_dispatch_calls':t2.calls},'production_CLI_factory_Runtime_gate_or_transport_executions':0,
        'actual_network_Git_native_lock_CAS_PR_globalfive_or_intake_effects':False,'source_or_module_monkeypatches':False,
        'ordinary_synthetic_workers_guards_and_controlled_clock':True,
        'limits':'Transport engine and original NativeBodyProofs were exercised with synthetic actual-shaped local raw/receipt fixtures. Production GuardedRuntime acceptance and live oldAPI transport are structurally inspected, not executed.'}

if __name__=='__main__':
    if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):
        raise RuntimeError('Use -E -S -B -P')
    print(json.dumps(run(),sort_keys=True,indent=2))

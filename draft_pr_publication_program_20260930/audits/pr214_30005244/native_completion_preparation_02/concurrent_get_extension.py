"""Inactive PR214 GET transport extension; no ref/PR writer or new effect authority."""
import argparse,base64,concurrent.futures,hashlib,json,os,re,stat,sys,threading,time,types
from pathlib import Path
BASE=Path(__file__).absolute().parent
CASE=BASE.parent
PROGRAM=CASE.parents[1]
CHECKOUT=PROGRAM.parent
DRIVER=BASE
PROTOCOL_PIN={'bytes': 44492, 'sha256': '30bdc4dd56c176da4176be136a34ba2424d73c8653e50a501dd624210957a945'}
MAX_BLOBS=664
MAX_DECODED=32_000_000
MAX_CANONICAL=48_000_000
PREFETCH_SECONDS=120
OPERATIONS={'verify','candidate','hold-CAS','sync','terminal'}

def need(ok,message):
    if type(ok) is not bool or not ok:raise RuntimeError(message)

def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def enc(obj):return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def read_regular(path,cap=4_000_000,absent=False):
    """No-follow descriptor walk, exact readonly mode and identity stability."""
    need(path.is_absolute() and path.is_relative_to(CHECKOUT) and path.resolve()==path,
         'Canonical source/preimage inside checkout required')
    handles=[]
    fd=None
    try:
        current=Path('/')
        parent=os.open(current,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        handles.append((current,parent,os.fstat(parent)))
        for part in path.parent.parts[1:]:
            current=current/part
            parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
            handles.append((current,parent,os.fstat(parent)))
        try:
            fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
        except FileNotFoundError:
            need(absent,'Required regular file absent')
            need(not path.exists() and not path.is_symlink(),'File appeared during absence observation')
            for ancestor,descriptor,before in handles:
                a,b=os.fstat(descriptor),ancestor.lstat()
                need(stat.S_ISDIR(b.st_mode) and (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)==(before.st_dev,before.st_ino),
                     'Ancestor changed during absence observation')
            return None,None
        before=os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444
             and before.st_size<=cap,'Bounded readonly0444 regular file required')
        with os.fdopen(fd,'rb',closefd=False) as stream:
            raw=stream.read(cap+1)
        after,entry=os.fstat(fd),path.lstat()
        fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        need(fields(before)==fields(after)==fields(entry) and stat.S_ISREG(entry.st_mode)
             and stat.S_IMODE(entry.st_mode)==0o444 and len(raw)==after.st_size,'File changed during capture')
        for ancestor,descriptor,initial in handles:
            now,linked=os.fstat(descriptor),ancestor.lstat()
            need(stat.S_ISDIR(linked.st_mode) and (now.st_dev,now.st_ino)==(linked.st_dev,linked.st_ino)==(initial.st_dev,initial.st_ino),
                 'Source/preimage ancestor changed')
        return raw,{'device':after.st_dev,'inode':after.st_ino,'bytes':after.st_size,
                    'mtime_ns':after.st_mtime_ns,'ctime_ns':after.st_ctime_ns,'mode':'0444'}
    finally:
        if fd is not None:os.close(fd)
        for ancestor,descriptor,initial in reversed(handles):os.close(descriptor)

def source_module():
    raw,unused=read_regular(DRIVER/'completion_checkpoint.py')
    need(pin(raw)==PROTOCOL_PIN,'Approved old protocol changed')
    q=types.ModuleType('approved_PR214_protocol');q.__file__=str(DRIVER/'completion_checkpoint.py')
    exec(compile(raw,q.__file__,'exec'),q.__dict__);return q

def wanted_blobs(rt,aux):
    h=rt.h
    need(type(aux) is dict and set(aux)=={'schema','PR','files'}
         and aux['schema']=='pr214-concurrent-GET-auxiliary-blob-pins-v1'
         and type(aux['PR']) is int and aux['PR']==214,'Exact auxiliary native body pin descriptor')
    rows=aux['files']
    need(type(rows) is list and len(rows)<=32 and all(type(r) is dict and set(r)=={'oid','bytes','sha256'} for r in rows)
         and len({r['oid'] for r in rows})==len(rows),'Finite exact auxiliary body pins')
    wanted={}
    for raw in rt.overlay.values():
        oid=h.native('blob',raw);p=pin(raw)
        need(oid not in wanted or h.exact(wanted[oid],p),'Duplicate OID with inconsistent body pin')
        wanted[oid]=p
    for row in rt.m['protected_bodies']:
        p={k:row[k] for k in ('bytes','sha256')}
        need(row['sha'] not in wanted or h.exact(wanted[row['sha']],p),'Protected/selected object pin disagreement')
        wanted[row['sha']]=p
    required={rt.m['protected_queue']['sha'],h.CURRENT_QUEUE}
    for path in (h.VIEWS[2],h.VIEWS[1],h.VIEWS[4]):
        item=rt.pre[path]
        if item is not None:required.add(item[2])
    extras={}
    for row in rows:
        need(h.hexid(row['oid']),'Exact auxiliary blob OID')
        p=h.bytepin({k:row[k] for k in ('bytes','sha256')})
        need(row['oid'] in required,'Unexpected auxiliary object')
        extras[row['oid']]=p
    need(required.issubset(set(wanted)|set(extras)),'Missing current/parent QUEUE, baseline or native-log auxiliary pin')
    for oid,p in extras.items():
        need(oid not in wanted or h.exact(wanted[oid],p),'Auxiliary and selected pin disagreement')
        wanted[oid]=p
    need(len(wanted)<=MAX_BLOBS and sum(p['bytes'] for p in wanted.values())<=MAX_DECODED,
         'Exact unique current-invocation native body bounds')
    return wanted

class GuardedRuntime:
    """Delegates old Runtime; every refresh additionally authenticates this extension."""
    def __init__(self,driver,runtime,acceptance_ref,operation):
        need(type(driver) is types.ModuleType and type(runtime) is driver.Runtime,'Exact approved Runtime instance required')
        need(Path(driver.__file__).absolute()==DRIVER/'completion_checkpoint.py','Fixed approved driver path')
        need(operation in OPERATIONS,'Named reviewed operation required')
        self.driver,self.base,self.acceptance_ref,self.operation=driver,runtime,acceptance_ref,operation
        self.source=read_regular(Path(__file__).absolute())[0];self.source_pin=pin(self.source)
        self.manifest_raw=read_regular(BASE/'SOURCE_MANIFEST.json')[0];self.source_manifest_pin=pin(self.manifest_raw)
        self.acceptance_raw=driver.ref(runtime.h,runtime.seed.s,acceptance_ref)
        self.acceptance_pin={k:acceptance_ref[k] for k in ('bytes','sha256')}
        self.refresh()
    def __getattr__(self,name):return getattr(self.base,name)
    def check_sources(self):
        h=self.base.h
        need(read_regular(Path(__file__).absolute())[0]==self.source
             and read_regular(BASE/'SOURCE_MANIFEST.json')[0]==self.manifest_raw,'Extension source closure changed')
        need(pin(read_regular(DRIVER/'completion_checkpoint.py')[0])==PROTOCOL_PIN
             and read_regular(DRIVER/'SOURCE_MANIFEST.json')[0]==self.manifest_raw,'Approved old source identity changed')
        manifest=h.decode(self.manifest_raw)
        h.matches(manifest,{'schema':'pr214-completion-source-manifest-v1','source_only':True,'self_excluded':True},
                  'Positive extension source closure')
        rows=manifest.get('files')
        need(type(rows) is list and 3<=len(rows)<=20 and len({r.get('path') for r in rows})==len(rows)
             and all(type(r) is dict and set(r)=={'path','bytes','sha256'} for r in rows),'Finite source closure rows')
        need({'path':Path(__file__).name,**self.source_pin} in rows,'Extension source missing')
        for row in rows:
            name=h.rel(row['path']);need(Path(name).name==name,'No nested working source discovery')
            need(h.exact(pin(read_regular(BASE/name)[0]),h.bytepin({k:row[k] for k in ('bytes','sha256')})),
                 'Frozen extension source/document changed')
        gate=self.driver.ref(h,self.base.seed.s,self.acceptance_ref)
        need(h.exact(gate,self.acceptance_raw),'Exact extension acceptance changed')
        h.matches(gate,{'schema':'pr214-root-concurrent-GET-extension-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':214,'accepted':True,'extension_pin':self.source_pin,'extension_source_manifest_pin':self.source_manifest_pin,
            'protocol_pin':PROTOCOL_PIN,'protocol_source_manifest_pin':self.source_manifest_pin,
            'logical_manifest_pin':self.base.seed.manifest_pin,'logical_gate_pin':self.base.seed.logical_gate_pin,
            'admission_pin':self.base.admission_pin,'admission_gate_pin':self.base.gate_pin,
            'Root_full_source_read':True,'independent_source_adversarial_review_accepted':True,
            'fresh_actual_parameter_bindings_accepted':True,'old_logical_packet_and_source_identity_unchanged':True,
            'actual_native_GET_transport_extension_explicitly_accepted':True,
            'only_existing_inherited_per_admission_effect_authority':True,
            'no_ref_PR_or_global_five_authority_added':True,'original_driver_CLI_execution_claimed':False,
            'old_sync_and_hold_CAS_invoked_unchanged':True},'Exact separate Root transport-extension acceptance required')
        ops=gate.get('allowed_operations')
        need(type(ops) is list and ops==sorted(set(ops)) and all(type(x) is str and x in OPERATIONS for x in ops)
             and self.operation in ops,'Operation not explicitly accepted')
        if self.operation=='candidate':
            h.matches(gate,{'candidate_two_POST_orchestration_delta_reviewed':True},'Candidate reader-only delta must be separately reviewed')
        workers=gate.get('workers')
        need(type(workers) is int and 1<=workers<=8,'At most eight isolated old API workers')
        aux=self.driver.ref(h,self.base.seed.s,gate.get('auxiliary_blob_pins'))
        specs=wanted_blobs(self.base,aux)
        if 'worker_count' not in self.__dict__:
            self.worker_count,self.specs=workers,specs
        else:need(self.worker_count==workers and h.exact(self.specs,specs),'Extension worker/spec binding changed')
        return self
    def refresh(self):
        self.base.refresh();self.check_sources()
        need(self.base.h.exact(self.base.seed.source_pin,PROTOCOL_PIN)
             and self.base.h.exact(self.base.seed.source_manifest_pin,self.source_manifest_pin),'Loaded old protocol association differs')
        return self

def bind_runtime(driver,runtime,extension_acceptance_ref,operation):
    return GuardedRuntime(driver,runtime,extension_acceptance_ref,operation)

def validate_blob(h,worker,oid,value,wanted=None):
    """Validate actual returned bytes/origin before any aggregate cache collection."""
    need(h.hexid(oid) and type(value) is dict and value.get('sha')==oid
         and value.get('encoding')=='base64' and type(value.get('size')) is int
         and 0<=value['size']<=4_000_000 and type(value.get('content')) is str,'Bounded actual native blob response')
    body=base64.b64decode(''.join(value['content'].split()),validate=True)
    need(len(body)==value['size'] and h.native('blob',body)==oid,'Fresh native blob SHA1/size authentication')
    body_pin=pin(body)
    if wanted is not None:need(h.exact(body_pin,h.bytepin(wanted)),'Fresh native length/SHA256 differs from expected body pin')
    origin=getattr(worker,'actual_GET_origins',{}).get('git/blobs/'+oid)
    h.matches(origin,{'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math','route':'git/blobs/'+oid},
              'Actual worker raw origin required')
    response=origin['raw_response'];raw,unused=h.read_regular(Path(response['path']),cap=12_000_000)
    need(h.exact(pin(raw),{k:response[k] for k in ('bytes','sha256')}),'Actual raw worker response changed')
    rawvalue=h.decode(raw)
    need(h.exact(rawvalue,value),'Actual raw worker envelope differs from returned object')
    err=origin['raw_stderr'];stderr,unused=h.read_regular(Path(err['path']),cap=65536)
    need(h.exact(pin(stderr),{k:err[k] for k in ('bytes','sha256')}),'Actual worker stderr changed')
    receipt=h.root_ref({'path':origin['receipt'],**origin['receipt_pin']})
    h.matches(receipt,{'method':'GET','path':'git/blobs/'+oid,'exit':0,'raw_stdout':response,'raw_stderr':err},
              'Actual raw response/receipt route association required')
    canonical=enc(value);origin_raw=enc(origin)
    need(len(canonical)<=6_000_000 and len(origin_raw)<=65536,'Bounded canonical native blob envelope/origin')
    return canonical,pin(canonical),body_pin,origin_raw,pin(origin_raw)

def collect_workers(h,workers,specs,check,clock=time.monotonic,deadline_seconds=PREFETCH_SECONDS):
    """Each worker is owned by one thread; aggregate only after every thread joins."""
    need(1<=len(workers)<=8 and len(specs)<=MAX_BLOBS
         and sum(x['bytes'] for x in specs.values())<=MAX_DECODED,'Bounded worker collection')
    need(type(deadline_seconds) is int and 1<=deadline_seconds<=PREFETCH_SECONDS and callable(clock),'Bounded overall prefetch deadline')
    deadline=clock()+deadline_seconds
    stop=threading.Event();jobs=[[] for unused in workers]
    budget_lock=threading.Lock();budget={'canonical':0,'origin':0}
    for index,item in enumerate(sorted(specs.items())):jobs[index%len(workers)].append(item)
    def work(index):
        rows=[];worker=workers[index]
        try:
            for oid,wanted in jobs[index]:
                if stop.is_set():break
                need(clock()<deadline,'Overall prefetch deadline before source check')
                check()
                if stop.is_set():break
                need(clock()<deadline,'Overall prefetch dispatch deadline exceeded')
                value=worker('GET','git/blobs/'+oid)
                result=validate_blob(h,worker,oid,value,wanted)
                if stop.is_set():break
                need(clock()<deadline,'Overall prefetch deadline exceeded before result acceptance')
                with budget_lock:
                    canonical=budget['canonical']+len(result[0]);origins=budget['origin']+len(result[3])
                    need(canonical+origins<=MAX_CANONICAL,'Shared aggregate canonical/origin budget exceeded before retention')
                    budget['canonical'],budget['origin']=canonical,origins
                rows.append((oid,result))
                if stop.is_set():break
            return rows
        except BaseException:
            stop.set();raise
    executor=concurrent.futures.ThreadPoolExecutor(max_workers=len(workers))
    futures=[];results=[];error=None
    try:
        futures=[executor.submit(work,i) for i in range(len(workers))]
        for future in concurrent.futures.as_completed(futures):
            try:results.extend(future.result())
            except BaseException as caught:
                stop.set();error=caught
                for item in futures:item.cancel()
        need(error is None and len(results)==len(specs),'Concurrent collection failed; no retry or incomplete cache')
        need(sum(len(result[0]) for unused,result in results)<=MAX_CANONICAL
             and sum(len(result[0])+len(result[3]) for unused,result in results)<=MAX_CANONICAL,
             'Independent aggregate canonical/origin cache bound')
        return dict(results)
    finally:
        stop.set()
        executor.shutdown(wait=True,cancel_futures=True)

class Origins:
    """Readonly mapping view returns fresh decoded exact origin data."""
    def __init__(self,pool):self.pool=pool
    def get(self,path,default=None):
        need(not self.pool.failed,'Stopped composite observer has no reusable origins')
        row=self.pool._cache.get(path.rsplit('/',1)[-1]) if path.startswith('git/blobs/') else None
        if row is None:return default
        need(pin(row[3])==row[4],'Sealed actual origin cache changed')
        return self.pool.h.decode(row[3])

class FastAPI:
    """Fresh per-invocation composite GET observer, never a POST transport."""
    def __init__(self,guard,journal,workers):
        self.guard,self.h,self.journal=guard,guard.h,journal
        self.workers=workers;self.owner=threading.get_ident();self.failed=False
        self._cache={};self.actual_GET_origins=Origins(self);self.calls=0
        try:self._cache=collect_workers(self.h,workers,guard.specs,guard.check_sources)
        except BaseException:
            self.failed=True;self._cache.clear();raise
    def __call__(self,method,path,body=None,expected_oid=None):
        try:
            need(threading.get_ident()==self.owner,'Composite observer consumed by its owner only')
            need(not self.failed and method=='GET' and body is None and expected_oid is None,'GET-only composite observer; stopped observers never retry')
            self.guard.check_sources();self.calls+=1
            need(self.calls<=5000,'Bounded composite lookup count')
            match=re.fullmatch('git/blobs/([0-9a-f]{40})',path)
            if match:
                oid=match.group(1)
                if oid not in self._cache:
                    value=self.workers[0]('GET',path)
                    row=validate_blob(self.h,self.workers[0],oid,value,self.guard.specs.get(oid))
                    need(len(self._cache)<MAX_BLOBS
                         and sum(x[2]['bytes'] for x in self._cache.values())+row[2]['bytes']<=MAX_DECODED
                         and sum(len(x[0])+len(x[3]) for x in self._cache.values())+len(row[0])+len(row[3])<=MAX_CANONICAL,
                         'Dynamic current-invocation native body bounds')
                    self._cache[oid]=row
                row=self._cache[oid]
                need(pin(row[0])==row[1] and pin(row[3])==row[4],'Composite immutable envelope/origin changed')
                value=self.h.decode(row[0])
                need(value.get('sha')==oid,'Composite route/OID association changed')
                return value
            # Workers have all joined. Worker0 now serves metadata/mutable GETs
            # sequentially; its actual origins are mirrored for any dynamic blob.
            return self.workers[0](method,path)
        except BaseException:
            self.failed=True;raise
    def provenance(self):
        need(not self.failed,'Failed observer cannot issue successful provenance')
        return {'schema':'pr214-current-invocation-concurrent-GET-provenance-v1',
            'observer':'Fresh composite GET observer, not original driver CLI',
            'extension_pin':self.guard.source_pin,'extension_source_manifest_pin':self.guard.source_manifest_pin,
            'extension_acceptance':self.guard.acceptance_ref,'operation':self.guard.operation,
            'worker_count':len(self.workers),'worker_journals':[str(w.journal) for w in self.workers],
            'joined_before_original_proof':True,'prefetch_dispatch_deadline_seconds':PREFETCH_SECONDS,
            'inflight_cleanup_per_request_cap_seconds':120,'cleanup_cancellation_is_not_instantaneous':True,'decoded_bytes':sum(r[2]['bytes'] for r in self._cache.values()),
            'unique_native_bodies':len(self._cache),'cross_run_or_source_body_cache':False,
            'mutable_GETs_cached_by_extension':False,'POST_or_ref_authority_added':False}

def make_readonly_api(driver,runtime,journal):
    need(type(runtime) is GuardedRuntime and runtime.driver is driver,'Explicit bound extension Runtime required')
    runtime.refresh()
    need(journal.parent==DRIVER and journal.name.startswith(('ROOT_COMPLETE214_FAST_READ_','ROOT_COMPLETE214_SYNC_FAST_','ROOT_COMPLETE214_CANDIDATE_','ROOT_COMPLETE214_READ_ROOT_TERMINAL_')),
         'Exact reviewed owned main journal prefix')
    workers=[]
    for index in range(runtime.worker_count):
        runtime.check_sources()
        name='ROOT_COMPLETE214_FAST_WORK_'+hashlib.sha256((journal.name+runtime.operation).encode()).hexdigest()[:20]+'_'+str(index)
        worker_journal=runtime.e.journal_new(name)
        workers.append(runtime.e.API(runtime.h,worker_journal,mutate=False))
    api=FastAPI(runtime,journal,workers)
    runtime.refresh()
    runtime.e.put(journal,'FAST_GET_EXTENSION_BINDING.json',api.provenance())
    return api

def candidate(driver,rt):
    """Old orchestration; only post-construction verification reader is replaced."""
    need(type(rt) is GuardedRuntime and rt.driver is driver and rt.operation=='candidate','Explicit candidate extension binding required')
    rt.refresh();e,h=rt.e,rt.h
    with e.WriterLock(rt.m['writer_lock']) as lock:
        rt.refresh()
        journal=e.journal_new(rt.admission['candidate_journal'])
        api=e.API(h,journal,mutate=True)
        driver.lease_guard(rt,api,lock)
        driver.reserve_candidate_oid(rt)
        entries=[{'path':path,'mode':'100644','type':'blob','content':body.decode('utf-8')}
                 for path,body in sorted(rt.overlay.items())]
        tree_request={'base_tree':rt.admission['parent_tree'],'tree':entries}
        commit_request,oid=h.commit_request(rt.m,rt.admission['tree'],[rt.admission['parent']])
        e.put(journal,'ONE_USE_ADMISSION_RESERVATION.json',{'admission_pin':rt.admission_pin,
            'protocol_pin':rt.seed.source_pin,'logical_manifest_pin':rt.seed.manifest_pin,'gate_pin':rt.gate_pin,
            'expected_tree':rt.admission['tree'],'expected_candidate':oid,
            'semantics':'One tree POST and one commit POST only. No redispatch after uncertainty or stale stop.'})
        driver.lease_guard(rt,api,lock)
        api('POST','git/trees',tree_request,expected_oid=rt.admission['tree'])
        driver.lease_guard(rt,api,lock)
        api('POST','git/commits',commit_request,expected_oid=oid)
        reader=make_readonly_api(driver,rt,journal)
        rt.refresh();result=driver.verify_immutable(rt,reader)
        result['transport_extension']=reader.provenance()
        rt.refresh();driver.local_states(rt);lock.check()
        e.put(journal,'IMMUTABLE_CANDIDATE_VERIFIED.json',result)
        return {'candidate':oid,'tree':rt.admission['tree'],'journal':str(journal),
            'this_action_immutable_POST_dispatches':2,'actual_CAS_or_completion_inferred':False,
            'transport_extension':reader.provenance()}

def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and sys.flags.safe_path and not sys.flags.optimize,'Use Python -E -S -B -P without optimization')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation',choices=sorted(OPERATIONS))
    for name in ('manifest','logical-gate','admission','admission-gate','extension-acceptance','actual-CAS','preCAS-acceptance'):
        p.add_argument('--'+name);p.add_argument('--'+name+'-bytes',type=int);p.add_argument('--'+name+'-sha256')
    p.add_argument('--journal')
    args=p.parse_args()
    def ref(name):
        k=name.replace('-','_');return {'path':getattr(args,k),'bytes':getattr(args,k+'_bytes'),'sha256':getattr(args,k+'_sha256')}
    q=source_module();seed=q.Seed(ref('manifest'),ref('logical-gate'))
    old=q.Runtime(seed,ref('admission'),ref('admission-gate'))
    rt=bind_runtime(q,old,ref('extension-acceptance'),args.operation)
    if args.operation=='candidate':
        need(args.journal is None,'Candidate uses exact old admitted journal only')
        result=candidate(q,rt)
    else:
        prefix='ROOT_COMPLETE214_SYNC_FAST_' if args.operation=='sync' else 'ROOT_COMPLETE214_FAST_READ_'
        rt.refresh()
        journal=q.read_journal(rt.e,args.journal,prefix)
        api=make_readonly_api(q,rt,journal)
        if args.operation=='verify':
            rt.refresh();result=q.verify_immutable(rt,api);rt.refresh()
            result['transport_extension']=api.provenance();rt.e.put(journal,'VERIFIED.json',result)
        elif args.operation=='hold-CAS':
            result=q.hold_CAS(rt,api,journal,ref('preCAS-acceptance'))
            result['transport_extension']=api.provenance()
        elif args.operation=='sync':
            result=q.sync(rt,api,journal,ref('actual-CAS'))
            result={**result,'transport_extension':api.provenance()}
        else:
            q.actual_cas(rt,ref('actual-CAS'),api);q.verify_immutable(rt,api)
            with rt.e.WriterLock(rt.m['writer_lock']) as lock:
                rt.refresh();q.actual_cas(rt,ref('actual-CAS'),api)
                q.checked_pointer(rt,ref('actual-CAS'));q.local_states(rt,all_post=True)
                result=q.main_closure(rt,api);lock.check();rt.refresh()
                q.actual_cas(rt,ref('actual-CAS'),api);q.local_states(rt,all_post=True)
                need(api('GET','git/ref/heads/main')['object']['sha']==result['actual_MAIN_observed'],'R moved after dated closure')
                result['external_Root_terminal_acceptance_inferred']=False
                result['transport_extension']=api.provenance()
                rt.e.put(journal,'TERMINAL_FACTUAL_READOUT.json',result)
        rt.refresh();rt.e.put(journal,'EXTENSION_ACTION_RESULT.json',result)
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()

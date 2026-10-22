"""Independent isolated adversarial controls. Standard library, synthetic only.
Only executes exact source bytes frozen in this audit folder; subprocess is stubbed.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import stat
import types
import tempfile

BASE=Path(__file__).absolute().parent
RESULTS=[]

def check(name,ok,detail=None):
    if not ok: raise RuntimeError('Audit test assertion failed: '+name)
    RESULTS.append({'name':name,'observed':detail})

def rejected(fn):
    try: fn()
    except (RuntimeError,ValueError,KeyError,OSError,TypeError):return True
    return False

def load(name):
    p=BASE/'source_freeze'/name
    raw=p.read_bytes()
    manifest=json.loads((BASE/'SOURCE_FREEZE.json').read_bytes())
    want=manifest['files'][name]
    check('freeze_'+name,len(raw)==want['bytes'] and hashlib.sha256(raw).hexdigest()==want['sha256'])
    m=types.ModuleType('audit_'+name.replace('.','_'));m.__file__=str(p)
    exec(compile(raw,str(p),'exec'),m.__dict__)
    return m

h=load('native209_model.py');x=load('native209_future_executor.py');c=load('native_trees_readonly.py')
def forbidden_transport(*args,**kwargs):raise RuntimeError('REAL TRANSPORT DISABLED BY INDEPENDENT AUDIT')
x.subprocess.run=forbidden_transport
F=Path(tempfile.mkdtemp(prefix='synthetic_fixtures_',dir=BASE))

class NativeFixture:
    def __init__(self):self.number=0;self.trees={};self.blobs={};self.calls=[];self.commits={};self.pr={};self.main=None;self.post_hook=lambda *unused:None;self.get_hook=lambda *unused:None
    def blob(self,raw):
        oid=h.native('blob',raw);self.blobs[oid]=raw;return oid
    def tree(self,rows):
        rows=sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''));oid=c.tree_hash(rows)
        self.trees[oid]={'sha':oid,'truncated':False,'tree':[dict(path=n,mode=m,type=t,sha=s) for n,m,t,s in rows]};return oid
    def flat(self,files):
        trie={}
        for path,raw in files.items():
            node=trie;parts=path.split('/')
            for part in parts[:-1]:node=node.setdefault(part,{})
            node[parts[-1]]=raw
        def rec(node):
            rows=[]
            for name,value in node.items():
                rows.append((name,'040000','tree',rec(value)) if type(value) is dict else (name,'100644','blob',self.blob(value)))
            return self.tree(rows)
        return rec(trie)
    def __call__(self,method,path,body=None,expected_oid=None):
        self.number+=1;self.calls.append((method,path,body))
        if method=='POST':
            self.post_hook(path,body)
            if path=='git/blobs':return {'sha':self.blob(base64.b64decode(body['content']))}
            if path=='git/trees':return {'sha':self.wanted}
            if path=='git/commits':return {'sha':self.candidate}
            raise RuntimeError('Forbidden synthetic POST')
        if method!='GET':raise RuntimeError('Forbidden synthetic method')
        self.get_hook(path)
        if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
        if path=='pulls/209':return self.pr
        kind,oid=path.rsplit('/',1)
        if kind=='git/trees':return self.trees[oid]
        if kind=='git/commits':return self.commits[oid]
        if kind=='git/blobs':
            raw=self.blobs[oid];return {'sha':oid,'size':len(raw),'encoding':'base64','content':base64.b64encode(raw).decode()}
        raise RuntimeError('Unexpected synthetic GET: '+path)

# Canonical trees preserve the entire opaque tuple, including nonregular modes and empty trees.
f=NativeFixture();empty=f.tree([]);blob=f.blob(b'foreign\n')
foreign=f.tree([('empty','040000','tree',empty),('exec','100755','blob',blob),('link','120000','blob',blob),('submodule','160000','commit','e'*40)])
before=f.tree([('foreign','040000','tree',foreign),('own','100644','blob',f.blob(b'before'))])
after=f.tree([('foreign','040000','tree',foreign),('own','100644','blob',f.blob(b'after'))])
w,changed,dirs=h.expected(c,c.NativeTrees(f),before,{'own':b'after'},{'own':('100644','blob',f.blob(b'before'))})
check('canonical_rebuild_foreign_modes_empty_gitlinks',w==after and changed=={'own'} and dirs==set())
check('canonical_full_scope_delta',c.NativeTrees(f).changes(before,after)==({'own'},set(),set()))
check('stale_native_preimage_refused',rejected(lambda:h.expected(c,c.NativeTrees(f),before,{'own':b'after'},{'own':None})))
check('foreign_tree_preserved_opaque',not any(p=='git/trees/'+foreign for _,p,_ in f.calls))
for value in [True,1.0]:check('typed_bytepin_'+repr(value),rejected(lambda value=value:h.bytepin({'bytes':value,'sha256':'0'*64})))
check('duplicate_json_refused',rejected(lambda:h.decode(b'{"a":1,"a":1}')))
for name in ['a/../b','a//b','/absolute','a\\b','a\nb']:
    check('unsafe_rel_'+repr(name),rejected(lambda name=name:h.rel(name)))

# Native fixture exercises the real candidate/state/verify functions while the loader is synthetic.
def setup(label):
    root=F/label;root.mkdir();checkout=root
    x.CHECKOUT=checkout;x.PROGRAM=checkout/'draft_pr_publication_program_20260930';x.PROGRAM.mkdir();x.BASE=root
    h.BASE=root
    (x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock').write_bytes(x.LOCK_BYTES);(x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock').chmod(0o444)
    f=NativeFixture();parent='1'*40;original='2'*40;prepared='3'*40;candidate='4'*40
    oldrow=b'| 222 | 5100015 / AMR-050-0015 | Elliptic-billiard invariant k_{303,b} | 0.1905 | 5.0 | 3 | 2021 | queued | 0/5 |  |  |  |\n'
    q=json.loads((BASE/'QUEUE_ROWS.json').read_bytes());newrow=q['revised'].encode()
    overlay={h.QUEUE:newrow,h.ATTEMPT+'a.bin':b'\xff\0binary',**{p:(b'{"synthetic":true}\n' if p.endswith('.json') else b'new log\n') for p in h.VIEWS}}
    oldprogress=b'{"synthetic_baseline":true}\n'
    oldfiles={h.QUEUE:oldrow,h.VIEWS[2]:oldprogress}
    h.BASELINE_PROGRESS_PIN=h.pin(oldprogress)
    pre={p:None for p in overlay};pre[h.QUEUE]=('100644','blob',f.blob(oldrow));pre[h.VIEWS[2]]=('100644','blob',f.blob(oldprogress))
    # Main retains an explicit shared empty tree; overlay does not touch it.
    maintree=f.flat(oldfiles)
    sharedfiles={'science/'+str(i)+'.txt':('synthetic science '+str(i)+'\n').encode() for i in range(228)}
    shared=f.flat(sharedfiles)
    reused={h.SHARED+'/'+path:{'path':h.SHARED+'/'+path,**h.pin(raw),'git_blob':f.blob(raw)} for path,raw in sharedfiles.items()}
    def insert_tree(root,path,oid):
        def rec(old,parts):
            rows={r['path']:(r['mode'],r['type'],r['sha']) for r in f.trees[old]['tree']}
            name=parts[0]
            rows[name]=('040000','tree',oid if len(parts)==1 else rec(rows[name][2] if name in rows else f.tree([]),parts[1:]))
            return f.tree([(n,*r) for n,r in rows.items()])
        return rec(root,path.split('/'))
    maintree=insert_tree(maintree,h.SHARED,shared)
    wanted,changes,newdirs=h.expected(c,c.NativeTrees(f),maintree,overlay,pre)
    built=insert_tree(f.flat({**oldfiles,**overlay}),h.SHARED,shared)
    check('fixture_independent_tree_rebuild_'+label,wanted==built)
    attempt=c.NativeTrees(f).lookup(wanted,h.ATTEMPT[:-1])[2]
    h.ANCHOR=parent;h.ORIGINAL=original;h.PREPARED=prepared;h.ORIGINAL_TREE=maintree;h.PREPARED_TREE=wanted;h.SHARED_TREE=shared;h.ATTEMPT_TREE=attempt
    m={'expected_parent':parent,'expected_parent_tree':maintree,'phase':'merge95','facts':h.phase_facts('merge95'),'commit_message':'Synthetic audit commit\n','helper_pin':{'bytes':1,'sha256':'0'*64},'executor_pin':{'bytes':1,'sha256':'1'*64},'local_views':[]}
    m['commit_message']='Synthetic audit commit\n'
    m['commit_author']=m['commit_committer']={'name':'Synthetic Auditor','email':'fixture@example.invalid','date':'2026-10-17T00:00:00Z'}
    m['candidate_journal']='journal'
    ls=(x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock').stat()
    m['writer_lock']={'path':h.PROGRAM+'ROOT_GLOBAL_FIVE_WRITER.lock','device':ls.st_dev,'inode':ls.st_ino,**h.pin(x.LOCK_BYTES)}
    candidate=h.commit_request(m,wanted,[parent,prepared])[1]
    for i,p in enumerate(h.VIEWS):
        path=checkout/p;path.parent.mkdir(parents=True,exist_ok=True)
        raw=None if i==0 else b'old local\n'
        if raw is not None:path.write_bytes(raw)
        m['local_views'].append({'path':p,'preimage':None if raw is None else h.pin(raw),'source':None})
    f.main=parent;f.wanted=wanted;f.candidate=candidate
    f.pr={'number':209,'head':{'sha':prepared},'base':{'ref':'main'},'draft':False,'state':'open','merged':False}
    f.commits={parent:{'sha':parent,'tree':{'sha':maintree},'parents':[]},original:{'sha':original,'tree':{'sha':maintree},'parents':[]},prepared:{'sha':prepared,'tree':{'sha':wanted},'parents':[{'sha':original},{'sha':'53b8291b2247008172f1fc3f596c96708faf8903'}]},candidate:{'sha':candidate,'tree':{'sha':wanted},'parents':[{'sha':parent},{'sha':prepared}],'message':m['commit_message']}}
    journal=root/'journal';journal.mkdir()
    return root,f,m,overlay,pre,lambda:(c,m,overlay,pre,reused),journal


# Strict deep typing and exact phase facts.
check('nested_float_pin_refused',not h.exact({'bytes':153.0},{'bytes':153}))
check('nested_bool_counter_refused',not h.exact([True],[1]))
check('membership_float_refused',not h.exact([9.0],[9]))
for phase in ('merge95','completion100'):
    facts=h.phase_facts(phase)
    for key in ('active_PR','case_workflow_estimate_percent','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor'):
        bad={**facts,key:float(facts[key])}
        check('phase_typed_'+phase+'_'+key,rejected(lambda bad=bad,facts=facts:h.matches(bad,facts,'typed facts')))

root,f,m,overlay,pre,loader,j=setup('candidate_positive')
real_api=x.API;x.API=lambda *args,**kwargs:f
try:positive=x.candidate(h,loader,f,j)
finally:x.API=real_api
check('candidate_positive_full_native_readback',positive['full_scope_verified'] and positive['selected_file_count']==235)
check('candidate_current_ready_HEAD_second_parent',positive['parents']==[m['expected_parent'],h.PREPARED])
check('candidate_reuse_same_journal_refused',rejected(lambda:x.candidate(h,loader,f,j)))
other=root/'other_journal';other.mkdir()
check('candidate_alternate_journal_refused',rejected(lambda:x.candidate(h,loader,f,other)))
request,oid=h.commit_request(m,f.wanted,[m['expected_parent'],h.PREPARED])
raw=('tree '+f.wanted+'\n'+'parent '+m['expected_parent']+'\nparent '+h.PREPARED+'\nauthor Synthetic Auditor <fixture@example.invalid> 1792195200 +0000\ncommitter Synthetic Auditor <fixture@example.invalid> 1792195200 +0000\n\n'+m['commit_message']).encode()
check('deterministic_commit_independently_rebuilt',oid==hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
check('deterministic_commit_bad_date_refused',rejected(lambda:h.commit_request({**m,'commit_author':{**m['commit_author'],'date':'2026-02-30T00:00:00Z'}},f.wanted,[m['expected_parent']])) )

root,f,m,overlay,pre,loader,j=setup('candidate_pr_drift')
def change_pr(path,body):
    if path=='git/blobs':f.pr['head']['sha']='f'*40
f.post_hook=change_pr
check('fresh_PR_before_next_POST',rejected(lambda:x.candidate(h,loader,f,j)) and [p for method,p,_ in f.calls if method=='POST']==['git/blobs'])
root,f,m,overlay,pre,loader,j=setup('candidate_local_drift')
def change_local(path,body):
    if path=='git/trees':(x.CHECKOUT/h.VIEWS[1]).write_bytes(b'changed after tree')
f.post_hook=change_local
check('fresh_local_preimage_before_commit',rejected(lambda:x.candidate(h,loader,f,j)) and [p for method,p,_ in f.calls if method=='POST']==['git/blobs','git/trees'])
root,f,m,overlay,pre,loader,j=setup('candidate_reused_body_tamper')
first=next(iter(loader()[-1].values()));f.blobs[first['git_blob']]=b'tampered'
check('reused_full_body_mismatch_stops_before_effect',rejected(lambda:x.candidate(h,loader,f,j)) and not any(method=='POST' for method,_,_ in f.calls))

root,f,m,overlay,pre,loader,j=setup('lock_identity')
lockpath=x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock';expected=m['writer_lock']
with x.WriterLock(expected):pass
check('pinned_lock_positive',True)
for key in ('device','inode','bytes'):
    check('lock_float_'+key,rejected(lambda key=key:x.WriterLock({**expected,key:float(expected[key])})))
# Rename preserves the original inode and ensures the replacement gets a different one.
lockpath.rename(lockpath.with_name('old_lock'));lockpath.write_bytes(x.LOCK_BYTES);lockpath.chmod(0o444)
check('same_payload_replacement_lock_refused',rejected(lambda:x.WriterLock(expected).__enter__()))

# Descriptor readers prevent leaf and ancestor swaps before following attacker targets.
x.CHECKOUT=F
for label,reader in [('local',lambda p:x.local_pin(h,p)),('sealed',lambda p:h.sealed(p.name,h.pin(b'old')))]:
    directory=F/('read_'+label);directory.mkdir();p=directory/'target';p.write_bytes(b'old');p.chmod(0o444);victim=directory/'victim';victim.write_bytes(b'synthetic outside sentinel');victim.chmod(0o444)
    h.BASE=directory;real_open=os.open;triggered=[]
    def race_leaf(path,flags,*args,**kwargs):
        if path=='target' and kwargs.get('dir_fd') is not None and not triggered:
            p.rename(directory/'old_target');p.symlink_to(victim);triggered.append(True)
        return real_open(path,flags,*args,**kwargs)
    os.open=race_leaf
    try:refused=rejected(lambda:reader(p))
    finally:os.open=real_open
    check(label+'_leaf_swap_refused_before_read',triggered and refused)
    check(label+'_static_symlink_refused',rejected(lambda:reader(p)))
for label,reader in [('local',lambda p:x.local_pin(h,p)),('sealed',lambda p:h.sealed('component/target',h.pin(b'old')))]:
    directory=F/('ancestor_'+label);directory.mkdir();component=directory/'component';component.mkdir();p=component/'target';p.write_bytes(b'old');p.chmod(0o444)
    victim=directory/'victim';victim.mkdir();(victim/'target').write_bytes(b'synthetic outside sentinel');h.BASE=directory
    real_open=os.open;triggered=[]
    def race_ancestor(path,flags,*args,**kwargs):
        if path=='component' and kwargs.get('dir_fd') is not None and not triggered:
            component.rename(directory/'saved');component.symlink_to(victim,target_is_directory=True);triggered.append(True)
        return real_open(path,flags,*args,**kwargs)
    os.open=race_ancestor
    try:refused=rejected(lambda:reader(p))
    finally:os.open=real_open
    check(label+'_ancestor_swap_refused_before_read',triggered and refused)

# Actual API mechanism: mocked transport, real immutable intents, no service calls.
root,f,m,overlay,pre,loader,j=setup('uncertain_dispatch');transports=[];real_transport=x.run_bounded
body,expected=h.commit_request(m,f.wanted,[m['expected_parent'],h.PREPARED])
def unavailable(*args,**kwargs):transports.append(args);raise TimeoutError('synthetic lost response')
x.run_bounded=unavailable
try:
    a=x.API(h,j,mutate=True)
    check('uncertain_POST_stops',rejected(lambda:a('POST','git/commits',body,expected_oid=expected)))
    check('uncertain_API_no_retry',rejected(lambda:a('POST','git/commits',body,expected_oid=expected)) and len(transports)==1)
finally:x.run_bounded=real_transport
intent=json.loads((j/'00001.OBJECT_INTENT.json').read_bytes())
check('durable_exact_known_object_intent',intent['exact_request']==body and intent['expected_oid']==expected and intent['request_pin']==x.pin(x.enc(body)))
reconcile=root/'reconcile';reconcile.mkdir();calls=[]
def known_get(argv,request):calls.append((argv,request));return types.SimpleNamespace(returncode=0,stdout=json.dumps({'sha':expected}).encode(),stderr=b'')
x.run_bounded=known_get
try:
    api=x.API(h,reconcile,mutate=False)
    check('known_object_reconcile_GET_only',api('GET','git/commits/'+expected)['sha']==expected and rejected(lambda:api('POST','git/commits',body,expected_oid=expected)) and len(calls)==1)
    check('no_ref_writer_route',rejected(lambda:api('PATCH','git/refs/heads/main',{'sha':expected,'force':False})))
finally:x.run_bounded=real_transport

# Gate reversal after first installed view must stop, leave no success pointer, then recover safely.
def actual_gate(root,f,m):
    wanted={'bytes':1,'sha256':'2'*64}
    a={'schema':'pr209-root-native-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':209,'phase':m['phase'],'accepted':True,'manifest_pin':wanted,'helper_pin':m['helper_pin'],'executor_pin':m['executor_pin'],'core_pin':h.CORE_PIN,'facts':m['facts'],'parent':m['expected_parent'],'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,'candidate':f.candidate,'tree':f.wanted,'actual_MAIN_observed':f.candidate,'Root_ref_update':{'expected_sha':m['expected_parent'],'sha':f.candidate,'force':False,'success_confirmed_by_actual_native_readback':True}}
    p=root/'synthetic_actual_gate.json';raw=x.enc(a);p.write_bytes(raw);p.chmod(0o444);return wanted,p,raw,h.pin(raw)
root,f,m,overlay,pre,loader,j=setup('sync_gate_drift');f.main=f.candidate;wanted,apath,raw,ap=actual_gate(root,f,m)
real_put=x.put;revoked=[]
def revoke_after_first(directory,name,value):
    real_put(directory,name,value)
    if name=='VIEW_0.json':apath.chmod(0o644);apath.write_bytes(b'{"revoked":true}\n');apath.chmod(0o444);revoked.append(True)
x.put=revoke_after_first
try:failed=rejected(lambda:x.sync(h,loader,f,j,wanted,apath.name,ap))
finally:x.put=real_put
pointer=root/'ROOT_ACTUAL_MERGE95_POINTER.json'
check('sync_gate_drift_stops_no_pointer',failed and revoked and not pointer.exists() and not (j/'LOCAL_GLOBAL_FIVE_SYNC.json').exists())
check('sync_partial_first_post_remaining_pre',x.local_pin(h,x.CHECKOUT/h.VIEWS[0])==h.pin(overlay[h.VIEWS[0]]) and all(x.local_pin(h,x.CHECKOUT/r['path'])==r['preimage'] for r in m['local_views'][1:]))
apath.chmod(0o644);apath.write_bytes(raw);apath.chmod(0o444);recover=root/'recovery';recover.mkdir()
receipt=x.sync(h,loader,f,recover,wanted,apath.name,ap)
check('sync_partial_recovery_exact_all_five',pointer.is_file() and receipt['all_five_local_files_match_actual_checkpoint'] and all(x.local_pin(h,x.CHECKOUT/p)==h.pin(overlay[p]) for p in h.VIEWS))
check('sync_lock_inode_preserved',(x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock').stat().st_ino==m['writer_lock']['inode'])
check('sync_duplicate_pointer_refused',rejected(lambda:x.sync(h,loader,f,root,wanted,apath.name,ap)))

# Real local child processes exercise capped transport; the argv is never GH or any provider.
import sys
argv=[sys.executable,'-E','-S','-B','-P','-c']
result=x.run_bounded(argv+["import sys; data=sys.stdin.buffer.read();sys.stdout.buffer.write(data);sys.stderr.buffer.write(b'ok')"],b'local synthetic bytes')
check('bounded_transport_concurrent_pipes_positive',result.returncode==0 and result.stdout==b'local synthetic bytes' and result.stderr==b'ok')
for channel,count in [('stdout',12_000_001),('stderr',65537)]:
    try:x.run_bounded(argv+["import sys;sys."+channel+".buffer.write(b'x'*"+str(count)+")"],None)
    except x.BoundedTransportFailure as error:
        check('bounded_transport_'+channel+'_overflow',error.receipt[channel+'_pin']['bytes'] <= error.receipt[channel+'_cap'] and error.receipt['process_killed_and_reaped'])
    else:raise RuntimeError('Expected transport overflow')


# Successful fixed-SHA in-memory GET reuse must preserve native validation and freshness.
root,f,m,overlay,pre,loader,j=setup('immutable_memo');real_transport=x.run_bounded;wire=[]
rawbody=b'synthetic immutable cache body\n';boid=f.blob(rawbody);toid=f.tree([('body','100644','blob',boid)])
def memo_transport(argv,request):
    path=argv[4].split('/Math/',1)[1];wire.append((path,request))
    if path in ('git/blobs/'+boid,'git/trees/'+toid):value=f('GET',path)
    elif path=='git/ref/heads/main':value={'object':{'sha':str(len(wire)).zfill(40)}}
    elif path=='pulls/209':value={'number':209,'fresh_marker':len(wire)}
    elif path.startswith('compare/'):value={'status':'ahead','fresh_marker':len(wire)}
    elif path=='git/commits':value={'sha':'a'*40}
    else:raise RuntimeError('Unexpected memo fixture transport')
    return types.SimpleNamespace(returncode=0,stdout=x.enc(value),stderr=b'')
x.run_bounded=memo_transport
try:
    api=x.API(h,j,mutate=True)
    first=api('GET','git/blobs/'+boid);first['content']='mutated returned value';first['size']=999
    check('memo_return_mutation_cannot_poison_cached_body',h.read_blob(api,boid)==rawbody and len(wire)==1)
    check('memo_tree_reauthenticated',c.NativeTrees(api).get(toid,0)=={'body':('100644','blob',boid)})
    check('memo_tree_repeat_preserves_validation',c.NativeTrees(api).get(toid,0)=={'body':('100644','blob',boid)} and len(wire)==2)
    for route in ['git/ref/heads/main','pulls/209','compare/'+'1'*40+'...'+'2'*40]:
        before=len(wire);a=api('GET',route);b=api('GET',route)
        check('memo_mutable_fresh_'+route.split('/')[0],len(wire)==before+2 and a!=b)
    api('POST','git/commits',{'synthetic':True},expected_oid='a'*40)
    check('memo_never_stores_POST',set(api._immutable_cache)=={'git/blobs/'+boid,'git/trees/'+toid})
    second=root/'fresh_reader';second.mkdir();fresh=x.API(h,second,mutate=False);before=len(wire)
    check('memo_fresh_independent_API_starts_empty',not fresh._immutable_cache and h.read_blob(fresh,boid)==rawbody and len(wire)==before+1)
    original,expected,origin=api._immutable_cache['git/blobs/'+boid]
    api._immutable_cache['git/blobs/'+boid]=(original+b' ',expected,origin);before=len(wire)
    check('memo_corruption_fails_closed_no_dispatch',rejected(lambda:api('GET','git/blobs/'+boid)) and api.failed and len(wire)==before)
    check('memo_corruption_no_automatic_retry',rejected(lambda:api('GET','git/blobs/'+boid)) and len(wire)==before)
    badj=root/'wrong_route_identity';badj.mkdir();bad=x.API(h,badj,mutate=False)
    def wrong_sha(argv,request):return types.SimpleNamespace(returncode=0,stdout=b'{"sha":"0000000000000000000000000000000000000000"}',stderr=b'')
    x.run_bounded=wrong_sha
    check('memo_route_SHA_mismatch_never_cached',rejected(lambda:bad('GET','git/blobs/'+boid)) and not bad._immutable_cache and bad.failed)
    dupej=root/'duplicate_json';dupej.mkdir();bad=x.API(h,dupej,mutate=False)
    x.run_bounded=lambda *args:types.SimpleNamespace(returncode=0,stdout=('{"sha":"'+boid+'","sha":"'+boid+'"}').encode(),stderr=b'')
    check('memo_duplicate_JSON_never_cached',rejected(lambda:bad('GET','git/blobs/'+boid)) and not bad._immutable_cache)
finally:x.run_bounded=real_transport


# Full actual verifier path through the memo API, against the independent native fixture.
root,f,m,overlay,pre,loader,j=setup('memo_full_native_verify');wire=[];real_transport=x.run_bounded
reused=loader()[-1]
def full_transport(argv,request):
    path=argv[4].split('/Math/',1)[1];wire.append(path)
    return types.SimpleNamespace(returncode=0,stdout=x.enc(f('GET',path)),stderr=b'')
x.run_bounded=full_transport
try:
    api=x.API(h,j,mutate=False)
    result=h.verify(c,m,overlay,pre,reused,api,f.candidate)
    immutable=[p for p in wire if p.startswith(('git/blobs/','git/trees/','git/commits/'))]
    check('memo_full_scope_and_all_228_reused_bodies',result['full_scope_verified'] and result['all_selected_native_bodies_verified'] and result['selected_file_count']==235 and len(immutable)==len(set(immutable)) and api.number>len(wire))
    check('memo_complete_verification_stays_readonly',not any(p in ('git/blobs','git/trees','git/commits') for p in wire))
finally:x.run_bounded=real_transport
root,f,m,overlay,pre,loader,j=setup('memo_bad_native_body');badrow=next(iter(loader()[-1].values()));f.blobs[badrow['git_blob']]=b'synthetic tampered response body'
x.run_bounded=lambda argv,request:types.SimpleNamespace(returncode=0,stdout=x.enc(f('GET',argv[4].split('/Math/',1)[1])),stderr=b'')
try:
    api=x.API(h,j,mutate=False)
    check('memo_does_not_bypass_full_body_authentication',rejected(lambda:h.verify(c,m,overlay,pre,loader()[-1],api,f.candidate)))
finally:x.run_bounded=real_transport

out={'schema':'pr209-independent-final-source-offline-adversarial-results-v1','UTC':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'status':'PASS_SOURCE_ONLY_CONDITIONAL','test_count':len(RESULTS),'results':RESULTS,'external_calls':0,'production_mutations':0,'scope':'Exact replacement source freeze; synthetic loader/native providers/local files and local Python child transport controls. Actual Root manifest/candidate/CAS/source gates/science not certified.'}
result_path=BASE/'OFFLINE_RESULTS.json'
if result_path.exists():
    descriptor,replay_name=tempfile.mkstemp(prefix='REPLAY_OFFLINE_RESULTS_',suffix='.json',dir=BASE)
    with os.fdopen(descriptor,'w') as replay:replay.write(json.dumps(out,sort_keys=True,indent=2)+'\n')
else:result_path.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
__import__('shutil').rmtree(F)
print(json.dumps({'status':out['status'],'tests':out['test_count']},sort_keys=True))

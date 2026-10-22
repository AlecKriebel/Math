"""Independent finite actual-source adversary; isolated fake native effects only.

No production CLI, original lock, current five, network, Git, provider or ref
write is permitted. Unchanged production sources are compiled in a temporary
owned checkout. Synthetic Root-shaped records are explicitly fixture-only.
"""
from pathlib import Path
import ast,base64,copy,datetime,hashlib,itertools,json,os,shutil,socket,stat,subprocess,sys,tempfile,threading,time,types

D=Path(__file__).absolute().parent
A=D.parent
S=A/'concurrent_native_integration_01'
B=A/'native_adoption_preparation_01'
SOURCE={'bytes':50308,'sha256':'4e0304a5cfe9d6e74b8b2f3622ed513d59060c6f39002978a04068acca961588'}
RESULT=[]

def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(o):return (json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def need(x,msg):
    if type(x) is not bool or not x:raise AssertionError(msg)
def yes(x,name):need(x,name);RESULT.append({'test':name,'outcome':'PASS'})
def no(fn,name):
    try:fn()
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,AssertionError) as e:
        RESULT.append({'test':name,'outcome':'REFUSED_AS_EXPECTED','exception':type(e).__name__,'reason':str(e)[:180]})
    else:raise AssertionError('Unexpected acceptance: '+name)
def load(path,raw):
    m=types.ModuleType('independent_fixture_'+path.stem);m.__file__=str(path)
    exec(compile(raw,str(path),'exec'),m.__dict__);return m
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and not p.is_symlink():p.chmod(0o644)
    p.write_bytes(b);p.chmod(0o444)
def deny(*a,**k):raise AssertionError('Real network/process operation forbidden by independent audit')

class Fixture:
    def __init__(self,root,source_raw):
        self.root=root;self.program=root/'draft_pr_publication_program_20260930'
        self.case=self.program/'audits/pr211_5100063';self.native=self.case/'native_adoption_preparation_01'
        self.src=self.case/'concurrent_native_integration_01';self.src.mkdir(parents=True)
        def cp(p,dest):write(dest,p.read_bytes())
        binding=json.loads((A/'native_input_snapshot_preparation_01/FROZEN_OPERATOR_SOURCE_BINDINGS.json').read_bytes())
        for n in binding['files']:cp(B/n,self.native/n)
        for n in ['snapshot_preimages.py','FROZEN_OPERATOR_SOURCE_BINDINGS.json']:
            cp(A/'native_input_snapshot_preparation_01'/n,self.case/'native_input_snapshot_preparation_01'/n)
        sm=json.loads((S/'SOURCE_MANIFEST.json').read_bytes())
        for n in [r['path'] for r in sm['files']]+['SOURCE_MANIFEST.json','EXTERNAL_SEAL.json']:cp(S/n,self.src/n)
        logical=json.loads((B/'_private_ROOT_INPUTS_ADOPTION100_06/INPUT_MANIFEST.json').read_bytes())
        gate=json.loads((B/'ROOT_ADOPTION100_MODEL_ACCEPTANCE_06.json').read_bytes())
        oldnames={'_private_ROOT_INPUTS_ADOPTION100_06/INPUT_MANIFEST.json','ROOT_ADOPTION100_MODEL_ACCEPTANCE_06.json'}
        oldnames.update(r['source'] for r in logical['files'])
        oldnames.update(r['source'] for r in logical['local_views'] if r['source'])
        oldnames.update(r['path'] for r in gate['native_audits'])
        for n in oldnames:cp(B/n,self.native/n)
        ck=A/'concurrent_native_body_cache_01';cm=json.loads((ck/'ROOT_ACTUAL_GET_CACHE_01/BODY_CACHE_MANIFEST.json').read_bytes())
        names={'BODY_CACHE_MANIFEST.json','BODY_CACHE_EXTERNAL_SEAL.json','FROZEN_COLLECTION_INPUT.json'}
        names.update(o[k]['path'] for o in cm['objects'] for k in ['raw_response','receipt','stderr'])
        for n in names:cp(ck/'ROOT_ACTUAL_GET_CACHE_01'/n,self.case/'concurrent_native_body_cache_01/ROOT_ACTUAL_GET_CACHE_01'/n)
        for n in ['collect_native_body_cache.py','ROOT_NATIVE_BODY_CACHE_ACCEPTANCE_01.json']:
            cp(ck/n,self.case/'concurrent_native_body_cache_01'/n)
        self.v=load(self.src/'concurrent_checkpoint.py',source_raw)
        self.seed=self.v.Seed();self.h,self.c,self.e=self.seed.h,self.seed.c,self.seed.e
        yes(len(self.seed.bodies)==202 and sum(map(len,self.seed.bodies.values()))==2756787,'unchanged_Seed_complete_cloned202_raw_GET_cache_and_original18')
        self.objects={};self.blobs={};self.commits={};self.edges={};self.calls=[];self.posts=[];self.overrides={};self.ref_reads=0
        self.ref='0'*40;self.ref_hook=None;self.post_fail=None
        self.local_before={r['path']:self.h.sealed(r['source'],r['preimage']) if r['preimage'] else None for r in logical['local_views']}
        # Recreate exactly the fixed historical parent-preimage tuples from their
        # separately frozen local bodies, not a fabricated source of GET bytes.
        self.before={}
        for r in logical['files']:
            if r['preimage']:
                body=self.local_before[r['path']]
                need(body is not None and self.blob(body)==r['preimage']['sha'],'fixture exact native preimage/body association')
                self.before[r['path']]=(r['preimage']['mode'],r['preimage']['type'],r['preimage']['sha'])
        h=self.h
        self.before.update({h.ATTEMPT[:-1]:('040000','tree',h.ATTEMPT_TREE),h.SHARED:('040000','tree',h.SHARED_TREE),h.QUEUE:h.tuple_pin(logical['protected_queue'])})
        self.foreign={'foreign/run':('100755','blob',self.blob(b'executable\n')),'foreign/link':('120000','blob',self.blob(b'../target')),'foreign/submodule':('160000','commit','9'*40),'foreign/empty':('040000','tree',self.tree({}))}
        self.before.update(self.foreign)
        # Exact25 policy needs one chosen fixture directory shape. These names
        # are historical plan data only; no live lease or execution is inferred.
        added=set(json.loads((B/'ROOT_PLAN_ADOPTION100_STDOUT_06.json').read_bytes())['new_directories'])
        self.existing=set()
        for p in self.seed.overlay:
            ps=p.split('/')
            for i in range(1,len(ps)):
                n='/'.join(ps[:i])
                if n not in added:self.existing.add(n)
        maps=json.loads((A/'native_custody_01/FINAL_NATIVE_TREES_SUPPLEMENT.json').read_bytes())
        for oid,entries in maps.items():
            computed=self.tree({n:(r['mode'],r['type'],r['sha']) for n,r in entries.items()})
            need(computed==oid,'authenticated historical immediate tree for fixture')
        self.parent_tree=self.build(self.before)
        self.parent=self.commit(self.parent_tree,[h.ANCHOR,h.MERGED],date='2026-10-17T21:00:00Z',message='Independent audit synthetic parent\n')
        self.after={**self.before,**{p:('100644','blob',self.blob(b)) for p,b in self.seed.overlay.items()}}
        self.target_tree=self.build(self.after)
        date='2026-10-17T21:00:01Z'
        self.a={'schema':'pr211-concurrent-parent-admission-v1','PR':211,'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,'logical_manifest_pin':self.v.MP,'logical_gate_pin':self.v.GP,'cache_manifest_pin':self.v.CM,'cache_acceptance_pin':self.v.CA,'facts':logical['facts'],'parent':self.parent,'parent_tree':self.parent_tree,'created_UTC':date,'commit_author':{**logical['commit_author'],'date':date},'commit_committer':{**logical['commit_committer'],'date':date},'commit_message':logical['commit_message'],'parents':[self.parent],'tree':self.target_tree,'candidate':'0'*40,'candidate_journal':'ROOT_CONCURRENT_CANDIDATE_INDEPENDENT'}
        tmp={**logical,'commit_author':self.a['commit_author'],'commit_committer':self.a['commit_committer']}
        self.request,self.target=h.commit_request(tmp,self.target_tree,[self.parent]);self.a['candidate']=self.target
        self.commits[self.target]={'sha':self.target,'tree':{'sha':self.target_tree},'parents':[{'sha':self.parent}],**{k:self.request[k] for k in ['author','committer','message']}}
        self.edges[self.target]=[self.parent]
        self.commits.update({h.ORIGINAL:{'sha':h.ORIGINAL,'tree':{'sha':h.ORIGINAL_TREE},'parents':[{'sha':'a3bdcb55173cb41866a58aded968b68d6a14d1a4'}]},h.PREPARED:{'sha':h.PREPARED,'tree':{'sha':h.PREPARED_TREE},'parents':[{'sha':h.ORIGINAL},{'sha':h.PREPARED_SECOND_PARENT}]},h.MERGED:{'sha':h.MERGED,'tree':{'sha':h.MERGED_TREE},'parents':[{'sha':h.MERGE_FIRST_PARENT},{'sha':h.PREPARED}]}})
        self.pr={'number':211,'head':{'sha':h.PREPARED},'base':{'ref':'main'},'draft':False,'state':'closed','merged':True,'merge_commit_sha':h.MERGED,'merged_at':h.MERGED_AT}
        self.rt=types.SimpleNamespace(seed=self.seed,h=h,c=self.c,e=self.e,admission=self.a,admission_pin=pin(enc(self.a)),gate_pin=pin(b'fixture-gate'),m=self.v.checked_admission(self.seed,self.a),overlay=self.seed.overlay,pre=self.seed.pre,reused=self.seed.reused,bodies=self.seed.bodies)
        self.refresh_hook=None;self.refreshes=0
        def refresh():
            self.refreshes+=1
            if self.refresh_hook:self.refresh_hook()
            return self.rt
        self.rt.refresh=refresh
        self.lockpath=self.program/'ROOT_GLOBAL_FIVE_WRITER.lock';write(self.lockpath,self.e.LOCK_BYTES)
        st=self.lockpath.stat();self.fixture_lock={**h.WRITER_LOCK_REFERENCE,'device':st.st_dev,'inode':st.st_ino}
        self.rt.m['writer_lock']=self.fixture_lock
        self.ref=self.parent;self.reset_locals([False]*5)
        # Only the temporary executor transport is replaced by an explicit fake.
        # Unchanged candidate/API/intent/guard code otherwise runs as authored.
        self.e.run_bounded=self.transport
    def blob(self,b):
        oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();self.blobs[oid]=b;return oid
    def tree(self,entries):
        rows=sorted(entries.items(),key=lambda r:r[0].encode()+(b'/' if r[1][0]=='040000' else b''))
        raw=b''.join((v[0].lstrip('0')+' '+n).encode()+b'\0'+bytes.fromhex(v[2]) for n,v in rows)
        oid=hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        self.objects[oid]={'sha':oid,'truncated':False,'tree':[{'path':n,'mode':v[0],'type':v[1],'sha':v[2]} for n,v in rows]};return oid
    def build(self,leaves):
        trie={}
        for p in sorted(self.existing,key=lambda s:(s.count('/'),s)):
            t=trie
            for n in p.split('/'):t=t.setdefault(n,{})
        for p,v in leaves.items():
            t=trie
            for n in p.split('/')[:-1]:t=t.setdefault(n,{})
            t[p.split('/')[-1]]=v
        def descend(t):return self.tree({n:('040000','tree',descend(v)) if isinstance(v,dict) else v for n,v in t.items()})
        return descend(trie)
    def commit(self,root,parents,date='2026-10-17T21:01:00Z',message='Independent synthetic foreign change\n'):
        m={**self.seed.logical,'commit_author':{**self.seed.logical['commit_author'],'date':date},'commit_committer':{**self.seed.logical['commit_committer'],'date':date},'commit_message':message}
        request,oid=self.h.commit_request(m,root,parents)
        self.commits[oid]={'sha':oid,'tree':{'sha':root},'parents':[{'sha':p}for p in parents],**{k:request[k]for k in ['author','committer','message']}};self.edges[oid]=list(parents);return oid
    def ancestor(self,base,head):
        seen=set();todo=[head]
        while todo:
            cur=todo.pop()
            if cur==base:return True
            if cur not in seen:seen.add(cur);todo.extend(self.edges.get(cur,[]))
        return False
    def observer(self,method,path,body=None):
        need(method=='GET' and body is None,'fake observer GET only');self.calls.append(path)
        if path in self.overrides:return copy.deepcopy(self.overrides[path])
        if path=='git/ref/heads/main':
            self.ref_reads+=1
            if self.ref_hook:return self.ref_hook(self.ref_reads)
            return {'ref':'refs/heads/main','object':{'type':'commit','sha':self.ref}}
        if path=='pulls/211':return copy.deepcopy(self.pr)
        if path.startswith('compare/'):
            l,r=path.split('/')[1].split('...');return {'status':'identical' if l==r else 'ahead' if self.ancestor(l,r) else 'diverged','merge_base_commit':{'sha':l if self.ancestor(l,r) else '0'*40}}
        oid=path.rsplit('/',1)[1]
        if path.startswith('git/trees/'):return copy.deepcopy(self.objects[oid])
        if path.startswith('git/commits/'):return copy.deepcopy(self.commits[oid])
        if path.startswith('git/blobs/'):
            b=self.blobs[oid];return {'sha':oid,'size':len(b),'encoding':'base64','content':base64.b64encode(b).decode()}
        raise AssertionError('Unrecognized fake GET')
    def transport(self,argv,request):
        need(argv[:5]==[self.e.GH,'api','--hostname','github.com','--method'],'fixed host transport shape')
        method=argv[5];path=argv[6].removeprefix('repos/AlecKriebel/Math/')
        need(argv[6].startswith('repos/AlecKriebel/Math/'),'fixed repo transport')
        if method=='GET':value=self.observer(method,path)
        else:
            need(method=='POST' and path in ['git/trees','git/commits'],'fake immutable-only POST')
            body=self.h.decode(request);self.posts.append((path,body))
            if self.post_fail==path:raise RuntimeError('Synthetic uncertain transport after dispatch')
            if path=='git/trees':
                need(body['base_tree']==self.parent_tree,'fake POST exact base tree')
                need(body['tree']==[{'path':p,'mode':'100644','type':'blob','content':b.decode()}for p,b in sorted(self.seed.overlay.items())],'fake POST exact192 full contents')
                value={'sha':self.target_tree}
            else:need(self.h.exact(body,self.request),'fake POST canonical request');value={'sha':self.target}
        return types.SimpleNamespace(returncode=0,stdout=enc(value),stderr=b'')
    def record(self,name,obj):
        p=self.case/'_synthetic_authority_not_usable'/name
        raw=enc({**obj,'synthetic_fixture_only_not_Root_authority':True});write(p,raw);return {'path':str(p),**pin(raw)}
    def reset_locals(self,posts):
        for r,ispost in zip(self.rt.m['local_views'],posts):
            b=self.rt.overlay[r['path']] if ispost else self.local_before[r['path']]
            p=self.root/r['path']
            if b is None:
                if p.exists()or p.is_symlink():p.unlink()
            else:write(p,b)
    def cas_records(self,proof):
        v=self.v;r=self.rt;a=self.a
        reports=[self.record('proof_'+str(i)+'.json',proof)for i in [1,2]]
        self.pre_obj={'schema':'pr211-root-concurrent-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':211,'accepted':True,'protocol_pin':self.seed.source_pin,'admission_pin':r.admission_pin,'logical_manifest_pin':v.MP,'logical_gate_pin':v.GP,'candidate':self.target,'tree':self.target_tree,'immutable_candidate_verification_accepted':True,'independent_GET_candidate_verification_accepted':True,'cache_manifest_pin':v.CM,'cache_acceptance_pin':v.CA,'verification_reports':reports}
        self.pre_ref=self.record('preCAS.json',self.pre_obj)
        self.ready_obj={'schema':'pr211-concurrent-locked-CAS-ready-v1','evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS','protocol_pin':self.seed.source_pin,'admission_pin':r.admission_pin,'parent':self.parent,'candidate':self.target,'original_stable_lock_held':True,'guard_pid':12345}
        self.ready_ref=self.record('ready.json',self.ready_obj)
        self.req_obj={'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main','expected_sha':self.parent,'sha':self.target,'force':False};req=self.record('request.json',self.req_obj)
        self.res_ref=self.record('response.json',{'isError':False,'structuredContent':{'success':True}})
        self.read_ref=self.record('readback.json',{'ref':'refs/heads/main','object':{'type':'commit','sha':self.target}})
        receipt=self.record('readback_receipt.json',{'method':'GET','path':'git/ref/heads/main','exit':0,'stdout_pin':{k:self.read_ref[k]for k in ['bytes','sha256']}})
        self.poll_obj={'session_id':98765,'output':'','exit_code':None};poll=self.record('poll.json',self.poll_obj)
        self.conf_obj={'schema':'pr211-root-postCAS-same-live-guard-confirmation-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'protocol_pin':self.seed.source_pin,'admission_pin':r.admission_pin,'actual_lock_guard_ready_pin':{k:self.ready_ref[k]for k in ['bytes','sha256']},'actual_tool_response_pin':{k:self.res_ref[k]for k in ['bytes','sha256']},'actual_readback_response_pin':{k:self.read_ref[k]for k in ['bytes','sha256']},'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,'original_lock_continuity_from_linear_held_source_and_same_live_session':True,'guard_pid':12345,'session_id':98765,'actual_same_session_poll_response':poll}
        conf=self.record('confirmation.json',self.conf_obj)
        self.cas_obj={'schema':'pr211-root-concurrent-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':211,'accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math','protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,'admission_pin':r.admission_pin,'logical_manifest_pin':v.MP,'logical_gate_pin':v.GP,'cache_manifest_pin':v.CM,'cache_acceptance_pin':v.CA,'facts':r.m['facts'],'parent':self.parent,'candidate':self.target,'tree':self.target_tree,'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False,'actual_MAIN_after_CAS':self.target,'preCAS_acceptance':self.pre_ref,'actual_lock_guard_ready':self.ready_ref,'actual_tool_request':req,'actual_tool_response':self.res_ref,'actual_readback_response':self.read_ref,'actual_readback_receipt':receipt,'post_CAS_same_live_guard_confirmation':conf}
        self.cas=self.record('actual_CAS.json',self.cas_obj);return self.cas

def pipe_controls(v):
    cases=[('short',b'{}\n',b'{}',True),('max4096',b'{}'+b' '*4093+b'\n',b'{}'+b' '*4093,True),('max4096_queuedjunk',b'{}'+b' '*4093+b'\nJUNK',None,True),('two_lines',b'{}\n{}\n',None,True),('prefix_tail',b'{}\nX',None,True),('partial_eof',b'{',None,True),('empty_eof',b'',None,True),('partial_open_timeout',b'{',None,False),('oversize',b'x'*4097,None,True)]
    for blocking in [False,True]:
        for name,payload,expected,close in cases:
            r,w=os.pipe();os.set_blocking(r,blocking);calls=[];started=time.monotonic()
            try:
                if payload:os.write(w,payload)
                if close:os.close(w);w=None
                fn=lambda:v.wait_actual_CAS_reference(r,lambda:calls.append(1),timeout=.04)
                if expected is None:no(fn,'framing_'+name+'_'+str(blocking))
                else:yes(fn()==expected,'framing_'+name+'_'+str(blocking))
                yes(os.get_blocking(r)==blocking and bool(calls) and time.monotonic()-started<1,'framing_restored_flags_bounded_'+name+'_'+str(blocking))
            finally:
                os.close(r)
                if w is not None:os.close(w)
    r,w=os.pipe()
    try:
        os.write(w,b'{}\n')
        no(lambda:v.wait_actual_CAS_reference(r,lambda:(_ for _ in()).throw(RuntimeError('lock changed')),.04),'handshake_guard_failure')
        yes(os.get_blocking(r),'handshake_exception_restores_blocking')
    finally:os.close(r);os.close(w)

def cache_controls(f):
    v,h=f.v,f.h;cm=json.loads((v.CACHE/'BODY_CACHE_MANIFEST.json').read_bytes());o=copy.deepcopy(cm['objects'][17])
    raw=(v.CACHE/o['raw_response']['path']).read_bytes();rec=(v.CACHE/o['receipt']['path']).read_bytes()
    yes(v.validate_object(h,o,raw,rec,b'')==f.seed.bodies[o['oid']],'actual_cache_inner_positive')
    def altered(change_response=None,change_receipt=None,raw_literal=None):
        row=copy.deepcopy(o);rr=raw if change_response is None else enc({**h.decode(raw),**change_response})
        if raw_literal is not None:rr=raw_literal
        row['raw_response'].update(pin(rr));rc={**h.decode(rec),'stdout':row['raw_response']}
        if change_receipt:rc.update(change_receipt)
        rb=enc(rc);row['receipt'].update(pin(rb))
        return v.validate_object(h,row,rr,rb,b'')
    for k,x in [('sha','0'*40),('size',True),('size',0.0),('size',4000001),('size',0),('encoding','utf8'),('content','not/base64!'),('content',''),('content',base64.b64encode(b'other body').decode())]:
        no(lambda k=k,x=x:altered({k:x}),'repinned_cache_response_'+k+'_'+str(x)[:24])
    for k,x in [('method','POST'),('path','git/ref/heads/main'),('path','git/blobs/'+'0'*40),('exit',False),('exit',1),('no_retry',1),('no_retry',False),('expected_body_pin',{'bytes':0,'sha256':'0'*64})]:
        no(lambda k=k,x=x:altered(change_receipt={k:x}),'repinned_cache_receipt_'+k+'_'+str(x)[:24])
    duplicate=raw.rstrip()[:-1]+b',"sha":"'+o['oid'].encode()+b'"}'
    no(lambda:altered(raw_literal=duplicate),'repinned_cache_duplicate_inner_JSON')
    no(lambda:altered(raw_literal=b'{"sha":NaN}'),'repinned_cache_nonfinite_inner_JSON')

def source_runtime_controls(f):
    v,h=f.v,f.h
    # The unchanged complete Seed reads all source/cache bodies in this clone.
    for path,kind in [(f.src/'README.md','new_source_payload'),(f.native/'native_trees_readonly.py','original_bound_source'),(v.CACHE/json.loads((v.CACHE/'BODY_CACHE_MANIFEST.json').read_bytes())['objects'][0]['raw_response']['path'],'raw_cache'),(f.native/v.GN,'legacy_logical_gate')]:
        b=path.read_bytes();write(path,b+b' ')
        no(f.seed.refresh,'full_Seed_changed_'+kind+'_refused');write(path,b);f.seed.refresh()
    path=f.src/'README.md';b=path.read_bytes();path.chmod(0o644)
    no(f.seed.refresh,'full_Seed_writable_source_refused');path.chmod(0o444)
    target=path.with_name('fixture_readme_backing');write(target,b);path.unlink();path.symlink_to(target.name)
    no(f.seed.refresh,'full_Seed_leaf_symlink_refused');path.unlink();path.rename(path) if False else None;write(path,b);target.unlink()
    # Full new Runtime authority parser, with genuine unchanged cloned Seed.
    a_ref=f.record('runtime_admission.json',f.a)
    # Admission has exact keys; record helper's fixture annotation intentionally
    # cannot be admitted, so write an exact-key synthetic object here instead.
    ap=Path(a_ref['path']);write(ap,enc(f.a));a_ref={'path':str(ap),**pin(enc(f.a))}
    review_obj={'schema':'pr211-root-concurrent-protocol-review-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':211,'accepted':True,'protocol_pin':f.seed.source_pin,'source_manifest_pin':f.seed.source_manifest_pin,'logical_manifest_pin':v.MP,'logical_gate_pin':v.GP,'cache_manifest_pin':v.CM,'cache_acceptance_pin':v.CA,'Root_full_source_read':True,'independent_adversarial_review_accepted':True,'all_original_verifications_retained':True,'parent_only_admissions_without_new_peer_review_approved':True}
    review=f.record('runtime_review.json',review_obj)
    gate_obj={'schema':'pr211-root-concurrent-admission-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':211,'accepted':True,'protocol_pin':f.seed.source_pin,'source_manifest_pin':f.seed.source_manifest_pin,'admission_pin':{k:a_ref[k]for k in ['bytes','sha256']},'logical_manifest_pin':v.MP,'logical_gate_pin':v.GP,'cache_manifest_pin':v.CM,'cache_acceptance_pin':v.CA,'facts':f.seed.logical['facts'],'parent_only_parameterization_reviewed':True,'one_use_two_immutable_POSTs_authorized':True,'supersedes_legacy_exactMain_bridge_for_this_admission':True,'no_ref_writer_authority':True,'prior04_and06_retired_no_redispatch':True,'protocol_review':review}
    gate=f.record('runtime_gate.json',gate_obj)
    rr=v.Runtime(f.seed,a_ref,gate);yes(rr.admission['candidate']==f.target,'full_Runtime_new_protocol_admission_chain_positive_fixture_only')
    for field,value in [('accepted',1),('one_use_two_immutable_POSTs_authorized',False),('protocol_pin',{'bytes':SOURCE['bytes'],'sha256':'0'*64}),('logical_gate_pin',{'bytes':6438,'sha256':'0'*64}),('facts',{**f.seed.logical['facts'],'fully_completed_count':53.0}),('protocol_review',None)]:
        gr=f.record('bad_gate_'+field+'.json',{**gate_obj,field:value})
        no(lambda gr=gr:v.Runtime(f.seed,a_ref,gr),'Runtime_typed_gate_'+field+'_refused')
    old=f.record('old_g6_not_new_gate.json',json.loads((f.native/v.GN).read_bytes()))
    no(lambda:v.Runtime(f.seed,a_ref,old),'Runtime_old_g6_cannot_authorize_new_helper')

def run():
    source=(S/'concurrent_checkpoint.py').read_bytes();need(pin(source)==SOURCE,'Root frozen source pin')
    sm=json.loads((S/'SOURCE_MANIFEST.json').read_bytes())
    for r in sm['files']:yes(pin((S/r['path']).read_bytes())=={k:r[k]for k in ['bytes','sha256']},'frozen_payload_'+r['path'])
    # Hard fail rather than accidentally dispatch any real service/process.
    socket.socket=deny;socket.create_connection=deny;subprocess.Popen=deny
    with tempfile.TemporaryDirectory(prefix='_synthetic_independent_',dir=D)as temp:
        f=Fixture(Path(temp)/'checkout',source);v,h,c,e,rt=f.v,f.h,f.c,f.e,f.rt
        cache_controls(f);source_runtime_controls(f);pipe_controls(v)
        # The fixture has a complete exact preimage parent; production immutable
        # proof independently authenticates all native tree paths and202 bodies.
        f.calls.clear();f.ref='f'*40
        proof=v.verify_immutable(rt,f.observer)
        yes(proof['selected_count']==192 and len(proof['changed_leaves'])==192 and len(proof['new_directories'])==25 and proof['deleted_directories']==[],'full_actual_immutable_192leaves25dirs202bodies')
        yes('git/ref/heads/main' not in f.calls and proof['mutable_Main_observed_or_spoofed'] is False,'immutable_with_unrelated_Main_does_not_read_or_spoof_ref')
        yes(all(not(p.startswith('git/blobs/')and p.rsplit('/',1)[1]in f.seed.bodies)for p in f.calls),'actual_cache_reuse_no_synthetic_body_GET')
        tree=c.NativeTrees(f.observer)
        yes(all(tree.lookup(f.target_tree,p)==entry for p,entry in f.foreign.items()),'foreign_executable_symlink_gitlink_emptytree_tuples_preserved')
        for field,value in [('commit_message',f.a['commit_message']+'changed'),('PR',True),('facts',{**f.a['facts'],'completed':1}),('parents',[f.parent,f.parent]),('created_UTC','2026-10-17T21:00:02Z'),('candidate_journal','ROOT_CANDIDATE_ADOPTION100_06'),('candidate','0'*40),('tree','0'*40)]:
            bad=copy.deepcopy(f.a);bad[field]=value;no(lambda bad=bad:v.checked_admission(f.seed,bad),'typed_admission_'+field+'_refused')
        for retired in v.RETIRED:
            bad={**f.a,'candidate':retired};no(lambda bad=bad:v.checked_admission(f.seed,bad),'admission_retired_'+retired+'_refused')
        for role in ['commit_author','commit_committer']:
            bad=copy.deepcopy(f.a);bad[role]['name']='Other';no(lambda bad=bad:v.checked_admission(f.seed,bad),'admission_'+role+'_identity_refused')
        for key,value in [('parents',[{'sha':h.ANCHOR}]),('tree',{'sha':f.parent_tree}),('author',{**f.request['author'],'email':'wrong@example.invalid'}),('committer',{**f.request['committer'],'date':'2026-10-17T21:00:00Z'}),('message',f.request['message']+'\n')]:
            saved=f.commits[f.target][key];f.commits[f.target][key]=value
            no(lambda:v.verify_immutable(rt,f.observer),'immutable_noncanonical_'+key+'_refused');f.commits[f.target][key]=saved
        f.commits[f.target]['message']=f.request['message'][:-1]
        yes(v.verify_immutable(rt,f.observer)['commit_message_readback']['terminal_LFs_omitted']==1,'only_exact_one_terminalLF_representation_accepted')
        f.commits[f.target]['message']=f.request['message']
        # Complete scope attacks use internally authenticated different trees,
        # not malformed SHA response envelopes alone.
        extras={**f.after,'foreign/extra':('100644','blob',f.blob(b'unselected effect'))}
        for label,leaves in [('extra_leaf',extras),('foreign_mode',{**f.after,'foreign/run':('100644','blob',f.foreign['foreign/run'][2])}),('foreign_delete',{p:t for p,t in f.after.items()if p!='foreign/link'})]:
            root=f.build(leaves);bad=copy.deepcopy(f.a);bad['tree']=root
            mm={**rt.m,'commit_author':bad['commit_author'],'commit_committer':bad['commit_committer']};req,bad['candidate']=h.commit_request(mm,root,[f.parent])
            f.commits[bad['candidate']]={'sha':bad['candidate'],'tree':{'sha':root},'parents':[{'sha':f.parent}],**{k:req[k]for k in ['author','committer','message']}}
            olda,oldm=rt.admission,rt.m;rt.admission=bad;rt.m=v.checked_admission(f.seed,bad)
            no(lambda:v.verify_immutable(rt,f.observer),'authenticated_full_scope_'+label+'_refused');rt.admission,rt.m=olda,oldm
        # All32 resumable combinations and80 distinct single-third-state cases.
        for bits in itertools.product([False,True],repeat=5):
            f.reset_locals(bits);v.local_states(rt,resume=True)
            yes(True,'local_mixed_prepost_'+''.join(map(lambda b:'1'if b else'0',bits)))
        for slot in range(5):
            other=[i for i in range(5)if i!=slot]
            for bits in itertools.product([False,True],repeat=4):
                mask=[False]*5
                for i,b in zip(other,bits):mask[i]=b
                f.reset_locals(mask);write(f.root/rt.m['local_views'][slot]['path'],b'independent third state')
                no(lambda:v.local_states(rt,resume=True),'local_third_'+str(slot)+'_'+''.join('1'if b else'0'for b in bits))
        f.reset_locals([False]*5)
        no(lambda:v.local_states(rt,all_post=True),'mixed_or_pre_is_not_allpost_terminal')
        for slot in range(5):
            p=f.root/rt.m['local_views'][slot]['path'];raw=p.read_bytes();back=p.with_name('fixture_backing_'+str(slot));write(back,raw);p.unlink();p.symlink_to(back.name)
            no(lambda:v.local_states(rt,resume=True),'local_leaf_symlink_'+str(slot)+'_refused');p.unlink();write(p,raw);back.unlink()
        # Native ancestry is computed from fixture graph, never blindly 'ahead'.
        foreign_root=f.build({**f.after,'other_chat/new':('100644','blob',f.blob(b'independent writer'))})
        child=f.commit(foreign_root,[f.target]);f.ref=child;observation=v.main_closure(rt,f.observer)
        yes(observation['actual_MAIN_observed']==child and observation['actual_MAIN_tree']==foreign_root and observation['CAS_target']==f.target and foreign_root!=f.target_tree,'preserving_foreign_descendant_distinct_C_R_roots')
        sibling=f.commit(f.target_tree,[f.parent],message='Owned-exact sibling\n');f.ref=sibling
        no(lambda:v.main_closure(rt,f.observer),'owned_exact_sibling_without_C_ancestry_refused')
        merge=f.commit(foreign_root,[f.parent,f.target],message='Preserving merge\n');f.ref=merge;v.main_closure(rt,f.observer);yes(True,'preserving_merge_actual_C_ancestry_accepted')
        for i,path in enumerate(rt.overlay):
            badroot=f.build({**f.after,path:('100755','blob',h.native('blob',rt.overlay[path]))})
            bad=f.commit(badroot,[f.target],date='2026-10-17T21:02:00Z',message='Owned mode attack '+str(i)+'\n');f.ref=bad
            no(lambda:v.main_closure(rt,f.observer),'hostile_descendant_owned_tuple_'+str(i))
        for label,path,entry in [('QUEUE',h.QUEUE,('100644','blob',f.blob(b'changed QUEUE'))),('own44',h.ATTEMPT[:-1],('040000','tree',f.tree({}))),('shared',h.SHARED,('040000','tree',f.tree({})))]:
            bad=f.commit(f.build({**f.after,path:entry}),[f.target],message='Protected attack '+label+'\n');f.ref=bad
            no(lambda:v.main_closure(rt,f.observer),'hostile_descendant_'+label+'_refused')
        f.ref=child;f.ref_reads=0
        f.ref_hook=lambda n:{'object':{'sha':child if n==1 else sibling}}
        no(lambda:v.main_closure(rt,f.observer),'coherent_ref_moves_to_sibling_during_read_refused');f.ref_hook=None
        saved=f.pr['merged'];f.pr['merged']=False;no(lambda:v.main_closure(rt,f.observer),'live_PR_identity_change_refused');f.pr['merged']=saved
        # Candidate driver executes both actual API/intent sites with only fake
        # bounded transport; canonical ledger remains durable in the fixture.
        f.ref=f.parent;f.posts=[];f.reset_locals([False]*5)
        cand=v.candidate(rt)
        yes(len(f.posts)==2 and [p for p,b in f.posts]==['git/trees','git/commits'] and cand['candidate']==f.target,'actual_candidate_driver_two_fake_POSTs_exact_intents_and_guards')
        ledger=f.src/'_private_candidate_oid_ledger'/ (f.target+'.json')
        yes(ledger.is_file()and json.loads(ledger.read_bytes())['candidate']==f.target,'durable_canonical_candidate_OID_reservation')
        before=len(f.posts);rt.admission={**f.a,'candidate_journal':'ROOT_CONCURRENT_CANDIDATE_NEW_ADMISSION'};rt.admission_pin=pin(b'fresh admission same canonical candidate')
        no(lambda:v.candidate(rt),'same_candidate_fresh_admission_and_journal_zero_redispatch');yes(len(f.posts)==before,'same_candidate_redispach_count_stays_zero')
        rt.admission=f.a;rt.admission_pin=pin(enc(f.a))
        for retired in v.RETIRED:
            rt.admission={**f.a,'candidate':retired};no(lambda:v.reserve_candidate_oid(rt),'permanent_retired_oid_reservation_'+retired)
        rt.admission=f.a
        # Fresh canonical candidate/date, same fixture parent: uncertainty creates
        # a permanent reservation and cannot be replayed under a new admission.
        oldtarget,oldrequest,olda=f.target,f.request,copy.deepcopy(f.a)
        fresh=copy.deepcopy(f.a);fresh['created_UTC']='2026-10-17T21:00:03Z'
        for k in ['commit_author','commit_committer']:fresh[k]['date']=fresh['created_UTC']
        fresh['candidate_journal']='ROOT_CONCURRENT_CANDIDATE_UNCERTAIN'
        mm={**rt.m,'commit_author':fresh['commit_author'],'commit_committer':fresh['commit_committer']}
        f.request,f.target=h.commit_request(mm,fresh['tree'],[f.parent]);fresh['candidate']=f.target
        rt.admission=fresh;rt.admission_pin=pin(enc(fresh));rt.m=v.checked_admission(f.seed,fresh);rt.m['writer_lock']=f.fixture_lock
        f.post_fail='git/trees';n=len(f.posts);no(lambda:v.candidate(rt),'uncertain_tree_POST_stops_after_one_fake_dispatch')
        yes(len(f.posts)==n+1,'uncertain_transport_no_following_commit_dispatch')
        rt.admission={**fresh,'candidate_journal':'ROOT_CONCURRENT_CANDIDATE_UNCERTAIN_RENAMED'};rt.admission_pin=pin(b'new root admission after uncertainty')
        no(lambda:v.candidate(rt),'uncertain_candidate_fresh_admission_journal_cannot_redispatch');yes(len(f.posts)==n+1,'uncertain_candidate_dispatch_count_unchanged')
        f.target,f.request,f.a=oldtarget,oldrequest,olda;rt.admission=f.a;rt.admission_pin=pin(enc(f.a));rt.m=v.checked_admission(f.seed,f.a);rt.m['writer_lock']=f.fixture_lock;f.post_fail=None
        # Stable-inode/lock/PID/mode checks are exercised on only this clone.
        f.ref=f.parent
        with e.WriterLock(f.fixture_lock)as lock:
            v.lease_guard(rt,f.observer,lock);yes(True,'full_original_lock_algorithm_and_fresh_lease_fixture_positive')
            f.ref=child;no(lambda:v.lease_guard(rt,f.observer,lock),'preCAS_stale_parent_refused_even_preserving_descendant');f.ref=f.parent
            pid=lock.pid;lock.pid=-1;no(lock.check,'fixture_wrong_lock_PID_refused');lock.pid=pid
        original_inode=f.fixture_lock['inode'];replacement=f.lockpath.with_name('other_lock');write(replacement,e.LOCK_BYTES);os.replace(replacement,f.lockpath)
        no(lambda:e.WriterLock(f.fixture_lock).__enter__(),'same_payload_replaced_original_fixture_lock_inode_refused')
        f.fixture_lock['inode']=f.lockpath.stat().st_ino;rt.m['writer_lock']=f.fixture_lock
        # Actual CAS parser never infers from C or descendant alone.
        f.ref=child;no(lambda:v.actual_cas(rt,None,f.observer),'descendant_without_actual_Root_CAS_record_refused')
        cas=f.cas_records(proof);v.actual_cas(rt,cas,f.observer);yes(True,'full_actual_CAS_provenance_parser_positive_synthetic_only')
        for field,value in [('unknown_outcome',True),('actual_Root_MCP_CAS_performed',False),('original_lock_held_across_actual_Root_CAS',False),('accepted',1),('hostname','evil.invalid'),('actual_MAIN_after_CAS',sibling),('post_CAS_same_live_guard_confirmation',None)]:
            bad=f.record('bad_cas_'+field+'.json',{**f.cas_obj,field:value});no(lambda bad=bad:v.actual_cas(rt,bad,f.observer),'actual_CAS_'+field+'_refused')
        for field,value in [('force',True),('expected_sha',child),('sha',child),('ref','heads/other'),('tool','ordinary_ref_update')]:
            req=f.record('bad_request_'+field+'.json',{**f.req_obj,field:value});bad=f.record('bad_request_cas_'+field+'.json',{**f.cas_obj,'actual_tool_request':req})
            no(lambda bad=bad:v.actual_cas(rt,bad,f.observer),'actual_CAS_request_'+field+'_refused')
        for field,value in [('session_id',True),('session_id',0),('exit_code',0),('output',None)]:
            poll=f.record('bad_poll_'+field+str(value)+'.json',{**f.poll_obj,field:value});conf=f.record('bad_confirmation_'+field+str(value)+'.json',{**f.conf_obj,'actual_same_session_poll_response':poll});bad=f.record('bad_poll_cas_'+field+str(value)+'.json',{**f.cas_obj,'post_CAS_same_live_guard_confirmation':conf})
            no(lambda bad=bad:v.actual_cas(rt,bad,f.observer),'same_live_poll_'+field+str(value)+'_refused')
        conf=f.record('wrong_pid_confirmation.json',{**f.conf_obj,'guard_pid':12346});bad=f.record('wrong_pid_cas.json',{**f.cas_obj,'post_CAS_same_live_guard_confirmation':conf});no(lambda:v.actual_cas(rt,bad,f.observer),'same_live_confirmation_wrong_PID_refused')
        # All-source wrapper Runtime authority is tested separately above. These
        # sync tests inject explicit guard failures via supplied Runtime.refresh
        # callbacks and retain the actual unchanged install/pointer algorithm.
        pointer=f.native/'ROOT_ACTUAL_CONCURRENT_ADOPTION100_POINTER.json'
        f.reset_locals([False]*5);f.ref=child
        original_put=e.put;injected=[False]
        def partial_put(directory,name,value):
            original_put(directory,name,value)
            if name=='VIEW_0.json'and not injected[0]:
                injected[0]=True;f.refresh_hook=lambda:(_ for _ in()).throw(RuntimeError('Changed pinned authority before next effect'))
        e.put=partial_put;j=e.journal_new('ROOT_CONCURRENT_SYNC_INDEPENDENT_INTERRUPTED')
        no(lambda:v.sync(rt,f.observer,j,cas),'source_guard_failure_after_first_view_stops_next_effect')
        yes(not pointer.exists()and not(j/'ACTUAL_FIVE_SYNC.json').exists(),'partial_sync_no_pointer_or_allfive_receipt')
        posts=[e.local_pin(h,f.root/r['path'])==pin(rt.overlay[r['path']])for r in rt.m['local_views']]
        yes(posts==[True,False,False,False,False],'partial_sync_one_exactpost_four_exactpre')
        e.put=original_put;f.refresh_hook=None
        # Existing first exactpost must not be rewritten during resume.
        p0=f.root/rt.m['local_views'][0]['path'];inode=p0.stat().st_ino
        j=e.journal_new('ROOT_CONCURRENT_SYNC_INDEPENDENT_RESUMED');receipt=v.sync(rt,f.observer,j,cas)
        yes(p0.stat().st_ino==inode,'mixed_sync_resume_skips_exactpost_without_rewrite')
        yes(receipt['all_five_local_postimages_verified'] and receipt['actual_MAIN_observed']==child and receipt['CAS_target']==f.target,'actual_sync_allfive_and_distinct_actual_descendant')
        yes(not receipt['external_Root_terminal_acceptance_inferred']and not receipt['perpetual_or_write_time_Main_equality_claimed'],'actual_sync_does_not_promote_external_terminal_or_perpetual_lease')
        v.checked_pointer(rt,cas);v.local_states(rt,all_post=True);yes(pointer.exists(),'checked_pointer_only_after_allfive_actual_native_closure')
        # Refuse corrupt receipt pointer bindings and false terminal allposts.
        saved=pointer.read_bytes();p=json.loads(saved);p['CAS_target']='0'*40;write(pointer,enc(p));no(lambda:v.checked_pointer(rt,cas),'pointer_wrong_CAS_candidate_refused');write(pointer,saved)
        f.reset_locals([True,True,False,True,True]);no(lambda:v.local_states(rt,all_post=True),'terminal_mixed_exact_prepost_refused')
        f.reset_locals([True]*5);f.ref=sibling;no(lambda:v.main_closure(rt,f.observer),'terminal_allfive_local_without_native_ancestry_refused')
        # Pure static callgraph properties complement runtime injections.
        tree=ast.parse(source)
        calls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)]
        postsites=[n for n in calls if n.args and isinstance(n.args[0],ast.Constant)and n.args[0].value=='POST']
        yes(len(postsites)==2 and [n.args[1].value for n in postsites]==['git/trees','git/commits'],'whole_source_exact_two_immutable_POST_sites_no_ref_writer')
        main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
        yes(all(not(isinstance(n,ast.Call)and getattr(n.func,'attr','')in ['run','Popen','system'])for n in ast.walk(main)),'CLI_dispatch_has_no_hidden_process_effect')
    return {'schema':'pr211-independent-actual-concurrent-source-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','protocol_pin':SOURCE,'checks':RESULT,'check_count':len(RESULT),'production_source_modified':False,'production_CLI_or_network_Git_ref_provider_real_lock_currentfive_actions':False,'fixture_compile_source_unchanged':True,'fixture_executor_transport_replaced_with_explicit_fake':True,'fixture_Runtime_refresh_callbacks_used_for_effect_injections':True,'synthetic_Root_records_not_operational_authority':True,'environment_assumptions_not_proved_by_finite_controls':True}

if __name__=='__main__':
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Python -E -S -B -P required')
    result=run();print(json.dumps(result,sort_keys=True,indent=2))

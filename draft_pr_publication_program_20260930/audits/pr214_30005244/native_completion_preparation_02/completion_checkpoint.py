"""Inactive PR214 completion native checkpoint; no ref or PR writer.
All inputs, gates, admissions and actual receipts are separately Root-bound.
Adoption54/38 is conditional until separate actual Root terminal; no new publication.
"""
import argparse,datetime,hashlib,json,os,re,selectors,signal,stat,sys,time,types
from pathlib import Path
BASE=Path(__file__).absolute().parent
CASE=BASE.parent
NATIVE=BASE
PROGRAM=CASE.parents[1]
CHECKOUT=PROGRAM.parent
MODEL_PIN={'bytes': 38904, 'sha256': 'f9850c22381f7be5937cd01b9b01890faed56eb252f7ee300ae7ed0b3b1ffee4'}
PRIMITIVE_PIN={'bytes': 16405, 'sha256': 'f64ecc9301a2870526ee27582246a5b7c6c013e64a45881bc3f2df423ad71a13'}
RETIRED=set()
IMMUTABLE_SCOPE='IMMUTABLE_CANDIDATE_ONLY_NOT_MAIN_LEASE_CAS_OR_COMPLETION'

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


def need(ok,message):
    if type(ok) is not bool or not ok:raise RuntimeError(message)


def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def enc(obj):return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def ref(h,s,row):
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['path']) is str,'Exact file reference')
    path=Path(row['path']);need(path.is_absolute() and path.is_relative_to(CASE),'Case-owned canonical input required')
    raw,unused=s.read_regular(path)
    need(h.exact(pin(raw),h.bytepin({k:row[k] for k in ('bytes','sha256')})),'Referenced body differs')
    return h.decode(raw)


def load_module(name,path,wanted):
    raw,identity=read_regular(path)
    need(pin(raw)==wanted,'Pinned local source changed')
    out=types.ModuleType(name);out.__file__=str(path);exec(compile(raw,str(path),'exec'),out.__dict__);return out

class Seed:
    """Fresh PR214 source/logical authority, never implicit operational permission."""
    def __init__(self,manifest_ref,logical_gate_ref):
        self.s=types.SimpleNamespace(read_regular=read_regular)
        self.h=load_module('pr214_conditional_model',BASE/'native214_model.py',MODEL_PIN)
        self.e=load_module('pr214_owned_primitives',BASE/'native214_primitives.py',PRIMITIVE_PIN)
        self.c=self.h.core()
        self.source,self.source_identity=read_regular(Path(__file__).absolute())
        self.source_pin=pin(self.source)
        self.manifest_ref,self.logical_gate_ref=manifest_ref,logical_gate_ref
        self.manifest_pin={k:manifest_ref[k] for k in ('bytes','sha256')}
        self.logical_gate_pin={k:logical_gate_ref[k] for k in ('bytes','sha256')}
        self.manifest_raw,unused=read_regular(BASE/'SOURCE_MANIFEST.json')
        self.source_manifest_pin=pin(self.manifest_raw)
        self.refresh()
    def refresh(self):
        h=self.h
        for name,wanted in (('native214_model.py',MODEL_PIN),('native214_primitives.py',PRIMITIVE_PIN)):
            need(pin(read_regular(BASE/name)[0])==wanted,'Frozen implementation changed')
        need(read_regular(Path(__file__).absolute())[0]==self.source
             and read_regular(BASE/'SOURCE_MANIFEST.json')[0]==self.manifest_raw,'Protocol/source manifest changed')
        sm=h.decode(self.manifest_raw)
        h.matches(sm,{'schema':'pr214-completion-source-manifest-v1','self_excluded':True,'source_only':True},'New source closure')
        rows=sm.get('files')
        need(type(rows) is list and 4<=len(rows)<=20 and all(type(r) is dict and set(r)=={'path','bytes','sha256'} for r in rows)
             and len({r['path'] for r in rows})==len(rows),'Finite positive implementation files')
        need({'path':'completion_checkpoint.py',**self.source_pin} in rows,'Own protocol absent')
        for row in rows:
            name=h.rel(row['path']);need(Path(name).name==name,'Source closure has no nested working paths')
            need(h.exact(pin(read_regular(BASE/name)[0]),h.bytepin({k:row[k] for k in ('bytes','sha256')})),'Listed source body changed')
        self.logical,self.overlay,self.pre=h.load_inputs(self.manifest_ref,self.logical_gate_ref,
            self.source_manifest_pin,self.source_pin,PRIMITIVE_PIN)
        return self

def checked_admission(seed,a):
    h=seed.h
    need(type(a) is dict and set(a)=={'schema','PR','evidence_scope','protocol_pin','source_manifest_pin',
        'logical_manifest_pin','logical_gate_pin','facts','body_proof_policy','QUEUE_policy','parent','parent_tree',
        'created_UTC','commit_author','commit_committer','commit_message','parents','tree','candidate','candidate_journal'},
        'Exact typed completion admission')
    h.matches(a,{'schema':'pr214-completion-parent-admission-v1','PR':214,
        'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':seed.source_pin,
        'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':seed.manifest_pin,
        'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,
        'QUEUE_policy':h.QUEUE_POLICY,'commit_message':seed.logical['commit_message']},'Admission fixed semantics')
    need(all(h.hexid(a[k]) for k in ('parent','parent_tree','tree','candidate'))
         and h.exact(a['parents'],[a['parent']]) and a['parent'] not in (h.ORIGINAL,h.CURRENT,h.MERGED) and a['candidate'] not in RETIRED
         and a['candidate'] not in seed.logical['retired_candidates'],'Only canonical one-parent archive; retired candidates forbidden')
    need(type(a['candidate_journal']) is str and len(a['candidate_journal'])<=80
         and re.fullmatch('ROOT_COMPLETE214_CANDIDATE_[A-Za-z0-9_-]{1,50}',a['candidate_journal']) is not None,'Fresh exact one-use candidate journal')
    for key in ('commit_author','commit_committer'):
        need(type(a[key]) is dict and set(a[key])=={'name','email','date'},'Fixed commit identity fields')
        for k in ('name','email'):need(h.exact(a[key][k],seed.logical[key][k]),'Identity substitution refused')
        need(h.exact(a[key]['date'],a['created_UTC']),'Single explicit UTC-seconds date')
    m={**seed.logical,'expected_parent':a['parent'],'expected_parent_tree':a['parent_tree'],
       'commit_author':a['commit_author'],'commit_committer':a['commit_committer'],'candidate_journal':a['candidate_journal']}
    request,oid=h.commit_request(m,a['tree'],[a['parent']])
    need(oid==a['candidate'],'Canonical candidate identity differs')
    return m

class Runtime:
    def __init__(self,seed,admission_ref,gate_ref):
        self.seed,self.e,self.h,self.c=seed,seed.e,seed.h,seed.c
        self.admission_ref,self.gate_ref=admission_ref,gate_ref
        self.pool=self.h.NativeBodyProofs()
        self.refresh()
    def refresh(self):
        self.seed.refresh();h=self.h
        self.admission=ref(h,self.seed.s,self.admission_ref)
        self.m=checked_admission(self.seed,self.admission)
        self.admission_pin={k:self.admission_ref[k] for k in ('bytes','sha256')}
        self.gate=ref(h,self.seed.s,self.gate_ref)
        self.gate_pin={k:self.gate_ref[k] for k in ('bytes','sha256')}
        h.matches(self.gate,{'schema':'pr214-root-completion-admission-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':214,'accepted':True,'protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,
            'admission_pin':self.admission_pin,'logical_manifest_pin':self.seed.manifest_pin,'logical_gate_pin':self.seed.logical_gate_pin,
            'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
            'parent_only_parameterization_reviewed':True,'one_use_two_immutable_POSTs_authorized':True,
            'no_ref_writer_or_PR_action_authority':True,'exact_baseline_plus214_memberships':True,
            'Root_full_source_read':True,'independent_source_review_accepted':True,
            'parent_only_admissions_without_new_peer_review_approved':True},'Separate exact Root completion admission acceptance')
        self.overlay,self.pre=self.seed.overlay,self.seed.pre
        return self

def protected(rt,trees,root,post):
    h=rt.h
    for path,expected in rt.m['protected_nodes'].items():
        need(trees.lookup(root,path)==h.preserved_tuple(expected,tree_only=True),'Fresh opaque attempt/audit state changed')
    for row in rt.m['protected_bodies']:
        need(trees.lookup(root,row['path'])==(row['mode'],row['type'],row['sha']),
             'Protected existing science native body association changed')
    for path,body in rt.overlay.items():
        expected=('100644','blob',h.native('blob',body)) if post else rt.pre[path]
        need(trees.lookup(root,path)==expected,'Selected native pre/postimage differs: '+path)

def parent_state(rt,observer):
    """Immutable fixed-parent truth, never a mutable Main observation."""
    h,c,m=rt.h,rt.c,rt.m;api=h.GetOnly(observer);parent=m['expected_parent'];root=m['expected_parent_tree']
    need(parent not in (h.ORIGINAL,h.CURRENT,h.MERGED),'A PR214 snapshot can never be the archival commit parent')
    value=api('GET','git/commits/'+parent)
    need(value.get('sha')==parent and value['tree']['sha']==root,'Admission parent/root differs')
    if parent!=h.ANCHOR:
        comp=api('GET','compare/'+h.ANCHOR+'...'+parent)
        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==h.ANCHOR,'Fresh Main must preserve actual212 administrative terminal ancestry')
    comp=api('GET','compare/'+h.MERGED+'...'+parent)
    need((parent==h.MERGED and comp.get('status')=='identical') or
         (comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==h.MERGED),
         'Fresh parent must preserve actual already-merged PR214 ancestry')
    h.pr_identity(observer,m,rt.pool)
    trees=c.NativeTrees(api);protected(rt,trees,root,False)
    queue=h.queue_observation(observer,trees,root,m,rt.pool,False)
    wanted,changed,dirs=h.expected(c,trees,root,rt.overlay,rt.pre)
    need(changed==set(m['expected_changed_paths']) and dirs==set(m['expected_new_directories']),'Full exact bound selected scope')
    need(rt.pre[h.VIEWS[2]] is not None,'Native progress baseline required')
    progress=h.decode(rt.pool.get(observer,rt.pre[h.VIEWS[2]][2]))
    h.matches(progress,h.baseline_facts(),'Intervening ascending checkpoint refused')
    for key,value in h.source_baseline().items():need(h.exact(progress.get(key),value),'Exact53/37 memberships changed')
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Dated99 baseline changed')
    for path in (h.VIEWS[1],h.VIEWS[4]):
        if rt.pre[path] is not None:need(rt.overlay[path].startswith(rt.pool.get(observer,rt.pre[path][2])),'Native log prefix changed')
    return wanted,changed,dirs

def body_associations(rt,observer,trees,root,allow_foreign_rows=False):
    h=rt.h;protected(rt,trees,root,True)
    queue=h.queue_observation(observer,trees,root,rt.m,rt.pool,allow_foreign_rows)
    for row in rt.m['protected_bodies']:
        rt.pool.get(observer,row['sha'],{k:row[k] for k in ('bytes','sha256')})
    selected={}
    for path,expected in rt.overlay.items():
        oid=h.native('blob',expected)
        body=rt.pool.get(observer,oid,pin(expected))
        need(body==expected,'Actual selected native bytes differ')
        selected[path]={**pin(body),'mode':'100644','type':'blob','git_blob':oid,
            'actual_native_GET_origin':rt.pool.origin(observer,oid)}
    return selected,queue

def verify_immutable(rt,observer):
    h,c,a=rt.h,rt.c,rt.admission;api=h.GetOnly(observer)
    wanted,expected_leaves,expected_dirs=parent_state(rt,observer)
    need(wanted==a['tree'],'Reconstructed archive tree differs')
    request,oid=h.commit_request(rt.m,wanted,[a['parent']])
    need(oid==a['candidate'] and oid not in RETIRED and oid not in rt.m['retired_candidates'],'Canonical candidate differs/retired')
    commit=api('GET','git/commits/'+oid)
    need(commit.get('sha')==oid and commit['tree']['sha']==wanted
         and [r['sha'] for r in commit['parents']]==[a['parent']],'Exact one-parent archive metadata')
    h.matches(commit.get('author'),rt.m['commit_author'],'Canonical author')
    h.matches(commit.get('committer'),rt.m['commit_committer'],'Canonical committer')
    message=h.commit_message_readback(rt.m['commit_message'],commit.get('message'))
    trees=c.NativeTrees(api);leaves,dirs,deleted=trees.changes(a['parent_tree'],wanted)
    need(leaves==expected_leaves and dirs==expected_dirs and not deleted,'Full native scope/foreign preservation differs')
    selected,queue=body_associations(rt,observer,trees,wanted)
    return {'schema':'pr214-completion-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
        'PR':214,'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
        'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,'admission_pin':rt.admission_pin,
        'parent':a['parent'],'parent_tree':a['parent_tree'],'candidate':oid,'tree':wanted,'parents':[a['parent']],
        'selected_files':selected,'selected_count':len(selected),'protected_body_paths_verified':len(rt.m['protected_bodies']),'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'deleted_directories':[],
        'Main_QUEUE_observation':queue,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
        'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,
        'deterministic_canonical_commit_oid_verified':True,'fixed_author_and_committer_metadata_verified':True,
        'commit_message_readback':message,'mutable_Main_observed_or_spoofed':False,
        'actual_CAS_or_completion_inferred':False,'this_action_native_POSTs':0,'earlier_attempt_effects_not_characterized':True}

def accepted_verifications(rt,row):
    root=ref(rt.h,rt.seed.s,row);h=rt.h
    h.matches(root,{'schema':'pr214-root-completion-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':214,'accepted':True,'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
        'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,'candidate':rt.admission['candidate'],
        'tree':rt.admission['tree'],'immutable_candidate_verification_accepted':True,
        'independent_GET_candidate_verification_accepted':True,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY},
        'Actual Root acceptance of independent full native proofs')
    reports=root.get('verification_reports')
    need(type(reports) is list and len(reports)==2 and len({r.get('path') for r in reports})==2,'Two distinct native GET proof records')
    for row in reports:
        proof=ref(h,rt.seed.s,row)
        h.matches(proof,{'schema':'pr214-completion-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
            'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,'admission_pin':rt.admission_pin,
            'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,
            'candidate':rt.admission['candidate'],'tree':rt.admission['tree'],'parent':rt.admission['parent'],
            'parent_tree':rt.admission['parent_tree'],'full_scope_verified':True,'all_selected_native_bodies_verified':True,
            'foreign_native_tuples_preserved':True,'selected_count':len(rt.overlay),'body_proof_policy':h.BODY_POLICY,
            'QUEUE_policy':h.QUEUE_POLICY,'mutable_Main_observed_or_spoofed':False,'actual_CAS_or_completion_inferred':False},
            'Exact complete immutable native proof differs')
    return root

def main_closure(rt,observer):
    h,c=rt.h,rt.c;api=h.GetOnly(observer)
    observed=api('GET','git/ref/heads/main')['object']['sha'];need(h.hexid(observed),'Fresh native R')
    commit=api('GET','git/commits/'+observed)
    need(commit.get('sha')==observed and h.hexid(commit['tree']['sha']),'Actual R/root differs')
    if observed!=rt.admission['candidate']:
        comp=api('GET','compare/'+rt.admission['candidate']+'...'+observed)
        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==rt.admission['candidate'],'R must equal or actually descend from C')
    root=commit['tree']['sha'];trees=c.NativeTrees(api)
    selected,queue=body_associations(rt,observer,trees,root,True)
    pr=h.pr_identity(observer,rt.m,rt.pool)
    need(api('GET','git/ref/heads/main')['object']['sha']==observed,'R changed during coherent owned-state proof; explicit readonly reconciliation needed')
    return {'actual_MAIN_observed':observed,'actual_MAIN_tree':root,'CAS_target':rt.admission['candidate'],
        'CAS_target_tree':rt.admission['tree'],'selected_postimage_paths_verified':len(selected),
        'protected_opaque_attempt_audit_verified':True,'Main_QUEUE_observation':queue,
        'fresh_merged_PR_status_observation':pr,'protected_body_paths_verified':len(rt.m['protected_bodies']),'native_final_ref_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'coherent_before_after_ref':True,'CAS_or_completion_inferred_from_ancestry':False,
        'perpetual_or_write_time_Main_equality_claimed':False}

def propose(seed,api,date,journal_name):
    h=seed.h;seed.refresh()
    parent=api('GET','git/ref/heads/main')['object']['sha'];need(h.hexid(parent),'Actual proposed parent')
    commit=api('GET','git/commits/'+parent);need(commit.get('sha')==parent and h.hexid(commit['tree']['sha']),'Actual proposed root')
    a={'schema':'pr214-completion-parent-admission-v1','PR':214,'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE',
       'protocol_pin':seed.source_pin,'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':seed.manifest_pin,
       'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
       'parent':parent,'parent_tree':commit['tree']['sha'],'parents':[parent],'created_UTC':date,
       'commit_author':{**seed.logical['commit_author'],'date':date},'commit_committer':{**seed.logical['commit_committer'],'date':date},
       'commit_message':seed.logical['commit_message'],'tree':'0'*40,'candidate':'0'*40,'candidate_journal':journal_name}
    q=types.SimpleNamespace(seed=seed,h=h,e=seed.e,c=seed.c,m={**seed.logical,'expected_parent':parent,
        'expected_parent_tree':commit['tree']['sha']},overlay=seed.overlay,pre=seed.pre,pool=h.NativeBodyProofs())
    with seed.e.WriterLock(seed.logical['writer_lock']) as lock:
        local_states(q);tree,unused,unused_dirs=parent_state(q,api);a['tree']=tree
        m={**q.m,'commit_author':a['commit_author'],'commit_committer':a['commit_committer']}
        unused,a['candidate']=h.commit_request(m,tree,[parent])
        checked_admission(seed,a);seed.refresh();local_states(q);lock.check()
        need(api('GET','git/ref/heads/main')['object']['sha']==parent,'Admission became stale; no silent rebind')
    return a

def local_states(rt,resume=False,all_post=False):
    for row in rt.m['local_views']:
        raw,identity=rt.seed.s.read_regular(CHECKOUT/row['path'],absent=True)
        now=pin(raw) if raw is not None else None;post=pin(rt.overlay[row['path']])
        need(rt.h.exact(now,post) if all_post else
             rt.h.exact(now,row['preimage']) or (resume and rt.h.exact(now,post)),
             'Local five third state refused: '+row['path'])


def lease_guard(rt,api,lock):
    lock.check();rt.refresh();local_states(rt)
    need(api('GET','git/ref/heads/main')['object']['sha']==rt.admission['parent'],'Stale admission before immutable effect/CAS')
    wanted,unused,unused_dirs=parent_state(rt,api)
    need(wanted==rt.admission['tree'],'Fresh native preimages/root differ')
    local_states(rt);rt.refresh();lock.check()
    need(api('GET','git/ref/heads/main')['object']['sha']==rt.admission['parent'],'Lease lost immediately before effect/CAS')
    lock.check()


def reserve_candidate_oid(rt):
    """Exclusive canonical-OID reservation survives admission/journal renaming."""
    oid=rt.admission['candidate']
    need(rt.h.hexid(oid) and oid not in RETIRED and oid not in rt.m['retired_candidates'],'Retired/invalid candidate cannot be reserved')
    ledger=BASE/'_private_candidate_oid_ledger'
    with rt.e.ParentHandle(ledger) as parent:
        parent.check()
        try:os.mkdir(ledger.name,0o700,dir_fd=parent.fd)
        except FileExistsError:pass
        parent.check();os.fsync(parent.fd)
    name=oid+'.json'
    with rt.e.ParentHandle(ledger/name) as parent:
        parent.check()
        fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
        try:
            raw=enc({'schema':'pr214-one-use-canonical-candidate-reservation-v1','candidate':oid,
                'admission_pin':rt.admission_pin,'protocol_pin':rt.seed.source_pin,
                'candidate_journal':rt.admission['candidate_journal'],
                'semantics':'Permanent attempt reservation before immutable POST. Never remove/reuse after failure or uncertainty.'})
            with os.fdopen(fd,'wb',closefd=False) as stream:
                need(stream.write(raw)==len(raw),'Short OID reservation write')
                stream.flush();os.fchmod(fd,0o444);os.fsync(fd)
        finally:os.close(fd)
        parent.check();os.fsync(parent.fd)


def candidate(rt):
    """Exactly two original audited API immutable POSTs; no resume/retry/ref writer."""
    e,h=rt.e,rt.h
    with e.WriterLock(rt.m['writer_lock']) as lock:
        rt.refresh()
        # Fixed journal from accepted admission prevents a fresh-journal retry of that admission.
        journal=e.journal_new(rt.admission['candidate_journal'])
        api=e.API(h,journal,mutate=True)
        lease_guard(rt,api,lock)
        reserve_candidate_oid(rt)
        entries=[{'path':path,'mode':'100644','type':'blob','content':body.decode('utf-8')}
                 for path,body in sorted(rt.overlay.items())]
        tree_request={'base_tree':rt.admission['parent_tree'],'tree':entries}
        commit_request,oid=h.commit_request(rt.m,rt.admission['tree'],[rt.admission['parent']])
        e.put(journal,'ONE_USE_ADMISSION_RESERVATION.json',{'admission_pin':rt.admission_pin,
            'protocol_pin':rt.seed.source_pin,'logical_manifest_pin':rt.seed.manifest_pin,'gate_pin':rt.gate_pin,
            'expected_tree':rt.admission['tree'],'expected_candidate':oid,
            'semantics':'One tree POST and one commit POST only. No redispatch after uncertainty or stale stop.'})
        lease_guard(rt,api,lock)
        api('POST','git/trees',tree_request,expected_oid=rt.admission['tree'])
        lease_guard(rt,api,lock)
        api('POST','git/commits',commit_request,expected_oid=oid)
        # New GET API instance, independent of construction API/cache. Main may now advance.
        reader=e.API(h,journal,mutate=False);reader.number=api.number
        rt.refresh();result=verify_immutable(rt,reader)
        rt.refresh();local_states(rt);lock.check()
        e.put(journal,'IMMUTABLE_CANDIDATE_VERIFIED.json',result)
        return {'candidate':oid,'tree':rt.admission['tree'],'journal':str(journal),
                'this_action_immutable_POST_dispatches':2,'actual_CAS_or_completion_inferred':False}


def actual_cas(rt,row,api):
    """Actual request/result/readback, never ancestry alone or a planned receipt."""
    h=rt.h;a=ref(h,rt.seed.s,row)
    h.matches(a,{'schema':'pr214-root-completion-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':214,'accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math',
        'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
        'admission_pin':rt.admission_pin,'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,
        'body_proof_policy':rt.h.BODY_POLICY,'QUEUE_policy':rt.h.QUEUE_POLICY,'facts':rt.m['facts'],
        'parent':rt.admission['parent'],'candidate':rt.admission['candidate'],'tree':rt.admission['tree'],
        'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
        'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False},
        'Separate actual external Root CAS acceptance required')
    accepted_verifications(rt,a.get('preCAS_acceptance'))
    ready=ref(h,rt.seed.s,a.get('actual_lock_guard_ready'))
    h.matches(ready,{'schema':'pr214-completion-locked-CAS-ready-v1',
        'evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS',
        'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
        'parent':rt.admission['parent'],'candidate':rt.admission['candidate'],
        'original_stable_lock_held':True},'Actual held-lock ready record required')
    request=ref(h,rt.seed.s,a.get('actual_tool_request'))
    h.matches(request,{'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
        'expected_sha':rt.admission['parent'],'sha':rt.admission['candidate'],'force':False},'True Root expectedSHA forcefalse request')
    result=ref(h,rt.seed.s,a.get('actual_tool_response'))
    h.matches(result,{'isError':False,'structuredContent':{'success':True}},'Actual successful MCP tool response required')
    response_row=a.get('actual_readback_response');response=ref(h,rt.seed.s,response_row)
    receipt=ref(h,rt.seed.s,a.get('actual_readback_receipt'))
    h.matches(receipt,{'method':'GET','path':'git/ref/heads/main','exit':0,
        'stdout_pin':{k:response_row[k] for k in ('bytes','sha256')}},'Actual native ref readback receipt differs')
    need(response.get('ref')=='refs/heads/main' and response['object'].get('type')=='commit'
         and h.hexid(response['object'].get('sha')),'Actual native Main readback required')
    # A ready file alone says nothing about process lifetime after Root's CAS.
    # Root separately confirms a same-session live poll after actual CAS/readback
    # and before acceptance/ack, binding its raw poll, PID and exact evidence.
    confirmation=ref(h,rt.seed.s,a.get('post_CAS_same_live_guard_confirmation'))
    h.matches(confirmation,{'schema':'pr214-root-postCAS-same-live-guard-confirmation-v1',
        'evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'protocol_pin':rt.seed.source_pin,
        'admission_pin':rt.admission_pin,
        'actual_lock_guard_ready_pin':{k:a['actual_lock_guard_ready'][k] for k in ('bytes','sha256')},
        'actual_tool_response_pin':{k:a['actual_tool_response'][k] for k in ('bytes','sha256')},
        'actual_readback_response_pin':{k:response_row[k] for k in ('bytes','sha256')},
        'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,
        'original_lock_continuity_from_linear_held_source_and_same_live_session':True},
        'Separate actual Root post-CAS same-live-session confirmation required')
    need(type(ready.get('guard_pid')) is int and ready['guard_pid']>0
         and h.exact(confirmation.get('guard_pid'),ready['guard_pid']),'Same live guard PID required')
    poll=ref(h,rt.seed.s,confirmation.get('actual_same_session_poll_response'))
    need(type(poll.get('session_id')) is int and poll['session_id']>0
         and h.exact(confirmation.get('session_id'),poll['session_id'])
         and poll.get('exit_code') is None and type(poll.get('output')) is str,
         'Actual still-running session poll response required; exited guard is not continuity')
    observed=response['object']['sha']
    need(h.exact(a.get('actual_MAIN_after_CAS'),observed),'Actual readback observation differs')
    if observed!=rt.admission['candidate']:
        comp=api('GET','compare/'+rt.admission['candidate']+'...'+observed)
        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==rt.admission['candidate'],
             'Actual readback must equal/descend from true CAS target')
    return a


def wait_actual_CAS_reference(fd,check,timeout=180):
    """Bounded one-line Root acknowledgment; reject immediately queued excess.

    Only this descriptor's nonblocking flag is changed and restored. The bound
    is an observation of already queued bytes, not a promise about future input.
    """
    need(type(timeout) in (int,float) and 0<timeout<=180,'Finite CAS hold deadline')
    selector=selectors.DefaultSelector();prior=os.get_blocking(fd)
    data=bytearray();deadline=time.monotonic()+timeout
    try:
        os.set_blocking(fd,False);selector.register(fd,selectors.EVENT_READ)
        while True:
            check()
            remaining=deadline-time.monotonic()
            need(remaining>0,'Root CAS hold timed out; reconcile actual outcome read-only')
            if not selector.select(min(1,remaining)):continue
            try:chunk=os.read(fd,4097-len(data))
            except BlockingIOError:continue
            need(bool(chunk),'Root CAS input closed before a complete reference; no success inferred')
            data.extend(chunk)
            need(len(data)<=4096 and time.monotonic()<deadline,'Root CAS input oversized/late; no success inferred')
            if b'\n' not in data:continue
            need(data.count(b'\n')==1 and data.endswith(b'\n'),'One exact Root CAS reference line required')
            try:extra=os.read(fd,1)
            except BlockingIOError:extra=b''
            need(extra==b'','Queued excess after Root CAS reference refused')
            check()
            return bytes(data[:-1])
    finally:
        selector.close();os.set_blocking(fd,prior)


def hold_CAS(rt,api,journal,preCAS_ref):
    """Keep the original lock held while external Root alone uses true MCP CAS."""
    accepted_verifications(rt,preCAS_ref)
    old_handlers={}
    def interrupted(signum,frame):raise RuntimeError('Root hold interrupted; no CAS outcome inferred')
    for signum in (signal.SIGINT,signal.SIGTERM):
        old_handlers[signum]=signal.signal(signum,interrupted)
    try:
        with rt.e.WriterLock(rt.m['writer_lock']) as lock:
            lease_guard(rt,api,lock)
            ready={'schema':'pr214-completion-locked-CAS-ready-v1',
                'evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS',
                'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'guard_pid':os.getpid(),
                'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
                'parent':rt.admission['parent'],'candidate':rt.admission['candidate'],
                'original_stable_lock_held':True,'actual_CAS_success_inferred':False}
            rt.e.put(journal,'LOCKED_CAS_READY.json',ready)
            print(json.dumps({'status':'READY_ORIGINAL_LOCK_HELD','ready_path':str(journal/'LOCKED_CAS_READY.json'),
                              'ready_pin':pin(enc(ready)),'expected_sha':rt.admission['parent'],
                              'sha':rt.admission['candidate'],'force':False}),flush=True)
            cas_ref=rt.h.decode(wait_actual_CAS_reference(sys.stdin.fileno(),lock.check))
            rt.refresh();local_states(rt,resume=True);lock.check()
            actual_cas(rt,cas_ref,api)
            observation=main_closure(rt,api)
            local_states(rt,resume=True);lock.check()
            rt.e.put(journal,'LOCKED_ACTUAL_CAS_READBACK.json',{'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
                **observation,'original_stable_lock_held':True,'terminal_acceptance_inferred':False})
            return observation
    finally:
        for signum,handler in old_handlers.items():signal.signal(signum,handler)


def sync(rt,api,journal,cas_ref):
    e,h=rt.e,rt.h;rt.refresh()
    actual=actual_cas(rt,cas_ref,api)
    verify_immutable(rt,api)
    pointer=NATIVE/'ROOT_ACTUAL_COMPLETION_POINTER.json'
    need(not pointer.exists() and not pointer.is_symlink(),'Actual pointer already exists')
    with e.WriterLock(rt.m['writer_lock']) as lock:
        def guard():
            lock.check();rt.refresh()
            now=actual_cas(rt,cas_ref,api)
            need(h.exact(now,actual),'Actual Root CAS envelope changed')
            local_states(rt,resume=True)
            observation=main_closure(rt,api)
            local_states(rt,resume=True);lock.check()
            need(api('GET','git/ref/heads/main')['object']['sha']==observation['actual_MAIN_observed'],
                 'Main moved after owned closure/local guard; no local effect permitted')
            observation['native_final_ref_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
            return observation
        guard()
        e.put(journal,'SYNC_INTENT.json',{'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
            'semantics':'Five per-file atomic installs under original lock; mixed exact pre/post resumable, never a five-file transaction.'})
        for index,row in enumerate(rt.m['local_views']):
            guard();path=CHECKOUT/row['path'];body=rt.overlay[row['path']];post=pin(body)
            if e.local_pin(h,path)!=post:
                with e.ParentHandle(path) as parent:
                    temp='.pr214-completion-'+journal.name+'-'+str(index)+'.tmp'
                    guard();parent.check()
                    fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
                    try:
                        with os.fdopen(fd,'wb',closefd=False) as stream:
                            need(stream.write(body)==len(body),'Short current-view temporary write')
                            stream.flush();os.fchmod(fd,0o444);os.fsync(fd)
                    finally:os.close(fd)
                    guard();parent.check()
                    need(h.exact(e.local_pin(h,path),row['preimage']),'Local preimage changed before atomic install')
                    if row['preimage'] is None:
                        os.link(temp,path.name,src_dir_fd=parent.fd,dst_dir_fd=parent.fd,follow_symlinks=False)
                        os.unlink(temp,dir_fd=parent.fd)
                    else:os.replace(temp,path.name,src_dir_fd=parent.fd,dst_dir_fd=parent.fd)
                    parent.check();os.fsync(parent.fd)
            need(h.exact(e.local_pin(h,path),post),'Installed current-view postimage differs')
            observation=guard()
            e.put(journal,'VIEW_'+str(index)+'.json',{'path':row['path'],'postimage':post,'native_observation':observation})
        local_states(rt,all_post=True);observation=guard();local_states(rt,all_post=True)
        receipt={'schema':'pr214-completion-actual-five-sync-v1','evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
            'PR':214,'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
            'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
            'CAS_target':rt.admission['candidate'],'CAS_target_tree':rt.admission['tree'],**observation,
            'all_five_local_postimages_verified':True,'facts':rt.m['facts'],'external_Root_terminal_acceptance_inferred':False}
        e.put(journal,'ACTUAL_FIVE_SYNC.json',receipt)
        observation=guard();local_states(rt,all_post=True)
        e.put(NATIVE,pointer.name,{'schema':'pr214-completion-actual-five-pointer-v1','evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
            'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
            'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},'sync_path':str(journal/'ACTUAL_FIVE_SYNC.json'),
            'sync_pin':pin(enc(receipt)),**observation,'all_five_local_postimages_verified':True,
            'recorded_under_original_stable_lock':True,'external_Root_terminal_acceptance_inferred':False})
        return receipt


def read_journal(e,name,prefix):
    need(type(name) is str and name.startswith(prefix) and len(name)<=80,'Exact new read/sync journal prefix')
    return e.journal_new(name)


def checked_pointer(rt,cas_ref):
    raw,unused=rt.seed.s.read_regular(NATIVE/'ROOT_ACTUAL_COMPLETION_POINTER.json')
    pointer=rt.h.decode(raw)
    rt.h.matches(pointer,{'schema':'pr214-completion-actual-five-pointer-v1',
        'evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE','protocol_pin':rt.seed.source_pin,
        'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
        'CAS_target':rt.admission['candidate'],'CAS_target_tree':rt.admission['tree'],
        'all_five_local_postimages_verified':True,'recorded_under_original_stable_lock':True,
        'external_Root_terminal_acceptance_inferred':False},'Exact actual-sync pointer required before terminal readout')
    path=Path(pointer['sync_path'])
    need(path.parent.parent==NATIVE and path.parent.name.startswith('ROOT_COMPLETE214_SYNC_')
         and path.name=='ACTUAL_FIVE_SYNC.json','Exact actual sync journal pointer')
    proof=ref(rt.h,rt.seed.s,{'path':str(path),**pointer['sync_pin']})
    rt.h.matches(proof,{'schema':'pr214-completion-actual-five-sync-v1',
        'evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
        'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
        'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},'CAS_target':rt.admission['candidate'],
        'CAS_target_tree':rt.admission['tree'],'all_five_local_postimages_verified':True,
        'facts':rt.m['facts'],'external_Root_terminal_acceptance_inferred':False},'Actual sync receipt association differs')
    return pin(raw)


def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
         and not sys.flags.optimize,'Use Python -E -S -B -P without optimization')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('admit','candidate','verify','preCAS','hold-CAS','postcheck','sync','terminal'))
    parser.add_argument('--manifest');parser.add_argument('--manifest-bytes',type=int);parser.add_argument('--manifest-sha256')
    parser.add_argument('--logical-gate');parser.add_argument('--logical-gate-bytes',type=int);parser.add_argument('--logical-gate-sha256')
    parser.add_argument('--admission');parser.add_argument('--admission-bytes',type=int);parser.add_argument('--admission-sha256')
    parser.add_argument('--Root-gate');parser.add_argument('--Root-gate-bytes',type=int);parser.add_argument('--Root-gate-sha256')
    parser.add_argument('--preCAS-acceptance');parser.add_argument('--preCAS-acceptance-bytes',type=int);parser.add_argument('--preCAS-acceptance-sha256')
    parser.add_argument('--actual-CAS');parser.add_argument('--actual-CAS-bytes',type=int);parser.add_argument('--actual-CAS-sha256')
    parser.add_argument('--journal');parser.add_argument('--commit-date');parser.add_argument('--candidate-journal')
    args=parser.parse_args()
    def supplied(prefix):
        name=prefix.replace('-','_')
        return {'path':getattr(args,name),'bytes':getattr(args,name+'_bytes'),'sha256':getattr(args,name+'_sha256')}
    seed=Seed(supplied('manifest'),supplied('logical-gate'));h,e=seed.h,seed.e
    if args.action=='admit':
        journal=read_journal(e,args.journal,'ROOT_COMPLETE214_READ_');api=e.API(h,journal,mutate=False)
        result=propose(seed,api,args.commit_date,args.candidate_journal)
        e.put(journal,'ADMISSION.json',result)
    else:
        rt=Runtime(seed,supplied('admission'),supplied('Root-gate'))
        if args.action=='candidate':
            need(args.journal is None,'Mutation journal only from accepted admission')
            result=candidate(rt)
        else:
            prefix='ROOT_COMPLETE214_SYNC_' if args.action=='sync' else 'ROOT_COMPLETE214_READ_'
            journal=read_journal(e,args.journal,prefix);api=e.API(h,journal,mutate=False)
            if args.action=='verify':
                rt.refresh();result=verify_immutable(rt,api);rt.refresh();e.put(journal,'VERIFIED.json',result)
            elif args.action=='preCAS':
                accepted_verifications(rt,supplied('preCAS-acceptance'))
                with e.WriterLock(rt.m['writer_lock']) as lock:lease_guard(rt,api,lock)
                result={'schema':'pr214-completion-preCAS-fresh-lease-observation-v1','parent':rt.admission['parent'],
                        'candidate':rt.admission['candidate'],'expected_sha':rt.admission['parent'],'force':False,
                        'ref_writer_exists':False,'observation_is_not_atomic_CAS_or_future_lease':True}
                e.put(journal,'PRECAS_FRESH_OBSERVATION.json',result)
            elif args.action=='hold-CAS':result=hold_CAS(rt,api,journal,supplied('preCAS-acceptance'))
            elif args.action=='sync':result=sync(rt,api,journal,supplied('actual-CAS'))
            else:
                rt.refresh();actual_cas(rt,supplied('actual-CAS'),api);verify_immutable(rt,api)
                with e.WriterLock(rt.m['writer_lock']) as lock:
                    local_states(rt,resume=True,all_post=args.action=='terminal')
                    if args.action=='terminal':checked_pointer(rt,supplied('actual-CAS'))
                    result=main_closure(rt,api);lock.check()
                    rt.refresh();actual_cas(rt,supplied('actual-CAS'),api)
                    local_states(rt,resume=True,all_post=args.action=='terminal')
                    need(api('GET','git/ref/heads/main')['object']['sha']==result['actual_MAIN_observed'],
                         'Main moved after dated reconciliation; no terminal/readout receipt')
                    result['native_final_ref_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
                    result['external_Root_terminal_acceptance_inferred']=False
                    e.put(journal,args.action.upper()+'.json',result)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()

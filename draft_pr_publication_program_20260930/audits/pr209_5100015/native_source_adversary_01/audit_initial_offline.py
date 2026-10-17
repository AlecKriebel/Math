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
    p=BASE/'source_freeze_initial'/name
    raw=p.read_bytes()
    manifest=json.loads((BASE/'INITIAL_SOURCE_FREEZE.json').read_bytes())
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
    def __call__(self,method,path,body=None):
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
    root=F/label;root.mkdir();checkout=root/'checkout';checkout.mkdir()
    x.CHECKOUT=checkout;x.PROGRAM=checkout/'draft_pr_publication_program_20260930';x.PROGRAM.mkdir();x.BASE=root
    h.BASE=root
    (x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock').write_bytes(x.LOCK_BYTES);(x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock').chmod(0o444)
    f=NativeFixture();parent='1'*40;original='2'*40;prepared='3'*40;candidate='4'*40
    oldrow=b'| 222 | 5100015 / AMR-050-0015 | Elliptic-billiard invariant k_{303,b} | 0.1905 | 5.0 | 3 | 2021 | queued | 0/5 |  |  |  |\n'
    q=json.loads((BASE/'QUEUE_ROWS.json').read_bytes());newrow=q['revised'].encode()
    overlay={h.QUEUE:newrow,h.ATTEMPT+'a.bin':b'\xff\0binary',**{p:(b'{"synthetic":true}\n' if p.endswith('.json') else b'new log\n') for p in h.VIEWS}}
    oldfiles={h.QUEUE:oldrow}
    pre={p:None for p in overlay};pre[h.QUEUE]=('100644','blob',f.blob(oldrow))
    # Main retains an explicit shared empty tree; overlay does not touch it.
    maintree=f.flat(oldfiles);shared=f.tree([])
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
    m={'expected_parent':parent,'expected_parent_tree':maintree,'phase':'merge95','facts':h.phase_facts('merge95'),'commit_message':'Synthetic audit commit','helper_pin':{'bytes':1,'sha256':'0'*64},'executor_pin':{'bytes':1,'sha256':'1'*64},'local_views':[]}
    for i,p in enumerate(h.VIEWS):
        path=checkout/p;path.parent.mkdir(parents=True,exist_ok=True)
        raw=None if i==0 else b'old local\n'
        if raw is not None:path.write_bytes(raw)
        m['local_views'].append({'path':p,'preimage':None if raw is None else h.pin(raw),'source':None})
    f.main=parent;f.wanted=wanted;f.candidate=candidate
    f.pr={'number':209,'head':{'sha':prepared},'base':{'ref':'main'},'draft':False,'state':'open','merged':False}
    f.commits={parent:{'sha':parent,'tree':{'sha':maintree},'parents':[]},original:{'sha':original,'tree':{'sha':maintree},'parents':[]},prepared:{'sha':prepared,'tree':{'sha':wanted},'parents':[{'sha':original},{'sha':'53b8291b2247008172f1fc3f596c96708faf8903'}]},candidate:{'sha':candidate,'tree':{'sha':wanted},'parents':[{'sha':parent},{'sha':prepared}],'message':m['commit_message']}}
    journal=root/'journal';journal.mkdir()
    return root,f,m,overlay,pre,lambda:(c,m,overlay,pre,{}),journal

root,f,m,overlay,pre,loader,j=setup('candidate_pr_drift')
def change_pr(path,body):
    if path=='git/blobs':f.pr['head']['sha']='f'*40
f.post_hook=change_pr
real_api=x.API;x.API=lambda *args,**kwargs:f
try:failed=rejected(lambda:x.candidate(h,loader,f,j))
finally:x.API=real_api
posts=[p for method,p,_ in f.calls if method=='POST']
check('candidate_live_PR_drift_gap',failed and posts==['git/blobs','git/trees','git/commits'],posts)

root,f,m,overlay,pre,loader,j=setup('candidate_local_drift')
def change_local(path,body):
    if path=='git/trees':(x.CHECKOUT/h.VIEWS[1]).write_bytes(b'changed after tree')
f.post_hook=change_local
# The real post-candidate verification needs the API wrapper; stop immediately after commit dispatch.
real_api=x.API;x.API=lambda *args,**kwargs:f
try:x.candidate(h,loader,f,j)
except Exception:pass
finally:x.API=real_api
posts=[p for method,p,_ in f.calls if method=='POST']
check('candidate_commit_local_preimage_gap',posts==['git/blobs','git/trees','git/commits'],posts)

root,f,m,overlay,pre,loader,j=setup('lock_identity')
lockpath=x.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock';first=lockpath.stat().st_ino
lockpath.chmod(0o644);lockpath.unlink();lockpath.write_bytes(x.LOCK_BYTES);lockpath.chmod(0o444)
# Occupy an extra file if the filesystem immediately reused the freed inode.
if lockpath.stat().st_ino==first:
    lockpath.chmod(0o644);lockpath.unlink();(x.PROGRAM/'occupied').write_bytes(b'x');lockpath.write_bytes(x.LOCK_BYTES);lockpath.chmod(0o444)
with x.WriterLock():accepted=True
check('replaced_same_payload_lock_accepted_gap',accepted and lockpath.stat().st_ino!=first,{'before_inode':first,'accepted_inode':lockpath.stat().st_ino})

# Path.read_bytes swap proves the local reader can follow a substituted symlink after its static checks.
p=F/'race_target';p.write_bytes(b'old');victim=F/'race_victim';victim.write_bytes(b'private synthetic sentinel')
original_read=Path.read_bytes;triggered=[]
def racing_read(self):
    if self==p:
        self.unlink();self.symlink_to(victim);triggered.append(True)
    return original_read(self)
Path.read_bytes=racing_read
try:got=x.local_pin(h,p)
finally:Path.read_bytes=original_read
check('local_read_symlink_swap_gap',triggered and got==h.pin(victim.read_bytes()))
check('static_local_symlink_refused',rejected(lambda:x.local_pin(h,p)))

# API journal is real and durable locally; transport is an in-memory stub only.
root,f,m,overlay,pre,loader,j=setup('uncertain_dispatch')
transports=[];real_run=x.subprocess.run
def unavailable(*args,**kwargs):transports.append(args);raise TimeoutError('synthetic lost response')
x.subprocess.run=unavailable
try:
    a=x.API(h,j,mutate=True)
    check('uncertain_POST_stops',rejected(lambda:a('POST','git/commits',{'tree':'a'*40,'parents':['b'*40],'message':'synthetic'})))
    check('same_API_no_retry',rejected(lambda:a('POST','git/commits',{'tree':'a'*40,'parents':['b'*40],'message':'synthetic'})) and len(transports)==1)
finally:x.subprocess.run=real_run
intent=json.loads((j/'00001.OBJECT_INTENT.json').read_bytes())
check('lost_commit_intent_no_reconcilable_object_gap','expected_sha' not in intent and 'request_body' not in intent and 'returned_sha' not in intent,intent)

# Test actual sync ordering with real verification and local installs, exclusively synthetic files.
root,f,m,overlay,pre,loader,j=setup('sync_gate_drift');f.main=f.candidate
wanted={'bytes':1,'sha256':'2'*64}
a={'schema':'pr209-root-native-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':209,'phase':m['phase'],'accepted':True,'manifest_pin':wanted,'helper_pin':m['helper_pin'],'executor_pin':m['executor_pin'],'core_pin':h.CORE_PIN,'facts':m['facts'],'parent':m['expected_parent'],'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,'candidate':f.candidate,'tree':f.wanted,'actual_MAIN_observed':f.candidate,'Root_ref_update':{'expected_sha':m['expected_parent'],'sha':f.candidate,'force':False,'success_confirmed_by_actual_native_readback':True}}
apath=root/'synthetic_actual_gate.json';raw=x.enc(a);apath.write_bytes(raw);apath.chmod(0o444);ap=h.pin(raw)
real_put=x.put;revoked=[]
def revoke_after_first(directory,name,value):
    real_put(directory,name,value)
    if name=='VIEW_0.json':
        apath.chmod(0o644);apath.write_bytes(b'{"revoked":true}\n');apath.chmod(0o444);revoked.append(True)
x.put=revoke_after_first
try:receipt=x.sync(h,loader,f,j,wanted,apath.name,ap)
finally:x.put=real_put
pointer=root/'ROOT_ACTUAL_MERGE95_POINTER.json'
check('sync_gate_not_refreshed_before_each_effect_gap',revoked and pointer.is_file() and all(x.local_pin(h,x.CHECKOUT/p)==h.pin(overlay[p]) for p in h.VIEWS))
check('sync_changed_gate_now_refused',rejected(lambda:x.actual_acceptance(h,m,wanted,apath.name,ap)))

out={'schema':'pr209-independent-source-offline-adversarial-results-v1','UTC':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'status':'CHANGES_REQUIRED','test_count':len(RESULTS),'results':RESULTS,'external_calls':0,'production_mutations':0,'scope':'Exact source freeze; synthetic loader/providers/files. Does not validate actual manifest/candidate/Root gates/science.'}
result_path=BASE/'INITIAL_OFFLINE_RESULTS.json'
if result_path.exists():
    descriptor,replay_name=tempfile.mkstemp(prefix='REPLAY_INITIAL_OFFLINE_RESULTS_',suffix='.json',dir=BASE)
    with os.fdopen(descriptor,'w') as replay:replay.write(json.dumps(out,sort_keys=True,indent=2)+'\n')
else:result_path.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
__import__('shutil').rmtree(F)
print(json.dumps({'status':out['status'],'tests':out['test_count']},sort_keys=True))

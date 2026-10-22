"""Independent exact-v02 OS/metadata/native-budget attacks; owned synthetic only."""
from pathlib import Path
import copy, hashlib, json, os, subprocess, sys, tempfile, types
HERE=Path(__file__).absolute().parent
SOURCE=HERE/'sealed_source/support206.py'
S=types.ModuleType('repair_support');S.__file__=str(SOURCE);exec(compile(SOURCE.read_bytes(),str(SOURCE),'exec'),S.__dict__)
ready=HERE/'sealed_source/ready206.py';R=types.ModuleType('repair_ready');R.__file__=str(ready);exec(compile(ready.read_bytes(),str(ready),'exec'),R.__dict__);R.configure(S)
OUT=[];RAW=[]
def test(name,fn,reject=False,predicate=None):
    try:
        value=fn();ok=not reject and (predicate is None or bool(predicate(value)));error=None;observed='accepted'
    except Exception as e:value=None;ok=reject;error=type(e).__name__+': '+str(e);observed='rejected'
    OUT.append({'case':name,'expected':'reject' if reject else 'accept','observed':observed,'pass':ok,'error':error})
    return value
class Patch:
    def __init__(self,**kw):self.kw=kw
    def __enter__(self):
        self.old={k:getattr(S,k) for k in self.kw}
        for k,v in self.kw.items():setattr(S,k,v)
    def __exit__(self,*a):
        for k,v in self.old.items():setattr(S,k,v)
PY=[sys.executable,'-E','-S','-B','-P']+(['-O'] if sys.flags.optimize else [])
with tempfile.TemporaryDirectory(prefix='repairs_owned_',dir=HERE) as temp:
    root=Path(temp);(root/'owned').mkdir();(root/'views').mkdir();(root/'program').mkdir()
    views=tuple('views/v'+str(i) for i in range(5));lock='program/LOCK'
    (root/lock).write_bytes(S.PROGRAM_VIEW_LOCK_BYTES);(root/lock).chmod(0o444)
    serial=[0]
    def generation():
        serial[0]+=1;g='owned/g'+str(serial[0])+'/';(root/g).mkdir();return g
    def reset():
        for p in views:
            q=root/p
            if q.is_symlink() or q.exists():q.unlink()
            q.write_bytes(b'OLD')
    def images():return [(p,S.pin(b'OLD'),b'POST') for p in views]
    with Patch(ROOT=root,OWN='owned/',VIEWS=views,PROGRAM_VIEW_LOCK=lock):
        g=generation();reset()
        test('view_write_without_ownership',lambda:S.atomic(views[0],b'POST',S.pin(b'OLD')),True)
        test('sync_without_ownership',lambda:S.sync_images(images(),g),True)
        with S.WriterOwnership(g):
            test('ownership_positive',S._writer_owned)
            test('view_write_without_full_five_session',lambda:S.atomic(views[0],b'POST',S.pin(b'OLD')),True)
            test('ownership_nonreentrant',lambda:S.WriterOwnership(g).__enter__(),True)
            original_pid=S._writer_lease['pid'];S._writer_lease['pid']=-1
            test('wrong_process_ownership',S._writer_owned,True);S._writer_lease['pid']=original_pid
            child="import os,fcntl,sys,json\nf=os.open(sys.argv[1],os.O_RDONLY)\ntry:\n fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);print(json.dumps({'acquired':True}))\nexcept BlockingIOError:\n print(json.dumps({'acquired':False}))\nfinally:os.close(f)"
            result=subprocess.run(PY+['-c',child,str(root/lock)],capture_output=True,text=True,timeout=5,check=True)
            test('real_child_lock_excluded',lambda:json.loads(result.stdout),predicate=lambda d:d['acquired'] is False)
            test('all_five_under_ownership',lambda:S.sync_images(images(),g),predicate=lambda v:len(v)==5 and all((root/p).read_bytes()==b'POST' for p in views))
        result=subprocess.run(PY+['-c',child,str(root/lock)],capture_output=True,text=True,timeout=5,check=True)
        test('real_child_lock_available_after_release',lambda:json.loads(result.stdout),predicate=lambda d:d['acquired'] is True)
        test('lease_cleared_after_release',lambda:S._writer_lease is None,predicate=bool)

        # Exact old failure window now targets the real os.link installation.
        g=generation();target=g+'COLLISION.json';original_link=os.link
        def competing_link(source,destination,**kw):
            Path(destination).write_bytes(b'COMPETITOR');return original_link(source,destination,**kw)
        with Patch(os=S.os):
            os.link=competing_link
            try:test('create_at_final_link_boundary',lambda:S.atomic(target,b'INCOMING',None),True)
            finally:os.link=original_link
        test('competing_receipt_preserved',lambda:(root/target).read_bytes()==b'COMPETITOR',predicate=bool)
        test('no_replace_conflict_latched',lambda:(root/g/'LOCAL_WRITE_CONFLICT.json').exists(),predicate=bool)
        evidence=[f.read_bytes() for f in (root/g).iterdir() if f.is_file()]
        test('incoming_and_competing_evidence_retained',lambda:b'INCOMING' in evidence and b'COMPETITOR' in evidence,predicate=bool)
        test('latched_generation_barred',lambda:S.atomic(g+'OTHER.json',b'OTHER',None),True)

        # Both real child processes stop immediately before their source's real
        # link; the parent releases them only after both reached that boundary.
        (root/'owned/shared').mkdir();gs=[generation(),generation()]
        child_code="""from pathlib import Path
import os,sys,json,types
p=Path(sys.argv[1]);s=types.ModuleType('child_support');s.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),s.__dict__)
s.ROOT=Path(sys.argv[2]);s.OWN='owned/'
original=os.link
def barrier(a,b,**kw):
 print('READY',flush=True);sys.stdin.readline();return original(a,b,**kw)
os.link=barrier
try:
 s.atomic('owned/shared/RECEIPT.json',sys.argv[4].encode(),None,sys.argv[3]);result={'won':True}
except Exception as error:result={'won':False,'error':type(error).__name__}
print(json.dumps(result),flush=True)
"""
        children=[subprocess.Popen(PY+['-c',child_code,str(SOURCE),str(root),gs[i],'WRITER'+str(i)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for i in range(2)]
        ready_lines=[p.stdout.readline().strip() for p in children]
        for child_process in children:child_process.stdin.write('GO\n');child_process.stdin.flush()
        child_results=[]
        for child_process in children:
            stdout,stderr=child_process.communicate(timeout=5)
            child_results.append({'returncode':child_process.returncode,'result':json.loads(stdout.strip()),'stderr':stderr})
        RAW.append({'case':'two_process_source_link_race','ready':ready_lines,'children':child_results,'final':(root/'owned/shared/RECEIPT.json').read_text()})
        test('two_real_source_writers_one_winner',lambda:ready_lines==['READY','READY'] and sum(x['result']['won'] for x in child_results)==1,predicate=bool)
        test('two_real_source_writers_preserve_winner',lambda:(root/'owned/shared/RECEIPT.json').read_bytes() in (b'WRITER0',b'WRITER1'),predicate=bool)

        # Identity replacement is detectable, permanently bars the generation,
        # and clears/closes its lease even when the context exit itself fails.
        g=generation();old_lock=root/'program/ORIGINAL_LOCK'
        def replace_lock():
            with S.WriterOwnership(g):
                (root/lock).rename(old_lock);(root/lock).write_bytes(S.PROGRAM_VIEW_LOCK_BYTES);(root/lock).chmod(0o444)
        test('lock_identity_replacement_rejected',replace_lock,True)
        test('lock_identity_conflict_latched',lambda:(root/g/'LOCAL_WRITE_CONFLICT.json').exists(),predicate=bool)
        test('lease_closed_after_identity_error',lambda:S._writer_lease is None,predicate=bool)
        (root/lock).unlink();old_lock.rename(root/lock)
        g=generation();reset();(root/views[-1]).write_bytes(b'CONFLICT')
        def bad_five():
            with S.WriterOwnership(g):return S.sync_images(images(),g)
        test('full_five_conflict_before_any_write',bad_five,True)
        test('full_five_conflict_no_earlier_write',lambda:all((root/p).read_bytes()==b'OLD' for p in views[:-1]),predicate=bool)
        test('full_five_conflict_latched',lambda:(root/g/'LOCAL_WRITE_CONFLICT.json').exists(),predicate=bool)
        (root/views[-1]).write_bytes(b'OLD')
        test('full_five_conflict_not_retried',bad_five,True)

        # Canonical pointer's own checks/install run under the real writer lease.
        # Native acceptance is injected only at that explicit pure unit boundary.
        data={'gate_pin':S.pin(b'SYNTHETIC'),'package':'publication_package_SYNTHETIC','package_seal':S.pin(b'SYNTHETIC'),'whole_package_reviews_completed':2}
        checkpoint='a'*40;main='b'*40
        def pointer_fixture(sync_complete=True,view_changed=False):
            g=generation();reset()
            for p in views:(root/p).write_bytes(b'POST');(root/p).chmod(0o444)
            if view_changed:(root/views[-1]).unlink();(root/views[-1]).write_bytes(b'CHANGED');(root/views[-1]).chmod(0o444)
            acceptance=b'SYNTHETIC ACCEPTANCE';(root/g/'ACCEPTANCE.json').write_bytes(acceptance);(root/g/'ACCEPTANCE.json').chmod(0o444)
            sy={'schema':'pr206-lifecycle-five-sync-v1','PR':206,'phase':'ready','actual_checkpoint':checkpoint,
                'acceptance_pin':S.pin(acceptance),'all_five_local_files_match_actual_checkpoint':sync_complete,
                'facts':R.facts(data,True),'files':[{'path':p,'postimage':S.pin(b'POST')} for p in views]}
            (root/g/'LOCAL_GLOBAL_FIVE_SYNC.json').write_bytes(S.enc(sy));(root/g/'LOCAL_GLOBAL_FIVE_SYNC.json').chmod(0o444)
            pointer='program/POINTER_'+g.split('/')[1]+'.json';owned_checks=[]
            def accepted(phase,name):
                S._writer_owned();owned_checks.append(True)
                return None,types.SimpleNamespace(api=lambda endpoint:{'object':{'sha':main}}),data,None,g,{'commit':checkpoint},{p:b'POST' for p in views},{'main_observed':main},main,{}
            with Patch(_fresh_accepted=accepted,POINTER={'ready':pointer}):
                result=S.pointer('ready',g.split('/')[1])
                return result,owned_checks,(root/pointer).exists()
        test('canonical_pointer_under_owned_full_checks',pointer_fixture,predicate=lambda v:v[1]==[True] and v[2] is True)
        test('canonical_pointer_incomplete_sync_rejected',lambda:pointer_fixture(False),True)
        test('canonical_pointer_changed_view_rejected',lambda:pointer_fixture(True,True),True)
        g=generation();pointer='program/COLLIDING_POINTER.json'
        with Patch(POINTER={'ready':pointer}):
            with S.WriterOwnership(g):
                os.link=competing_link
                try:test('canonical_pointer_atomic_collision',lambda:S.atomic(pointer,b'NEW POINTER',None,g),True)
                finally:os.link=original_link
        test('canonical_pointer_competitor_preserved',lambda:(root/pointer).read_bytes()==b'COMPETITOR',predicate=bool)

        # Deliberate noncooperating same-UID mutation reproduces the documented
        # excluded final window. This raw outcome is explicitly NOT a safety PASS.
        g=generation();reset();replace=os.replace;ignored_lock=[]
        def excluded_replace(source,destination):
            if not ignored_lock:
                Path(destination).write_bytes(b'IGNORED_LOCK_COMPETITOR');ignored_lock.append(str(destination))
            return replace(source,destination)
        try:
            os.replace=excluded_replace
            with S.WriterOwnership(g):limitation_result=S.sync_images(images(),g)
            limitation_error=None
        except Exception as error:limitation_result=None;limitation_error=type(error).__name__+': '+str(error)
        finally:os.replace=replace
        RAW.append({'case':'excluded_noncooperating_same_UID_final_window','classification':'KNOWN_LIMITATION_NON_PASS',
                    'considered_safety_PASS':False,'lock_deliberately_ignored':True,
                    'competing_content_lost':(root/views[0]).read_bytes()!=b'IGNORED_LOCK_COMPETITOR',
                    'sync_images_returned_success':limitation_result is not None,'exception':limitation_error})

        # Current original-metadata pin is real and fixed; substitute only local
        # bytes and live comparison data. Rejection must precede PR lookup.
        actual_pin={'bytes':18017,'sha256':'198a22a7e5b536d6b96f65597446e3b7d2d5e7648d2ad23390106dc49d48800a'}
        test('exact_original_metadata_constant',lambda:S.ORIGINAL_METADATA,predicate=lambda d:d==actual_pin)
        meta=root/S.CASE/'ORIGINAL_PR_METADATA.json';meta.parent.mkdir(parents=True)
        altered={'title':'UNACKNOWLEDGED TITLE','body':'UNACKNOWLEDGED BODY','updated_at':'2030-01-01'}
        meta.write_bytes(S.enc(altered));meta.chmod(0o444);calls=[]
        h=types.SimpleNamespace(api=lambda endpoint:calls.append(endpoint) or altered)
        test('metadata_substitution_matching_live_rejected',lambda:R.original(h,{}),True)
        test('metadata_rejected_before_live_PR_read',lambda:calls==[],predicate=bool)
        good={'head':{'sha':S.HEAD,'ref':'dot/math-5100062'},'base':{'ref':'main'},'state':'open','draft':True,'merged':False,
              'title':'SYNTHETIC ORIGINAL','body':'SYNTHETIC BODY','created_at':'old','updated_at':'old','commits':4,'changed_files':22}
        meta.unlink();meta.write_bytes(S.enc(good));meta.chmod(0o444)
        with Patch(ORIGINAL_METADATA=S.pin(S.enc(good))):
            h=types.SimpleNamespace(api=lambda endpoint:copy.deepcopy(good))
            test('synthetic_pinned_metadata_positive',lambda:R.original(h,{}))
            changed=copy.deepcopy(good);changed['title']='CHANGED';meta.unlink();meta.write_bytes(S.enc(changed));meta.chmod(0o444)
            h.api=lambda endpoint:copy.deepcopy(changed)
            test('synthetic_local_and_live_rebase_rejected',lambda:R.original(h,{}),True)

# Native DAG budgets/path/depth and pre-descent authentication, valid Git hashes.
def oid(rows):
    payload=[]
    for r in rows:payload.append((r['path'].encode()+(b'/' if r['type']=='tree' else b''),r['mode'].lstrip('0').encode()+b' '+r['path'].encode()+b'\0'+bytes.fromhex(r['sha'])))
    raw=b''.join(v for k,v in sorted(payload));return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
blob=S.bpin(b'SYNTHETIC')['git_blob']
class TreeH:
    def __init__(self,rows,objects=None):self.root=oid(rows);self.objects={self.root:rows,**(objects or {})};self.calls=[]
    def lookup(self,*args):return ('040000','tree',self.root)
    def api(self,endpoint):
        tree=endpoint.split('/')[-1];self.calls.append(tree)
        if len(self.calls)>100:raise RuntimeError('Independent fake request bound')
        return {'sha':tree,'truncated':False,'tree':copy.deepcopy(self.objects[tree])}
child_rows=[{'path':'leaf','mode':'100644','type':'blob','sha':blob}];child_oid=oid(child_rows)
parent_rows=[{'path':'sub','mode':'040000','type':'tree','sha':child_oid}]
h=TreeH(parent_rows,{child_oid:child_rows});h.objects[h.root][0]['path']='WRONG-HASH'
test('parent_SHA_verified_before_descent',lambda:S.native_leaves(h,'a'*40,S.NATIVE),True)
test('bad_parent_never_fetches_child',lambda:len(h.calls)==1,predicate=bool)
for label,name in (('name_256','x'*256),('path_oversize','x'*250)):
    rows=[{'path':name,'mode':'100644','type':'blob','sha':blob}];h=TreeH(rows)
    prefix=S.NATIVE if label=='name_256' else 'a'*900+'/'
    test('native_'+label,lambda h=h,prefix=prefix:S.native_leaves(h,'a'*40,prefix),True)
objects={};rows=child_rows
for i in range(66):
    ident=oid(rows);objects[ident]=rows;rows=[{'path':'d','mode':'040000','type':'tree','sha':ident}]
h=TreeH(rows,objects)
test('native_depth_65_rejected',lambda:S.native_leaves(h,'a'*40,S.NATIVE),True)
test('native_depth_GET_bound',lambda:len(h.calls)<=65,predicate=bool)
sub=[{'path':f'f{i}','mode':'100644','type':'blob','sha':blob} for i in range(5)];subid=oid(sub)
h=TreeH([{'path':f'd{i}','mode':'040000','type':'tree','sha':subid} for i in range(3)],{subid:sub})
with Patch(MAX_NATIVE_WORK=12):test('small_shared_DAG_work_before_insertion',lambda:S.native_leaves(h,'a'*40,S.NATIVE),True)
test('shared_subtree_fetched_once',lambda:len(h.calls)==2,predicate=bool)
test('writer_protocol_honest_same_UID_limit',lambda:S.writer_protocol()['uncooperative_same_UID_content_CAS_guaranteed'] is False,predicate=bool)
result={'schema':'pr206-independent-repair-attacks-v02','optimized':bool(sys.flags.optimize),
        'source_pins':{'support206.py':S.pin(SOURCE.read_bytes()),'ready206.py':S.pin(ready.read_bytes())},
        'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'only_owned_synthetic_fixtures':True,
        'tests':len(OUT),'passed':sum(x['pass'] for x in OUT),'failed':sum(not x['pass'] for x in OUT),'outcomes':OUT,'raw_process_outcomes':RAW}
print(json.dumps(result,indent=2))
raise SystemExit(bool(result['failed']))

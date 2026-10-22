"""Bounded owned-only v02 race and cooperating-writer regressions; no phase/backend."""
from pathlib import Path
import ast,copy,hashlib,json,os,stat,subprocess,sys,tempfile,types
D=Path(__file__).absolute().parent
raw=(D/'support206.py').read_bytes();S=types.ModuleType('race_support206');S.__file__=str(D/'support206.py');exec(compile(raw,S.__file__,'exec'),S.__dict__)
source={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def need(ok,message):
    if not ok:raise RuntimeError(message)
def worker():
    mode,folder,name,label=sys.argv[2:6];S.ROOT=Path(folder);g=S.generation(name)
    try:
        if mode=='create':
            link=os.link
            def at_link(src,dst,**kw):
                print('READY',flush=True);need(sys.stdin.buffer.read(1)==b'G','Owned race gate');return link(src,dst,**kw)
            os.link=at_link
            S.atomic(g+'competing_receipt.json',label.encode(),None)
        else:
            with S.WriterOwnership():
                if mode=='update':S.sync_images([(path,S.pin(S.read(path,readonly=False)),(label+str(i)).encode()) for i,path in enumerate(S.VIEWS)],g)
        print(json.dumps({'success':True,'mode':mode}),flush=True);return 0
    except Exception as exc:
        print(json.dumps({'success':False,'mode':mode,'error':type(exc).__name__+': '+str(exc)}),flush=True);return 3
if len(sys.argv)>1 and sys.argv[1]=='--worker':sys.exit(worker())

results=[]
def check(label,fn):fn();results.append({'name':label,'pass':True})
def same(a,b):need(a==b,'Expected equality')
def reject(label,fn):
    def run():
        try:fn()
        except (RuntimeError,OSError,ValueError):return
        raise RuntimeError('Expected rejection '+label)
    check(label,run)
def command(mode,folder,name,label):return [sys.executable,'-E','-S','-B','-P']+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).absolute()),'--worker',mode,str(folder),name,label]

realroot=S.ROOT
with tempfile.TemporaryDirectory(prefix='race_guards_owned_',dir=D) as folder:
    S.ROOT=Path(folder)
    for path in S.VIEWS:(S.ROOT/path).parent.mkdir(parents=True,exist_ok=True)
    lock=S.ROOT/S.PROGRAM_VIEW_LOCK;lock.write_bytes(S.PROGRAM_VIEW_LOCK_BYTES);lock.chmod(0o444)
    counter=[0]
    def generation():
        counter[0]+=1;name='race'+str(counter[0]);g=S.generation(name);(S.ROOT/g).mkdir(parents=True);return name,g
    def reset():
        for i,path in enumerate(S.VIEWS):
            p=S.ROOT/path
            if p.exists():p.chmod(0o644);p.unlink()
            p.write_bytes(('OLD'+str(i)).encode())
    def images():return [(path,S.pin(('OLD'+str(i)).encode()),('OURS'+str(i)).encode()) for i,path in enumerate(S.VIEWS)]
    def payloads(g):return [p.read_bytes() for p in (S.ROOT/g).glob('.pr206_staged_postimage_*')]

    # Exact receipt race occurs after optional() preimage comparison, at link().
    name,g=generation();target=S.ROOT/(g+'receipt.json');link=os.link
    def receipt_competitor(src,dst,**kw):
        Path(dst).write_bytes(b'COMPETING_RECEIPT');return link(src,dst,**kw)
    os.link=receipt_competitor
    try:reject('Post-check receipt competitor causes atomic EEXIST',lambda:S.atomic(g+'receipt.json',b'OUR_RECEIPT',None))
    finally:os.link=link
    check('Competing receipt bytes preserved unconditionally',lambda:same(target.read_bytes(),b'COMPETING_RECEIPT'))
    check('Failed receipt proposal retained independently',lambda:same(b'OUR_RECEIPT' in payloads(g),True))
    check('Receipt collision durably latches generation',lambda:same((S.ROOT/g/'LOCAL_WRITE_CONFLICT.json').is_file(),True))

    # Both real child processes pass the absent preimage check before either link.
    name,g=generation();children=[subprocess.Popen(command('create',folder,name,label),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE) for label in ('CHILD_A','CHILD_B')]
    for p in children:need(p.stdout.readline()==b'READY\n','Both children reached atomic link boundary')
    outcomes=[]
    for p in children:
        out,err=p.communicate(input=b'G',timeout=10);need(not err,'Unexpected child stderr');outcomes.append(json.loads(out))
    check('Two-process absent-target race has exactly one success',lambda:same(sorted(x['success'] for x in outcomes),[False,True]))
    winner=(S.ROOT/(g+'competing_receipt.json')).read_bytes()
    check('Two-process winner bytes preserved',lambda:same(winner in (b'CHILD_A',b'CHILD_B'),True))
    check('Both two-process proposed payloads retained',lambda:same(set(payloads(g)),{b'CHILD_A',b'CHILD_B'}))

    # Existing views require current-process ownership AND complete-five session.
    reset();name,g=generation()
    reject('Existing view atomic refuses absent program ownership',lambda:S.atomic(S.VIEWS[0],b'BAD',S.pin(b'OLD0'),g))
    reject('Whole-five sync refuses absent program ownership',lambda:S.sync_images(images(),g))
    check('Unowned view requests preserve all five',lambda:same([S.read(x,readonly=False) for x in S.VIEWS],[('OLD'+str(i)).encode() for i in range(5)]))
    with S.WriterOwnership():
        reject('Owned single-view atomic refuses absent full-five session',lambda:S.atomic(S.VIEWS[0],b'BAD',S.pin(b'OLD0'),g))
        child=subprocess.run(command('lock',folder,name,'BLOCKED'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
        need(child.returncode==3,'Contending child must fail nonblocking lock')
        check('Second process cannot acquire same stable lock inode',lambda:same(json.loads(child.stdout)['success'],False))
        # A fork inherits the FD but is not the recorded owning process.
        rd,wr=os.pipe();pid=os.fork()
        if pid==0:
            os.close(rd)
            try:S._writer_owned();result=b'BAD'
            except RuntimeError:result=b'REJECTED'
            os.write(wr,result);os.close(wr);os._exit(0)
        os.close(wr);forked=os.read(rd,100);os.close(rd);os.waitpid(pid,0)
        check('Inherited fork descriptor is not writer ownership',lambda:same(forked,b'REJECTED'))
        check('Lease protects complete-five update and readbacks',lambda:same(len(S.sync_images(images(),g)),5))
    check('All five successful cooperative postimages readonly',lambda:same(all(stat.S_IMODE((S.ROOT/x).lstat().st_mode)==0o444 for x in S.VIEWS),True))
    name2,g2=generation();child=subprocess.run(command('update',folder,name2,'NEXT'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
    check('Second process can update after ownership release',lambda:same((child.returncode,json.loads(child.stdout)['success']),(0,True)))
    check('Serialized next writer bytes retained',lambda:same([S.read(x) for x in S.VIEWS],[('NEXT'+str(i)).encode() for i in range(5)]))

    # Detectable same-UID mutation after capture is preserved and stops all writes.
    reset();name,g=generation();evidence=S._evidence;injected=[False]
    def changed_after_capture(directory,label,content):
        path=evidence(directory,label,content)
        if label=='view_preimage' and not injected[0]:
            injected[0]=True;(S.ROOT/S.VIEWS[0]).write_bytes(b'COMPETING_CAPTURED_VIEW')
        return path
    S._evidence=changed_after_capture
    try:
        with S.WriterOwnership():reject('Changed view after capture fails before first replacement',lambda:S.sync_images(images(),g))
    finally:S._evidence=evidence
    check('Detected competing view bytes preserved',lambda:same((S.ROOT/S.VIEWS[0]).read_bytes(),b'COMPETING_CAPTURED_VIEW'))
    check('Other four not replaced after full-set conflict',lambda:same([S.read(x,readonly=False) for x in S.VIEWS[1:]],[('OLD'+str(i)).encode() for i in range(1,5)]))
    check('Detected view conflict latches generation',lambda:same((S.ROOT/g/'LOCAL_WRITE_CONFLICT.json').exists(),True))
    with S.WriterOwnership():
        reject('Latched generation cannot sync later',lambda:S.sync_images(images(),g))
        reject('Latched generation cannot install pointer',lambda:S.atomic(S.POINTER['ready'],b'NO_SUCCESS_POINTER',None,g))
    check('No successful pointer after detected conflict',lambda:same((S.ROOT/S.POINTER['ready']).exists(),False))

    # Existing-view mutation detectable immediately after replace: preserve actual
    # competitor plus an independent copy of our attempted postimage/preimage.
    reset();name,g=generation();replace=os.replace;injected=[False]
    def changed_after_replace(src,dst):
        value=replace(src,dst)
        if not injected[0]:
            injected[0]=True;p=Path(dst);p.chmod(0o644);p.write_bytes(b'COMPETING_AFTER_REPLACE');p.chmod(0o444)
        return value
    os.replace=changed_after_replace
    try:
        with S.WriterOwnership():reject('Detected post-replace same-UID mutation fails readback',lambda:S.sync_images(images(),g))
    finally:os.replace=replace
    check('Detected post-replace competitor remains',lambda:same((S.ROOT/S.VIEWS[0]).read_bytes(),b'COMPETING_AFTER_REPLACE'))
    check('Failed postimage retained in independent inode',lambda:same(b'OURS0' in payloads(g),True))
    check('Failed preimage retained',lambda:same(b'OLD0' in [p.read_bytes() for p in (S.ROOT/g).glob('.pr206_view_preimage_*')],True))
    check('Observed conflicting bytes retained',lambda:same(b'COMPETING_AFTER_REPLACE' in [p.read_bytes() for p in (S.ROOT/g).glob('.pr206_observed_conflict_*')],True))

    # Disclose the precise excluded boundary rather than claim impossible CAS.
    # This writer intentionally ignores the lock and mutates after the final
    # preimage check but immediately before os.replace; the source cannot detect
    # this transient mutation. This is a LIMITATION PROBE, not a safety PASS.
    reset();name,g=generation();replace=os.replace;ignored_lock=[False]
    def uncooperative_final_window(src,dst):
        if not ignored_lock[0]:
            ignored_lock[0]=True;p=Path(dst);p.chmod(0o644);p.write_bytes(b'IGNORED_LOCK_TRANSIENT_VIEW')
        return replace(src,dst)
    os.replace=uncooperative_final_window
    try:
        with S.WriterOwnership():S.sync_images(images(),g)
    finally:os.replace=replace
    limitation_probe={'case':'same_UID_writer_ignores_program_lock_in_final_replace_window','inside_guaranteed_model':False,'transient_competing_bytes': 'IGNORED_LOCK_TRANSIENT_VIEW','final_bytes':(S.ROOT/S.VIEWS[0]).read_bytes().decode(),'competing_content_can_be_lost':(S.ROOT/S.VIEWS[0]).read_bytes()!=b'IGNORED_LOCK_TRANSIENT_VIEW','result':'Known excluded limitation, explicitly disclosed; not a successful safety test and not a filesystem-CAS claim.'}

    # Canonical pointer creation is no-replace even when lock is owned.
    reset();name,g=generation();ptr=S.ROOT/S.POINTER['ready'];link=os.link
    def pointer_competitor(src,dst,**kw):Path(dst).write_bytes(b'COMPETING_POINTER');return link(src,dst,**kw)
    os.link=pointer_competitor
    try:
        with S.WriterOwnership():reject('Canonical pointer collision cannot overwrite competitor',lambda:S.atomic(S.POINTER['ready'],b'OUR_POINTER',None,g))
    finally:os.link=link
    check('Competing pointer preserved unconditionally',lambda:same(ptr.read_bytes(),b'COMPETING_POINTER'))

    # Same-UID lock inode replacement is detected, not silently accepted.
    reset()
    def replaced_inode():
        with S.WriterOwnership():
            lock.unlink();lock.write_bytes(S.PROGRAM_VIEW_LOCK_BYTES);lock.chmod(0o444);S._writer_owned()
    reject('Lock path inode replacement rejected',replaced_inode)
    name,g=generation()
    def replaced_at_exit():
        with S.WriterOwnership(g):
            lock.unlink();lock.write_bytes(S.PROGRAM_VIEW_LOCK_BYTES);lock.chmod(0o444)
    reject('Lock identity conflict at ownership exit rejected',replaced_at_exit)
    check('Exit lock identity conflict durably bars phase generation',lambda:same((S.ROOT/g/'LOCAL_WRITE_CONFLICT.json').exists(),True))
    check('Failed lock identity check releases local lease state',lambda:same(S._writer_lease,None))
    check('Lock ownership failure writes no actual view',lambda:same([S.read(x,readonly=False) for x in S.VIEWS],[('OLD'+str(i)).encode() for i in range(5)]))
S.ROOT=realroot
functions={n.name:ast.unparse(n) for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)}
for name in ('sync','pointer'):
    check('Complete '+name+' body is under ownership',lambda name=name:same('with WriterOwnership(generation(name)):' in functions[name],True))
check('Stable lock path is program-level across source families',lambda:same(S.PROGRAM_VIEW_LOCK,S.P+'ROOT_GLOBAL_FIVE_WRITER.lock'))
check('Receipt install uses atomic no-replace link',lambda:same('os.link(installation, target, follow_symlinks=False)' in functions['atomic'],True))
check('No uncooperative same-UID CAS claim in adopted protocol',lambda:same(S.writer_protocol()['uncooperative_same_UID_content_CAS_guaranteed'],False))
print(json.dumps({'schema':'pr206-v02-owned-race-regressions-v1','optimized':bool(sys.flags.optimize),'source':source,'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'uncooperative_limit_probe':limitation_probe,'checks':len(results),'all_pass':all(x['pass'] for x in results),'results':results,'limits':['Every fixture and child process operates solely within a temporary child of new02; no phase/backend/API/global-five/service action.','Real two-process no-replace race and shared-lock exclusion are tested; forced detectable conflicts retain bytes/evidence and latch the generation.','Advisory flock serializes cooperating writers only; arbitrary same-UID writers ignoring it are outside the content-CAS guarantee. No five-file transaction is claimed.']},indent=2,sort_keys=True))

"""Publish a reviewed overlay using a private index; never change checkout refs/index.

Local installation is a separate forward-only step after authenticated publication.
Every action requires the exact plan and an independent source/plan PASS.
"""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, signal, stat, subprocess, sys, time, tempfile

R = Path('/Users/alec/Documents/Math')
C = R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A = C/'draft_pr_publication_program_20260930/audits/pr134_2306064'
D = A/'scoped_completion_transaction_20261007'
G = '/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
URL = 'https://github.com/AlecKriebel/Math.git'
AUDIT = 'draft_pr_publication_program_20260930/audits/pr134_2306064/'
NATIVE = {'unsolved_math_prioritization/'+s for s in ['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','QUEUE.md']}
ATTEMPT = {'unsolved_math_prioritization/attempts/2306064/'+s for s in ['DISPOSITION.json','HISTORICAL_DESK_ASSESSMENT.json','PRIORITY_EVIDENCE.json','README.md','RESEARCH_LOG.md','assessment.json']}
PROGRAM = {'draft_pr_publication_program_20260930/'+s for s in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}

def require(ok, message):
    if not ok: raise RuntimeError(message)

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(body): return hashlib.sha256(body).hexdigest()
def safe(path):
    path = Path(path)
    require(path.is_absolute(), 'absolute path required')
    for p in [path, *path.parents]:
        require(not p.is_symlink(), 'symlink: '+str(p))
    return path

def pin(path):
    path = safe(path); fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'regular single-link file required')
        h=hashlib.sha256()
        while b:=os.read(fd,1048576):h.update(b)
        after=os.fstat(fd); named=path.lstat()
        signature=lambda z:(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns,z.st_mode,z.st_nlink)
        require(signature(s)==signature(after)==signature(named),'file changed during pin read')
        return {'bytes':s.st_size,'mode':stat.S_IMODE(s.st_mode),'sha256':h.hexdigest()}
    finally:os.close(fd)

def check(path, expected):
    require(pin(path) == {k:expected[k] for k in ['bytes','mode','sha256']}, 'pin mismatch: '+str(path))

def dump(path, value):
    path = safe(path)
    with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,prefix=path.name+'.tmp.',delete=False) as f:
        tmp=Path(f.name)
        json.dump(value,f,indent=2,sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.chmod(tmp,420)
    os.replace(tmp,path)

def run(argv, journal, env=None, data=None, allowed=(0,)):
    e={'UTC_start':utc(),'argv':argv}; journal['children'].append(e)
    try:child = subprocess.Popen(argv,cwd=R,env=env,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    except BaseException:
        # A constructor exception may occur after fork. No PID custody was
        # obtained here: retain the operation barrier and report uncertainty.
        e.update(UTC_end=utc(),child_started=None,child_reaped=False,process_group_empty=False,constructor_outcome_unresolved=True)
        raise
    e['PID']=child.pid
    out=b'';err=b''; failure=None
    try:out,err=child.communicate(data,timeout=45)
    except BaseException as exc:
        failure=exc;e['timed_out']=isinstance(exc,subprocess.TimeoutExpired)
    finally:
        try:os.killpg(child.pid,0);empty=False
        except ProcessLookupError:empty=True
        except OSError as exc:empty=False;e['group_probe_error']=str(exc)
        if child.returncode is None or not empty:
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            except OSError as exc:e['group_kill_error']=str(exc)
            if child.returncode is None:
                try:out,err=child.communicate(timeout=5)
                except BaseException as exc:e['reap_error']=type(exc).__name__
        until=time.monotonic()+1
        while True:
            try:os.killpg(child.pid,0);empty=False
            except ProcessLookupError:empty=True
            except OSError as exc:empty=False;e['group_probe_error']=str(exc)
            if empty or time.monotonic()>=until:break
            time.sleep(.05)
        e.update(UTC_end=utc(),exit_code=child.returncode,child_reaped=child.returncode is not None,process_group_empty=empty,stdout_bytes=len(out),stdout_sha256=digest(out),stderr_bytes=len(err),stderr_sha256=digest(err))
    if failure is not None:raise failure
    require(empty and not e.get('timed_out') and child.returncode in allowed,'child failed; see journal: '+argv[0])
    return out

def git(args,journal,index=None,data=None,allowed=(0,)):
    env=os.environ.copy()
    for k in list(env):
        if k.startswith('GIT_'): del env[k]
    env['GIT_OPTIONAL_LOCKS']='0'
    env['GIT_NO_REPLACE_OBJECTS']='1'
    if index is not None: env['GIT_INDEX_FILE']=str(index)
    return run([G,'-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','core.splitIndex=false',*args],journal,env,data,allowed)

def remote(journal):
    v=run([GH,'api','repos/AlecKriebel/Math/git/ref/heads/main','--jq','.object.sha'],journal).decode().strip()
    require(len(v)==40 and all(x in '0123456789abcdef' for x in v),'invalid remote SHA')
    return v

def guard(plan,journal):
    for x in plan['protected']: check(x['path'],x)
    for x in plan['protected_absences']: require(not safe(x).exists(),'protected absence changed: '+x)
    for root,expected in [(R,plan['R_HEAD']),(C,plan['C_HEAD'])]:
        got=git(['-C',str(root),'rev-parse','HEAD','refs/heads/main'],journal).decode().splitlines()
        require(got==[expected,expected],'local main/HEAD changed')
    pr=json.loads(run([GH,'api','repos/AlecKriebel/Math/pulls/134'],journal))
    require(pr['state']=='closed' and pr['merged_at'] is None and pr['draft'] is True and pr['head']['sha']==plan['original_PR_head'],'PR134 disposition changed')
    comment=json.loads(run([GH,'api','repos/AlecKriebel/Math/issues/comments/6028564660'],journal))
    require(digest(comment['body'].encode())==plan['closing_comment_body_sha256'],'closing comment changed')

def load_inputs(plan_path,plan_sha,review_path,review_sha):
    require(digest(safe(plan_path).read_bytes())==plan_sha,'plan SHA')
    plan=json.loads(Path(plan_path).read_bytes())
    require(plan['schema']=='pr134-scoped-overlay/v1','plan schema')
    require(plan['source_sha256']==digest(Path(__file__).read_bytes()),'source SHA')
    require(digest(safe(review_path).read_bytes())==review_sha,'review SHA')
    review=json.loads(Path(review_path).read_bytes())
    require(review['verdict']=='PASS' and review['plan_sha256']==plan_sha and review['source_sha256']==plan['source_sha256'],'independent source/plan review')
    check(G,plan['git_executable']);check(GH,plan['gh_executable'])
    seen=set()
    for m in plan['members']:
        rel=m['path'];require(str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts,'invalid relative path')
        require(rel in NATIVE|ATTEMPT|PROGRAM or rel.startswith(AUDIT),'outside publication scope')
        require(rel.lower() not in seen,'case duplicate');seen.add(rel.lower())
        check(m['source'],m['post'])
        require(m['post']['mode']==420,'publication mode')
        require(not m['install'] or rel in NATIVE|ATTEMPT|PROGRAM,'outside local installation scope')
    return plan

def publish(plan,journal,run_dir):
    guard(plan,journal);require(remote(journal)==plan['base_commit'],'remote changed; rebuild/review plan')
    git(['cat-file','-e',plan['base_commit']+'^{commit}'],journal)
    for m in plan['protected_remote_inputs']:
        z=git(['ls-tree','-z',plan['base_commit'],'--',m['path']],journal)
        require(digest(z)==m['tree_sha256'],'native dependency tree changed')
        b=git(['show',plan['base_commit']+':'+m['path']],journal)
        require(len(b)==m['bytes'] and digest(b)==m['sha256'],'native dependency body changed')
    require(not (run_dir/'index').exists(),'private index exists')
    index=run_dir/'index'
    for m in plan['members']:
        z=git(['ls-tree','-z',plan['base_commit'],'--',m['path']],journal)
        require(digest(z)==m['pre_tree_sha256'],'current remote path/mode/blob changed')
    git(['read-tree',plan['base_commit']],journal,index)
    for m in plan['members']:
        b=Path(m['source']).read_bytes();require(digest(b)==m['post']['sha256'],'source changed before staging')
        blob=git(['hash-object','-w','--stdin'],journal,data=b).decode().strip()
        require(blob==m['post_blob'],'blob mismatch')
        git(['update-index','--add','--cacheinfo','100644',blob,m['path']],journal,index)
    tree=git(['write-tree'],journal,index).decode().strip()
    changed=set(git(['diff','--name-only','-z',plan['base_commit'],tree],journal).decode().split('\0'))-{''}
    require(changed==set(plan['expected_changed_paths']),'complete tree differs outside exact overlay')
    for m in plan['members']:
        z=git(['ls-tree','-z',tree,'--',m['path']],journal)
        require(z==('100644 blob '+m['post_blob']+'\t'+m['path']+'\0').encode(),'proposed tree blob/mode')
    guard(plan,journal);require(remote(journal)==plan['base_commit'],'remote changed before commit')
    commit=git(['commit-tree',tree,'-p',plan['base_commit']],journal,data=(plan['commit_message']+'\n').encode()).decode().strip()
    journal.update(proposed_commit=commit,tree=tree,status='push_outcome_unresolved',push_dispatch_pending=True);dump(run_dir/'RECEIPT.json',journal)
    # Normal push: a concurrent remote update causes rejection, never replacement.
    try: git(['push',URL,commit+':refs/heads/main'],journal)
    except BaseException:
        journal['status']='push_outcome_unresolved';dump(run_dir/'RECEIPT.json',journal);raise
    journal['status']='push_returned_success_readback_pending';dump(run_dir/'RECEIPT.json',journal)
    current=remote(journal)
    if current!=commit:
        git(['fetch','--no-write-fetch-head','--no-tags','--refmap=',URL,current],journal)
        git(['merge-base','--is-ancestor',commit,current],journal)
    for m in plan['members']:
        z=git(['show',current+':'+m['path']],journal)
        require(len(z)==m['post']['bytes'] and digest(z)==m['post']['sha256'],'published full body changed')
    guard(plan,journal)
    journal.update(status='published_local_install_pending',published_commit=commit,observed_remote=current,public_full_body_readback=True,whole_parent_tree_preserved_outside_exact_overlay=True)

def install(plan,journal,run_dir,published_receipt,published_sha):
    require(digest(safe(published_receipt).read_bytes())==published_sha,'published receipt SHA')
    previous=json.loads(safe(published_receipt).read_bytes())
    require(previous['plan_sha256']==journal['plan_sha256'] and previous['status']=='published_local_install_pending','authenticated published receipt required')
    current=remote(journal);commit=previous['published_commit']
    if current!=commit:
        git(['fetch','--no-write-fetch-head','--no-tags','--refmap=',URL,current],journal);git(['merge-base','--is-ancestor',commit,current],journal)
    guard(plan,journal)
    selected=[m for m in plan['members'] if m['install']]
    # Resume forward after interruption: every owned path must match pre or post.
    already=[]
    for m in selected:
        path=safe(C/m['path'])
        if path.exists() and pin(path)==m['post']:already.append(m['path'])
        elif m['local_pre'] is None:require(not path.exists(),'new local path differs from reviewed postimage')
        else:check(path,m['local_pre'])
        b=git(['show',current+':'+m['path']],journal)
        require(digest(b)==m['post']['sha256'],'current public postimage mismatch')
    journal.update(status='published_local_install_in_progress',published_commit=commit,installed=[],observed_preexisting_postimages=already);dump(run_dir/'RECEIPT.json',journal)
    for i,m in enumerate(selected):
        path=safe(C/m['path']);path.parent.mkdir(parents=True,exist_ok=True);safe(path.parent)
        if m['path'] in already:check(path,m['post']);continue
        if m['local_pre'] is not None:
            backup=run_dir/('before_'+str(i));backup.write_bytes(path.read_bytes());os.chmod(backup,m['local_pre']['mode']);check(backup,m['local_pre'])
        # A new run gets a distinct temporary name, preserving old partial files.
        tmp=path.with_name(path.name+'.pr134-'+journal['plan_sha256'][:12]+'-'+run_dir.name+'.tmp')
        if tmp.exists():
            check(tmp,m['post']);journal.setdefault('observed_preexisting_install_temps',[]).append(str(tmp))
        else:
            with tmp.open('xb') as f:
                f.write(Path(m['source']).read_bytes());f.flush();os.fsync(f.fileno())
            os.chmod(tmp,420);check(tmp,m['post'])
        journal['installing_path']=m['path'];dump(run_dir/'RECEIPT.json',journal)
        if m['local_pre'] is None: require(not path.exists(),'concurrent local creation')
        else: check(path,m['local_pre'])
        os.replace(tmp,path);check(path,m['post']);journal['installed'].append(m['path']);dump(run_dir/'RECEIPT.json',journal)
    for m in selected:check(C/m['path'],m['post'])
    guard(plan,journal)
    journal.update(status='public_and_local_install_verified',local_full_body_mode_readback=True,multiple_file_install_globally_atomic=False,private_cache_installed=False)

def main():
    action,pp,ps,rp,rs,rd,*rest=sys.argv[1:]
    require(action in ['publish','install'],'action')
    run_dir=safe(rd);require(run_dir.parent==D/'private','run directory scope');run_dir.mkdir(exist_ok=False)
    journal={'schema':'pr134-scoped-operation-receipt/v1','actual_PID':os.getpid(),'UTC_start':utc(),'action':action,'plan_sha256':ps,'source_sha256':digest(Path(__file__).read_bytes()),'review_sha256':rs,'children':[],'status':'starting'}
    lock=D/'private/OPERATION_LOCK.json';owned_lock=None;lock_identity=None
    try:
        safe(lock);fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        try:
            s=os.fstat(fd);lock_identity=(s.st_dev,s.st_ino)
            os.write(fd,json.dumps({'PID':os.getpid(),'UTC':utc(),'plan_sha256':ps}).encode());os.fsync(fd)
        finally:os.close(fd)
        owned_lock=pin(lock)
        plan=load_inputs(pp,ps,rp,rs)
        if action=='publish': require(not rest,'publish arguments');publish(plan,journal,run_dir)
        else: require(len(rest)==2,'published receipt path/SHA arguments');install(plan,journal,run_dir,rest[0],rest[1])
    except BaseException as e:
        journal.update(error_type=type(e).__name__,error=str(e)[:4096]);raise
    finally:
        children_safe=all(e.get('child_reaped') is True and e.get('process_group_empty') is True for e in journal['children'])
        if lock_identity is not None and children_safe:
            try:
                safe(lock);s=lock.lstat();require((s.st_dev,s.st_ino)==lock_identity,'lock ownership changed')
                if owned_lock is not None:check(lock,owned_lock)
                lock.unlink();journal['own_operation_lock_released']=True
            except BaseException as exc:journal['own_operation_lock_released']=False;journal['lock_release_error']=str(exc)[:4096]
        elif lock_identity is not None:
            journal['own_operation_lock_released']=False;journal['lock_retained_for_unresolved_children']=True
        journal['UTC_end']=utc()
        try:dump(run_dir/'RECEIPT.json',journal)
        except BaseException:
            print(json.dumps({'receipt_persistence_failed':True,'PID':os.getpid(),'status':journal['status'],'original_error_type':journal.get('error_type'),'unresolved_children':[e.get('PID') for e in journal['children'] if not e.get('child_reaped') or not e.get('process_group_empty')],'lock_released':journal.get('own_operation_lock_released')}))
            raise
    require(journal.get('own_operation_lock_released') is True,'owned operation lock release incomplete')
    print(json.dumps({'status':journal['status'],'receipt':str(run_dir/'RECEIPT.json'),'PID':os.getpid()}))

if __name__=='__main__': main()

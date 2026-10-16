"""Publish a reviewed sparse tree overlay; never change checkout refs/index.

Audit-only checkpoint: native, canonical and global program paths are excluded; no local installation action exists.
Every action requires the exact plan and an independent source/plan PASS.
"""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, signal, stat, subprocess, sys, time, tempfile

R = Path('/Users/alec/Documents/Math')
C = R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A = C/'draft_pr_publication_program_20260930/audits/pr141_30003818'
D = A/'checkpoint_preparation_20261007'
G = '/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
URL = 'https://github.com/AlecKriebel/Math.git'
AUDIT = ('draft_pr_publication_program_20260930/audits/pr141_30003818/','draft_pr_publication_program_20260930/ordered_intake_20261007/after_PR140/')
PREVIOUS_AUDIT = 'draft_pr_publication_program_20260930/audits/pr140_5100023/'
PREVIOUS_PUBLIC = {PREVIOUS_AUDIT+n for n in ['ROOT_FINAL_METADATA_ACCEPTANCE_20261007.json','actual_final_metadata_root_readback_20261007/ROOT_READBACK.json','RESEARCH_LOG.md']}
ORIGINAL_HEAD = '523247e3246a5f44c7b0089074bb304c1f642bd0'
PREVIOUS_ACCEPTANCE_SHA = 'cee4dff32b212eac03bfc29844bcc0facd8a6e779aa0ebb2f15191c5449305a5'

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
    require(digest(Path(__file__).read_bytes())==plan['source_sha256'],'running source changed')
    prior=plan['previous_PR140_acceptance'];require(prior['path']==str(C/PREVIOUS_AUDIT/'ROOT_FINAL_METADATA_ACCEPTANCE_20261007.json') and prior['sha256']==PREVIOUS_ACCEPTANCE_SHA,'actual prior completion custody')
    check(prior['path'],prior);accepted=json.loads(Path(prior['path']).read_bytes())
    require(accepted['owner']=='ROOT' and accepted['fixture_only'] is False and accepted['status']=='ACCEPTED_COMPLETE' and accepted['case_PR']==140 and accepted['case_percent']==100 and accepted['completed_count']==24 and accepted['published_count']==12 and accepted['overall_goal_complete'] is False,'genuine PR140 completed case; overall goal incomplete')
    for role in ['source','plan','publish','install','root_readback','native_acceptance','actual_acceptance_inputs']:check(accepted[role]['path'],accepted[role])
    for x in plan['protected']: check(x['path'],x)
    for x in plan['protected_absences']: require(not safe(x).exists(),'protected absence changed: '+x)
    for root,expected in [(R,plan['R_HEAD']),(C,plan['C_HEAD'])]:
        got=git(['-C',str(root),'rev-parse','HEAD','refs/heads/main'],journal).decode().splitlines()
        require(got==[expected,expected],'local main/HEAD changed')
    pr=json.loads(run([GH,'api','repos/AlecKriebel/Math/pulls/134'],journal))
    require(pr['state']=='closed' and pr['merged_at'] is None and pr['draft'] is True and pr['head']['sha']==plan['previous_PR134_original_head'],'PR134 disposition changed')
    comment=json.loads(run([GH,'api','repos/AlecKriebel/Math/issues/comments/6028564660'],journal))
    require(digest(comment['body'].encode())==plan['closing_comment_body_sha256'],'closing comment changed')
    previous_pr=json.loads(run([GH,'api','repos/AlecKriebel/Math/pulls/140'],journal))
    merge=plan['previous_PR140_merge']
    require(previous_pr['state']=='closed' and previous_pr['merged'] is True and previous_pr['merged_at']==merge['merged_at'] and previous_pr['merge_commit_sha']==merge['commit'] and previous_pr['head']['sha']==merge['original_head'],'PR140 accepted original merge changed')
    current_pr=json.loads(run([GH,'api','repos/AlecKriebel/Math/pulls/141'],journal))
    require(current_pr['state']=='open' and current_pr['merged_at'] is None and current_pr['draft'] is True and current_pr['head']['sha']==ORIGINAL_HEAD,'PR141 original intake head/state changed')

def load_inputs(plan_path,plan_sha,review_path,review_sha):
    require(digest(safe(plan_path).read_bytes())==plan_sha,'plan SHA')
    plan=json.loads(Path(plan_path).read_bytes())
    require(plan['schema']=='pr141-audit-only-checkpoint-overlay/v1','plan schema')
    require(plan['source_sha256']==digest(Path(__file__).read_bytes()),'source SHA')
    require(plan['scope']=='PR141_AUDIT_ONLY_PROVISIONAL' and plan['case_publication_acceptance'] is False and plan['priority_clearance'] is False and plan['goal_complete'] is False,'audit checkpoint; mathematical gate separate, priority/publication pending')
    require(digest(safe(review_path).read_bytes())==review_sha,'review SHA')
    review=json.loads(Path(review_path).read_bytes())
    require(review['verdict']=='PASS' and review['plan_sha256']==plan_sha and review['source_sha256']==plan['source_sha256'],'independent source/plan review')
    check(G,plan['git_executable']);check(GH,plan['gh_executable'])
    required={str(root/'.git'/name) for root in (R,C) for name in ['index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main','index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']}
    protected={x['path'] for x in plan['protected']};absent=set(plan['protected_absences'])
    require(len(protected)==len(plan['protected']) and len(absent)==len(plan['protected_absences']) and not protected&absent and required<=protected|absent,'complete exact real Git resource baselines')
    require(all(str(C/'unsolved_math_prioritization'/name) in absent for name in ['queue.py','manifest.json','policy.json','cache/catalog.sqlite']),'intentional backend/cache absences preserved')
    require(all(str(root/'.git'/name) in absent for root in (R,C) for name in ['index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']),'real Git locks remain absent')
    seen=set()
    for m in plan['members']:
        rel=m['path'];require(str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts,'invalid relative path')
        require(rel in PREVIOUS_PUBLIC or rel.startswith(AUDIT),'outside exact audit-only publication scope')
        require(not any(p.casefold().startswith('private') or p.casefold() in {'cache','.git','replay','working_controls'} for p in PurePosixPath(rel).parts),'private/cache/working control publication forbidden')
        require(PurePosixPath(rel).suffix.casefold() in {'.md','.json','.jsonl','.py','.patch'},'copyrighted primary material and raster/text exports excluded')
        require(rel.casefold() not in seen,'case duplicate');seen.add(rel.casefold())
        check(m['source'],m['post'])
        require(m['post']['mode']==420,'publication mode')
        require(m['install'] is False and m['local_pre'] is None,'audit-only checkpoint cannot install any path')
    require(seen,'nonempty explicit public audit selection')
    return plan

def tree_oid(value):
    require(isinstance(value, str) and len(value)==40 and all(c in '0123456789abcdef' for c in value), 'invalid Git object ID')
    return value

def tree_oid_output(body):
    require(isinstance(body, bytes) and len(body)==41 and body[-1:]==b'\n', 'invalid Git object output')
    try:value=body[:-1].decode('ascii')
    except UnicodeDecodeError:raise RuntimeError('non-ASCII Git object output')
    return tree_oid(value)

def parse_tree_entries(body):
    require(isinstance(body, bytes), 'tree listing must be bytes')
    if not body:return {}
    require(body.endswith(b'\0'), 'unterminated tree listing')
    entries={}
    types={b'040000':b'tree', b'100644':b'blob', b'100755':b'blob', b'120000':b'blob', b'160000':b'commit'}
    for record in body[:-1].split(b'\0'):
        header, sep, name=record.partition(b'\t')
        fields=header.split(b' ')
        require(sep and len(fields)==3, 'malformed tree record')
        mode,kind,raw_oid=fields
        require(mode in types and kind==types[mode], 'tree mode/type collision')
        require(name and name not in (b'.',b'..') and b'/' not in name, 'invalid tree entry name')
        require(name not in entries, 'duplicate tree entry name')
        try:oid=raw_oid.decode('ascii')
        except UnicodeDecodeError:raise RuntimeError('non-ASCII tree object ID')
        tree_oid(oid)
        entries[name]=(mode,kind,raw_oid,name)
    return entries

def overlay_path_trie(replacements):
    require(isinstance(replacements, dict) and replacements, 'nonempty overlay required')
    root={};seen=set()
    for path,oid in replacements.items():
        require(isinstance(path,str) and path and '\0' not in path, 'invalid overlay path')
        p=PurePosixPath(path)
        require(p.parts and not p.is_absolute() and str(p)==path and all(x not in ('.','..') for x in p.parts), 'noncanonical overlay path')
        require(path.casefold() not in seen, 'case duplicate overlay path');seen.add(path.casefold())
        try:parts=[part.encode('utf-8') for part in p.parts]
        except UnicodeEncodeError:raise RuntimeError('overlay path is not UTF-8')
        tree_oid(oid);node=root
        for i,name in enumerate(parts):
            aliases=[n for n in node if n.decode('utf-8').casefold()==name.decode('utf-8').casefold() and n!=name]
            require(not aliases, 'case alias overlay prefix')
            if i==len(parts)-1:
                require(name not in node, 'overlay leaf/tree-prefix collision')
                node[name]=('blob',oid)
            else:
                if name not in node:node[name]={}
                require(isinstance(node[name],dict), 'overlay leaf/tree-prefix collision')
                node=node[name]
    return root

def serialize_tree_entries(entries):
    ordered=sorted(entries.values(), key=lambda e:e[3]+(b'/' if e[1]==b'tree' else b'\0'))
    return b''.join(mode+b' '+kind+b' '+oid+b'\t'+name+b'\0' for mode,kind,oid,name in ordered)

def sparse_overlay_tree(base_tree, replacements, read_tree, write_tree):
    # Callbacks read immediate children and write only changed ancestor trees.
    # Unselected subtrees, opaque byte names, modes and object IDs remain intact.
    trie=overlay_path_trie(replacements);tree_oid(base_tree)
    def descend(old_oid,node):
        before=parse_tree_entries(read_tree(old_oid)) if old_oid is not None else {}
        after=before.copy()
        for name,replacement in node.items():
            folded=name.decode('utf-8').casefold()
            aliases=[n for n in before if n!=name and n.decode('utf-8','surrogateescape').casefold()==folded]
            require(not aliases, 'existing tree case alias collision')
            old=before.get(name)
            if isinstance(replacement,dict):
                require(old is None or (old[0],old[1])==(b'040000',b'tree'), 'overlay branch collides with non-tree')
                child=descend(old[2].decode('ascii') if old is not None else None,replacement)
                after[name]=(b'040000',b'tree',child.encode('ascii'),name)
            else:
                require(old is None or (old[0] in (b'100644',b'100755') and old[1]==b'blob'), 'overlay leaf mode/type collision')
                after[name]=(b'100644',b'blob',replacement[1].encode('ascii'),name)
        if old_oid is not None and after==before:return old_oid
        return tree_oid(write_tree(serialize_tree_entries(after)))
    return descend(base_tree,trie)

def build_proposed_tree(plan,journal):
    replacements={}
    for m in plan['members']:
        require(m['path'] not in replacements, 'duplicate selected path')
        replacements[m['path']]=tree_oid(m['post_blob'])
    # Reject prefix/case/type ambiguities before creating selected blob objects.
    overlay_path_trie(replacements)
    for m in plan['members']:
        b=Path(m['source']).read_bytes()
        require(len(b)==m['post']['bytes'] and digest(b)==m['post']['sha256'], 'source changed before staging')
        expected=hashlib.sha1(b'blob '+str(len(b)).encode('ascii')+b'\0'+b).hexdigest()
        blob=tree_oid_output(git(['hash-object','-w','--stdin'],journal,data=b))
        require(blob==m['post_blob']==expected, 'blob mismatch')
    base_tree=tree_oid_output(git(['rev-parse',plan['base_commit']+'^{tree}'],journal))
    def read_tree(oid):return git(['ls-tree','-z',oid],journal)
    def write_tree(body):return tree_oid_output(git(['mktree','-z'],journal,data=body))
    return sparse_overlay_tree(base_tree,replacements,read_tree,write_tree)

def publish(plan,journal,run_dir):
    guard(plan,journal);require(remote(journal)==plan['base_commit'],'remote changed; rebuild/review plan')
    git(['cat-file','-e',plan['base_commit']+'^{commit}'],journal)
    for m in plan['protected_remote_inputs']:
        z=git(['ls-tree','-z',plan['base_commit'],'--',m['path']],journal)
        require(digest(z)==m['tree_sha256'],'readonly dependency tree changed')
        b=git(['show',plan['base_commit']+':'+m['path']],journal)
        require(len(b)==m['bytes'] and digest(b)==m['sha256'],'readonly dependency body changed')
    for m in plan['members']:
        z=git(['ls-tree','-z',plan['base_commit'],'--',m['path']],journal)
        require(digest(z)==m['pre_tree_sha256'],'current remote path/mode/blob changed')
    tree=build_proposed_tree(plan,journal)
    changed=set(git(['diff','--no-ext-diff','--no-textconv','--no-renames','--name-only','-z',plan['base_commit'],tree],journal).decode().split('\0'))-{''}
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
    journal.update(status='published_audit_only_checkpoint_verified',published_commit=commit,observed_remote=current,public_full_body_readback=True,whole_parent_tree_preserved_outside_exact_overlay=True)


def main():
    action,pp,ps,rp,rs,rd,*rest=sys.argv[1:]
    require(action=='publish' and not rest,'audit-only publish action')
    run_dir=safe(rd);require(run_dir.parent==D/'private','run directory scope');run_dir.mkdir(exist_ok=False)
    journal={'schema':'pr141-audit-only-checkpoint-operation-receipt/v1','actual_PID':os.getpid(),'UTC_start':utc(),'action':action,'plan_sha256':ps,'source_sha256':digest(Path(__file__).read_bytes()),'review_sha256':rs,'children':[],'status':'starting'}
    lock=D/'private/OPERATION_LOCK.json';owned_lock=None;lock_identity=None
    try:
        safe(lock);fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        try:
            s=os.fstat(fd);lock_identity=(s.st_dev,s.st_ino)
            os.write(fd,json.dumps({'PID':os.getpid(),'UTC':utc(),'plan_sha256':ps}).encode());os.fsync(fd)
        finally:os.close(fd)
        owned_lock=pin(lock)
        plan=load_inputs(pp,ps,rp,rs)
        publish(plan,journal,run_dir)
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

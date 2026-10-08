"""Later PR141 final package/audits/program3 publisher. SOURCE PREPARATION ONLY.
No actual plan, closing gate, grant, write, push or installation is supplied here.
Runtime requires exact native closure, pure renderer replay, selected full inventory,
current protection and an independent actual source/data/plan PASS.
"""
from pathlib import Path, PurePosixPath
import argparse,base64,datetime,hashlib,json,lzma,os,signal,stat,subprocess,sys,time,types,uuid
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A=C/'draft_pr_publication_program_20260930/audits/pr141_30003818'
D=A/'final_package_metadata_operator_preparation_20261007'
G='/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
URL='https://github.com/AlecKriebel/Math.git'
ORIGINAL_HEAD='523247e3246a5f44c7b0089074bb304c1f642bd0'
ATTEMPT_PREFIX='unsolved_math_prioritization/attempts/30003818/'
PROGRAM={'draft_pr_publication_program_20260930/'+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
READONLY_PATHS={'unsolved_math_prioritization/'+n for n in ('queue.py','manifest.json','policy.json','SHORTLIST.md')}
GIT_FILES=('index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main')
GIT_LOCKS=('index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock','config.lock','FETCH_HEAD.lock')
RENDERER_SOURCE_SHA='40656b6792dfc5d7facaa2797ae6e187f1f2160747dd85da761b371b22c007c0'
RENDERER_CONTRACT_SHA='6087a81599af53547d95c71166dd390a89631d56ca27f565133ecd746d3bd03a'


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
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_nlink>=1,'regular file required')
        h=hashlib.sha256()
        while b:=os.read(fd,1048576):h.update(b)
        after=os.fstat(fd); named=path.lstat()
        signature=lambda z:(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns,z.st_mode,z.st_nlink)
        require(signature(s)==signature(after)==signature(named),'file changed during pin read')
        return {'bytes':s.st_size,'mode':stat.S_IMODE(s.st_mode),'sha256':h.hexdigest()}
    finally:os.close(fd)

def check(path, expected):
    require(pin(path) == {k:expected[k] for k in ['bytes','mode','sha256']}, 'pin mismatch: '+str(path))

class JournalWriteFailure(RuntimeError):
    def __init__(self,error,custody):
        super().__init__('journal write failed: '+type(error).__name__+': '+str(error))
        self.journal_write_failure=custody

def dump(path, value):
    path=safe(path)
    tmp=path.with_name(path.name+'.tmp.'+str(os.getpid())+'.'+uuid.uuid4().hex)
    fd=None;identity=None;created=False;replaced=False
    custody={'path':str(path),'temporary_path':str(tmp),'created':False,'replaced':False,'owned_identity':None,'cleanup':'not_needed'}
    try:
        safe(tmp);fd=os.open(tmp,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        created=True;custody['created']=True
        info=os.fstat(fd);identity=(info.st_dev,info.st_ino)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink==1,'own journal temporary regular single-link file')
        custody['owned_identity']={'dev':identity[0],'ino':identity[1]}
        handle=os.fdopen(fd,'w',encoding='utf-8');fd=None
        with handle:
            json.dump(value,handle,indent=2,sort_keys=True);handle.write('\n');handle.flush()
            os.fchmod(handle.fileno(),420);os.fsync(handle.fileno())
        safe(tmp);named=tmp.lstat()
        require((named.st_dev,named.st_ino)==identity and stat.S_ISREG(named.st_mode) and named.st_nlink==1,'owned journal temporary identity changed before replacement')
        safe(path);os.replace(tmp,path);replaced=True;custody['replaced']=True
    except BaseException as error:
        if fd is not None:
            try:os.close(fd)
            except BaseException as close_error:custody['close_error']=type(close_error).__name__+': '+str(close_error)
            fd=None
        if created and not replaced:
            try:
                safe(tmp);named=tmp.lstat()
                require(identity is not None and (named.st_dev,named.st_ino)==identity and stat.S_ISREG(named.st_mode) and named.st_nlink==1,'journal cleanup ownership not proven')
                tmp.unlink();custody['cleanup']='owned_temporary_removed'
            except FileNotFoundError:custody['cleanup']='temporary_already_absent'
            except BaseException as cleanup_error:
                custody['cleanup']='retained_cleanup_unresolved';custody['cleanup_error']=type(cleanup_error).__name__+': '+str(cleanup_error)
        raise JournalWriteFailure(error,custody) from error

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

def native_json(body):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result, 'duplicate JSON key');result[key]=value
        return result
    def bad(value):raise RuntimeError('nonfinite JSON constant')
    return json.loads(body,object_pairs_hook=pairs,parse_constant=bad)

def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()

def sha_value(value):
    require(isinstance(value,str) and len(value)==64 and all(c in '0123456789abcdef' for c in value),'SHA256 required')
    return value

def absolute(value):
    require(isinstance(value,str) and Path(value).is_absolute() and str(Path(value))==value and '..' not in Path(value).parts,'canonical absolute path required')
    return safe(value)

def relative(value):
    require(isinstance(value,str) and value and '\0' not in value and '\\' not in value,'relative path required')
    p=PurePosixPath(value)
    require(not p.is_absolute() and str(p)==value and all(c not in ('.','..') for c in p.parts),'canonical relative path required')
    require(not any(c.casefold().startswith('private') or c.casefold() in {'cache','.git'} for c in p.parts),'private/cache/Git publication forbidden')
    return value

def full_pin(spec):
    require(isinstance(spec,dict) and set(spec)=={'path','bytes','mode','sha256'},'exact full file pin required')
    absolute(spec['path']);sha_value(spec['sha256'])
    require(type(spec['bytes']) is int and spec['bytes']>=0 and type(spec['mode']) is int and 0<=spec['mode']<=0o777,'typed file bytes/mode')
    check(spec['path'],spec)
    return spec

def read_pinned(spec):
    full_pin(spec);body=absolute(spec['path']).read_bytes()
    require(len(body)==spec['bytes'] and digest(body)==spec['sha256'],'body changed during authenticated read')
    return body

def path_pin(path):
    path=absolute(str(path));return {'path':str(path),**pin(path)}

def decode_storage(body,encoding,expected):
    require(type(body) is bytes and encoding in ('raw','xz'),'explicit raw/xz postimage storage')
    require(set(expected)=={'bytes','mode','sha256'} and type(expected['bytes']) is int and expected['bytes']>=0 and expected['mode']==420,'exact decoded body pin')
    sha_value(expected['sha256'])
    if encoding=='xz':
        try:
            decoder=lzma.LZMADecompressor(format=lzma.FORMAT_XZ,memlimit=256*1024*1024)
            decoded=decoder.decompress(body,max_length=expected['bytes']+1)
        except lzma.LZMAError:raise RuntimeError('invalid or excessive-memory XZ postimage')
        require(decoder.eof and not decoder.unused_data,'truncated, trailing or concatenated XZ postimage')
    else:decoded=body
    require(len(decoded)==expected['bytes'] and digest(decoded)==expected['sha256'],'decoded postimage fullbody size/SHA mismatch')
    return decoded

def local_case_guard(path):
    path=absolute(str(path));parts=path.parts
    parent=Path(parts[0])
    for name in parts[1:]:
        if parent.exists():
            require(parent.is_dir(),'non-directory local prefix')
            aliases=[p.name for p in parent.iterdir() if p.name.casefold()==name.casefold() and p.name!=name]
            require(not aliases,'local case alias: '+str(parent/name))
        parent=parent/name
    return path

def closed_directory(spec):
    require(isinstance(spec,dict) and set(spec)=={'path','files','directories'},'closed protected directory specification')
    root=local_case_guard(spec['path']);require(root.is_dir(),'protected directory absent')
    require(isinstance(spec['files'],list) and isinstance(spec['directories'],list),'closed directory inventory types')
    expected={};folded=set()
    for item in spec['files']:
        require(isinstance(item,dict) and set(item)=={'relative','bytes','mode','sha256'},'protected directory file pin')
        rel=item['relative'];p=PurePosixPath(rel)
        require(isinstance(rel,str) and str(p)==rel and not p.is_absolute() and '..' not in p.parts and rel,'protected relative path')
        require(rel.casefold() not in folded,'protected directory case duplicate');folded.add(rel.casefold())
        require(type(item['bytes']) is int and item['bytes']>=0 and type(item['mode']) is int and 0<=item['mode']<=0o777,'typed protected directory file bytes/mode')
        sha_value(item['sha256'])
        expected[rel]={k:item[k] for k in ('bytes','mode','sha256')}
    dirs=set(spec['directories']);require(len(dirs)==len(spec['directories']),'duplicate protected directory')
    for rel in dirs:
        p=PurePosixPath(rel);require(isinstance(rel,str) and rel and str(p)==rel and not p.is_absolute() and '..' not in p.parts,'protected directory relative path')
        require(rel.casefold() not in folded,'protected directory case duplicate');folded.add(rel.casefold())
    actual_files={};actual_dirs=set()
    for directory,children,files in os.walk(root,followlinks=False):
        for name in children:
            child=Path(directory)/name;safe(child);require(child.is_dir(),'protected non-directory child')
            actual_dirs.add(child.relative_to(root).as_posix())
        for name in files:
            child=Path(directory)/name;actual_files[child.relative_to(root).as_posix()]=pin(child)
    require(actual_files==expected and actual_dirs==dirs,'closed protected directory changed: '+str(root))

def git(args,journal,data=None,allowed=(0,),root=R):
    require(args and args[0] in {'rev-parse','cat-file','ls-tree','hash-object','mktree','diff','commit-tree','merge-base','push','fetch'},'object-only Git command required')
    require(args[0]!='push' or args==['push','--no-verify','--no-follow-tags',URL,journal['proposed_commit']+':refs/heads/main'],'exact normal main push required')
    require(args[0]!='fetch' or args==['fetch','--no-write-fetch-head','--no-tags','--refmap=',URL,tree_oid(journal['object_acquisition_oid'])],'one fixed-OID object-only acquisition required')
    env=os.environ.copy()
    for key in list(env):
        if key.startswith('GIT_'):del env[key]
    env['GIT_OPTIONAL_LOCKS']='0';env['GIT_NO_REPLACE_OBJECTS']='1'
    return run([G,'-C',str(root),'-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','core.splitIndex=false','-c','gc.auto=0','-c','maintenance.auto=0','-c','push.recurseSubmodules=no','-c','fetch.prune=false','-c','fetch.pruneTags=false','-c','fetch.recurseSubmodules=false','-c','fetch.writeCommitGraph=false',*args],journal,env,data,allowed)

def remote(journal):
    body=run([GH,'api','repos/AlecKriebel/Math/git/ref/heads/main'],journal)
    value=native_json(body);require(value['ref']=='refs/heads/main','direct main response identity')
    return tree_oid(value['object']['sha'])

def expected_tree_record(member,post=False):
    spec=member['post'] if post else member['remote_pre']
    if spec is None:return b''
    require(spec['mode']==420,'scoped public body must mode100644')
    blob=member['post_blob'] if post else spec['Git_blob']
    tree_oid(blob)
    return ('100644 blob '+blob+'\t'+member['path']+'\0').encode()

def ensure_base_objects(plan,journal):
    before=len(journal['children'])
    git(['cat-file','-e',plan['base_commit']+'^{commit}'],journal,allowed=(0,1,128))
    require(len(journal['children'])==before+1,'base object probe child custody')
    if journal['children'][-1]['exit_code']==0:return
    guard(plan,journal);require(remote(journal)==plan['base_commit'],'direct main drift before object-only acquisition')
    journal['object_acquisition_oid']=tree_oid(plan['base_commit'])
    journal['fixed_oid_object_acquisition_attempted']=True
    git(['fetch','--no-write-fetch-head','--no-tags','--refmap=',URL,plan['base_commit']],journal)
    guard(plan,journal);require(remote(journal)==plan['base_commit'],'direct main drift during object-only acquisition')
    git(['cat-file','-e',plan['base_commit']+'^{commit}'],journal)
    journal['fixed_oid_object_acquisition_verified']=True

def build_proposed_tree(plan,journal):
    replacements={m['path']:tree_oid(m['post_blob']) for m in plan['remote_members']}
    overlay_path_trie(replacements)
    for member in plan['remote_members']:
        body=read_postimage(member)
        blob=tree_oid_output(git(['hash-object','-w','--stdin'],journal,data=body))
        require(blob==member['post_blob'],'selected blob object equality')
    base_tree=tree_oid_output(git(['rev-parse',plan['base_commit']+'^{tree}'],journal))
    def read_tree(oid):return git(['ls-tree','-z',oid],journal)
    def write_tree(body):return tree_oid_output(git(['mktree','-z'],journal,data=body))
    tree=sparse_overlay_tree(base_tree,replacements,read_tree,write_tree)
    changed=git(['diff','--no-ext-diff','--no-textconv','--no-renames','--name-only','-z',plan['base_commit'],tree],journal)
    names=changed.decode('utf-8').split('\0')
    require(names[-1:]==[''] and len(names[:-1])==len(plan['expected_changed_paths']) and set(names[:-1])==set(plan['expected_changed_paths']),'whole parent tree differs at exact reviewed selected paths only')
    for member in plan['remote_members']:
        require(git(['ls-tree','-z',tree,'--',member['path']],journal)==expected_tree_record(member,True),'proposed exact selected100644 postimages')
    return tree

def public_readback(plan,journal,commit,members):
    require(remote(journal)==commit,'remote main changed; no fetch, retry or installation')
    for member in members:
        record=git(['ls-tree','-z',commit,'--',member['path']],journal)
        require(record==expected_tree_record(member,True),'observed public path/mode/blob differs')
        response=native_json(run([GH,'api','repos/AlecKriebel/Math/git/blobs/'+member['post_blob']],journal))
        require(response['sha']==member['post_blob'] and response['encoding']=='base64' and type(response['size']) is int and response['size']==member['post']['bytes'] and isinstance(response['content'],str),'direct public blob response identity/size/encoding')
        try:body=base64.b64decode(response['content'].replace('\n',''),validate=True)
        except (ValueError,TypeError):raise RuntimeError('invalid direct public blob encoding')
        require(len(body)==member['post']['bytes'] and digest(body)==member['post']['sha256'],'direct public fullbody differs')
        journal.setdefault('public_blob_readbacks',[]).append({'path':member['path'],'commit':commit,'Git_blob':member['post_blob'],'bytes':len(body),'sha256':digest(body),'mode':420})
    require(remote(journal)==commit,'remote main changed during public readback')

def publish(plan,journal,run_dir):
    guard(plan,journal);local_preimage_guard(plan)
    require(remote(journal)==plan['base_commit'],'remote main changed; new actual request/plan/review required')
    ensure_base_objects(plan,journal)
    check_remote_preimages(plan,journal)
    tree=build_proposed_tree(plan,journal)
    guard(plan,journal);local_preimage_guard(plan)
    require(remote(journal)==plan['base_commit'],'remote main changed before commit')
    commit=tree_oid_output(git(['commit-tree',tree,'-p',plan['base_commit']],journal,data=(plan['commit_message']+'\n').encode()))
    commit_body=git(['cat-file','commit',commit],journal)
    headers=commit_body.split(b'\n\n',1)[0].splitlines()
    require([h for h in headers if h.startswith(b'tree ')]==[b'tree '+tree.encode()] and [h for h in headers if h.startswith(b'parent ')]==[b'parent '+plan['base_commit'].encode()],'exact sole-parent overlay commit')
    journal.update(proposed_commit=commit,tree=tree,status='push_dispatch_pending',push_dispatch_pending=True)
    dump(run_dir/'RECEIPT.json',journal)
    guard(plan,journal);require(remote(journal)==plan['base_commit'],'remote main changed at dispatch guard')
    journal['status']='push_outcome_unresolved';dump(run_dir/'RECEIPT.json',journal)
    git(['push','--no-verify','--no-follow-tags',URL,commit+':refs/heads/main'],journal)
    journal.update(status='public_published_local_install_pending_readback',published_commit=commit,push_dispatch_pending=False)
    dump(run_dir/'RECEIPT.json',journal)
    public_readback(plan,journal,commit,plan['remote_members'])
    guard(plan,journal);local_preimage_guard(plan)
    journal.update(status='published_local_install_pending',observed_remote=commit,public_full_body_readback=True,public_full_body_mode_readback=True,
                   remote_changed_path_count=len(plan['expected_changed_paths']),remote_selected_path_count=len(plan['remote_members']),local_install_path_count=3,whole_parent_tree_preserved_outside_exact_overlay=True,sole_parent=plan['base_commit'],local_installation_performed=False)

def observe_install_path(path,identity=None):
    result={'path':str(path),'owned_identity':identity}
    try:
        safe(path);info=Path(path).lstat()
        result.update(present=True,identity={'dev':info.st_dev,'ino':info.st_ino},bytes=info.st_size,mode=stat.S_IMODE(info.st_mode),
                      owned_identity_matches=identity=={'dev':info.st_dev,'ino':info.st_ino} if identity is not None else None)
    except FileNotFoundError:result['present']=False
    except BaseException as error:result['observation_error']=type(error).__name__+': '+str(error)
    return result

def install_one(member,journal,run_dir):
    path=local_case_guard(C/member['path']);pre=member['local_pre']
    if pre is None:require(not path.exists(),'concurrent local creation before installation')
    else:check(path,pre)
    body=read_postimage(member)
    tmp=path.with_name(path.name+'.pr141-'+journal['plan_sha256'][:12]+'-'+run_dir.name+'.tmp')
    local_case_guard(tmp);require(not tmp.exists(),'install temp already exists; no automatic recovery')
    current=C;new_dirs=[]
    for component in path.parent.relative_to(C).parts:
        current=current/component;local_case_guard(current)
        if current.exists():require(current.is_dir(),'installation ancestor is not a directory')
        else:new_dirs.append(current)
    intent={'path':member['path'],'local_path':str(path),'temporary_path':str(tmp),'newly_required_directories':[str(p) for p in new_dirs],
            'directories':[{'path':str(p),'state':'intended','identity':None} for p in new_dirs],
            'temporary_file':{'path':str(tmp),'state':'intended','identity':None,'written_bytes':0},
            'replacement':'pending','postimage_readback':'pending','phase':'intent_persistence_pending'}
    journal['installing_path']=member['path'];journal['installing_temp']=str(tmp)
    journal.setdefault('installation_intents',[]).append(intent)
    fd=None
    try:
        # Persist complete exact-path intent before any target mkdir/open.
        dump(run_dir/'RECEIPT.json',journal);intent['phase']='intent_persisted'
        for directory,record in zip(new_dirs,intent['directories']):
            intent['phase']='directory_creation_intended';require(not directory.exists(),'concurrent installation ancestor creation')
            directory.mkdir(exist_ok=False)
            record['state']='created_identity_pending';journal.setdefault('created_install_directories',[]).append(record)
            local_case_guard(directory);info=directory.lstat()
            require(stat.S_ISDIR(info.st_mode),'created installation ancestor changed type')
            record.update(state='created',identity={'dev':info.st_dev,'ino':info.st_ino})
            intent['phase']='directory_created'
            dump(run_dir/'RECEIPT.json',journal)
        local_case_guard(path);local_case_guard(tmp)
        intent['phase']='temporary_creation_intended'
        fd=os.open(tmp,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        intent['temporary_file']['state']='created_identity_pending';journal.setdefault('owned_install_temps',[]).append(str(tmp))
        intent['phase']='temporary_created_identity_pending'
        info=os.fstat(fd);require(stat.S_ISREG(info.st_mode) and info.st_nlink==1,'owned installation temporary regular single-link file')
        identity={'dev':info.st_dev,'ino':info.st_ino}
        intent['temporary_file'].update(state='created',identity=identity)
        intent['phase']='temporary_created'
        dump(run_dir/'RECEIPT.json',journal)
        intent['phase']='writing_temporary';view=memoryview(body)
        while view:
            count=os.write(fd,view[:1048576]);require(type(count) is int and 0<count<=min(len(view),1048576),'zero/invalid installation write')
            intent['temporary_file']['written_bytes']+=count;view=view[count:]
        intent['phase']='chmod_temporary';os.fchmod(fd,420)
        intent['phase']='fsync_temporary';os.fsync(fd)
        os.close(fd);fd=None
        intent['phase']='verify_temporary';check(tmp,member['post'])
        intent['temporary_file']['state']='postimage_verified'
        intent['phase']='replacement_intended';dump(run_dir/'RECEIPT.json',journal)
        if pre is None:require(not path.exists(),'concurrent local creation at atomic replace guard')
        else:check(path,pre)
        local_case_guard(tmp);info=tmp.lstat()
        require({'dev':info.st_dev,'ino':info.st_ino}==identity and stat.S_ISREG(info.st_mode) and info.st_nlink==1,'owned installation temporary identity changed before replace')
        os.replace(tmp,path)
        # Record successful physical replacement before any post-replace check.
        intent['replacement']='completed';intent['temporary_file']['state']='moved_to_target';intent['phase']='replacement_completed'
        journal.setdefault('replaced_paths',[]).append(member['path']);journal['owned_install_temps'].remove(str(tmp))
        dump(run_dir/'RECEIPT.json',journal)
        intent['phase']='verify_replaced_target';check(path,member['post'])
        intent['postimage_readback']='verified';intent['phase']='complete'
        journal['installed'].append(member['path']);dump(run_dir/'RECEIPT.json',journal)
    except BaseException as error:
        intent['failure_phase']=intent['phase'];intent['failure_type']=type(error).__name__
        intent['failure_observation']={'temporary':observe_install_path(tmp,intent['temporary_file']['identity']),
             'target':observe_install_path(path,intent['temporary_file']['identity'] if intent['replacement']=='completed' else None),
             'directories':[observe_install_path(p,record['identity']) for p,record in zip(new_dirs,intent['directories'])]}
        if isinstance(error,JournalWriteFailure):intent['journal_write_failure']=error.journal_write_failure
        # The outer receipt retains this custody; never delete native residues.
        raise
    finally:
        if fd is not None:
            try:os.close(fd)
            except BaseException as error:intent['descriptor_close_error']=type(error).__name__+': '+str(error)

def install(plan,journal,run_dir,receipt_path,receipt_sha):
    receipt_body=absolute(receipt_path).read_bytes();require(digest(receipt_body)==sha_value(receipt_sha),'explicit published receipt SHA')
    prior=native_json(receipt_body)
    require(prior['schema']=='pr141-final-package-program3-operation-receipt/v1' and prior['action']=='publish' and prior['fixture_only'] is False and prior['transaction']==FINAL_TRANSACTION and prior['status']=='published_local_install_pending','actual completed public receipt required')
    require(prior['source_sha256']==journal['source_sha256'] and prior['plan_sha256']==journal['plan_sha256'] and prior['review_sha256']==journal['review_sha256'],'identical reviewed publication custody')
    require(prior['own_operation_lock_released'] is True and prior['public_full_body_readback'] is True and prior['public_full_body_mode_readback'] is True and prior['whole_parent_tree_preserved_outside_exact_overlay'] is True and prior['sole_parent']==plan['base_commit'] and prior['remote_changed_path_count']==len(plan['expected_changed_paths']) and prior['remote_selected_path_count']==len(plan['remote_members']) and prior['local_install_path_count']==3,'complete selected public scope, released owned lock and parent-tree proof')
    require(type(prior['actual_PID']) is int and prior['actual_PID']>0 and 'error_type' not in prior and prior['children'] and all(x.get('child_reaped') is True and x.get('process_group_empty') is True for x in prior['children']),'actual public operation PID/closed children')
    commit=tree_oid(prior['published_commit']);journal.update(published_commit=commit,status='public_published_local_install_pending')
    guard(plan,journal);local_preimage_guard(plan)
    public_readback(plan,journal,commit,plan['remote_members'])
    journal.update(status='public_published_local_install_in_progress',installed=[],published_receipt={'path':str(absolute(receipt_path)),**pin(receipt_path)},multiple_file_install_globally_atomic=False)
    dump(run_dir/'RECEIPT.json',journal)
    for member in plan['install_members']:
        guard(plan,journal);install_one(member,journal,run_dir)
    readbacks=[]
    for member in plan['install_members']:
        spec=path_pin(C/member['path']);require({k:spec[k] for k in ('bytes','mode','sha256')}==member['post'],'final3 local fullbody/mode readback')
        readbacks.append(spec)
    guard(plan,journal);require(remote(journal)==commit,'remote main changed after final3 local readbacks')
    journal.update(status='public_and_local_install_verified',local_full_body_mode_readback=True,local_readback_path_count=3,installed_postimages=readbacks,
                   public_full_body_readback=True,public_full_body_mode_readback=True,private_cache_installed=False,raw_backend_installed=False,
                   program3_changed=True,native_changed=False,scientific_package_local_installation_performed=False,native_acceptance_or_program_completion_claimed=False)

def operation(args):
    run_dir=absolute(args.run_dir);require(run_dir.parent==D/'private','operation run directory scope');run_dir.mkdir(exist_ok=False)
    journal={'schema':'pr141-final-package-program3-operation-receipt/v1','actual_PID':os.getpid(),'UTC_start':utc(),'action':args.action,'transaction':FINAL_TRANSACTION,
             'plan_sha256':args.plan_sha,'source_sha256':digest(Path(__file__).read_bytes()),'review_sha256':args.review_sha,'children':[],'status':'starting',
             'auto_retry_performed':False,'fixture_only':False,'native_acceptance_or_program_completion_claimed':False}
    lock=D/'private/OPERATION_LOCK.json';owned_lock=None;lock_identity=None
    try:
        local_case_guard(lock);fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        try:
            identity=os.fstat(fd);lock_identity=(identity.st_dev,identity.st_ino)
            os.write(fd,canonical({'PID':os.getpid(),'UTC':utc(),'plan_sha256':args.plan_sha}));os.fsync(fd)
        finally:os.close(fd)
        owned_lock=pin(lock)
        plan=load_inputs(args.plan,args.plan_sha,args.review,args.review_sha)
        if args.action=='publish':publish(plan,journal,run_dir)
        else:install(plan,journal,run_dir,args.published_receipt,args.published_receipt_sha)
    except BaseException as error:
        journal.update(error_type=type(error).__name__,error=str(error)[:4096])
        if isinstance(error,JournalWriteFailure):journal['journal_write_failure']=error.journal_write_failure
        if journal.get('published_commit'):
            journal['failure_state']='public_published_local_installation_pending';journal['local_installation_pending']=True
        raise
    finally:
        children_safe=all(x.get('child_reaped') is True and x.get('process_group_empty') is True for x in journal['children'])
        journal['all_obtained_children_reaped_and_groups_empty']=children_safe
        if lock_identity is not None and children_safe:
            try:
                safe(lock);identity=lock.lstat();require((identity.st_dev,identity.st_ino)==lock_identity,'owned lock identity changed')
                if owned_lock is not None:check(lock,owned_lock)
                lock.unlink();journal['own_operation_lock_released']=True
            except BaseException as error:journal.update(own_operation_lock_released=False,lock_release_error=str(error)[:4096])
        elif lock_identity is not None:journal.update(own_operation_lock_released=False,lock_retained_for_unresolved_children=True)
        journal['UTC_end']=utc()
        try:dump(run_dir/'RECEIPT.json',journal)
        except BaseException as persistence_error:
            print(json.dumps({'receipt_persistence_failed':True,'PID':os.getpid(),'status':journal['status'],'original_error_type':journal.get('error_type'),
                              'unresolved_children':[x.get('PID') for x in journal['children'] if not x.get('child_reaped') or not x.get('process_group_empty')],'lock_released':journal.get('own_operation_lock_released'),
                              'journal_write_failure':getattr(persistence_error,'journal_write_failure',None),'installation_intents':journal.get('installation_intents',[]),
                              'owned_install_temps':journal.get('owned_install_temps',[]),'created_install_directories':journal.get('created_install_directories',[]),'replaced_paths':journal.get('replaced_paths',[])}))
            raise
    require(journal.get('own_operation_lock_released') is True,'owned operation lock release incomplete')
    print(json.dumps({'status':journal['status'],'receipt':str(run_dir/'RECEIPT.json'),'PID':os.getpid()}))

"""Source fragment for the later final publisher; contains no actual plan/gate."""

AUDIT_PREFIX='draft_pr_publication_program_20260930/audits/pr141_30003818/'
PACKAGE_PREFIX=AUDIT_PREFIX+'publication_package_v1/'
FINAL_SCHEMA='pr141-final-package-program3-overlay/v1'
FINAL_TRANSACTION='final_package_and_program_metadata'
FINAL_REVIEW_SCHEMA='pr141-final-package-program3-source-plan-review/v1'
GATE_PATH=A/'ROOT_ACTUAL_NATIVE_ACCEPTANCE_20261007.json'
RENDERER_PATH=A/'final_program3_renderer_source_preparation_20261007/render_program3_acceptance.py'
RENDERER_CONTRACT_PATH=A/'final_program3_renderer_source_preparation_20261007/CONTRACT.json'
ROLES={'source','builder_source','plan','review','publish','install','publication','tracker','sheet','merge','clean_package','mathematics','priority','original_manifest','full_postimage_inventory','full_local_inventory'}

def member_path(value):
    value=relative(value);parts=PurePosixPath(value).parts
    require(value in PROGRAM or value.startswith(AUDIT_PREFIX),'final overlay outside exact PR141/program3 scope')
    banned=('credential','secret','access_token','refresh_token','fullpaper','full_paper','fulltext','full_text')
    require(not any(part.startswith('.') or part.casefold().startswith(('tmp','temp')) or any(word in part.casefold() for word in banned) or part.casefold() in {'index','indexes','cache','caches'} for part in parts),'private/credential/temp/full-paper/index publication path')
    require(not value.casefold().endswith(('.sqlite','.sqlite3','.db','.pem','.p12','.key','.env','.tmp','.xz','.gz')),'forbidden raw cache/credential/temporary container')
    if value.casefold().endswith('.pdf'):require(value==PACKAGE_PREFIX+'brownian_first_visit.pdf','only the reviewed paper PDF may be selected')
    return value

def body_pin(spec):
    require(isinstance(spec,dict) and set(spec)=={'bytes','mode','sha256'},'exact body pin')
    require(type(spec['bytes']) is int and spec['bytes']>=0 and type(spec['mode']) is int and spec['mode']==420,'selected regular logical public0644 body, including an empty diff')
    sha_value(spec['sha256']);return spec

def logical_pin(spec):
    """Git nonexecutability is distinct from a captured source's actual0444 bits."""
    return {'bytes':spec['bytes'],'mode':420,'sha256':spec['sha256']}

def install_scope(remote_members,install_members):
    require(isinstance(remote_members,list) and isinstance(install_members,list),'explicit selected and installed lists')
    selected=[]
    for member in remote_members:
        path=member_path(member['path'])
        require(type(member['install']) is bool and member['install']==(path in PROGRAM),'only3 program paths can be locally installed')
        if member['install']:selected.append(member)
    require(len(selected)==3 and {m['path'] for m in selected}==PROGRAM and install_members==selected,'all and only3 explicit program installations')

def load_renderer(spec):
    require(spec['path']==str(RENDERER_PATH) and spec['sha256']==RENDERER_SOURCE_SHA,'exact sealed independently reviewed pure renderer required')
    body=read_pinned(spec);module=types.ModuleType('pr141_final_pure_renderer')
    exec(compile(body,str(RENDERER_PATH),'exec'),module.__dict__)
    return module

def manifest_sources(manifest):
    require(isinstance(manifest,dict) and manifest.get('schema')=='pr141-final-program3-postimages/v1','exact future rendered program3 manifest')
    require(manifest.get('preparation_only') is True and manifest.get('authoritative_before_final_transaction_acceptance') is False,'truthful not-yet-authoritative final proposal')
    require(all(manifest.get(k) is None for k in ('final_metadata_commit','final_metadata_actual_PID','final_metadata_actual_UTC','final_metadata_actual_readback')),'no invented future final commit/PID/time/readback')
    before,after=program_views(manifest)
    require(set(manifest['replay'])=={'context','contract','input_pins'},'complete pure replay inputs')
    require(manifest['contract_pin']['path']==str(RENDERER_CONTRACT_PATH) and manifest['contract_pin']['sha256']==RENDERER_CONTRACT_SHA,'exact sealed renderer CONTRACT.json')
    contract=native_json(read_pinned(manifest['contract_pin']));small=manifest['replay']['contract']
    require(set(small)=={'known_role_pins','previous140_final_acceptance','current_preimages'} and small=={k:contract[k] for k in small},'exact checked small renderer input contract binding')
    require(set(small['current_preimages'])=={Path(path).name for path in PROGRAM},'complete original3 sealed renderer baseline')
    for path,spec in before.items():
        old=small['current_preimages'][Path(path).name]
        require(old['path']==str(C/path) and logical_pin(spec)=={k:old[k] for k in ('bytes','mode','sha256')},'all3 immutable captured before bodies equal sealed original physical baseline')
    specs=[manifest['source'],manifest['genuinegate'],manifest['freshgoal'],manifest['contract_pin'],*before.values(),*after.values(),*manifest['replay']['input_pins']]
    found={}
    for spec in specs:
        full_pin(spec)
        if spec['path'] in found:require(found[spec['path']]==spec,'conflicting input pin alias')
        found[spec['path']]=spec
    return found

def program_views(manifest):
    views=[]
    for role in ('preimages','postimages'):
        specs=manifest[role];require(isinstance(specs,list) and len(specs)==3,'exact3 full pin list')
        view={}
        for spec in specs:
            full_pin(spec);path='draft_pr_publication_program_20260930/'+Path(spec['path']).name
            require(path in PROGRAM and path not in view,'unique exact program3 body filename')
            if role=='preimages':require(spec['path']!=str(C/path),'preimage inputs must be immutable captured before bodies, not overwritten local destinations')
            view[path]=spec
        require(set(view)==PROGRAM,'complete exact3 filenames');views.append(view)
    return tuple(views)

def read_postimage(member):
    storage=member['storage'];require(set(storage)=={'encoding','pin'} and storage['pin']['path']==member['source'],'exact selected storage custody')
    require(type(storage['pin']['mode']) is int and storage['pin']['mode'] in (292,420),'actual sealed0444 or prepared0644 storage mode')
    return decode_storage(read_pinned(storage['pin']),storage['encoding'],member['post'])

def native_closure(plan,renderer,program):
    require(plan['native_gate']['path']==str(GATE_PATH) and program['genuinegate']==plan['native_gate'],'exact actual closing gate role binding')
    gate=native_json(read_pinned(plan['native_gate']));require(set(gate['evidence_pins'])==ROLES,'exact16 actual evidence roles')
    specs=manifest_sources(program)
    for spec in gate['evidence_pins'].values():
        full_pin(spec)
        if spec['path'] in specs:require(specs[spec['path']]==spec,'renderer/gate evidence pin conflict')
        specs[spec['path']]=spec
    bodies={path:{'body':read_pinned(spec),'mode':spec['mode']} for path,spec in specs.items()}
    checked=renderer.validate_gate(plan['native_gate'],bodies,program['replay']['contract'])
    require(checked==gate and gate['native_commit']==plan['base_commit'],'actual native commit must be final sole parent/base')
    native_plan=native_json(bodies[gate['evidence_pins']['plan']['path']]['body'])
    require(len(native_plan['install_members'])==32 and len(native_plan['remote_members'])==18,'exact completed native32/18')
    expected={m['path']:m['post'] for m in native_plan['install_members']}
    require(len(expected)==32 and plan['preserved_native32']==expected,'exact32 immutable native installed bodies')
    for name in expected:require(name not in PROGRAM and not name.startswith(AUDIT_PREFIX),'native protected family is outside final overlay')
    require(program['source']==plan['renderer_source'],'same exact independently prepared renderer')
    before,after=program_views(program)
    pre={Path(path).name:bodies[spec['path']]['body'] for path,spec in before.items()}
    rendered=renderer.render(pre,plan['native_gate'],program['freshgoal'],bodies,program['replay']['context'],program['replay']['contract'])
    require(set(rendered)=={Path(path).name for path in PROGRAM},'pure renderer exact3 result')
    for path,spec in after.items():require(rendered[Path(path).name]==read_pinned(spec),'full exact renderer postimage mismatch')
    return gate,native_plan,specs

def validate_members(plan,selection,program,gate,native_plan):
    require(selection.get('schema')=='pr141-final-selected-public-inventory/v1' and selection.get('owner')=='ROOT' and selection.get('fixture_only') is False and type(selection.get('actual_ROOT_PID')) is int and selection['actual_ROOT_PID']>0,'concrete future ROOT selected inventory required')
    require(selection.get('all_selected_bodies_safe_for_publication') is True,'actual selected-public curation required')
    require(selection['native_gate']==plan['native_gate'] and selection['program3_manifest']==plan['program3_manifest'],'selected inventory binds exact native gate/rendered3')
    require(selection['members']==plan['remote_members'],'no inferred broad or unreviewed member selection')
    members=plan['remote_members'];require(isinstance(members,list) and 58<=len(members)<=2048,'bounded selected55package+3program family')
    install_scope(members,plan['install_members'])
    before,after=program_views(program)
    seen=set();folded=set();program_members={};classes={'package','whole_review','prepublication','service','native_closing','source_preparation','research_log','program_metadata'}
    for m in members:
        require(set(m)=={'path','source','origin','storage','post','post_blob','remote_pre','local_pre','install','category','publication_reason'},'exact declared selected member schema')
        path=member_path(m['path']);require(path not in seen and path.casefold() not in folded,'duplicate selected path/case alias');seen.add(path);folded.add(path.casefold())
        require(m['category'] in classes and isinstance(m['publication_reason'],str) and m['publication_reason'].strip(),'meaningful explicit publication classification')
        body_pin(m['post']);tree_oid(m['post_blob']);body=read_postimage(m)
        blob=digest_git_blob(body);require(blob==m['post_blob'],'selected exact Git blob computed from full decoded body')
        if m['origin'] is not None:
            origin=read_pinned(m['origin']);require(origin==body,'published mode copy must preserve full original body')
        require(type(m['install']) is bool and m['install']==(path in PROGRAM),'exactly program3 may be locally installed')
        if path in PROGRAM:
            require(m['category']=='program_metadata' and m['origin'] is None and m['local_pre'] is not None and m['post']==logical_pin(after[path]) and m['source']==after[path]['path'],'actual3 rendered whole bytes with explicit installed0644 mode')
            require(m['local_pre']==logical_pin(before[path]),'exact current3 local preimage bodies/0644 mode, separately from captured source permissions')
            require(m['remote_pre'] is not None and {k:m['remote_pre'][k] for k in ('bytes','mode','sha256')}==m['local_pre'],'whole fresh main3 must equal current physical preimages')
            program_members[path]=m
        else:require(m['local_pre'] is None,'audit/package paths are public-only; no local overwrite')
        if m['remote_pre'] is not None:
            require(set(m['remote_pre'])=={'bytes','mode','sha256','Git_blob'},'complete selected remote preimage pin');body_pin({k:m['remote_pre'][k] for k in ('bytes','mode','sha256')});tree_oid(m['remote_pre']['Git_blob'])
    require(set(program_members)==PROGRAM and plan['install_members']==[m for m in members if m['install']],'all and only explicit program3 local installs')
    package_pin=selection['package_manifest'];require(package_pin['path']==str(A/'publication_package_v1/PACKAGE_MANIFEST.json'),'exact final scientific package manifest path')
    package=native_json(read_pinned(package_pin));clean=native_json(read_pinned(gate['evidence_pins']['clean_package']))
    require(package_pin['sha256']==clean['package_manifest_sha256'] and package['schema']=='pr141-publication-package-manifest/v1','genuinely final clean-reviewed package manifest')
    require(isinstance(package['files'],dict) and len(package['files'])==54 and package['upload_files']==['brownian_first_visit.pdf','brownian_first_visit_support.zip'],'actual54 scientific package family')
    expected_package={PACKAGE_PREFIX+name for name in package['files']}|{PACKAGE_PREFIX+'PACKAGE_MANIFEST.json'}
    require(expected_package<=seen,'all55 package working bodies/manifests must be selected')
    bypath={m['path']:m for m in members}
    for name,spec in package['files'].items():require(bypath[PACKAGE_PREFIX+name]['post']==spec,'all54 package member pins preserved exactly')
    require(bypath[PACKAGE_PREFIX+'PACKAGE_MANIFEST.json']['post']=={k:package_pin[k] for k in ('bytes','mode','sha256')},'exact final self-excluded whole package manifest')
    original=native_json(read_pinned(gate['evidence_pins']['original_manifest']));require(original['head']==ORIGINAL_HEAD and len(original['files'])==20,'frozen original20 identity')
    protected_archive={AUDIT_PREFIX+'original_submitted_attempt/'+m['path']:{k:m[k] for k in ('bytes','mode','sha256')} for m in original['files']}
    for path,spec in protected_archive.items():
        if path in bypath:require(bypath[path]['post']==spec,'selected original archive body or mode changed')
    changed={m['path'] for m in members if m['remote_pre'] is None or m['remote_pre']['Git_blob']!=m['post_blob']}
    require(changed and set(plan['expected_changed_paths'])==changed and len(plan['expected_changed_paths'])==len(changed),'exact selected remote changed-set, including unchanged publication members')
    preserved=plan['preserved_remote_inputs'];require(isinstance(preserved,list) and len({m['path'] for m in preserved})==len(preserved),'unique remote preservation dependency list')
    required=set(plan['preserved_native32'])|READONLY_PATHS
    require({m['path'] for m in preserved}==required,'all native32 plus four readonly dependencies must be protected in remote tree')
    for item in preserved:
        require(set(item)=={'path','bytes','mode','sha256','Git_blob'},'complete preserved remote blob pin');body_pin({k:item[k] for k in ('bytes','mode','sha256')});tree_oid(item['Git_blob'])
        if item['path'] in plan['preserved_native32']:require({k:item[k] for k in ('bytes','mode','sha256')}==plan['preserved_native32'][item['path']],'preserved remote native member changed')

def digest_git_blob(body):return hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()

def protection_contract(plan,gate):
    protected={x['path']:x for x in plan['protected']};absences=set(plan['protected_absences']);dirs={x['path']:x for x in plan['protected_directories']}
    require(len(protected)==len(plan['protected']) and len(absences)==len(plan['protected_absences']) and len(dirs)==len(plan['protected_directories']) and not set(protected)&absences,'unique current protected resources')
    required_git={str(root/'.git'/name) for root in (R,C) for name in GIT_FILES}
    require(required_git<=set(protected)|absences,'all current real Git main/ref/index/HEAD/config/FETCH controls')
    required_locks={str(root/'.git'/name) for root in (R,C) for name in GIT_LOCKS};require(required_locks<=absences,'all real Git writer locks stay absent')
    for root in (R,C):require(str(root/'.git/refs') in dirs or str(root/'.git/refs') in absences,'closed complete current refs directory custody')
    cache=str(R/'unsolved_math_prioritization/cache/catalog.sqlite');require(cache in protected and protected[cache]['bytes']==157691904,'original157MB cache full stream pin; never copied or executed')
    require({str(C/'unsolved_math_prioritization'/name) for name in ('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}<=absences,'checkout backend/cache absences preserved')
    for path,spec in plan['preserved_native32'].items():require(protected.get(str(C/path))=={'path':str(C/path),**spec},'all current32 installed native/canonical full pins preserved')
    archive=native_json(read_pinned(gate['evidence_pins']['original_manifest']))
    for m in archive['files']:
        path=str(A/'original_submitted_attempt'/m['path']);require(protected.get(path)=={'path':path,**{k:m[k] for k in ('bytes','mode','sha256')}},'all original20 archive bodies protected')
    require(str(C/ATTEMPT_PREFIX.rstrip('/')) in dirs,'closed current canonical24 directory required')
    require(str(A/'original_submitted_attempt') in dirs,'closed original archive directory required')
    require(not ({str(C/path) for path in PROGRAM}&set(protected)),'only program3 protected exclusions are writable')
    require({str(R/path) for path in PROGRAM}<=set(protected)|absences,'foreign root program3 baseline stays immutable')

def validate_plan(plan):
    require(isinstance(plan,dict) and plan['schema']==FINAL_SCHEMA and plan['transaction']==FINAL_TRANSACTION,'sole final package/program metadata transaction')
    require(plan.get('owner')=='ROOT' and plan.get('fixture_only') is False and plan.get('action_executed') is False and type(plan.get('actual_preparer_PID')) is int and plan['actual_preparer_PID']>0,'concrete ROOT actual-input proposal, never a fixture or performed action')
    require(plan['source_sha256']==digest(Path(__file__).read_bytes()),'reviewed running final source SHA')
    tree_oid(plan['base_commit']);tree_oid(plan['R_HEAD']);tree_oid(plan['C_HEAD'])
    require(plan['git_executable']['path']==G and plan['gh_executable']['path']==GH,'fixed approved Git/GH executables')
    full_pin(plan['git_executable']);full_pin(plan['gh_executable'])
    renderer=load_renderer(plan['renderer_source']);program=native_json(read_pinned(plan['program3_manifest']));selection=native_json(read_pinned(plan['selection_manifest']))
    gate,native_plan,specs=native_closure(plan,renderer,program)
    validate_members(plan,selection,program,gate,native_plan);protection_contract(plan,gate)
    require(isinstance(plan['commit_message'],str) and plan['commit_message'].strip() and '\0' not in plan['commit_message'],'explicit reviewed final commit message')
    return gate

def load_inputs(plan_path,plan_sha,review_path,review_sha):
    body=absolute(plan_path).read_bytes();require(digest(body)==sha_value(plan_sha),'out-of-band exact final plan SHA');plan=native_json(body);require(body==canonical(plan),'canonical exact final plan body')
    review_body=absolute(review_path).read_bytes();require(digest(review_body)==sha_value(review_sha),'out-of-band whole independent final review SHA');review=native_json(review_body)
    require(review['schema']==FINAL_REVIEW_SCHEMA and review['verdict']=='PASS' and review['mandatory_findings']==[] and review['actual_review'] is True and review['fixture_only'] is False,'fresh independent actual final source/data/inventory/plan PASS')
    require(type(review['actual_reviewer_PID']) is int and review['actual_reviewer_PID']>0 and isinstance(review['reviewer_identity'],str) and review['reviewer_identity'],'actual independent reviewer identity')
    for key in ('native_gate_authenticated','renderer_full3_replayed','selected_inventory_full_bodies_and_modes_authenticated','all_foreign_tree_preservation_verified','current_protection_binding_authenticated'):require(review[key] is True,'actual final review completeness: '+key)
    require(review['source_sha256']==plan['source_sha256'] and review['plan_sha256']==plan_sha and review['native_gate_sha256']==plan['native_gate']['sha256'] and review['renderer_source_sha256']==plan['renderer_source']['sha256'] and review['program3_manifest_sha256']==plan['program3_manifest']['sha256'] and review['selection_manifest_sha256']==plan['selection_manifest']['sha256'],'review binds every whole final authority input')
    require(type(review['local_install_path_count']) is int and review['local_install_path_count']==3 and type(review['remote_selected_path_count']) is int and review['remote_selected_path_count']==len(plan['remote_members']) and type(review['remote_changed_path_count']) is int and review['remote_changed_path_count']==len(plan['expected_changed_paths']),'review binds dynamic public inventory and exact3 install scope')
    validate_plan(plan);return plan

def guard(plan,journal):
    validate_plan(plan)
    for spec in plan['protected']:full_pin(spec)
    for path in plan['protected_absences']:require(not local_case_guard(path).exists(),'protected current absence changed')
    for spec in plan['protected_directories']:closed_directory(spec)
    for root,expected in ((R,plan['R_HEAD']),(C,plan['C_HEAD'])):
        values=git(['rev-parse','HEAD','refs/heads/main'],journal,root=root).decode().splitlines();require(values==[expected,expected],'real main/HEAD drift')
    installed=set(journal.get('installed',[]))
    for m in plan['install_members']:check(local_case_guard(C/m['path']),m['post'] if m['path'] in installed else m['local_pre'])

def local_preimage_guard(plan):
    for member in plan['install_members']:check(local_case_guard(C/member['path']),member['local_pre'])

def check_remote_preimages(plan,journal):
    git(['cat-file','-e',plan['base_commit']+'^{commit}'],journal)
    for member in plan['remote_members']:
        record=git(['ls-tree','-z',plan['base_commit'],'--',member['path']],journal);require(record==expected_tree_record(member),'complete selected remote preimage mode/path/blob')
        spec=member['remote_pre']
        if spec is not None:
            body=git(['cat-file','blob',spec['Git_blob']],journal);require(len(body)==spec['bytes'] and digest(body)==spec['sha256'],'selected full remote preimage')
    for member in plan['preserved_remote_inputs']:
        record=git(['ls-tree','-z',plan['base_commit'],'--',member['path']],journal);require(record==('100644 blob '+member['Git_blob']+'\t'+member['path']+'\0').encode(),'current preserved dependency tree record')
        body=git(['cat-file','blob',member['Git_blob']],journal);require(len(body)==member['bytes'] and digest(body)==member['sha256'],'current native/readonly remote body drift')

def main():
    parser=argparse.ArgumentParser(description=__doc__);actions=parser.add_subparsers(dest='action',required=True)
    for action in ('publish','install'):
        sub=actions.add_parser(action);sub.add_argument('--plan',required=True);sub.add_argument('--plan-sha',required=True);sub.add_argument('--review',required=True);sub.add_argument('--review-sha',required=True);sub.add_argument('--run-dir',required=True)
        if action=='install':sub.add_argument('--published-receipt',required=True);sub.add_argument('--published-receipt-sha',required=True)
    args=parser.parse_args();operation(args)

if __name__=='__main__':main()

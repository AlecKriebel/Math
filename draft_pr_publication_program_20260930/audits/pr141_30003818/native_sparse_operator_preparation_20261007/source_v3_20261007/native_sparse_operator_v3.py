"""PR141 exact18 remote publication and separate exact32 local installation.

Source preparation only until ROOT supplies actual authenticated final roles,
a current protection binding, the exact expected plan SHA and independent PASS.
No checkout, index, ref synchronization, cache, backend CLI or program3 transaction.
Missing base objects may be acquired by one guarded fixed-OID object-only fetch.
"""
from pathlib import Path, PurePosixPath
import argparse, base64, datetime, hashlib, json, lzma, os, signal, stat, subprocess, sys, time, tempfile, types, uuid

R = Path('/Users/alec/Documents/Math')
C = R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A = C/'draft_pr_publication_program_20260930/audits/pr141_30003818'
D = A/'native_sparse_operator_preparation_20261007'
BUILDER = A/'native_data_adapter_preparation_20261007/low_memory_v2_20261007/native_data_builder_v2.py'
BUILDER_SOURCE_SHA = '0e1e77c410b17186676a175f67413b2fe0e1cfa4255a2f48110021f35933fb93'
G = '/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
URL = 'https://github.com/AlecKriebel/Math.git'
K, CODE = '30003818', 'OWR-16164-012'
ORIGINAL_HEAD = '523247e3246a5f44c7b0089074bb304c1f642bd0'
ORIGINAL_MANIFEST_SHA = 'c1e54b286a8229bb99051341815937c53a8203008a21bf900525d43d991cfe07'
ATTEMPT_PREFIX = 'unsolved_math_prioritization/attempts/30003818/'
BACKEND = ('assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','QUEUE.md')
CANONICAL_METADATA = ('assessment.json','HISTORICAL_DESK_ASSESSMENT.json','PUBLICATION_EVIDENCE.json','ACCEPTANCE_EVIDENCE.json','README.md','RESEARCH_LOG.md')
REPAIRS = ('verify.py','review/author_replay/verify.py','frozen_artifacts.json','review/review_summary.json')
REMOTE_PATHS = {'unsolved_math_prioritization/'+n for n in BACKEND}|{ATTEMPT_PREFIX+n for n in CANONICAL_METADATA+REPAIRS}
READONLY_PATHS = {'unsolved_math_prioritization/'+n for n in ('queue.py','manifest.json','policy.json','SHORTLIST.md')}
PROGRAM = {'draft_pr_publication_program_20260930/'+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
GIT_FILES = ('index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main')
GIT_LOCKS = ('index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock','config.lock','FETCH_HEAD.lock')
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

def read_postimage(member):
    storage=member['storage'];require(set(storage)=={'encoding','pin'} and storage['pin']['path']==member['source'],'exact selected storage custody')
    require(storage['pin']['mode']==420,'prepared source storage mode420')
    return decode_storage(read_pinned(storage['pin']),storage['encoding'],member['post'])

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

def original_paths(request,bodies):
    manifest_body=bodies[request['original_manifest']]
    require(digest(manifest_body)==ORIGINAL_MANIFEST_SHA,'immutable original20 manifest SHA')
    manifest=native_json(manifest_body)
    require(manifest['head']==ORIGINAL_HEAD and len(manifest['files'])==20,'original20 identity')
    names=[relative(x['path']) for x in manifest['files']]
    require(len(set(names))==len(names) and len({n.casefold() for n in names})==20,'original20 unique paths')
    return {ATTEMPT_PREFIX+n for n in names}

def validate_inventory(remote_members,install_members,unchanged):
    require(isinstance(remote_members,list) and isinstance(install_members,list) and isinstance(unchanged,list),'declared scoped member lists')
    for members,expected in [(remote_members,18),(install_members,32)]:
        names=[relative(m['path']) for m in members]
        require(len(names)==expected and len(set(names))==expected and len({p.casefold() for p in names})==expected,'exact unique scoped member count')
        require(all(m['post']['mode']==420 for m in members),'all selected postimages mode100644')
    remote_set={m['path'] for m in remote_members};local_set={m['path'] for m in install_members}
    require(remote_set==REMOTE_PATHS and remote_set<=local_set,'exact remote18 family')
    require(len(unchanged)==14 and len(set(unchanged))==14 and set(unchanged)==local_set-remote_set and all(p.startswith(ATTEMPT_PREFIX) for p in unchanged),'exact14 remote-unchanged local originals')
    require(not (remote_set|local_set)&PROGRAM,'program3 requires later separate actual acceptance')

def protection_contract(plan):
    protected=plan['protected'];absences=plan['protected_absences']
    require(isinstance(protected,list) and isinstance(absences,list),'current protection inventories')
    present=[p['path'] for p in protected]
    require(len(present)==len(set(present)) and len(absences)==len(set(absences)) and not set(present)&set(absences),'unique protected resources')
    all_paths=present+absences
    require(len(all_paths)==len({p.casefold() for p in all_paths}),'protected resource case alias')
    for value in absences:absolute(value)
    required={str(root/'.git'/name) for root in (R,C) for name in GIT_FILES+GIT_LOCKS}
    required|={str(R/'unsolved_math_prioritization'/name) for name in BACKEND+('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}
    required|={str(root/name) for root in (R,C) for name in PROGRAM}
    required|={str(C/'unsolved_math_prioritization'/name) for name in ('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}
    require(required<=set(all_paths),'complete current R/C Git, R backend/cache and program3 baselines')
    require({str(root/'.git'/name) for root in (R,C) for name in GIT_LOCKS}<=set(absences),'all real Git writer locks must stay absent')
    require({str(C/'unsolved_math_prioritization'/name) for name in ('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}<=set(absences),'C raw backend/cache remains absent')
    require({str(R/'unsolved_math_prioritization'/name) for name in BACKEND+('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}<=set(present),'R backend/cache must be pinned current bodies')
    require({str(C/name) for name in PROGRAM}<=set(present),'all current C program3 bodies pinned; R observed presence/absence protected')
    installing={str(C/m['path']) for m in plan['install_members']}
    require(not installing&set(all_paths),'installed paths cannot be immutable protected resources')
    dirs=[x['path'] for x in plan['protected_directories']]
    require(len(dirs)==len(set(dirs)) and len(dirs)==len({p.casefold() for p in dirs}),'unique protected directories')
    required_dirs={str(root/'.git/refs') for root in (R,C)}|{str(R/'unsolved_math_prioritization/cache'),str(A/'original_submitted_attempt'),str(A/'publication_package_v1'),plan['postimage_root']}
    require(required_dirs<=set(dirs),'closed current refs/cache/archive/package/prepared-postimage custody')
    for directory in dirs:
        absolute(directory)
        require(not any(Path(p)==Path(directory) or Path(directory) in Path(p).parents for p in installing),'protected directory intersects local installation')
        require(Path(directory)!=D/'private' and not (D/'private').is_relative_to(Path(directory)),'operation receipts cannot live inside protected directory')
    archive_spec=next(x for x in plan['protected_directories'] if x['path']==str(A/'original_submitted_attempt'))
    manifest=native_json(read_pinned(plan['original_manifest']))
    require(plan['original_manifest']['path']==str(A/'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json') and plan['original_manifest']['sha256']==ORIGINAL_MANIFEST_SHA,'original manifest path/pin')
    expected={x['path']:{k:x[k] for k in ('bytes','mode','sha256')} for x in manifest['files']}
    require({x['relative']:{k:x[k] for k in ('bytes','mode','sha256')} for x in archive_spec['files']}==expected,'exact20 immutable archived bodies protected')

def load_builder(spec):
    require(spec['path']==str(BUILDER) and spec['sha256']==BUILDER_SOURCE_SHA,'reviewed PR141 adapter path/source SHA')
    body=read_pinned(spec);module=types.ModuleType('pr141_reviewed_pure_builder')
    module.__file__=spec['path'];exec(compile(body,spec['path'],'exec'),module.__dict__)
    require(callable(module.build_verified),'pure builder entry point')
    return module

def proposal(request_spec,binding_spec):
    request_body=read_pinned(request_spec);binding_body=read_pinned(binding_spec)
    request=native_json(request_body);binding=native_json(binding_body)
    fields={'schema','request_sha256','builder_source','input_paths','postimage_root','postimage_paths','local_preimages','base_commit','R_HEAD','C_HEAD','git_executable','gh_executable','protected','protected_absences','protected_directories','commit_message'}
    require(set(binding)==fields and binding['schema']=='pr141-current-native-operator-binding/v1','explicit current actual binding schema')
    require(binding['request_sha256']==request_spec['sha256'] and request['mode']=='actual','actual request/binding whole SHA')
    require(set(binding['input_paths'])==set(request['input_pins']),'exact input source set')
    input_specs={};bodies={}
    for name,path in binding['input_paths'].items():
        spec=path_pin(path);expected=request['input_pins'][name]
        require(spec['bytes']==expected['bytes'] and spec['sha256']==expected['sha256'],'whole declared request input pin')
        input_specs[name]=spec;bodies[name]=read_pinned(spec)
    builder=load_builder(binding['builder_source']);result=builder.build_verified(request_body,bodies,request_spec['sha256'])
    require(result['fixture'] is False and result['status']=='PROPOSED_DATA_ONLY_NOT_NATIVE_ACCEPTANCE','actual proposal, never fixture authority')
    original_set=original_paths(request,bodies)
    local_set=original_set|REMOTE_PATHS
    require(set(result['outputs'])==REMOTE_PATHS and set(result['local_installation_inventory'])==local_set and len(local_set)==32,'builder exact18/exact32 scope')
    require(set(binding['postimage_paths'])==REMOTE_PATHS and set(binding['local_preimages'])==local_set,'complete post/local preimage source inventory')
    post_root=absolute(binding['postimage_root']);require(D/'private' in post_root.parents,'prepared postimage root scope')
    fresh=native_json(bodies[request['fresh_main']]);merge=native_json(bodies[request['merge']])
    base=tree_oid(binding['base_commit']);require(base==fresh['MAIN_commit']==fresh['direct_remote_MAIN'],'actual fresh-main request/base binding')
    tree=native_json(bodies[fresh['scoped_tree']])
    require(set(tree)==local_set,'actual complete32 scoped remote preimages')
    members={};remote_members=[]
    for path in sorted(local_set):
        body=result['local_installation_inventory'][path];remote_pre=tree[path]
        post={'bytes':len(body),'mode':420,'sha256':digest(body)}
        if path in REMOTE_PATHS:
            selected=binding['postimage_paths'][path]
            if isinstance(selected,str):storage={'encoding':'raw','pin':path_pin(selected)}
            else:
                require(isinstance(selected,dict) and set(selected)=={'encoding','pin'} and selected['encoding'] in ('raw','xz'),'explicit prepared postimage raw/xz storage')
                full_pin(selected['pin']);storage=selected
            source=absolute(storage['pin']['path'])
            require(source==post_root/(path+('.xz' if storage['encoding']=='xz' else '')),'exact prepared storage path')
        else:
            name=path[len(ATTEMPT_PREFIX):];label=request['original_files'][name]
            source=absolute(binding['input_paths'][label]);require(source==A/'original_submitted_attempt'/name,'unchanged original direct archive source')
            storage={'encoding':'raw','pin':path_pin(source)}
        require(storage['pin']['mode']==420 and decode_storage(read_pinned(storage['pin']),storage['encoding'],post)==body,'prepared decoded postimage byte/mode equality')
        pre=binding['local_preimages'][path]
        if path.startswith(ATTEMPT_PREFIX):require(pre is None,'complete32 route requires current absent canonical directory')
        else:
            require(pre is not None and set(pre)=={'bytes','mode','sha256'},'exact eight current local preimages')
            require(type(pre['bytes']) is int and pre['bytes']>=0 and type(pre['mode']) is int and 0<=pre['mode']<=0o777,'typed local preimage bytes/mode')
            sha_value(pre['sha256'])
            check(C/path,pre)
        blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
        member={'path':path,'source':str(source),'storage':storage,'post':post,'post_blob':blob,'remote_pre':remote_pre,'local_pre':pre}
        members[path]=member
        if path in REMOTE_PATHS:
            require(remote_pre is None or remote_pre['sha256']!=post['sha256'],'all18 declared remote changes must differ')
            remote_members.append(member)
        else:require(remote_pre=={**post,'Git_blob':blob},'all14 installed originals are remote byte/mode unchanged')
    require(not local_case_guard(C/ATTEMPT_PREFIX.rstrip('/')).exists(),'canonical directory must currently be absent')
    for path in original_set:
        label=request['original_files'][path[len(ATTEMPT_PREFIX):]]
        require(binding['input_paths'][label]==str(A/'original_submitted_attempt'/path[len(ATTEMPT_PREFIX):]),'all20 original bodies read from immutable archive')
    require(binding['input_paths'][request['original_manifest']]==str(A/'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json'),'original manifest direct custody')
    for spec in input_specs.values():require(spec['path'] not in {str(C/p) for p in local_set},'input custody cannot be replaced by local installation')
    message=binding['commit_message'];require(isinstance(message,str) and K in message and message.strip()==message and '\0' not in message,'scoped commit message')
    plan={'schema':'pr141-native-sparse-main-overlay/v1','transaction':'native_acceptance','original_head':ORIGINAL_HEAD,'source_sha256':digest(Path(__file__).read_bytes()),
          'builder_source':binding['builder_source'],'request':request_spec,'binding':binding_spec,'input_sources':input_specs,
          'original_manifest':input_specs[request['original_manifest']],'base_commit':base,'PR141_merge':{'original_head':ORIGINAL_HEAD,'commit':tree_oid(merge['merge_commit']),'merged_at':merge['merged_at']},
          'R_HEAD':tree_oid(binding['R_HEAD']),'C_HEAD':tree_oid(binding['C_HEAD']),'git_executable':binding['git_executable'],'gh_executable':binding['gh_executable'],
          'protected':binding['protected'],'protected_absences':binding['protected_absences'],'protected_directories':binding['protected_directories'],'postimage_root':str(post_root),
          'remote_members':remote_members,'install_members':[members[p] for p in sorted(members)],'expected_changed_paths':sorted(REMOTE_PATHS),
          'remote_unchanged_canonical_paths':result['remote_unchanged_canonical_paths'],'readonly_remote_inputs':[],
          'canonical_directory_initially_absent':True,'original_effort':'1/5','original_author_turn_ledger_present':True,'original_native_transition_ledger_present':False,
          'new_central_proof_search_turns':0,'native_acceptance_or_program_completion_claimed':False,'commit_message':message}
    for path,label in sorted(request['readonly'].items()):
        body=bodies[label];plan['readonly_remote_inputs'].append({'path':path,'bytes':len(body),'sha256':digest(body),'mode':420,'Git_blob':hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()})
    validate_inventory(plan['remote_members'],plan['install_members'],plan['remote_unchanged_canonical_paths']);protection_contract(plan)
    full_pin(plan['git_executable']);full_pin(plan['gh_executable'])
    require(plan['git_executable']['path']==G and plan['gh_executable']['path']==GH,'exact reviewed executable paths')
    for spec in plan['protected']:full_pin(spec)
    for path in plan['protected_absences']:require(not local_case_guard(path).exists(),'current protected absence changed')
    for spec in plan['protected_directories']:closed_directory(spec)
    return plan

def guard(plan,journal):
    require(digest(Path(__file__).read_bytes())==plan['source_sha256'],'running source changed')
    for spec in [plan['builder_source'],plan['request'],plan['binding'],*plan['input_sources'].values(),plan['git_executable'],plan['gh_executable'],*plan['protected']]:full_pin(spec)
    for member in plan['install_members']:read_postimage(member)
    for path in plan['protected_absences']:require(not local_case_guard(path).exists(),'protected absence changed')
    for spec in plan['protected_directories']:closed_directory(spec)
    for root,expected in [(R,plan['R_HEAD']),(C,plan['C_HEAD'])]:
        values=git(['rev-parse','HEAD','refs/heads/main'],journal,root=root).decode().splitlines()
        require(values==[expected,expected],'R/C real main and HEAD changed')
    provider=native_json(run([GH,'api','repos/AlecKriebel/Math/pulls/141'],journal))
    merge=plan['PR141_merge']
    require(provider['number']==141 and provider['state']=='closed' and provider['merged'] is True and provider['head']['sha']==ORIGINAL_HEAD and provider['base']['ref']=='main' and provider['merge_commit_sha']==merge['commit'] and provider['merged_at']==merge['merged_at'],'actual original-head merge changed')

def load_inputs(plan_path,plan_sha,review_path,review_sha):
    sha_value(plan_sha);sha_value(review_sha)
    plan_body=absolute(plan_path).read_bytes();require(digest(plan_body)==plan_sha,'explicit expected plan SHA')
    plan=native_json(plan_body)
    require(plan['schema']=='pr141-native-sparse-main-overlay/v1' and plan['transaction']=='native_acceptance','sole PR141 scoped transaction')
    require(plan['source_sha256']==digest(Path(__file__).read_bytes()),'reviewed running source SHA')
    review_body=absolute(review_path).read_bytes();require(digest(review_body)==review_sha,'independent review whole SHA')
    review=native_json(review_body)
    require(review['schema']=='pr141-native-sparse-operator-source-plan-review/v1' and review['verdict']=='PASS' and review['mandatory_findings']==[] and review['actual_review'] is True and review['actual_data_inputs_authenticated'] is True and review['raw_publication_tracker_original_merge_roles_authenticated'] is True,'fresh independent actual source/data/plan PASS')
    require(review['source_sha256']==plan['source_sha256'] and review['builder_source_sha256']==plan['builder_source']['sha256'] and review['plan_sha256']==plan_sha and review['request_sha256']==plan['request']['sha256'] and review['binding_sha256']==plan['binding']['sha256'],'review binds exact source/adapter/actualrequest/currentbinding/plan')
    require(type(review['actual_reviewer_PID']) is int and review['actual_reviewer_PID']>0 and isinstance(review['reviewer_identity'],str) and review['reviewer_identity'],'actual independent reviewer identity')
    require(review['remote_changed_path_count']==18 and type(review['remote_changed_path_count']) is int and review['local_install_path_count']==32 and type(review['local_install_path_count']) is int,'reviewed separate exact scopes')
    replay=proposal(plan['request'],plan['binding'])
    require(canonical(plan)==plan_body==canonical(replay),'exact deterministic actualrequest-dependent plan')
    return plan

def expected_tree_record(member,post=False):
    spec=member['post'] if post else member['remote_pre']
    if spec is None:return b''
    require(spec['mode']==420,'scoped public body must mode100644')
    blob=member['post_blob'] if post else spec['Git_blob']
    tree_oid(blob)
    return ('100644 blob '+blob+'\t'+member['path']+'\0').encode()

def check_remote_preimages(plan,journal):
    git(['cat-file','-e',plan['base_commit']+'^{commit}'],journal)
    git(['merge-base','--is-ancestor',plan['PR141_merge']['commit'],plan['base_commit']],journal)
    for member in plan['install_members']:
        record=git(['ls-tree','-z',plan['base_commit'],'--',member['path']],journal)
        require(record==expected_tree_record(member),'complete32 remote preimage mode/path/blob')
        spec=member['remote_pre']
        if spec is not None:
            body=git(['cat-file','blob',spec['Git_blob']],journal)
            require(len(body)==spec['bytes'] and digest(body)==spec['sha256'],'complete scoped remote fullbody preimage')
    require({m['path'] for m in plan['readonly_remote_inputs']}==READONLY_PATHS,'exact readonly remote dependencies')
    for member in plan['readonly_remote_inputs']:
        record=git(['ls-tree','-z',plan['base_commit'],'--',member['path']],journal)
        require(record==('100644 blob '+member['Git_blob']+'\t'+member['path']+'\0').encode(),'readonly dependency mode/path/blob')
        body=git(['cat-file','blob',member['Git_blob']],journal)
        require(len(body)==member['bytes'] and digest(body)==member['sha256'],'readonly dependency fullbody')

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

def local_preimage_guard(plan):
    require(not local_case_guard(C/ATTEMPT_PREFIX.rstrip('/')).exists(),'reviewed canonical directory absent preimage changed')
    for member in plan['install_members']:
        path=local_case_guard(C/member['path'])
        if member['local_pre'] is None:require(not path.exists(),'expected local path absence changed')
        else:check(path,member['local_pre'])

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
    require(names[-1:]==[''] and len(names[:-1])==18 and set(names[:-1])==set(plan['expected_changed_paths']),'whole parent tree differs at exact18 paths only')
    for member in plan['remote_members']:
        require(git(['ls-tree','-z',tree,'--',member['path']],journal)==expected_tree_record(member,True),'proposed18 exact100644 postimages')
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
                   remote_changed_path_count=18,local_install_path_count=32,whole_parent_tree_preserved_outside_exact_overlay=True,sole_parent=plan['base_commit'],local_installation_performed=False)

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
    require(prior['schema']=='pr141-native-sparse-operation-receipt/v1' and prior['action']=='publish' and prior['transaction']=='native_acceptance' and prior['status']=='published_local_install_pending','actual completed public receipt required')
    require(prior['source_sha256']==journal['source_sha256'] and prior['plan_sha256']==journal['plan_sha256'] and prior['review_sha256']==journal['review_sha256'],'identical reviewed publication custody')
    require(prior['own_operation_lock_released'] is True and prior['public_full_body_readback'] is True and prior['public_full_body_mode_readback'] is True and prior['whole_parent_tree_preserved_outside_exact_overlay'] is True and prior['sole_parent']==plan['base_commit'] and prior['remote_changed_path_count']==18 and prior['local_install_path_count']==32,'complete public18 scope, released owned lock and parent-tree proof')
    require(type(prior['actual_PID']) is int and prior['actual_PID']>0 and 'error_type' not in prior and prior['children'] and all(x.get('child_reaped') is True and x.get('process_group_empty') is True for x in prior['children']),'actual public operation PID/closed children')
    commit=tree_oid(prior['published_commit']);journal.update(published_commit=commit,status='public_published_local_install_pending')
    guard(plan,journal);local_preimage_guard(plan)
    public_readback(plan,journal,commit,plan['install_members'])
    journal.update(status='public_published_local_install_in_progress',installed=[],published_receipt={'path':str(absolute(receipt_path)),**pin(receipt_path)},multiple_file_install_globally_atomic=False)
    dump(run_dir/'RECEIPT.json',journal)
    for member in plan['install_members']:install_one(member,journal,run_dir)
    readbacks=[]
    for member in plan['install_members']:
        spec=path_pin(C/member['path']);require({k:spec[k] for k in ('bytes','mode','sha256')}==member['post'],'final32 local fullbody/mode readback')
        readbacks.append(spec)
    guard(plan,journal);require(remote(journal)==commit,'remote main changed after final32 local readbacks')
    journal.update(status='public_and_local_install_verified',local_full_body_mode_readback=True,local_readback_path_count=32,installed_postimages=readbacks,
                   public_full_body_readback=True,public_full_body_mode_readback=True,private_cache_installed=False,raw_backend_installed=False,
                   program3_changed=False,native_acceptance_or_program_completion_claimed=False)

def operation(args):
    run_dir=absolute(args.run_dir);require(run_dir.parent==D/'private','operation run directory scope');run_dir.mkdir(exist_ok=False)
    journal={'schema':'pr141-native-sparse-operation-receipt/v1','actual_PID':os.getpid(),'UTC_start':utc(),'action':args.action,'transaction':'native_acceptance',
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

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    actions=parser.add_subparsers(dest='action',required=True)
    for action in ('plan-sha','prepare'):
        sub=actions.add_parser(action);sub.add_argument('--request',required=True);sub.add_argument('--request-sha',required=True)
        sub.add_argument('--binding',required=True);sub.add_argument('--binding-sha',required=True)
        if action=='prepare':sub.add_argument('--expected-plan-sha',required=True);sub.add_argument('--plan',required=True)
    for action in ('publish','install'):
        sub=actions.add_parser(action);sub.add_argument('--plan',required=True);sub.add_argument('--plan-sha',required=True)
        sub.add_argument('--review',required=True);sub.add_argument('--review-sha',required=True);sub.add_argument('--run-dir',required=True)
        if action=='install':sub.add_argument('--published-receipt',required=True);sub.add_argument('--published-receipt-sha',required=True)
    args=parser.parse_args()
    if args.action in ('plan-sha','prepare'):
        request=path_pin(args.request);binding=path_pin(args.binding)
        require(request['sha256']==sha_value(args.request_sha) and binding['sha256']==sha_value(args.binding_sha),'explicit whole request/currentbinding SHA')
        plan=proposal(request,binding);body=canonical(plan);expected=digest(body)
        if args.action=='prepare':
            require(expected==sha_value(args.expected_plan_sha),'explicit expected plan SHA mismatch')
            path=absolute(args.plan);require(D/'private' in path.parents and not path.exists(),'new scoped plan path required')
            with path.open('xb') as handle:handle.write(body);handle.flush();os.fsync(handle.fileno())
            os.chmod(path,420);require(path.read_bytes()==body,'prepared whole plan readback')
        print(json.dumps({'status':'PROPOSED_PLAN_ONLY_NOT_NATIVE_ACCEPTANCE','plan_sha256':expected,'remote_changes':18,'local_installation_paths':32}))
    else:operation(args)

if __name__=='__main__':main()

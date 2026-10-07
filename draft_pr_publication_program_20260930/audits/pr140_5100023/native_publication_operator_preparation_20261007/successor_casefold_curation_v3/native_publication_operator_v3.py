"""Publish reviewed PR140 native acceptance or final metadata after actual publication/merge.

Local installation is a separate forward-only step after authenticated publication.
Every action requires the exact plan and an independent source/plan PASS.
"""
from pathlib import Path, PurePosixPath
import collections, csv, datetime, hashlib, io, json, os, re, signal, stat, subprocess, sys, time, tempfile

R = Path('/Users/alec/Documents/Math')
C = R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A = C/'draft_pr_publication_program_20260930/audits/pr140_5100023'
D = A/'native_publication_operator_preparation_20261007'
G = '/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
URL = 'https://github.com/AlecKriebel/Math.git'
AUDIT = ('draft_pr_publication_program_20260930/audits/pr140_5100023/',)
K, CODE = '5100023', 'AMR-050-0023'
ORIGINAL_HEAD = '9e908ae58b5ceee6a0825bbebd8acf565db55340'
REVIEW_HASH = '374cf32e1f1b5885551fe8b3a02d43c749e7b392715cc4eb0b4ac77f628a865b'
STATEMENT_HASH = '70a4186cf9778db261377679ae614deec32ed1c2e80e209f809fba637b4e4b89'
ORIGINAL_MANIFEST_SHA = '687a08ae8eba9789f65a8a4c64650b9de7ea2ac6a4b970710cc9a33b83ebb672'
R1_REVIEWED_MANIFEST_SHA = '0d4f2a1fe22d06a787712b60821d477b54880c63c3f5716307a7a2eb0cf4b00f'
ORIGINAL_AUTHOR_LOG_SHA = '4670501b285b8d577b53097a7fdb17cabc0abc7ba28a88f28a258e583da4ffb3'
ORIGINAL_QUEUE_ROW_SHA = '0976537e7836d8d1a7dac530af9d0cc5a66dcdba3b670ddb38942d38e8439114'
SHEET_ID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
ATTEMPT_PREFIX = 'unsolved_math_prioritization/attempts/5100023/'
BACKEND = ('assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','QUEUE.md')
CANONICAL_METADATA = ('assessment.json','HISTORICAL_DESK_ASSESSMENT.json','PUBLICATION_EVIDENCE.json','ACCEPTANCE_EVIDENCE.json','README.md','RESEARCH_LOG.md')
NATIVE = {'unsolved_math_prioritization/'+n for n in BACKEND}|{ATTEMPT_PREFIX+n for n in CANONICAL_METADATA}
ATTEMPT = {ATTEMPT_PREFIX+n for n in ('PROOF.md','verify.py','verification.json','SHA256SUMS','independent_review/independent_checks.py','independent_review/independent_results.json','independent_review/author_replay/PROOF.md','independent_review/author_replay/verify.py','independent_review/author_replay/verification.json')}
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
    require(digest(Path(__file__).read_bytes())==plan['source_sha256'],'running source changed')
    acceptance_inputs(plan);original_archive(plan)
    if plan['transaction']=='final_metadata':completion_inputs(plan)
    for x in plan['protected']: check(x['path'],x)
    for x in plan['protected_absences']: require(not safe(x).exists(),'protected absence changed: '+x)
    for root,expected in [(R,plan['R_HEAD']),(C,plan['C_HEAD'])]:
        got=git(['-C',str(root),'rev-parse','HEAD','refs/heads/main'],journal).decode().splitlines()
        require(got==[expected,expected],'local main/HEAD changed')
    pr=json.loads(run([GH,'api','repos/AlecKriebel/Math/pulls/134'],journal))
    require(pr['state']=='closed' and pr['merged_at'] is None and pr['draft'] is True and pr['head']['sha']==plan['previous_PR134_original_head'],'PR134 disposition changed')
    comment=json.loads(run([GH,'api','repos/AlecKriebel/Math/issues/comments/6028564660'],journal))
    require(digest(comment['body'].encode())==plan['closing_comment_body_sha256'],'closing comment changed')
    current_pr=json.loads(run([GH,'api','repos/AlecKriebel/Math/pulls/140'],journal))
    merged=plan['PR140_merge']
    require(current_pr['state']=='closed' and current_pr['merged'] is True and current_pr['merged_at']==merged['merged_at'] and current_pr['merge_commit_sha']==merged['commit'] and current_pr['draft']==merged['draft'] and current_pr['head']['sha']==ORIGINAL_HEAD and current_pr['base']['ref']=='main','PR140 actual merged head/OID/time changed')

def load_inputs(plan_path,plan_sha,review_path,review_sha):
    require(digest(safe(plan_path).read_bytes())==plan_sha,'plan SHA')
    plan=json.loads(Path(plan_path).read_bytes())
    require(plan['schema']=='pr140-native-publication-overlay/v1','plan schema')
    require(plan['source_sha256']==digest(Path(__file__).read_bytes()),'source SHA')
    require(digest(safe(review_path).read_bytes())==review_sha,'review SHA')
    review=json.loads(Path(review_path).read_bytes())
    require(review['verdict']=='PASS' and review['plan_sha256']==plan_sha and review['source_sha256']==plan['source_sha256'],'independent source/plan review')
    require(review['scope']=='PR140_actual_native_publication_source_and_data' and review['actual_review'] is True and review['actual_data_inputs_authenticated'] is True and review['actual_DOI_tracker_merge_authenticated'] is True,'actual final source/data/service-input review')
    check(G,plan['git_executable']);check(GH,plan['gh_executable'])
    seen=set()
    for m in plan['members']:
        rel=m['path'];require(str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts,'invalid relative path')
        require(rel in NATIVE|ATTEMPT|PROGRAM or rel.startswith(AUDIT),'outside publication scope')
        require(rel.lower() not in seen,'case duplicate');seen.add(rel.lower())
        check(m['source'],m['post'])
        require(m['post']['mode']==420,'publication mode')
        require(not m['install'] or rel in NATIVE|ATTEMPT|PROGRAM,'outside local installation scope')
    require(plan['transaction'] in ['native_acceptance','final_metadata'],'explicit scoped transaction')
    require(plan['current_PR140_original_head']==ORIGINAL_HEAD,'frozen original PR140 head')
    paths={m['path'] for m in plan['members']}
    require(paths,'nonempty reviewed member selection')
    repairs=plan['canonical_repair_paths']
    require(isinstance(repairs,list) and len(repairs)==len(set(repairs)) and set(repairs)<=ATTEMPT and paths&ATTEMPT==set(repairs),'exact declared canonical repair selection')
    for rel in paths:
        require(not rel.casefold().startswith(AUDIT[0].casefold()+'original/') and rel.casefold()!=AUDIT[0].casefold()+'original17_manifest.json','frozen original archive cannot be overwritten through a case alias')
        require(not any(p.casefold().startswith('private') or p.casefold() in {'cache','.git'} for p in PurePosixPath(rel).parts),'private-prefixed/cache/Git paths cannot be published through any case alias')
    native_protection_contract(plan);manifest=original_archive(plan);acceptance_inputs(plan)
    remote_inputs={x['path']:x for x in plan['protected_remote_inputs']}
    require(len(remote_inputs)==len(plan['protected_remote_inputs']),'unique full remote input dependencies')
    for name in ['queue.py','manifest.json','policy.json','SHORTLIST.md']:
        require('unsolved_math_prioritization/'+name in remote_inputs,'readonly native dependency not pinned')
    if plan['transaction']=='native_acceptance':
        require(NATIVE<=paths and not paths&PROGRAM,'complete native14 family; program completion waits for actual native installation')
        require(all(m['install'] is True for m in plan['members'] if m['path'] in NATIVE|ATTEMPT),'native/repair local installation must be separately completed')
        for m in manifest['members']:
            expected=digest(('100644 blob '+m['Git_blob']+'\t'+m['path']+'\0').encode())
            dep=remote_inputs.get(m['path'])
            require(dep is not None and dep['bytes']==m['bytes'] and dep['sha256']==m['sha256'] and dep['tree_sha256']==expected,'actual original-head merged canonical preimages required')
        protected_local={x['path']:{k:x[k] for k in ['bytes','mode','sha256']} for x in plan['protected']}
        for original in manifest['members']:
            if original['path'] not in paths:
                require(protected_local.get(str(C/original['path']))=={k:original[k] for k in ['bytes','mode','sha256']}, 'unselected original canonical history must stay fully protected locally')
        for name in CANONICAL_METADATA:
            if name not in ['README.md','RESEARCH_LOG.md']:
                member=next(m for m in plan['members'] if m['path']==ATTEMPT_PREFIX+name)
                require(member['pre_tree_sha256']==digest(b''),'new canonical metadata preimage must be absent')
    else:
        require(not paths&(NATIVE|ATTEMPT) and not repairs and PROGRAM<=paths,'final metadata requires complete program3 and no native/repair changes')
        require(all(m['install'] is True for m in plan['members'] if m['path'] in PROGRAM),'all3 final program metadata files must be locally installed')
        completion_inputs(plan)
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

def native_json(body):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result, 'duplicate JSON key');result[key]=value
        return result
    def bad(value):raise RuntimeError('nonfinite JSON constant')
    return json.loads(body,object_pairs_hook=pairs,parse_constant=bad)

def native_equal(a,b):
    return json.dumps(a,sort_keys=True,ensure_ascii=False,allow_nan=False)==json.dumps(b,sort_keys=True,ensure_ascii=False,allow_nan=False)

def actual_utc(value):
    require(isinstance(value,str), 'actual UTC string required')
    try:dt=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:raise RuntimeError('invalid actual UTC')
    require(dt.tzinfo is not None and dt.utcoffset()==datetime.timedelta(0), 'actual UTC offset required')
    return dt

def actual_doi(value):
    prefix='10.5281/zenodo.'
    require(isinstance(value,str) and value.startswith(prefix), 'actual Zenodo version DOI required')
    tail=value[len(prefix):]
    require(tail and tail[0]!='0' and all(c in '0123456789' for c in tail), 'invalid actual Zenodo version DOI')
    return value

def native_full_pin(spec):
    require(isinstance(spec,dict) and all(k in spec for k in ['path','bytes','mode','sha256']), 'complete actual input pin required')
    require(isinstance(spec['path'],str) and Path(spec['path']).is_absolute() and str(Path(spec['path']))==spec['path'] and '..' not in Path(spec['path']).parts, 'canonical absolute input path')
    require(type(spec['bytes']) is int and spec['bytes']>=0 and type(spec['mode']) is int and spec['mode'] in (292,420,493), 'actual pin byte/mode types')
    require(isinstance(spec['sha256'],str) and len(spec['sha256'])==64 and all(c in '0123456789abcdef' for c in spec['sha256']), 'actual pin SHA256')
    check(spec['path'],spec)

def original_archive(plan):
    spec=plan['original17_manifest']
    require(spec['path']==str(A/'ORIGINAL17_MANIFEST.json') and spec['sha256']==ORIGINAL_MANIFEST_SHA, 'frozen original17 manifest')
    native_full_pin(spec);manifest=native_json(Path(spec['path']).read_bytes())
    require(manifest['head']==ORIGINAL_HEAD and manifest['originals_captured']==17 and len(manifest['members'])==17, 'original17 manifest identity')
    required={}
    for m in manifest['members']:
        rel=m['relative'];require(isinstance(rel,str) and str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts, 'original relative path')
        require(m['path']==ATTEMPT_PREFIX+rel and m['Git_mode']=='100644' and m['mode']==420, 'original path/mode')
        tree_oid(m['Git_blob']);path=str(A/'original'/rel)
        require(path not in required, 'duplicate original archive path')
        required[path]={k:m[k] for k in ['bytes','mode','sha256']}
    protected={x['path']:{k:x[k] for k in ['bytes','mode','sha256']} for x in plan['protected']}
    require(all(protected.get(p)==v for p,v in required.items()), 'all17 frozen archive bodies must be protected')
    return manifest

def native_protection_contract(plan):
    present={x['path'] for x in plan['protected']};absent=set(plan['protected_absences'])
    require(len(present)==len(plan['protected']) and len(absent)==len(plan['protected_absences']) and not present&absent, 'unique protected resources')
    required={str(root/'.git'/name) for root in (R,C) for name in ['index','config','HEAD','packed-refs','FETCH_HEAD','refs/heads/main','refs/remotes/origin/main','index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']}
    required|={str(C/'unsolved_math_prioritization'/name) for name in ['queue.py','manifest.json','policy.json','cache/catalog.sqlite']}
    require(required<=present|absent, 'exact real Git and backend-presence baselines required')
    require(all(str(C/'unsolved_math_prioritization'/name) in absent for name in ['queue.py','manifest.json','policy.json','cache/catalog.sqlite']), 'intentional checkout backend/cache absences must stay absent')
    require(all(str(root/'.git'/name) in absent for root in (R,C) for name in ['index.lock','HEAD.lock','packed-refs.lock','refs/heads/main.lock','refs/remotes/origin/main.lock']), 'real Git writer locks must remain absent')
    installing={str(C/m['path']) for m in plan['members'] if m['install']}
    require(not installing&(present|absent), 'installed paths cannot be immutable protected resources')

def acceptance_inputs(plan):
    spec=plan['actual_acceptance_inputs']
    require(spec['path']==str(A/'ROOT_NATIVE_PUBLICATION_INPUTS_AUTHENTICATION_20261007.json'), 'fixed actual ROOT input attestation path')
    native_full_pin(spec);a=native_json(Path(spec['path']).read_bytes())
    require(a['schema']=='pr140-actual-native-publication-inputs/v1' and a['owner']=='ROOT' and a['fixture_only'] is False and type(a['actual_ROOT_PID']) is int and a['actual_ROOT_PID']>0, 'actual ROOT acceptance identity')
    actual_utc(a['UTC'])
    require(a['original_head']==ORIGINAL_HEAD and a['review_hash']==REVIEW_HASH and a['statement_hash']==STATEMENT_HASH and a['original_effort']=='2/5' and type(a['new_central_proof_search_turns']) is int and a['new_central_proof_search_turns']==0, 'accepted original source/effort')
    require(a['package_finally_reviewed_and_published'] is True and a['actual_tracker_row_verified'] is True and a['actual_original_head_merge_verified'] is True, 'actual package/publication/tracker/merge completion required')
    actual_doi(a['DOI']);native_full_pin(a['package_manifest_pin'])
    require(isinstance(a['package_member_pins'],list) and a['package_member_pins'], 'full accepted package member inventory')
    package_paths=[]
    for pin_spec in a['package_member_pins']:
        native_full_pin(pin_spec);package_paths.append(pin_spec['path'])
    require(len(package_paths)==len(set(package_paths)) and any(p.endswith('.pdf') for p in package_paths) and any(p.endswith('.zip') for p in package_paths), 'unique actual accepted PDF/support inventory')
    require(isinstance(a['roles'],dict) and set(a['roles'])=={'package','whole_package_R1','whole_package_R2','publication','tracker','merge'}, 'exact actual evidence roles')
    for role,pin_spec in a['roles'].items():native_full_pin(pin_spec)
    require(a['R1_reviewed_manifest_sha256']==R1_REVIEWED_MANIFEST_SHA and a['R2_final_reviewed_manifest_sha256']==a['package_manifest_pin']['sha256'], 'dated first review and final corrected package identity')
    relation_pin=a['review_relationship_pin'];native_full_pin(relation_pin)
    require(relation_pin['path']==str(A/'ROOT_ACTUAL_R1_FINAL_PACKAGE_REPAIR_RELATIONSHIP_20261007.json'), 'actual dated review relationship path')
    relation=native_json(Path(relation_pin['path']).read_bytes())
    require(relation['schema']=='pr140-actual-R1-to-final-package-repair-relationship/v1' and relation['owner']=='ROOT' and relation['fixture_only'] is False and type(relation['actual_ROOT_PID']) is int and relation['actual_ROOT_PID']>0, 'actual review relationship identity')
    actual_utc(relation['UTC'])
    require(relation['R1_reviewed_manifest_sha256']==a['R1_reviewed_manifest_sha256'] and relation['final_package_manifest_sha256']==a['R2_final_reviewed_manifest_sha256'] and relation['R1_result_pin']==a['roles']['whole_package_R1'] and relation['R2_result_pin']==a['roles']['whole_package_R2'] and relation['whole_package_clean_gate_pin']==a['roles']['package'], 'actual dated review/corrected-final/gate custody')
    require(relation['R1_mandatory_findings']==[] and relation['optional_bibliography_correction_applied'] is True and relation['TEX_exact_single_printed_title_substitution'] is True and relation['all_mathematical_proof_text_equations_assumptions_and_code_unchanged'] is True and relation['all_metadata_verification17_README_audit_summary_license_unchanged'] is True and relation['new_fresh_R2_review_of_final_package_is_PASS_with_no_findings'] is True and relation['R1_is_not_claimed_to_have_reviewed_final_changed_bytes'] is True and relation['repair_loop_fulfilled_by_dated_R1_then_repair_then_fresh_clean_final_R2'] is True, 'truthful preserved first review then repair then clean final review')
    comparison=relation['full29_member_comparison'];require(isinstance(comparison,list) and len(comparison)==29, 'full archived/final package comparison')
    seen=set();final_paths=set()
    for member in comparison:
        rel=member['relative'];require(isinstance(rel,str) and str(PurePosixPath(rel))==rel and not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts and rel not in seen, 'unique canonical compared package member')
        seen.add(rel);native_full_pin(member['R1']);native_full_pin(member['final_R2']);final_paths.add(member['final_R2']['path'])
        require(member['full_body_equal'] is (member['R1']['bytes']==member['final_R2']['bytes'] and member['R1']['sha256']==member['final_R2']['sha256']), 'full compared package body equality labels')
    require(final_paths==set(package_paths), 'actual final package inventory binds full review relationship')
    native_full_pin(a['raw_deposition_pin']);native_full_pin(a['actual_original17_local_materialization_pin'])
    require(a['intended_metadata_exactly_matches_all_supplied_provider_fields'] is True and set(a['provider_added_metadata_fields'])=={'doi','imprint_publisher','prereserve_doi'}, 'supplied metadata exactness with truthful provider additions')
    merge=plan['PR140_merge'];require(native_equal(merge,a['PR140_merge']), 'actual merge/plan binding')
    require(merge['original_head']==ORIGINAL_HEAD and merge['url']=='https://github.com/AlecKriebel/Math/pull/140' and merge['base_ref']=='main' and type(merge['draft']) is bool, 'actual merged PR identity')
    tree_oid(merge['commit']);actual_utc(merge['merged_at'])
    sheet=a['sheet'];require(sheet['spreadsheet_id']==SHEET_ID and sheet['gid']==1254632077 and sheet['title']=='Math Puzzles', 'actual tracker identity')
    require(isinstance(sheet['range'],str) and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",sheet['range']), 'actual four-cell tracker range')
    require(isinstance(sheet['values'],list) and len(sheet['values'])==4 and all(isinstance(x,str) for x in sheet['values']) and all(sheet['values'][i].strip() for i in [0,2,3]), 'actual tracker four-cell readback')
    require(sheet['values'][2] in [a['DOI'],'https://doi.org/'+a['DOI']] and K+' / '+CODE in sheet['values'][3], 'actual DOI/problem tracker cells')
    return a

def native_csv_records(body):
    text=body.decode('utf-8');lines=re.findall(r'[^\r\n]*(?:\r\n|\r|\n|$)',text)
    lines=[line for line in lines if line];require(''.join(lines)==text, 'physical CSV coverage')
    reader=csv.reader(io.StringIO(text,newline=''),strict=True);out=[];start=0
    for fields in reader:
        end=reader.line_num;out.append((fields,''.join(lines[start:end]),start,end));start=end
    require(start==len(lines), 'physical CSV record spans')
    return lines,out

def native_csv_overlay(body,target):
    lines,rows=native_csv_records(body);require(rows and 'id' in rows[0][0], 'native CSV header')
    fields=rows[0][0];require(len(fields)==len(set(fields)) and all(len(r[0])==len(fields) for r in rows), 'native CSV field widths')
    col=fields.index('id');ids=[r[0][col] for r in rows[1:]]
    require(len(ids)==len(set(ids)) and ids.count(K)==1, 'unique native CSV target')
    i=ids.index(K)+1;old=rows[i];last=lines[old[3]-1]
    ending='\r\n' if last.endswith('\r\n') else '\r' if last.endswith('\r') else '\n' if last.endswith('\n') else ''
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore',lineterminator='\r\n')
    writer.writerow({**target,'holds':'; '.join(target['holds']),'reasons':'; '.join(target['reasons'])})
    result=(''.join(lines[:old[2]])+stream.getvalue()[:-2]+ending+''.join(lines[old[3]:])).encode()
    _,after=native_csv_records(result)
    require(len(after)==len(rows) and [r[0][col] for r in after[1:]]==ids and all(a[1]==b[1] for j,(a,b) in enumerate(zip(rows,after)) if j!=i), 'unrelated physical CSV rows/order')
    return result

def native_queue_overlay(body,note,doi):
    actual_doi(doi);require(isinstance(note,str) and len(note.split())>=8 and not any(c in note for c in '|\r\n'), 'accepted scoped campaign note')
    text=body.decode('utf-8');lines=[x for x in re.findall(r'[^\r\n]*(?:\r\n|\r|\n|$)',text) if x]
    matches=[i for i,line in enumerate(lines) if line.startswith('| ') and len(line.split('|'))==14 and line.split('|')[2].strip()==K+' / '+CODE]
    require(len(matches)==1, 'unique merged campaign target');i=matches[0];old=lines[i]
    ending='\r\n' if old.endswith('\r\n') else '\r' if old.endswith('\r') else '\n' if old.endswith('\n') else ''
    cells=old.rstrip('\r\n').split('|')
    require(cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5', 'actual original-head merge campaign preimage')
    cells[11],cells[12]=' '+note+' ',' https://doi.org/'+doi+' '
    lines[i]='|'.join(cells)+ending;return ''.join(lines).encode()

def native_ledger_append(before,after,expected):
    require((not before or before.endswith(b'\n')) and after.startswith(before), 'full historical ledger byte prefix')
    suffix=after[len(before):]
    require(suffix.endswith(b'\n') and len(suffix.splitlines())==1 and native_equal(native_json(suffix),expected), 'exact one declared target ledger event')

def validate_native_delta(before,after,canonical,a,attestation_sha,original_manifest_sha):
    require(set(before)==set(BACKEND) and set(after)==set(BACKEND), 'exact eight backend body maps')
    old_ass,new_ass=native_json(before['assessments.json']),native_json(after['assessments.json'])
    require(K in old_ass and set(old_ass)==set(new_ass) and all(native_equal(v,new_ass[k]) for k,v in old_ass.items() if k!=K), 'all unrelated assessments unchanged')
    target=new_ass[K];metadata={'note','rationale','remaining_gap','first_experiment','sources','reviewed_at','original_budget','new_central_proof_search_turns','original_structured_ledger_present','publication_DOI','package_manifest_sha256','native_import_provenance'}
    changed={k for k in set(old_ass[K])|set(target) if k not in old_ass[K] or k not in target or not native_equal(old_ass[K][k],target[k])}
    require(changed<=metadata and target['review_hash']==REVIEW_HASH and target['statement_hash']==STATEMENT_HASH, 'target assessment metadata/source scope')
    require(target['original_budget']=='2/5' and target['original_structured_ledger_present'] is False and type(target['new_central_proof_search_turns']) is int and target['new_central_proof_search_turns']==0 and target['publication_DOI']==a['DOI'] and target['package_manifest_sha256']==a['package_manifest_pin']['sha256'], 'target actual publication/legacy effort')
    actual_utc(target['reviewed_at'])
    state0,state1=native_json(before['state.json']),native_json(after['state.json'])
    require(K not in state0 and set(state1)==set(state0)|{K} and all(native_equal(v,state1[k]) for k,v in state0.items()), 'target import only; existing state requires reconciliation')
    event=state1[K];require(event['id']==K and event['status']=='claimed_solved' and type(event['turns_used']) is int and event['turns_used']==2 and event['review_hash']==REVIEW_HASH and event['statement_hash']==STATEMENT_HASH and event['original_head']==ORIGINAL_HEAD, 'literal dated target import')
    require(event['original_budget']=='2/5' and event['original_structured_ledger_present'] is False and type(event['new_central_proof_search_turns']) is int and event['new_central_proof_search_turns']==0 and event['event']=='dated_import_of_authenticated_author_count' and 'candidate_turn' not in event and 'readiness_review_hash' not in event, 'no synthetic proof/verification chain')
    require(event['original_author_log_sha256']==ORIGINAL_AUTHOR_LOG_SHA and event['original_queue_row_sha256']==ORIGINAL_QUEUE_ROW_SHA, 'authenticated original author-count sources')
    actual_utc(event['at'])
    native_ledger_append(before['history.jsonl'],after['history.jsonl'],event)
    native_ledger_append(before['assessment_history.jsonl'],after['assessment_history.jsonl'],{'id':K,**target})
    catalog0,catalog1=native_json(before['catalog.json']),native_json(after['catalog.json'])
    require(len(catalog0)==len(catalog1) and [x['id'] for x in catalog0]==[x['id'] for x in catalog1] and len({x['id'] for x in catalog0})==len(catalog0), 'catalog identities and physical list order')
    selected=[x for x in catalog1 if x['id']==K];require(len(selected)==1, 'unique catalog target');row=selected[0]
    allowed={'local_status','turns_used','eligible','rank','desk_note'}
    for x,y in zip(catalog0,catalog1):
        if x['id']!=K:require(native_equal(x,y), 'unrelated catalog record/rank/score changed')
        else:require(native_equal({k:v for k,v in x.items() if k not in allowed},{k:v for k,v in y.items() if k not in allowed}), 'target source/score/hold changed')
    require(row['local_status']=='claimed_solved' and type(row['turns_used']) is int and row['turns_used']==2 and row['eligible'] is False and row['rank'] is None and row['desk_note']==target['note'], 'accepted target catalog projection')
    require(after['ranking.csv']==native_csv_overlay(before['ranking.csv'],row), 'exact physical CSV target overlay')
    require(after['QUEUE.md']==native_queue_overlay(before['QUEUE.md'],target['note'],a['DOI']), 'exact campaign target overlay')
    summary=native_json(before['summary.json']);summary.update(records=len(catalog1),eligible=sum(x['eligible'] for x in catalog1),assessed=len(new_ass),holds=dict(collections.Counter(h.split(':')[0] for x in catalog1 for h in x['holds'])))
    require(native_equal(native_json(after['summary.json']),summary), 'complete scoped summary counts')
    require(set(canonical)==set(CANONICAL_METADATA), 'exact six canonical metadata bodies')
    require(native_equal(native_json(canonical['assessment.json']),target) and native_equal(native_json(canonical['HISTORICAL_DESK_ASSESSMENT.json']),old_ass[K]), 'canonical accepted/historical assessments')
    pub=native_json(canonical['PUBLICATION_EVIDENCE.json']);acc=native_json(canonical['ACCEPTANCE_EVIDENCE.json'])
    require(pub['schema']=='pr140-published-native-evidence/v1' and pub['DOI']==a['DOI'] and pub['Sheet_range']==a['sheet']['range'] and pub['package_manifest_sha256']==a['package_manifest_pin']['sha256'] and pub['actual_acceptance_inputs_sha256']==attestation_sha, 'actual canonical publication evidence')
    require(pub['original_head']==ORIGINAL_HEAD and pub['review_hash']==REVIEW_HASH and pub['statement_hash']==STATEMENT_HASH and pub['original_budget']=='2/5' and type(pub['new_central_proof_search_turns']) is int and pub['new_central_proof_search_turns']==0, 'canonical publication source/effort')
    require(acc['schema']=='pr140-scoped-native-acceptance/v1' and acc['literal_native_status']=='claimed_solved' and acc['original_effort']=='2/5' and native_equal(acc['legacy_import'],event) and acc['actual_merge_commit']==a['PR140_merge']['commit'] and acc['actual_merged_at']==a['PR140_merge']['merged_at'] and acc['actual_acceptance_inputs_sha256']==attestation_sha and acc['original17_manifest_sha256']==original_manifest_sha and type(acc['new_central_proof_search_turns']) is int and acc['new_central_proof_search_turns']==0, 'canonical actual merge/import acceptance evidence')
    require(canonical['README.md'].strip() and canonical['RESEARCH_LOG.md'].strip(), 'dated canonical guidance/log required')

def validate_native_proposed_inputs(plan,journal):
    a=acceptance_inputs(plan)
    before={name:git(['show',plan['base_commit']+':unsolved_math_prioritization/'+name],journal) for name in BACKEND}
    members={m['path']:m for m in plan['members']}
    after={name:Path(members['unsolved_math_prioritization/'+name]['source']).read_bytes() for name in BACKEND}
    canonical={name:Path(members[ATTEMPT_PREFIX+name]['source']).read_bytes() for name in CANONICAL_METADATA}
    shortlist=git(['show',plan['base_commit']+':unsolved_math_prioritization/SHORTLIST.md'],journal)
    require(('## '+K+' ').encode() not in shortlist, 'target SHORTLIST requires separate reviewed scope')
    validate_native_delta(before,after,canonical,a,plan['actual_acceptance_inputs']['sha256'],ORIGINAL_MANIFEST_SHA)

def completion_inputs(plan):
    spec=plan['actual_native_completion']
    require(spec['path']==str(A/'ROOT_NATIVE_PUBLICATION_INSTALLATION_ACCEPTANCE_20261007.json'), 'fixed actual native completion attestation path')
    native_full_pin(spec);r=native_json(Path(spec['path']).read_bytes())
    require(r['schema']=='pr140-root-native-installation-acceptance/v1' and r['owner']=='ROOT' and r['fixture_only'] is False and type(r['actual_ROOT_PID']) is int and r['actual_ROOT_PID']>0, 'actual native completion identity')
    actual_utc(r['UTC'])
    require(r['public_native_full_readback'] is True and r['local_native_full_readback'] is True and r['original17_archive_preserved'] is True and r['private_cache_and_backend_absences_preserved'] is True, 'actual completed native readbacks required')
    require(r['actual_acceptance_inputs']==plan['actual_acceptance_inputs'], 'same actual publication/tracker/merge custody')
    for name in ['source','plan','publish','install','root_readback']:native_full_pin(r[name])
    pub=native_json(Path(r['publish']['path']).read_bytes());ins=native_json(Path(r['install']['path']).read_bytes())
    require(pub['schema']==ins['schema']=='pr140-native-publication-operation-receipt/v1' and pub['transaction']==ins['transaction']=='native_acceptance', 'native operation receipt identity')
    require(pub['source_sha256']==ins['source_sha256']==r['source']['sha256'] and pub['plan_sha256']==ins['plan_sha256']==r['plan']['sha256'], 'actual native source/plan custody')
    require(pub['status']=='published_local_install_pending' and pub['public_full_body_readback'] is True and pub['whole_parent_tree_preserved_outside_exact_overlay'] is True and ins['status']=='public_and_local_install_verified' and ins['local_full_body_mode_readback'] is True and pub['own_operation_lock_released'] is True and ins['own_operation_lock_released'] is True, 'actual publication and separate released local installation')
    require(pub['published_commit']==ins['published_commit']==r['published_commit'], 'native completed commit binding');tree_oid(r['published_commit'])
    native_plan=native_json(Path(r['plan']['path']).read_bytes())
    require(native_plan['schema']=='pr140-native-publication-overlay/v1' and native_plan['transaction']=='native_acceptance' and native_plan['source_sha256']==r['source']['sha256'], 'exact completed native plan/source')
    require(native_plan['actual_acceptance_inputs']==plan['actual_acceptance_inputs'], 'completed native plan shares publication custody')
    require(pub['action']=='publish' and ins['action']=='install' and type(pub['actual_PID']) is int and pub['actual_PID']>0 and type(ins['actual_PID']) is int and ins['actual_PID']>0, 'actual separate operation roles/PIDs')
    for receipt in [pub,ins]:
        require('error_type' not in receipt and all(c.get('child_reaped') is True and c.get('process_group_empty') is True for c in receipt['children']), 'completed native operations have no unresolved child/error custody')
    expected={}
    for member in native_plan['members']:
        if member['path'] in NATIVE|ATTEMPT:
            require(member['install'] is True, 'native/repair completed local selection')
            path=str(C/member['path']);require(path not in expected, 'duplicate completed native/repair member')
            expected[path]=member['post']
    require({str(C/path) for path in NATIVE}<=set(expected), 'completed native plan contains all14 native metadata members')
    protected={x['path']:{k:x[k] for k in ['bytes','mode','sha256']} for x in plan['protected']}
    require(isinstance(r['installed_postimages'],list) and len(r['installed_postimages'])==len(expected), 'exact actual native/repair installation inventory')
    names=set()
    for p in r['installed_postimages']:
        native_full_pin(p);require(p['path'] not in names, 'duplicate installed postimage pin');names.add(p['path'])
        value={k:p[k] for k in ['bytes','mode','sha256']}
        require(expected.get(p['path'])==value and protected.get(p['path'])==value, 'installed native/repair outputs remain immutable during final metadata')
    require(names==set(expected), 'no omitted or extra installed native/repair postimages')
    return r

def publish(plan,journal,run_dir):
    guard(plan,journal);require(remote(journal)==plan['base_commit'],'remote changed; rebuild/review plan')
    git(['cat-file','-e',plan['base_commit']+'^{commit}'],journal)
    git(['merge-base','--is-ancestor',plan['PR140_merge']['commit'],plan['base_commit']],journal)
    if plan['transaction']=='native_acceptance':validate_native_proposed_inputs(plan,journal)
    else:git(['merge-base','--is-ancestor',completion_inputs(plan)['published_commit'],plan['base_commit']],journal)
    for m in plan['protected_remote_inputs']:
        z=git(['ls-tree','-z',plan['base_commit'],'--',m['path']],journal)
        require(digest(z)==m['tree_sha256'],'native dependency tree changed')
        b=git(['show',plan['base_commit']+':'+m['path']],journal)
        require(len(b)==m['bytes'] and digest(b)==m['sha256'],'native dependency body changed')
    for m in plan['members']:
        z=git(['ls-tree','-z',plan['base_commit'],'--',m['path']],journal)
        require(digest(z)==m['pre_tree_sha256'],'current remote path/mode/blob changed')
    tree=build_proposed_tree(plan,journal)
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
    require(previous['schema']=='pr140-native-publication-operation-receipt/v1' and previous['source_sha256']==journal['source_sha256'] and previous['transaction']==plan['transaction'] and previous['public_full_body_readback'] is True and previous['whole_parent_tree_preserved_outside_exact_overlay'] is True,'same reviewed actual publication receipt')
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
        tmp=path.with_name(path.name+'.pr140-'+journal['plan_sha256'][:12]+'-'+run_dir.name+'.tmp')
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
    journal={'schema':'pr140-native-publication-operation-receipt/v1','actual_PID':os.getpid(),'UTC_start':utc(),'action':action,'plan_sha256':ps,'source_sha256':digest(Path(__file__).read_bytes()),'review_sha256':rs,'children':[],'status':'starting'}
    lock=D/'private/OPERATION_LOCK.json';owned_lock=None;lock_identity=None
    try:
        safe(lock);fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        try:
            s=os.fstat(fd);lock_identity=(s.st_dev,s.st_ino)
            os.write(fd,json.dumps({'PID':os.getpid(),'UTC':utc(),'plan_sha256':ps}).encode());os.fsync(fd)
        finally:os.close(fd)
        owned_lock=pin(lock)
        plan=load_inputs(pp,ps,rp,rs)
        journal['transaction']=plan['transaction']
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

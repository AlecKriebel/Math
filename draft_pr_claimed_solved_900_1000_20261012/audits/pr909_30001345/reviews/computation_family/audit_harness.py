"""Reproduce immutable PR909 only in disposable copies; capture adversarial controls."""
import hashlib, json, os, platform, shutil, socket, stat, subprocess, sys, time
from pathlib import Path
BASE=Path(__file__).resolve().parent
ORIGINAL=BASE.parents[1]/'original/unsolved_math_prioritization/attempts/30001345'
HEAD='d186dea31791cd3e8acf6829e0b65d01849623b8'
PREFIX='unsolved_math_prioritization/attempts/30001345/'
TMP=BASE/'tmp'
TMP.mkdir(exist_ok=True)
ENV=os.environ.copy(); ENV['TMPDIR']=str(TMP); ENV['PYTHONDONTWRITEBYTECODE']='1'; ENV.pop('PYTHONOPTIMIZE',None)
def check(p,m):
    if not p: raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,obj):(BASE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args,cwd=None,env=None,timeout=180):
    started=time.monotonic()
    try:
        p=subprocess.run([str(a) for a in args],cwd=cwd or BASE,env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
        return {'returncode':p.returncode,'seconds':round(time.monotonic()-started,4),'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace'),'timeout':False}
    except subprocess.TimeoutExpired as e:
        return {'returncode':None,'seconds':round(time.monotonic()-started,4),'stdout':(e.stdout or b'').decode(errors='replace'),'stderr':(e.stderr or b'').decode(errors='replace'),'timeout':True}
def invoke(root,flags=(),integrity=True,env=None,timeout=15):
    return run([sys.executable,'-I','-B',*flags,root/'verify_publication.py',*(['--integrity-only'] if integrity else [])],cwd=root.parent,env=env,timeout=timeout)
def fresh(name):
    p=TMP/name
    if p.exists():shutil.rmtree(p)
    shutil.copytree(ORIGINAL,p)
    return p
def rewrite_manifest(root,transform=None,raw_transform=None):
    p=root/'PACKAGE_MANIFEST.json'; d=json.loads(p.read_bytes())
    if transform:transform(d)
    b=json.dumps(d,indent=2).encode()+b'\n'
    if raw_transform:b=raw_transform(b)
    p.write_bytes(b)
    (root/'PACKAGE_MANIFEST.sha256').write_text(sha(b)+'  PACKAGE_MANIFEST.json\n')

# Authenticate independently against the original Git tree, not a mutable manifest.
gitfiles=subprocess.check_output(['git','ls-tree','-r','--name-only',HEAD,'--',PREFIX],cwd=BASE.parents[4]).decode().splitlines()
snapshot={p.relative_to(ORIGINAL).as_posix():p for p in ORIGINAL.rglob('*') if p.is_file()}
check(len(gitfiles)==28 and {p[len(PREFIX):] for p in gitfiles}==set(snapshot),'closed Git/snapshot inventory')
identities={}
for rel,p in sorted(snapshot.items()):
    check(stat.S_ISREG(p.lstat().st_mode),'snapshot regular file')
    b=p.read_bytes(); gitb=subprocess.check_output(['git','show',HEAD+':'+PREFIX+rel],cwd=BASE.parents[4])
    check(b==gitb,'Git byte mismatch '+rel)
    identities[rel]={'bytes':len(b),'sha256':sha(b)}
check(identities['PACKAGE_MANIFEST.json']['sha256']=='a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02','outer pin')
check(identities['frozen_v2/PROOF.md']['sha256']=='561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b','proof pin')
save('original_identities.json',{'head':HEAD,'tree_prefix':PREFIX,'files':identities,'file_count':28,'all_bytes_equal_git':True})

replays={}
if '--resume-completed-replays' not in sys.argv[1:]:
    root=fresh('historical replay [spaces]')
    for name,flags,environment,isolated in [('normal',[],ENV,True),('O',['-O'],ENV,True),('OO',['-OO'],ENV,True),('inherited_PYTHONOPTIMIZE2',[],dict(ENV,PYTHONOPTIMIZE='2'),False)]:
        args=[sys.executable,*(['-I'] if isolated else []),'-B',*flags,root/'verify_publication.py']
        replays[name]=run(args,cwd=root.parent,env=environment,timeout=180)
        check(replays[name]['returncode']==0,'historical full replay '+name)
        save('historical_replay_results.json',replays)
    replays['original_mutation_suite']=run([sys.executable,'-I','-B',root/'mutation_tests.py'],cwd=root.parent,timeout=180)
    check(replays['original_mutation_suite']['returncode']==0,'original mutations')
    save('historical_replay_results.json',replays)
else:
    replays=json.loads((BASE/'historical_replay_results.json').read_bytes())
    check(len(replays)==5 and all(r['returncode']==0 for r in replays.values()),'complete successful replay checkpoint required')

negative={}
def record(name,root,expected=None,timeout=15):
    r=invoke(root,timeout=timeout); negative[name]=r
    if expected is not None:check((r['returncode']==0)==expected and not r['timeout'],name)
    save('negative_results.json',negative)
root=fresh('negative fixture')
(root/'extra-empty-directory').mkdir(); record('extra_empty_directory',root,True)
shutil.rmtree(root/'extra-empty-directory')
rewrite_manifest(root,lambda d:d.update(schema=True));record('schema_boolean_true',root,True)
root=fresh('negative fixture');rewrite_manifest(root,lambda d:d.update(schema=1.0,problem_id=30001345.0));record('schema_and_id_float',root,True)
root=fresh('negative fixture');rewrite_manifest(root,raw_transform=lambda b:b.replace(b'"schema": 1',b'"schema": 999, "schema": 1'));record('duplicate_schema_last_wins',root,True)
root=fresh('negative fixture');rewrite_manifest(root,lambda d:d.update(scope='now claims all fine-M and unibranched conjectures'));record('unbound_scope_rewrite',root,True)
root=fresh('negative fixture');rewrite_manifest(root,lambda d:d['files'][0].update(bytes=float(d['files'][0]['bytes'])));record('payload_bytes_float',root,True)
root=fresh('negative fixture');rewrite_manifest(root,raw_transform=lambda b:b[:-2]+b', "schema": NaN}\n');record('nonstandard_NaN_json',root,False)
root=fresh('negative fixture');rewrite_manifest(root,lambda d:d['files'][0].update(file='../escape'));record('manifest_path_escape',root,False)
root=fresh('negative fixture');rewrite_manifest(root,lambda d:d['files'].__setitem__(1,d['files'][0]));record('duplicate_manifest_item',root,False)
root=fresh('negative fixture');(root/'frozen_v2/PROOF.md').write_bytes(b'altered proof\n')
rewrite_manifest(root,lambda d:[x.update(bytes=14,sha256=sha(b'altered proof\n')) for x in d['files'] if x['file']=='frozen_v2/PROOF.md'])
record('rewritten_outer_manifest_proof_still_pinned',root,False)
root=fresh('negative fixture');(root/'README.md').write_bytes(b'rewritten wrapper\n')
rewrite_manifest(root,lambda d:[x.update(bytes=18,sha256=sha(b'rewritten wrapper\n')) for x in d['files'] if x['file']=='README.md'])
record('rewritten_unanchored_wrapper',root,True)
root=fresh('negative fixture');p=root/'frozen_v2/PROOF.md';p.unlink();p.symlink_to(ORIGINAL/'frozen_v2/PROOF.md');record('listed_file_symlink',root,False)
root=fresh('negative fixture');(root/'alias-dir').symlink_to(root/'frozen_v2',target_is_directory=True);record('directory_symlink',root,False)
root=fresh('negative fixture');os.mkfifo(root/'fifo');record('unlisted_FIFO',root,False,3)
root=fresh('negative fixture');p=root/'frozen_v2/PROOF.md';p.unlink();os.mkfifo(p);record('listed_FIFO',root,False,3)
root=fresh('negative fixture');sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
prior_cwd=os.getcwd();os.chdir(root)
try:sock.bind('socket')
finally:os.chdir(prior_cwd)
record('unlisted_socket',root,False,3);sock.close()
root=fresh('negative fixture');alias=TMP/'root alias'
if alias.is_symlink():alias.unlink()
alias.symlink_to(root,target_is_directory=True);record('root_symlink_alias',alias,True)
record('root_dotdot_alias',root/'..'/root.name,True)

# Direct replay bypasses the outer hash check only to test subprocess guards.
root=fresh('false assertions')
p=root/'audit_a/independent_checks.py'; b=p.read_bytes();needle=b'assert len(pair_points) == 36 and len(points) == 12'
check(b.count(needle)==1,'unique false assertion fixture');p.write_bytes(b.replace(needle,b'assert False, "INJECTED_FALSE_ASSERTION"'))
for name,args,environment,expect in [('auditA_direct_normal',[sys.executable,'-I','-B',p],ENV,False),('auditA_direct_OO',[sys.executable,'-I','-B','-OO',p],ENV,True),('auditA_wrapper_OO',[sys.executable,'-I','-B','-OO',root/'run_audit_a.py'],ENV,False),('auditA_wrapper_inherited2',[sys.executable,'-B',root/'run_audit_a.py'],dict(ENV,PYTHONOPTIMIZE='2'),False)]:
    r=run(args,env=environment,timeout=15);negative[name]=r;check((r['returncode']==0)==expect,name)
code="import runpy; runpy.run_path("+repr(str(root/'verify_publication.py'))+")[\"replay\"]()"
r=run([sys.executable,'-B','-OO','-c',code],env=dict(ENV,PYTHONOPTIMIZE='2'),timeout=180)
negative['replay_false_assertion_child_under_OO_inherited2']=r
check(r['returncode']!=0 and 'INJECTED_FALSE_ASSERTION' in r['stderr'],'false assertion must propagate child failure')
root=fresh('explicit predicate');p=root/'frozen_v2/checks.py';b=p.read_bytes();p.write_bytes(b.replace(b"require(len(intersections)==12,'exactly twelve pair-intersection points')",b"require(False,'INJECTED_FALSE_PREDICATE')"))
r=run([sys.executable,'-I','-B','-OO',p],timeout=15);negative['author_explicit_false_predicate_OO']=r
check(r['returncode']!=0 and 'INJECTED_FALSE_PREDICATE' in r['stderr'],'explicit author predicate under OO')
save('negative_results.json',negative)
check(all(p.read_bytes()==subprocess.check_output(['git','show',HEAD+':'+PREFIX+rel],cwd=BASE.parents[4]) for rel,p in snapshot.items()),'original changed after all replays')
import sympy,mpmath
save('runtime.json',{'python':sys.version,'implementation':platform.python_implementation(),'sympy':sympy.__version__,'mpmath':mpmath.__version__,'temporary_root':str(TMP),'source_original_bytes_unchanged':True,'roundoff':'none in exact algebra; seconds fields are diagnostic wall-clock floats'})
print(json.dumps({'status':'PASS','authenticated_files':28,'full_replays':4,'new_controls':len(negative)},indent=2))

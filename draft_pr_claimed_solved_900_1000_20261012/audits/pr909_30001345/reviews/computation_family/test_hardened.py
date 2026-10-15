"""Focused negative controls for the standalone pinned verifier."""
import hashlib,json,os,runpy,shutil,socket,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
ORIGINAL=BASE.parents[1]/'original/unsolved_math_prioritization/attempts/30001345'
TMP=BASE/'tmp'; FIXTURE=TMP/'hardened fixture'
ENV=os.environ.copy();ENV['TMPDIR']=str(TMP);ENV['PYTHONDONTWRITEBYTECODE']='1'
RESULTS={}
def require(p,m):
    if not p:raise RuntimeError(m)
def fresh():
    if FIXTURE.exists():shutil.rmtree(FIXTURE)
    shutil.copytree(ORIGINAL,FIXTURE)
    return FIXTURE
def invoke(name,root,good=False,flags=(),env=None,replay=False):
    start=time.monotonic()
    args=[sys.executable,'-B',*flags,BASE/'hardened_verify.py',root,*(['--replay'] if replay else [])]
    timeout=180 if replay else 3
    try:
        p=subprocess.run([str(a) for a in args],env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
        require((p.returncode==0)==good,name)
        RESULTS[name]={'returncode':p.returncode,'seconds':round(time.monotonic()-start,4),'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'timeout':False}
    except subprocess.TimeoutExpired:
        raise RuntimeError(name+' HUNG')
    (BASE/'hardened_test_results.json').write_text(json.dumps(RESULTS,indent=2,sort_keys=True)+'\n')
def rewrite(root,mutate):
    p=root/'PACKAGE_MANIFEST.json';d=json.loads(p.read_bytes());mutate(d);b=json.dumps(d).encode()+b'\n';p.write_bytes(b)
    (root/'PACKAGE_MANIFEST.sha256').write_text(hashlib.sha256(b).hexdigest()+'  PACKAGE_MANIFEST.json\n')

if '--path-spellings-only' in sys.argv[1:]:
    RESULTS.update(json.loads((BASE/'hardened_test_results.json').read_bytes()))
    r=fresh()
    invoke('root_trailing_slash_accepted',str(r)+'/',True)
    invoke('root_repeated_separator_accepted',str(r.parent)+'//'+r.name,True)
    print(json.dumps({'status':'PASS','new_focused_controls':2,'total_focused_controls':len(RESULTS)},indent=2))
    raise SystemExit(0)

r=fresh();invoke('baseline_normal',r,True)
invoke('root_trailing_slash_accepted',str(r)+'/',True)
invoke('root_repeated_separator_accepted',str(r.parent)+'//'+r.name,True)
invoke('baseline_O',r,True,flags=('-O',))
invoke('baseline_OO',r,True,flags=('-OO',))
invoke('baseline_inherited2',r,True,env=dict(ENV,PYTHONOPTIMIZE='2'))
invoke('relocated_full_replay',r,True,flags=('-OO',),env=dict(ENV,PYTHONOPTIMIZE='2'),replay=True)
r=fresh();(r/'empty-dir').mkdir();invoke('extra_empty_dir_rejected',r)
r=fresh();(r/'frozen_v2/empty-dir').mkdir();invoke('nested_extra_empty_dir_rejected',r)
r=fresh();(r/'unexpected.txt').write_text('x');invoke('extra_file_rejected',r)
r=fresh();(r/'README.md').unlink();invoke('missing_file_rejected',r)
r=fresh();p=r/'frozen_v2/PROOF.md';p.unlink();p.symlink_to(ORIGINAL/'frozen_v2/PROOF.md');invoke('listed_file_symlink_rejected',r)
r=fresh();(r/'alias-dir').symlink_to(r/'frozen_v2',target_is_directory=True);invoke('directory_symlink_rejected',r)
r=fresh();os.mkfifo(r/'fifo');invoke('unlisted_FIFO_rejected_without_hang',r)
r=fresh();p=r/'frozen_v2/PROOF.md';p.unlink();os.mkfifo(p);invoke('listed_FIFO_rejected_without_hang',r)
r=fresh();sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);old=os.getcwd();os.chdir(r)
try:sock.bind('socket')
finally:os.chdir(old)
invoke('socket_rejected_without_hang',r);sock.close()
r=fresh();alias=TMP/'hardened alias'
if alias.is_symlink():alias.unlink()
alias.symlink_to(r,target_is_directory=True);invoke('root_symlink_rejected',alias)
invoke('root_dotdot_rejected',str(r)+'/../'+r.name)
invoke('relative_root_rejected',r.name)
r=fresh();rewrite(r,lambda d:d.update(schema=True));invoke('boolean_schema_rejected',r)
r=fresh();rewrite(r,lambda d:d.update(schema=1.0,problem_id=30001345.0));invoke('float_schema_id_rejected',r)
r=fresh();rewrite(r,lambda d:d['files'][0].update(bytes=float(d['files'][0]['bytes'])));invoke('float_size_rejected',r)
r=fresh();rewrite(r,lambda d:d.update(scope='unibranched/fine-M claims'));invoke('scope_rewrite_rejected',r)
r=fresh();(r/'README.md').write_text('changed wrapper');rewrite(r,lambda d:[a.update(bytes=15,sha256=hashlib.sha256(b'changed wrapper').hexdigest()) for a in d['files'] if a['file']=='README.md']);invoke('rewritten_wrapper_and_manifest_rejected',r)
r=fresh();(r/'frozen_v2/PROOF.md').write_text('changed proof');rewrite(r,lambda d:[a.update(bytes=13,sha256=hashlib.sha256(b'changed proof').hexdigest()) for a in d['files'] if a['file']=='frozen_v2/PROOF.md']);invoke('rewritten_proof_and_manifest_rejected',r)
r=fresh();p=r/'PACKAGE_MANIFEST.json';p.write_bytes(p.read_bytes().replace(b'"schema": 1',b'"schema": 99, "schema": 1'));(r/'PACKAGE_MANIFEST.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  PACKAGE_MANIFEST.json\n');invoke('duplicate_json_key_and_manifest_rejected',r)
r=fresh();rewrite(r,lambda d:d['files'][0].update(file='../escape'));invoke('manifest_path_escape_rejected',r)
strict=runpy.run_path(str(BASE/'hardened_verify.py'))['strict_json']
for name,b in [('duplicate_keys',b'{"x":1,"x":2}'),('NaN',b'{"x":NaN}'),('Infinity',b'{"x":Infinity}'),('malformed',b'{broken')]:
    try:strict(b)
    except ValueError:RESULTS['strict_parser_'+name]={'rejected':True}
    else:raise RuntimeError('strict parser accepted '+name)
(BASE/'hardened_test_results.json').write_text(json.dumps(RESULTS,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','focused_controls':len(RESULTS)},indent=2))

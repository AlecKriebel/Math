#!/usr/bin/env python3
"""Isolated review launches only; original sources never executed or changed."""
from pathlib import Path
import copy,datetime,hashlib,json,os,platform,shutil,stat,subprocess,sys,time
W=Path(__file__).resolve().parent
O=W.parents[1]/'original/unsolved_math_prioritization/attempts/10400145'
T=W/'tmp';T.mkdir(exist_ok=True)
PINS={'BOOTSTRAP.py':'72378da263ab077353da81c68c3d890ad1eafdeba170c3e450d3b1ccd4b72ad3','VERIFY_PUBLICATION.py':'26af53e20751505dcb2b310fb10d66c79042daf220c85b96395d8fed03066d6e','PUBLICATION_MANIFEST.json':'e5748a840564410c91e0c4268415a802401a642f7b484494d9e0daa8831160cb','author_v3/bootstrap.py':'301e0c33f5eafccb1701687ae9cfbd574496b0ef1fd357bb4c4efe728c2379fa','author_v3/AUTHOR_MANIFEST.json':'abc975e091ff72d9b020f238ef4ff7884a4ce9c0ed755b34f45626c1ef74158c','author_v3/packet/verify.py':'f131676e31272e2a0a55ad242b0302e6a356ecb6c3cfbe56f71c3fd4dac0ab53','TEST_MUTATIONS.py':'405733c6b0914e8645b088954315b4e4a826bdf2198826e7c399fd272a07eb9b','audit_algebra/audit_controls.py':'18baf9448829a8049332e6dfa11cb3f0585dcc18a26c4d1a134ec3baa01d160e','audit_source_bridge/independent_algebra.py':'cca45522c8ca635caffd92589e7aa52372f16371e97e7f6eb0c2b7ecc1732020','audit_source_bridge/run_audit.py':'c35afade977c17eb0afa73953b37467dd19e273fa5763b54b4d6b8db311f2c43'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(c,m):
    if not c:raise RuntimeError(m)
def copycase(n):
    d=T/n
    need(not d.exists(),'case exists: '+n)
    shutil.copytree(O,d)
    return d
base=copycase('cold_packet')
for n,pin in PINS.items():need(sha((base/n).read_bytes())==pin,'initial external pin '+n)
(T/'work').mkdir(exist_ok=True);(T/'temp').mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(T/'temp'))
rows=[]
def run(label,script,args=(),mode='',cwd=None,environ=None,expect='pass',root=base,external=True):
    if external:
        rel=str(script.relative_to(root)) if script.is_relative_to(root) else None
        if rel in PINS and sha(script.read_bytes())!=PINS[rel]:
            rows.append({'label':label,'mode':mode or 'normal','status':'REJECT_INITIAL_EXTERNAL_PIN','script':rel,'payload_executed':False,'expected':expect});return None
    t=time.perf_counter();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    flags=[] if not mode else [mode]
    try:
        p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=cwd or T/'work',env=environ or env,capture_output=True,timeout=180)
        r={'label':label,'mode':mode or 'normal','utc':utc,'elapsed_seconds':round(time.perf_counter()-t,6),'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode('utf-8','replace'),'expected':expect}
        if p.stdout:
            try:r['output']=json.loads(p.stdout)
            except ValueError:r['stdout']=p.stdout.decode('utf-8','replace')
        rows.append(r)
        (W/'RUNTIME_RESULTS.json').write_text(json.dumps({'schema':'pr952-computation-runtime-v1','host':platform.platform(),'python':sys.version,'python_executable':sys.executable,'uid':os.getuid(),'bwrap':shutil.which('bwrap'),'initial_external_pins':PINS,'rows':rows},indent=2)+'\n')
        need((p.returncode==0 and not p.stderr) if expect=='pass' else p.returncode!=0,'unexpected '+label+' '+mode)
        return p
    except subprocess.TimeoutExpired as e:
        rows.append({'label':label,'mode':mode,'utc':utc,'elapsed_seconds':round(time.perf_counter()-t,6),'status':'TIMEOUT','failed_attempt':True})
        raise
for mode in ['','-O','-OO']:
    run('independent-math',W/'independent_math.py',mode=mode)
    run('original-author-direct',base/'author_v3/packet/verify.py',mode=mode)
    run('original-author-bootstrap',base/'author_v3/bootstrap.py',[base/'author_v3/packet'],mode)
    run('original-algebra-audit',base/'audit_algebra/audit_controls.py',[base/'author_v3'],mode)
    run('original-bridge-algebra',base/'audit_source_bridge/independent_algebra.py',mode=mode)
    run('original-outer-integrity',base/'BOOTSTRAP.py',[base,'--integrity-only'],mode)
    # These expected failures are genuine; no chmod or replacement bwrap.
    run('original-full-replay-unavailable',base/'BOOTSTRAP.py',[base],mode,expect='reject')
    run('original-source-bridge-unavailable',base/'audit_source_bridge/run_audit.py',[base/'author_v3',PINS['author_v3/AUTHOR_MANIFEST.json'],PINS['author_v3/bootstrap.py'],T/('bridge'+(mode or 'normal')+'.json')],mode,expect='reject')
run('original-publication-mutation-harness',base/'TEST_MUTATIONS.py',[base])
# Our independent direct semantic controls, keeping the checker code pinned.
cert=json.loads((base/'author_v3/packet/CERTIFICATE.json').read_bytes())
mutations=[('wrong-cubic-v3',lambda c:c.update(first_coefficients=[0,-6,-12])),('zero-residual',lambda c:c.update(second_difference=0)),('off-by-one-rank',lambda c:c.update(ranks=[0,1,2])),('bool-rank',lambda c:c.update(ranks=[1,True,3])),('float-coefficient',lambda c:c.update(first_coefficients=[0,-6,-24.0])),('zero-casson',lambda c:c.update(casson_normalization=0)),('orientation-sign',lambda c:c.update(casson_normalization=1)),('wrong-parameter',lambda c:c.update(quantum_parameter='q=1+2*x')),('poles-at-one',lambda c:c.update(base_ring='Q((x))')),('two-node-quotient',lambda c:c.update(quotient_level=2)),('extra-certificate-key',lambda c:c.update(extra=0)),('missing-certificate-key',lambda c:c.pop('witness'))]
for label,mutate in mutations:
    d=copycase('semantic_'+label);c=copy.deepcopy(cert);mutate(c);(d/'author_v3/packet/CERTIFICATE.json').write_text(json.dumps(c))
    for mode in ['','-O','-OO']:run('own-semantic-'+label,d/'author_v3/packet/verify.py',mode=mode,root=d,expect='reject')
for label,raw in [('duplicate-key',b'{"problem_id":10400145,'+(base/'author_v3/packet/CERTIFICATE.json').read_bytes().lstrip()[1:]),('nonfinite',b'{"second_difference":NaN}'),('nonobject',b'[]'),('truncated',b'{'),('trailing', (base/'author_v3/packet/CERTIFICATE.json').read_bytes()+b'[]')]:
    d=copycase('json_'+label);(d/'author_v3/packet/CERTIFICATE.json').write_bytes(raw)
    for mode in ['','-O','-OO']:run('own-JSON-'+label,d/'author_v3/packet/verify.py',mode=mode,root=d,expect='reject')
# Namespace and byte attacks at outer boundary; mode-only change is an explicitly
# accepted boundary probe because the original manifests do not bind Unix modes.
for label in ['stale-proof','extra-shadow','extra-dir','symlink-payload','fifo','changed-verifier','changed-outer-bootstrap','changed-author-bootstrap','mode-only','world-writable','parent-symlink']:
    d=copycase('integrity_'+label)
    if label=='stale-proof':
        p=d/'author_v3/packet/PROOF_AND_STATUS.md';p.write_bytes(p.read_bytes()+b'\nchanged\n')
    elif label=='extra-shadow':(d/'author_v3/packet/json.py').write_text('raise Exception("shadow")\n')
    elif label=='extra-dir':(d/'unlisted-empty').mkdir()
    elif label=='symlink-payload':
        p=d/'author_v3/packet/CERTIFICATE.json';p.unlink();p.symlink_to(base/'author_v3/packet/CERTIFICATE.json')
    elif label=='fifo':os.mkfifo(d/'UNEXPECTED_FIFO')
    elif label=='changed-verifier':
        p=d/'VERIFY_PUBLICATION.py';p.write_bytes(p.read_bytes()+b'\n# changed\n')
    elif label=='changed-outer-bootstrap':
        p=d/'BOOTSTRAP.py';p.write_bytes(p.read_bytes()+b'\n# changed\n')
    elif label=='changed-author-bootstrap':
        p=d/'author_v3/bootstrap.py';p.write_bytes(p.read_bytes()+b'\n# changed\n')
    elif label=='mode-only':(d/'author_v3/packet/PROOF_AND_STATUS.md').chmod(0o755)
    elif label=='world-writable':(d/'author_v3/packet/verify.py').chmod(0o666)
    elif label=='parent-symlink':
        alias=T/'alias';alias.symlink_to(T,target_is_directory=True);d=alias/d.name
    expected='pass' if label in ['mode-only','world-writable','parent-symlink'] else 'reject'
    for mode in ['','-O','-OO']:run('own-integrity-'+label,d/'BOOTSTRAP.py',[d,'--integrity-only'],mode,root=d,expect=expected)
# Root symlink is rejected, unlike symlink ancestors.
alias=T/'direct-root-link';alias.symlink_to(base,target_is_directory=True)
for mode in ['','-O','-OO']:run('own-integrity-root-symlink',base/'BOOTSTRAP.py',[alias,'--integrity-only'],mode,expect='reject')
# Neither module shadows nor Python environment variables may execute a sentinel.
host=T/'hostile';host.mkdir();sentinel=host/'IMPORTED'
for n in ['json','hashlib','pathlib','subprocess','site','sitecustomize','usercustomize']:
    (host/(n+'.py')).write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\nraise RuntimeError("hostile import")\n')
henv=dict(env,PYTHONPATH=str(host),PYTHONSTARTUP=str(host/'json.py'),PYTHONHOME=str(host/'absent'),PYTHONINSPECT='1',PYTHONWARNINGS='error')
for mode in ['','-O','-OO']:
    run('own-hostile-outer',base/'BOOTSTRAP.py',[base,'--integrity-only'],mode,cwd=host,environ=henv)
    run('own-hostile-author',base/'author_v3/bootstrap.py',[base/'author_v3/packet'],mode,cwd=host,environ=henv)
need(not sentinel.exists(),'hostile sentinel was executed')
# Verify cold-copy byte/mode preservation; originals are separately reauthenticated.
after={str(p.relative_to(base)):{'sha256':sha(p.read_bytes()),'mode':f'{stat.S_IMODE(p.stat().st_mode):04o}'} for p in base.rglob('*') if p.is_file()}
expected=json.loads((W/'START.json').read_bytes())['files']
need(all(v['sha256']==expected['unsolved_math_prioritization/attempts/10400145/'+n]['sha256'] and v['mode']==expected['unsolved_math_prioritization/attempts/10400145/'+n]['disk_mode'] for n,v in after.items()) and len(after)==33,'cold copy changed')
r=json.loads((W/'RUNTIME_RESULTS.json').read_bytes());r['cold_copy_bytes_and_modes_unchanged']=True;r['hostile_sentinel_absent']=True;r['row_count']=len(rows);r['elapsed_seconds_sum']=round(sum(x.get('elapsed_seconds',0) for x in rows),6);r['full_readonly_replay']='NOT_REPRODUCED_MACOS_BWRAP_ABSENT';r['no_original_executable_was_run']=True;(W/'RUNTIME_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'elapsed_seconds_sum':r['elapsed_seconds_sum'],'cold_copy_unchanged':True,'full_replay':r['full_readonly_replay']}))

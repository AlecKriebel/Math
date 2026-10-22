#!/usr/bin/env python3
"""Independent concrete CLI tests, with evidence persisted before assertions.
Usage: python -I -S -B independent_runtime_checks.py CANDIDATE REVIEW
No subject or source mutation; optional source-only inputs are original read-only corpora.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,shutil,subprocess,sys,time

def stamp():return datetime.now(timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def check(ok,why):
    if not ok:raise ValueError(why)
def main():
    C=Path(sys.argv[1]).resolve();R=Path(sys.argv[2]).resolve();P=R/'private_tmp';results=[]
    tool=C/'portable.py';idx='d7700197f73c55bee8fc3006fe30107dcec58ebf99c69579ebec3f248075c455';outer='746ca08c65b489a216edfc3962f7001ac6750945f8468fdb96bd9ba4c7739f0c'
    def run(label,args,env=None,flags=('-I','-S','-B')):
        cmd=[sys.executable,*flags,*map(str,args)];start=stamp();mono=time.monotonic_ns()
        proc=subprocess.Popen(cmd,cwd=P,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);launch=stamp()
        expired=False
        try:out,err=proc.communicate(timeout=180)
        except subprocess.TimeoutExpired:expired=True;proc.kill();out,err=proc.communicate()
        meta={'started_utc':start,'launched_utc':launch,'ended_utc':stamp(),'elapsed_monotonic_ns':time.monotonic_ns()-mono,'pid':proc.pid,'returncode':proc.returncode,'timeout':expired,'stdout':pin(out),'stderr':pin(err)}
        save(P/(label+'.stdout.bin'),out);save(P/(label+'.stderr.bin'),err);save(P/(label+'.json'),(json.dumps(meta,indent=2,sort_keys=True)+'\n').encode())
        results.append({'label':label,**meta});check(not expired,'timeout '+label);return proc.returncode,out,err
    rc,out,err=run('verify-only',[tool,'current',outer,'--root',C,'--verify-only'])
    v=json.loads(out);check(rc==0 and not err and v['portable']['replay']['archival_code_executed'] is False and v['portable']['replay']['label']=='VERIFY_ONLY_BYTE_AUTHENTICATION_NO_ARCHIVAL_EXECUTION','verify-only contract')
    for label,args,reason,flags in [
        ('verify-only-receipts',[tool,'current',outer,'--root',C,'--verify-only','--receipt-dir',P/'forbidden-receipts'],'zero archival process receipts',('-I','-S','-B')),
        ('bad-external-pin',[tool,'current','0'*64,'--root',C,'--receipt-dir',P/'bad-pin-receipts'],'external current manifest pin mismatch',('-I','-S','-B')),
        ('missing-B',[tool,'current',outer,'--root',C,'--verify-only'],'actual -I -S -B',('-I','-S')),
        ('double-optimized',[tool,'current',outer,'--root',C,'--verify-only'],'normal or single -O',('-I','-S','-B','-OO'))]:
        rc,out,err=run(label,args,flags=flags);check(rc!=0 and reason.encode() in out,'expected CLI rejection '+label)
    check(not (P/'forbidden-receipts').exists() and not (P/'bad-pin-receipts').exists(),'rejection before receipt mutation')
    code="""import pathlib,sys,subprocess
p=pathlib.Path(sys.argv[1]);n={'__file__':str(p),'__name__':'review_instrumented'}
exec(compile(p.read_bytes(),str(p),'exec'),n)
calls=[]
def reject(*a,**k):
 calls.append(True);raise RuntimeError('UNEXPECTED_PROCESS')
subprocess.Popen=reject
sys.argv=[str(p),'current',sys.argv[2],'--root',sys.argv[3],'--verify-only']
n['isolated']();n['main']()
if calls:raise RuntimeError('ARCHIVAL_EXECUTION')
print('INDEPENDENT_PROCESS_TRAP_ZERO_CALLS')
"""
    rc,out,err=run('zero-execution-trap',['-c',code,tool,outer,C]);check(rc==0 and not err and out.endswith(b'INDEPENDENT_PROCESS_TRAP_ZERO_CALLS\n'),'independent zero-execution process trap')
    hook=P/'hostile-startup';hook.mkdir();marker=P/'hostile-hook.marker'
    (hook/'sitecustomize.py').write_text("import os\nfrom pathlib import Path\nPath("+repr(str(marker))+").write_bytes(b'CAPABLE_HOSTILE_STARTUP')\nos.write(1,b'HOSTILE_STARTUP_EXECUTED\\n')\nos._exit(0)\n")
    env=dict(os.environ);env.update(PYTHONPATH=str(hook),PYTHONOPTIMIZE='2',PYTHONDONTWRITEBYTECODE='1')
    rc,out,err=run('hostile-capability',['-c',"raise RuntimeError('MAIN_SHOULD_NOT_RUN')"],env=env,flags=())
    check(rc==0 and out==b'HOSTILE_STARTUP_EXECUTED\n' and marker.read_bytes()==b'CAPABLE_HOSTILE_STARTUP','functioning hostile startup control')
    # Preserve the control marker, and change the payload destination for the subject.
    protected_marker=P/'hostile-hook-during-tool.marker'
    (hook/'sitecustomize.py').write_text((hook/'sitecustomize.py').read_text().replace(str(marker),str(protected_marker)))
    rc,out,err=run('hostile-current',[tool,'current',outer,'--root',C,'--receipt-dir',P/'hostile-replay'],env=env)
    check(rc==0 and not err and not protected_marker.exists(),'isolated tool resists capable startup hook')
    v=json.loads(out);check([e['measured_flags']['optimize'] for e in v['portable']['replay']['launcher']['events']]==[0,1,0,0,0,1,1,1],'hostile actual child modes')
    # Coherently reindex a deliberately changed historical file in a private copy.
    copied=P/'corrupt-portable';shutil.copytree(C/'verification',copied)
    target=copied/'source/authored/check_algebra.py';target.write_bytes(target.read_bytes()+b'\nCORRUPT_BYTES_MUST_NOT_EXECUTE\n')
    index=json.loads((copied/'package_index.json').read_bytes())
    for row in index['files']:
        if row['path']=='source/authored/check_algebra.py':row.update(pin(target.read_bytes()))
    b=(json.dumps(index,indent=2,sort_keys=True)+'\n').encode();(copied/'package_index.json').write_bytes(b)
    rc,out,err=run('reindexed-immutable-corruption',[copied/'portable.py','verify',hashlib.sha256(b).hexdigest(),'--root',copied,'--receipt-dir',P/'corrupt-replay'])
    check(rc!=0 and b'pin mismatch: source/authored/check_algebra.py' in out and not (P/'corrupt-replay').exists(),'immutable source rejects reindexed corruption before replay')
    # Original complete corpora, never copied or prefiltered.
    W=C.parents[4];native=W/'unsolved_math_prioritization'
    corpus=[native/'catalog.json',native/'cache/problems.json',native/'cache/research_results.json']
    check(all(p.is_file() for p in corpus),'complete corpus locations')
    rc,out,err=run('source-only',[tool,'source-only','--catalog',corpus[0],'--problems',corpus[1],'--reports',corpus[2]])
    v=json.loads(out);check(rc==0 and not err and len(v['inputs'])==3 and all(r['complete_pin_before_any_extraction'] for r in v['inputs']) and v['archival_code_executed'] is False,'source-only complete-input authentication')
    result={'status':'PASS','scope':'Independent concrete CLI tests; finite diagnostics do not certify the theorem','tests':[{'label':r['label'],'returncode':r['returncode'],'pid':r['pid'],'started_utc':r['started_utc'],'launched_utc':r['launched_utc'],'ended_utc':r['ended_utc'],'elapsed_monotonic_ns':r['elapsed_monotonic_ns'],'stdout':r['stdout'],'stderr':r['stderr']} for r in results],'hostile_hook_capability_control':'EXECUTED','hostile_hook_during_isolated_tool':'NOT_EXECUTED','zero_execution_trap_calls':0,'original_corpora_copied':False,'optional_closed_five_primary_route':'NOT_RUN','implementer_regression':'NOT_RUN'}
    (R/'RUNTIME_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()

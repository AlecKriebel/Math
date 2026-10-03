"""Actual captures of this family's own source authoring/readiness controls only."""
from pathlib import Path
import argparse,datetime as dt,hashlib,json,os,subprocess,sys,stat
F=Path(__file__).absolute().parent
ALLOWED={'author_v2.py','private_controls.py','bind_predecessor_design.py','readiness_private.py'}
SOURCES=['pr49_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def enc(q):return (json.dumps(q,sort_keys=True,indent=2)+'\n').encode()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('capture');ap.add_argument('script');a=ap.parse_args()
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise ValueError('Optimization prohibited')
    if a.script not in ALLOWED or not a.capture or '/' in a.capture or a.capture in {'.','..'}:raise ValueError('Own source/control allowlist only')
    script=F/a.script
    if script.is_symlink() or not stat.S_ISREG(script.lstat().st_mode):raise ValueError('Own regular script')
    source=script.read_bytes();operator=Path(__file__).read_bytes();d=F/a.capture;d.mkdir()
    pre=dict(schema='pr49-v2-private-prelaunch/v1',created_utc=now(),operator_pid=os.getpid(),argv=[sys.executable,'-B',str(script)],cwd=str(F),stdin_supplied=False,source_sha256=sha(source),operator_sha256=sha(operator))
    put(d/'PRELAUNCH_SOURCE.py',source);put(d/'PRELAUNCH_OPERATOR.py',operator)
    rows=[]
    if a.script in {'private_controls.py','readiness_private.py'}:
        q=d/'PRELAUNCH_PROPOSED_SOURCES';q.mkdir()
        for n in SOURCES:
            b=(F/n).read_bytes();put(q/n,b);rows.append(dict(path=n,bytes=len(b),sha256=sha(b)))
    pre['proposed_sources_read_as_text_only']=rows
    if a.script=='readiness_private.py':
        b=(F/'source_package_checks.py').read_bytes();put(d/'PRELAUNCH_SOURCE_PACKAGE_CHECKS.py',b);pre['own_common']=dict(path='PRELAUNCH_SOURCE_PACKAGE_CHECKS.py',bytes=len(b),sha256=sha(b))
    put(d/'PRELAUNCH.json',enc(pre));start=now();c=subprocess.Popen(pre['argv'],cwd=F,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=c.communicate();end=now()
    q=dict(schema='pr49-v2-private-actual-capture/v1',prelaunch=pre,actual_execution=True,completed=True,operator_pid=os.getpid(),pid=c.pid,exit_code=c.returncode,started_utc=start,finished_utc=end,source_unchanged=script.read_bytes()==source,operator_unchanged=Path(__file__).read_bytes()==operator)
    for n,b in [('stdout',out),('stderr',err)]:put(d/(n+'.bin'),b);q[n]=dict(path=n+'.bin',bytes=len(b),sha256=sha(b))
    q['status']='PASS' if c.returncode==0 and q['source_unchanged'] and q['operator_unchanged'] else 'FAIL';put(d/'CAPTURE.json',enc(q))
    print(json.dumps(dict(capture=a.capture,actual_child_pid=c.pid,status=q['status'],exit_code=c.returncode,stdout=out.decode(errors='replace'),stderr=err.decode(errors='replace'))));return 0 if q['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())

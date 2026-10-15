"""Reproduce submitted finite controls; no geometric acceptance is inferred."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,signal,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];S=A/'snapshot/unsolved_math_prioritization/attempts/30002792';sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def need(x,m):
    if not x:raise RuntimeError(m)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=p.stat().st_mode&511)
def main():
    need(not sys.flags.optimize,'parent assertions enabled')
    code=S/'final_review/check_small_characteristics.py';proof=S/'PUBLIC_TURN_2.md';expected=S/'final_review/SMALL_CHARACTERISTIC_CHECKS.json'
    need(pin(code)['sha256']=='08744c44e2a0c057ac8d25b315c5a0c282ce60a32ce5c9bdd7546fc0b3668b4d' and pin(proof)['sha256']=='56d7aee2dbb567f1574952bfe905b5407c0f0b06ec60e4b53b72acda48c245e1','exact submitted executable and proof')
    manifest=json.loads((S/'FINAL_MANIFEST.json').read_bytes());need(len(manifest['files'])==17,'17 nonself submitted manifest roles')
    for x in manifest['files']:
        b=(S/x['path']).read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'entire submitted manifest body')
    D=A/'root_original_control_replay';D.mkdir(exist_ok=False);archives=[]
    for i,p in enumerate([Path(__file__),code,proof,expected]):
        z=D/f'{i}_source.gz';z.write_bytes(gzip.compress(p.read_bytes(),mtime=0));archives.append(dict(input=pin(p),stored=pin(z)))
    argv=['/opt/homebrew/bin/python3','-E','-B',str(code),'--proof',str(proof)];q=dict(argv=argv,cwd=str(R),UTC=utc(),actual_recorder_PID=os.getpid(),source=pin(Path(__file__)),full_prelaunch_inputs=archives,automatic_retry=False,geometric_acceptance=False)
    (D/'request.json').write_text(json.dumps(q,indent=2)+'\n');proc=None;out=err=b'';failure=None;complete=False
    try:
        proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        try:
            (D/'started.json').write_text(json.dumps(dict(actual_PID=proc.pid,start_UTC=utc()),indent=2)+'\n');out,err=proc.communicate(timeout=55);complete=True
        except BaseException:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            out,err=proc.communicate(timeout=5);complete=True;raise
    except BaseException as ex:failure=dict(type=type(ex).__name__,message=str(ex))
    streams={}
    for n,b in [('stdout',out),('stderr',err)]:
        z=D/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(z),bytes=len(b),sha256=sha(b))
    e=dict(**q,end_UTC=utc(),actual_PID=proc.pid if proc else None,exit_code=proc.returncode if proc else None,parent_reaped=proc is not None and proc.poll() is not None,complete_streams=complete,failure=failure,streams=streams)
    (D/'execution.json').write_text(json.dumps(e,indent=2)+'\n');need(failure is None and complete and proc.returncode==0 and not err,'actual finite controls completed')
    got=json.loads(out);want=json.loads(expected.read_bytes());need(got==want and got['assertions']==3888 and got['proof_sha256']==pin(proof)['sha256'],'whole native JSON exactly equals submitted controls')
    p=A/'ROOT_ORIGINAL_CONTROL_REPRODUCTION.json';record=dict(status='PASS_EXACT_SUBMITTED_FINITE_CONTROLS_REPRODUCED',UTC=utc(),actual_ROOT_PID=os.getpid(),source=pin(Path(__file__)),actual_child_PID=proc.pid,actual_child_exit=0,execution=pin(D/'execution.json'),native_full_stdout_JSON=got,whole_submitted_final_manifest_authenticated=True,assertions=3888,finite_line_examples=24,geometric_lemma_certified=False,mathematical_acceptance=False,priority_acceptance=False,qualification='Exact bounded algebra/numeric replay only; arbitrary-characteristic surface existence and all theorem assumptions still require independent proof and primary-source audits.')
    with p.open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    p.chmod(0o444);print(json.dumps(dict(status=record['status'],actual_child_PID=proc.pid,exit_code=0,assertions=3888,acceptance=pin(p)),indent=2))
if __name__=='__main__':main()

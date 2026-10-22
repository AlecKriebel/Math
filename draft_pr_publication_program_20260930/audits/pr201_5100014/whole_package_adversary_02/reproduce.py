"""Run pinned package controls, read-only inputs, with inherited shared deps."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,os,json,time
D=Path(__file__).resolve().parent;P=D.parent/'publication_package_v2/materials';records=[]
for opt in (False,True):
    for false in (False,True):
        cmd=[sys.executable,'-B']+(['-O'] if opt else [])+[str(P/'verification/run_checks.py')]+(['--guard-false'] if false else [])
        label=('optimized' if opt else 'normal')+('_deliberate_false' if false else '_portable')
        started=datetime.now(timezone.utc).isoformat();t=time.monotonic()
        r=subprocess.run(cmd,cwd=P,capture_output=True,text=True,env=os.environ.copy())
        (D/(label+'.stdout')).write_text(r.stdout);(D/(label+'.stderr')).write_text(r.stderr)
        passed=(r.returncode!=0 and 'DELIBERATE FALSE CONDITION' in r.stderr) if false else (r.returncode==0 and json.loads(r.stdout)['status']=='PASS')
        records.append({'start_UTC':started,'end_UTC':datetime.now(timezone.utc).isoformat(),'label':label,'command':cmd,'returncode':r.returncode,'expected_behavior_observed':passed,'seconds':time.monotonic()-t})
        (D/'reproduction_receipt.json').write_text(json.dumps({'PYTHONPATH':os.environ.get('PYTHONPATH'),'records':records},indent=2)+'\n')
        if not passed:raise RuntimeError(label+' failed expected behavior')
print(json.dumps({'status':'PASS','records':records},indent=2))

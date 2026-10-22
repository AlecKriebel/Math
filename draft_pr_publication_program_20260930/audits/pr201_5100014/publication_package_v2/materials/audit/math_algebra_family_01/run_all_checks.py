"""Reproduce this audit using the existing interpreter/shared software only.

All stdout/stderr and runner timestamps stay in fresh_reproduction/. Candidate
code is never modified. Any unexpected exit or result raises explicitly.
"""
import subprocess,sys,json,datetime,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
DEST=HERE/'fresh_reproduction';DEST.mkdir(exist_ok=True)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
steps=[]
jobs=[(name,[]) for name in ('exact_independent_controls.py','extended_exact_controls.py','physical_phase_checks.py','probe_assertion_enforcement.py')]+[('replay_original.py',[kind]) for kind in ('exact','generic','reviewer')]
for opt in (False,True):
    for name,args in jobs:
        label=Path(name).stem+('_'+args[0] if args else '')+('_optimized' if opt else '_normal')
        cmd=[sys.executable,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(HERE/name)]+args
        started=utc();tick=time.monotonic()
        with (DEST/(label+'.stdout')).open('wb') as out,(DEST/(label+'.stderr')).open('wb') as err:
            r=subprocess.run(cmd,cwd=HERE,stdout=out,stderr=err)
        steps.append({'label':label,'started_utc':started,'finished_utc':utc(),'elapsed_seconds':time.monotonic()-tick,'returncode':r.returncode,'command':cmd})
        (DEST/'RUN_RECEIPT.json').write_text(json.dumps({'steps':steps},indent=2)+'\n')
        if r.returncode:raise RuntimeError('reproduction failed: '+label)
r=subprocess.run([sys.executable,'-E','-S','-B','-P',str(HERE/'audit_original_manifests.py')],cwd=HERE,stdout=subprocess.DEVNULL)
if r.returncode:raise RuntimeError('original manifest audit failed')
for mode in ('normal','optimized'):
    for name in ('exact_independent_controls','extended_exact_controls','physical_phase_checks','probe_assertion_enforcement'):
        data=json.loads((DEST/(name+'_'+mode+'.stdout')).read_text())
        if data['status']!='PASS':raise RuntimeError('unexpected fresh verdict '+name)
    for name,old in (('exact','turn1_exact.txt'),('generic','turn1_generic_six.txt')):
        if (DEST/('replay_original_'+name+'_'+mode+'.stdout')).read_bytes()!=(HERE.parent/'original_submitted_head'/old).read_bytes():
            raise RuntimeError('author replay bytes differ '+name)
print(json.dumps({'status':'PASS','completed_jobs':len(steps)+1,'receipt':str(DEST/'RUN_RECEIPT.json'),'limitations':'Finite evidence; optimized original assertions are stripped, as deliberately false probes demonstrate.'},indent=2))

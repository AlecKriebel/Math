#!/usr/bin/env python3
import datetime,hashlib,importlib.util,json,pathlib,sys,time
F=pathlib.Path(__file__).resolve().parent
P=F.parents[1]/'publication'
spec=importlib.util.spec_from_file_location('round2_operative_workflow',P/'workflow_regression.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.REPORT_ROOT=F
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
result=m.worker()
receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'started_at_utc':start,'optimization':sys.flags.optimize,'elapsed_seconds':time.monotonic()-t,'program_sha256':hashlib.sha256((P/'workflow_regression.py').read_bytes()).hexdigest(),'result':result,'scope':'Independent invocation of actual operative worker; only REPORT_ROOT is redirected inside assigned review folder. Synthetic fixtures stub remote operations, compiler and reviewer evidence; no live release assurance.'}
path=F/('WORKFLOW_MODE_'+str(sys.flags.optimize)+'.json');path.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'path':path.name,'status':result['status'],'elapsed_seconds':receipt['elapsed_seconds'],'keys':list(result)},indent=2))

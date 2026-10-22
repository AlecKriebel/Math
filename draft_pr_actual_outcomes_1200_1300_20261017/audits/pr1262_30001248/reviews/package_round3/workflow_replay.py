from pathlib import Path
import datetime,json,os,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parents[1]/'publication'
code="import importlib.util,pathlib,json; s=importlib.util.spec_from_file_location('actual_workflow',"+repr(str(P/'workflow_regression.py'))+"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.REPORT_ROOT=pathlib.Path("+repr(str(R))+" ); print(json.dumps(m.worker(),sort_keys=True))"
runs=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
for flags in [[],['-O'],['-OO']]:
    p=subprocess.run([sys.executable,'-B',*flags,'-c',code],capture_output=True,text=True,env=env,timeout=180)
    if p.returncode:raise RuntimeError(p.stderr)
    obj=json.loads(p.stdout)
    if obj['status']!='PASS':raise RuntimeError('actual workflow worker not PASS')
    runs.append({'flags':flags,'result':obj})
if not all(x['result']==runs[0]['result'] for x in runs):raise RuntimeError('mode disagreement')
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','runs':runs,'same_all_modes':True,'runtime_hook':'REPORT_ROOT overridden to own reviewer family so every temporary fixture is under own _local. No operative source byte changed.','limits':'Actual deployed worker with mocked compiler/services/Git only. No live release or integration approval.'}
(R/'WORKFLOW_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','same_all_modes':True,'actual_worker':str(P/'workflow_regression.py')}))

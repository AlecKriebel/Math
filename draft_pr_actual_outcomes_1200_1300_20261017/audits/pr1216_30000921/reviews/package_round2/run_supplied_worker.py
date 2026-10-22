from pathlib import Path
import subprocess,json,sys,datetime,hashlib
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';runs=[]
for flags in [[],['-O'],['-OO']]:
 p=subprocess.run([sys.executable,'-B',*flags,str(P/'workflow_regression.py'),'--worker'],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr)
 runs.append({'flags':flags,'result':json.loads(p.stdout)})
if not all(x['result']==runs[0]['result'] for x in runs):raise RuntimeError('different mode output')
(R/'SUPPLIED_WORKER_RECEIPT.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'program_sha256':hashlib.sha256((P/'workflow_regression.py').read_bytes()).hexdigest(),'runs':runs,'scope':'Only supplied offline --worker entry; does not rewrite reviewed WORKFLOW_REGRESSION_RECEIPT.'},indent=2)+'\n')
print('Supplied worker passed normal/O/OO')

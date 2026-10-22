from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parents[1]/'publication';program=P/'workflow_regression.py'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
started=datetime.datetime.now(datetime.timezone.utc).isoformat();jobs=[]
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 out=(R/'_local'/('documented_'+label+'.json')).open('w');err=(R/'_local'/('documented_'+label+'.stderr')).open('w');p=subprocess.Popen([sys.executable,'-B',*flags,str(program),'--worker'],stdout=out,stderr=err);jobs.append((label,flags,p,out,err))
runs=[]
for label,flags,p,out,err in jobs:
 code=p.wait();out.close();err.close();need(code==0,(R/'_local'/('documented_'+label+'.stderr')).read_text());result=json.loads((R/'_local'/('documented_'+label+'.json')).read_text());need(result['status']=='PASS','Worker did not pass '+label);runs.append({'flags':flags,'result':result})
need(all(r['result']==runs[0]['result'] for r in runs),'Optimization-dependent guards')
d=json.loads((R/'ACTUAL_DEPLOYMENT_RECEIPT.json').read_text());bindings={e['path']:sha(Path(e['path'])) for e in d['files']};need(bindings=={e['path']:e['sha256'] for e in d['files']},'Deployment drift during validation')
receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'started_utc':started,'runs':runs,'all_modes_identical':True,'authored_workflow_sha256':bindings,'execution':'Three independent exact workflow_regression.py --worker processes, normal/-O/-OO, launched concurrently; same full business guards and equality comparisons as the helper main. All source/deployment hashes reread after completion.','runner_sha256':sha(Path(__file__)),'scope':'Offline synthetic fixture regressions only; final actual package requires rerun and independent whole-package review.'}
(R/'_local/WORKFLOW_REGRESSION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':'PASS','all_modes_identical':True,'at_utc':receipt['at_utc']},indent=2))

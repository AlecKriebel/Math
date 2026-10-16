import json,os,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';rows=[]
for label,flags,opt,want in [('normal',[],None,0),('O',['-O'],None,1),('OO',['-OO'],None,2),('env2',[],'2',2)]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',REVIEW_MODE=label+'_final');env.pop('PYTHONOPTIMIZE',None)
 if opt is not None:env['PYTHONOPTIMIZE']=opt
 for name in ['helper_controls.py','r7_controls.py']:
  p=subprocess.run([PY,*flags,'-B',str(R/name)],env=env,capture_output=True,text=True,timeout=120)
  (R/'private'/(name+'.'+label+'.stderr')).write_text(p.stderr)
  if p.returncode:raise RuntimeError(label+name+p.stderr)
  result=json.loads(p.stdout)
  if result['actual_parent_optimization']!=want:raise RuntimeError('actual optimization')
  (R/(name[:-3].upper()+'_'+label+'.json')).write_text(json.dumps(result,indent=2)+'\n');rows.append({'script':name,'mode':label,'actual_parent_optimization':want,'cases':result['cases'],'status':'PASS'})
 print(label+' PASS',flush=True)
(R/'HELPER_MODE_SUMMARY.json').write_text(json.dumps({'status':'PASS','rows':rows,'real_external_calls':0,'operational_mains_called':False},indent=2)+'\n')

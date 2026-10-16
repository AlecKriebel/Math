import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent;PYTHON='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';rows=[];r7=[]
for label,flags,opt,want in [('normal',[],None,0),('O',['-O'],None,1),('OO',['-OO'],None,2),('env2',[],'2',2)]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',REVIEW_MODE=label+'_final');env.pop('PYTHONOPTIMIZE',None)
 if opt is not None:env['PYTHONOPTIMIZE']=opt
 for script,collection in [('helper_controls.py',rows),('finalizer_auth_control.py',r7)]:
  p=subprocess.run([PYTHON,*flags,'-B',str(R/script)],env=env,capture_output=True,text=True,timeout=120)
  (R/'private'/(script+'.'+label+'.stderr')).write_text(p.stderr)
  if p.returncode:raise RuntimeError(label+' '+script+': '+p.stderr)
  data=json.loads(p.stdout)
  if script=='helper_controls.py' and data['actual_parent_optimization']!=want:raise RuntimeError('Wrong outer optimization')
  if script=='finalizer_auth_control.py':
   if data['actual_parent_optimization']!=want:raise RuntimeError('Wrong actual R7 optimization')
   data['observed_outer_optimization']=data['actual_parent_optimization']
  (R/((script.removesuffix('.py')).upper()+'_'+label+'.json')).write_text(json.dumps(data,indent=2)+'\n');collection.append({'mode':label,'observed_outer_optimization':want,'cases':data.get('cases',1),'status':data['status']})
 print(label+' helper controls '+str(rows[-1]['cases'])+' PASS; R7 reproduced',flush=True)
(R/'HELPER_MODE_SUMMARY.json').write_text(json.dumps({'status':'PASS','independent_current_helper_controls':rows,'R7_adverse_controls':r7,'operational_mains_called':False},indent=2)+'\n')

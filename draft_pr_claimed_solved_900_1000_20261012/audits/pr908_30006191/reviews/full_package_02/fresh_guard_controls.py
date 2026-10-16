#!/usr/bin/env python3
"""Independent post-copy mutation and exact-type boundary attacks."""
from pathlib import Path
import datetime,importlib.util,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
PIN='eff4b4b19c1d931d3f067af7261c315a33452b732ba1c647163e3995804f5b39'
HARNESS=r'''
import importlib.util,json,sys
from pathlib import Path
root,work,target,marker=map(Path,sys.argv[1:])
spec=importlib.util.spec_from_file_location('review02_boundary',root/'verify_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pin='eff4b4b19c1d931d3f067af7261c315a33452b732ba1c647163e3995804f5b39'
m.validate(root,pin)
old=m.shutil.copytree
def corrupt(source,destination,*a,**kw):
 result=old(source,destination,*a,**kw)
 if Path(destination).name=='package':
  (Path(destination)/target).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')
 return result
m.shutil.copytree=corrupt
try:m.worker(root,pin,work)
except RuntimeError as e:
 if 'Payload fingerprint mismatch: '+str(target) not in str(e):raise
else:raise RuntimeError('post-copy mutation accepted')
if marker.exists():raise RuntimeError('unauthenticated copied code executed')
print(json.dumps({'rejected_before_execution':True,'target':str(target),'optimization':sys.flags.optimize,'isolated':sys.flags.isolated}))
'''
LAUNCHER=r'''
import os,subprocess,sys
env=dict(os.environ)
for k in ('PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME'):env.pop(k,None)
raise SystemExit(subprocess.run([sys.executable,'-I','-B',*sys.argv[1:]],env=env).returncode)
'''
def need(ok,label):
 if not ok:raise RuntimeError(label)
def main():
 root=HERE/'tmp/bundle';work=HERE/'tmp/fresh_guards';work.mkdir(exist_ok=True)
 harness=work/'harness.py';harness.write_text(HARNESS)
 launcher=work/'launcher.py';launcher.write_text(LAUNCHER)
 rows=[]
 for mode,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
  for target in ('run_checked.py','original_packet/author/verify.py'):
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(work));env.pop('PYTHONOPTIMIZE',None)
   if opt:env['PYTHONOPTIMIZE']=opt
   marker=work/(mode+'_'+target.replace('/','_')+'.marker')
   p=subprocess.run([sys.executable,*flags,str(launcher),str(harness),str(root),str(work),target,str(marker)],capture_output=True,text=True,env=env,timeout=30)
   need(p.returncode==0,p.stderr);r=json.loads(p.stdout)
   need(r['optimization']==0 and r['isolated']==1 and not marker.exists(),'guard state')
   rows.append({'outer_mode':mode,**r})
 spec=importlib.util.spec_from_file_location('boundary_api',root/'verify_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 rejected=[]
 for label,fn in [
  ('bool_vs_int',lambda:m.equivalent(True,1)),
  ('int_vs_bool',lambda:m.equivalent(1,True)),
  ('float_vs_int_count',lambda:m.equivalent(1.,1)),
  ('string_vs_int_count',lambda:m.equivalent('1',1)),
  ('NaN_value',lambda:m.equivalent(float('nan'),1.)),
  ('outside_float_tolerance',lambda:m.equivalent(1.0001,1.)),
  ('duplicate_JSON',lambda:m.strict_json('{"x":1,"x":2}')),
  ('nonfinite_JSON',lambda:m.strict_json('{"x":Infinity}')),
 ]:
  try:fn()
  except (RuntimeError,ValueError):rejected.append(label)
  else:raise RuntimeError('false boundary accepted '+label)
 m.equivalent(1.+5e-10,1.);m.equivalent(True,True);m.equivalent(1,1)
 out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'package_manifest_sha256':PIN,'post_copy_negative_runs':len(rows),'rows':rows,
  'type_and_JSON_negatives':rejected,'positive_semantic_boundary_controls':3,
  'scope':'Controlled copy mutations, exact type semantics and JSON parsing. No signature or concurrent-ancestor-race guarantee.'}
 (HERE/'FRESH_GUARD_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()

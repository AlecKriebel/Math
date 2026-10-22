#!/usr/bin/env python3
"""Packaging fault-injection checks on disposable copies only."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
reader=Path(sys.argv[1]).resolve(); output=Path(sys.argv[2]); rows=[]
def need(x,m):
 if not x: raise RuntimeError(m)
for scenario in ['unknown_id','modified_script','modified_expected_pin','modified_result_semantics','outer_optimization']:
 with tempfile.TemporaryDirectory(prefix='eisenstein_guard_') as d:
  r=Path(d); shutil.copy2(reader/'run_checks.py',r/'run_checks.py');spec=json.loads((reader/'CHECK_INVENTORY.json').read_text());check=next(x for x in spec['checks'] if x['id']=='C04');spec['checks']=[check];
  for key in ['script','expected']:
   target=r/check[key];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(reader/check[key],target)
  if scenario=='modified_script': (r/check['script']).write_bytes((r/check['script']).read_bytes()+b'\n# altered disposable test\n')
  if scenario=='modified_expected_pin': (r/check['expected']).write_bytes((r/check['expected']).read_bytes()+b' ')
  if scenario=='modified_result_semantics':
   p=r/check['expected'];j=json.loads(p.read_text());j['P_augmentation']='incorrect';p.write_text(json.dumps(j)+'\n');check['expected_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
  (r/'CHECK_INVENTORY.json').write_text(json.dumps(spec));env=dict(os.environ)
  if scenario=='outer_optimization':env['PYTHONOPTIMIZE']='2'
  out=subprocess.run([sys.executable,str(r/'run_checks.py'),'--only','UNKNOWN' if scenario=='unknown_id' else 'C04'],cwd=r,env=env,capture_output=True,text=True)
  if scenario=='outer_optimization':need(out.returncode==0,'normal assertion check under outer optimization');j=json.loads(out.stdout);need(j['execution_count']==1 and j['results'][0]['mode']=='normal' and j['results'][0]['bytes_match'],'mode mismatch');message='Normal assertion-based child ran with outer PYTHONOPTIMIZE=2 and matched frozen bytes.'
  else:
   wanted={'unknown_id':'Unknown requested check IDs','modified_script':'Script pin mismatch','modified_expected_pin':'Expected-output pin mismatch','modified_result_semantics':'result differs from the frozen JSON'}[scenario];need(out.returncode!=0 and wanted in out.stderr,'fault injection not rejected '+scenario);message=wanted
  rows.append({'scenario':scenario,'status':'PASS','observed_exit_code':out.returncode,'confirmed_behavior':message})
output.write_text(json.dumps({'status':'PASS','scope':'Runner guard behavior in disposable copies; accepted scripts and reader untouched','results':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))

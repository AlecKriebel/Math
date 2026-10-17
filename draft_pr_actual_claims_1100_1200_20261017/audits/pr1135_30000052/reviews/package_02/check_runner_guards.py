from pathlib import Path
import importlib.util,json,hashlib,copy,sys,tempfile,shutil,subprocess
R=Path(__file__).resolve().parent;M=R/'tmp/mirror'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[]
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='hostile-') as tmp:
 T=Path(tmp);shutil.copytree(M/'audit',T/'audit');shutil.copytree(M/'verification',T/'verification')
 mod=importlib.util.spec_from_file_location('runner',T/'verification/verify_all.py');runner=importlib.util.module_from_spec(mod);mod.loader.exec_module(runner)
 plan=json.loads((T/'verification/CONTROL_PLAN.json').read_text());base=plan['controls'][0]
 for opt in [False,True]:
  for label in ['input_corruption','checker_corruption','expected_corruption','repinned_false_result','repinned_assert']:
   s=copy.deepcopy(base);inputs=plan['inputs'];p=None;old=None
   if label=='input_corruption':p=T/'audit/inputs/PROOF.md';old=p.read_bytes();p.write_bytes(old+b'\n')
   elif label=='checker_corruption':p=T/'audit'/s['file'];old=p.read_bytes();p.write_bytes(old+b'\n')
   elif label=='expected_corruption':p=T/'audit'/s['expected'];old=p.read_bytes();p.write_bytes(old+b'\n')
   elif label=='repinned_false_result':
    p=T/'audit'/s['expected'];old=p.read_bytes();d=json.loads(old);d['status']='WRONG';p.write_text(json.dumps(d));s['expected_pin']=pin(p)
   else:
    p=T/'audit'/s['file'];old=p.read_bytes();p.write_bytes(old+b'\nassert True\n');s['pin']=pin(p)
   try:runner.run((s,opt,inputs))
   except RuntimeError as e:rows.append({'control':label,'optimized':opt,'rejected':True,'reason':str(e).replace(str(T),'<mirror>')})
   else:raise RuntimeError('runner accepted adverse '+label)
   finally:p.write_bytes(old)
 # Real explicit mathematical forced-failure guard in each mode.
 for opt in [False,True]:
  q=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(R/'check_arrangement.py'),'--force-failure'],capture_output=True,text=True)
  if q.returncode==0 or 'explicit forced failure remains active under -O' not in q.stderr:raise RuntimeError('new control failure guard not active')
  rows.append({'control':'new_independent_math_forced_failure','optimized':opt,'exit_code':q.returncode,'intended_failure_seen':True})
result={'status':'PASS','python':sys.version,'runner_adverse_cases':rows,'new_math_normal_optimized_byte_equal':(R/'RESULTS.normal.json').read_bytes()==(R/'RESULTS.optimized.json').read_bytes(),'new_math_requirements':json.loads((R/'RESULTS.normal.json').read_text())['requirements'],'new_math_adverse_count':len(json.loads((R/'RESULTS.normal.json').read_text())['adverse_controls'])}
(R/'ADVERSE_AND_RUN_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))

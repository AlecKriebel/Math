#!/usr/bin/env python3
"""Reproduce normal, optimized, and corrupted mathematical checks without assertions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
checker=root/'verify_scope.py'
run_dir=root/'harness_runs';run_dir.mkdir(exist_ok=True)
records=[]
for label,opt,corrupt,receipt_name in [
 ('normal',False,False,'CHECKS.json'),
 ('optimized',True,False,'CHECKS_OPTIMIZED.json'),
 ('corrupt_normal',False,True,'CORRUPT_NORMAL_SHOULD_NOT_EXIST.json'),
 ('corrupt_optimized',True,True,'CORRUPT_OPTIMIZED_SHOULD_NOT_EXIST.json')]:
 receipt=root/receipt_name
 if corrupt and receipt.exists():raise RuntimeError('Negative receipt path must begin absent')
 cmd=[sys.executable]+(['-O'] if opt else [])+[str(checker),'--receipt',str(receipt)]
 if corrupt:cmd.append('--corrupt-annihilator')
 r=subprocess.run(cmd,cwd=root,text=True,capture_output=True)
 stdout=run_dir/(label+'.stdout.txt');stderr=run_dir/(label+'.stderr.txt')
 stdout.write_text(r.stdout);stderr.write_text(r.stderr)
 record={'label':label,'command':cmd,'exit_code':r.returncode,'stdout_file':str(stdout.relative_to(root)),'stderr_file':str(stderr.relative_to(root)),'stdout_sha256':hashlib.sha256(stdout.read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(stderr.read_bytes()).hexdigest(),'receipt_created':receipt.exists()}
 if corrupt:
  if r.returncode==0 or 'PASS' in r.stdout or 'PASS' in r.stderr or receipt.exists():raise RuntimeError('Corrupted mathematical condition did not fail closed')
  if 'Mathematical check' not in r.stderr or 'failed' not in r.stderr:raise RuntimeError('Failure was not an explicit mathematical-check failure')
  record['expected_mathematical_failure']=True
 else:
  if r.returncode!=0:raise RuntimeError('Valid checker run failed: '+r.stderr)
  value=json.loads(receipt.read_text())
  if value.get('status')!='PASS' or value.get('exact_controls')!=3788 or value.get('negative_control_requested') is not False:raise RuntimeError('Unexpected positive run receipt')
  expected_opt=1 if opt else 0
  if value.get('python_optimization_level')!=expected_opt:raise RuntimeError('Optimization mode was not exercised')
  record.update({'receipt_file':receipt_name,'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),'exact_controls':value['exact_controls'],'optimization_level':value['python_optimization_level']})
 records.append(record)
validation={'completed_utc':datetime.now(timezone.utc).isoformat(),'validation_status':'PASS','checker_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),'python_executable':sys.executable,'python_version':sys.version,'python_executable_sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),'positive_control_counts':[r['exact_controls'] for r in records if 'exact_controls' in r],'negative_control':'Falsely require Ann(B3) to contain nonzero r=(1,0). Both ordinary and optimized runs must fail with no PASS and no receipt.','runs':records}
(root/'HARNESS_VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps({'validation_status':'PASS','normal_controls':3788,'optimized_controls':3788,'corrupted_normal_exit':records[2]['exit_code'],'corrupted_optimized_exit':records[3]['exit_code'],'corrupted_outputs_contain_PASS':False,'negative_receipts_created':False},indent=2))

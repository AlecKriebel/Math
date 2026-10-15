#!/usr/bin/env python3
import hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE/'extract/support_slit_verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
results=[]
for num,job in enumerate(json.loads((ROOT/'JOBS.json').read_text()),1):
 with tempfile.TemporaryDirectory(prefix='isolated-job-',dir=HERE) as directory:
  scratch=Path(directory)
  for n in ['original','reviews','root_reproduction']:shutil.copytree(ROOT/n,scratch/n,ignore=shutil.ignore_patterns('__pycache__'))
  script=scratch/job['script'];p=subprocess.run([str(HERE/'venv/bin/python'),str(script)],cwd=script.parent,env=dict(os.environ,PYTHONPATH=str(HERE/'offline_guard'),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
  assert p.returncode==0,(job['script'],p.stderr)
  stdout=json.loads(p.stdout);actual=stdout
  if 'generated_record' in job:
   assert stdout==json.loads((ROOT/job['stdout_record']).read_text())
   actual=json.loads((scratch/job['generated_record']).read_text())
  wanted=json.loads((ROOT/job['record']).read_text())
  ignored=job.get('ignored_dynamic_fields',[])
  assert ignored==[] or (job['script']=='reviews/source01/check_source_bridge.py' and ignored==['checked_at_utc'])
  for k in ignored:
   assert k in actual and k in wanted
   del actual[k];del wanted[k]
  assert actual==wanted,job['script']
  results.append({'job':num,'script':job['script'],'full_json_equal':True,'ignored_dynamic_fields':ignored,'compared_json_sha256':sha(json.dumps(actual,sort_keys=True,separators=(',',':')).encode()),'stdout_sha256':sha(p.stdout.encode()),'generated_record_compared':job.get('generated_record'),'stderr_bytes':len(p.stderr)})
(HERE/'INDEPENDENT_REPLAY.json').write_text(json.dumps({'status':'PASS','jobs':results,'isolated_scratch_per_job':True,'fresh_venv_mpmath':'1.4.1','network_denied':True,'method':'Independent replay implementation, full JSON comparison; no import of package runner.'},indent=2)+'\n')
print('PASS',len(results))

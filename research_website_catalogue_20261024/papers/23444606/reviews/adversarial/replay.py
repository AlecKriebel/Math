"""Isolated, unmodified published mathematical diagnostic; no historical opinions."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
O=Path(__file__).resolve().parent;P=O.parents[1]
B=P/'sources/published-source/initial-omnific-models-source-and-verification'
program=B/'draft_pr_actual_claims_1100_1200_20261017/audits/pr1151_30003321/verify_finite_signs.py'
raw=program.read_bytes();h=hashlib.sha256(raw).hexdigest()
copy=O/'cache/unmodified_replay/verify_finite_signs.py';copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes(raw)
assert hashlib.sha256(copy.read_bytes()).hexdigest()==h
expected=(B/'verification/EXPECTED_FINITE_SIGNS.stdout.json').read_bytes()
mutations={'omit_deletion':'ValueError: explicit inverse failure','keep_minimum':'ValueError: rotation collision','append_plus':'ValueError: rotation collision','omit_scaling':'ValueError: bottom source generator does not map to target unit'}
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
records=[]
for optimized in (False,True):
 cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(copy)]
 for mutation in [None,*mutations]:
  args=cmd+(['--mutation',mutation] if mutation else [])
  r=subprocess.run(args,cwd=copy.parent,env=env,capture_output=True,timeout=90)
  stem=('optimized' if optimized else 'normal')+'-'+(mutation or 'positive')
  (O/'cache'/f'{stem}.stdout').write_bytes(r.stdout);(O/'cache'/f'{stem}.stderr').write_bytes(r.stderr)
  if mutation:assert r.returncode==1 and not r.stdout and r.stderr.decode().splitlines()[-1]==mutations[mutation]
  else:assert r.returncode==0 and not r.stderr and r.stdout==expected
  records.append({'mode':'optimized' if optimized else 'normal','mutation':mutation,'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'actual_mathematical_failure':r.stderr.decode().splitlines()[-1] if mutation else None,'positive_output':json.loads(r.stdout) if not mutation else None})
assert program.read_bytes()==raw and copy.read_bytes()==raw
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'program_path':str(program.relative_to(P)),'program_sha256':h,'copy_unmodified':True,'positive_runs':2,'wrong_construction_failures':8,'full_historical_wrapper_run':False,'records':records,'finite_only_not_ordinal_or_class_proof':True}
(O/'replay-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'positive_runs':2,'negative_runs':8,'program_sha256':h,'finite_only':True}))

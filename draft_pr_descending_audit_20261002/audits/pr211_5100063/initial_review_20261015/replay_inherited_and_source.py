"""Replay inspected controls in isolated directories; preserve every input byte."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import shutil, subprocess, json, hashlib, datetime, os
D=Path(__file__).resolve().parent
S=D/'submitted/unsolved_math_prioritization/attempts/5100063'
PY='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
tasks=[('inherited_independent',S/'independent_review','independent_check.py','INDEPENDENT_CHECKS.json'),('new_source',D/'source_scope_adversary_01','source_geometry_check.py','source_geometry_checks.json')]
def replay(task):
 label,source,program,receipt=task
 target=D/'root_reproduction'/label;target.mkdir(parents=True,exist_ok=False)
 shutil.copyfile(source/program,target/program)
 before=hashlib.sha256((source/receipt).read_bytes()).hexdigest()
 p=subprocess.run([PY,'-B',str(target/program)],capture_output=True,text=True,timeout=600,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 (target/'stdout.txt').write_text(p.stdout);(target/'stderr.txt').write_text(p.stderr)
 assert p.returncode==0,p.stderr
 actual=(target/receipt).read_bytes();expected=(source/receipt).read_bytes()
 assert json.loads(actual)==json.loads(expected),(label,'receipt mismatch')
 assert hashlib.sha256(expected).hexdigest()==before
 return dict(label=label,semantic_exact_replay=True,byte_identical=actual==expected,program_sha256=hashlib.sha256((source/program).read_bytes()).hexdigest(),receipt_sha256=hashlib.sha256(actual).hexdigest(),input_receipt_unchanged=True,counts=json.loads(actual))
with ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(replay,tasks))
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',isolated_replays=rows,original_inputs_unchanged=True)
(D/'ROOT_ADDITIONAL_REPLAYS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({**result,'isolated_replays':[{k:v for k,v in r.items() if k!='counts'} for r in rows]},indent=2))

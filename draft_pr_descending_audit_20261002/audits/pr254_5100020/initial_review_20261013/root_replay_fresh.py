from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json,subprocess,shutil,hashlib
D=Path(__file__).resolve().parent;R=D/'root_fresh_reproduction';R.mkdir(exist_ok=True)
PYTHON='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
tasks=[('complex_exact','meromorphic_adversary_01/fresh_exact_checks.py','meromorphic_adversary_01/EXACT_CHECKS.json',None),('complex_poles','meromorphic_adversary_01/fresh_near_pole_diagnostics.py','meromorphic_adversary_01/NEAR_POLE_DIAGNOSTICS.json',None),('cartesian_exact','geometric_adversary_01/cartesian_exact_checks.py','geometric_adversary_01/CARTESIAN_EXACT_CHECKS.json','CARTESIAN_EXACT_CHECKS.json'),('cartesian_numeric','geometric_adversary_01/cartesian_numeric_checks.py','geometric_adversary_01/CARTESIAN_NUMERIC_CHECKS.json','CARTESIAN_NUMERIC_CHECKS.json')]
def run(task):
 name,src,expected,outname=task;o=R/name;o.mkdir(exist_ok=True);script=o/Path(src).name;shutil.copyfile(D/src,script)
 sha=hashlib.sha256(script.read_bytes()).hexdigest()
 r=subprocess.run([PYTHON,str(script)],capture_output=True);(o/'stdout.json').write_bytes(r.stdout);(o/'stderr.txt').write_bytes(r.stderr);assert r.returncode==0,(name,r.stderr.decode())
 got=json.loads((o/outname).read_text()) if outname else json.loads(r.stdout);want=json.loads((D/expected).read_text())
 for x in [got,want]:
  for key in ['utc','elapsed_seconds']:x.pop(key,None)
 assert got==want,name
 assert hashlib.sha256((D/src).read_bytes()).hexdigest()==sha,'Reviewer code changed during root replay'
 return {'program':name,'status':'PASS','copied_script_sha256':sha,'semantic_receipt_match':True,'ignored_fields':['utc','elapsed_seconds'],'reviewer_outputs_unchanged':True}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,tasks))
x={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','runs':results,'diagnostics_are_not_universal_proof':True};(R/'ROOT_FRESH_REPLAY.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))

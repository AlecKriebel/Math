from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,shutil
D=Path(__file__).resolve().parent;S=D/'submitted/unsolved_math_prioritization/attempts/5100020';R=D/'root_reproduction';R.mkdir(exist_ok=True)
PYTHON='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
for name in ['FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json','independent_review/REVIEW_MANIFEST.json']:
 m=json.loads((S/name).read_text());files=m['files'];files=files if isinstance(files,list) else [{'path':p,'sha256':h} for p,h in files.items()]
 base=S/'independent_review' if name.startswith('independent_review/') else S
 for x in files:
  path=base/x['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==x['sha256'],(name,x['path'])
(R/'MANIFEST_VALIDATION.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','manifests':['FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json','independent_review/REVIEW_MANIFEST.json']},indent=2)+'\n')
programs=[('author_exact','check_exact.py','exact_receipt.json'),('author_numeric','check_numerical.py','numerical_receipt.json'),('old_independent_exact','independent_review/independent_checks.py','independent_review/INDEPENDENT_CHECKS.json'),('old_independent_numeric','independent_review/independent_diagnostics.py','independent_review/INDEPENDENT_DIAGNOSTICS.json')]
def run(t):
 name,script,receipt=t;o=R/name;o.mkdir(exist_ok=True);f=o/Path(script).name;shutil.copyfile(S/script,f)
 r=subprocess.run([PYTHON,str(f)],capture_output=True);(o/'stdout.json').write_bytes(r.stdout);(o/'stderr.txt').write_bytes(r.stderr);assert r.returncode==0,(name,r.stderr.decode())
 assert r.stdout==(S/receipt).read_bytes(),name
 return {'program':name,'status':'PASS','receipt_byte_identical':True,'script_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'assertions':json.loads(r.stdout).get('assertions',json.loads(r.stdout).get('exact_assertions'))}
with ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(run,programs))
r={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','original_snapshot_unmodified':True,'runs':result}
(R/'REPLAY_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

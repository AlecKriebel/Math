#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import subprocess,os,json,hashlib,concurrent.futures
O=Path(__file__).resolve().parent
B=O.parent/'submitted/unsolved_math_prioritization/attempts/5100026'
V=O.parents[3]/'pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor'
# Explicit absolute path avoids any directory-hierarchy assumptions for runtime.
V=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor')
def pin(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def replay(name,rel):
    src=B/rel;work=O/'replays'/name;work.mkdir(parents=True,exist_ok=True);dst=work/src.name;dst.write_bytes(src.read_bytes())
    env=os.environ.copy();env['PYTHONPATH']=str(V);env.pop('PYTHONOPTIMIZE',None)
    started=datetime.now(timezone.utc).isoformat();p=subprocess.run(['/opt/homebrew/bin/python3',str(dst)],cwd=work,env=env,capture_output=True)
    (work/'stdout.json').write_bytes(p.stdout);(work/'stderr.txt').write_bytes(p.stderr)
    result={'name':name,'source':str(src),'source_pin':pin(src),'copy':str(dst),'copy_pin':pin(dst),'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':p.returncode,'stdout':pin(work/'stdout.json'),'stderr':pin(work/'stderr.txt'),'library_root':str(V),'optimization_disabled':True}
    try:result['observed_result']=json.loads(p.stdout)
    except Exception:result['parse_error']=True
    (work/'RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');return result
jobs=[('author_exact','verify_exact.py'),('author_numeric','verify_numeric.py'),('review_exact','independent_review/independent_exact.py'),('review_numeric','independent_review/independent_numeric.py')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(lambda j:replay(*j),jobs))
(O/'ORIGINAL_REPLAY_RECEIPTS.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results:print(r['name'],r['exit_code'],r.get('observed_result',{}).get('status'),r['stdout'])
assert all(r['exit_code']==0 and r.get('observed_result',{}).get('status')=='PASS' for r in results)

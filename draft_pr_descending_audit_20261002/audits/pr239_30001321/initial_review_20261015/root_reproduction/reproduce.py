from pathlib import Path
from datetime import datetime, timezone
import subprocess,json,shutil,hashlib,sys
D=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr239_30001321/initial_review_20261015')
S=D/'submitted/unsolved_math_prioritization/attempts/30001321'
R=D/'root_reproduction'; R.mkdir(exist_ok=False)
py=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python')
ver=subprocess.run([str(py),'-c','import sys,sympy; print(sys.version); print("SymPy",sympy.__version__)'],capture_output=True,check=True)
(R/'runtime.txt').write_bytes(ver.stdout)
results=[]
for label,program,expected in [('turn1','check_turn1.py','turn1_receipt.json'),('turn2','check_turn2.py','turn2_receipt.json'),('turn3','check_turn3.py','turn3_receipt.json'),('inherited_independent','independent_review/independent_check.py','independent_review/independent_check.json')]:
    W=R/label;shutil.copytree(S,W/'source')
    start=datetime.now(timezone.utc).isoformat()
    r=subprocess.run([str(py),program],cwd=W/'source',capture_output=True,timeout=300)
    end=datetime.now(timezone.utc).isoformat()
    (W/'stdout.json').write_bytes(r.stdout); (W/'stderr.txt').write_bytes(r.stderr)
    want=(S/expected).read_bytes()
    item={'program':program,'start_utc':start,'end_utc':end,'returncode':r.returncode,'empty_stderr':not r.stderr,'expected_receipt':expected,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'complete_stdout_byte_identical':r.stdout==want,'program_sha256':hashlib.sha256((S/program).read_bytes()).hexdigest()}
    if r.returncode==0: item['actual_output']=json.loads(r.stdout)
    results.append(item)
    (W/'REPLAY_RECEIPT.json').write_text(json.dumps(item,indent=2)+'\n')
    print(json.dumps(item),flush=True)
    assert r.returncode==0 and not r.stderr and r.stdout==want,item
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','all_four_unchanged_actual_programs_executed':True,'full_stdout_bytes_compared':True,'runtime':ver.stdout.decode(),'results':results,'scope':'Finite exact rational controls; not proofs of asymptotic estimates'}
(D/'ROOT_ORIGINAL_REPLAY_ACCEPTANCE.json').write_text(json.dumps(receipt,indent=2)+'\n')
shutil.copy2('/tmp/pr239_root_replay_20261015.py',R/'reproduce.py')

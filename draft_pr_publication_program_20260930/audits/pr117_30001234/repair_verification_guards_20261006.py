"""Repair disabled assertion guards only; mathematical candidate unchanged."""
from pathlib import Path
import datetime,hashlib,json,os,shutil
A=Path(__file__).resolve().parent
O=A/'original_head_authentication_20261006/original_attempt'
D=A/'repaired_diagnostics_v1'
def require(value,label):
    if not value:raise ValueError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
require(not D.exists(),'Existing effective diagnostic: inspect before retry')
D.mkdir()
shutil.copyfile(O/'CANDIDATE.md',D/'CANDIDATE.md')
author=(O/'verify.py').read_text()
independent=(O/'review/independent_checks.py').read_text()
require(author.count(' assert b\n')==1,'Exact author guard')
require(independent.count('    assert b,name\n')==1,'Exact independent guard')
(D/'verify.py').write_text(author.replace(' assert b\n',' if not b:raise ValueError("Exact verification guard failed")\n'))
(D/'independent_checks.py').write_text(independent.replace('    assert b,name\n','    if not b:raise ValueError(name)\n'))
(D/'author_replay').mkdir()
shutil.copyfile(O/'CANDIDATE.md',D/'author_replay/CANDIDATE.md')
record={'schema':'pr117-verification-guard-repair/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_operator_PID':os.getpid(),'proof_unchanged':True,'CANDIDATE_sha256':sha(D/'CANDIDATE.md'),
    'repair':'Replace only both ck assertion statements with explicit ValueError guards. Numerical/algebraic logic unchanged.',
    'original_author_checker_sha256':sha(O/'verify.py'),'effective_author_checker_sha256':sha(D/'verify.py'),
    'original_independent_checker_sha256':sha(O/'review/independent_checks.py'),'effective_independent_checker_sha256':sha(D/'independent_checks.py'),
    'normal_and_optimized_validation_pending':True,'new_central_proof_search_turns':0}
(D/'REPAIR.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps(record,sort_keys=True))

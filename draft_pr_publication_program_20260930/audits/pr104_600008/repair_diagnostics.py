"""Preserve the proof and repair the submitted diagnostic assertion guards."""
from pathlib import Path
import json,hashlib,datetime,os
A=Path(__file__).resolve().parent
O=A/'original_source_authentication_20261006/original_attempt'
D=A/'repaired_diagnostics_v1';D.mkdir(exist_ok=False)
(D/'author_replay').mkdir()
def require(value,message):
    if not value:raise RuntimeError(message)
files=[]
for relative,destination,old,new in [
 ('verify.py','verify.py',' assert bool(b),k',' if not bool(b):raise RuntimeError(k)'),
 ('review/independent_checks.py','independent_checks.py','    assert bool(value),name','    if not bool(value):raise RuntimeError(name)')]:
    source=(O/relative).read_text();require(source.count(old)==1,'unique guard')
    repaired=source.replace(old,new)
    (D/destination).write_text(repaired)
    files.append({'original':relative,'original_sha256':hashlib.sha256(source.encode()).hexdigest(),'repaired':destination,'repaired_sha256':hashlib.sha256(repaired.encode()).hexdigest(),'change':'explicit failure guard replaces optimizable assertion'})
body=(O/'ANALYTIC_CRITERION.md').read_bytes()
for destination in ['ANALYTIC_CRITERION.md','author_replay/ANALYTIC_CRITERION.md']:(D/destination).write_bytes(body)
(D/'README.md').write_text('# Repaired PR104 diagnostics\n\nThe mathematical proof is byte-identical to the submitted candidate. Both diagnostic check functions now reject false conditions normally and under Python -O. The original checkers and receipts remain preserved separately. The original independent checker writes independent_results.json in its own copied directory; use this diagnostic folder only. Counts are bounded diagnostic evidence, not a proof of global analytic claims. These code repairs establish no priority or publication clearance.\n')
(D/'REPAIR.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'files':files,'proof_sha256':hashlib.sha256(body).hexdigest(),'original_budget':'1/5','new_central_proof_search_turns':0,'mathematical_proof_changed':False},indent=2)+'\n')
print(json.dumps({'folder':str(D),'repaired_guards':2,'proof_changed':False}))

from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parents[1]
O=A/'original_submission/files/unsolved_math_prioritization/attempts/30002720'
R=A/'root_reproduction';S=R/'scratch/author_independent';S.mkdir(parents=True,exist_ok=True)
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
def require(x,msg):
 if not x:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
source=(O/'review/independent_checks.py').read_text()
needle='    assert condition,group'
require(source.count(needle)==1,'Guard source differs')
repaired=source.replace(needle,'    if not condition: raise RuntimeError(group)')
(R/'independent_checks_raised.py').write_text(repaired)
mutations={'changed_source':'q=F(3,4)','wrong_first_square':'r>=4 and isqrt(r)**2==r','charged_final_singleton':'    return total\n\ndef count_cost'}
replacements={'changed_source':'q=F(4,5)','wrong_first_square':'r>=9 and isqrt(r)**2==r','charged_final_singleton':'    return total+1\n\ndef count_cost'}
receipt=dict(UTC=datetime.now(timezone.utc).isoformat(),scope='Reproduce historical 44,602 finite diagnostics; robustness of original and explicit-exception repair. No finite controls prove the asymptotic theorem.',original_inputs=[pin(O/'review/independent_checks.py'),pin(O/'COUNTEREXAMPLE.md'),pin(O/'review/independent_results.json')],repaired_checker=pin(R/'independent_checks_raised.py'),runs=[])
for family,body in [('original',source),('repaired',repaired)]:
 for mutation in [None]+list(mutations):
  altered=body if mutation is None else body.replace(mutations[mutation],replacements[mutation])
  if mutation is not None:require(altered!=body,'Missing mutation')
  for optimize in [False,True]:
   folder=S/(family+'_'+str(mutation)+'_'+str(optimize));folder.mkdir(exist_ok=True)
   (folder/'author_replay').mkdir(exist_ok=True)
   (folder/'author_replay/COUNTEREXAMPLE.md').write_bytes((O/'COUNTEREXAMPLE.md').read_bytes())
   p=folder/'independent_checks.py';p.write_text(altered)
   proc=subprocess.run([PY,'-E','-S','-B','-P']+(['-O'] if optimize else [])+[str(p)],capture_output=True,text=True,timeout=60)
   out=folder/'independent_results.json'
   result=json.loads(out.read_text()) if out.exists() else None
   row=dict(family=family,mutation=mutation,optimized=optimize,returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr,receipt_created=out.exists(),receipt=result,executed_source=pin(p))
   if mutation is None:
    require(proc.returncode==0 and result and result['status']=='PASS' and result['assertions']==44602 and result['adaptive_selection_cases']==6732,'Baseline reproduction failed')
    row['historical_receipt_byte_identical']=out.read_bytes()==(O/'review/independent_results.json').read_bytes()
    require(row['historical_receipt_byte_identical'],'Historical diagnostic receipt differs')
   elif family=='repaired' or not optimize:
    require(proc.returncode!=0 and not out.exists(),'False mutation accepted')
   else:
    require(proc.returncode==0 and result and result['status']=='PASS','Expected original optimized assert weakness not reproduced')
    row['false_pass_with_original_optimized_assertions']=True
   receipt['runs'].append(row)
receipt.update(status='PASS_REPRODUCED_ORIGINAL_AND_REPAIR_WITH_SIX_REPAIRED_NEGATIVE_EXECUTIONS',repaired_negative_modes_detected=6,original_optimized_false_passes=3,baseline_checks_per_mode=44602,adaptive_selection_cases_per_mode=6732)
target=R/'AUTHOR_INDEPENDENT_REPRODUCTION_AND_NEGATIVES.json';target.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(status=receipt['status'],checks=44602,adaptive_cases=6732,original_optimized_false_passes=3,repaired_negative_modes_detected=6,receipt=pin(target)),indent=2))


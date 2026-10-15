#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,sys
r=Path(__file__).resolve().parent
base=(r/'check_degree_two.py').read_text(); folder=r/'mutations'; folder.mkdir(exist_ok=True)
mutants=[
('wrong_magnus','(2, 3): Fraction(1)','(2, 3): Fraction(-1)','original checker line 70'),
('erased_rational_plat','[1, r, r * r, 0, 0, 1]','[1, r, r * r, 0, 0, 0]','original checker line 103'),
('collapsed_component_values','det([[1, 5], [5, 1]])','det([[1, 1], [1, 1]])','original checker line 96')]
results=[]
for name,old,new,expected in mutants:
 if old not in base:raise RuntimeError('mutation target absent '+name)
 path=folder/(name+'.py'); path.write_text(base.replace(old,new,1))
 for optimized in (False,True):
  cmd=[sys.executable]+(['-O'] if optimized else [])+[str(path)]
  completed=subprocess.run(cmd,capture_output=True,text=True)
  passed=completed.returncode!=0 and expected in completed.stderr
  results.append({'name':name,'optimized':optimized,'expected_guard':expected,'exit_code':completed.returncode,'intended_rejection':passed,'stderr':completed.stderr})
  if not passed:raise RuntimeError('negative control did not fail at expected guard '+name)
out={'utc':datetime.now(timezone.utc).isoformat(),'scope':'new independent finite-algebra sensitivity checks only','all_intended_rejections':all(x['intended_rejection'] for x in results),'results':results}
(r/'MUTATION_RESULT.json').write_text(json.dumps(out,indent=2)+'\n'); print('Rejected all',len(results),'new negative controls at intended guards')
a,b=[json.loads((r/n).read_text()) for n in ['normal_run.json','optimized_run.json']]
a.pop('utc');b.pop('utc')
if a!=b:raise RuntimeError('normal/optimized semantic mismatch')
print('Baseline normal/optimized results semantically equal')

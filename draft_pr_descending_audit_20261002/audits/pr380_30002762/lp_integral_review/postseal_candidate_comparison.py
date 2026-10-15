#!/usr/bin/env python3
"""Post-seal comparison only: candidate execution is explicit and separately recorded."""
from pathlib import Path
from fractions import Fraction
import contextlib,io,json,runpy,random
import independent_exact_controls as independent
p=Path(__file__).resolve().parent
candidate=p/'ignoredprivate/frozen_snapshot/problems/30002762_conjugation_norms/check_turn_4.py'
stream=io.StringIO()
with contextlib.redirect_stdout(stream):ns=runpy.run_path(str(candidate))
compare=[]
sealed=json.loads((p/'independent_exact_results.json').read_text())
for case in sealed['cases']:
    v=case['element'];R=case['relations'];d=len(v);S=[[int(i==j) for i in range(d)] for j in range(d)]
    value,_,_,_=independent.primal_dual(R,S,v);got=ns['compute'](R,v);assert value==got
    compare.append({'case':case['name'],'generator_norm':'presentation generators','independent':str(value),'candidate':str(got)})
rng=random.Random(380991)
for i in range(100):
    d=rng.randrange(1,5);R=[[rng.randrange(-7,8) for _ in range(d)] for _ in range(rng.randrange(d+3))];v=[rng.randrange(-5,6) for _ in range(d)];S=[[int(i==j) for i in range(d)] for j in range(d)]
    value,_,_,_=independent.primal_dual(R,S,v);got=ns['compute'](R,v);assert value==got
    compare.append({'case':'additional_%d'%i,'relations':R,'element':v,'independent':str(value),'candidate':str(got)})
assert ns['compute']([],[])==0
assert ns['compute']([[0,0],[0,0]],[1,-2])==3
r={'postseal':True,'candidate_executed':str(candidate),'initial_candidate_stdout':stream.getvalue(),'cases':compare,'comparison_count':len(compare),'d_zero_and_zero_dependency_edges':True,'all_passed':True,'historical_review_not_used_as_evidence':True}
(p/'postseal_candidate_comparison_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'comparison_count':len(compare),'d_zero_and_zero_dependency_edges':True,'all_passed':True},indent=2))

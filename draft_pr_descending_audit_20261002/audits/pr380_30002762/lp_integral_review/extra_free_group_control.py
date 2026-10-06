#!/usr/bin/env python3
"""Candidate-free, post-seal negative control for omitting bounded-derived input."""
import random,json
from pathlib import Path
p=Path(__file__).resolve().parent

def reduce(w):
    out=[]
    for x in w:
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return tuple(out)
def inverse(w):return tuple(-x for x in reversed(w))
def phi(w):
    return sum(1 if pair==(1,2) else -1 if pair==(-2,-1) else 0 for pair in zip(w,w[1:]))
rng=random.Random(380882);checks=0;maxdef=0
for i in range(30000):
    u=reduce([rng.choice([-2,-1,1,2]) for _ in range(rng.randrange(51))]);v=reduce([rng.choice([-2,-1,1,2]) for _ in range(rng.randrange(51))])
    defect=abs(phi(reduce(u+v))-phi(u)-phi(v));assert defect<=3;maxdef=max(maxdef,defect)
    assert phi(inverse(u))==-phi(u);checks+=2
w=(1,2,-1,-2)
for n in range(1,201):
    assert phi(reduce(w*n))==n;assert sum(w*n)==0;checks+=2
for s in [1,-1,2,-2]:
    for n in range(1,201):assert phi((s,)*n)==0;checks+=1
r={'postseal':True,'candidate_imports':[],'random_seed':380882,'assertions':checks,'random_defect_pairs':30000,'largest_observed_defect':maxdef,'commutator_power_range':[1,200],'abelian_exponent_vector':[0,0],'homogenized_count_value_on_commutator':1,'rigorous_defect_bound_from_cancellation_proof':3,'homogenized_defect_bound':6,'derived_subgroup_unbounded':True,'stable_group_norm_lower_bound':'1/6','abelian_lp_value':'0','all_passed':True,'scope':'Exact controls supplement the written cancellation proof; finite observations alone do not establish the defect bound.'}
(p/'extra_free_group_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

#!/usr/bin/env python3
"""Excluded-boundary falsification controls; no infinite-time numerical claim."""
from fractions import Fraction as F
from pathlib import Path
import json, datetime
checks=0
def ck(x):
    global checks
    assert x
    checks+=1
# An excluded iid arrow law has delta=0; replica equality is absorbing.
d={0:F(1)}
for n in range(129):
    ck(d.get(0,F(0))==1 and sum((mass for x,mass in d.items() if x!=0),F(0))==0)
    nxt={}
    for x,mass in d.items():
        rate=F(0) if x==0 else F(1,4)
        for dx,prob in ((-1,rate),(0,1-2*rate),(1,rate)):
            if mass*prob:nxt[x+dx]=nxt.get(x+dx,F(0))+mass*prob
    d=nxt
# A general birth-death kernel can lack zero maximality; source delta<=a matters.
a=F(1,4); delta=F(1,2)
u1zero=1-2*delta
u1one=a
ck(u1one>u1zero)
ck(a-delta<0) # Such parameters cannot arise as Var(p)=a-delta.
# Endpoint laws from starting points of opposite parity are disjoint at all times.
for n in range(65):
    from_zero=set(range(-n,n+1,2))
    from_one=set(range(1-n,2+n,2))
    ck(from_zero.isdisjoint(from_one))
# In a deterministic-arrow environment the quenched coarse L1 distance equals
# 2(1-alpha(cell of its endpoint)); max alpha(cell)<=M*max binomial mass.
# At n=128, M=2 the exact bound already forces a large deterministic discrepancy.
from math import comb
n=128
maxmass=F(comb(n,n//2),2**n)
lower=2*(1-2*maxmass)
ck(lower>F(17,10))
x={"schema":"independent-pr239-excluded-boundary-controls-v1","UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","checks":checks,"excluded_arrow_delta_zero_g_through_128":"1 exactly","unphysical_delta_gt_a_zero_maximality_counterexample":{"a":str(a),"delta":str(delta),"u1_zero":str(u1zero),"u1_one":str(u1one)},"opposite_parity_disjoint_through_64":True,"excluded_arrow_n128_M2_deterministic_coarse_L1_lower_bound":str(lower),"interpretation":"These are successful controls against overextending the proof. They do not counterexample its fixed strictly elliptic same-parity scope."}
Path(__file__).with_name("BOUNDARY_RESULTS.json").write_text(json.dumps(x,indent=2)+"\n")
print(json.dumps({"status":"PASS","checks":checks}))

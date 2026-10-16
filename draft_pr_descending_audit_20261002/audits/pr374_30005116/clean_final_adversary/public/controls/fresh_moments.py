#!/usr/bin/env python3
"""Original exact controls for the full [0,1] three-moment region."""
from fractions import Fraction as Q
from itertools import product
import json
from source_first_counts import direct
from fresh_adversarial import bounded

def moments(values,weights):
    return tuple(sum(w*x**j for w,x in zip(weights,values)) for j in (1,2,3))

cases=0;equalities=0;strictgaps=0
for j in range(1,10):
    m=Q(j,10);p=m*m
    for k in range(5):
        s=m*m+Q(k,4)*(m-m*m)
        c=s/m;lowweight=m*m/s
        lowv=[Q(0),c];loww=[1-lowweight,lowweight]
        d=(m-s)/(1-m);upperweight=(m-d)/(1-d)
        upperv=[d,Q(1)];upperw=[1-upperweight,upperweight]
        assert moments(lowv,loww)==(m,s,s*s/m)
        assert moments(upperv,upperw)==(m,s,s-(m-s)**2/(1-m))
        equalities+=2
        for l in range(5):
            alpha=Q(l,4);values=lowv+upperv;weights=[alpha*w for w in loww]+[(1-alpha)*w for w in upperw]
            mm,ss,t=moments(values,weights)
            assert mm==m and ss==s and s*s/m<=t<=s-(m-s)**2/(1-m)
            w=[[x*y for y in values] for x in values]
            pp,q=direct(w,weights)
            assert pp==p and q==3*(s*s-t*t)**2
            R=Q(3,16)*p*p if p<=Q(1,2) else 3*p**4*(1-p)**2
            assert q<=R
            cases+=1
    R=Q(3,16)*p*p if p<=Q(1,2) else 3*p**4*(1-p)**2
    gap=Q(21,16)*p*p if p<=Q(1,2) else Q(141,256)*(1-p)**2 if p<=Q(3,4) else Q(1653,1024)*(1-p)**3
    bounded(p,R+gap);assert gap>0;strictgaps+=1
# Endpoints enforce deterministic f. Interior vertical laws at d=1 realize zero.
for m in (Q(0),Q(1)):
    p,q=direct([[m*m]],[Q(1)])
    assert p==m*m and q==0
print(json.dumps({'status':'PASS','moment_region_mixtures':cases,'boundary_laws':equalities,'strict_gap_cases':strictgaps,'endpoint_cases':2,'scope':'exact controls; arbitrary measurable proof and equality in mathematical_verdict.md'},sort_keys=True))

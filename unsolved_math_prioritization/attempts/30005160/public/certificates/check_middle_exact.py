#!/usr/bin/env python3
"""Corrected exact finite certificate. Retains factor N+3h.
The infinite bound is analytic in CUBIC_MIDDLE_DOMINANT_PROOF.md.
"""
from fractions import Fraction as F
from math import factorial as fac, comb
import json
records=[]
small=F(0)
cases=0
for N in range(3,100):
    values=[]
    for R in range(N+1):
        S=N-R
        total=F(0)
        for h in range(min(R//2,S)+1):
            n=N-3*h
            if n<3: continue
            den=fac(R+2*h+2)*fac(R-2*h)*fac(S+h+1)*fac(S-h)
            total+=F(2*fac(N+3*h)*fac(n-3),den)
            cases+=1
        values.append(total/comb(2*N,2*R))
    maximum=max(values)
    small+=maximum
    records.append({'N':N,'maximum':str(maximum),'maximizing_R':values.index(maximum),'ratios_by_R':[str(v) for v in values]})
assert small<F(7,125)
negative=F(3,2)*(F(7,125)+F(236,99**2))+F(1,8)
assert negative==F(800803,3267000) and negative<F(1,4)
result={'verdict':'PASS','coefficient_cases':sum(n+1 for n in range(3,100)),'resonance_cases':cases,'small_sum':str(small),'small_bound':'7/125','negative_upper_bound':str(negative),'gap_below_one_quarter':str(F(1,4)-negative),'records':records}
print(json.dumps(result,indent=2))

#!/usr/bin/env python3
"""Exact finite controls; the universal proof is TURN_1.md, not this sample."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, factorial
import json
checks=0
triples=0
for n in range(3,13):
    d=Q(1,16*n*n)
    intervals=[(Q(4*i+1,4*n),Q(4*i+3,4*n)) for i in range(n)]
    for lo,hi in intervals:
        assert lo*lo-d>=0 and hi*hi+d<1
        assert (hi-lo)*2*d==Q(1,16*n**3)
        checks+=2
    for i,j,k in combinations(range(n),3):
        triples+=1
        for x,y,z in product(intervals[i],intervals[j],intervals[k]):
            for ex,ey,ez in product((-d,d),repeat=3):
                D=(y-x)*(z-x)*(z-y)+ex*(z-y)-ey*(z-x)+ez*(y-x)
                assert D>=Q(1,8*n*n)*(z-x)>0
                checks+=1
for j in range(2,1001):
    R=1+comb(j,2)+j*(j-2)+(3*comb(j,4) if j>=4 else 0)
    t=j-2
    assert 128*R-(j+1)**4==15*t**4+20*t**3+122*t*t+308*t+175>0
    checks+=1
# Exact polynomial identity by interpolation (degree four, five nodes).
for j in range(2,7):
    R=Q(j**4-6*j**3+23*j*j-26*j+8,8)
    assert R==1+comb(j,2)+j*(j-2)+(3*comb(j,4) if j>=4 else 0)
    checks+=1
# Recurrence and the accumulated numerical constant, no floating point.
prodR=1
for n in range(3,51):
    j=n-1
    R=1+comb(j,2)+j*(j-2)+(3*comb(j,4) if j>=4 else 0)
    prodR*=R
    bound=Q(1024*factorial(n)**3,128**n)
    assert Q(prodR,factorial(n))>=bound
    prob=Q(factorial(n),16**n*n**(3*n))
    assert bound*prob==Q(1024*factorial(n)**4,2048**n*n**(3*n))
    checks+=2
print(json.dumps({'status':'PASS','assertions':checks,'strip_triples':triples,'strip_sizes':[3,12],
 'arrangement_sizes':[2,1000],'recurrence_sizes':[3,50],
 'scope':'Exact finite endpoint and algebra controls, not a replacement for the all-size proof.'},indent=2,sort_keys=True))

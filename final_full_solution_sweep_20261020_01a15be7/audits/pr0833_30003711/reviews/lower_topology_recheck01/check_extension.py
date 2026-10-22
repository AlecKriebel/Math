#!/usr/bin/env python3
"""Finite exact control for the central extension and cup coboundary."""
from itertools import product
import json
F=range(3)
P=list(product(F,repeat=3))
def mul(g,h):
    a,b,c=g; d,e,f=h
    return ((a+d)%3,(b+e)%3,(c+f+b*d)%3)
def cochain(g):
    a,b,c=g
    return (c-a*b)%3
identity=(0,0,0)
assert len(P)==27
for g,h,k in product(P,repeat=3):
    assert mul(mul(g,h),k)==mul(g,mul(h,k))
for g,h in product(P,repeat=2):
    assert (cochain(h)-cochain(mul(g,h))+cochain(g))%3==g[0]*h[1]%3
assert all(mul(mul(g,g),g)==identity for g in P)
center=[g for g in P if all(mul(g,h)==mul(h,g) for h in P)]
assert center==[(0,0,c) for c in F]
A=(1,0,0); B=(0,1,0)
assert mul(B,A)==(1,1,1) and mul(A,B)==(1,1,0)
print(json.dumps({"group_order":len(P),"center":center,"exponent":3,"associativity_cases":27**3,"cup_coboundary_cases":27**2,"all_exact_checks_passed":True},indent=2))

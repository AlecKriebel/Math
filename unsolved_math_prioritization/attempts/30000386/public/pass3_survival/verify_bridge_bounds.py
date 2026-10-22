"""Supplementary finite checks of the structural proofs, not a game search."""
from fractions import Fraction
from math import isqrt
import json

def need(x,msg):
    if not x:raise RuntimeError(msg)

cases=[]
for L in range(1,101):
    for R in range(4):
        M=(4*R+1)**2
        if M>L:continue
        pause_count=sum(max(abs(x),abs(y))<=L-M for x in range(-L,L+1) for y in range(-L,L+1))
        need(pause_count==(2*(L-M)+1)**2,'Pause count')
        need(M==len({(x,y) for x in range(-2*R,2*R+1) for y in range(-2*R,2*R+1)}),'Attack cardinality')
        cases.append({'L':L,'R':R,'M':M,'pause_probability':str(Fraction(pause_count,(2*L+1)**2))})
for R in range(6):
    errors=[(x,y) for x in range(-R,R+1) for y in range(-R,R+1)]
    for a in errors:
        for b in errors:
            need(max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=2*R,'Endpoint containment')
for L in range(1,10001):
    R=isqrt((L-1)//64)+1
    need(64*R*R>=L,'Radius floor')
    q=min(Fraction(1),Fraction((2*R+1)**2,(4*L+1)**2))
    need(q>=Fraction(1,400*L),'Union-series lower bound')
need(Fraction(1,2)*Fraction(1,400)==Fraction(1,800),'Block charge')
print(json.dumps({'status':'PASS','scope':'Supplementary exact checks only; no full-game solution','pause_formula_cases_checked':len(cases),'selected_pause_cases':[c for c in cases if c['L'] in (1,25,50,81,100)],'endpoint_containment_radii_checked':list(range(6)),'union_lower_bound_lengths_checked':10000,'per_block_charge':'1/800'},indent=2))

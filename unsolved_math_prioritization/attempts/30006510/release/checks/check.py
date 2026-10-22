#!/usr/bin/env python3
"""Exact finite controls; these do not prove the continuous geometric theorems."""
from fractions import Fraction as F
from pathlib import Path
import json

checks = []
def record(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

# Areas are measured in units of pi. This tests the ideal-polygon mixture exactly.
p = [F(1,2), F(1,2)]
v = [F(1), F(2)]
gamma = sum(a/b for a,b in zip(p,v))
q = [(a/b)/gamma for a,b in zip(p,v)]
record('triangle/quadrilateral gamma times pi = 3/4', gamma == F(3,4))
record('triangle count probability = 2/3', q[0] == F(2,3))
record('quadrilateral count probability = 1/3', q[1] == F(1,3))
record('zero-cell and count-typical distributions differ', q != p)
record('mean-volume inversion for ideal mixture', gamma*sum(a*b for a,b in zip(q,v)) == 1)

# Include an infinite-volume spatial sector. It contributes zero reciprocal mass.
for i, (p, v) in enumerate([
    ([F(1,3),F(1,6)], [F(2),F(7)]),
    ([F(1,4),F(1,4),F(1,4)], [F(1,3),F(4),F(11)]),
    ([F(1,5),F(2,5)], [F(1),F(2)]),
    ([F(1,2)], [F(13)]),
]):
    pf = sum(p); gamma = sum(a/b for a,b in zip(p,v))
    q = [(a/b)/gamma for a,b in zip(p,v)]
    record(f'mixed case {i}: typical probabilities normalized', sum(q)==1)
    record(f'mixed case {i}: gamma E_typ V equals finite spatial fraction',
           gamma*sum(a*b for a,b in zip(q,v))==pf)
    record(f'mixed case {i}: finite-sector bias reverses',
           [gamma*a*b for a,b in zip(q,v)] == p)

# Check exact decomposition of the coercivity lower bound.
for i,p in enumerate([F(3,5),F(2,3),F(3,4),F(9,10)]):
    R=F(i+1); D=F(17+i)
    record(f'median bound {i}: decomposition',
           p*(D-2*R)+(1-p)*(-D) == (2*p-1)*D-2*p*R)
    record(f'median bound {i}: positive escape coefficient',2*p-1>0)

# H^2 ball volumes without the common pi factor, t=exp(R), s=exp(r).
# These finite rational checks support the written limiting algebra, not a limit proof.
for i,(t,s) in enumerate([(F(20),F(2)),(F(100),F(3)),(F(1000),F(5))]):
    V=t+1/t-2
    outer=(t*s+1/(t*s)-2)/V
    inner=(t/s+s/t-2)/V
    record(f'ball ratio {i}: exact outer difference',
           outer-s == ((1/s-s)/t+2*s-2)/V)
    record(f'ball ratio {i}: exact inner difference',
           inner-1/s == ((s-1/s)/t+2/s-2)/V)
    record(f'ball ratio {i}: persistent outward bias',outer>1)
    record(f'ball ratio {i}: persistent inward bias',inner<1)

# Ideal n-gon area=(n-2) pi; verify finite geometric normalizations used in examples.
for n in (3,4,5):
    area=F(n-2); intensity=1/area
    record(f'ideal {n}-gon area/intensity consistency',area*intensity==1)

result={
    'all_passed':True,
    'passed':len(checks),
    'checks':checks,
    'scope':'Exact rational controls of normalization and displayed algebra only; no simulation, geometric theorem verification, or novelty certification.'
}
path=Path(__file__).with_name('result.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'passed':len(checks)}))

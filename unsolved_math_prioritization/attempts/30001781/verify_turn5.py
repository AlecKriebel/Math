"""Exact finite controls for the fifth-turn reduction; no asymptotic proof claim."""
from fractions import Fraction as F
from itertools import product, combinations
import json
checks=0

def check(x):
    global checks
    assert x
    checks+=1

# Exact iid maximum CDFs for finite supported distributions, with atoms/ties.
for weights in [(1,1,1),(1,2,3),(5,2,1),(2,5,7)]:
    total=sum(weights)
    probs=[F(w,total) for w in weights]
    for n in range(1,7):
        for threshold in [-1,0,1,2,3]:
            Fz=sum((p for z,p in enumerate(probs) if z<=threshold), F())
            enumerated=sum((__import__('functools').reduce(lambda a,b:a*b,(probs[j] for j in js),F(1))
                            for js in product(range(3),repeat=n) if max(js)<=threshold),F())
            check(enumerated==Fz**n)
            # Union bound, including equality at an atomic threshold.
            check(1-Fz**n<=n*(1-Fz))
# Union bound for nonidentical laws, the converse direction's required scope.
for qs in product([F(0),F(1,7),F(1,2),F(1)],repeat=4):
    prod=F(1)
    for q in qs: prod*=1-q
    check(1-prod<=sum(qs))
# Exact rational comparison underlying 1-exp(-s)<=s:
# (1-q)^n >= 1/2 also implies nq<=1 by (1-q)^(-n)>=1+nq.
for n in range(1,41):
    for j in range(101):
        q=F(j,100)
        if (1-q)**n>=F(1,2):
            check(n*q<=1)
# k=1 maximal-submatrix norm squared equals maximum top-m row norm squared.
for N in range(1,7):
    rows=[[F((i+2)*(j+1)%7-3, i+1) for j in range(N)] for i in range(4)]
    for m in range(1,N+1):
        direct=max(sum(row[j]**2 for j in J) for row in rows for J in combinations(range(N),m))
        top=max(sum(sorted((x*x for x in row),reverse=True)[:m]) for row in rows)
        check(direct==top)
# Gamma(p+1)=p! at integer p: p!<=p^p suffices for these controls.
fact=1
for p in range(1,201):
    fact*=p
    check(fact<=p**p)
print(json.dumps({"status":"PASS","exact_assertions":checks,
    "scope":["finite iid maximum CDFs with atoms","nonidentical union bound","rational quantile consequences","k=1 sparse-row identity","integer moment integral control"],
    "not_checked":"The dimension-free log-concave moment conjecture and the analytic all-real-p equivalence are not established by finite tests."},indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Independent finite diagnostics; no infinite-cluster simulation."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from math import prod
import hashlib,json

counts={}
def ck(name,value):
    assert value,name
    counts[name]=counts.get(name,0)+1

def components(V,E):
    labels={v:v for v in V}
    def root(v):
        while labels[v]!=v:
            labels[v]=labels[labels[v]];v=labels[v]
        return v
    for x,y in E:
        if x in labels and y in labels:
            labels[root(x)]=root(y)
    return {frozenset(v for v in V if root(v)==r) for r in {root(v) for v in V}}

# Fixed-set isolation on a larger finite test graph. Marked components are a
# finite analogue only, not substitutes for actual infinite components.
V=set(range(5));edges=list(combinations(sorted(V),2));cut={1,3};outside=V-cut
probs=[F(1,3+abs(x-y)) for x,y in edges]
incident=[i for i,e in enumerate(edges) if cut.intersection(e)]
isolation=prod((1-probs[i] for i in incident),start=F(1))
P_B=P_AB=total=F(0)
for bits in product((0,1),repeat=len(edges)):
    op=[e for e,b in zip(edges,bits) if b]
    weight=prod((p if b else 1-p for p,b in zip(probs,bits)),start=F(1))
    parts=components(outside,op)
    isolated=[e for e in op if not cut.intersection(e)]
    expected=parts|{frozenset({v}) for v in cut}
    ck("isolation_preserves_outside_partition",components(V,isolated)==expected)
    B=not any({0,4}.issubset(C) for C in parts)
    A=not any(bits[i] for i in incident)
    total+=weight
    if B:P_B+=weight
    if A and B:P_AB+=weight
ck("finite_product_mass",total==1)
ck("isolation_independence",P_AB==isolation*P_B)
ck("positive_isolation_probability",isolation>0)

# First-exit events ignore edges with both endpoints outside the fixed box.
verts=set(range(-2,3));box={-1,0,1};es=list(combinations(sorted(verts),2))
far=es.index((-2,2))
for bits in product((0,1),repeat=len(es)):
    op=[e for e,b in zip(es,bits) if b]
    crossing=any(0 in C and bool(C-box) for C in components(verts,op))
    flipped=list(bits);flipped[far]=1-flipped[far]
    op2=[e for e,b in zip(es,flipped) if b]
    crossing2=any(0 in C and bool(C-box) for C in components(verts,op2))
    ck("first_exit_ignores_outside_edge",crossing==crossing2)

# An exact positive infinite-product control:
# product_{j=1}^N (1-1/(j+1)^2)=(N+2)/(2(N+1))->1/2.
p=F(1)
for N in range(1,101):
    p*=1-F(1,(N+1)**2)
    ck("telescoping_positive_product",p==F(N+2,2*(N+1)) and p>F(1,2))

# The actual family's tail and explicit one-vertex isolation lower bound.
for N in range(9,100):
    tail=sum((F(1,j*j) for j in range(9,N+1)),F(0))
    ck("family_tail_bound",tail<F(1,8)-F(1,N))
ck("subcritical_mean_bound",F(2,64)+F(14,64)+4*F(1,8)==F(3,4)<1)
for t in (F(1,64),F(1,4),F(1,2),F(7,8),F(63,64)):
    # exp(-4 sum_{j>=9}j^-2)>=exp(-1/2)>=1/2.
    lower=(1-t)**2*F(63,64)**14/2
    ck("explicit_family_isolation_lower",0<lower<1)
    for size in range(1,6):
        ck("finite_set_lower_product",0<lower**size<=lower)

# Generic finite-parameter conditioning gives a polynomial, even if each
# coefficient represents a probability over infinitely many fixed tail edges.
from math import comb
for m in range(1,7):
    coefficients={bits:F(1+sum((i+1)*b for i,b in enumerate(bits)),m*(m+1)//2+2)
                  for bits in product((0,1),repeat=m)}
    polynomial=[F(0)]*(m+1)
    for bits,value in coefficients.items():
        k=sum(bits)
        for j in range(m-k+1):
            polynomial[k+j]+=value*(-1)**j*comb(m-k,j)
    for t in (F(0),F(1,7),F(1,2),F(6,7),F(1)):
        conditioned=sum((value*t**sum(bits)*(1-t)**(m-sum(bits))
                         for bits,value in coefficients.items()),F(0))
        expanded=sum((c*t**i for i,c in enumerate(polynomial)),F(0))
        ck("finite_parameter_polynomial",conditioned==expanded and 0<=expanded<=1)

root=Path(__file__).resolve().parent
result={"status":"PASS","exact_assertions":sum(counts.values()),"counts":counts,
 "artifact_sha256":hashlib.sha256((root/"author_replay/KNOWN_CONSEQUENCE.md").read_bytes()).hexdigest(),
 "scope":"Finite isolation/first-exit logic, exact products, tail estimates and conditioning "
         "polynomials only. Infinite-volume uniqueness, critical existence and ends are "
         "checked mathematically and through credited primary theorems in REVIEW.md."}
(root/"independent_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))

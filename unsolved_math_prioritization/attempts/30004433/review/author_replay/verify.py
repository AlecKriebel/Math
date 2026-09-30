#!/usr/bin/env python3
"""Exact finite diagnostics only; the infinite-volume proof is in KNOWN_CONSEQUENCE.md."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
import hashlib, json

checks = 0
families = {}
def check(v, family):
    global checks
    assert v, family
    checks += 1
    families[family] = families.get(family, 0) + 1

def components(vertices, edges):
    unseen=set(vertices); out=[]
    adj={v:set() for v in unseen}
    for u,v in edges:
        if u in adj and v in adj: adj[u].add(v);adj[v].add(u)
    while unseen:
        root=min(unseen); c={root}; todo=[root]; unseen.remove(root)
        while todo:
            for v in adj[todo.pop()] & unseen:
                unseen.remove(v);c.add(v);todo.append(v)
        out.append(c)
    return out

# Every connected finite graph through four vertices and every nonempty deletion.
for n in range(1,5):
    V=set(range(n)); E=list(combinations(V,2))
    for bits in product((0,1),repeat=len(E)):
        op=[e for e,b in zip(E,bits) if b]
        if len(components(V,op))!=1:continue
        for mask in range(1,1<<n):
            S={v for v in V if mask>>v&1}
            inc=sum(bool(S.intersection(e)) and not set(e)<=S for e in op)
            check(len(components(V-S,op))<=inc,'finite_component_deletion')

# Exact countable-product proof has a finite analogue with fully enumerated law.
V=set(range(4));E=list(combinations(V,2)); probs=[F(i+1,i+8) for i in range(len(E))]
for mask in range(1<<4):
    S={v for v in V if mask>>v&1};out=V-S
    A=prod((1-p for e,p in zip(E,probs) if S.intersection(e)),start=F(1))
    B=AB=mass=F(0)
    for bits in product((0,1),repeat=len(E)):
        weight=prod((p if b else 1-p for p,b in zip(probs,bits)),start=F(1))
        op=[e for e,b in zip(E,bits) if b]
        b=len(components(out,op))>=2
        a=not any(S.intersection(e) for e in op)
        mass+=weight
        if b:B+=weight
        if a and b:AB+=weight
    check(mass==1,'probability_normalization')
    check(A>0,'positive_isolation_atom')
    check(AB==A*B,'isolation_independence')

# Rational tail controls and the precise mean-degree bound used in the example.
check(F(16,64)+F(4,8)==F(3,4)<1,'critical_example_mean_degree')
for N in range(9,65):
    tail=sum((F(1,k*k) for k in range(9,N+1)),F(0))
    telescope=sum((F(1,k*(k-1)) for k in range(9,N+1)),F(0))
    check(tail<=telescope==F(1,8)-F(1,N),'inverse_square_tail')
for m in range(2,10):
    for N in range(m,40):
        ps=[F(1,k*(k+1)) for k in range(m,N+1)]
        check(prod((1-p for p in ps),start=F(1))>=1-sum(ps,F(0))>=1-F(1,m)>0,
              'summable_tail_product_control')

# Condition on long edges in a four-site example, giving an exact polynomial in t.
# Finite crossing event: vertex 0 is connected to vertex 3.
E=list(combinations(range(4),2)); short=[e for e in E if e[1]-e[0]==1]
long=[e for e in E if e not in short]; Lprob={e:F(1,7+e[1]-e[0]) for e in long}
poly=[F(0)]*4
for lb in product((0,1),repeat=len(long)):
    lw=prod((Lprob[e] if b else 1-Lprob[e] for e,b in zip(long,lb)),start=F(1))
    lop=[e for e,b in zip(long,lb) if b]
    for sb in product((0,1),repeat=len(short)):
        op=lop+[e for e,b in zip(short,sb) if b]
        if not any(0 in c and 3 in c for c in components(range(4),op)):continue
        a=sum(sb); b=len(short)-a
        for j in range(b+1):poly[a+j]+=lw*((-1)**j)*comb(b,j)
for t in [F(k,16) for k in range(17)]:
    direct=F(0)
    for bits in product((0,1),repeat=len(E)):
        ps=[t if e in short else Lprob[e] for e in E]
        w=prod((p if b else 1-p for p,b in zip(ps,bits)),start=F(1))
        op=[e for e,b in zip(E,bits) if b]
        if any(0 in c and 3 in c for c in components(range(4),op)):direct+=w
    check(sum((c*t**i for i,c in enumerate(poly)),F(0))==direct,'conditional_polynomial')

# Deliberately excluded p=1 diagnostic: a deterministic line has two long arms,
# while its vertex-isolation probability is zero. Finite truncation only.
line=[(i,i+1) for i in range(-4,4)]
check(len(components(set(range(-4,5))-{0},line))==2,'excluded_deterministic_line')
check((1-F(1))**2==0,'excluded_deterministic_line')
root=Path(__file__).resolve().parent
result={'problem_id':30004433,'artifact_sha256':hashlib.sha256((root/'KNOWN_CONSEQUENCE.md').read_bytes()).hexdigest(),
        'exact_assertions':checks,'families':families,'continuity_polynomial_coefficients':[str(c) for c in poly],
        'infinite_volume_claim_checked_by_computation':False,'status':'passed'}
(root/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

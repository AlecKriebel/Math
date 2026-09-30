#!/usr/bin/env python3
"""Exact algebraic controls; no arbitrary-knot isotopy or primeness test."""
from fractions import Fraction as F
from itertools import product, permutations
from math import gcd
from pathlib import Path
from hashlib import sha256
import json

counts={}
def ck(cat,value):
    assert value,cat
    counts[cat]=counts.get(cat,0)+1

def clean(p):return {i:a for i,a in p.items() if a}
def add(p,q):
    r=dict(p)
    for i,a in q.items():r[i]=r.get(i,0)+a
    return clean(r)
def neg(p):return {i:-a for i,a in p.items()}
def mul(p,q):
    r={}
    for i,a in p.items():
        for j,b in q.items():r[i+j]=r.get(i+j,0)+a*b
    return clean(r)
def scale(p,a):return clean({i:a*b for i,b in p.items()})
def shift(p,n):return {i+n:a for i,a in p.items()}
def bar(p):return {-i:a for i,a in p.items()}
def detpoly(m):
    n=len(m);out={}
    for perm in permutations(range(n)):
        term={0:(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))}
        for i,j in enumerate(perm):term=mul(term,m[i][j])
        out=add(out,term)
    return out
def alex(v):
    n=len(v)
    return shift(detpoly([[clean({0:v[i][j],1:-v[j][i]}) for j in range(n)] for i in range(n)]),-n//2)
def mm(a,b):return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*b)) for row in a)
def trans(a):return tuple(zip(*a))
def block(a,b):
    return tuple(tuple(row)+(0,)*len(b) for row in a)+tuple((0,)*len(a)+tuple(row) for row in b)

V=((1,0),(-1,-1));P=((1,1),(1,0))
ck('order_two_anti_isometry',mm(mm(trans(P),V),P)==tuple(tuple(-x for x in row) for row in V))
ck('anti_isometry_unimodular',P[0][0]*P[1][1]-P[0][1]*P[1][0]==-1)
ck('explicit_alexander',alex(V)=={-1:-1,0:3,1:-1})
G=((1,0),(0,1),(1,1),(1,0))
ck('primitive_graph_metabolizer',mm(mm(trans(G),block(V,V)),G)==((0,0),(0,0)))
ck('irrational_discriminant',2*2<5<3*3)
for e in range(-5,6):
    H=((e,1),(0,0));W=block(V,H)
    ck('metabolic_block_alexander',alex(H)=={0:1})
    ck('stabilized_alexander',alex(W)==alex(V))
    ck('metabolic_line',H[1][1]==0)
ck('rank_one_block_difference',all(block(V,((1,1),(0,0)))[i][j]-block(V,((0,1),(0,0)))[i][j]==int(i==j==2) for i,j in product(range(4),repeat=2)))

rank_two_cases=0
for a,b,d,s,eps in product(range(-4,5),range(-4,5),range(-4,5),(-1,1),(-1,1)):
    c=b-s;v=((a,b),(c,d));vp=((a+eps,b),(c,d))
    delta=add(alex(vp),neg(alex(v)))
    ck('rank_two_determinant_difference',delta==scale({-1:1,0:-2,1:1},eps*d))
    ck('equal_polynomials_exactly_d_zero',(alex(v)==alex(vp))==(d==0))
    if d==0:
        norm=mul(clean({0:b,1:-c}),clean({0:b,-1:-c}))
        ck('rank_two_norm_factor',alex(v)==norm)
        ck('rank_two_square_determinant',sum(coef*(-1 if power%2 else 1) for power,coef in norm.items())==(b+c)**2)
    rank_two_cases+=1

for a,b in product(range(-5,6),repeat=2):
    D=clean({-2:a,-1:b,0:1-2*a-2*b,1:b,2:a})
    ck('symmetric_normalized_polynomial',D==bar(D) and sum(D.values())==1)
    ck('crossing_witt_isotropy',add(mul(D,D),neg(mul(bar(D),D)))=={})

I=((1,0),(0,1))
def M(x):return ((x,1),(1,0))
words=[()]+[(x,) for x in range(-2,3)]+list(product(range(-2,3),repeat=2))
matrices=[]
for word in words:
    mat=I
    for x in word:mat=mm(mat,M(x))
    matrices.append(mat)
cf_cases=0;preserved=0;branches={'same_numerator':0,'opposite_numerator':0}
for Q,R,x in product(matrices,matrices,(-3,-2,-1,1,2,3)):
    (a,b),(c,d)=Q;u,w=R[0][0],R[1][0]
    eps=1 if x>0 else -1
    T=mm(mm(Q,M(x)),R);Tp=mm(mm(Q,M(x-2*eps)),R)
    p,q=T[0][0],T[1][0];pp,qp=Tp[0][0],Tp[1][0]
    delta=a*d-b*c
    ck('continued_fraction_update',pp==p-2*eps*a*u and qp==q-2*eps*c*u)
    ck('continued_fraction_primitive',abs(delta)==1 and gcd(u,w)==1 and gcd(p,q)==1 and gcd(pp,qp)==1)
    cf_cases+=1
    if not p or p%2==0 or abs(pp)!=abs(p):continue
    preserved+=1
    if pp==p:
        branches['same_numerator']+=1
        ck('degenerate_product',a*u==0)
        ck('same_knot_denominator_residue',(qp-q)%abs(p)==0)
    else:
        branches['opposite_numerator']+=1
        ck('opposite_numerator_equation',p==eps*a*u and a*u!=0)
        ck('primitive_divisibility',u in (a,-a))
        ck('square_numerator',abs(p)==a*a)
        qnorm=(1 if p>0 else -1)*q
        ck('ribbon_denominator_identity',qnorm==a*c+eps*delta)
        m=abs(a)
        if m>1:
            k=((1 if a>0 else -1)*c)%m
            ck('ribbon_family_parameters',0<k<m and gcd(m,k)==1 and m%2==1)
            ck('ribbon_family_residue',qnorm%(m*m)==m*k+eps*delta)
        qpnorm=(1 if pp>0 else -1)*qp
        ck('mirror_denominator_relation',(qnorm*qpnorm+1)%abs(p)==0)

for x,pq in ((-1,(9,4)),(1,(-9,-2))):
    t=mm(mm(M(3),M(x)),M(-3))
    ck('explicit_ribbon_example',(t[0][0],t[1][0])==pq)

r=Path(__file__).resolve().parent
receipt={'status':'PASS','artifact_sha256':sha256((r/'PARTIAL.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'categories':counts,'rank_two_cases':rank_two_cases,'continued_fraction_cases':cf_cases,'odd_determinant_preserving_cases':preserved,'preserving_branches':branches,'limitations':'Finite exact algebra and continued-fraction controls only; no arbitrary-knot isotopy, primeness, crossing-presentation conversion, or independent proof of the imported ribbon theorem.'}
(r/'verification.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))

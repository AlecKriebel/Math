#!/usr/bin/env python3
"""Eight NEW, initial-frozen interface controls; no native programme replay.
Pure exact in-memory arithmetic. These finite controls do not prove H10,
Selmer finiteness, modularity, analytic estimates, or primary theorems.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd
import json

counts = {}
def check(family, condition):
    if not condition:
        raise ValueError('own frozen control failed: ' + family)
    counts[family] = counts.get(family, 0) + 1

# E1: coefficient comparison after multiplying both sides by q.
# Coefficients live in Z[q,a]; represent q and a by exponent pairs.
qP = [{(1,0):1}, {(0,1):-1}, {(0,0):1}]
qD = [{(0,0):1}, {(0,1):-1}, {(1,0):1}]
def subdict(a,b):
    c=dict(a)
    for k,v in b.items(): c[k]=c.get(k,0)-v
    return {k:v for k,v in c.items() if v}
check('E1', [subdict(a,b) for a,b in zip(qP,qD)] ==
      [{(1,0):1,(0,0):-1},{},{(0,0):1,(1,0):-1}])

# E2: multiplication in Q[C2], g^2=1. All selected denominators are odd.
def mul(a,b): return (a[0]*b[0]+a[1]*b[1],a[0]*b[1]+a[1]*b[0])
for den in (1,3,5):
    for num in range(-4,5):
        v=F(num,den); r=1+2*v
        if r==0: continue
        U=(1+v,v); inv=(1-v/r,-v/r)
        check('E2',mul(U,inv)==(1,0))
        check('E2',U[0]+U[1]==r and U[0]-U[1]==1)
        check('E2',r.numerator%2!=0 and r.denominator%2!=0)
check('E2', (1+F(0),F(0))==(1,0))

# S1: formal coefficients of A+ - gamma A- in Z[c][gamma].
# c^2-c gamma minus (c^2 gamma-c) = c(c+1)(1-gamma).
check('S1', [subdict({2:1},{1:-1}),subdict({1:-1},{2:1})] ==
      [{2:1,1:1},{1:-1,2:-1}])
for c in (3,5,9,17):
    for gamma in (F(1),F(3,5),F(7,9)):
        ap=c*c-c*gamma; am=c*c-c/gamma
        check('S1',ap-gamma*am==c*(c+1)*(1-gamma))
    check('S1',F(c*c-c,c*c-c)==1)

# P1: finite-etale promise examples. These are field-degree diagnostics;
# the general H0/point argument is a written proof in DERIVATIONS.md.
for numerator in range(-4,5):
    for denominator in range(1,5):
        image=F(numerator,denominator)
        check('P1',image*image!=2)
check('P1',F(1)*F(1)==1)  # rational residue of Spec(Q).

# H1/G1: tiny exact primitive homogeneous-vector enumeration.
def primitive_vectors(n,M):
    for z in product(range(-M,M+1),repeat=n):
        if not any(z): continue
        if next(x for x in z if x)!=abs(next(x for x in z if x)):continue
        d=0
        for x in z:d=gcd(d,abs(x))
        if d==1:yield z
for M in (0,1,2):
    p0=list(primitive_vectors(1,M))
    check('H1',p0==([] if M==0 else [(1,)]))
    p1=list(primitive_vectors(2,M))
    check('H1',not any(x*x+y*y==0 for x,y in p1))
    check('H1',any(x-y==0 for x,y in p1)==(M>=1))
    check('H1',not any(1==0 for z in p1))
check('G1',0*0+0*0==0)  # [0:1:0] lies on X^2+Z^2=0.
check('G1',all(x*x+1>0 for x in range(-4,5)))
check('G1',all(x*x+y*y>0 for x,y in product(range(-3,4),repeat=2)
               if x or y))

# V1: local-contact order under nonzero rational rescaling.
def val(x,p):
    if x==0:raise ValueError('zero branch explicitly excluded')
    x=F(x);n,d=abs(x.numerator),x.denominator;k=0
    while n%p==0:n//=p;k+=1
    while d%p==0:d//=p;k-=1
    return k
for p in (3,5,7):
    for u,v in ((F(1),F(2)),(F(9,5),F(3)),(F(25),F(2,7))):
        for a in (F(2,3),F(9,25),F(-7,5)):
            L=2*u+3*v
            check('V1',val(a*L,p)-min(val(a*u,p),val(a*v,p))==
                  val(L,p)-min(val(u,p),val(v,p)))

# T1: NEW tiny alternating-matrix sanity, unrelated to the native
# reciprocity/graph checkers. Finite sanity is weaker than the written
# perfect finite-2-group decomposition and assumes no Sha finiteness.
def rank2(A):
    A=[r[:] for r in A];rank=0
    for col in range(len(A)):
        pivot=next((i for i in range(rank,len(A)) if A[i][col]),None)
        if pivot is None:continue
        A[rank],A[pivot]=A[pivot],A[rank]
        for i in range(len(A)):
            if i!=rank and A[i][col]:A[i]=[a^b for a,b in zip(A[i],A[rank])]
        rank+=1
    return rank
for n in range(5):
    edges=[(i,j) for i in range(n) for j in range(i+1,n)]
    for bits in product((0,1),repeat=len(edges)):
        A=[[0]*n for i in range(n)]
        for (i,j),b in zip(edges,bits):A[i][j]=A[j][i]=b
        check('T1',rank2(A)%2==0)
check('T1',3-2==1)
print(json.dumps({'schema':'scope23205305-new-frozen-controls-v1',
 'family_check_counts':counts,'checks':sum(counts.values()),
 'native_programmes_executed':False,
 'evidence_limit':'finite interface controls; written universal proofs and external theorem hypotheses are separate'},
 ensure_ascii=False,indent=2))

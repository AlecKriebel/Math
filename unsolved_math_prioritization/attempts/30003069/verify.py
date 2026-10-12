#!/usr/bin/env python3
"""Exact finite source/poset diagnostics, not a proof of the plabic theorem."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib,json
checks=0

def check(v):
    global checks
    assert v
    checks+=1

def rank(rows):
    if not rows:return 0
    a=[[F(x) for x in r] for r in rows];i=0
    for j in range(len(a[0])):
        p=next((p for p in range(i,len(a)) if a[p][j]),None)
        if p is None:continue
        a[i],a[p]=a[p],a[i];d=a[i][j];a[i]=[x/d for x in a[i]]
        for q in range(len(a)):
            if q!=i and a[q][j]:
                d=a[q][j];a[q]=[x-d*y for x,y in zip(a[q],a[i])]
        i+=1
        if i==len(a):break
    return i

def arank(vs):
    return rank([[x-y for x,y in zip(v,vs[0])] for v in vs[1:]])

def interval(n,d,s):return frozenset((s+t)%n for t in range(d))

def weak(I,J,n):
    a=I-J;b=J-I
    return not any((w in a and x in b and y in a and z in b) or
                   (w in b and x in a and y in b and z in a)
                   for w,x,y,z in combinations(range(n),4))

label_pairs=0
for n in range(2,9):
    U=frozenset(range(n))
    for d in range(1,n):
        frozen={interval(n,d,s) for s in range(n)}
        check(len(frozen)==n)
        check({U-I for I in frozen}=={interval(n,n-d,s) for s in range(n)})
        for s in range(n):check(U-interval(n,d,s)==interval(n,n-d,s+d))
        labels=list(map(frozenset,combinations(range(n),d)))
        for I,J in combinations(labels,2):
            check(weak(I,J,n)==weak(U-I,U-J,n));label_pairs+=1
        if n==2*d:
            mutable=set(labels)-frozen
            check(frozen|{U-I for I in mutable}=={U-I for I in set(labels)})
        else:
            check(all(len(I)!=n-d for I in frozen))
label_checks=checks

# Grid 3x3, increasing order; rank and all support evaluations are rational.
a=b=3;P=list(product(range(a),range(b)));N=len(P);ix={p:i for i,p in enumerate(P)}
covers=[(ix[p],ix[q]) for p in P for q in P if
        (q[0]-p[0],q[1]-p[1]) in ((1,0),(0,1))]
comparable=[(i,j) for i,p in enumerate(P) for j,q in enumerate(P)
            if i!=j and p[0]<=q[0] and p[1]<=q[1]]
orders=[];antis=[]
for v in product((0,1),repeat=N):
    if all(v[i]<=v[j] for i,j in covers):orders.append(v)
    if all(not(v[i] and v[j]) for i,j in comparable):antis.append(v)
check(len(orders)==len(antis)==comb(a+b,a)==20)
check(arank(orders)==arank(antis)==N)
chains=[]
def paths(i,j,path):
    path=path+(ix[(i,j)],)
    if (i,j)==(a-1,b-1):chains.append(path)
    if i+1<a:paths(i+1,j,path)
    if j+1<b:paths(i,j+1,path)
paths(0,0,())
check(len(chains)==comb(a+b-2,a-1)==6)
# inequalities are c + dot(row,x) >= 0
unit=lambda i:tuple(int(i==j) for j in range(N))
O=[(0,unit(0)),(1,tuple(-x for x in unit(N-1)))]+[
  (0,tuple(int(t==j)-int(t==i) for t in range(N))) for i,j in covers]
C=[(0,unit(i)) for i in range(N)]+[
  (1,tuple(-int(i in path) for i in range(N))) for path in chains]
for vs,ineq in ((orders,O),(antis,C)):
    for c,row in ineq:
        values=[c+sum(x*y for x,y in zip(row,v)) for v in vs]
        for value in values:check(value>=0)
        face=[v for v,value in zip(vs,values) if value==0]
        check(arank(face)==N-1)
check(len(O)==14);check(len(C)==15);check(len(O)!=len(C))
facet_checks=checks-label_checks
# Construct the strict chain-facet witness directly, as in the proof.
for selected in chains:
    v=tuple(F(1,5) if i in selected else F(1,100) for i in range(N))
    for j,path in enumerate(chains):
        value=sum(v[i] for i in path)
        check(value==1 if path==selected else value<1)
    check(all(x>0 for x in v))
# Enumeration of grid covers/maximal-chain counts, without polyhedral software.
for a,b in product(range(1,7),repeat=2):
    P=list(product(range(a),range(b)))
    count=sum((q[0]-p[0],q[1]-p[1]) in ((1,0),(0,1)) for p in P for q in P)
    check(count+2==2*a*b-a-b+2)
    dp={(0,0):1}
    for i,j in P:
        if i or j:dp[i,j]=dp.get((i-1,j),0)+dp.get((i,j-1),0)
    check(dp[a-1,b-1]==comb(a+b-2,a-1))
# Homogeneous lattice-map scaling and section-power valuation identities.
for r,d in product(range(1,9),repeat=2):
    z=(2*d,-d,3*d)
    check(tuple(F(r*x,r*d) for x in z)==tuple(F(x,d) for x in z))
    U=((1,2,0),(0,1,1),(0,0,1));t=(2,-1,3)
    image=tuple(sum(U[i][j]*z[j] for j in range(3))+t[i] for i in range(3))
    check(tuple(r*x for x in image)==tuple(sum(U[i][j]*(r*z[j]) for j in range(3))+r*t[i] for i in range(3)))
p=Path(__file__).resolve().parent
out={'problem_id':30003069,'assertions':checks,'label_pair_tests':label_pairs,
 'label_assertions':label_checks,'facet_assertions':facet_checks,
 'order_vertices':len(orders),'chain_vertices':len(antis),
 'order_facets':len(O),'chain_facets':len(C),
 'scope':'Exact finite complement, facet-rank, and scaling diagnostics; no general plabic-flow theorem is computationally certified.',
 'artifact_sha256':hashlib.sha256((p/'SOURCE_STATUS.md').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Finite exact sanity controls, not a proof of the infinite realization theorem."""
from itertools import product
from collections import Counter
import json

C=Counter()

def check(p,kind):
    if not p:
        raise AssertionError(kind)
    C[kind]+=1

def all_posets(n):
    pairs=[(i,j) for i in range(n) for j in range(n) if i!=j]
    for bits in range(1<<len(pairs)):
        rel={(i,i) for i in range(n)}
        rel.update(p for k,p in enumerate(pairs) if (bits>>k)&1)
        if any((j,i) in rel for i,j in rel if i!=j): continue
        if any((i,k) not in rel for i,j in rel for jj,k in rel if j==jj): continue
        yield rel

def fams(xs):
    for mask in range(1<<len(xs)):
        yield [x for k,x in enumerate(xs) if (mask>>k)&1]

def meet(xs,top):
    a=top
    for x in xs:a &= x
    return a

def join(xs):
    a=0
    for x in xs:a |= x
    return a

counts={}
for n in range(1,5):
    count=0
    top=(1<<n)-1
    for rel in all_posets(n):
        count+=1
        opens=[a for a in range(1<<n) if all(not((a>>i)&1) or ((a>>j)&1) for i,j in rel)]
        closed=[top^a for a in opens]
        closure={i:sum(1<<j for j in range(n) if (j,i) in rel) for i in range(n)}
        for F in closed:
            if not F:continue
            irreducible=not any(A!=F and B!=F and (A|B)==F for A in closed if (A&F)==A for B in closed if (B&F)==B)
            if irreducible:
                check(sum(closure[i]==F for i in range(n))==1,'finite_sobriety_generic_point')
        for family in fams(opens):
            check(meet(family,top) in opens,'all_family_meet_open')
            check(join(family) in opens,'all_family_join_open')
        # Open-cover assembly with two discrete-domain chart witnesses.
        for U in opens:
            for V in opens:
                if U|V!=top: continue
                lift=lambda W:(W&U,W&V)
                check(len({lift(W) for W in opens})==len(opens),'two_chart_injectivity')
                for W in opens:
                    for Z in opens:
                        check(lift(W|Z)==(lift(W)[0]|lift(Z)[0],lift(W)[1]|lift(Z)[1]),'two_chart_binary_join')
                        check(lift(W&Z)==(lift(W)[0]&lift(Z)[0],lift(W)[1]&lift(Z)[1]),'two_chart_binary_meet')
    counts[str(n)]=count
check(counts=={'1':1,'2':3,'3':19,'4':219},'labeled_poset_counts')

# Four-to-five point-lattice obstruction from Turn 4.
psi={0:0,1:1,2:2,3:7}
for family in fams(list(psi)):
    check(psi[meet(family,3)]==meet([psi[x] for x in family],7),'weak_map_all_infima')
    if family and all(any((a|b)&c==(a|b) for c in family) for a in family for b in family):
        check(psi[join(family)]==join([psi[x] for x in family]),'weak_map_directed_suprema')
check(psi[1|2]!=(psi[1]|psi[2]),'binary_join_negative_control')
check(len(set(psi.values())|{psi[1]|psi[2]})==5,'join_closure_changes_cardinality')

# Exact real-matrix tests of the AF connecting maps.
def add(A,B):return tuple(x+y for x,y in zip(A,B))
def mul(A,B):
    a,b,c,d=A;e,f,g,h=B
    return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def star(A):a,b,c,d=A;return (a,c,b,d)
def diag(a,b):return (a,0,0,b)

def xadd(x,y):
    return ([add(a,b) for a,b in zip(x[0],y[0])],x[1]+y[1],x[2]+y[2])
def xmul(x,y):
    return ([mul(a,b) for a,b in zip(x[0],y[0])],x[1]*y[1],x[2]*y[2])
def xstar(x):return ([star(a) for a in x[0]],x[1],x[2])
def emb(x):return (x[0]+[diag(x[1],x[2])],x[1],x[2])
for m in range(5):
    for t in range(-4,5):
        x=([(t+i,1,-2,t-i) for i in range(m)],t,t+2)
        for s in range(-4,5):
            y=([(s-i,-1,3,s+i) for i in range(m)],s-1,s+1)
            check(emb(xadd(x,y))==xadd(emb(x),emb(y)),'AF_map_addition')
            check(emb(xmul(x,y))==xmul(emb(x),emb(y)),'AF_map_multiplication')
        check(emb(xstar(x))==xstar(emb(x)),'AF_map_adjoint')

result={
 'status':'PASS',
 'kind':'finite exact sanity controls only',
 'labeled_posets':counts,
 'assertions_by_category':dict(C),
 'total_assertions':sum(C.values()),
 'not_certified':['infinite compactness arguments','all countable or uncountable spaces','C*-algebra realization theorem','formal theorem-prover verification','independent review'],
}
print(json.dumps(result,indent=2,sort_keys=True))

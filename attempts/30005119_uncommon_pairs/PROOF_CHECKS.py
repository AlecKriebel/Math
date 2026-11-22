#!/usr/bin/env python3
"""Exact finite sanity checks; the universal proof is analytic, not sampled."""
import itertools, json, sys
from fractions import Fraction as F

def require(ok, msg):
    if not ok: raise RuntimeError(msg)

R=((1,-1,-1,1,0,0),(0,0,1,-1,-1,1))
results=[]
for p,n in [(2,1),(2,2),(2,3),(3,1),(3,2),(5,1),(7,1)]:
    G=list(itertools.product(range(p),repeat=n)); N=len(G)
    idx={x:i for i,x in enumerate(G)}
    sub=[[idx[tuple((a-b)%p for a,b in zip(x,y))] for y in G] for x in G]
    supp=[]
    for a,b in itertools.product(range(p),repeat=2):
        if a or b:
            row=[(a*x+b*y)%p for x,y in zip(*R)]
            supp.append(sum(c!=0 for c in row))
    require(min(supp)==4,'shortest row-space support')
    cols=[tuple(row[i]%p for row in R) for i in range(6)]
    require(all(any(c) for c in cols),'zero column')
    require(p==2 or len(set(cols))==6,'distinct odd-characteristic columns')
    require((R[0][0]*R[1][4]-R[0][4]*R[1][0])%p!=0,'rank minor')
    if p>3:
        dense=[[ (R[0][i]+j*R[1][i])%p for i in range(6)] for j in (2,3)]
        require(all(x for row in dense for x in row),'dense equivalent rows')
    # Exhaust all indicator functions, plus all half-grid functions for N<=5.
    fs=list(itertools.product((0,1),repeat=N))
    if N<=5: fs+=list(itertools.product((F(0),F(1,2),F(1)),repeat=N))
    direct_checked=0
    for f in fs:
        f=tuple(map(F,f)); alpha=sum(f)/N
        h=[sum(f[a]*f[sub[a][s]] for a in range(N))/N for s in range(N)]
        t=sum(x**3 for x in h)/N
        require(sum(h)/N==alpha**2,'correlation mean')
        require(t>=alpha**6,'Sidorenko bound')
        g=[1-x for x in f]
        hg=[sum(g[a]*g[sub[a][s]] for a in range(N))/N for s in range(N)]
        require(t+sum(x**3 for x in hg)/N>=F(1,32),'common bound')
        if direct_checked<3:
            direct=sum(f[a]*f[sub[a][s]]*f[b]*f[sub[b][s]]*f[c]*f[sub[c][s]]
                       for s,a,b,c in itertools.product(range(N),repeat=4))/N**4
            require(direct==t,'direct solution normalization')
            direct_checked+=1
    # Every coordinate difference is a nonzero functional on scalar kernel.
    scalar=[(a,(a-s)%p,b,(b-s)%p,c,(c-s)%p)
            for s,a,b,c in itertools.product(range(p),repeat=4)]
    require(len(set(scalar))==p**4,'parameterization injective')
    require(all(all(sum(r[i]*x[i] for i in range(6))%p==0 for r in R) for x in scalar),'equations')
    require(all(sum(x[i]==x[j] for x in scalar)==p**3 for i in range(6) for j in range(i)),'collision codimension')
    results.append({'p':p,'additive_dimension':n,'group_size':N,'functions_checked':len(fs),'direct_density_checks':direct_checked,'shortest_row_support':4,'status':'PASS'})
# Sharpness holds algebraically, and tests must not be disabled by python -O.
require(2*F(1,2)**6==F(1,32),'sharp benchmark')
print(json.dumps({'status':'PASS','matrix':R,'checks':results,'total_functions':sum(r['functions_checked'] for r in results),'limitations':'Finite exact sanity checks only. Universal proof uses Jensen; extension fields need only their additive group for this ±1 matrix.'},indent=2))

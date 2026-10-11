#!/usr/bin/env python3
"""Exact finite diagnostics for the binary weak-shift counterexample.
Standard library only. Infinite limits and arbitrary-coupling quantifiers
are established by the written proof, not this finite enumeration.
"""
from fractions import Fraction as Q
from itertools import product
import json
checks=0
def check(ok,label):
    global checks
    assert ok,label
    checks+=1

def window(n,r):
    law={}
    for signs in product([-1,1],repeat=r+1):
        prob=Q(1,2)
        for j in range(r):
            flip=Q(1,n+j+2)
            prob*=flip if signs[j]!=signs[j+1] else 1-flip
        law[signs]=prob
    return law
windows=[]
for n in [0,1,2,5,10,50]:
    for r in range(7):
        law=window(n,r)
        check(sum(law.values())==1,'probability mass')
        check(all(x>=0 for x in law.values()),'nonnegative')
        noflip=sum(law[x] for x in [(-1,)*(r+1),(1,)*(r+1)])
        check(noflip==Q(n+1,n+r+1),'telescoping no-flip probability')
        target={(-1,)*(r+1):Q(1,2),(1,)*(r+1):Q(1,2)}
        tv=sum(abs(v-target.get(x,0)) for x,v in law.items())/2
        check(tv==Q(r,n+r+1),'finite-window TV')
        for j in range(r+1):check(sum(v for x,v in law.items() if x[j]==1)==Q(1,2),'fair marginal')
        if r:
            corr=sum(x[0]*x[-1]*v for x,v in law.items())
            check(corr==Q(n*(n+1),(n+r)*(n+r+1)),'endpoint correlation')
        windows.append({'n':n,'r':r,'tv':str(tv),'no_flip':str(noflip)})

# Independent two-state transition multiplication.
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
I=((Q(1),Q(0)),(Q(0),Q(1)))
for m in range(12):
    P=I
    for n in range(m+1,m+21):
        k=n-1;p=Q(1,k+2)
        P=mul(P,((1-p,p),(p,1-p)))
        corr=Q(m*(m+1),n*(n+1))
        check(P==(((1+corr)/2,(1-corr)/2),((1-corr)/2,(1+corr)/2)),'transition product')
        check(P[0][1]==(1-corr)/2,'mismatch identity')
for x,y,b in product([-1,1],repeat=3):
    check(int(x!=y)<=int(x!=b)+int(y!=b),'coupling-independent triangle bound')
for n in [1,2,3,10,100]:
    mismatch=(1-Q(n*(n+1),2*n*(2*n+1)))/2
    check(mismatch==Q(3*n+1,4*(2*n+1)),'double-time exact obstruction')
# Geometric weights and finite partial sums used in the metric bound.
for M in range(1,21):
    check(sum(Q(j,2**(j+1)) for j in range(M+1))==1-Q(M+2,2**(M+1)),'weighted index sum')
print(json.dumps({'status':'PASS','exact_assertions':checks,'window_cases':len(windows),
    'transition_products':240,'window_receipts':windows,
    'limits':['No finite test certifies all couplings','No simulation used',
    'Full characterization question remains unresolved']},indent=2))

#!/usr/bin/env python3
"""Exact checks for the symbolic three-deadline proof, not exhaustive game solving."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json


def geometry(k):
    a=2**k
    return 2*a-1,9*a*a,[(2**j,9*4**(j-1)) for j in range(1,k+1)]


def inc(profiles,N):
    return max(min(beta/Q(N),alpha) for beta,alpha in profiles)


def prep(k,w,profiles):
    R,N,parts=geometry(k)
    traversal=sum((d*inc(profiles,n) for d,n in parts),Q(0))
    D=N*(1-traversal-(w+1)*inc(profiles,N))
    assert D>0
    out=[(Q(1),Q(1))]
    for beta,alpha in profiles:
        out.append((N*beta/D,min(N*alpha,beta)/D))
    return out,D


def terminal(k,w,profiles):
    R,N,parts=geometry(k)
    return w*inc(profiles,N)+sum((d*inc(profiles,n) for d,n in parts),Q(0))

# Check actual coordinate-set recursion and disjointness.
A={-1,0,1}
for k in range(13):
    a=2**k
    assert len(A)==3*a and min(A)==-(2*a-1) and max(A)==2*a-1
    if k:
        assert 2*a-1-a==a-1
    if k<12:
        shift=2**(k+1)
        left={x-shift for x in A};right={x+shift for x in A}
        assert left.isdisjoint(right)
        A=left|right

for k in range(30):
    a=2**k;R,N,parts=geometry(k)
    traversal=sum((Q(d,n) for d,n in parts),Q(0))
    assert traversal==Q(4,9)*(1-Q(1,a))
    w=2*a-1
    total=Q(w,N)+traversal
    assert total==Q(4,9)-Q(2*a+1,9*a*a)
    assert Q(9,4)*total<1
    assert N*(1-traversal)-w-1==5*a*a+2*a

cases=0; profile_checks=0; maximal_F=(Q(0),None)
for ka in range(14):
 for kc in range(14):
    a,c=2**ka,2**kc
    Dc=5*c*c+2*c;Bc=Q(9*c*c,Dc)
    downstream,Dc_computed=prep(kc,2*c-1,[(Q(1),Q(1))])
    assert Dc_computed==Dc
    profiles,D=prep(ka,2*a-1,downstream)
    if a<c:
        Da=5*a*a+2*a;Ba=Q(9*a*a,Da)
        assert D==Da
        assert profiles==[(Q(1),Q(1)),(Ba,Q(1,Da)),(Ba*Bc,Ba/Dc)]
        g=lambda x:Q(4*x-2,x*(5*x+2))
        F=Q(4,9)*(1+g(a)+Ba*g(c))
        assert F<Q(27,35)<1
        for kb in range(18):
            b=2**kb
            wanted=Q(1,9*b*b) if b<a else (Ba/Q(9*b*b) if b<c else Ba*Bc/Q(9*b*b))
            assert inc(profiles,9*b*b)==wanted
            profile_checks+=1
    else:
        expected_D=a*a*(5-4*(Bc-1)/c)+2*Bc*a
        assert D==expected_D
        lam=Q(25,9)-Q(6,9*c)+Q(8,9*c*c)
        assert Q(8,3)<=lam<=3
        assert D/Bc==lam*a*a+2*a
        h=Bc/D
        assert profiles[-1]==(9*a*a*h,h)
        F=Q(4,9)-Q(4,9*a)+Q(4,1)/(lam*a+2)
        assert F<=Q(4,5)<1
        for kb in range(18):
            b=2**kb
            wanted=Q(1,9*b*b) if b<a else a*a*h/(b*b)
            assert inc(profiles,9*b*b)==wanted
            profile_checks+=1
    if F>maximal_F[0]:maximal_F=(F,(a,c))
    for kt in range(16):
        tscale=2**kt
        assert terminal(kt,2*tscale-1,profiles)<F
    cases+=1

# Exact certificate failure for a fourth deadline, not an actual game loss.
p=[(Q(1),Q(1))];Ds=[];farthest=[]
for _ in range(3):
    p,D=prep(0,1,p)
    Ds.append(D);farthest.append(p[-1])
assert Ds==[Q(7),Q(45,7),Q(27,5)]
assert farthest==[(Q(9,7),Q(1,7)),(Q(9,5),Q(1,5)),(Q(3),Q(1,3))]
assert terminal(2,0,p)==1

here=Path(__file__).parent
receipt={
 'status':'PASS',
 'scope':'Exact checks accompanying a symbolic arbitrary-three-known-deadline proof; not exhaustive strategy search',
 'dyadic_gap_scale_pairs':cases,
 'profile_band_checks':profile_checks,
 'initial_deadline_scale_checks':cases*16,
 'maximal_infinite_cost':str(maximal_F[0]),
 'maximizing_gap_scales':maximal_F[1],
 'four_deadline_certificate_failure':{'times':[7,9,11,13],'bound':'1','meaning':'Insufficient strict bound, not a Devil win'},
 'proof_sha256':sha256((here/'THREE_DEADLINES.md').read_bytes()).hexdigest(),
 'induction_limit_sha256':sha256((here/'INDUCTION_LIMIT.md').read_bytes()).hexdigest(),
}
print(json.dumps(receipt,indent=2))
(here/'THREE_DEADLINES_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n')

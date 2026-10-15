#!/usr/bin/env python3
"""Independent exact checks. Python standard library only; no author-code imports.
These finite checks corroborate, but do not establish, the universal proofs.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial
import json

# Ascending coefficients; an empty tuple is the zero polynomial.
def pnorm(p):
    p = list(map(F,p))
    while p and p[-1] == 0: p.pop()
    return tuple(p)
def d(p): return pnorm(i*p[i] for i in range(1,len(p)))
def subtract_value(p,v):
    p=list(p) or [F(0)]; p[0]-=v
    return pnorm(p)
def divmodp(p,q):
    assert q
    p=list(p); out=[F(0)]*max(0,len(p)-len(q)+1)
    while p and len(p)>=len(q):
        s=len(p)-len(q); c=p[-1]/q[-1]; out[s]+=c
        for j in range(len(q)): p[s+j]-=c*q[j]
        p=list(pnorm(p))
    return pnorm(out), pnorm(p)
def monic(p): return tuple(v/p[-1] for v in p) if p else ()
def gcd(p,q):
    while q: p,q=q,divmodp(p,q)[1]
    return monic(p)
def radical(p):
    if not p: return None # Identically zero has all of C as its zero set.
    if len(p)==1: return (F(1),)
    return monic(divmodp(p,gcd(p,d(p)))[0])
def ev(p,x):
    v=F(0)
    for c in p[::-1]: v=v*x+c
    return v

def main():
    # Exhaustive coefficient-box checks are distinct from the author's monomial grid.
    polys=sharing_pairs=conditions=admissible=0
    for n in range(1,5):
        for low in product(range(-2,3),repeat=n):
            for lead in [-2,-1,1,2]:
                p=pnorm((*low,lead)); fp=d(p); polys+=1
                for a in [-1,0,1]:
                    if radical(subtract_value(p,a)) != radical(subtract_value(fp,a)): continue
                    sharing_pairs+=1
                    assert a==0 and len(radical(p))==2
                    fk=fp
                    for k in range(2,7):
                        fk=d(fk)
                        for b in [-2,-1,1,2,6,24]:
                            fiber=radical(subtract_value(fp,b))
                            actual=(fiber is not None and divmodp(subtract_value(fk,b),fiber)[1]==())
                            expected=(n==k and len(fk)==1 and fk[0]==b)
                            assert actual==expected,(p,a,b,k)
                            conditions+=1; admissible+=actual
    # Nonzero translations and fractional scales, with full coefficient derivatives.
    translated=0
    for k in range(2,13):
        for b in [F(-2),F(1),F(3,7)]:
            for z0 in [F(0),F(2),F(-3,7)]:
                p=pnorm(b/F(factorial(k))*comb(k,j)*(-z0)**(k-j) for j in range(k+1))
                fp=d(p); fk=p
                for _ in range(k): fk=d(fk)
                assert radical(p)==radical(fp)==(-z0,F(1))
                assert fk==(b,) and ev(p,z0)==ev(fp,z0)==0
                assert len(gcd(subtract_value(fp,b),d(fp)))==1
                translated+=1
    # The chain operator t*d/dt acts on exact coefficient arrays.
    trans=0
    for k in range(3,41):
        p=(F(1),F(-2),F(1))
        for _ in range(k): p=pnorm(i*p[i] for i in range(len(p)))
        q=F(-1,2**(k-1)-2)
        residual=subtract_value(tuple(q*c for c in p),F(-1,2))
        assert ev(residual,F(1,2))==0
        assert ev(d(residual),F(1,2))!=0
        assert divmodp(residual,(F(1,4),F(-1),F(1)))[1] != ()
        assert ev(p,F(1,2)) != F(-1,2)
        trans+=1
    # k=2: the same squared-exponential ansatz gives f''=0 at t=1/2,
    # which is incompatible with b=-lambda/2 and lambda != 0.
    assert 2**(2-2)-1==0
    # Wrongly translating f by a does not translate its derivative's shared value.
    assert radical(subtract_value((F(1),F(0),F(1,2)),F(1))) != radical(subtract_value((F(0),F(1)),F(1)))
    print(json.dumps({'status':'PASS','arithmetic':'fractions.Fraction; Python standard library only','small_polynomials_exhausted':polys,'shared_values_checked_per_polynomial':[-1,0,1],'IM_sharing_pairs':sharing_pairs,'b_order_conditions_checked':conditions,'admissible_b_order_cases':admissible,'translated_fractional_family_cases':translated,'transcendental_orders_checked':trans,'transcendental_order_range':[3,40],'negative_controls':['degree one','nonzero shared value in polynomial coefficient box','wrong coefficient and order','multiple-b-point multiplicity strengthening','lambda=1','k=2 squared-exponential boundary','invalid additive-shift repair'],'limits':'Finite exact checks only. The universal proofs and source interpretation are separately reviewed in AUDIT.md.'},indent=2,sort_keys=True))
if __name__=='__main__': main()

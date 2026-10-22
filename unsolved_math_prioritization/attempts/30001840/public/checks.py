#!/usr/bin/env python3
"""Finite controls for stated formulas; no empirical output is an all-primes proof."""
import json
from collections import deque, Counter

def matrix_group(p):
    # O/pO = F_p[w]/(w^2+w-1). Works as a finite ring also at p=5.
    n=p*p
    def add(a,b):return ((a%p+b%p)%p)+p*((a//p+b//p)%p)
    def neg(a):return ((-a%p)%p)+p*((-(a//p))%p)
    def mul(a,b):
        x,y=a%p,a//p;z,v=b%p,b//p
        return ((x*z+y*v)%p)+p*((x*v+y*z-y*v)%p)
    one=1; zero=0; w=p
    c=add(2%p,w)
    I=(1,0,0,1)
    def prod(A,B):
        a,b,c,d=A;e,f,g,h=B
        return (add(mul(a,e),mul(b,g)),add(mul(a,f),mul(b,h)),add(mul(c,e),mul(d,g)),add(mul(c,f),mul(d,h)))
    U=(1,1,0,1); V=(1,0,neg(c),1)
    gens=(U,V)
    G={I}; Q=deque([I])
    while Q:
        A=Q.popleft()
        for B in gens:
            AB=prod(A,B)
            if AB not in G:G.add(AB);Q.append(AB)
    def powmat(A,k):
        B=I
        while k:
            if k%2:B=prod(B,A)
            A=prod(A,A);k//=2
        return B
    assert all(add(mul(a,d),neg(mul(b,c)))==1 for a,b,c,d in G)
    minusI=(neg(1),0,0,neg(1))
    assert powmat(prod(U,V),5)==minusI
    expected={2:10,3:120,5:15000,7:117600}[p]
    assert len(G)==expected,(p,len(G))
    result={'p':p,'ring_order':n,'generated_order':len(G),'minus_I_present':minusI in G,'projective_order':len(G)//(1 if p==2 else 2)}
    if p==3:
        # All element orders provide a supplementary binary-icosahedral fingerprint.
        orders=Counter()
        for A in G:
            B=I
            for k in range(1,121):
                B=prod(B,A)
                if B==I:orders[k]+=1;break
        result['element_order_counts']=dict(sorted(orders.items()))
        assert result['element_order_counts']=={1:1,2:1,3:20,4:30,5:24,6:20,10:24}
    return result

def scalar_controls():
    # Exact integer/Laurent polynomial verification through evaluations is only a
    # control; the symbolic identity is proved by a binomial expansion in the text.
    D=lambda x:x**5-5*x**3+5*x
    from fractions import Fraction
    count=0
    for a in range(-20,21):
        if a==0:continue
        u=Fraction(a,3)
        assert D(u+1/u)==u**5+u**-5;count+=1
    # Affine F_5 action on five roots and its even-slope dihedral subgroup.
    G={tuple((a*i+b)%5 for i in range(5)) for a in range(1,5) for b in range(5)}
    H={tuple((a*i+b)%5 for i in range(5)) for a in [1,4] for b in range(5)}
    assert len(G)==20 and len(H)==10
    return {'rational_identity_controls':count,'affine_group_order':len(G),'dihedral_group_order':len(H)}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--primes',nargs='+',type=int,default=[2,3,5,7]);args=parser.parse_args()
    print(json.dumps({'scope':'Finite abstract two-generator matrix controls; not a computation of an unproved integral lattice identification.','scalar':scalar_controls(),'matrix_groups':[matrix_group(p) for p in args.primes]},indent=2,sort_keys=True))

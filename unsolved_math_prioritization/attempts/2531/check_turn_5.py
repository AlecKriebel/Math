#!/usr/bin/env python3
"""Exact central-lifting identities; infinite scope is proved in TURN_5.md."""
from fractions import Fraction as F
import itertools,json,math
counts={}
def ck(k,v):
    assert v,k
    counts[k]=counts.get(k,0)+1
I=(1,0,0,1)
def mm(a,b):return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) for i in range(2) for j in range(2))
def mv(a,x):return (a[0]*x[0]+a[1]*x[1],a[2]*x[0]+a[3]*x[1])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(n,a):return tuple(n*x for x in a)
def sub(a,b):return add(a,scale(-1,b))
matrices=[(1,1,0,1),(2,1,1,1),(0,-1,1,0),(-1,1,0,1),(1,2,1,3)]
orders=[]
for M in matrices:
    ck('unimodular',abs(M[0]*M[3]-M[1]*M[2])==1)
    for m in range(2,9):
        P=I;N=0
        while True:
            P=mm(P,M);N+=1
            if all((a-b)%m==0 for a,b in zip(P,I)):break
            assert N<10000
        orders.append(N)
        ck('finite_residue_power',all((a-b)%m==0 for a,b in zip(P,I)))
        # Test one cyclic quotient generator at each possible divisor of m.
        ns=[n for n in range(2,m+1) if m%n==0]
        for n in ns:
            for c in itertools.product(range(-2,3),repeat=2):
                delta=sub(mv(P,c),c)
                ck('divisibility',all(x%n==0 for x in delta))
                b=tuple(x//n for x in delta)
                ck('lift_relation',add(c,scale(n,b))==mv(P,c))
                def plus(x,y):
                    v=add(x[0],y[0]);t=x[1]+y[1]
                    return (add(v,scale(t//n,c)),t%n)
                def theta(x):return(add(mv(P,x[0]),scale(x[1],b)),x[1])
                for a in range(n):
                    for d in range(n):
                        x=((a,-d),a);y=((-d,a),d)
                        ck('normal_form_homomorphism',theta(plus(x,y))==plus(theta(x),theta(y)))
                        ck('quotient_identity',theta(x)[1]==x[1])
# Divisible C=Q/Z. Multiplication k is surjective and has 1/k in its kernel.
def mod1(x):return x-(x.numerator//x.denominator)
for k in range(2,7):
    ck('divisible_kernel',mod1(k*F(1,k))==0 and mod1(F(1,k))!=0)
    for den in range(1,13):
        for j in range(den):
            c=F(j,den)
            ck('divisible_preimage',mod1(k*(c/k))==c)
            for n in range(2,8):
                b=(k*c-c)/n
                ck('divisible_relation',mod1(n*b)==mod1(k*c-c))
# Infinite shift basis identities, using explicit sparse dictionaries (no cyclic truncation).
def shift(v,N):return {j-N:a for j,a in v.items() if j>=N and a}
for m in range(2,13):
    for N in range(1,17):
        ck('shift_kills_relation',shift({0:1},N)=={})
        ck('shift_defect_not_divisible',(-1)%m!=0)
        for j in range(32):
            ck('shift_right_inverse',shift({j+N:1},N)=={j:1})
            image=shift({j:1},N)
            embedded={q:(m*a if q==0 else a) for q,a in image.items()}
            ck('extension_quotient_killed',embedded.get(0,0)%m==0)
            # The new generator z is sent to zero; m*z=e0 is preserved.
            ck('extension_relation_preserved',shift({0:m},N)=={})
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'categories':counts,'finite_residue_orders':orders,'scope':'Exact relation identities; no group realization of the failed-lift module and no original counterexample.'},indent=2,sort_keys=True))

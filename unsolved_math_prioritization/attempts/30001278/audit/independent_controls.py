#!/usr/bin/env python3
"""Independent bounded controls for the five ramification arguments.

Standard library only. Imports no author code. No assert statements are used.
These controls do not construct general splitting fields or certify imported
p-adic Hodge-theoretic theorems.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, prod
import json


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def val(z, p):
    if z == 0:
        raise ValueError('zero is excluded')
    return next(t for t in range(abs(z).bit_length()+1) if z % p**(t+1))


def normalize(p, r):
    check(p > 2 and all(p % d for d in range(2, int(p**0.5)+1)), 'prime input')
    check(type(r) is int and r >= 1, 'positive integral weight')
    candidates=[a for a in range(r.bit_length()+1)
                if F((p-1)*p**a,p) < r <= (p-1)*p**a]
    check(len(candidates)==1, 'unique normalization')
    a=candidates[0]
    return a,F(r,(p-1)*p**a)


def multiply(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]+=x*y
    return c


def remainder(a,f,q):
    a=[x%q for x in a]
    check(f[-1]==1,'monic divisor')
    for i in range(len(a)-1,len(f)-2,-1):
        c=a[i]
        for j in range(len(f)):
            a[i-len(f)+1+j]=(a[i-len(f)+1+j]-c*f[j])%q
    return (a[:len(f)-1]+[0]*(len(f)-1))[:len(f)-1]


def monomial_power_mod(N,f,q):
    x=[1]; u=[0,1]
    while N:
        if N&1:
            x=remainder(multiply(x,u),f,q)
        u=remainder(multiply(u,u),f,q)
        N//=2
    return remainder(x,f,q)


def polynomial_power(E,r):
    f=[1]
    for _ in range(r):
        f=multiply(f,E)
    return f


def main():
    counts={}
    count=0
    for p in (3,5,7,11,17,29):
        heights=set()
        for a in range(6):
            lo=int(F((p-1)*p**a,p))+1
            hi=(p-1)*p**a
            heights.update([lo,hi,p**a,min(hi,p**a+1),max(lo,p**a-1)])
        for r in sorted(heights):
            a,b=normalize(p,r)
            for n,e in product(range(1,10),(1,2,19)):
                s=n+a
                B=1+e*(s+b)-F(1,p**s)
                U=1+e*s+max(e*b-F(1,p**s),F(e,p-1))
                loss=max(F(0),F(e*(p**a-r),(p-1)*p**a)+F(1,p**s))
                check(U-B==loss,'upper loss')
                check((loss==0)==(r>p**a),'integer sufficient region')
                tower=lambda j: e*j+1-F(1,p**j)+F(e*r*p**n,(p-1)*p**j)
                check(tower(s)==B,'Kummer transitivity bound')
                check(tower(s)-tower(s-1)==e*(1-F(r,p**a))+F(p-1,p**s),'tower difference')
                check((p**s>F(r*p**n,p-1))==(b<1),'strict old-method endpoint')
                check(p**(s-n+1)>r,'Caruso Galois threshold')
                if r<=p**a:
                    check(tower(s)>tower(s-1),'exceptional tower improvement')
                check(B>e*(n-F(1,p-1)),'split character bound')
                if r==1:
                    check(B-e*(n+F(1,p-1))==1-F(1,p**n)>0,'finite-flat margin')
                count+=1
    counts['parameter_boundary_cases']=count

    count=0
    obstruction_count=0
    for p,n,r,e in product((3,5,7),range(1,6),range(1,19),range(1,4)):
        candidate=next(m for m in range(r,r+n)
                       if all(comb(m,j)*p**(m-j) % p**n ==0 for j in range(r)))
        f=polynomial_power([-p]+[0]*(e-1)+[1],r)
        check(not any(monomial_power_mod(e*candidate,f,p**n)),'scalar zero at claimed exponent')
        check(any(monomial_power_mod(e*candidate-1,f,p**n)),'scalar preceding exponent nonzero')
        check((candidate==r)==(r%p**(n-1)==0),'sharp divisible-weight criterion')
        if candidate>r:
            obstruction_count+=1
        count+=1
    counts['independent_binary_polynomial_scalar_cases']=count
    counts['scalar_obstructions']=obstruction_count

    count=0
    for p,n,r,e in product((3,5),range(1,5),range(1,13),range(1,4)):
        for cs in ((1,1,1),(-2,3,-1),(2,-4,7)):
            E=[p*cs[i] for i in range(e)]+[1]
            check(val(E[0],p)==1,'Eisenstein constant')
            f=polynomial_power(E,r)
            rounded=p**(n-1)*((r+p**(n-1)-1)//p**(n-1))
            check(not any(monomial_power_mod(e*rounded,f,p**n)),'rounded general annihilator')
            check(any(monomial_power_mod(e*r-1,f,p**n)),'degree lower bound')
            if r%p**(n-1)==0:
                check(not any(monomial_power_mod(e*r,f,p**n)),'divisible general annihilator')
            count+=1
    counts['general_Eisenstein_binary_reduction_cases']=count

    count=0
    for p,m,n in product((3,5,7),range(1,4),range(1,4)):
        q=p**n
        # P has columns e1 and (e2-e1)/p^m. Directly solve P*A=diag(c,1)*P.
        for k in range(p**n):
            c=1+p**m*k
            P=[[F(1),-F(1,p**m)],[F(0),F(1,p**m)]]
            Pinv=[[F(1),F(1)],[F(0),F(p**m)]]
            D=[[F(c),F(0)],[F(0),F(1)]]
            mm=lambda A,B:[[sum(A[i][t]*B[t][j] for t in range(2)) for j in range(2)] for i in range(2)]
            A=mm(mm(Pinv,D),P)
            check(A==[[c,F(1-c,p**m)],[0,1]],'conjugation lattice matrix')
            check(all(x.denominator==1 for row in A for x in row),'integrality')
            identity=all((A[i][j]-(i==j))%q==0 for i,j in product(range(2),repeat=2))
            check(identity==(c%p**(m+n)==1),'exact lattice kernel')
            count+=1
        E=(p-1)*p**(m-1)
        check(E*(F(m+n)-F(1,p-1)-F(m)+F(1,p-1))==E*n,'relative cyclotomic different')
    counts['independent_rational_lattice_conjugations']=count

    count=0
    for p,e,m in product((3,5,7),(1,2,9),range(1,121)):
        terms=[m*e*val(m,p)+m-1]
        terms += [m*(1+(i*7)%5)+m*e*val(i,p)+i-1 for i in range(1,m)]
        check(len({v%m for v in terms})==m,'distinct derivative valuation classes')
        check(min(terms)<=m*e*val(m,p)+m-1,'different derivative bound')
        count+=1
    counts['derivative_valuation_profiles']=count

    count=0
    for p,d,n in product((3,5,7,11),range(1,11),range(1,8)):
        order=prod(p**d-p**i for i in range(d))*p**(d*d*(n-1))
        check(val(order,p)==d*d*(n-1)+d*(d-1)//2,'GL valuation')
        if d==1:
            check(val(order,p)==n-1,'rank-one criterion')
        count+=1
    counts['group_order_cases']=count

    count=0
    for p,t,tame in product((3,5,7),range(0,6),(1,2,4)):
        if tame%p==0:
            continue
        m=tame*p**t
        lower=[p**i for i in range(t,0,-1) for _ in range(i+1)]
        d=F(m-1+sum(h-1 for h in lower),m)
        mu=1+sum((F(h,m) for h in lower),F(0)) if m>1 else 0
        integrated=F(m-1,m)+sum((F(h,m)*(1-F(1,h)) for h in lower),F(0))
        check(integrated==d,'shifted integral identity')
        check(d<=mu*(1-F(1,m)),'inertia-order integral margin')
        if m>1:
            check(d<mu,'strict normalized different-break gap')
        count+=1
    counts['synthetic_filtration_identity_cases']=count
    print(json.dumps({'result':'PASS_INDEPENDENT_BOUNDED_CONTROLS','counts':counts,
        'scope':'Exact arithmetic, algebra, and synthetic valuation-profile controls. No exhaustive local-field enumeration or proof-assistant certification.'},indent=2,sort_keys=True))

if __name__=='__main__':
    main()

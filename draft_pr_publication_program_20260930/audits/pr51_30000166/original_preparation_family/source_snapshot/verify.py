#!/usr/bin/env python3
"""Bounded exact transcription controls; no numerical inference of positivity."""
from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import gcd, isqrt
import json

checks = 0

def check(x):
    global checks
    assert x
    checks += 1

def factors(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p += 1
    if n > 1: out[n] = 1
    return out

def mu(n):
    f = factors(n)
    return 0 if any(a > 1 for a in f.values()) else (-1)**len(f)

def phi(n):
    for p in factors(n): n = n//p*(p-1)
    return n

def divisors(n): return [d for d in range(1,n+1) if n%d == 0]

def exponents(n, L):
    return [0]+[phi(n)*(k%n == 0)-sum(mu(d) for d in divisors(n) if k%d == 0) for k in range(1,L+1)]

def series(exps, L):
    a = [1]+[0]*L
    for k, e in enumerate(exps):
        if not k: continue
        for _ in range(abs(e)):
            if e > 0:
                for j in range(L,k-1,-1): a[j] -= a[j-k]
            else:
                for j in range(k,L+1): a[j] += a[j-k]
    return a

def Q(n):
    a=len(n)
    twice=a*sum(v*v for v in n)+2*sum(i*v for i,v in enumerate(n))
    assert twice%2 == 0
    return twice//2

def T(n,j):
    out=list(n[1:]+n[:1])
    if j:
        out[j-1] += 1
        out[-1] -= 1
    return tuple(out)

L=48
for n in range(1,121):
    for k in (1,2,3,6,17,30):
        check(sum(mu(d) for d in divisors(gcd(n,k))) == int(gcd(n,k)==1))
    if n > 1:
        p=2 if n%2==0 else min(factors(n))
        alpha=factors(n)[p]
        M=n//p**alpha
        Np=p*M
        t=p**(alpha-1)
        check(M%2==1 and gcd(p,M)==1)
        check(phi(n)==t*phi(Np))
        target=exponents(n,L)
        lifted=[v+phi(Np)*(t*(k%n==0)-(k%Np==0)) for k,v in enumerate(exponents(Np,L))]
        lifted[0]=0
        check(target==lifted)
        if M>1:
            rs=[r for r in range(1,(M+1)//2) if gcd(r,M)==1]
            check(2*len(rs)==phi(M))
            exp=[0]*(L+1)
            for r in rs:
                for k in range(1,L+1):
                    exp[k]+=(2*p-2)*(k%(p*M)==0)
                    exp[k]+=int(k%(p*M) in (p*r,p*(M-r)))
                    exp[k]-=int(k%M in (r,M-r))
            check(exp==exponents(Np,L))
    if n <= 40:
        coeff=series(exponents(n,L),L)
        check(coeff[0]==1 and min(coeff)>=0)
    A=Fraction(n*phi(n)-sum(d*mu(d) for d in divisors(n)),24)
    check(A>=0)
    if len(factors(n))==1 and factors(n)[next(iter(factors(n)))]==1:
        check(A==Fraction(n*n-1,24))
check(series(exponents(1,L),L)==[1]+[0]*L)

for a in (2,3,5):
    for ns in product((-1,0,1),repeat=a-1):
        n=tuple(ns)+(-sum(ns),)
        check(Q(n)>=0)
        for j in range(a):
            check(Q(T(n,j))-Q(n)==a*n[j]+j)
            for M,r in ((3,1),(5,2)):
                e=M*Q(n)+r*(a*n[j]+j)
                check(e==(M-r)*Q(n)+r*Q(T(n,j)) and e>=0)

# Fully bounded theta coefficients: e >= (M-r)Q(n), and each coordinate
# contributes >= a*|n_i|*(|n_i|-1)/2 to Q. The chosen B is safely larger
# than any coordinate capable of contributing through degree H.
H=24
theta_cases=[]
for a,M,r in ((2,3,1),(2,5,2),(3,5,1),(3,5,2)):
    B=2+isqrt(2*H//(a*(M-r)))
    theta=[0]*(H+1)
    for ns in product(range(-B,B+1),repeat=a-1):
        n=tuple(ns)+(-sum(ns),)
        for j in range(a):
            e=M*Q(n)+r*(a*n[j]+j)
            if e<=H: theta[e]+=1
    exp=[0]*(H+1)
    for k in range(1,H+1):
        exp[k]+=int(k%M==0)+(a-2)*int(k%(a*M)==0)
        exp[k]+=int(k%(a*M) in (a*r,a*(M-r)))
        exp[k]-=int(k%M in (r,M-r))
    check(theta==series(exp,H))
    theta_cases.append({'a':a,'M':M,'r':r,'degree':H,'coordinate_bound':B})
print(json.dumps({'status':'PASS','assertions':checks,'normalized_products_checked':40,'product_degree':L,'factorizations_checked_through_N':120,'theta_cases':theta_cases,'limitation':'Finite exact controls only; the proof uses the credited core and theta identities.'},indent=2,sort_keys=True))

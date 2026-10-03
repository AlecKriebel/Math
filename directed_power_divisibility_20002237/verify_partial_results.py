#!/usr/bin/env python3
"""Bounded exact regression checks. These do not replace the written proofs.
Standard library only; deterministic; writes JSON to stdout.
"""
from fractions import Fraction
from itertools import product
from math import gcd
import json
import random

PRIMES = (2, 3, 5, 7)
counts = {}

def rp(p, x, y):
    if x == 0:
        return y == 0
    if y % x:
        return False
    t = y // x
    if t < 1:
        return False
    while t % p == 0:
        t //= p
    return t == 1

def core(p, x):
    if x == 0:
        return None
    while x % p == 0:
        x //= p
    return x

def pow_member(p, f):
    return f.denominator == 1 and rp(p, 1, f.numerator)

def nr_formula(p, x, y):
    ux, uy = core(p, x), core(p, y)
    return ((x == 0 and y != 0) or (y == 0 and x != 0)
            or (ux is not None and uy is not None and ux != uy)
            or (y != 0 and rp(p, p*y, x)))

def gp_formula(p, U, x, y):
    if not rp(p, 1, U):
        return False
    r = 3 if p == 2 else 2
    c = (r-x) % (p*p)
    assert 0 <= c < p*p and (x+c-r) % (p*p) == 0
    return rp(p, x+c, y+c*U) and rp(p, x+c+p, y+(c+p)*U)

n=0
for p, x, y in product(PRIMES, range(-64,65), range(-64,65)):
    assert nr_formula(p,x,y) == (not rp(p,x,y)), (p,x,y)
    n+=1
counts['directed_complement_pairs']=n

n=0
for p,x in product(PRIMES, range(-512,513)):
    u=core(p,x)
    assert ((u is not None and u%p != 0 and rp(p,u,x)) == (x != 0))
    n+=1
counts['nonzero_witnesses']=n

n=0; exceptional=0
for p,x,a,b,u in product(PRIMES,range(-100,101),range(8),range(8),range(8)):
    if x%p==0:
        continue
    A,B,U=p**a,p**b,p**u
    if A*x+p*U==B*(x+p) and (A!=U or B!=U):
        assert x in (1,-p-1), (p,x,a,b,u)
        exceptional+=1
    n+=1
counts['synchronization_assignments']=n
counts['genuine_exceptional_assignments']=exceptional

n=0
for p,u,x,y in product(PRIMES,range(6),range(-32,33),range(-64,65)):
    U=p**u
    assert gp_formula(p,U,x,y)==(y==U*x), (p,U,x,y)
    n+=1
counts['named_power_graph_assignments']=n

n=0
for p,a,b,c in product(PRIMES,range(13),range(13),range(13)):
    d=gcd(p**a-1,p**b-1)
    assert d==p**gcd(a,b)-1
    rhs=p**c-1
    actual=(rhs==0 if d==0 else rhs%d==0)
    e=gcd(a,b)
    expected=(c==0 if e==0 else c%e==0)
    assert actual==expected
    n+=1
counts['multi_exponent_gcd_cases']=n

def trim(a):
    a=list(a)
    while a and a[-1]==0:
        a.pop()
    return a

def peval(a,T):
    out=0
    for c in reversed(a):
        out=out*T+c
    return out

def vp(p,a):
    a=abs(a)
    assert a
    n=0
    while a%p==0:
        a//=p; n+=1
    return n

def rational_tail(p,G,H):
    """Returns a proved threshold S and constant tail truth value."""
    G,H=trim(G),trim(H)
    assert H
    if not G:
        return 0,False
    a=next(i for i,v in enumerate(G) if v)
    b=next(i for i,v in enumerate(H) if v)
    g,h=G[a:],H[b:]
    c=vp(p,g[0])-vp(p,h[0])
    S=1+max(vp(p,g[0]),vp(p,h[0]))
    facg,fach=p**max(-c,0),p**max(c,0)
    K=trim([facg*(g[i] if i<len(g) else 0)-fach*(h[i] if i<len(h) else 0)
            for i in range(max(len(g),len(h)))])
    if K:
        B=0 if len(K)==1 else 1+(max(map(abs,K[:-1]))+abs(K[-1])-1)//abs(K[-1])
        while p**S <= B:
            S+=1
        return S,False
    d=a-b
    if d==0:
        return S,c>=0
    if d>0:
        S=max(S,(-c+d-1)//d,0)
        return S,True
    S=max(S,c//(-d)+1,0)
    return S,False

rng=random.Random(20002237)
cases=[([0],[1]),([1],[1]),([-1],[1]),([0,1],[1]),([1],[0,1]),
       ([1,1],[1,1]),([0,0,4],[1]),([1,0,1],[1]),([0,3],[1]),
       ([1,-2,1],[1,-1]),([1,2],[1,3])]
for _ in range(300):
    G=[rng.randrange(-4,5) for _ in range(rng.randrange(1,5))]
    H=[rng.randrange(-4,5) for _ in range(rng.randrange(1,5))]
    if not trim(H):H=[1]
    cases.append((G,H))
n=0; tail_cases=0
for p,(G,H) in product(PRIMES,cases):
    S,tail=rational_tail(p,G,H)
    tail_cases+=1
    for s in range(S,S+32):
        den=peval(H,p**s)
        actual=False if den==0 else pow_member(p,Fraction(peval(G,p**s),den))
        assert actual==tail,(p,G,H,S,tail,s)
        n+=1
counts['rational_function_tail_certificates']=tail_cases
counts['rational_function_tail_evaluations']=n

n=0
for a,b,c,d,x,y in product(range(-2,3),repeat=6):
    D=a*d-b*c
    if D==0:continue
    # Exact Cramer solvability versus equality of maximal-minor gcds.
    solvable=((d*x-b*y)%D==0 and (a*y-c*x)%D==0)
    delta_aug=gcd(abs(D),gcd(abs(a*y-c*x),abs(b*y-d*x)))
    assert solvable==(abs(D)==delta_aug)
    n+=1
counts['maximal_minor_lattice_checks']=n

def egcd(a,b):
    if b==0:return abs(a),(1 if a>=0 else -1),0
    g,u,v=egcd(b,a%b)
    return g,v,u-(a//b)*v

def universal_r(p,L,M):
    j=next((j for j,v in enumerate(L) if v),None)
    if j is None:return not any(M)
    U=Fraction(M[j],L[j])
    return pow_member(p,U) and all(Fraction(m)==U*l for l,m in zip(L,M))

n=0
for p in PRIMES:
    for _ in range(2000):
        q=[rng.randrange(-5,6),rng.randrange(-5,6)]
        if q==[0,0]:continue
        h=rng.randrange(-10,11)
        g,u,v=egcd(*q)
        if h%g:continue
        z0=[u*(h//g),v*(h//g)]
        kernel=[q[1]//g,-q[0]//g]
        L=[rng.randrange(-5,6) for _ in range(3)]
        M=[rng.randrange(-5,6) for _ in range(3)]
        LR=[L[0]+sum(L[i+1]*z0[i] for i in range(2)),sum(L[i+1]*kernel[i] for i in range(2))]
        MR=[M[0]+sum(M[i+1]*z0[i] for i in range(2)),sum(M[i+1]*kernel[i] for i in range(2))]
        j=next(i for i in range(2) if q[i])
        B=[L[0]*q[j]+L[j+1]*h]+[L[i+1]*q[j]-L[j+1]*q[i] for i in range(2)]
        A=[M[0]*q[j]+M[j+1]*h]+[M[i+1]*q[j]-M[j+1]*q[i] for i in range(2)]
        assert universal_r(p,LR,MR)==universal_r(p,B,A)
        n+=1
counts['fiber_identity_cross_product_checks']=n
print(json.dumps({'status':'PASS','problem_id':20002237,'test_kind':'bounded exact regression, not a substitute for proofs','counts':counts},indent=2))

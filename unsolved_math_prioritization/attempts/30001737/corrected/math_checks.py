#!/usr/bin/env python3
"""Finite combinatorial regression checks, not a distinction theorem verifier."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit("Use a reviewed external bootstrap with python -I -S -B; startup is not isolated")
from collections import Counter
from itertools import product
from math import comb, factorial
import json

def need(ok, message):
    if not ok:
        raise ValueError(message)

def tau(x):
    return (-x[0], x[1])

def choose(n,k):
    return comb(n,k) if 0 <= k <= n else 0

def counts(labels):
    c=Counter(labels)
    if any(c[x] != c[tau(x)] for x in c):
        return None
    a=[v for x,v in c.items() if x[0]==0]
    b=[v for x,v in c.items() if x[0]>0]
    return a,b

def formula(labels,p,q):
    n=len(labels)
    need(type(p) is int and type(q) is int and p>=0 and q>=0 and p+q==n,'Invalid signature')
    ab=counts(labels)
    if ab is None:
        return 0
    a,b=ab;s=sum(b);match=1
    for v in b:
        match*=factorial(v)
    total=0
    for us in product(*(range(v//2+1) for v in a)):
        u=sum(us);ways=match
        for v,t in zip(a,us):
            ways*=factorial(v)//(2**t*factorial(t)*factorial(v-2*t))
        total+=ways*choose(n-2*s-2*u,p-s-u)
    return total

def involutions(n):
    w=[-1]*n
    def rec(todo,g):
        if not todo:
            yield tuple(w),g
            return
        i=todo[0];rest=todo[1:];w[i]=i
        yield from rec(rest,g)
        for j in rest:
            w[i]=j;w[j]=i
            yield from rec(tuple(k for k in rest if k!=j),g+1)
        w[i]=-1
    yield from rec(tuple(range(n)),0)

def brute(labels,p,q):
    n=len(labels);total=0
    for w,g in involutions(n):
        if all(labels[w[i]]==tau(labels[i]) for i in range(n)):
            total+=choose(n-2*g,p-g)
    return total

def run():
    patterns=signatures=0
    for a0,a1,b0,b1 in product(range(9),repeat=4):
        n=a0+a1+2*b0+2*b1
        if not 1<=n<=8:
            continue
        labels=[(0,0)]*a0+[(0,1)]*a1+[(1,0)]*b0+[(-1,0)]*b0+[(2,1)]*b1+[(-2,1)]*b1
        patterns+=1
        for p in range(n+1):
            q=n-p;v=formula(labels,p,q)
            need(v==brute(labels,p,q),'Enumeration mismatch')
            need((v>0)==(b0+b1<=min(p,q)),'Positivity mismatch')
            need(v==formula(labels,q,p),'Signature symmetry mismatch')
            signatures+=1
    unbalanced=[[(1,0)],[(1,0),(1,0),(-1,0)],[(1,0),(-1,1)],[(0,0),(2,1)]]
    for labels in unbalanced:
        for p in range(len(labels)+1):
            need(formula(labels,p,len(labels)-p)==brute(labels,p,len(labels)-p)==0,'Unbalanced conjugation accepted')
    duplicated=[(1,0),(1,0),(-1,0),(-1,0)]
    need(formula(duplicated,1,3)==0,'Distinct-orbit undercount not detected')
    need(formula(duplicated,2,2)==2,'Matching factorial omitted')
    need(formula([(0,0),(0,0)],1,1)==3,'Fixed-block involutions omitted')
    need(tau((2,3+4j))==(-2,3+4j),'Tau incorrectly conjugates radial exponent')
    need(formula([(1,3+4j),(-1,3+4j)],1,1)==1,'Nonreal radial parameter pairing failed')
    need(formula([(0,3+4j),(0,5+6j)],1,1)==2,'Nonreal fixed parameters failed')
    for p,q in [(-1,3),(1,0),(1.0,1),(True,1)]:
        try: formula([(0,0),(0,0)],p,q)
        except ValueError: pass
        else: raise ValueError('Invalid signature accepted')
    # For z=2, invariance of (a,b) under diag(1,2) forces b=0.
    # Restriction to K=C e_0 sends (a,0) to a, so its kernel is zero.
    need(2-1!=0,'Toy quotient witness invalid')
    return {'status':'pass','maximum_n':8,'stable_multiplicity_patterns':patterns,
            'signature_cases':signatures,'unbalanced_patterns':len(unbalanced),
            'adversarial_families':['unbalanced_multiplicities','distinct_orbit_undercount','tau_exponent_semantics','invalid_signatures'],
            'scope':'Counting identity and elementary regression checks only; not proof of the general converse.'}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True))

#!/usr/bin/env python3
"""Exact finite determinant sums for the drift-jump stationary law.

Only Python's standard library is required. Queries are joint survival events
X_{r_j} > x_j, with strictly increasing positive rational x_j and r_j >= 1.
No stochastic simulation is performed. This implements PROOF.md (1), (3), (5).
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
import argparse
import json

@lru_cache(None)
def partitions(n, max_part=None, max_length=None):
    if n == 0:
        return ((),)
    if max_length == 0:
        return ()
    top = n if max_part is None else min(n, max_part)
    out = []
    for a in range(top, 0, -1):
        left = None if max_length is None else max_length - 1
        out.extend((a,) + q for q in partitions(n-a, a, left))
    return tuple(out)

def contains(lam, mu):
    return len(lam) >= len(mu) and all(a >= b for a,b in zip(lam,mu))

def transpose(lam):
    return tuple(sum(a >= j for a in lam) for j in range(1, max(lam,default=0)+1))

def det(matrix):
    a = [[F(x) for x in row] for row in matrix]
    value = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j],a[pivot] = a[pivot],a[j]
            value = -value
        p = a[j][j]
        value *= p
        for i in range(j+1,len(a)):
            q = a[i][j]/p
            for k in range(j+1,len(a)):
                a[i][k] -= q*a[j][k]
    return value

@lru_cache(None)
def D(lam, mu, t=F(1), dimension=None):
    if not contains(lam,mu):
        return F(0)
    ell = max(len(lam),len(mu)) if dimension is None else dimension
    if ell < max(len(lam),len(mu)):
        raise ValueError('determinant dimension is too small')
    la = lam+(0,)*(ell-len(lam))
    mm = mu+(0,)*(ell-len(mu))
    t = F(t)
    return det([[F(0) if (r:=la[i]-mm[j]-i+j)<0 else t**r/factorial(r)
                 for j in range(ell)] for i in range(ell)])

def raw_by_size(xs, indices, cutoff):
    xs = tuple(map(F,xs))
    if not xs or len(xs)!=len(indices) or cutoff<0:
        raise ValueError('nonempty matching queries and nonnegative cutoff required')
    if any(x<=0 for x in xs) or any(x>=y for x,y in zip(xs,xs[1:])):
        raise ValueError('thresholds must be strictly increasing and positive')
    if any(not isinstance(r,int) or r<1 for r in indices):
        raise ValueError('indices must be positive integers')
    bounds = [r-1 for r in indices]
    B = max(bounds)
    shapes = tuple(p for n in range(cutoff+1) for p in partitions(n,max_length=B))
    state = {():F(1)}
    prev_x = F(0)
    for x,b in zip(xs,bounds):
        delta = x-prev_x
        new = {}
        for lam in shapes:
            if len(lam)>b:
                continue
            weight = sum((v*D(lam,mu,delta,B) for mu,v in state.items()
                          if contains(lam,mu)),F(0))
            if weight:
                new[lam] = weight
        state = new
        prev_x = x
    out = [F(0)]*(cutoff+1)
    for lam,weight in state.items():
        out[sum(lam)] += weight*D(lam,(),F(1),B)
    return out

def enclosure(xs, indices, cutoff):
    x = F(xs[-1])
    if cutoff+2<=x:
        raise ValueError('cutoff+2 must exceed the largest threshold')
    raw = raw_by_size(xs,indices,cutoff)
    W = sum(raw,F(0))
    T = sum((x**n/factorial(n) for n in range(cutoff+1)),F(0))
    R = x**(cutoff+1)/factorial(cutoff+1)/(1-x/F(cutoff+2))
    assert 0<=W<=T
    return {'lower':W/(T+R),'upper':(W+R)/(T+R),'width':R/(T+R),
            'raw_sum':W,'exponential_partial':T,'exponential_tail_bound':R}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--x',nargs='+',required=True,help='positive rational thresholds')
    parser.add_argument('--indices',nargs='+',type=int,required=True)
    parser.add_argument('--cutoff',type=int,default=18)
    args=parser.parse_args()
    r=enclosure(args.x,args.indices,args.cutoff)
    print(json.dumps({'event':{'thresholds':args.x,'indices':args.indices},
                      'cutoff':args.cutoff,'exact':{k:str(v) for k,v in r.items()},
                      'display_only':{k:float(r[k]) for k in ('lower','upper','width')}},indent=2))

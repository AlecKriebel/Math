#!/usr/bin/env python3
"""Exact fixed-zero coefficient formula from Lagrange grid interpolation.

Independent of sparse polynomial multiplication. If e0=0, ej=n-2 and all other
exponents n-1, evaluates the coefficient by summing permutations of1,...,n-1.
"""
import argparse
from functools import reduce
from itertools import permutations
from math import factorial,gcd
from time import perf_counter


def coefficients(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)
           if j-i not in (1,n-1)]
    sums=[0]*n;checked=nonzero=0
    for tail in permutations(range(1,n)):
        checked+=1
        a=(0,)+tail
        s=[a[i]+a[(i+1)%n] for i in range(n)]
        f=1
        for i,j in pairs:
            z=s[j]-s[i]
            if z==0:
                break
            f*=z
        else:
            nonzero+=1
            inv=sum(tail[i]>tail[j] for i in range(n-1) for j in range(i+1,n-1))
            if inv%2:f=-f
            for j in range(1,n):sums[j]+=f*(n-1-a[j])
    H=1
    for k in range(1,n):H*=factorial(k)
    out=[]
    for value in sums[1:]:
        num=(-1)**len(pairs)*factorial(n-1)*value
        assert num%H==0
        out.append(num//H)
    return {'n':n,'permutations':checked,'nonzero_terms':nonzero,
            'coefficients':out,'gcd':reduce(gcd,map(abs,out),0)}


if __name__=='__main__':
    import json
    p=argparse.ArgumentParser();p.add_argument('--min-n',type=int,default=3)
    p.add_argument('--max-n',type=int,default=10);args=p.parse_args()
    for n in range(args.min_n,args.max_n+1):
        start=perf_counter();r=coefficients(n);r['seconds']=perf_counter()-start
        print(json.dumps(r),flush=True)

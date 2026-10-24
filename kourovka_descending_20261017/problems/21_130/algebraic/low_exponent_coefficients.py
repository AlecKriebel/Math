#!/usr/bin/env python3
"""Independent Lagrange formula for slackQ coefficients with t0=1.

Others have capn-1 except deficits totaling2: two caps n-2, or one capn-3.
The Vandermonde forces a permutation of0,...,n-1 with a0∈{0,1}.
"""
from itertools import permutations
from math import factorial,gcd
from functools import reduce
from time import perf_counter
import argparse,json


def probe(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n) if j-i not in(1,n-1)]
    targets=[(j,k) for j in range(1,n) for k in range(j,n)]
    sums=[0]*len(targets);checked=nonzero=0
    factorials=[factorial(i) for i in range(n)]
    for a0 in (0,1):
        for tail in permutations([i for i in range(n) if i!=a0]):
            checked+=1;a=(a0,)+tail
            s=[a[i]+a[(i+1)%n] for i in range(n)]
            f=1
            for i,j in pairs:
                z=s[j]-s[i]
                if not z:break
                f*=z
            else:
                nonzero+=1
                inv=a0+sum(tail[i]>tail[j] for i in range(n-1) for j in range(i+1,n-1))
                if inv%2:f=-f
                f*=factorials[n-1-a0]
                for z,(j,k) in enumerate(targets):
                    weight=(n-1-a[j])*(n-1-a[k]-(j==k))
                    sums[z]+=f*weight
    H=1
    for i in range(1,n):H*=factorials[i]
    witnesses=[];content=0
    for value,(j,k) in zip(sums,targets):
        num=(-1)**len(pairs)*value
        assert num%H==0
        coefficient=num//H
        t=[n-1]*n;t[0]=1;t[j]-=1;t[k]-=1
        witnesses.append({'exponents':t,'coefficient':coefficient})
        content=gcd(content,abs(coefficient))
    return {'n':n,'permutations':checked,'nonzero_terms':nonzero,
            'coefficients':witnesses,'gcd':content}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--min-n',type=int,default=4)
    p.add_argument('--max-n',type=int,default=10);args=p.parse_args()
    for n in range(args.min_n,args.max_n+1):
        start=perf_counter();r=probe(n);r['seconds']=perf_counter()-start
        print(json.dumps(r),flush=True)

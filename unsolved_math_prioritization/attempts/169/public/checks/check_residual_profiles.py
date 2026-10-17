#!/usr/bin/env python3
"""Rebuild small synthetic exact profiles and check final residual constants."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def choose(n,k):return comb(n,k) if 0<=k<=n else 0

def profiles(p,k):
    out={}
    for A in combinations(range(p),k):
        masks=[sum(1<<((a+t)%p) for a in A) for t in range(p)]
        covered=[0]*(1<<p);R=[p]*(p+1)
        for mask in range(1,1<<p):
            bit=mask&-mask;t=bit.bit_length()-1
            covered[mask]=covered[mask^bit]|masks[t]
        for mask,U in enumerate(covered):R[mask.bit_count()]=min(R[mask.bit_count()],p-U.bit_count())
        for m in range(1,p+1):R[m]=min(R[m],R[m-1])
        out[A]=R
    return out

def main():
    counters={'profiles':0,'swap_checks':0,'amplification_checks':0,'threshold_checks':0,'greedy_checks':0,'hypergeometric_means':0}
    for p in (2,3,5,7):
        for k in range(1,p+1):
            rows=profiles(p,k);g=[p]
            for i in range(p-k+1):g.append(g[-1]-(k*g[-1]+p-i-1)//(p-i))
            g.extend([0]*(p+1-len(g)))
            for i in range(1,p+1):
                x=F(p*choose(p-k,i),comb(p,i))
                require(x-i<g[i]<=x,'integer greedy sandwich')
            for A,R in rows.items():
                counters['profiles']+=1
                for a in A:
                    for b in set(range(p))-set(A):
                        Ap=tuple(sorted(set(A)-{a}|{b}))
                        for m in range(p+1):
                            require(abs(R[m]-rows[Ap][m])<=m,'improved residual swap constant')
                            counters['swap_checks']+=1
                for m in range(p+1):
                    require(R[m]<=g[m],'greedy profile upper bound');counters['greedy_checks']+=1
                    total=0
                    for T in combinations(range(p),m):total+=p-len({(a+t)%p for a in A for t in T})
                    require(F(total,comb(p,m))==F(p*choose(p-k,m),comb(p,m)),'fixed candidate hypergeometric mean');counters['hypergeometric_means']+=1
                    for n in range(p-m+1):
                        require(R[m+n]<=R[m]*R[n]//p,'same-A amplification');counters['amplification_checks']+=1
                    for r in range(1,5):
                        if r*m>p:continue
                        for c in range(r*m,p+1):
                            if R[c]>0:require(R[m]**r>=(c-r*m+1)*p**(r-1),'integer failure threshold')
                            counters['threshold_checks']+=1
    print(json.dumps({'status':'PASS','scope':'Synthetic exhaustive profiles for primes through seven, all nonempty set sizes; finite identities only.','counts':counters,'asymptotic_resolution_claimed':False},sort_keys=True,indent=2))
if __name__=='__main__':main()

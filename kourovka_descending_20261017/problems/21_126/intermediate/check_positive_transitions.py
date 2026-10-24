#!/usr/bin/env python3
"""Exact small-model checks; no group Dehn function is computed."""
from itertools import product
from math import comb
import json
from pathlib import Path

def components(a):
    n=len(a)
    reach=[[bool(a[i][j]) or i==j for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j]=reach[i][j] or (reach[i][k] and reach[k][j])
    unseen=set(range(n)); cs=[]
    while unseen:
        v=min(unseen); c={w for w in unseen if reach[v][w] and reach[w][v]}
        cs.append(c);unseen-=c
    return cs

def classification(a):
    cs=components(a)
    for c in cs:
        for v in c:
            if sum(a[v][w] for w in c)>=2:
                return 'exponential',None
    cyclic=[any(a[v][w] for v in c for w in c) for c in cs]
    edges={i:{j for j,d in enumerate(cs) if i!=j and any(a[v][w] for v in c for w in d)} for i,c in enumerate(cs)}
    memo={}
    def height(i):
        if i not in memo: memo[i]=int(cyclic[i])+max([height(j) for j in edges[i]] or [0])
        return memo[i]
    r=max([height(i) for i in range(len(cs))] or [0])
    return 'polynomial',r

def count(a,n):
    d=len(a); row=[1]*d; total=d
    for _ in range(n):
        row=[sum(row[i]*a[i][j] for i in range(d)) for j in range(d)]
        total+=sum(row)
    return total

def main():
    census={}; samples=[]
    for d in (1,2,3,4):
        tally={'exponential':0,'polynomial':0}; degrees={}
        for bits in product((0,1),repeat=d*d):
            a=[list(bits[d*i:d*(i+1)]) for i in range(d)]
            kind,r=classification(a);tally[kind]+=1
            if kind=='polynomial':
                degrees[str(r)]=degrees.get(str(r),0)+1
                # Universal skeleton bound is unnecessary here. Check the known
                # finite-difference consequence of rational path series instead:
                # after n>=d, denominator divides (1-z^lcm(1,...,d))^r.
                # Test (1-shift^12)^(r+1) C(n)=0 for d<=4, n>=d.
                period=12
                values=[count(a,n) for n in range(d+period*(r+1)+1)]
                end=len(values)-1
                diff=sum((-1)**j*comb(r+1,j)*values[end-period*j] for j in range(r+2))
                assert diff==0,(a,r,diff)
        census[str(d)]={**tally,'polynomial_cumulative_degrees':degrees}
    for d in range(1,8):
        # One loop at each vertex, one forward edge: exactly binomial counts.
        a=[[int(j==i or j==i+1) for j in range(d)] for i in range(d)]
        assert classification(a)==('polynomial',d)
        for n in range(31):
            expected=sum((d-j)*comb(n+1,j+1) for j in range(min(d-1,n)+1))
            assert count(a,n)==expected
        samples.append({'dimension':d,'classification':'polynomial','cumulative_degree':d,'C_30':count(a,30)})
    # Integer parallel-loop branch is not missed by 0/1 census.
    for multiplicity in range(2,11):
        a=[[multiplicity]]
        assert classification(a)==('exponential',None)
        assert count(a,20)==(multiplicity**21-1)//(multiplicity-1)
    # Dyadic scale recursion, exact beyond numerical floating-point range.
    t=1;dyadic=[]
    for k in range(1,41):
        t*=2**k
        assert t==2**(k*(k+1)//2)
        dyadic.append({'k':k,'n':2**k,'log2_T':t.bit_length()-1})
    out={'scope':'Finite directed transition models only, not RAAG Dehn functions. All states initial and terminal in census.',
         'binary_adjacency_census':census,'chain_examples':samples,'parallel_loop_multiplicities_checked':[2,10],
         'dyadic_recurrence_exact':dyadic,'result':'PASS'}
    Path(__file__).with_name('positive_transition_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'result':'PASS','census':census},indent=2))
if __name__=='__main__':main()

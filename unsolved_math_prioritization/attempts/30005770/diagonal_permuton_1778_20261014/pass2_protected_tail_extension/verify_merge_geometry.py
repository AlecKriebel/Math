#!/usr/bin/env python3
"""Exact finite regression checks, not an asymptotic proof."""
from itertools import combinations,permutations
from math import comb
from pathlib import Path
import json

def std(w):
    rank={x:i+1 for i,x in enumerate(sorted(w))}
    return tuple(rank[x] for x in w)

def avoids(p,q):
    return all(std(tuple(p[i] for i in inds))!=q for inds in combinations(range(len(p)),len(q)))

def residual(p):
    out=[]; low=len(p)+1
    for x in p:
        if x<low: low=x
        else: out.append(x)
    return std(out)

def numerator(p):
    n=len(p)
    return sum(abs(i+x-n-1) for i,x in enumerate(p,1))

def discrepancy_num(P,n,k):
    P=set(P); c=0; best=0
    for j in range(n+1):
        if j in P: c+=1
        best=max(best,abs(n*c-k*j))
    return best

canonical=0; profiles=[]
qs=[q for length in range(2,5) for q in permutations(range(1,length+1)) if q[0]==1]
for n in range(0,8):
    pc=0
    for p in permutations(range(1,n+1)):
        r=residual(p)
        for q in qs:
            qp=(1,)+tuple(x+1 for x in q)
            assert avoids(p,qp)==avoids(r,q),(p,q,r)
            canonical+=1;pc+=1
    profiles.append({'n':n,'canonical_tests':pc})

geometry=0; bounds=[]
for n in range(1,7):
    tested=0
    for k in range(n+1):
        subsets=list(combinations(range(1,n+1),k))
        for P in subsets:
            EP=discrepancy_num(P,n,k)
            Q=[x for x in range(1,n+1) if x not in P]
            for V in subsets:
                EV=discrepancy_num(V,n,k)
                W=sorted((x for x in range(1,n+1) if x not in V),reverse=True)
                for sigma in permutations(range(1,k+1)):
                    p=[0]*n
                    for r,ind in enumerate(P):p[ind-1]=V[sigma[r]-1]
                    for ind,x in zip(Q,W):p[ind-1]=x
                    if k:
                        # Clear denominators from ell_n <=(k/n)ell_k+2(E(P)+E(V))/n+1/n.
                        assert k*numerator(p)<=n*numerator(sigma)+2*k*(EP+EV)+k*n,(p,sigma,P,V)
                    else: assert numerator(p)==0
                    geometry+=1;tested+=1
    bounds.append({'n':n,'all_ambient_merge_tests':tested})

out={'status':'PASS','canonical_deletion_equivalences':canonical,'all_ambient_merge_geometries':geometry,
     'canonical_profiles':profiles,'geometry_profiles':bounds,
     'arithmetic':'exact integers only; all inequality denominators cleared',
     'scope':'Finite regression only. Exponential concentration follows from the analytic counting proof, not these checks.'}
Path(__file__).with_name('MERGE_REGRESSION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

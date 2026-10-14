"""Finite sanity checks only. These are not asymptotic proof evidence."""
from itertools import permutations, combinations
from functools import lru_cache
from collections import Counter
import json
from pathlib import Path


def standardize(p):
    order={v:i+1 for i,v in enumerate(sorted(p))}
    return tuple(order[v] for v in p)

@lru_cache(None)
def avoiders(pat,n):
    m=len(pat)
    return tuple(p for p in permutations(range(1,n+1))
                 if not any(standardize(tuple(p[i] for i in I))==pat
                            for I in combinations(range(n),m)))

@lru_cache(None)
def count(pat,n):
    return len(avoiders(pat,n))

from math import comb
checks=Counter()
for m in range(1,4):
    for alpha in permutations(range(1,m+1)):
        tau=tuple(v+1 for v in alpha)+(1,)
        for n in range(1,7):
            actual=Counter()
            for p in avoiders(tau,n):
                for i,j in enumerate(p,1):
                    r=sum(v>j for v in p[:i-1])
                    actual[i,j,r]+=1
            for (i,j,r),v in actual.items():
                rhs=(comb(i-1,r)*comb(n-i,n-j-r)*comb(n-j,r)*comb(j-1,i-1-r)
                     *count(alpha,r)*count(tau,i-1-r)
                     *count(tau,n-j-r)*count(tau,j-i+r))
                assert v<=rhs, (alpha,n,i,j,r,v,rhs)
                checks['quadrant_count_bounds']+=1
            if alpha[0]<m:
                point=Counter()
                for p in avoiders(tau,n):
                    for i,j in enumerate(p,1): point[i,j]+=1
                for i in range(1,n+1):
                    for j in range(i,n+1):
                        lower=count(tau,i-1)*count(tau,j-i)*count(tau,n-j)
                        assert point[i,j]>=lower
                        checks['upper_point_injection_counts']+=1
                assert point[1,n]==count(tau,n-1)
                checks['extreme_point_exact_counts']+=1
for n in range(1,8):
    for p in permutations(range(1,n+1)):
        q=[sum(v>k for v in p[:k]) for k in range(n+1)]
        assert all(abs(a-b)<=1 for a,b in zip(q,q[1:]))
        assert sum(abs(i-v) for i,v in enumerate(p,1))==2*sum(q)
        checks['cut_lipschitz_and_footrule']+=1
result={'status':'passed','scope':'Finite sanity checks only; no asymptotic conclusion',
        'counts':dict(checks),'alpha_lengths_checked':[1,2,3],
        'avoidance_n_max':6,'cut_identity_n_max':7}
out=Path(__file__).with_name('FINITE_CHECK_RESULTS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

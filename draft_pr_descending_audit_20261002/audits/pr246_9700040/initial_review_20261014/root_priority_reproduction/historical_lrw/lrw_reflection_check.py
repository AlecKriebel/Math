#!/usr/bin/env python3
"""Independent exact check: LRW 2001 no-jump determinant vs joint layer thresholds.
All arithmetic rational. No candidate or sibling audit implementation imported.
"""
from itertools import permutations, product
from fractions import Fraction as F
from bisect import bisect_right
from math import factorial
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone
import json


def compositions(n,k):
    if k==1:
        yield (n,)
    else:
        for d in range(n+1):
            for tail in compositions(n-d,k-1):
                yield (d,)+tail


def permutation_sign(p):
    return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1


def mul(a,b,N):
    c=[F(0)]*(N+1)
    for i,v in enumerate(a):
        for j,w in enumerate(b[:N+1-i]):
            c[i+j]+=v*w
    return c


def l_series(theta,z,N):
    ans=[F(0)]*(N+1)
    for s in range(N+1):
        power=s+max(theta,0)
        if power<=N:
            ans[power]=F(z)**power/F(factorial(s)*factorial(s+abs(theta)))
    return ans


def H_series(z,N):
    m=len(z)
    if not m:
        return [F(1)]+[F(0)]*N
    a=[[l_series(i-j,z[j],N) for j in range(m)] for i in range(m)]
    ans=[F(0)]*(N+1)
    for p in permutations(range(m)):
        v=[F(1)]+[F(0)]*N
        for i,j in enumerate(p):
            v=mul(v,a[i][j],N)
        sign=permutation_sign(p)
        ans=[u+sign*w for u,w in zip(ans,v)]
    return ans


def lis_prefix(p):
    row=[];lens=[0]
    for v in p:
        i=bisect_right(row,v)
        if i==len(row):row.append(v)
        else:row[i]=v
        lens.append(len(row))
    return tuple(lens)


def insert(row,u):
    i=bisect_right(row,u)
    if i<len(row):row[i]=u
    else:row.append(u)


def main():
    N=7
    cases=[(F(1),F(2)),(F(1,2),F(3,2),F(5,2)),
           (F(1),F(2),F(3),F(4)),(F(1,3),F(4,3),F(7,3),F(10,3),F(13,3))]
    trajectories={n:Counter(lis_prefix(p) for p in permutations(range(1,n+1))) for n in range(N+1)}
    receipts=[];pathwise_total=0
    for xs in cases:
        k=len(xs);deltas=tuple(b-a for a,b in zip((F(0),)+xs,xs))
        coeff=[];pathwise=0
        for n in range(N+1):
            val=F(0)
            for ds in compositions(n,k):
                sizes=[];v=0
                for d in ds:v+=d;sizes.append(v)
                accepted=sum(count for lens,count in trajectories[n].items() if all(lens[size]<i for i,size in enumerate(sizes,1)))
                weight=F(1,factorial(n))
                for delta,d in zip(deltas,ds):weight*=delta**d/F(factorial(d))
                val+=accepted*weight
                if n<=5 and k<=4:
                    # One ordered representative in each horizontal strip; all
                    # vertical permutations cover all combinatorial point orders.
                    us=[]
                    for lo,delta,d in zip((F(0),)+xs[:-1],deltas,ds):
                        us.extend(lo+delta*F(j,d+1) for j in range(1,d+1))
                    for p in permutations(range(1,n+1)):
                        event=all(lis_prefix(p)[size]<i for i,size in enumerate(sizes,1))
                        # Rotate each point (u,v) to (x_k-u,1-v): chronological
                        # order then corresponds to decreasing original v ranks.
                        rotated=[xs[-1]-us[j] for j in sorted(range(n),key=lambda j:p[j],reverse=True)]
                        initial=[xs[-1]-xs[k-j-1] if j<k else xs[-1] for j in range(1,k+1)]
                        row=initial[:]
                        for u in rotated:insert(row,u)
                        nojump=row[k-1]==xs[-1]
                        assert event==nojump,(xs,ds,p,row,event)
                        pathwise+=1
            coeff.append(val)
        z=tuple(xs[-1]-xs[i] for i in reversed(range(k-1)))
        det=H_series(z,N)
        assert coeff==det,(xs,coeff,det)
        receipts.append(dict(thresholds=[str(x) for x in xs],reflected_initial=[str(v) for v in z+(xs[-1],)],
                             matched_raw_coefficients=[str(c) for c in coeff],
                             exact_determinant_match_through_degree=N,pathwise_checks=pathwise))
        pathwise_total+=pathwise
    # Boundary/low-index conventions: k=1 uses the empty determinant.
    # Equal queried thresholds give the strongest X_1 > x event, exp(-x).
    # The one-time X_k > x Toeplitz marginal instead has earlier thresholds
    # tending to zero, so all reflected H arguments equal x. Repeated/no
    # effective queries follow by continuity in positive ordered thresholds.
    assert H_series((),N)==[F(1)]+[F(0)]*N
    unrestricted=[F(2)]
    for u in [F(1,2),F(1)]:insert(unrestricted,u)
    finite=[F(2)]
    for u in [F(1,2),F(1)]:
        j=bisect_right(finite,u)
        if j<len(finite):finite[j]=u
    assert unrestricted==[F(1,2),F(1)]
    assert finite==[F(1,2)]
    assert unrestricted[0]==finite[0]
    assert finite[0]!=F(2)
    negative_control=dict(initial=["2"],arrivals=["1/2","1"],
                          unrestricted_piles=[str(x) for x in unrestricted],
                          finite_particles=[str(x) for x in finite],
                          disproves_no_extra_pile_assertion=True,
                          first_prefix_autonomy_and_event_unchanged=True)
    result=dict(utc=datetime.now(timezone.utc).isoformat(),independent_of_campaign_code=True,
                determinant_definition='H_m(z)=det[l_(i-j)(z_j)]_(i,j=1..m)',
                cases=receipts,pathwise_rotation_nojump_checks=pathwise_total,
                empty_determinant_verified=True,negative_control=negative_control,all_checks_passed=True)
    Path(__file__).with_name('LRW_REFLECTION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['utc','pathwise_rotation_nojump_checks','all_checks_passed']}))

if __name__=='__main__':main()

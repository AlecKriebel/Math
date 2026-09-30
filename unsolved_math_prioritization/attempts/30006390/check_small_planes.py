#!/usr/bin/env python3
"""Exact diagnostics on PG(2,2) and PG(2,3), not asymptotic evidence."""
from collections import Counter
from itertools import product
import json
from pathlib import Path

def normalized(v,p):
    a=next(x for x in v if x)
    inv=pow(a,-1,p)
    return tuple(x*inv%p for x in v)

def projective_plane(p):
    points=sorted({normalized(v,p) for v in product(range(p),repeat=3) if any(v)})
    lines=[]
    for a in points:
        lines.append(sum(1<<i for i,x in enumerate(points) if sum(u*v for u,v in zip(a,x))%p==0))
    n=p*p+p+1
    assert len(points)==len(lines)==n
    assert all(L.bit_count()==p+1 for L in lines)
    assert all((L&M).bit_count()==1 for i,L in enumerate(lines) for M in lines[:i])
    point_lines=[sum(1<<j for j,L in enumerate(lines) if L>>i&1) for i in range(n)]
    assert all(x.bit_count()==p+1 for x in point_lines)
    return points,lines,point_lines

out=[]
for q in [2,3]:
    points,lines,point_lines=projective_plane(q)
    n=len(points); full=(1<<n)-1
    hit=[0]*(1<<n)
    blockers=[]
    counts=Counter(); minimal_counts=Counter()
    for S in range(1,1<<n):
        low=S&-S
        hit[S]=hit[S^low]|point_lines[low.bit_length()-1]
        if hit[S]==full:
            counts[S.bit_count()]+=1
            blockers.append(S)
            if all(hit[S^(1<<i)]!=full for i in range(n) if S>>i&1):
                minimal_counts[S.bit_count()]+=1
    # Minimum full blocking subset in each R from subset dynamic programming.
    tau=[n+1]*(1<<n)
    for S in blockers:tau[S]=S.bit_count()
    for i in range(n):
        for S in range(1<<n):
            if S>>i&1:tau[S]=min(tau[S],tau[S^(1<<i)])
    cond=Counter(tau[R] for R in blockers)
    # Check full-line absence is sufficient to exclude every blocker of size q+1.
    for R in blockers:
        if not any(R&L==L for L in lines):assert tau[R]>=q+2
    # Exact probability bounds and common-point dependence of empty sections.
    total=1<<n
    bad_empty=sum(hit[R]!=full for R in range(total))
    bad_full=sum(any(R&L==L for L in lines) for R in range(total))
    assert bad_empty==bad_full  # complementation
    assert bad_empty<=len(lines)*(1<<(n-q-1))
    L,M=lines[0],lines[1]
    simultaneous_empty=sum(not(R&L) and not(R&M) for R in range(total))
    assert simultaneous_empty==(1<<(n-2*q-1))
    result={'q':q,'points':n,'all_point_subsets_checked':total,
            'blocking_set_counts':dict(sorted(counts.items())),
            'minimal_blocking_set_counts':dict(sorted(minimal_counts.items())),
            'minimum_blocker_distribution_when_all_lines_nonempty':dict(sorted(cond.items())),
            'random_sets_with_empty_line':bad_empty,
            'random_sets_with_full_line':bad_full,
            'joint_empty_sections_numerator':simultaneous_empty,'probability_denominator':total}
    out.append(result)
report={'description':'Exact finite diagnostics only; no asymptotic conclusion', 'planes':out,'all_assertions_passed':True}
Path(__file__).with_name('check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

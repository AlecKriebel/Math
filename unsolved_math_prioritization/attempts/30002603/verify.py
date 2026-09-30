#!/usr/bin/env python3
"""Bounded exact diagnostics for the written discrepancy-tail argument."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json

counts=Counter()
def check(test,category):
    assert test,category
    counts[category]+=1

def paths(T,n):
    for steps in product((-1,0,1),repeat=T):
        if sum(steps)!=n: continue
        walk=[0]
        for step in steps: walk.append(walk[-1]+step)
        yield walk

def minimum(b,f,n):
    costs={0:0}
    for sign in b:
        nxt={}
        for x,val in costs.items():
            for y in (x-1,x,x+1):
                candidate=val+sign*f[y]
                if y not in nxt or candidate<nxt[y]:nxt[y]=candidate
        costs=nxt
    return costs[n]

walk_count=0;case_count=0
for T in range(1,7):
    for n in range(1,min(T,3)+1):
        for walk in paths(T,n):
            walk_count+=1
            for seed in range(3):
                f={x:((x*x*(seed+1)+3*x+5*seed)%9)-4 for x in range(-T-1,T+2)}
                d=lambda x:8-f[x]+min(f[x-1],f[x],f[x+1])
                order=[0,n]+sorted(range(1,n),key=lambda x:(d(x),x))
                U=list(range(1,T+1));removed=[]
                for stage,v in enumerate(order):
                    times=[j for j in [0]+U if walk[j]==v]
                    a,z=min(times),max(times)
                    L=[j for j in U if a<j<=z]
                    check(L==list(range(a+1,z+1)),'original_interval')
                    U=[j for j in U if j not in L]
                    compressed=[0]+[walk[j] for j in U]
                    check(compressed[-1]==n and all(abs(y-x)<=1 for x,y in zip(compressed,compressed[1:])),'valid_compressed_path')
                    check(len(U)>=n,'remaining_length')
                    check(all(compressed.count(old)==1 for old in order[:stage+1]),'processed_sites_once')
                    if stage>=1:check(all(0<=x<=n for x in compressed),'confined_after_endpoints')
                    if stage>=2:check(all(d(walk[j])>=d(v) for j in L),'discrepancy_order')
                    removed.append((list(L),list(U)))
                check(len(U)==n,'final_ballistic_length')
                check(sorted(U+[j for L,_ in removed for j in L])==list(range(1,T+1)),'time_partition')
                signs=list(product((-1,1),repeat=T)) if T<=3 else [tuple(1 if ((j+seed2)%p)==0 else -1 for j in range(T)) for seed2 in range(2) for p in (1,2,3)]
                for b in signs:
                    case_count+=1
                    signed=lambda j:b[j-1]*f[walk[j]]
                    original=sum(signed(j) for j in range(1,T+1))
                    es=[];ss=[]
                    for stage,(L,U) in enumerate(removed):
                        Lset=set(L)
                        e=sum(j+1 in Lset and b[j-1]==-1 and b[j]==1 for j in L)
                        s=sum(signed(j) for j in L)
                        es.append(e);ss.append(s)
                        check(s>=-4*len(L),'unweighted_loop_cost')
                        if stage>=2:check(s>=-4*len(L)+e*d(order[stage]),'weighted_loop_cost')
                        compressed_cost=sum(signed(j) for j in U)
                        check(compressed_cost==original-sum(ss),'exact_path_action_removal')
                        upper=original+4*(T-len(U))-sum(es[i]*d(order[i]) for i in range(2,stage+1))
                        check(compressed_cost<=upper,'admissible_path_upper_bound')
                    transitions=sum(b[j]==-1 and b[j+1]==1 for j in range(T-1))
                    check(sum(es)>=transitions-2*(n+1),'transition_boundary_loss')
                    for h in range(2,7):
                        ends={k:max([i for i in range(2,n+1) if d(order[i])*k<=8]+[1]) for k in range(1,h+1)}
                        left=sum(sum(es[i]*d(order[i]) for i in range(2,ends[g]+1)) for g in range(1,h))
                        right=4*sum(es[ends[h]+1:])
                        check(left>=right,'level_summation')
# Independent dynamic-programming minima for a bounded selection of original minimizers.
for T in range(2,8):
    n=min(2,T)
    for seed in range(4):
        f={x:((x*x+3*x*seed+seed)%9)-4 for x in range(-T-1,T+2)}
        b=tuple(1 if (j+seed)%3 else -1 for j in range(T))
        all_paths=list(paths(T,n))
        best=min(all_paths,key=lambda w:sum(b[j-1]*f[w[j]] for j in range(1,T+1)))
        optimum=sum(b[j-1]*f[best[j]] for j in range(1,T+1))
        check(optimum==minimum(b,f,n),'DP_matches_enumeration')
        d=lambda x:8-f[x]+min(f[x-1],f[x],f[x+1])
        order=[0,n]+sorted(range(1,n),key=lambda x:(d(x),x));U=list(range(1,T+1));weighted=0
        for stage,v in enumerate(order):
            times=[j for j in [0]+U if best[j]==v];a,z=min(times),max(times);L=[j for j in U if a<j<=z];Lset=set(L)
            e=sum(j+1 in Lset and b[j-1]==-1 and b[j]==1 for j in L)
            if stage>=2:weighted+=e*d(v)
            U=[j for j in U if j not in L]
            check(minimum(tuple(b[j-1] for j in U),f,n)<=optimum+4*(T-len(U))-weighted,'projected_minimum_upper_bound')
# Exact subset counts, without logarithmic floating-point comparisons.
for N in range(2,12):
    subsets=list(product((0,1),repeat=N))
    for m in range(0,N//2+1):
        q=m+1
        eligible=0
        for bits in subsets:
            intervals=sum(bits[j]==0 and (j==0 or bits[j-1]==1) for j in range(N))
            if intervals<=q:eligible+=1
        check(eligible<=sum(comb(N+1,j) for j in range(q+1))**2,'interval_endpoint_count')
        check((m+2)**2<=(N+1)**2,'concentration_polynomial_factor')
# The sign orientation of the local-tail event and union containment.
for values in product(range(-4,5),repeat=3):
    l,x,r=values;d=8-x+min(l,x,r)
    check(0<=d<=8,'discrepancy_range')
    for h in range(0,9):
        if d<=h:check(x>=4-h and min(l,r)<=-4+h if h<8 else True,'endpoint_tail_containment')
# Uniform spatial density on [-1,1] has exact modified discrepancy tail
# P(d<=h)=h^2/4-h^3/24 for 0<=h<2: integrate (1/2)(u-u^2/4).
# At h=2 the event includes the atom where the central site is the minimum.
for k in range(1,101):
    h=Fraction(2,k);p=Fraction(1) if k==1 else h*h/4-h*h*h/24
    check(Fraction(5,6*k*k)<=p<=Fraction(1,k*k),'uniform_tail_bounds')

result={'status':'PASS','assertions':sum(counts.values()),'categories':dict(counts),'lazy_paths':walk_count,'path_environment_sign_cases':case_count,'artifact_sha256':sha256(Path(__file__).with_name('PARTIAL.md').read_bytes()).hexdigest(),'limitations':'Bounded exact combinatorial and algebraic diagnostics. No simulation establishes the shape limit, the infinite series criterion, or a linear edge. The written argument uses the subadditive ergodic theorem and concentration.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

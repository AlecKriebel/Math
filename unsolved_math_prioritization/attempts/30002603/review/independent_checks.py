#!/usr/bin/env python3
"""Independent exact combinatorial checks, not a probabilistic proof."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from fractions import Fraction as Q
from itertools import product,permutations,combinations_with_replacement
from math import comb
import json
C=Counter()
def ck(cat,cond):
    assert cond,cat
    C[cat]+=1
def dp(signs,f,n):
    state={0:(0,(0,))}
    for b in signs:
        nxt={}
        for x,(cost,path) in state.items():
            for y in (x-1,x,x+1):
                candidate=(cost+b*f[y],path+(y,))
                if y not in nxt or candidate<nxt[y]:nxt[y]=candidate
        state=nxt
    return state[n]
def decompose(w,order):
    U=list(range(1,len(w)));loops=[]
    for v in order:
        ts=[j for j in [0]+U if w[j]==v]
        lo,hi=ts[0],ts[-1]
        removed=[j for j in U if lo<j<=hi]
        ck('original_interval_independent_order',removed==list(range(lo+1,hi+1)))
        U=[j for j in U if not lo<j<=hi]
        path=[0]+[w[j] for j in U]
        ck('compressed_admissibility',path[-1]==w[-1] and all(abs(a-b)<=1 for a,b in zip(path,path[1:])))
        ck('processed_once',all(path.count(x)==1 for x in order[:len(loops)+1]))
        loops.append((removed,list(U)))
    ck('final_ballistic_path',[w[j] for j in U]==list(range(1,w[-1]+1)))
    return loops
# Longer paths than the submitted exhaustive controls, with arbitrary interior order.
for steps in product((-1,0,1),repeat=7):
    n=sum(steps)
    if n not in (2,3,4):continue
    w=[0]
    for step in steps:w.append(w[-1]+step)
    for mid in permutations(range(1,n)):
        loops=decompose(w,[0,n]+list(mid))
        ck('partition',[j for j in sorted([j for L,_ in loops for j in L]+loops[-1][1])]==list(range(1,8)))
# Optimizers are computed independently; only the comparison inequality is tested.
strict=0; cases=0
for T in range(4,13):
    for n in (1,2,3):
        if n>T:continue
        for seed in range(4):
            f={x:(7*x*x*x+(seed+2)*x+seed)%5-2 for x in range(-T-1,T+2)}
            signs=tuple(-1 if (j*j+seed*j+1)%5<2 else 1 for j in range(T))
            best,w=dp(signs,f,n);d=lambda x:4-f[x]+min(f[x-1],f[x],f[x+1])
            order=[0,n]+sorted(range(1,n),key=lambda x:(d(x),-x))
            loops=decompose(w,order);weighted=0;pairs_total=0
            for i,(L,U) in enumerate(loops):
                pairs=sum(1 for j in L if j+1 in L and signs[j-1:j+1]==(-1,1))
                cost=sum(signs[j-1]*f[w[j]] for j in L)
                if i>=2:
                    ck('weighted_loop_lower_bound',cost>=-2*len(L)+pairs*d(order[i]))
                    weighted+=pairs*d(order[i])
                pairs_total+=pairs
                compressed=tuple(signs[j-1] for j in U)
                optimal,_=dp(compressed,f,n)
                retained=sum(signs[j-1]*f[w[j]] for j in U)
                ck('admissible_comparison_only',optimal<=best+2*(T-len(U))-weighted)
                ck('retained_path_vs_minimum',optimal<=retained)
                strict+=optimal<retained
            total=sum(signs[j:j+2]==(-1,1) for j in range(T-1))
            ck('sign_pair_boundary_loss',total-pairs_total<=2*(n+1));cases+=1
# Count deleted intervals directly from bit strings, including m=0.
for N in range(2,11):
    for n in range(1,N//2+1):
        counts=Counter()
        for mask in product((0,1),repeat=N):
            if sum(mask)<n:continue
            runs=sum(mask[j]==0 and (j==0 or mask[j-1]==1) for j in range(N))
            counts[runs]+=1
        for m in range(n+1):
            q=m+1;number=sum(v for k,v in counts.items() if k<=q)
            bound=sum(comb(N+1,j) for j in range(q+1))**2
            ck('interval_entropy_count_including_zero',number<=bound)
            ck('concentration_exact_polynomial_factor',Q((m+2)**2,(N+1)**8)<=Q(1,(N+1)**6))
# Exact finite-level double-counting at equality thresholds and zero discrepancy.
grid=(Q(0),Q(1,4),Q(1,2),Q(2,3),Q(1),Q(4,3),Q(2))
for ds in combinations_with_replacement(grid,3):
    for es in product((0,1,3),repeat=3):
        for h in (2,3,5,8):
            left=sum(sum(e*d for e,d in zip(es,ds) if d<=Q(2,g)) for g in range(1,h))
            right=sum(e for e,d in zip(es,ds) if d>Q(2,h))
            ck('finite_level_summation',left>=right)
# Uniform[-1,1] density: integrate (2q-q^2)/2 exactly, q=v/2.
# The continuous part up to h<2 is h^2/4-h^3/24.
for k in range(2,102):
    h=Q(2,k);integral=h*h/4-h*h*h/24
    ck('uniform_tail_exact',integral==Q(1,k*k)-Q(1,3*k*k*k))
    ck('uniform_tail_order',Q(2,3*k*k)<=integral<=Q(1,k*k))
ck('uniform_discrepancy_atom',Q(2)**2/4-Q(2)**3/24+Q(1,3)==1)
# Endpoint containment on a rational grid, with the self-minimum included.
vals=[Q(j,3) for j in range(-3,4)]
for x,y,z,h in product(vals,vals,vals,(Q(1,6),Q(1,2),Q(1))):
    d=2-x+min(x,y,z)
    ck('endpoint_containment',not(d<=h) or (x>=1-h and (y<=-1+h or z<=-1+h)))
# Time-extension monotonicity for the conditional squeezing step.
for seed in range(4):
    signs=tuple(-1 if (i+seed)%3 else 1 for i in range(13))
    f={x:(x*x+seed*x+3)%5-2 for x in range(-14,15)}
    for n in (1,2,3):
        previous=None
        for T in range(n,13):
            a,_=dp(signs[:T],f,n);now=a-2*T
            if previous is not None:ck('time_extension_monotonicity',now<=previous)
            previous=now
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),'optimizer_cases':cases,
     'strictly_cheaper_compressed_minima_observed':strict,
     'artifact_sha256':sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),
     'scope':'Bounded exact diagnostics only. Shape existence, concentration, diagonal selection and infinite summability are checked in the written independent review.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


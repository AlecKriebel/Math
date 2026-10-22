#!/usr/bin/env python3
"""Exhaustive finite regressions for the exact deletion identity; not an asymptotic proof."""
from itertools import permutations, combinations
from collections import Counter
from math import comb
from pathlib import Path
import json, hashlib, sys
P=Path(__file__).resolve().parent

def require(ok,data):
    if not ok: raise RuntimeError(data)

def avoids1324(pi):
    n=len(pi)
    pre=[n+1]*(n+1); suf=[0]*(n+1)
    for i,x in enumerate(pi): pre[i+1]=min(pre[i],x)
    for i in range(n-1,-1,-1): suf[i]=max(suf[i+1],pi[i])
    return not any(pre[j]<pi[k]<pi[j]<suf[k+1]
                   for j in range(1,n-2) for k in range(j+1,n-1))

def standardize(seq):
    ranks={x:i+1 for i,x in enumerate(sorted(seq))}
    return tuple(ranks[x] for x in seq)

def insert_record(sigma, positions, values):
    n=len(sigma)+len(positions)
    positions=set(positions); values=set(values)
    keep_values=[x for x in range(1,n+1) if x not in values]
    old=iter(keep_values[x-1] for x in sigma)
    new=iter(sorted(values))
    return tuple(next(new) if i in positions else next(old) for i in range(n))

MAX_N=8; ALLOCATION_MAX_N=7
classes={n:[pi for pi in permutations(range(1,n+1)) if avoids1324(pi)] for n in range(MAX_N+1)}
Z=Counter(); B=Counter(); roundtrips=0; empty_records=[]
for n,perms in classes.items():
    for pi in perms:
        for i,j in combinations(range(n),2):
            u,v=pi[i],pi[j]
            if u>=v: continue
            inside=[t for t in range(i+1,j) if u<pi[t]<v]
            vals=[pi[t] for t in inside]
            require(vals==sorted(vals),('rectangle_not_increasing',pi,i,j))
            m=len(inside); p=j-i-1-m; q=v-u-1-m
            Z[n,m,p,q]+=1
            if m==0:
                B[n,p,q]+=1
                if n<=ALLOCATION_MAX_N: empty_records.append((pi,i,j,p,q))
            keep=[pi[t] for t in range(n) if t not in set(inside)]
            sigma=standardize(keep)
            require(sigma[i]==u and sigma[j-m]==v-m,('endpoint_shift',pi,i,j,sigma))
            require(not any(u<sigma[t]<v-m for t in range(i+1,j-m)),('skeleton_not_empty',pi,i,j))
            require(insert_record(sigma,inside,vals)==pi,('roundtrip',pi,i,j,sigma,inside,vals))
            roundtrips+=1
for (n,m,p,q),count in Z.items():
    upper=B[n-m,p,q]*comb(m+p,m)*comb(m+q,m)
    require(count<=upper,('fiber_upper_bound',n,m,p,q,count,upper))

reconstructed=Counter(); candidates=0; rejected=0
for sigma,i,j,p,q in empty_records:
    N=len(sigma);u,v=sigma[i],sigma[j]
    for m in range(ALLOCATION_MAX_N-N+1):
        for positions in combinations(range(i+1,j+m),m):
            for values in combinations(range(u+1,v+m),m):
                output=insert_record(sigma,positions,values)
                candidates+=1
                if avoids1324(output): reconstructed[N+m,m,p,q]+=1
                else: rejected+=1
expected=Counter({key:value for key,value in Z.items() if key[0]<=ALLOCATION_MAX_N})
require(reconstructed==expected,('exact_admissibility_identity',reconstructed-expected,expected-reconstructed))
sigma=(3,1,5,2,4); output=insert_record(sigma,[2],[4])
require(avoids1324(sigma) and output==(3,1,4,6,2,5) and not avoids1324(output),('unsafe_insertion_example',output))
require(11**11>3**24,('exact_entropy_threshold',))
files=['RECTANGLE_DELETION_AND_ENTROPY.md','COMB_RECTANGLE_OBSTRUCTION.md','COARSE_RECTANGLE_DICHOTOMY.md',Path(__file__).name]
result={'status':'passed','scope':'Finite exact regression only; no asymptotic growth or uniform probability inferred',
        'max_permutation_size':MAX_N,'avoidance_counts':{str(n):len(v) for n,v in classes.items()},
        'marked_pair_deletion_roundtrips':roundtrips,'statistic_classes_checked':len(Z),
        'allocation_identity_max_size':ALLOCATION_MAX_N,'allocation_candidates':candidates,
        'allocations_rejected_by_actual_avoidance':rejected,'exact_identity_marked_pairs':sum(reconstructed.values()),
        'unsafe_insertion_example':{'skeleton':sigma,'reconstructed':output},
        'exact_threshold_integers':[11**11,3**24],
        'pins':{name:{'bytes':(P/name).stat().st_size,'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest()} for name in files}}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'CHECK_NORMAL.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

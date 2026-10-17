#!/usr/bin/env python3
"""Finite exact checks of the authored minimum-frontier lemmas.
This is evidence at explicit finite bounds, not an all-n proof.
No optimization-sensitive assert statements are used.
"""
from itertools import permutations, combinations
from collections import defaultdict
from functools import lru_cache
from math import comb
import json, hashlib, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parent

def require(cond, message):
    if not cond:
        raise RuntimeError(message)

def standardize(seq):
    ranks={v:i+1 for i,v in enumerate(sorted(seq))}
    return tuple(ranks[v] for v in seq)

@lru_cache(maxsize=400000)
def patterns(pi, m):
    return frozenset(standardize(tuple(pi[i] for i in inds)) for inds in combinations(range(len(pi)),m))

def contains(pi, alpha):
    return alpha in patterns(pi,len(alpha))

def label(pi, alpha):
    m=len(alpha)
    best=len(pi)+1
    for inds in combinations(range(len(pi)),m):
        if inds[-1]+1 < best and standardize(tuple(pi[i] for i in inds))==alpha:
            best=inds[-1]+1
    return best

def insert(pi,k):
    return tuple(v+1 for v in pi[:k])+(1,)+tuple(v+1 for v in pi[k:])

def delete_low(pi,k):
    return tuple(v-k for v in pi if v>k)

def ballot(L,t):
    numerator=L*comb(L+2*t,t)
    require(numerator%(L+2*t)==0,'ballot integrality')
    return numerator//(L+2*t)

# Formula and recurrence, independently evaluated integer arithmetic.
for L in range(1,41):
    require(ballot(L,0)==1,'ballot initial')
    for t in range(15):
        require(ballot(L,t+1)==sum(ballot(j,t) for j in range(2,L+2)), 'ballot recurrence')

classes_checked=0
parents_checked=0
edges_checked=0
deletions_checked=0
tail_bounds_checked=0
descendants_checked=0
records=[]
all_perms={n:list(permutations(range(1,n+1))) for n in range(8)}
for m in range(1,5):
  for alpha in permutations(range(1,m+1)):
    tau=tuple(v+1 for v in alpha)+(1,)
    Cs={n:[p for p in all_perms[n] if not contains(p,tau)] for n in range(8)}
    Ls={n:{p:label(p,alpha) for p in Cs[n]} for n in range(8)}
    classes_checked+=1
    for n in range(7):
      for p in Cs[n]:
        L=Ls[n][p]
        parents_checked+=1
        actual=[]
        for k in range(n+1):
          ch=insert(p,k)
          valid=ch in Ls[n+1]
          require(valid==(k<L),f'active gaps {alpha} {p} {k}')
          if valid:
            actual.append(Ls[n+1][ch])
            require(delete_low(ch,1)==p,'unique parent')
            require(Ls[n+1][ch]<=L+1,'upper child label')
            require(Ls[n+1][ch]>=k+1,'weak lower child label')
            edges_checked+=1
        require(len(actual)==L,'degree')
        if m>=2:
          require(all(b>=j+1 for j,b in enumerate(sorted(actual),1)), 'Catalan sorted domination')
          require(all(b>=min(L+1,j+m-1) for j,b in enumerate(sorted(actual),1)), 'strong sorted domination')
    # Every low-value deletion and its exact ancestor support and weight.
    for n in range(1,8):
      for k in range(1,min(n,4)+1):
        by_parent=defaultdict(int)
        for p in Cs[n]:
          parent=delete_low(p,k)
          require(parent in Ls[n-k], 'deletion hereditary')
          M=max(p.index(v)+1 for v in range(1,k+1))
          L=Ls[n-k][parent]
          require(M<=L+k-1, f'deletion position bound {alpha} {p} {k}')
          by_parent[parent]+=1
          deletions_checked+=1
        for p,count in by_parent.items():
          L=Ls[n-k][p]
          require(count<=comb(n,k)*len(Cs[k]),'coarse completion bound')
          require(count<=comb(L+k-1,k)*len(Cs[k]),'sharp completion bound')
        for q in range(1,n+2):
          event=sum(max(p.index(v)+1 for v in range(1,k+1))>=q for p in Cs[n])
          badparents=sum(L>=q-k+1 for L in Ls[n-k].values())
          require(event<=comb(n,k)*len(Cs[k])*badparents,'weighted finite small-value tail')
          require(len(Cs[k])*len(Cs[n-k])<=len(Cs[n]), 'sum supermultiplicativity')
          tail_bounds_checked+=1
        if m>=2:
          # Exact depth-k descendant count is computed through unique deletion.
          for p in Cs[n-k]:
            require(by_parent[p]>=ballot(Ls[n-k][p],k), 'Catalan descendants')
            descendants_checked+=1
    if m>=2:
      for n in range(8):
        for t in range(0,8-n):
          for ell in range(1,n+3):
            bad=sum(L>=ell for L in Ls[n].values())
            require(bad*ballot(ell,t)<=len(Cs[n+t]),'exact frontier tail')
            tail_bounds_checked+=1
    records.append({'alpha':''.join(map(str,alpha)), 'tau':''.join(map(str,tau)), 'counts_n0_to_n7':[len(Cs[n]) for n in range(8)]})

# Deterministic nonimplication example, alpha=132, direct-sum copies plus reversal.
for copies in range(1,6):
  for tail in range(0,10):
    p=tuple(3*j+v for j in range(copies) for v in (1,3,2))+tuple(range(3*copies+tail,3*copies,-1))
    require(not contains(p,(2,4,3,1)), 'nonimplication avoids2431')
    require(label(p,(1,3,2))==3,'nonimplication frontier')
    for k in range(1,3*copies+1):
      require(max(p.index(v)+1 for v in range(1,k+1))<=k+2,'nonimplication low ranks')
    inv=sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
    require(inv==copies+tail*(tail-1)//2,'nonimplication inversion exact')

report={
 'status':'PASS',
 'scope':'Finite exact checks only; not an all-n proof or a uniform permuton-limit test.',
 'python_optimization_level':sys.flags.optimize,
 'bounds':{'alpha_lengths':[1,2,3,4], 'class_sizes_n':'0 through 7', 'minimum_insertion_parent_n':'0 through 6', 'deletion_depth_k':'1 through min(n,4)', 'ballot_formula_L':'1 through 40', 'ballot_recurrence_t':'0 through 14'},
 'checks':{'classes':classes_checked,'parents':parents_checked,'valid_edges':edges_checked,'low_value_deletions':deletions_checked,'tail_bounds':tail_bounds_checked,'individual_descendant_counts':descendants_checked},
 'class_counts':records,
 'proof_sha256':hashlib.sha256((ROOT/'ACTIVE_FRONTIER_PROOF.md').read_bytes()).hexdigest(),
 'checker_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
}
print(json.dumps(report,indent=2,sort_keys=True))

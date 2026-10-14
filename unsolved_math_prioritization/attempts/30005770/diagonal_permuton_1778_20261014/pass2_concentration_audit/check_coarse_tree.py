#!/usr/bin/env python3
"""Finite exact regression for an abstract-tree obstruction, not avoidance evidence."""
from collections import defaultdict
from functools import lru_cache
from math import comb
from pathlib import Path
import json,hashlib,sys

def need(x,msg):
    if not x: raise RuntimeError(msg)

def children(typ,L):
    if typ=='B': return [('B',j) for j in range(2,L+2)]
    if L<3: return [('A',L+1)]+[('B',j) for j in range(2,L+1)]
    return [('A',L+1)]*3+[('B',j) for j in range(2,L-1)]

N=100
for typ in ['A','B']:
 for L in range(1,N+1):
    ch=children(typ,L);b=sorted(j for _,j in ch)
    need(len(ch)==L,'degree')
    need(max(b)<=L+1,'upper label')
    need(all(j>=k+1 for k,j in enumerate(b,1)),'sorted Catalan lower bound')

cur={('A',1):(1,0)};counts=[];marks=[]
for depth in range(N+1):
    counts.append(sum(c for c,r in cur.values()))
    marks.append(sum(r for c,r in cur.values()))
    nxt=defaultdict(lambda:[0,0])
    for (typ,L),(count,rsum) in cur.items():
      for child in children(typ,L):
        nxt[child][0]+=count
        if typ=='A':
            nxt[child][1]+=count*(depth+1 if child[0]=='A' else depth)
        else:
            nxt[child][1]+=rsum
    cur=nxt

w=[0]+[comb(2*(n-1),n-1)//n for n in range(1,N+1)]
h=[1]+[0]*N
for n in range(1,N+1):h[n]=3*sum(w[k]*h[n-k] for k in range(1,n+1))
formula=[(1 if n==0 else w[n])+(h[n-2] if n>=2 else 0) for n in range(N+1)]
need(counts==formula,'level GF mismatch')
atoms=[0]*(N+1)
for n in range(1,N+1):
 atoms[n]=counts[n]-sum(atoms[k]*counts[n-k] for k in range(1,n))
 need(atoms[n]>=0,'negative renewal atom coefficient')
for p in range(N+1):
 for q in range(N+1-p):need(counts[p+q]>=counts[p]*counts[q],'supermultiplicativity finite check')

@lru_cache(None)
def desc(typ,L,t):
 if t==0:return 1
 return sum(desc(k,j,t-1) for k,j in children(typ,L))
need(desc('A',3,3)==51,'A3 descendants')
need(comb(5,3)*counts[3]==50,'permutation upper bound comparison')
report={'result':'PASS','scope':'Finite exact checks on an abstract rooted tree; no evidence for a target avoidance-class limit.','optimization_level':sys.flags.optimize,'level_max':N,'level_counts_n0_to_n15':counts[:16],'marked_spine_ratios':{str(n):{'E_R':marks[n]/counts[n],'E_R_over_n':marks[n]/(n*counts[n])} for n in [20,40,60,80,100]},'avoidance_specific_completion_upper_bound':{'actual_D3_A3':51,'putative_upper_bound':50,'verdict':'FAILS in the abstract model, intentionally outside the accepted countermodel scope'},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(report,indent=2))

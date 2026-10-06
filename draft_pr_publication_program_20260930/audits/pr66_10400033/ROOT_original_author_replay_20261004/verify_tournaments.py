#!/usr/bin/env python3
"""Exact bounded checks of the oriented-graph completion proof.
All oriented chord diagrams with up to four arrows, every sign assignment,
and every tournament with up to five vertices are included.
"""
from fractions import Fraction as F
from itertools import combinations,product
from math import comb
from collections import Counter
import json
from verify_jones import canon,P,T,pv
checks=Counter()
def check(x,k):
 assert x,k
 checks[k]+=1
def matches(items):
 if not items:
  yield ()
  return
 a=items[0]
 for i in range(1,len(items)):
  b=items[i]
  for rest in matches(items[1:i]+items[i+1:]):
   yield ((a,b),)+rest
def arc(a,b,t,m):return 0<(t-a)%m<(b-a)%m
def graph(arrows):
 n=len(arrows);m=2*n
 g=[[0]*n for _ in range(n)]
 for i,j in combinations(range(n),2):
  a,b=arrows[i];c,e=arrows[j]
  if arc(a,b,c,m)!=arc(a,b,e,m):
   if arc(a,b,c,m):g[i][j]=1;g[j][i]=-1
   else:g[i][j]=-1;g[j][i]=1
   check((g[i][j]==1)==(not arc(c,e,a,m)),'antisymmetry')
 return g
def cycle(g,S):
 return all(sum(g[i][j]==1 for j in S if j!=i)==1 for i in S)
def local_expectation(g,S):
 pairs=list(combinations(S,2))
 missing=[(i,j) for i,j in pairs if g[i][j]==0]
 count=0
 for bits in product([-1,1],repeat=len(missing)):
  h=[row[:] for row in g]
  for (i,j),b in zip(missing,bits):h[i][j]=b;h[j][i]=-b
  count+=cycle(h,S)
 return F(count,2**len(missing))
def bound(n):return F(n*(n*n-1),24) if n%2 else F(n*(n*n-4),24)
diagram_count=0
for n in range(1,5):
 for matching in matches(tuple(range(2*n))):
  for bits in product([0,1],repeat=n):
   arrows=[pair if bit else tuple(reversed(pair)) for pair,bit in zip(matching,bits)]
   g=graph(arrows);unsigned=F(0);expected=F(0)
   for S in combinations(range(n),3):
    ends=sorted(p for i in S for p in arrows[i]);order={p:i for i,p in enumerate(ends)}
    sig=canon([(order[arrows[i][0]],order[arrows[i][1]]) for i in S])
    c=F(1,2) if sig==P else F(1) if sig==T else F(0)
    e=local_expectation(g,S)
    check(c<=e,'pointwise_domination')
    if sig==P:check(e==F(1,2),'P_is_directed_path')
    if sig==T:check(e==1,'T_is_directed_cycle')
    unsigned+=c;expected+=e
   check(unsigned<=expected<=bound(n),'formal_unsigned_bound')
   for signs in product([-1,1],repeat=n):
    signed,_=pv(arrows,signs)
    check(abs(signed)<=unsigned,'arbitrary_sign_domination')
   diagram_count+=1
# Every tournament up to five vertices, with no chord representation assumed.
tournament_count=0
for n in range(1,6):
 pairs=list(combinations(range(n),2))
 for bits in product([-1,1],repeat=len(pairs)):
  g=[[0]*n for _ in range(n)]
  for (i,j),b in zip(pairs,bits):g[i][j]=b;g[j][i]=-b
  C=sum(cycle(g,S) for S in combinations(range(n),3))
  degrees=[sum(x==1 for x in row) for row in g]
  check(C==comb(n,3)-sum(comb(k,2) for k in degrees),'tournament_degree_identity')
  check(C<=bound(n),'tournament_extremal_bound')
  tournament_count+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(checks),
                  'oriented_chord_diagrams':diagram_count,'tournaments':tournament_count},indent=2))

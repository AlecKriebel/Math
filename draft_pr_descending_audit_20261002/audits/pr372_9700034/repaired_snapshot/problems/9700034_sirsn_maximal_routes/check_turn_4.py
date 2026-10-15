#!/usr/bin/env python3
from itertools import product
from collections import deque
from fractions import Fraction as F
import json
checks=trees=configs=arcs=0
def tree(seq,n):
 deg=[1]*n
 for x in seq:deg[x]+=1
 es=[]
 for x in seq:
  a=next(i for i in range(n) if deg[i]==1);es.append((a,x));deg[a]-=1;deg[x]-=1
 a,b=[i for i in range(n) if deg[i]==1];es.append((a,b));return es
def path(adj,a,b):
 parent={a:None};q=deque([a])
 while b not in parent:
  u=q.popleft()
  for v in adj[u]:
   if v not in parent:parent[v]=u;q.append(v)
 out=[b]
 while out[-1]!=a:out.append(parent[out[-1]])
 return out[::-1]
for n in range(2,7):
 for seq in product(range(n),repeat=n-2):
  es=tree(seq,n);adj=[[] for _ in range(n)]
  for a,b in es:adj[a].append(b);adj[b].append(a)
  paths={v:path(adj,0,v) for v in range(1,n)};trees+=1
  for bits in product([0,1],repeat=n-1):
   outside=(0,)+bits;C={tuple(sorted((a,b))) for a,b in es if outside[a]!=outside[b]};known={};configs+=1
   for v,P in paths.items():
    if outside[v]:continue
    j=0
    while j<len(P)-1:
     if not outside[P[j]] and outside[P[j+1]]:
      start=j;j+=1
      while outside[P[j]]:j+=1
      e1=tuple(sorted((P[start],P[start+1])));e2=tuple(sorted((P[j-1],P[j])));pair=tuple(sorted((e1,e2)))
      assert e1!=e2 and e1 in C and e2 in C;checks+=1
      arc=tuple(P[start:j+1]);canonical=min(arc,arc[::-1])
      if pair in known:assert known[pair]==canonical;checks+=1
      known[pair]=canonical;arcs+=1
     else:j+=1
   assert len(known)<=len(C)*(len(C)-1)//2;checks+=1
for j in range(100):
 area=F(1,4**j)-F(1,4**(j+1))
 intensity=2**(j+1)
 assert area*intensity==F(3,2)*F(1,2**j);checks+=1
for n in range(100):
 assert sum(F(3,2)*F(1,2**j) for j in range(n+1))==3*(1-F(1,2**(n+1)));checks+=1
 assert sum(F(1,2**j) for j in range(n+1))==2-F(1,2**n);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'labeled_trees':trees,'inside_outside_configurations':configs,'recorded_exterior_arcs':arcs,'scope':'Finite compatible rooted-tree arc uniqueness and exact dyadic localization constants. No SIRSN simulation or exterior moment bound.'},indent=2,sort_keys=True))

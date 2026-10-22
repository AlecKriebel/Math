#!/usr/bin/env python3
"""Exact Laplacian/maximum-principle controls for the general network obstruction."""
from fractions import Fraction
from itertools import combinations,product
from math import isqrt
import json
checks=0;tested=0;balanced=0;proper_balanced=0
def ok(x):
 global checks
 assert x
 checks+=1
def connected(n,E):
 seen={0}
 while True:
  new=seen|{u for u,v in E if v in seen}|{v for u,v in E if u in seen}
  if new==seen:return len(seen)==n
  seen=new
def inverse_and_tree(n,E):
 L=[[0]*n for _ in range(n)]
 for u,v in E:L[u][u]+=1;L[v][v]+=1;L[u][v]-=1;L[v][u]-=1
 d=n-1;A=[[Fraction(L[i][j]) for j in range(d)]+[Fraction(i==j) for j in range(d)] for i in range(d)];z=Fraction(1)
 for k in range(d):
  j=next(j for j in range(k,d) if A[j][k])
  if j!=k:A[k],A[j]=A[j],A[k];z=-z
  p=A[k][k];z*=p;A[k]=[x/p for x in A[k]]
  for j in range(d):
   if j!=k:
    q=A[j][k];A[j]=[x-q*y for x,y in zip(A[j],A[k])]
 G=[r[d:]+[Fraction(0)] for r in A]+[[Fraction(0)]*n]
 assert z.denominator==1
 return int(z),G
def squarefree(g):return all(g%(p*p) for p in range(2,isqrt(g)+1))
def terminal_proper(n,E,s,t):
 adj=[[] for _ in range(n)]
 for k,(u,v) in enumerate(E):adj[u].append((v,k));adj[v].append((u,k))
 used=set()
 def visit(v,seen,path):
  if v==t:used.update(path);return
  for w,k in adj[v]:
   if w not in seen:visit(w,seen|{w},path+[k])
 visit(s,{s},[])
 return len(used)==len(E)
def audit(n,E):
 global tested,balanced,proper_balanced
 if not connected(n,E):return
 tested+=1;g,G=inverse_and_tree(n,E)
 if not squarefree(g):return
 for s,t in combinations(range(n),2):
  R=G[s][s]+G[t][t]-2*G[s][t]
  if R!=1:continue
  balanced+=1
  h=[G[i][s]-G[i][t]-G[t][s]+G[t][t] for i in range(n)]
  ok(all(x.denominator==1 for x in h));ok(set(h)<={0,1});ok(h[s]==1 and h[t]==0)
  cross=[j for j,(u,v) in enumerate(E) if h[u]!=h[v]]
  ok(len(cross)==1);ok(set(E[cross[0]])=={s,t})
  ok(not connected(n,E[:cross[0]]+E[cross[0]+1:]))
  proper=terminal_proper(n,E,s,t)
  if proper:proper_balanced+=1;ok(n==2 and len(E)==1 and g==1)
for n in range(2,6):
 allE=list(combinations(range(n),2))
 for mask in range(1,1<<len(allE)):
  audit(n,[e for j,e in enumerate(allE) if mask>>j&1])
allE=list(combinations(range(4),2))
for weights in product(range(3),repeat=6):audit(4,[e for e,w in zip(allE,weights) for _ in range(w)])
# Sharp witness: a prime cycle attached at a terminal plus a unit bridge.
for p in [3,5,7,11,13,17,19,23,29,31]:
 E=[(i,(i+1)%p) for i in range(p)]+[(0,p)]
 g,G=inverse_and_tree(p+1,E);R=G[0][0]
 ok(g==p and R==1);ok(not terminal_proper(p+1,E,0,p));ok(not connected(p+1,E[:-1]))
print(json.dumps(dict(status='PASS',assertions=checks,connected_graph_instances=tested,balanced_squarefree_terminal_pairs=balanced,terminal_proper_balanced_pairs=proper_balanced,exhaustive_simple_vertex_bound=5,multigraph_vertex_count=4,multigraph_multiplicity_bound=2,attached_cycle_witnesses=10,scope='finite exact controls for the proved all-network obstruction; no knot nonexistence claim'),indent=2,sort_keys=True))

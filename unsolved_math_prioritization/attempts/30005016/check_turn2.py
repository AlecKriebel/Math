#!/usr/bin/env python3
"""Exact finite partition-poset certificate, not a local-cohomology proof checker."""
from itertools import combinations
from fractions import Fraction as F
import json

def parts(n):
 if n==0:yield ();return
 for p in parts(n-1):
  yield p+((n-1,),)
  for j in range(len(p)):
   yield p[:j]+(p[j]+(n-1,),)+p[j+1:]
def refines(a,b):return all(any(set(x)<=set(y) for y in b) for x in a)
def rank(a):
 a=[[F(x) for x in r] for r in a];i=0
 for j in range(len(a[0]) if a else 0):
  k=next((k for k in range(i,len(a)) if a[k][j]),None)
  if k is None:continue
  a[k],a[i]=a[i],a[k];v=a[i][j];a[i]=[x/v for x in a[i]]
  for k in range(len(a)):
   if k!=i:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
  i+=1
 return i
P=list(parts(4));assert len(P)==15
V=[p for p in P if len(p) in (2,3)]
E=[(i,j) for i in range(len(V)) for j in range(i+1,len(V)) if refines(V[i],V[j]) or refines(V[j],V[i])]
assert len(V)==13 and len(E)==18
M=[[int(v==j)-int(v==i) for i,j in E] for v in range(len(V))]
r=rank(M);assert r==12
assert len(E)-r==6
counts={}
for p in V:
 typ='+'.join(map(str,sorted(map(len,p),reverse=True)));counts[typ]=counts.get(typ,0)+1
assert counts=={'2+1+1':6,'2+2':3,'3+1':4}
for a,b in combinations([p for p in V if len(p)==3],2):
 assert any(refines(a,c) and refines(b,c) for c in V if len(c)==2)
print(json.dumps({'partitions':P,'interval_vertices':V,'interval_edges':E,'type_counts':counts,'boundary_rank':r,'H0_dimension':len(V)-r,'H1_dimension':len(E)-r,'H2_dimension':0,'checks':20,'scope':'Finite incidence and rational homology check; the primary arrangement theorem and Nullstellensatz step require independent mathematical review.'},indent=2,sort_keys=True))

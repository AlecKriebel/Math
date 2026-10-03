#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import json
N=0;branches={}
def ck(v):
 global N
 assert v;N+=1
def norm(v):
 a=next(x for x in v if x);return tuple(F(x,a) for x in v)
def cross(a,b):return norm((a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sing(A):return {cross(a,b) for a,b in combinations(A,2)}
P=(F(0),F(1),F(0)) # common point of vertical affine lines
cases=0
pool=[norm((a,b,c)) for a,b,c in [(1,1,0),(1,-1,0),(2,1,-1),(1,2,-3),(1,0,-7),(0,1,-6),(2,-1,2)]]
for a,b in [(2,2),(2,3),(3,2),(3,3),(4,2),(2,4)]:
 base={norm((1,0,-i)) for i in range(a)}|{norm((0,1,-j)) for j in range(b)}|{norm((0,0,1))}
 for added in [()]+[(x,) for x in pool]+list(combinations(pool,2)):
  A=base|set(added);Z=sing(A);pencil={L for L in A if dot(L,P)==0};m=len(pencil)
  new={L for L in A-base if dot(L,P)!=0};t=len(new)
  ka=max(sum(dot(L,p)==0 for p in Z) for L in A)
  W={p for p in Z if all(dot(L,p)!=0 for L in pencil)}
  ck(ka>=m);ck(all(any(dot(L,p)==0 for L in new) for p in W))
  if not W:cover=set(pencil);key='pencil'
  elif ka>=m+t:cover=pencil|new;key='pencil_plus_added'
  else:
   ck(t==2 and len(W)<=2 and ka>=m+1)
   if len(W)==2:H=cross(*tuple(W))
   else:H=next(L for L in new if dot(L,next(iter(W)))==0)
   cover=pencil|{H};key='auxiliary_join'
  branches[key]=branches.get(key,0)+1
  ck(len(cover)<=ka);ck(all(any(dot(L,p)==0 for L in cover) for p in Z))
  support=cover|A;k0=max(sum(dot(L,p)==0 for p in Z) for L in support)
  all_lines={cross(p,q) for p,q in combinations(Z,2)}
  for L in all_lines:
   hits=sum(dot(L,p)==0 for p in Z)
   ck(hits<=k0)
   if L not in cover:ck(hits<=len(cover))
  cases+=1
print(json.dumps({'status':'PASS','assertions':N,'rational_arrangements':cases,'certificate_cases':branches,'scope':'Finite exact incidence controls for the all-size two-line-extension proof; no general conjecture resolution.'},indent=2,sort_keys=True))

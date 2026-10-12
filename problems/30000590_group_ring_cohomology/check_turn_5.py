#!/usr/bin/env python3
"""Finite exact controls for the free-group height-kernel argument."""
from itertools import product
from collections import Counter
import json
checks=conjugacies=decompositions=grids=0
def red(w):
 r=[]
 for a in w:
  if r and r[-1]==-a:r.pop()
  else:r.append(a)
 return tuple(r)
def mul(a,b):return red(a+b)
def inv(a):return tuple(-x for x in a[::-1])
def pw(a,n):
 if n<0:return pw(inv(a),-n)
 z=()
 for _ in range(n):z=mul(z,a)
 return z
def gm(a,b):return (mul(a[0],b[0]),mul(a[1],b[1]))
def gi(a):return (inv(a[0]),inv(a[1]))
def gp(a,n):return (pw(a[0],n),pw(a[1],n))
def ht(a):return sum(1 if x>0 else -1 for x in a)
def gen(i):return mul(mul(pw((1,),i),(2,)),pw((1,),-i-1))
t=((1,),(-1,));one=((),())
for i in range(-100,101):
 u=(gen(i),());v=((),gen(i))
 assert gm(gm(t,u),gi(t))==(gen(i+1),());checks+=1
 assert gm(gm(t,v),gi(t))==((),gen(i-1));checks+=1
 assert ht(gen(i))==0;checks+=1;conjugacies+=2
 assert gm(u,v)==gm(v,u);checks+=1
words={()}
for n in range(1,6):words|={red(x) for x in product((-2,-1,1,2),repeat=n)}
words=sorted(words)
byh={}
for w in words:byh.setdefault(ht(w),[]).append(w)
for s,ws in byh.items():
 for w in ws:
  for z in byh.get(-s,[]):
   k=(mul(w,pw((1,),-s)),mul(z,pw((1,),s)))
   assert ht(k[0])==ht(k[1])==0;checks+=1
   assert gm(k,gp(t,s))==(w,z);checks+=1;decompositions+=1
# Finite index rectangles: adjacency orbits have fixed i+j, one path each.
for n in range(1,51):
 pts=list(product(range(-n,n+1),repeat=2));parent={x:x for x in pts}
 def find(x):
  while parent[x]!=x:
   parent[x]=parent[parent[x]];x=parent[x]
  return x
 edges=0
 for i,j in pts:
  y=(i+1,j-1)
  if y in parent:
   a,b=find((i,j)),find(y)
   assert a!=b;checks+=1
   parent[a]=b;edges+=1
 groups={}
 for x in pts:groups.setdefault(find(x),[]).append(x)
 assert len(groups)==4*n+1;checks+=1
 assert edges==len(pts)-len(groups);checks+=1
 for vs in groups.values():
  assert len({i+j for i,j in vs})==1;checks+=1
 assert {sum(vs[0]) for vs in groups.values()}==set(range(-2*n,2*n+1));checks+=1;grids+=1
# Right augmentation identity, in the noncommutative integral group ring.
def add(*cs):
 out=Counter()
 for c in cs:
  for k,v in c.items():out[k]+=v
 return {k:v for k,v in out.items() if v}
def shift(c,h):return {mul(k,h):v for k,v in c.items()}
small=[w for w in words if len(w)<=3]
for g,h in product(small,repeat=2):
 lhs=add({mul(g,h):1},{():-1})
 rhs=add(shift(add({g:1},{():-1}),h),add({h:1},{():-1}))
 assert lhs==rhs;checks+=1
print(json.dumps({'assertions':checks,'conjugacy_identities':conjugacies,'height_kernel_decompositions':decompositions,'finite_orbit_rectangles':grids,'scope':'Finite exact controls; infinite-rank homology and non-finite-generation proofs are in TURN_5.md.'},indent=2))

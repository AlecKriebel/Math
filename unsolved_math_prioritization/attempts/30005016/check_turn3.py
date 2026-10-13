#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json
# Independently included determinant to keep this checker standalone.
def det(a):
 a=[[F(z) for z in row] for row in a];out=F(1)
 for j in range(len(a)):
  i=next((i for i in range(j,len(a)) if a[i][j]),None)
  if i is None:return F(0)
  if i!=j:a[i],a[j]=a[j],a[i];out=-out
  v=a[j][j];out*=v
  for i in range(j+1,len(a)):
   w=a[i][j]/v
   for k in range(j+1,len(a)):a[i][k]-=w*a[j][k]
 return out

def witness(U,V,W):
 U,V,W=map(F,(U,V,W));assert (U,V,W)!=(0,0,0)
 if V:
  c=next(F(c) for c in range(1,5) if c!=U/V and (not W or c!=V/W))
  a=1-c*W/V;b=c-U/V
  return [(0,0),(0,a),(b,0),(c,1)]
 if U and W:
  r=next(F(r) for r in range(1,4) if r*r!=U)
  t=next(F(t) for t in range(1,4) if t*t!=-W)
  return [(r,0),(U/r,0),(0,t),(0,-W/t)]
 p=[(0,0),(1,0),(2,0),(0,1)]
 return p if U else [(y,x) for x,y in p]

def Ds(p):return [det([[1,x,y,f(x,y)] for x,y in p]) for f in (lambda x,y:x*x,lambda x,y:x*y,lambda x,y:y*y)]
def kernel(a,b):
 c=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
 if any(c):return c
 v=a if any(a) else b
 if not any(v):return [1,0,0]
 i=next(i for i in range(3) if v[i]);j=(i+1)%3
 c=[0,0,0];c[i]=-v[j];c[j]=v[i];return c
n=0
for v in product(range(-3,4),repeat=3):
 if not any(v):continue
 p=witness(*v);d=Ds(p);assert len(set(p))==4 and len({x for x,y in p})<4 and len({y for x,y in p})<4;n+=1
 assert any(d) and all(d[i]*v[j]==d[j]*v[i] for i in range(3) for j in range(3));n+=1
coeff=list(product(range(-1,2),repeat=3))
for a,b in product(coeff,repeat=2):
 v=kernel(a,b);p=witness(*v);d=Ds(p)
 assert sum(a[i]*d[i] for i in range(3))==sum(b[i]*d[i] for i in range(3))==0;n+=1
 assert det([[1,x,x*x,x**3] for x,y in p])==det([[1,y,y*y,y**3] for x,y in p])==0;n+=1
print(json.dumps({'assertions':n,'nonzero_directions':342,'quadratic_pairs':729,'status':'all exact finite controls passed','scope':'Tests support the symbolic construction; they do not prove an unrestricted minimum.'},indent=2,sort_keys=True))

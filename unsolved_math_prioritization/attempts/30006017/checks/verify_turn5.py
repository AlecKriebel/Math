#!/usr/bin/env python3
"""Exact geometry and polynomial genericity controls for the area-continuity construction."""
from fractions import Fraction as Q
from itertools import product
import json
count=0
def ck(v):
 global count
 assert v
 count+=1

def det(x,y):return x[0]*y[1]-x[1]*y[0]
def sub(x,y):return(x[0]-y[0],x[1]-y[1])
q=[(Q(1),Q(1)),(Q(-1),Q(1)),(Q(-1),Q(-1)),(Q(1),Q(-1))]
for N in range(1,101):
 for a in (Q(1,2),Q(1,3),Q(2,5),Q(3,4)):
  outer=[q[j%4] for j in range(4*N+1)]
  inner=[(a*q[j%4][0],a*q[j%4][1]) for j in range(4*N,-1,-1)]
  path=outer+inner+[outer[0]]
  sides=[sub(path[j+1],path[j]) for j in range(len(path)-1)]
  ck(len(sides)==8*N+2)
  ck(tuple(sum(v[d] for v in sides) for d in range(2))==(0,0))
  area=sum(det(path[j],path[j+1]) for j in range(len(path)-1))/2
  energy=sum(x*x+y*y for x,y in sides)
  ck(area==4*N*(1-a*a))
  ck(energy==16*N*(1+a*a)+4*(1-a)**2)
  xx=sum(x*x for x,y in sides); yy=sum(y*y for x,y in sides);xy=sum(x*y for x,y in sides)
  ck(xx==yy==8*N*(1+a*a)+2*(1-a)**2)
  ck(xy==2*(1-a)**2)
  r2=2/energy
  ck(r2*xx==r2*yy==1)
  ck(r2*area==8*N*(1-a*a)/(16*N*(1+a*a)+4*(1-a)**2))
  for j in range(4):
   A=q[j];B=q[(j+1)%4];C=(a*B[0],a*B[1]);D=(a*A[0],a*A[1])
   ck(det(sub(B,A),sub(C,A))==2*(1-a)>0)
   ck(det(sub(C,A),sub(D,A))==2*a*(1-a)>0)
# Every forbidden subset-determinant polynomial has an explicit nonzero zero-sum witness.
for n in range(3,9):
 for assignment in product(range(3),repeat=n):
  if set(assignment)!={0,1,2}:continue
  i=assignment.index(1);j=assignment.index(2);k=assignment.index(0)
  vectors=[(0,0) for _ in range(n)];vectors[i]=(1,0);vectors[j]=(0,1);vectors[k]=(-1,-1)
  u=tuple(sum(vectors[t][d] for t in range(n) if assignment[t]==1) for d in range(2))
  v=tuple(sum(vectors[t][d] for t in range(n) if assignment[t]==2) for d in range(2))
  ck(det(u,v)==1)
  ck(tuple(sum(x[d] for x in vectors) for d in range(2))==(0,0))
ck((1-Q(1,2)**2)/(2*(1+Q(1,2)**2))==Q(3,10))
ck((1-Q(1,3)**2)/(2*(1+Q(1,3)**2))==Q(2,5))
print(json.dumps({'status':'PASS','assertions':count,'coverage':['annular-cover boundary count and closure','intrinsic shoelace area and quadratic energy','covariance normalization','positive triangulation orientations','nonzero polynomial witnesses for all small genericity constraints','distinct limiting areas'],'scope':'Exact deterministic disks and genericity witnesses; no claim about the source conditional-uniform Gaussian sampling law.'},indent=2,sort_keys=True))

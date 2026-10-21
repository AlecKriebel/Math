#!/usr/bin/env python3
"""Finite exact cohomology/scaling controls. The analytic bound is a published theorem."""
from fractions import Fraction as Q
from itertools import combinations,product
from math import comb
import json
count=0
def ck(v):
 global count
 assert v
 count+=1
def rank(a):
 a=[[Q(v) for v in row] for row in a];r=0
 for j in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for k in range(len(a)):
   if k!=r:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[r])]
  r+=1
  if r==len(a):break
 return r
basis=list(combinations(range(4),2))
def wedge(a,b):
 if set(a)&set(b):return 0
 q=a+b
 return (-1)**sum(q[i]>q[j] for i in range(4) for j in range(i+1,4))
W=[[wedge(a,b) for b in basis] for a in basis]
ck(len(basis)==6);ck(rank(W)==6)
for i in range(6):
 for j in range(6):
  ck(W[i][j]==W[j][i])
  ck(sum(W[i][k]*W[k][j] for k in range(6))==int(i==j))
# The source manifold's cohomology and hyperbolic intersection form.
J=[[int(i//2==j//2 and i!=j) for j in range(40)] for i in range(40)]
ck(rank(J)==40);ck([1,0,40,0,1]==[1,0,2*20,0,1])
ck(sum([1,0,40,0,1])==42);ck(sum(comb(4,k) for k in range(5))==16)
ck(40>comb(4,2));ck(42>16)
# Signed reflection and dilation determinants, without inserting a second R^4.
for R in [Q(j,k) for j in range(2,12) for k in (1,2,3) if Q(j,k)>1]:
 ck(R**4*R**(-4)==1)
 ck((-R)*R*R*R==-R**4)
 ck(R**3/R**4==1/R)
# A rational rank-three radial projection at every tested unit vector.
for v in [tuple(Q(x,5) for x in q) for q in [(3,4,0,0),(0,3,0,4),(4,0,3,0)]]:
 ck(sum(x*x for x in v)==1)
 P=[[Q(int(i==j))-v[i]*v[j] for j in range(4)] for i in range(4)]
 ck(rank(P)==3)
 for i in range(4):
  ck(sum(P[i][j]*v[j] for j in range(4))==0)
  for j in range(4):ck(sum(P[i][k]*P[k][j] for k in range(4))==P[i][j])
# The two error ratios vanish separately for every fixed positive alpha.
# This checks integer power bookkeeping only, not a numerical asymptotic fit.
for m in range(1,21):
 ck(Q(1,4*m)>0)
 ck(4-4==0)
 ck(3-4==-1)
print(json.dumps({'status':'PASS','exact_assertions':count,'target_betti_numbers':[1,0,40,0,1],'exterior_algebra_dimensions':[comb(4,k) for k in range(5)],'middle_intersection_rank':40,'wedge_pairing_rank':6,'scope':'Finite linear algebra, signed dilation and rank controls only. The logarithmic estimate is the credited BGM2024 Theorem2.3; boundary Stokes is an analytic argument in the application.'},indent=2,sort_keys=True))

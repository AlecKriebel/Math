#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json,math
checks=edges=0
for n in range(8):
 h=F(1,2**n);N=2**(n+1)
 assert (N+1)**2<=9*4**n;checks+=1
 for i,j in product(range(N+1),repeat=2):
  x,y=-1+i*h,-1+j*h
  if n:
   px,py=-1+(i//2)*(2*h),-1+(j//2)*(2*h)
   assert (x-px)**2+(y-py)**2<=2*h*h;checks+=1
   assert (px+1)/(2*h)==i//2 and (py+1)/(2*h)==j//2;checks+=1
  else:
   assert x*x+y*y<=2;checks+=1
  edges+=1
for p in [F(3),F(4),F(5),F(8)]:
 for an in range(1,13):
  alpha=F(an,4)
  if alpha<=2/p:continue
  exponent=alpha-2/p
  assert exponent>0;checks+=1
  for n in range(30):
   assert -n*alpha+n*F(2)/p==-n*exponent;checks+=1
for r in [F(1,2),F(1,3),F(3,4),F(7,8)]:
 for n in range(50):
  assert sum(r**k for k in range(n+1))==(1-r**(n+1))/(1-r);checks+=1
  assert sum(r**k for k in range(n+1))<=1/(1-r);checks+=1
# Exact finite controls for the radial energy after s=log(1/r):
# integral_1^R s^(-2) ds=1-1/R, with total limit one.
for R in range(2,2001):
 assert F(1)-F(1,R)>0;checks+=1
 assert (F(1)-F(1,R))+F(1,R)==1;checks+=1
# Independent Bernoulli hits of every fixed positive-area set:
for a in [F(1,2),F(1,5),F(1,100),F(1,1000)]:
 for n in range(1,101):
  assert (1-a)**n<=(1-a)**(n-1);checks+=1
  assert 1-(1-a)**n<=n*a;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'grid_parent_edges':edges,'max_grid_level':7,'scope':'Exact dyadic parent geometry, chaining exponents, geometric sums, radial-energy identity and finite sampling controls. No SIRSN counterexample or continuum simulation.'},indent=2,sort_keys=True))

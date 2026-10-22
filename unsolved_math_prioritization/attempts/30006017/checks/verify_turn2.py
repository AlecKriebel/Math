#!/usr/bin/env python3
"""Rational interval covariance and laminar-measure bounds; no Brownian simulation."""
from fractions import Fraction as Q
import json
count=0
def check(v):
 global count
 assert v
 count+=1

def cov(i,j):
 return max(Q(0),min(i[1],j[1])-max(i[0],j[0]))-(i[1]-i[0])*(j[1]-j[0])
intervals=[]
for depth in range(7):
 for k in range(2**depth):intervals.append((Q(k,2**depth),Q(k+1,2**depth),depth))
for i in intervals:
 for j in intervals:
  s=i[1]-i[0];t=j[1]-j[0];c=cov(i,j)
  nested=(i[0]<=j[0] and j[1]<=i[1]) or (j[0]<=i[0] and i[1]<=j[1])
  if nested:check(abs(c)<=min(s,t))
  else:check(c==-s*t)
  check(c*c<=s*(1-s)*t*(1-t))
# Finite laminar measures, with explicit ancestor-chain height bound.
for base in (2,3,5):
 weights=[Q(1,base)**d for d in range(7)]
 H=sum(weights)
 for cutoff in (Q(1),Q(1,2),Q(1,4),Q(1,8),Q(1,32)):
  active=[i for i in intervals if i[1]-i[0]<=cutoff]
  T=sum(weights[i[2]]*(i[1]-i[0]) for i in active)
  covariance_bound=sum(weights[i[2]]*weights[j[2]]*abs(cov(i,j)) for i in active for j in active)
  check(covariance_bound<=2*H*T+T*T)
  for i in active:
   ancestor_weight=sum(weights[j[2]] for j in intervals if j[0]<=i[0] and i[1]<=j[1])
   check(ancestor_weight<=H)
# Exact Brownian-bridge increment covariance from the min(s,t)-st kernel.
K=lambda x,y:min(x,y)-x*y
for i in intervals[1:]:
 for j in intervals[1:]:
  c=K(i[1],j[1])-K(i[1],j[0])-K(i[0],j[1])+K(i[0],j[0])
  check(c==cov(i,j))
print(json.dumps({'status':'PASS','assertions':count,'coverage':['nested/disjoint bridge covariances','covariance positive semidefinite minor bound','finite laminar ancestor integration bound','independent bridge-kernel increment identity'],'scope':'Exact deterministic covariance controls; Gaussian interpolation and infinite layer limits are proved in TURN_2.md.'},indent=2,sort_keys=True))

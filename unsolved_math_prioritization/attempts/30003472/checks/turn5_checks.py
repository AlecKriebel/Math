#!/usr/bin/env python3
"""Exact finite controls. The infinite-mixture proof and seed input are separate."""
from fractions import Fraction as Q
from itertools import combinations,product
from math import comb,factorial
from functools import lru_cache
import json
checks=0;triple_controls=0
# The explicitly selected seed parameters satisfy the published geometry condition.
a=Q(1,4);b=Q(1,16)
assert b<=a*(1-2*a)*(1-2*b)==Q(7,64);checks+=1
# Rational exposing-line margins for a large finite prefix of the ball family.
for i in range(1,81):
 xi=Q(1,2**i)
 for j in range(1,81):
  xj=Q(1,2**j)
  if i==j:
   assert -xi*xi/16+xi*xi/64<0
  else:
   margin=(xj-xi)**2-xi*xi/16
   assert margin>=15*xj*xj/64
   assert margin-xj*xj/64>0
  checks+=1
@lru_cache(None)
def trees(n):
 if n==1:return (None,)
 return tuple((l,r) for k in range(1,n) for l in trees(k) for r in trees(n-k))
for n in range(1,9):
 assert len(trees(n))==comb(2*n-2,n-1)//n<=4**(n-1);checks+=1
def prefix(a,b):
 return next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
def compress(words):
 if len(words)==1:return ['']
 split=prefix(words[0],words[-1]);left=[w for w in words if w[split]=='0'];right=[w for w in words if w[split]=='1']
 return ['0'+z for z in compress(left)]+['1'+z for z in compress(right)]
words=[format(i,'04b') for i in range(16)]
for n in range(3,7):
 for chosen in combinations(words,n):
  short=compress(chosen)
  for i,j,k in combinations(range(n),3):
   assert (prefix(chosen[i],chosen[j])<prefix(chosen[j],chosen[k]))==(prefix(short[i],short[j])<prefix(short[j],short[k]))
   checks+=1;triple_controls+=1
# Exact coefficient/occupancy identity on synthetic finite arrays, not the seed law.
weights=[Q(1,2),Q(1,3),Q(1,6)]
seed=[Q(1) if k<=2 else Q(1,2**((k-2)**2)) for k in range(9)]
poly=[Q(1)]+[Q(0)]*8
for w in weights:
 terms=[seed[k]*w**k/factorial(k) for k in range(9)]
 poly=[sum(poly[i]*terms[k-i] for i in range(k+1)) for k in range(9)]
for n in range(9):
 direct=sum(factorial(n)*seed[i]*seed[j]*seed[n-i-j]*weights[0]**i*weights[1]**j*weights[2]**(n-i-j)/(factorial(i)*factorial(j)*factorial(n-i-j)) for i in range(n+1) for j in range(n-i+1))
 assert factorial(n)*poly[n]==direct;checks+=1
for n in range(3,81):
 w=Q(1,7)
 T=Q(1024*factorial(n)**3,128**n)
 assert T*w**n/4**(n-1)==4096*factorial(n)**3*(w/512)**n;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'binary_triple_controls':triple_controls,'explicit_ball_indices':[1,80],
 'scope':'Exact geometry, tree-coding and coefficient controls. The seed quadratic convex-probability bound is the credited published input; infinite-product and asymptotic arguments are proved in TURN_5.md, not numerically certified.'},indent=2,sort_keys=True))

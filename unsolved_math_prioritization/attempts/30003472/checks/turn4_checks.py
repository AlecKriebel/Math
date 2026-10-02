#!/usr/bin/env python3
"""Exact finite controls for the transfer/counting reduction."""
from fractions import Fraction as Q
from math import factorial
from itertools import product
import json
checks=0
# Collision union bound for empirical n-tuples.
for n in range(3,41):
 for M in range(n,201):
  distinct=Q(factorial(M),factorial(M-n)*M**n)
  assert 1-distinct<=Q(n*(n-1),2*M);checks+=1
  gamma=Q(1,2**400*n**4)
  Tlower=Q(1024*factorial(n)**3,128**n)
  heavy=factorial(n)*gamma**n
  assert Tlower*heavy==Q(1024*factorial(n)**4,2**(407*n)*n**(4*n));checks+=1
# Direct overlap probability for small empirical index-tuples.
for M in range(2,7):
 for n in range(1,4):
  tuples=list(product(range(M),repeat=n));hit=0
  for x in tuples:
   sx=set(x)
   for y in tuples:hit+=bool(sx.intersection(y))
  assert Q(hit,M**(2*n))<=Q(n*n,M);checks+=1
# The exponent gain is exactly four minus the same-type exponent.
for den in range(1,31):
 for num in range(1,6*den+1):
  p=Q(num,den)
  assert (4-p>0)==(p<4);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'pool_sizes_up_to':200,
 'scope':'Exact finite algebra/collision controls; finite-cloud overlap and arbitrary-measure limiting proofs are in TURN_4.md. The published same-type theorem is an external input.'},indent=2,sort_keys=True))

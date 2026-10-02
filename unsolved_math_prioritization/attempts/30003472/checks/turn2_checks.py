#!/usr/bin/env python3
"""Exact finite controls for the good-interval and convex-strip construction."""
from fractions import Fraction as Q
from itertools import product
from math import ceil
import json
checks=0; arrays=0
# Exhaustive discrete set-mass allocations. No numerical differentiation claims.
for N in range(2,8):
 for mass in product(range(5),repeat=N):
  S=sum(mass)
  if not S:continue
  arrays+=1;m=Q(S,4*N)
  heavy=[i for i,z in enumerate(mass) if Q(z,4*N)>=m/(2*N)]
  assert len(heavy)>=m*N/2;checks+=1
  # Remove the maximal permitted number in several adversarial locations.
  b=int(m*N/4)
  for order in (heavy,heavy[::-1],heavy[::2]+heavy[1::2]):
   good=set(heavy)-set(order[:b])
   ev=[i for i in good if i%2==0];od=[i for i in good if i%2]
   assert len(good)>=m*N/4
   chosen=ev if len(ev)>=len(od) else od
   assert len(chosen)>=m*N/8
   assert all(abs(i-j)>=2 for i in chosen for j in chosen if i!=j)
   checks+=3
for den in range(1,31):
 for num in range(1,den+1):
  m=Q(num,den)
  for n in range(3,31):
   N=ceil(8*n/m)
   assert m*N/8>=n and N<=9*n/m;checks+=1
   assert m/(8*N**3)>=m**4/(5832*n**3);checks+=1
   delta=Q(1,4*N*N)
   assert Q(1,N*N)-2*delta==Q(1,2*N*N);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'discrete_mass_arrays':arrays,
 'mass_grid_denominator_per_cell':4,'interval_sizes':[2,7],
 'scope':'Finite exact combinatorial and constant controls; Fubini, differentiation, dominated convergence and density-point arguments are analytic proofs in TURN_2.md, not numerical tests.'},indent=2,sort_keys=True))

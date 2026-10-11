#!/usr/bin/env python3
"""Exact scalar/lattice controls for the written relative-shadow argument."""
from fractions import Fraction as F
from collections import Counter
from math import gcd
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
low=F(223,71);high=F(22,7)
ck(39<4*low*low<4*high*high<40,'rational_pi_bracket_integer_threshold')
ck(1-high*high/10==F(3,245),'rational_volume_factor')
for parity in (0,1):
 for g2 in range(-80,81):
  if g2%2!=parity:continue
  a=(g2-parity)//2
  for k in range(1,33):
   vec=(2*a+parity,k)
   Q=g2*g2+k*k
   ck(vec==(g2,k) and sum(t*t for t in vec)==Q,'half_integral_cusp_vector')
   ck(gcd(a,1)==1,'primitive_region_filling_class')
   ck((Q>=40)==(Q>4*high*high)==(Q>4*low*low),'exact_long_slope_integer_test')
   if abs(g2)<=k and Q>=40:ck(k>=5,'corner_bound_forces_valence_five')
for V in range(1,101):
 for u in range(1,101):
  f=V+1
  ck(f-V==1,'collapsible_Euler_count')
  ck((6*V>=5*f+u)==(V>=5+u),'relative_incidence_budget')
  if V<=5:ck(6*V<5*f+u,'small_vertex_relative_obstruction')
for Q in range(40,201):
 ck(1-4*high*high/Q>=F(3,245)>0,'uniform_positive_volume_factor')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Scalar and cusp-lattice checks only; no manifold identification, shadow realization, hyperbolicity or alternating coverage is inferred from finite arithmetic.'},indent=2))

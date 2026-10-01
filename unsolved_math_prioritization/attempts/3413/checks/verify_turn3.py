#!/usr/bin/env python3
"""Arithmetic/local-model controls. TURN_3.md supplies the topological proofs."""
from math import gcd,lcm
from fractions import Fraction
from collections import Counter
import json
C=Counter()
def ck(b,k):
 assert b,k
 C[k]+=1
# Local linear cyclic models. Fixed axes of powers and subgroup intersections
# are reconstructed from exponents, not an assumption that the generator is free.
for m in range(2,41):
 for a in range(m):
  for b in range(m):
   if gcd(gcd(a,b),m)!=1:continue
   PA={j for j in range(m) if b*j%m==0} # axis z=0
   PB={j for j in range(m) if a*j%m==0} # axis w=0
   ck(PA&PB=={0},'faithful_action_axis_kernels_disjoint')
   ck(gcd(len(PA),len(PB))==1,'axis_kernel_orders_coprime')
   for j in range(1,m):
    fixed=(a*j%m==0 or b*j%m==0)
    ck(fixed==(j in PA or j in PB),'all_fixed_elements_in_axis_kernels')
   if m%2==0 and len(PA)==2:
    d=m//2
    ck(PA=={0,d},'negative_axis_exact_involution_kernel')
    ck(m//gcd(b,m)==d,'negative_axis_rotation_order')
    ck(a*d%m==d,'involution_normal_half_turn')
    for j in range(2,m):
     if m%j:continue
     k=m//j;H={(r*j)%m for r in range(k)}
     if H<=PA or H<=PB:
      ck(k==2 or k%2==1,'proper_positive_orbit_even_stabilizer_filter')
# Involution derivative preserves the normal-disk orientation and reverses
# the mixed tangent-normal disk orientation.
h=(1,-1,-1)
ck(h[0]*h[1]==-1,'negative_circle_plane_degree')
ck(h[1]*h[2]==1,'positive_circle_plane_degree')
ck(h[0]*h[1]*h[2]==1,'ambient_orientation_positive')
for m in range(2,101,2):
 d=m//2
 # Distinct translates of a point on A, with exact rational angular parameters.
 orbit={Fraction(2*j,m)%1 for j in range(m)}
 ck(len(orbit)==d,'axis_center_orbit_size')
 ck({j for j in range(m) if Fraction(2*j,m)%1==0}=={0,d},'ball_stabilizer_order_two')
 ck(Fraction(d,m)%1==Fraction(1,2),'last_return_normal_rotation_half_turn')
 # Signed blocks produced by the three disk choices and invariant coordinate U.
 for negative,positive,free in [(1,0,0),(2,3,1),(4,2,3)]:
  data=[(d,-1)]*negative+[(d,1)]*positive+[(m,1)]*free+[(1,1)]
  image=lcm(*(a*(2 if s<0 else 1) for a,s in data))
  ck(image==m,'constructed_signed_action_faithful')
  ck(sum(a for a,s in data)==d*(negative+positive)+m*free+1,'constructed_component_count')
# Abstract homomorphisms separated by the additional geometric obstructions.
examples=[(8,[(4,-1),(2,1)],'even_stabilizer'),(12,[(6,-1),(3,1)],'even_stabilizer'),(4,[(2,-1),(1,1),(1,1)],'two_singletons'),(6,[(3,-1),(2,1),(1,1)],'singleton_mixed_orbit')]
for m,blocks,why in examples:
 ck(lcm(*(d*(2 if s<0 else 1) for d,s in blocks))==m,'new_exclusion_is_faithful_abstract_action')
 ck(all(s>0 or 2*d==m for d,s in blocks),'new_exclusion_passes_turn1')
 if why=='even_stabilizer':ck(any(s>0 and 1<d<m and (m//d)%2==0 and m//d>2 for d,s in blocks),'exclusion_even_stabilizer')
 if why=='two_singletons':ck(sum(s>0 and d==1 for d,s in blocks)>1,'exclusion_two_positive_singletons')
 if why=='singleton_mixed_orbit':ck(any(s>0 and d==1 for d,s in blocks) and any(s>0 and 1<d<m and d!=m//2 for d,s in blocks),'exclusion_singleton_and_mixed_length')
# Arithmetic of the distinct normalization in free and branched covers.
for p in range(2,25):
 for ell in range(-10,11):
  ck(Fraction(p*ell,p)==ell,'branched_lift_linking_normalization')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Finite group exponent, local orientation and normalization arithmetic only. Smith input, equivariant-unknot input, branched-cover surfaces and all-order obstructions are proved/cited in TURN_3.md; no hyperbolic completion is inferred.'},indent=2))

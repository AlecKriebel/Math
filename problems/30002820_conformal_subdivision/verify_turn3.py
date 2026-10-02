#!/usr/bin/env python3
"""Exact controls for the fixed-fraction1-to-4 obstruction, with arbitrary inner lengths."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json
checks=Counter()
def ck(x,label):
 assert x,label;checks[label]+=1
def tri(a,b,c):return a+b>c and b+c>a and c+a>b
valid_bases=0;theta_records=Counter()
# Edge order12,23,13; inner edges are indexed by corner1,2,3.
for t12,t23,t13 in product((Q(1,3),Q(1,2),Q(2,3)),repeat=3):
 for k1,k2,k3 in product((Q(1,5),Q(2,5),Q(3,5),Q(4,5)),repeat=3):
  if not (tri(t12,t13,k1) and tri(1-t12,t23,k2) and tri(1-t23,1-t13,k3) and tri(k1,k2,k3)):continue
  valid_bases+=1;theta_records[str((t12,t23,t13))]+=1
  eps=min(Q(1),k3/(2*(k1+k2)))
  ck(tri(eps,Q(1),Q(1)),'strict_original_skinny_triangle')
  ck(eps>0 and eps<=1 and (k1+k2)*eps<=k3/2,'explicit_failure_margin')
  # Original squared endpoint multipliers give (eps,1,1) as length ratios.
  sq=(eps,eps,1/eps)
  ck(sq[0]*sq[1]==eps**2 and sq[1]*sq[2]==sq[0]*sq[2]==1,'original_conformal_scaling_squared')
  for c in (Q(1,2),Q(1),Q(2),Q(5,3)):
   b1=b2=b3=c;m12=eps/c;m23=m13=1/c
   ck(b1*m12*t12==eps*t12 and b2*m12*(1-t12)==eps*(1-t12),'first_edge_interpolation')
   ck(b2*m23*t23==t23 and b3*m23*(1-t23)==1-t23,'second_edge_interpolation')
   ck(b1*m13*t13==t13 and b3*m13*(1-t13)==1-t13,'third_edge_interpolation')
   inner=(k1*m12*m13,k2*m12*m23,k3*m13*m23)
   ck(inner==(k1*eps/c**2,k2*eps/c**2,k3/c**2),'forced_inner_lengths')
   ck(not tri(*inner) and inner[0]+inner[1]<inner[2],'central_triangle_strict_failure')
# The simple numerical example in the proof.
k=Q(1,2);eps=Q(1,4)
ck((k*eps,k*eps,k)==(Q(1,8),Q(1,8),Q(1,2)) and not tri(k*eps,k*eps,k),'explicit_midpoint_reference_control')
print(json.dumps({'status':'PASS','arithmetic':'exact rational','assertions':sum(checks.values()),'by_scope':dict(checks),'valid_reference_refined_metrics':valid_bases,'fixed_fraction_choices_with_valid_reference':len(theta_records),'scope':'Excludes only1-to-4 topology with fixed boundary split fractions, even with arbitrary inner metric functions. Metric-dependent split fractions remain outside the result; original source question unresolved.'},indent=2,sort_keys=True))

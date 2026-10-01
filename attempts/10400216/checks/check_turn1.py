#!/usr/bin/env python3
"""Exact finite controls for the all-size written Euler/corner proof."""
from collections import Counter
from functools import lru_cache
import json
C=Counter()
def ck(a,k):assert a,k;C[k]+=1
@lru_cache(None)
def fixed_parts(total,count,lo=1):
 if count==0:return ((),) if total==0 else ()
 return tuple((a,)+p for a in range(lo,total//count+1) for p in fixed_parts(total-a,count-1,a))
seqs=0
for n in range(1,13):
 for vals in fixed_parts(4*n,n+2):
  seqs+=1
  ck(sum(4-v for v in vals)==8,'Euler_deficit')
  small=sum(v<=3 for v in vals)
  ck(small>=3,'three_small_faces')
  if vals[0]>=2:ck(small>=4,'four_small_faces_without_monogons')
  for outside in range(len(vals)):
   ck(any(v<=3 for i,v in enumerate(vals) if i!=outside),'every_outside_choice_leaves_small_bounded_face')
for v in range(1,65):
 for plus in range(v+1):
  twice_g=2*plus-v
  ck(twice_g*twice_g+v*v<=2*v*v,'corner_triangle_inequality')
  if v<=3:ck(twice_g*twice_g+v*v<=18<36,'strict_below_2pi_squared_using_pi_greater_than_3')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'arithmetic_face_sequences':seqs,'families':dict(C),'scope':'Integer incidence controls only; no planar realization or hyperbolic volume is inferred from these finite cases.'},indent=2))

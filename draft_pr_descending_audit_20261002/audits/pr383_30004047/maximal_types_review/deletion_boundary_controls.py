#!/usr/bin/env python3
"""Independent exact near-boundary and denominator controls, no author import."""
from fractions import Fraction as Q
import json
checks=0;zero_boundaries=0;sign_failures=0;strict_equal_failures=0
for k in (2,3,7,19,101):
 for x,y in [(Q(1,2*k),Q(1,2)),(Q(1,k+1)+Q(1,10**6),Q(1,k+1)+Q(1,10**6)),(Q(1),Q(1,100)),(Q(1,k),Q(1,k)),(Q(1,5*k),Q(1,5*k))]:
  lower_gap=x+k*y-1;upper_gap=k*x+y-1
  first=lower_gap/(k*y);second=upper_gap/(k+y-1)
  assert k*y>0 and k+y-1>0;checks+=2
  points={Q(0),x/2,x-Q(1,10**9),first,second,first-Q(1,10**9),first+Q(1,10**9),second-Q(1,10**9),second+Q(1,10**9)}
  for eps in points:
   if not 0<=eps<x:continue
   xp=(x-eps)/(1-eps)
   assert 0<xp<=1;checks+=1
   assert (xp+k*y>1)==(eps<first);checks+=1
   assert (k*xp+y>=1)==(eps<=second);checks+=1
   if eps==first:assert xp+k*y==1;strict_equal_failures+=1
  if upper_gap==0:
   assert second==0
   for eps in (Q(1,10**9),x/2):
    assert 0<eps<x and k*(x-eps)/(1-eps)+y<1
    checks+=1
   zero_boundaries+=1
  if lower_gap<0 or upper_gap<0:sign_failures+=1
# Exact deletion incidence control: dropping epsilon of B can reduce every A
# degree by at most epsilon; renormalization is necessary, even if all removed
# neighbors hit the same A vertex.
beta=[Q(2,5),Q(1,5),Q(2,5)];eps=beta[1]
neighbors=[{0,1},{1,2},{0,2}];x=Q(3,5)
for S in neighbors:
 before=sum(beta[b] for b in S);after=sum(beta[b] for b in S if b!=1)/(1-eps)
 assert before>=x and after>=(x-eps)/(1-eps);checks+=1
print(json.dumps({'status':'PASS','exact_checks':checks,'weak_boundary_zero_deletion_cases':zero_boundaries,'negative_gap_controls':sign_failures,'first_bound_equalities_rejected':strict_equal_failures,'scope':'Algebraic equivalence on rational extreme and adjacent boundaries plus exact B-deletion incidence; no asserted universal structural deletion.'},indent=2))

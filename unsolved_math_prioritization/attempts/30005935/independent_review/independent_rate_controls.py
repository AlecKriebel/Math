#!/usr/bin/env python3
from fractions import Fraction as Q
from collections import Counter
import json
C=Counter()
def ck(name,value):
 assert value,name
 C[name]+=1
# Parameterize sqrt(kappa) rather than introducing rounded floating square roots.
for cden in range(1,23):
 for cnum in range(1,19):
  c1=Q(cnum,cden)
  for a in (Q(1,8),Q(1,3),Q(2,3),Q(1)):
   root_kappa=a/(8*c1);kappa=root_kappa**2;exponent=c1*root_kappa
   ck('small_cutoff_exponent',0<exponent<=Q(1,8))
   ck('root_mean_square_power',Q(-1,4)+exponent/2<=Q(-3,16))
   ck('exit_probability_power',Q(-1,2)+exponent<=Q(-3,8))
   ck('cutoff_square_identity',kappa==root_kappa*root_kappa)
# Check L_K powers by writing K=q^4: no irrational arithmetic is involved.
for n in range(1,80):
 q=Q(n,13);K=q**4;L=Q(5,4)*q
 ck('L_squared',L**2==Q(25,16)*q*q)
 ck('L_fourth',L**4==Q(625,256)*K)
# Exact relation behind the log-vs-power argument: exp(x) >= x^3/6.
# The exponential assertion is analytic; these controls test the rescaling.
for den in range(1,35):
 for num in range(1,30):
  a=Q(num,den);ell=Q(den+num,den)
  ck('polynomial_majorant_rescale',ell**3/(a*ell)**3*6==6/a**3)
# Bad-event weak comparison is uniform over any bounded-Lipschitz class.
for den in range(2,53):
 for num in range(den+1):
  bad=Q(num,den)
  for good_error in (Q(0),Q(1,7),Q(3,2),Q(3)):
   worst=(1-bad)*min(Q(2),good_error)+2*bad
   ck('bounded_test_event_bound',worst<=good_error+2*bad)
print(json.dumps({'status':'PASS_INDEPENDENT_RATE_CONTROLS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact rate/coupling algebra. The infinite-dimensional estimates and localization are assessed analytically in the review.'},indent=2,sort_keys=True))

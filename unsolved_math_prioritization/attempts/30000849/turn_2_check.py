#!/usr/bin/env python3
from fractions import Fraction as F
from math import prod
import json
counts={}
def check(group,test):
    if not test:raise AssertionError(group)
    counts[group]=counts.get(group,0)+1
# Separate partial-fraction representation of finite exponential convolutions.
for p in [-2,-1,1]:
 for j in range(2,11):
    rates=[F(k)**p for k in range(2,j+1)]
    coeff=[a*prod(b/(b-a) for b in rates if b!=a) for a in rates]
    for z in [F(1,7),F(1,2),F(1),F(3),F(11)]:
        check('laplace_product_vs_residues',sum(c/(z+a) for c,a in zip(coeff,rates))==prod(a/(z+a) for a in rates))
    m=sum(1/a for a in rates);v=sum(1/a**2 for a in rates)
    check('kernel_mass',sum(c/a for c,a in zip(coeff,rates))==1)
    check('kernel_first_moment',sum(c/a**2 for c,a in zip(coeff,rates))==m)
    check('kernel_second_moment',sum(2*c/a**3 for c,a in zip(coeff,rates))==m*m+v)
for j in range(2,51):
 for z in [F(1,3),F(2),F(5)]:
    check('erlang_constant_rate_control',prod(F(1)/(z+1) for k in range(2,j+1))==1/(z+1)**(j-1))
# Exact constraints for both signs in the exponential Markov optimization.
for x in [F(k,7) for k in range(1,30)]:
 for v in [F(1,3),F(1),F(3),F(11)]:
  for B in [F(1,4),F(1),F(5)]:
    lam=min(x/(2*v),1/(2*B))
    check('chernoff_admissible_parameter',lam*B<=F(1,2))
    check('chernoff_exponent',-lam*x+lam*lam*v<=-min(x*x/(4*v),x/(4*B)))
# Clock and amplitude transformations derived independently as rational identities.
for pn in range(-15,10):
 p=F(pn,10)
 for wn in range(-4,21):
    w=F(wn,10);r=(1-w*(1-p))/((w+2)*(1-p))
    s=1/((1-p)*(r+1));q=p+(1-p)*r
    check('positive_clock_power',r+1>0)
    check('clock_size_exponent',s==(w+2)/(3-2*p))
    check('corrected_amplitude',q==(1-w+2*p*(w+1))/(w+2))
    check('mass_exponent_compatibility',s*(2-q)==w+1)
    if p==0:check('constant_kernel_recovery',q==r)
check('selected_parameters',F(1,4)+(1-F(1,4))*F(2,3)==F(3,4))
print(json.dumps({'problem_id':30000849,'substantive_turn':2,'all_exact_checks_passed':True,'counts':counts,'total_exact_assertions':sum(counts.values()),'scope':'Finite convolution identities, Chernoff optimization and rational scaling identities; analytic concentration and conditional transport require proof. The nonlinear monomer asymptotic is not certified.'},indent=2,sort_keys=True))

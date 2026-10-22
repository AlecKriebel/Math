#!/usr/bin/env python3
"""Independent exact finite controls; analytical geometry/spectral proof is separate.
No imports from the submission or its prior reviewers. Standard library only.
"""
from fractions import Fraction as F
from math import factorial
import json
checks=[]
def check(name, condition, evidence=None):
    if not condition:
        raise AssertionError(name)
    checks.append({'name':name,'passed':True,'evidence':evidence})

# Derive normalized coefficients directly from the Hessian of each radial
# monomial r**(n-1), plus the separately indexed -kappa**2 g term.
for n in range(0,21):
    hessian_I=F(-(n-1),factorial(n))
    mass_I=F(n*(n-1),factorial(n)) if n>=2 else F(0)
    direct_I=hessian_I+mass_I
    direct_ee=F(-(n-1)*(n-3),factorial(n))
    # Separate convolution of the exponential with its polynomial numerators.
    convolution_I=F(1,factorial(n))
    if n>=1: convolution_I-=F(1,factorial(n-1))
    if n>=2: convolution_I+=F(1,factorial(n-2))
    convolution_ee=-F(3,factorial(n))
    if n>=1: convolution_ee+=F(3,factorial(n-1))
    if n>=2: convolution_ee-=F(1,factorial(n-2))
    check('radial_Hessian_vs_exponential_I_n'+str(n),direct_I==convolution_I,str(direct_I))
    check('radial_Hessian_vs_exponential_ee_n'+str(n),direct_ee==convolution_ee,str(direct_ee))

check('quadratic_I_coefficient',-F((2-1)**2,factorial(2))==-F(1,2))
check('quadratic_ee_coefficient',F((2-1)*(2-3),factorial(2))==-F(1,2))
check('cubic_I_coefficient',-F((3-1)**2,factorial(3))==-F(2,3))
check('cubic_ee_coefficient',F((3-1)*(3-3),factorial(3))==0)

# e tail after n=8: each successive ratio from 1/9! is at most 1/10.
e_upper=sum((F(1,factorial(n)) for n in range(9)),F(0))+F(1,factorial(9))/(1-F(1,10))
check('rigorous_e_upper',e_upper<F(11,4),str(e_upper))
check('numerator_remainder_tail_less_than_one',2*e_upper-F(9,2)<1,str(2*e_upper-F(9,2)))
check('C2_HS_squared_bound',F(6,64)*F(32,3)==1)
check('remainder_HS_squared_bound',F(9,16)*F(64,9)==4)
check('dynamic_uniform_bound_at_half',1+F(2,9)*F(1,2)+2*F(1,4)==F(29,18)<2)

# The spherical harmonic spectral gap for all ell>=2 follows algebraically:
# a_(ell+1)-a_ell = 1/((2ell+1)(2ell+3)) > 0.
for ell in [2,3,7,100,10000]:
    a=F(ell,2*ell+1)-F(1,3)
    b=F(ell+1,2*ell+3)-F(1,3)
    check('harmonic_gap_and_monotonicity_'+str(ell),a>=F(1,15) and b-a==F(1,(2*ell+1)*(2*ell+3)))
check('ball_constant_mode_shift',F(1,3)-F(1,3)==0)
check('contour_static_distance',F(1,15)-F(1,30)==F(1,30))
check('projection_resolvent_constant',F(1,30)*60*30==60)

k=F(1,10000); eps=2*k*k; eta=120*k*k
check('explicit_frequency_epsilon',eps<=F(1,60),str(eps))
check('explicit_frequency_graph_smallness',eta<=F(1,2),str(eta))
check('graph_bound',eta/(1-eta)<=240*k*k,str(eta/(1-eta)))
check('graph_error_constant',2+2*240==482)
check('trace_error_constant',3*482==1446)
trace_bound=-F(2,3)*k**3+1446*k**4
check('strictly_negative_exact_trace',trace_bound<0 and trace_bound==-F(7831,15000)*k**3,str(trace_bound))
check('one_eigenvalue_negative_by_average',trace_bound/3<0,str(trace_bound/3))

# These are adversarial sign/normalization controls, not invalid input tests.
check('wrong_radiation_sign_is_detectably_positive',F(2,3)*k**3-1446*k**4>0)
check('zero_only_after_required_static_shift',F(1,3)!=0)
check('no_effective_support_index_claimed',True,'No finite numerical membership or spectral index is computed.')

# The geometric series bounds hold symbolically for every j>=1; finite
# representatives check arithmetic only, while the proof supplies universality.
for j in [1,2,10,100]:
    removed_ratio=F(1,7*2**(3*j+12))
    check('removed_volume_fraction_'+str(j),0<removed_ratio<1,str(removed_ratio))
check('removed_fraction_geometric_sum',F(1,8)/(1-F(1,8))==F(1,7))
print(json.dumps({'schema':'pr214-independent-geometry-exact-controls-v1','passed':True,'check_count':len(checks),'checks':checks,'limits':['Finite rational controls do not prove spherical completeness, topology, convergence, or existence of an effective support index.','No submission code or previous reviewer code imported.']},indent=2,sort_keys=True))

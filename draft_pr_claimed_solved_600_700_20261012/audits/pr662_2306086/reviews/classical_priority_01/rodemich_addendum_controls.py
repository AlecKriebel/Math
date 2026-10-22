#!/usr/bin/env python3
"""Exact margins for the analytic proof in RODEMICH_ADDENDUM.md.
The continuum argument is the written proof, not a floating-point grid.
"""
from fractions import Fraction as Q
from math import factorial, exp, sin, cos, sqrt
import json
x=Q(1,100)
sum5=sum(Q(1,factorial(k)) for k in range(6))
# After the n=6 term, successive denominators increase by at least7.
e_upper=sum5+Q(1,factorial(6))/(1-Q(1,7))
e_lower=sum(Q(1,factorial(k)) for k in range(4))
checks={
 'e_upper_less_than_11_over4':e_upper<Q(11,4),
 'e_lower_greater_than5_over2':e_lower>Q(5,2),
 'sqrt3_less_than7_over4':Q(3)<Q(7,4)**2,
 '27_times7_over4_less_than50':27*Q(7,4)<50,
 'sin_lower_taylor_greater_than99_over10000':x-x**3/6>Q(99,10000),
 'cos_lower_taylor_greater_than9_over10':1-x*x/2>Q(9,10),
 'derivative_product_margin':Q(99,10000)*500/Q(11,4)==Q(9,5),
 'pre_schwarzian_squared_lower_bound':4*(Q(9,5)**2+Q(9,10)**2)==Q(81,5),
 'squared_lower_bound_exceeds16':Q(81,5)>16,
}
if not all(checks.values()):raise RuntimeError('An exact margin failed')
# Stable form; no exponentially tiny amplitude multiplied by a huge cosh.
hp=500*(exp(-1)+exp(1-100*3.141592653589793))
a_squared=4*((sin(.01)*hp)**2+cos(.01)**2)
print(json.dumps({'exact_checks':checks,'exact_check_count':len(checks),
 'rational_proof_lower_bound':str(Q(81,5)),
 'illustrative_noncertified':{'A_squared':a_squared,'A_modulus':sqrt(a_squared)},
 'countermodel_is_globally_univalent':False,
 'countermodel_refutes_PR662':False},indent=2))

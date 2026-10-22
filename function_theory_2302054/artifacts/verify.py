#!/usr/bin/env python3
"""Finite exact checks for PROOF.md; these are not an analytic proof."""
from fractions import Fraction as F
import json

checks = {}
# e > 2 follows from its series; t=e^2>4. Constants use t>=4.
checks['exp_series_lower_bound'] = sum((F(1), F(1), F(1, 2))) > 2
checks['c_lower_bound_at_t4'] = 1-F(1,4) == F(3,4)
checks['C_lower_bound_at_t4'] = 1-F(4,15) > F(1,2)
# t^2 - 2t - 1 is positive at 4 and strictly increasing for t>=4.
checks['C_half_polynomial_at_t4'] = 4**2-2*4-1 > 0
checks['C_half_polynomial_derivative_at_t4'] = 2*4-2 > 0
checks['large_radius_uniform_margin'] = F(1,2)*F(3,4)*4 == F(3,2)
checks['small_radius_margin'] = F(1,2) > F(1,16**2)
# Symbolic exponent identities, checked at enough exact points for degree <=2.
checks['product_exponent_identity'] = all(
    (n-1)*(F(2*n-1,2))-F(n*(n-1),2)-n == F(n*n-4*n+1,2)
    for n in range(1,6))
a = lambda n:F(n*n-4*n+1,2)
checks['ratio_exponent_identity'] = all(a(n+1)-a(n)==F(2*n-3,2) for n in range(1,6))
checks['minimum_exponent_n2'] = a(2)==F(-3,2)
checks['ratio_lower_bound_n_ge2'] = F(3,4)*4 > 1
# pi<4 yields an angle/chord bound <r/4 for the 32-link chain.
checks['chain_step_bound_using_pi_lt4'] = F(4,16)==F(1,4)
checks['harnack_factor_half_radius'] = (1+F(1,2))/(1-F(1,2))==3
checks['annulus_disk_inclusion_lower_using_e_gt2'] = F(1,2)==F(1,2)
checks['annulus_disk_inclusion_upper_using_e_gt2'] = F(3,2)<2
checks['nearest_disk_inner_separation_using_e_gt2'] = 16*(2-1)>1
checks['nearest_disk_outer_separation_using_e_gt2'] = 2**7*(2-1)>1
assert all(checks.values()), checks
print(json.dumps({
    'all_passed': all(checks.values()),
    'check_count': len(checks),
    'checks': checks,
    'harnack_exponent': 3**32,
    'scope': 'Exact finite algebra and conservative constants only; analytic convergence, Harnack, maximum modulus and Liouville are proved or invoked in PROOF.md, not certified by these checks.'
}, indent=2, sort_keys=True))

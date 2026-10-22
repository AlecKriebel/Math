#!/usr/bin/env python3
"""Finite arithmetic checks; these do not substitute for the accompanying proof."""
import json, math
from pathlib import Path

def v(n, p):
    k = 0
    while n and n % p == 0:
        k += 1
        n //= p
    return k

def norm_square_values(p, d):
    return sorted({((a*a+d*b*b) % p)**2 % p
                   for a in range(p) for b in range(p)
                   if (a*a+d*b*b) % p})

checks = {}
checks['surface_trace_gcd'] = math.gcd(7**4-1, 11**4-1)
checks['surface_trace_gcd_after_T5'] = math.gcd(checks['surface_trace_gcd'], 5**4-1)
assert checks['surface_trace_gcd'] == 240  # 5 times an R-unit
assert checks['surface_trace_gcd_after_T5'] == 48  # an R-unit
assert -6*(7**4-1)+(11**4-1) == 240
assert 125*5-(5**4-1) == 1
checks['ramified_five_norm_squares'] = norm_square_values(5, 5)
checks['split_five_norm_squares'] = norm_square_values(5, 1)
checks['inert_five_norm_squares'] = norm_square_values(5, 2)
checks['ramified_seven_norm_squares'] = norm_square_values(7, 7)
assert checks['ramified_five_norm_squares'] == [1]
assert checks['split_five_norm_squares'] == [1, 4]
assert checks['inert_five_norm_squares'] == [1, 4]
assert checks['ramified_seven_norm_squares'] == [1, 2, 4]
checks['quadratic_biquadratic_discriminants'] = {
    'F': -20, 'real_subfield': 5, 'other_quadratic': -4,
    'biquadratic_absolute': (-20)*5*(-4), 'relative_norm': ((-20)*5*(-4))//((-20)**2)
}
assert checks['quadratic_biquadratic_discriminants']['relative_norm'] == 1
norm_alpha = 1+5*3**2  # alpha=1+3 sqrt(-5), congruent to 1 modulo (3)
checks['principal_ray_auxiliary'] = {
    'alpha': '1+3*sqrt(-5)', 'norm': norm_alpha,
    'smoothing_scalar': norm_alpha**2-1,
    'five_valuation': v(norm_alpha**2-1,5)
}
assert norm_alpha == 46 and v(norm_alpha**2-1,5) == 1
checks['definition_modulus_residues'] = {
    str(p): [(2**e-1)%p for e in (1,2)] for p in (5,7,11,13,17,19)
}
assert all(all(x != 0 for x in pair) for pair in checks['definition_modulus_residues'].values())
checks['localized_counterexample_support'] = {
    'F': 'Q(sqrt(-5))', 'class_number': 2,
    'level': '(11)', 'inert_norm': 121,
    'residue_unit_order': 120, 'five_valuation': v(120,5),
    'meaning': 'Nonzero ambient exceptional residue module; no actual cocycle nonvanishing claimed.'
}
assert pow((-5)%11,5,11)==10  # 11 inert
checks['status'] = 'all exact finite checks passed'
path=Path(__file__).with_name('CHECK_RESULTS.json')
path.write_text(json.dumps(checks,indent=2)+'\n')
print(path.read_text())

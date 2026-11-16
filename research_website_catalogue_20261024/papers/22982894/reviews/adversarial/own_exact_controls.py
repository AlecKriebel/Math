#!/usr/bin/env python3
"""Own finite rational controls from sealed paper-first hand oracles.
No target imports, external files, network, subprocess, random search, or writes.
This finite calculation does not prove the universal theorem.
"""
from fractions import Fraction as F
from math import comb
import json

checks = 0


def need(condition, message):
    global checks
    checks += 1
    if not condition:
        raise ValueError(message)


def text(q):
    return str(F(q))


def line(c, t):
    return sum((F(a) * t**r for r, a in enumerate(c)), F(0))


def entry(c, k, t):
    d = len(c) - 1
    return sum((F(comb(k, r), comb(d, r)) * F(c[r]) * t**r
                for r in range(k + 1)), F(0))


def case(name, c, t, expectation):
    d, p = len(c) - 1, line(c, t)
    need(c[0] == 1 and d % 2 == 0 and p > 0, name + ' domain')
    rows = []
    for k in range(d + 1):
        n = entry(c, k, t)
        den = p**k
        gap = den - n**d
        if k in (0, d):
            need(gap == 0, name + ' pure equality')
        rows.append({'copies_of_perturbed_column': k, 'polarized_N': text(n),
                     'product_of_d_diagonal_values': text(den),
                     'gap_product_minus_N_power_d': text(gap),
                     'strictly_positive_N': n > 0, 'strictly_positive_gap': gap > 0})
    mixed = rows[1:-1]
    good = all(v['strictly_positive_N'] and v['strictly_positive_gap'] for v in mixed)
    need(good == expectation, name + ' declared entire mixed-tuple outcome')
    return {'name': name, 'degree': d, 'epsilon': text(t),
            'line_polynomial_coefficients': [text(a) for a in c],
            'p_perturbed': text(p), 'all_mixed_success_expected': expectation,
            'all_mixed_success_observed': good, 'every_repetition_row': rows}


def gap(c, k, t):
    d = len(c) - 1
    return line(c, t)**k - entry(c, k, t)**d


radial2 = [1, 0, 1]
radial4 = [1, 0, 2, 0, 1]
radial6 = [1, 0, 3, 0, 3, 0, 1]
nonconvex_min = [1, 0, 14, 0, 1]
nonconvex_wrong = [1, 0, -1, 0, 1]
large_cubic = [1, 0, 3, -2000, 1000001]
cases = [
    case('quadratic_nonzero_basis', radial2, F(1, 2), True),
    case('quadratic_singular_limit', radial2, F(0), False),
    case('radial_quartic_sharp_Hessian', radial4, F(1), True),
    case('radial_sextic_sharp_Hessian', radial6, F(1, 2), True),
    case('nonconvex_minimum_small_epsilon', nonconvex_min, F(1, 10), True),
    case('nonconvex_minimum_large_epsilon_equality', nonconvex_min, F(1), False),
    case('nonconvex_minimum_large_epsilon_upper_failure', nonconvex_min, F(2), False),
    case('nonconvex_wrong_direction', nonconvex_wrong, F(1, 2), False),
    case('large_cubic_sufficiently_small', large_cubic, F(1, 10), True),
    case('large_cubic_sign_failure', large_cubic, F(1, 5), False),
    case('semidefinite_rank_one_excluded', [1, 0, 0, 0, 0], F(1, 2), False),
]
hand_matches = {
    'quadratic_gap': (gap(radial2, 1, F(1, 2)), F(1, 4)),
    'radial4_k1': (gap(radial4, 1, F(1)), F(3)),
    'radial4_k2': (gap(radial4, 2, F(1)), F(1040, 81)),
    'radial4_k3': (gap(radial4, 3, F(1)), F(48)),
    'nonconvex_equality': (gap(nonconvex_min, 3, F(1)), F(0)),
    'nonconvex_upper_failure': (gap(nonconvex_min, 3, F(2)), F(-318264)),
    'wrong_direction_gap': (gap(nonconvex_wrong, 1, F(1, 2)), F(-3, 16)),
    'large_cubic_N_small': (entry(large_cubic, 3, F(1, 10)), F(103, 200)),
    'large_cubic_N_sign_failure': (entry(large_cubic, 3, F(1, 5)), F(-147, 50)),
}
for name, (actual, expected) in hand_matches.items():
    need(actual == expected, 'sealed hand oracle ' + name)
need(gap(large_cubic, 3, F(1, 5)) > 0,
     'gap positive does not establish lower coefficient positivity')
need(F(radial4[2], comb(4, 2)) == F(1, 3), 'sharp quartic tangent Q')
need(F(radial6[2], comb(6, 2)) == F(1, 5), 'sharp sextic tangent Q')
need(F(nonconvex_wrong[2], comb(4, 2)) == F(-1, 6), 'wrong-direction Hessian fails')

# Actual rational three-dimensional columns; compute Gram and determinant.
t = F(1, 2)
columns = [(F(1), t, F(0)), (F(1), F(0), t), (F(1), F(0), F(0))]
gram = [[sum((a*b for a, b in zip(x, y)), F(0)) for y in columns]
        for x in columns]
a, b, c = columns
# Determinant of the matrix whose columns are a,b,c.
det = a[0]*(b[1]*c[2]-b[2]*c[1])-b[0]*(a[1]*c[2]-a[2]*c[1])+c[0]*(a[1]*b[2]-a[2]*b[1])
need(det == F(1, 4), 'three-dimensional full-rank determinant')
quad3 = []
for i in range(3):
    for j in range(3):
        n, den = gram[i][j], gram[i][i]*gram[j][j]
        g = den - n*n
        need(n > 0 and (g == 0 if i == j else g > 0), 'all ordered3d quadratic entries')
        quad3.append({'tuple': [i+1, j+1], 'N': text(n), 'gap': text(g),
                      'normalized_entry_squared': text(n*n/den)})

# The normalized quartic 1122 entry has a rational denominator sqrt(4)=2.
ordered1122 = entry(radial4, 2, F(1)) / 2
ordinary1122 = comb(4, 2) * ordered1122
need(ordered1122 == F(2, 3) and ordinary1122 == 4, 'multinomial distinction')
need(F(12, comb(4, 2)) == 2, 'original-coordinate ordered entry can exceed1')
need(F(81) * F(1, 3)**4 == 1, 'm1 unit diagonal')

scales = []
t = F(1, 10)
for lam in [F(10**60), F(1, 10**60)]:
    for k in [1, 2, 3]:
        n, p = entry(nonconvex_min, k, t), line(nonconvex_min, t)
        original_den = p**k
        scaled_n = lam*n
        scaled_den = (lam*p)**k * lam**(4-k)
        scaled_gap = scaled_den - scaled_n**4
        need(scaled_gap == lam**4 * (original_den - n**4) and scaled_gap > 0,
             'positive scale homogeneity and sign')
        need(scaled_n**4 / scaled_den == n**4 / original_den,
             'scale invariant normalized entry power')
        scales.append({'lambda': text(lam), 'copies': k,
                       'exact_gap_scaling_ratio': text(scaled_gap/(original_den-n**4)),
                       'normalized_entry_power4': text(scaled_n**4/scaled_den)})

print(json.dumps({'status': 'PASS_OWN_SEALED_HAND_ORACLES_AND_EXPECTED_BOUNDARY_FAILURES',
                  'checks': checks, 'native_or_foreign_material_imported': False,
                  'finite_controls_prove_universal_theorem': False,
                  'all_actual_cases': cases,
                  'hand_oracles_actual_and_expected': {k: [text(a), text(b)] for k, (a, b) in hand_matches.items()},
                  'quadratic3d': {'epsilon': '1/2', 'determinant': text(det),
                                   'all_ordered_rows': quad3},
                  'normalized_ordered1122': text(ordered1122),
                  'normalized_ordinary1122': text(ordinary1122),
                  'extreme_positive_scale_controls': scales}, indent=2))

#!/usr/bin/env python3
"""Exact arithmetic checks for the partial results on Function Theory 5.39.

Run with Python 3. No external packages or source files are used. The analytic
arguments are in PROOF.md; these checks do not replace their proof or review.
"""
from fractions import Fraction as Q
from math import comb
import json


def multiply(x, y):
    out = [Q(0)] * (len(x) + len(y) - 1)
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i + j] += a * b
    return out


def power(x, exponent):
    result = [Q(1)]
    for _ in range(exponent):
        result = multiply(result, x)
    return result


def derivative(x):
    return [i * x[i] for i in range(1, len(x))]


def subtract(x, y):
    n = max(len(x), len(y))
    return [(x[i] if i < len(x) else Q(0)) -
            (y[i] if i < len(y) else Q(0)) for i in range(n)]


def run():
    checks = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    a, r = Q(2, 3), Q(99, 200)
    phi_num, phi_den = [Q(0), a, Q(1)], [Q(1), a]
    dp_num = subtract(multiply(derivative(phi_num), phi_den),
                      multiply(phi_num, derivative(phi_den)))
    check('quotient_rule_for_phi_derivative', dp_num == [a, Q(2), a])
    u_num = [Q(1), a + a / 5, Q(1, 5)]
    check('composition_with_f_prime', u_num == [Q(1), 6*a/5, Q(1, 5)])
    check('admissible_Blaschke_parameter', 0 < a < 1)
    check('radius_below_one_half', 0 < r < Q(1, 2))

    numerator = multiply(power(dp_num, 7), power(u_num, 7))
    denominator = power(phi_den, 21)
    order = 10
    inverse = [Q((-1)**n * comb(20+n, n)) * a**n
               for n in range(order + 1)]
    c = [sum((numerator[j] * inverse[n-j]
              for j in range(min(n, len(numerator)-1) + 1)), Q(0))
         for n in range(order + 1)]

    # A second calculation solves denominator * series = numerator directly,
    # without the negative-binomial formula used in the first calculation.
    recurrence = []
    for n in range(order + 1):
        target = numerator[n] if n < len(numerator) else Q(0)
        target -= sum((denominator[k] * recurrence[n-k]
                       for k in range(1, min(n, len(denominator)-1)+1)), Q(0))
        recurrence.append(target / denominator[0])
    expected = list(map(Q, [
        '128/2187', '896/1215', '563584/164025', '9755648/1476225',
        '19731712/7381125', '-1822435328/553584375',
        '109413686144/24911296875', '-12353279872/124556484375',
        '-23093018368/2767921875', '3793230310016/224201671875',
        '-279418450304/14946778125']))
    for n in range(order + 1):
        check('coefficient_%02d_independent_recurrence' % n, c[n] == recurrence[n])
        check('coefficient_%02d_matches_manuscript' % n, c[n] == expected[n])

    left = sum((c[n]**2 * r**(2*n) for n in range(order+1)), Q(0))
    right = sum((Q(comb(7, n)**2, 5**(2*n)) * r**(2*n)
                 for n in range(8)), Q(0))
    right_independent_coeffs = power([Q(1), Q(1, 5)], 7)
    right_independent = sum((v*v*r**(2*n)
                             for n, v in enumerate(right_independent_coeffs)), Q(0))
    check('right_mean_independent_polynomial_power', right == right_independent)
    gap = left - right
    expected_gap = Q(171427691243281345585321685814196084464053669376850321,
                    29893556250000000000000000000000000000000000000000000000)
    check('exact_gap_matches_manuscript', gap == expected_gap)
    check('strict_positive_gap_exceeds_one_two_hundredth', gap > Q(1, 200))

    # Laurent coefficient arithmetic for the perturbation at a=0, r=1/2.
    v = {-1: Q(1), 1: Q(-3, 4)}
    v_conjugate = {-n: c for n, c in v.items()}
    real_v = {n: (v.get(n, Q(0)) + v_conjugate.get(n, Q(0))) / 2
              for n in set(v) | set(v_conjugate)}
    mean_abs_v_squared = sum((c*c for c in v.values()), Q(0))
    mean_real_v_squared = sum((c*real_v.get(-n, Q(0))
                              for n, c in real_v.items()), Q(0))
    mean_real_w = Q(-1)
    check('perturbation_mean_abs_v_squared', mean_abs_v_squared == Q(25, 16))
    check('perturbation_mean_real_v_squared', mean_real_v_squared == Q(1, 32))
    # Coefficients of p and p^2 in p*Re(w)+(p/2)|v|^2+
    # (p*(p-2)/2)*(Re(v))^2.
    linear = mean_real_w + mean_abs_v_squared/2 - mean_real_v_squared
    quadratic = mean_real_v_squared/2
    check('perturbation_polynomial_p_coefficient', linear == Q(-1, 4))
    check('perturbation_polynomial_p_squared_coefficient', quadratic == Q(1, 64))

    # Universal polynomial identity used for decreasing quadratic weights.
    # n^2-(n+1)^2/4 = (n-1)(3n+1)/4.
    lhs_coeff = [Q(-1, 4), Q(-1, 2), Q(3, 4)]
    rhs_coeff = multiply([Q(-1), Q(1)], [Q(1, 4), Q(3, 4)])
    check('quadratic_weight_factorization', lhs_coeff == rhs_coeff)
    # (1-t)-k(1-t^2) = (1-t)(1-k-kt), verified coefficientwise
    # at two k values; the general algebraic identity is proved in PROOF.md.
    for k in (Q(1, 3), Q(1, 2)):
        check('pointwise_bound_factorization_k_' + str(k),
              [1-k, Q(-1), k] == multiply([Q(1), Q(-1)], [1-k, -k]))

    return {
        'result': 'PASS',
        'problem_id': 2305039,
        'overall_mathematical_status': 'unsolved_partial_results',
        'exact_check_count': len(checks),
        'checks': checks,
        'certificate': {
            'p': 14, 'r': str(r), 'a': str(a),
            'retained_coefficients': len(c),
            'coefficients': list(map(str, c)),
            'right_mean_power': str(right),
            'lower_bound_minus_right': str(gap),
            'gap_greater_than': '1/200',
            'tail_handling': 'All omitted Parseval terms are nonnegative.'
        },
        'limitations': [
            'Exact arithmetic checks do not formally verify the analytic arguments.',
            'No exact value of r_p for finite p>2 is established.',
            'No historical novelty or complete literature coverage is claimed.'
        ]
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

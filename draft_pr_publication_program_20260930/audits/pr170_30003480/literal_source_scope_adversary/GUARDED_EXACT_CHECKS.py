"""Independent exact arithmetic controls. Finite controls do not prove the theorem."""
import argparse
from fractions import Fraction as F
from itertools import product
from math import prod
import json
import sys


class VerificationFailure(RuntimeError):
    pass


def guard(condition, message):
    if not condition:
        raise VerificationFailure(message)


def run(variant):
    d = [F(2401, 10000), F(81, 625), F(81, 625), F(1, 10000)]
    roots = [F(49, 100), F(36, 100), F(36, 100), F(1, 100)]
    q2_coefficient = F(1, 2)
    ghz_secondary_relation = '<='
    if variant == 'q2_coefficient':
        q2_coefficient = F(1, 4)
    elif variant == 'witness_roots':
        roots[0] = F(48, 100)
    elif variant == 'witness_coordinates':
        d[3] = F(0)
    elif variant == 'ghz_discrepancy':
        ghz_secondary_relation = '>='

    guard(all(0 < x < F(1, 4) for x in d),
          'Witness must remain strictly inside cube')
    guard([x*x for x in roots] == d,
          'Witness roots do not square to coordinates')
    polygon_factors = [sum(d)-2*x for x in d]
    guard(all(x > 0 for x in polygon_factors),
          'Witness determinant polygon inequalities must be strict')
    q1 = prod(polygon_factors)
    all_sign_factors = [sum(e*x for e, x in zip(eps, roots))
                        for eps in product([-1, 1], repeat=4)]
    guard(len(all_sign_factors) == 16, 'Full sign product must contain 16 factors')
    q2 = q2_coefficient * prod(all_sign_factors)
    guard(q1 == F(168760917, 305175781250), 'Q1 exact product changed')
    guard(q2 == F(23632249608, 2384185791015625),
          'Q2 coefficient/full-product value changed')
    guard(q1-q2 == F(2589624828909, 4768371582031250) and q1-q2 > 0,
          'Positive exact conjecture gap changed')
    guard(d[0] > F(2, 5)*(1-F(2, 5)), 'Witness largest-eigenvalue lower threshold failed')
    guard(d[1] < F(1, 6)*(1-F(1, 6)) and d[2] < F(1, 6)*(1-F(1, 6)),
          'Witness two eigenvalue upper thresholds failed')
    guard(d[3] < F(1, 100)*(1-F(1, 100)), 'Witness final eigenvalue upper threshold failed')
    guard(F(1, 3)+F(1, 100) < F(2, 5), 'Eigenvalue polygon exclusion margin failed')

    parity_cases = [(F(0), F(0), F(0)),
                    (F(0), F(1, 2), F(1, 2)),
                    (F(1, 2), F(1, 2), F(1, 2)),
                    (F(1, 5), F(1, 10), F(1, 10)),
                    (F(1, 3), F(1, 3), F(1, 3))]
    parity_results = []
    for t in parity_cases:
        a, b, c = t
        weights = [1-(a+b+c)/2, (b+c-a)/2, (a+c-b)/2, (a+b-c)/2]
        if variant == 'parity_weights' and t == (F(1, 5), F(1, 10), F(1, 10)):
            # Preserve normalization and positivity, but corrupt two requested marginals.
            weights[0] -= F(1, 100)
            weights[1] += F(1, 100)
        guard(all(x >= 0 for x in weights) and sum(weights) == 1,
              'Parity weights must be nonnegative and normalized')
        marginals = [weights[2]+weights[3], weights[1]+weights[3], weights[1]+weights[2]]
        guard(marginals == list(t),
              'Parity weights do not realize requested marginal eigenvalues')
        guard(all(0 <= x <= F(1, 2) for x in marginals),
              'Parity marginal values must be smaller eigenvalues')
        determinants = [x*(1-x) for x in marginals]
        parity_results.append({'t': list(map(str, t)), 'weights': list(map(str, weights)),
                               'determinants': list(map(str, determinants))})
    for t in parity_cases[-2:]:
        determinants = [x*(1-x) for x in t]
        guard(all(0 < x < F(1, 4) for x in determinants),
              'Boundary/reflected patch coordinates must be strictly inside cube')
        guard(all(sum(determinants)-2*x > 0 for x in determinants),
              'Boundary/reflected patch determinant polygon slacks must be positive')

    ghz_d = [F(1, 4)]*3
    ghz_q1 = prod(sum(ghz_d)-2*x for x in ghz_d)
    ghz_q2 = F(1, 2)*prod(sum(F(e, 2) for e in eps)
                         for eps in product([-1, 1], repeat=3))
    pair_values = [(ghz_d[i]-ghz_d[j])**2+(ghz_d[i]+ghz_d[j])/2
                   for i, j in [(0, 1), (0, 2), (1, 2)]]
    upper_bound = F(3, 16)
    if ghz_secondary_relation == '<=':
        secondary_pairs_hold = all(x <= upper_bound for x in pair_values)
    elif ghz_secondary_relation == '>=':
        secondary_pairs_hold = all(x >= upper_bound for x in pair_values)
    else:
        raise VerificationFailure('Unrecognized GHZ secondary relation')
    literal_union_includes_ghz = (ghz_q1 >= ghz_q2 or
                                (ghz_q1 <= ghz_q2 and secondary_pairs_hold))
    guard(not literal_union_includes_ghz, 'Literal GHZ discrepancy is not reproduced')
    guard(ghz_q1 == F(1, 64) and ghz_q2 == F(9, 512) and ghz_q1 < ghz_q2,
          'GHZ full-product exact values changed')
    guard(all(x == F(1, 4) and x > upper_bound for x in pair_values),
          'GHZ printed secondary inequality discrepancy changed')

    return {'status': 'verified_finite_controls', 'variant': variant,
            'universal_theorem_proved_by_finite_checks': False,
            'Q1': str(q1), 'Q2': str(q2), 'Q1_minus_Q2': str(q1-q2),
            'all_sign_factors': list(map(str, all_sign_factors)),
            'parity_support_boundary_checks': parity_results,
            'GHZ_Q1': str(ghz_q1), 'GHZ_Q2': str(ghz_q2),
            'GHZ_literal_union_includes_feasible_tuple': literal_union_includes_ghz}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', default='baseline',
                        choices=['baseline', 'q2_coefficient', 'witness_roots',
                                 'witness_coordinates', 'parity_weights', 'ghz_discrepancy'])
    args = parser.parse_args()
    try:
        result = run(args.variant)
    except VerificationFailure as exc:
        print(json.dumps({'status': 'verification_failed', 'variant': args.variant,
                          'error': str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Independent, exact finite adversarial controls; no existence theorem is inferred."""
from itertools import combinations
from fractions import Fraction
from math import comb
from pathlib import Path
import json


def projection_statistics(values, n, s):
    # Independently aggregate output-1 COUNTS on outside projections.
    outside = [i for i in range(n) if not (s >> i) & 1]
    hits = [0] * (1 << len(outside))
    for x, value in enumerate(values):
        u = sum(((x >> j) & 1) << pos for pos, j in enumerate(outside))
        hits[u] += value
    size = 1 << s.bit_count()
    return (sum(0 < h < size for h in hits),
            sum(h > 0 for h in hits),
            sum(h < size for h in hits), len(hits))


def run():
    pair_count = 0
    by_dimension = []
    for n in range(5):
        pairs = 0
        for mask in range(1 << (1 << n)):
            values = [(mask >> x) & 1 for x in range(1 << n)]
            rows = [projection_statistics(values, n, s) for s in range(1 << n)]
            for s, (u, jp, jm, den) in enumerate(rows):
                assert u == jp + jm - den
                assert 0 <= u <= min(jp, jm) <= den
                assert jp * len(values) >= sum(values) * den
                assert jm * len(values) >= (len(values) - sum(values)) * den
                for bit in range(n):
                    a, b, c, d = rows[s | (1 << bit)]
                    assert u * d <= a * den
                    assert jp * d <= b * den
                    assert jm * d <= c * den
                pairs += 1
        by_dimension.append({'n': n, 'pairs': pairs})
        pair_count += pairs
    assert pair_count == 1050698

    deletion_pairs = 0
    for n in range(4):
        # Every pair f <= g is represented uniquely by a base-3 labeling
        # (0,0), (0,1), or (1,1) of each cube input.
        for code in range(3 ** (1 << n)):
            f = []; g = []
            for x in range(1 << n):
                digit = code % 3; code //= 3
                f.append(int(digit == 2)); g.append(int(digit >= 1))
            for s in range(1 << n):
                _, f_jp, _, den = projection_statistics(f, n, s)
                _, g_jp, _, den2 = projection_statistics(g, n, s)
                assert den == den2 and f_jp <= g_jp
                deletion_pairs += 1
    # U itself is NOT monotone under support deletion. This is deliberate.
    f = projection_statistics([0, 1], 1, 1)
    g = projection_statistics([1, 1], 1, 1)
    assert f[0] == 1 and g[0] == 0 and f[1] <= g[1]

    clause_cases = 0
    for n in range(1, 7):
        for k in range(1, n + 1):
            for distance in range(n + 1):
                y = (1 << distance) - 1
                both = total = 0
                for support in combinations(range(n), k):
                    for signs in range(1 << k):
                        sat0 = any(((signs >> j) & 1) == 0 for j in range(k))
                        saty = any(((signs >> j) & 1) == ((y >> i) & 1)
                                   for j, i in enumerate(support))
                        both += sat0 and saty; total += 1
                q = Fraction(1, 1 << k)
                overlap = Fraction(comb(n - distance, k), comb(n, k)) if n-distance >= k else 0
                assert Fraction(both, total) == 1 - 2*q + q*overlap
                clause_cases += 1
    # Polynomial/exponential comparison, checked by exact integer arithmetic.
    asymptotic_controls = []
    for c in (Fraction(1, 2), Fraction(9, 10), Fraction(99, 100)):
        n = 2
        while Fraction(1, n**7) <= c**n:
            n *= 2
        asymptotic_controls.append({'c': str(c), 'C': 7, 'n': n})
    return {
        'status': 'passed',
        'method': 'Independent output-count projection enumeration; no frozen verifier imports',
        'all_boolean_function_coalition_pairs': pair_count,
        'by_dimension': by_dimension,
        'all_support_inclusion_coalition_pairs_dimensions_0_through_3': deletion_pairs,
        'total_influence_support_deletion_counterexample': {'f_values':[0,1], 'g_values':[1,1], 'S':[0], 'U_f':'1', 'U_g':'0', 'Jplus_f':'1', 'Jplus_g':'1'},
        'exact_random_clause_joint_probability_cases': clause_cases,
        'polynomial_exponential_finite_controls': asymptotic_controls,
        'limitations': 'All computations are finite controls only. No large-n existence, fixed-exponent bound, or infinite asymptotic assertion is certified computationally.'
    }

if __name__ == '__main__':
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    Path(__file__).with_name('independent_results.json').write_text(text)
    print(text, end='')

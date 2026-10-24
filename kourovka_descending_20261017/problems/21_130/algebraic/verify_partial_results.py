#!/usr/bin/env python3
"""Independent finite checks of formulas, not proof of the full conjecture.

No third-party dependencies. This checks exact cycle probabilities and canonical
support counts, then audits every 4-subset of Z/9Z and Z/3Z x Z/3Z against the
first-moment criterion. The proof itself is in PARTIAL_RESULTS.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import factorial


def cycles(n):
    for tail in permutations(range(1, n)):
        if tail[0] < tail[-1]:
            yield (0,) + tail


def cycle_edges(order):
    return {tuple(sorted((order[i], order[(i + 1) % len(order)])))
            for i in range(len(order))}


def verify_cycle_probabilities():
    records = []
    for n in range(4, 9):
        cs = list(cycles(n))
        count = sum({(0, 1), (2, 3)} <= cycle_edges(c) for c in cs)
        observed = Fraction(count, len(cs))
        predicted = Fraction(4, (n - 1) * (n - 2))
        assert len(cs) == factorial(n - 1) // 2
        assert observed == predicted
        template = cycle_edges(tuple(range(n)))
        pairs = [(e, f) for e, f in combinations(template, 2)
                 if not set(e) & set(f)]
        assert len(pairs) == n * (n - 3) // 2
        for a in range(n):
            assert sum(a in e + f for e, f in pairs) == 2 * (n - 3)
        records.append({'n': n, 'cycles': len(cs),
                        'specified_pair_cycles': count,
                        'probability': str(observed)})
    return records


def addition(x, y, moduli):
    return tuple((a + b) % m for a, b, m in zip(x, y, moduli))


def audit_subsets(moduli, n):
    g = list(product(*(range(m) for m in moduli)))
    number = pass_first_moment = 0
    for subset in combinations(g, n):
        colors = {edge: addition(subset[edge[0]], subset[edge[1]], moduli)
                  for edge in combinations(range(n), 2)}
        multiplicities = Counter(colors.values())
        T = sum(m * (m - 1) // 2 for m in multiplicities.values())
        histogram = Counter()
        for c in cycles(n):
            counts = Counter(colors[e] for e in cycle_edges(c))
            collision_pairs = sum(m * (m - 1) // 2 for m in counts.values())
            histogram[collision_pairs] += 1
        actual_expectation = Fraction(sum(k * v for k, v in histogram.items()),
                                      sum(histogram.values()))
        assert actual_expectation == Fraction(4 * T, (n - 1) * (n - 2))
        if 4 * T < (n - 1) * (n - 2):
            assert histogram[0] > 0
            pass_first_moment += 1
        number += 1
    return {'moduli': moduli, 'n': n, 'subsets_checked': number,
            'first_moment_applicable': pass_first_moment}


if __name__ == '__main__':
    import json
    result = {'cycle_probability_checks': verify_cycle_probabilities(),
              'additive_subset_checks':
              [audit_subsets(m, 4) for m in [(9,), (3, 3)]]}
    print(json.dumps(result, indent=2))

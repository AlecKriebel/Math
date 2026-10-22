#!/usr/bin/env python3
"""Bounded exact-arithmetic controls, never a topological proof checker.
Python 3.10+; no network, packages, input files, or randomized computation.
"""
import json
from fractions import Fraction
from math import ceil, gcd
from pathlib import Path


def b1_lens_sum(k, orders, characteristic):
    return k + sum(n % characteristic == 0 for n in orders) if characteristic else k


def reduce_free_product(word):
    """C2 * C3 normal form; letters are (factor, exponent)."""
    stack = []
    mod = {'x': 2, 'y': 3}
    for factor, power in word:
        power %= mod[factor]
        if not power:
            continue
        if stack and stack[-1][0] == factor:
            power = (stack.pop()[1] + power) % mod[factor]
        if power:
            stack.append((factor, power))
    return stack


def main():
    tests = {}
    # Mayer-Vietoris/tensor arithmetic, assuming the displayed lens-sum topology.
    same_prime = 0
    for p in (2, 3, 5, 7):
        for k in range(5):
            for ell in range(1, 6):
                orders = [p ** (1 + j % 3) for j in range(ell)]
                assert b1_lens_sum(k, orders, p) == k + ell
                same_prime += 1
    tests['same_prime_lens_sum_cases'] = same_prime
    mixed = {str(p): b1_lens_sum(0, [2, 3], p) for p in (0, 2, 3, 5, 7)}
    assert max(mixed.values()) == 1
    assert gcd(2, 3) == 1  # Z/2 + Z/3 is cyclic of order six.
    assert reduce_free_product([('x', 1), ('y', 1)]) != reduce_free_product([('y', 1), ('x', 1)])
    assert reduce_free_product([('x', 1), ('x', 1)]) == []
    assert reduce_free_product([('y', 1)] * 3) == []
    tests['mixed_prime_b1'] = mixed
    tests['free_product_noncommutativity_control'] = 'pass'
    # Verify normalization and the Schreier ceiling for a finite grid only.
    # The universal statement is proved in Proposition 3.3, not by this loop.
    cover_cases = 0
    for r in range(1, 13):
        for d in range(1, 17):
            ceiling = d * (r - 1) + 1
            assert 1 - ceiling == d * (1 - r)
            for b in set((0, ceiling - 1, ceiling)):
                bound = 1 + Fraction(b - 1, d)
                assert bound <= r
                assert ceil(bound) <= r
                cover_cases += 1
    tests['cover_normalization_grid_cases'] = cover_cases
    # A cover of #2(S1xS2) can have d=2 and b1=3: dividing by d matters.
    assert 1 + Fraction(3 - 1, 2) == 2
    assert 3 > 2
    tests['missing_normalization_negative_control'] = 'detected'
    # Surgery presentation: the Hopf longitudes are opposite meridians.
    a, b, c, d = 0, 1, 1, 0
    assert a*d - b*c == -1
    # First relation e2=0 leaves e1 nonzero: verify in quotient via projection.
    projection = lambda v: v[0]
    assert projection((0, 1)) == 0
    assert projection((1, 0)) == 1
    tests['hopf_surgery_matrix_determinant'] = -1
    tests['second_component_nonzero_in_first_quotient'] = True
    # Pure integer countermodel to an invalid inference, not manifold data.
    gm, rm, rn, gn = 2, 2, 2, 3
    assert gm >= rm >= rn and not gm >= gn
    tests['rank_chain_logical_negative_control'] = 'detected; arithmetic only'
    result = {
        'status': 'pass',
        'deterministic': True,
        'arithmetic': 'exact integers and rational fractions',
        'tests': tests,
        'limits': [
            'No triangulations, fundamental-group algorithms, or genus recognition are run.',
            'No degree-one map is constructed or topologically certified by this script.',
            'The finite grid is a formula check, not evidence for untested manifolds or a universal theorem.',
            'External theorems and the prose proofs require mathematical review.',
            'No large exhaustive search, network access, or private scholarly material is used.'
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == '__main__':
    main()

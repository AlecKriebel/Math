#!/usr/bin/env python3
"""Independent finite-ring checks for the frozen partial-result audit.

Standard library only. This is a second implementation, not an import of the
packet's polynomial engine. No topological theorem is certified by this script.
"""
from itertools import product
from fractions import Fraction
import json


def convolution(a, b, modulus):
    return [sum(a[i] * b[d-i] for i in range(len(a))
                if 0 <= d-i < len(b)) % modulus
            for d in range(len(a)+len(b)-1)]


def remainder(a, b):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    while len(a) >= len(b):
        if a[-1]:
            off = len(a)-len(b)
            for j, value in enumerate(b):
                a[off+j] ^= value
        while a and a[-1] == 0:
            a.pop()
    return a


def main():
    delta = [1, -4, 8, -9, 8, -4, 1]
    target = [0] * 13
    for i, value in enumerate(delta):
        target[2*i] = value % 4
    matches = []
    mod2_candidates = 0
    possible_middle = set()
    for coeffs in product(range(4), repeat=7):
        reflected = [(-1)**i * v for i, v in enumerate(coeffs)]
        norm = convolution(coeffs, reflected, 4)
        if all((a-b) % 2 == 0 for a, b in zip(norm, target)):
            mod2_candidates += 1
            possible_middle.add(norm[6])
        if norm == target:
            matches.append(coeffs)
    assert not matches
    assert mod2_candidates == 128 and possible_middle == {1}

    reduced = [1, 0, 0, 1, 0, 0, 1]
    factors = []
    tests = 0
    for degree in (1, 2, 3):
        for lower in product((0, 1), repeat=degree):
            divisor = list(lower) + [1]
            tests += 1
            if not remainder(reduced, divisor):
                factors.append(divisor)
    assert tests == 14 and not factors

    a = Fraction(1, 4)
    assert (1-3*a+2*a*a)/(1+a)**2 == Fraction(6, 25)
    # Polynomial identity behind the angular derivative:
    # Im(conj(c)c') = 1 + 3 a cos(t) + 2 a^2.
    # The lower bound is global because -1 <= cos(t) <= 1.
    result = {
        'status': 'PASS',
        'implementation': 'independent list convolution and coefficient-list division',
        'all_degree_at_most_6_mod4_polynomials_tested': 4**7,
        'exact_norm_matches_mod4': len(matches),
        'norm_matches_mod2': mod2_candidates,
        'middle_residues_for_mod2_matches': sorted(possible_middle),
        'required_middle_residue': target[6],
        'binary_monic_trial_divisors': tests,
        'binary_divisors_found': factors,
        'angle_derivative_lower_bound': '6/25',
        'limits': [
            'The symbolic proofs establish the unrestricted integer and Laurent conclusions.',
            'Only free period 2 is tested by the displayed norm identity.',
            'No proof of fibering, the Newton classification, or the universal conjecture.'
        ]
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

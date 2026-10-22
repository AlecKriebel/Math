#!/usr/bin/env python3
"""Independent finite checks for the elementary Fourier implication.

This verifies no Gilmer-Kopparty analytic inequality. Exact graph enumeration and
rational moment checks precede double-precision finite Fourier sanity checks.
Run using Python 3.10+ with only the standard library.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb, pi, sqrt
import cmath
import json
from pathlib import Path


def triangle_numerators(n, num, den):
    edges = list(combinations(range(n), 2))
    index = {e: i for i, e in enumerate(edges)}
    triangle_masks = []
    for vertices in combinations(range(n), 3):
        mask = sum(1 << index[e] for e in combinations(vertices, 2))
        triangle_masks.append(mask)
    masses = Counter()
    for graph in range(1 << len(edges)):
        m = graph.bit_count()
        triangles = sum((graph & mask) == mask for mask in triangle_masks)
        masses[triangles] += num**m * (den - num)**(len(edges) - m)
    return masses, den**len(edges)


def run():
    errors = dict(filter=0.0, centered_reduction=0.0, coefficient_lower_bound=0.0,
                  pair_count=0.0, envelope_pairing=0.0)
    graph_states = 0
    modular_cases = 0
    residue_cases = 0
    exact_moment_cases = 0
    for n in range(3, 7):
        for num, den in ((1, 2), (2, 5)):
            masses, total = triangle_numerators(n, num, den)
            graph_states += 1 << comb(n, 2)
            assert sum(masses.values()) == total
            p = Fraction(num, den)
            mu = sum(Fraction(k * v, total) for k, v in masses.items())
            var = sum(Fraction(v, total) * (k - mu)**2 for k, v in masses.items())
            assert mu == comb(n, 3) * p**3
            assert var == comb(n, 3) * p**3 * (1 - p**3) + 12 * comb(n, 4) * p**5 * (1 - p)
            linear_var = comb(n, 2) * (n-2)**2 * p**5 * (1-p)
            remainder_var = comb(n, 3) * p**3 * (1-p)**2 * (1+2*p)
            assert var == linear_var + remainder_var
            exact_moment_cases += 1
            sigma = sqrt(float(var))
            pmf = {k: v / total for k, v in masses.items()}
            def psi(t):
                return sum(v * cmath.exp(1j * t * (k - float(mu)) / sigma)
                           for k, v in pmf.items())
            for q in range(1, 41):
                modular_cases += 1
                residues = [sum(v for k, v in masses.items() if k % q == a) / total
                            for a in range(q)]
                discrepancy = max(abs(q * v - 1) for v in residues)
                roots = [cmath.exp(2j * pi * j / q) for j in range(q)]
                coefficients = [sum(v * roots[(j * k) % q] for k, v in pmf.items())
                                for j in range(q)]
                for a in range(q):
                    residue_cases += 1
                    filtered = sum(roots[(-j * a) % q] * coefficients[j]
                                   for j in range(1, q))
                    errors['filter'] = max(errors['filter'], abs(filtered - (q * residues[a] - 1)))
                if q == 1:
                    assert discrepancy == 0
                    continue
                for j in range(1, q):
                    jstar = min(j, q - j)
                    reduced_abs = abs(psi(2 * pi * sigma * jstar / q))
                    errors['centered_reduction'] = max(errors['centered_reduction'],
                                                       abs(abs(coefficients[j]) - reduced_abs))
                errors['coefficient_lower_bound'] = max(errors['coefficient_lower_bound'],
                                                         max(0.0, abs(coefficients[1]) - discrepancy))
                multiplicities = Counter(min(j, q-j) for j in range(1, q))
                expected = {k: (1 if 2*k == q else 2) for k in range(1, q//2+1)}
                assert dict(multiplicities) == expected
                for delta in (0.01, 1.0):
                    s = 1 + delta
                    lhs = sum(min(j, q-j)**(-s) for j in range(1, q))
                    rhs = 2 * sum(k**(-s) for k in range(1, q//2+1))
                    errors['envelope_pairing'] = max(errors['envelope_pairing'], max(0.0, lhs-rhs))
    # A deliberate wrong invariant must fail: centering is not genuinely periodic.
    p = Fraction(2, 5)
    mu = float(p**3)  # n=3 triangle probability
    quasi_period_gap = abs(cmath.exp(-2j*pi*mu) - 1)
    assert quasi_period_gap > 0.1
    assert max(errors.values()) < 1e-10, errors
    return {
        'status': 'PASS',
        'enumerated_graph_states': graph_states,
        'exact_rational_mean_variance_cases': exact_moment_cases,
        'n': [3, 4, 5, 6], 'p': ['1/2', '2/5'],
        'q_range': [1, 40], 'modular_cases': modular_cases,
        'residue_cases': residue_cases, 'max_numeric_errors': errors,
        'wrong_centered_periodicity_control_gap': quasi_period_gap,
        'numeric_tolerance': 1e-10,
        'limitations': 'Finite checks test identities and normalization only; the analytic envelope is imported, not computationally certified.'
    }

if __name__ == '__main__':
    report = run()
    result_path = Path(__file__).resolve().with_name('FINITE_CONTROLS.json')
    result_path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))

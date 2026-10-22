#!/usr/bin/env python3
"""Exact finite controls for the authored proofs, using only stdlib.

This is not a formal verification of the infinite construction, analytic
regularity, or infinite-series arguments. Those are proved in PROOFS.md.
No source PDF, source text, dataset, network, or nonstdlib package is needed.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt
import json


def advance(b, c, a):
    b = b + a
    c = c + b
    return b, c


def potential_controls(seq, m):
    b = c = F(0)
    old_p = None
    good_large = 0
    for n, a in enumerate(seq, 1):
        assert 0 <= a <= n
        old_b, old_c = b, c
        b, c = advance(b, c, a)
        p = (c + m*b)/(n+m)
        if n >= 2:
            numerator = ((n-1)*old_b-old_c
                         +(n-1+m)*(m+1)*a)
            assert numerator >= 0
            assert p-old_p == numerator/F((n+m)*(n-1+m))
            assert p >= old_p
        good = a > 0 and c <= m*m*a
        if good and n >= m:
            good_large += 1
            assert p >= (1+F(1, 2*m))*old_p
            assert p <= m*m*(1+m)
            assert seq[0]*(1+F(1, 2*m))**good_large <= m*m*(1+m)
        old_p = p
    return good_large


def ratio_block(b, c, start, m, length, check_cap=True):
    q = F(m, m-1)
    for n in range(start, start+length):
        old_w = c+m*b
        a = (c+b)/(m*m-1)
        b, c = advance(b, c, a)
        assert a > 0
        assert c == m*m*a
        assert c+m*b == q*old_w
        if check_cap:
            assert a <= F(m, 6) <= n
    return b, c


def run():
    results = {}
    # Every integer N has an arbitrarily late term with r_N=2.
    spike_ratios = []
    for n in (2, 3, 10, 1000, 10**9):
        b, c = F(1), F(n-1)
        b, c = advance(b, c, F(n))
        assert c/F(n) == 2
        spike_ratios.append(n)
    results['single_spike_indices_exact_ratio_two'] = spike_ratios

    # First-order factorization is not summable even on this simple sequence.
    b, c, end = F(1), F(1), 1
    for j in range(1, 13):
        n = 2*3**(j-1)
        c += (n-end-1)*b
        b, c = advance(b, c, F(n))
        assert b/F(n) == F(3, 2)
        end = n
    results['first_order_ratio_three_halves_spikes'] = 12

    # Exhaust finite families for the exact potential identity and budget.
    total = 0
    for seed in (F(1), F(1, 2)):
        for picks in product((0, 1, 2), repeat=5):
            seq = [seed] + [F(n*p, 2) for n, p in zip(range(2, 7), picks)]
            for m in (2, 3, 4, 8):
                potential_controls(seq, m)
                total += 1
    results['exact_potential_sequence_threshold_cases'] = total

    # Sharp-count examples, with floor(log_4(m^2/16)) evaluated exactly.
    lower_blocks = []
    for m in (8, 16, 32, 64):
        h = 0
        while 16*4**(h+1) <= m*m:
            h += 1
        assert 16*4**h <= m*m < 16*4**(h+1)
        length = m*h
        assert F(m, m-1)**m <= 4
        assert F(m, m-1)**length <= F(m*m, 16)
        ratio_block(F(1), F(m-1), m, m, length)
        lower_blocks.append({'m': m, 'active_terms': length, 'ratio': m*m})
    results['sharp_count_blocks'] = lower_blocks

    # The first two genuine blocks of Theorem 1, including the zero gap.
    b, c, end = F(1), F(1), 1
    stages = []
    for j in (1, 2):
        target = 16*b*4**(2**j)
        m = max(end+1, 2, isqrt(target.numerator//target.denominator))
        while m*m < target:
            m += 1
        assert m > end and m*m >= target
        length = 2**j*m
        c += (m-end-1)*b
        assert c < m*b
        b, c = ratio_block(b, c, m, m, length)
        assert F(length, 2**j*m) == 1
        end = m+length-1
        stages.append({'stage': j, 'm': m, 'active_terms': length,
                       'ratio': m*m, 'mass_coefficient_before_exp_minus_one': 1})
    results['counterexample_exact_prefix_blocks'] = stages
    results['geometric_gaussian_weight_sum_first_two'] = '3/4'
    assert sum((F(1, 2**j) for j in (1, 2)), F(0)) == F(3, 4)

    # Negative control: replacing m^2-1 by m^2 changes the target ratio.
    m, b, c = 16, F(1), F(15)
    wrong_a = (c+b)/(m*m)
    wrong_b, wrong_c = advance(b, c, wrong_a)
    assert wrong_c/wrong_a == m*m+1
    assert wrong_c != m*m*wrong_a
    results['wrong_denominator_control_detected'] = True

    # Negative control: a too-small m cannot support arbitrary old mass.
    m, b, c = 2, F(100), F(100)
    wrong_a = (c+b)/(m*m-1)
    assert wrong_a > m
    results['missing_mass_cap_control_detected'] = True
    results['status'] = 'all_exact_finite_controls_passed'
    results['limits'] = ('Finite rational controls only; the infinite and analytic '
                         'claims require the written proofs.')
    return results


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

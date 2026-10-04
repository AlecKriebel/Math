#!/usr/bin/env python3
"""Exact finite checks of the influence-normalization bridge; not a proof of BKK."""
from fractions import Fraction
import json
from pathlib import Path


def fibers(n, subset):
    groups = {}
    outside = ((1 << n) - 1) ^ subset
    for x in range(1 << n):
        u = x & outside
        groups[u] = groups.get(u, 0) | (1 << x)
    return tuple(groups.values())


def counts(truth, partition):
    reach_one = reach_zero = undetermined = 0
    for fiber in partition:
        selected = truth & fiber
        one = bool(selected)
        zero = selected != fiber
        reach_one += one
        reach_zero += zero
        undetermined += one and zero
    return undetermined, reach_one, reach_zero, len(partition)


def run():
    checked = 0
    by_n = []
    for n in range(5):
        parts = [fibers(n, subset) for subset in range(1 << n)]
        number_functions = 1 << (1 << n)
        total_pairs = 0
        for truth in range(number_functions):
            rows = [counts(truth, part) for part in parts]
            for subset, (und, one, zero, den) in enumerate(rows):
                assert und == one + zero - den
                assert 0 <= und <= one <= den
                assert 0 <= und <= zero <= den
                # The paper's I^+ + I^- equals the undetermined probability.
                # Multiplication by 2^n * den avoids all rounding.
                ones_total = truth.bit_count()
                ip_scaled = one * (1 << n) - ones_total * den
                im_scaled = zero * (1 << n) - ((1 << n) - ones_total) * den
                assert ip_scaled + im_scaled == und * (1 << n)
                assert ip_scaled >= 0 and im_scaled >= 0
                for bit in range(n):
                    larger = subset | (1 << bit)
                    u2, p2, m2, d2 = rows[larger]
                    assert one * d2 <= p2 * den
                    assert zero * d2 <= m2 * den
                    assert und * d2 <= u2 * den
                total_pairs += 1
        checked += total_pairs
        by_n.append({'n': n, 'functions': number_functions, 'pairs': total_pairs})

    # Explicit controls distinguish total influence, one-sided reachability,
    # and shifted one-sided influence.
    majority3 = sum(1 << x for x in range(8) if x.bit_count() >= 2)
    u, p, m, d = counts(majority3, fibers(3, 1))
    assert (Fraction(u,d), Fraction(p,d), Fraction(m,d)) == (Fraction(1,2), Fraction(3,4), Fraction(3,4))
    assert Fraction(p,d) - Fraction(1,2) == Fraction(1,4)
    c = Fraction(1,2)
    assert Fraction(1,64**6) > c**64
    # A whole infinite subsequence: for n=2^m and m>=6, 2^m>6m.
    # Base m=6 is checked; the inductive step follows from
    # 2^(m+1)>12m>=6(m+1), since m>=1.
    assert 2**6 > 6*6
    result = {
        'status': 'passed',
        'scope': 'Finite exact controls of definitions, identities, and inequality direction only; the infinite counterexample is the cited theorem.',
        'by_dimension': by_n,
        'function_coalition_pairs': checked,
        'identities': ['U=Jplus+Jminus-1', 'U<=Jplus', 'U<=Jminus', 'Iplus+Iminus=U'],
        'coalition_monotonicity': ['U', 'Jplus', 'Jminus'],
        'majority3_singleton': {'U': '1/2', 'Jplus': '3/4', 'Jminus': '3/4', 'Iplus': '1/4'},
        'polynomial_exponential_control': {'n': 64, 'C': 6, 'c': '1/2', 'inequality': 'n^(-C)>c^n'},
    }
    return result

if __name__ == '__main__':
    text = json.dumps(run(), indent=2, sort_keys=True) + '\n'
    Path(__file__).with_name('control_results.json').write_text(text)
    print(text, end='')

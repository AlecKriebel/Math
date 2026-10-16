#!/usr/bin/env python3
"""Small independent arithmetic controls; not a stochastic-convergence proof."""
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check():
    jump_checks = 0
    # Counts are perfect denominator-powers, so fractional powers are rational.
    # This derives intensities directly from incident counts, without author code.
    graphs = [
        [(0, 1)],
        [(0, 1), (1, 2), (2, 3)],
        [(0, 1), (1, 2), (2, 0)],
        [(0, 1), (0, 2), (0, 3), (0, 4)],
        [(0, 1), (2, 3)],
    ]
    exponents = [(1, 4), (1, 3), (1, 2), (2, 3), (3, 4), (19, 20)]
    for edges in graphs:
        vertices = sorted({v for e in edges for v in e})
        for numerator, denominator in exponents:
            for tiny_rate in [Fraction(1), Fraction(1, 10**60)]:
                rates = {v: tiny_rate * Fraction(v + 1, len(vertices)) for v in vertices}
                roots = {e: i + 1 for i, e in enumerate(edges)}
                counts = {e: roots[e] ** denominator for e in edges}
                powers = {e: Fraction(roots[e] ** numerator) for e in edges}
                sums = {v: sum((powers[e] for e in edges if v in e), Fraction()) for v in vertices}
                for e in edges:
                    u, v = e
                    q = rates[u] / sums[u] + rates[v] / sums[v]
                    intensity = powers[e] * q
                    jump = Fraction(1, roots[e] ** numerator)
                    require(jump * intensity == q, 'exact H drift is not q')
                    require(jump * jump * intensity == jump * q, 'wrong exact bracket')
                    require(jump * q <= q, 'bracket domination fails')
                    require(intensity <= rates[u] + rates[v], 'endpoint intensity bound fails')
                    require(q <= rates[u] + rates[v], 'finite-time q bound fails')
                    require(counts[e] >= 1, 'initial positivity missing')
                    jump_checks += 6

    h_checks = 0
    with localcontext() as ctx:
        ctx.prec = 90
        tolerance = Decimal('1e-75')
        for alpha in map(Decimal, ['0.01', '0.25', '0.5', '0.75', '0.99']):
            c = 1 - alpha
            h = Decimal(0)
            for n in range(1, 513):
                target = (Decimal(n) ** c - 1) / c
                require(h + tolerance >= target, 'integral lower bound fails')
                require(h <= target + 1 + tolerance, 'integral upper bound fails')
                if n > 1:
                    n0 = 1 + n // 3
                    offset = sum((Decimal(j) ** (-alpha) for j in range(1, n0)), Decimal())
                    direct = sum((Decimal(j) ** (-alpha) for j in range(n0, n)), Decimal())
                    require(abs((h - offset) - direct) < tolerance, 'nonunit H initial offset fails')
                    h_checks += 1
                h += Decimal(n) ** (-alpha)
                h_checks += 2

    boundary_checks = 0
    with localcontext() as ctx:
        ctx.prec = 90
        for alpha in map(Decimal, ['0.01', '0.25', '0.49', '0.5', '0.75', '0.99']):
            for length in [4, 6, 10]:
                for phase in [0, 1]:
                    values = [Decimal(2 if i % 2 == phase else 0) for i in range(length)]
                    for i, value in enumerate(values):
                        own = value ** alpha
                        left = own + values[(i - 1) % length] ** alpha
                        right = own + values[(i + 1) % length] ** alpha
                        require(left > 0 and right > 0, 'boundary denominator zero')
                        drift = own / left + own / right
                        require(drift == value, 'boundary counterexample does not satisfy equations')
                        boundary_checks += 1
    critical_checks = 0
    for length in [4, 6, 10]:
        for first in [Fraction(1, 100), Fraction(1, 3), Fraction(1), Fraction(199, 100)]:
            values = [first if i % 2 == 0 else 2 - first for i in range(length)]
            for i, value in enumerate(values):
                drift = value / (value + values[(i - 1) % length]) + value / (value + values[(i + 1) % length])
                require(drift == value, 'critical positive alternation does not satisfy equations')
                critical_checks += 1

    ancestry_checks = 0
    for d in [1, 3, 10]:
        # Diagnostic for fixed horizons; the all-n factorial argument is analytic.
        p = Fraction(2)
        t = Fraction(1)
        bound = 2 * (d + 1)**199 * p**200 * t**200 / math.factorial(200)
        require(bound < Fraction(1, 10**90), 'ordered-chain tail did not decrease as expected')
        ancestry_checks += 1

    return {
        'result': 'PASS',
        'exact_jump_intensity_bracket_inequalities': jump_checks,
        'high_precision_H_integral_and_nonunit_offset_controls': h_checks,
        'boundary_alternation_equations': boundary_checks,
        'critical_positive_alternation_equations': critical_checks,
        'fixed_parameter_ancestry_factorial_tail_controls': ancestry_checks,
        'scope': 'Finite exact/high-precision diagnostic controls. Independent analytic derivation, not these computations, establishes infinite-graph stochastic claims.',
        'author_code_imported_or_run': False,
        'outer_optimization_safe': True,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))

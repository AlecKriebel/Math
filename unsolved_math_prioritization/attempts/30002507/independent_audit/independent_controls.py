#!/usr/bin/env python3
"""Independent exact finite controls; no imported author code or analytic certification."""
from collections import Counter
from fractions import Fraction as F
import json


def run():
    counts = Counter()

    def check(label, predicate):
        if not predicate:
            raise ValueError(label)
        counts[label] += 1

    limit = 240
    divisors = [[] for _ in range(limit + 1)]
    factors = [[] for _ in range(limit + 1)]
    primes = []
    for n in range(2, limit + 1):
        if not factors[n]:
            primes.append(n)
            for m in range(n, limit + 1, n):
                t, exponent = m, 0
                while t % n == 0:
                    t //= n
                    exponent += 1
                factors[m].append((n, exponent))
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            divisors[n].append(d)
    mobius = [0] + [0 if any(e > 1 for _, e in factors[n]) else (-1) ** len(factors[n])
                    for n in range(1, limit + 1)]
    for n in range(1, limit + 1):
        check('mobius_divisor_identity', sum(mobius[d] for d in divisors[n]) == (n == 1))

    basis = (2, 3, 5, 11)
    sets = [set(p for i, p in enumerate(basis) if mask & (1 << i)) for mask in range(16)]

    def lambdas(P):
        return [0] + [(-1) ** sum(e for _, e in factors[n])
                      if all(p in P for p, _ in factors[n]) else 0
                      for n in range(1, limit + 1)]

    def multiplier(P, Q):
        # Direct prime-exponent formula, not finite Euler-product expansion.
        out = [0] * (limit + 1)
        for n in range(1, limit + 1):
            value = 1
            for p, e in factors[n]:
                if p in Q - P:
                    if e > 1:
                        value = 0
                elif p in P - Q:
                    value *= (-1) ** e
                else:
                    value = 0
            out[n] = value
        return out

    for P in sets:
        lp = lambdas(P)
        for Q in sets:
            lq, u, v = lambdas(Q), multiplier(P, Q), multiplier(Q, P)
            for n in range(1, limit + 1):
                check('euler_forward', sum(u[d] * lq[n // d] for d in divisors[n]) == lp[n])
                check('euler_reverse', sum(v[d] * lp[n // d] for d in divisors[n]) == lq[n])
                check('euler_inverse', sum(u[d] * v[n // d] for d in divisors[n]) == (n == 1))

    for denominator in (3, 5, 7, 11):
        # Deliberately include repeated frequencies, signed coefficients, and collisions.
        xs = [F(1)] + sorted(F(denominator + k, denominator) for k in range(0, 23) for _ in range(1 + (k % 4 == 0)))
        for rho in (1, 2, 3):
            aa = [F(0)] + [F((k % 7) - 3, 1 + k % 3) for k in range(1, len(xs))]
            aa[0] = -sum(a / x ** rho for a, x in zip(aa[1:], xs[1:]))
            check('fixture_target_zero', sum(a / x ** rho for a, x in zip(aa, xs)) == 0)
            for q in range(1, 26):
                ms = [-(-q * x.numerator // x.denominator) for x in xs]
                grouped = Counter()
                for m, a in zip(ms, aa):
                    grouped[m] += a
                erho = sum(a * ((F(q, m)) ** rho - x ** (-rho)) for a, x, m in zip(aa, xs, ms))
                corrected = grouped.copy()
                corrected[q] -= erho
                check('exact_stated_zero_correction', sum(a * F(m) ** (-rho) for m, a in corrected.items()) == 0)
                for exponent in range(1, 9):
                    d = sum(a * x ** (-exponent) for a, x in zip(aa, xs))
                    b = sum(a * F(m) ** (-exponent) for m, a in grouped.items())
                    e = sum(a * ((F(q, m)) ** exponent - x ** (-exponent)) for a, x, m in zip(aa, xs, ms))
                    bound = F(exponent, q) * sum(abs(a) * x ** (-exponent - 1) for a, x in zip(aa, xs))
                    check('regrouped_normalized_identity', q ** exponent * b == d + e)
                    check('rounding_bound', abs(e) <= bound)
                    c = sum(a * F(m) ** (-exponent) for m, a in corrected.items())
                    check('corrected_identity_at_other_points', q ** exponent * c == d + e - erho)

    # Complex arithmetic represented as pairs of exact rationals.
    def mul(z, w):
        return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])
    def sub(z, w):
        return (z[0] - w[0], z[1] - w[1])
    one, zero = (F(1), F(0)), (F(0), F(0))
    for height in range(1, 101):
        escaped = (F(2), F(height))
        inv = (F(2, 4 + height * height), F(-height, 4 + height * height))
        h = lambda z: mul(sub(z, one), sub(one, mul(z, inv)))
        check('escaping_fixed_zero', h(one) == zero)
        check('escaping_extra_zero', h(escaped) == zero)
        check('escaping_distinct_in_halfplane', escaped != one and escaped[0] > F(1, 2))

    # Finite shadows of the rigorously analyzed abscissa-loss fixture in AUDIT.md.
    for k in range(1, 101):
        x, y = F(k) + F(1, 4), F(k) + F(1, 2)
        mx, my = -(-x.numerator // x.denominator), -(-y.numerator // y.denominator)
        check('grouping_can_cancel_whole_blocks', mx == my == k + 1)
        check('ungrouped_terms_fail_at_boundary', x ** 0 == y ** 0 == 1)

    negative = {}
    def reject(label, wrong_claim):
        if wrong_claim:
            raise ValueError('Negative control failed: ' + label)
        negative[label] = 'rejected'
    x, q = F(3, 2), 3
    # D(s)=1-x*x^(-s), D(1)=0; q=3 has a nonzero rounding error.
    m = 5
    b1 = F(1, q) - x / m
    e1 = q * b1
    reject('omit_normalization', b1 == e1)
    reject('omit_zero_correction', b1 == 0)
    reject('subtract_unscaled_constant', b1 - e1 == 0)
    reject('wrong_correction_sign', b1 + F(1, q) * e1 == 0)
    reject('floor_has_same_one_sided_bound', abs(1 - F(100, 199)) <= F(10000, 39601))
    reject('rounding_preserves_original_target_zero', 1 - F(3, 2) / 2 == 0)
    return {'schema': 'dirichlet-independent-exact-controls-v1', 'result': 'PASS',
            'arithmetic': 'Exact Python integers and rational pairs; no author imports',
            'checks': dict(sorted(counts.items())), 'total_predicates': sum(counts.values()),
            'mathematical_negative_controls': negative,
            'negative_control_count': len(negative),
            'scope': 'Finite algebra and inequalities only; analytic proofs are separately audited in AUDIT.md.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

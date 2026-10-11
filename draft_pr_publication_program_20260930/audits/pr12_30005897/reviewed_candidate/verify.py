#!/usr/bin/env python3
"""Exact, bounded checks for the indexing and finite models in PROOF.md.

These checks do not certify an infinite-dimensional theorem.  All arithmetic
is rational; the source proof, including measurability and uniformity, still
requires independent mathematical review.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


checks = {}


def pow2(n):
    return F(2) ** n


def check_band_models():
    count = 0
    comparisons = 0
    for d in range(1, 7):
        for seed in range(12):
            cuts = [((seed + 3 * r) % 7) - 3 for r in range(d)]
            offsets = [((2 * seed + r) % 5) - 2 for r in range(d)]

            def rho(n):
                q, r = divmod(n, d)
                return pow2(-abs(q - cuts[r]) + offsets[r])

            # Work far inside a padded interval. The checks below are finite.
            lo, hi = -25 * d, 25 * d

            def A0(n):
                return rho(n - d) <= rho(n) / 2

            def A(n):
                return all(A0(n + j) for j in range(d))

            # p-th powers of the operator-condition-number bounds; the
            # densities encode all p simultaneously without taking roots.
            Dp = max(
                max(rho(n - j) / rho(n) for n in range(lo, hi + 1))
                * max(rho(n + j) / rho(n) for n in range(lo, hi + 1))
                for j in range(d)
            )
            for n in range(-12 * d, 12 * d + 1):
                assert min(rho(n - d), rho(n + d)) <= rho(n) / 2
                if A0(n):
                    assert A0(n - d)
                else:
                    assert not A0(n + d)
                if A(n):
                    assert A(n - 1)
                else:
                    assert not A(n + 1)
                assert (not A(n)) == any(not A0(n + j) for j in range(d))
                for m in range(9):
                    if A(n):
                        assert rho(n - m * d) / rho(n) <= F(1, 2) ** m
                    else:
                        assert rho(n + m * d) / rho(n) <= Dp * F(1, 2) ** m
                    comparisons += 1
            count += 1

    # Empty stable or unstable bands are allowed and occur here.
    for direction in (-1, 1):
        for d in range(1, 7):
            rho = lambda n: pow2(direction * n)
            stable = lambda n: rho(n - d) <= rho(n) / 2
            for n in range(-20, 21):
                assert stable(n) == (direction == 1)
                assert min(rho(n - d), rho(n + d)) <= rho(n) / 2
                comparisons += 1
            count += 1
    checks['band_models'] = {'models': count, 'exact_comparisons': comparisons}


def check_scalar_propagation():
    # Every five-term positive sequence chosen from these seven exact values.
    # Check the local implication whenever its full hypotheses are available.
    count = 0
    values = [pow2(n) for n in range(-3, 4)]
    for seq in product(values, repeat=5):
        condition = all(min(seq[i - 1], seq[i + 1]) <= seq[i] / 2
                        for i in (1, 2, 3))
        if not condition:
            continue
        stable = lambda i: seq[i - 1] <= seq[i] / 2
        if stable(2):
            assert stable(1)
        else:
            assert not stable(3)
        count += 1
    checks['scalar_propagation'] = {'admissible_five_term_sequences': count}


def check_telescoping():
    # Finite rational test of sum u_j(y_{j+1}-Ay_j)
    # = sum (u_{j-1}-A* u_j)(y_j), including both boundary terms.
    A = ((F(2), F(1)), (F(0), F(1, 2)))
    zero = (F(0), F(0))
    mv = lambda M, x: tuple(sum(M[i][j] * x[j] for j in range(2)) for i in range(2))
    sub = lambda x, y: tuple(x[i] - y[i] for i in range(2))
    dot = lambda x, y: sum(x[i] * y[i] for i in range(2))
    At = tuple(tuple(A[j][i] for j in range(2)) for i in range(2))
    tests = 0
    for seed in range(30):
        u = {j: (F(seed + j, 3), F(seed - 2 * j, 5)) for j in range(-3, 4)}
        y = {j: (F(seed + j * j, 7), F(seed - j, 11)) for j in range(-4, 6)}
        lhs = sum(dot(u[j], sub(y[j + 1], mv(A, y[j]))) for j in u)
        rhs = sum(dot(sub(u.get(j - 1, zero), mv(At, u.get(j, zero))), y[j])
                  for j in range(-3, 5))
        assert lhs == rhs
        tests += 1
    checks['dual_telescoping'] = {'exact_rational_tests': tests}


def clean(v):
    return {n: x for n, x in v.items() if x}


def add(*vs):
    ans = {}
    for v in vs:
        for n, x in v.items():
            ans[n] = ans.get(n, F(0)) + x
    return clean(ans)


def scale(v, c):
    return clean({n: c * x for n, x in v.items()})


def B(v):
    # p=1, rho_n=2^{-|n|}; backward-shift coefficient at output n.
    return {n - 1: x * pow2(abs(n) - abs(n - 1)) for n, x in v.items()}


def Binv(v):
    return {n + 1: x * pow2(abs(n) - abs(n + 1)) for n, x in v.items()}


def iterate(fun, v, k):
    for _ in range(k):
        v = fun(v)
    return v


def check_green_identity():
    P = lambda v: {n: x for n, x in v.items() if n <= 0}
    Q = lambda v: {n: x for n, x in v.items() if n > 0}
    # This splitting is generalized: the two projections do NOT both
    # commute with B. The test must not silently replace it by a diagonal one.
    probe = {1: F(1)}
    assert P(B(probe)) != B(P(probe))
    forcing = {t: {-2: F(t + 4, 3), 1: F(7 - t, 5), 3: F(t * t, 11)}
               for t in range(-3, 4)}

    def y(n):
        terms = []
        for t, b in forcing.items():
            if t <= n - 1:
                terms.append(iterate(B, P(b), n - 1 - t))
            if t >= n:
                terms.append(scale(iterate(Binv, Q(b), t - n + 1), -1))
        return add(*terms)

    for n in range(-15, 16):
        assert y(n + 1) == add(B(y(n)), forcing.get(n, {}))
    checks['green_identity'] = {'time_indices_checked': 31,
                                'noncommuting_projection_control': 'passed'}


def check_controls():
    failures = 0
    # Identity and a valley have the wrong density geometry.
    for d in range(1, 11):
        assert not min(F(1), F(1)) <= F(1, 2)
        assert not min(pow2(abs(-d)), pow2(abs(d))) <= F(1, 2)
        failures += 2
    # The positive constant-mass tail in prior Example 6.2 fails the new
    # criterion while its aggregate level masses have HC ratio exactly 2^-d.
    for d in range(1, 11):
        n = d + 2
        bad_rho = lambda j: F(1) if j >= 1 else pow2(j - 1)
        assert min(bad_rho(n - d), bad_rho(n + d)) > bad_rho(n) / 2
        assert pow2(n) / pow2(n + d) == pow2(-d)
        failures += 1
    checks['negative_controls'] = {'rejected_cases': failures}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: assertions perform the exact checks.')
    check_band_models()
    check_scalar_propagation()
    check_telescoping()
    check_green_identity()
    check_controls()
    result = {'status': 'passed',
              'arithmetic': 'Python standard-library fractions.Fraction',
              'scope': 'Finite algebra/index/support tests; not a proof certificate',
              'checks': checks}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

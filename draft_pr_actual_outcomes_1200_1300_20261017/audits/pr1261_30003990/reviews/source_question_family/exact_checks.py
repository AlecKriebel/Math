#!/usr/bin/env python3
"""Exact supplementary checks for the independent source-question derivation.

Uses only Python's standard library. No SDP, floating-point integration, source
fetching, candidate material, or repository operations. Writes exact_results.json
beside this file. These finite checks supplement, and do not replace, the proof.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return trim([c * x for x in a])


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def power(a, k):
    result = [F(1)]
    for _ in range(k):
        result = mul(result, a)
    return result


def kernel_binomial(m):
    assert m % 2 == 1 and m >= 1
    s = (m - 1) // 2
    result = [F(0)]
    for j in range(s + 1):
        term = [F(0)] * j + scale(
            power([F(1), F(-1)], s - j),
            F((-1) ** j * comb(m, 2 * j + 1), m))
        result = add(result, term)
    return result


def kernel_recurrence(m):
    """Independent sin((2s+1)theta)/sin(theta) recurrence."""
    s = (m - 1) // 2
    if s == 0:
        return [F(1)]
    previous, current = [F(1)], [F(3), F(-4)]
    for _ in range(1, s):
        previous, current = current, add(
            mul([F(2), F(-4)], current), scale(previous, F(-1)))
    return scale(current, F(1, m))


def rational(a):
    return f"{a.numerator}/{a.denominator}"


def cone_moment(q, n, power_t):
    # Pushforward of n-dimensional simplex by sum coordinates has density
    # n*t**(n-1) on [0,1]. The common factor n cancels in the ratio.
    return sum((c * F(1, j + n + power_t)
                for j, c in enumerate(q)), F(0))


def badd(a, b):
    out = dict(a)
    for monomial, coefficient in b.items():
        out[monomial] = out.get(monomial, F(0)) + coefficient
    return {ij: c for ij, c in out.items() if c}


def bscale(a, c):
    return {ij: c * coefficient for ij, coefficient in a.items()
            if c * coefficient}


def bmul(a, b):
    out = {}
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            key = (i + k, j + l)
            out[key] = out.get(key, F(0)) + c * d
    return {ij: c for ij, c in out.items() if c}


def bpower(a, k):
    out = {(0, 0): F(1)}
    for _ in range(k):
        out = bmul(out, a)
    return out


def compose(a, b):
    out = {}
    for c in reversed(a):
        out = badd(bmul(out, b), {(0, 0): c})
    return out


def triangle_integral(a):
    # Integral x**i*y**j over x,y >= 0, x+y <= 1.
    return sum((c * F(factorial(i) * factorial(j), factorial(i + j + 2))
                for (i, j), c in a.items()), F(0))


def degree(a):
    return max((i + j for i, j in a), default=0)


def main():
    identities = []
    for m in range(1, 66, 2):
        a, b = kernel_binomial(m), kernel_recurrence(m)
        assert a == b
        assert len(a) - 1 == (m - 1) // 2
        assert a[0] == 1
        # At t=1 the quotient equals (-1)**((m-1)/2)/m.
        assert sum(a) == F((-1) ** ((m - 1) // 2), m)
        identities.append(m)

    budgets = 0
    for n in range(1, 41):
        k = n + 2
        for r in range(1, 501):
            s = r // (2 * k)
            m = 2 * s + 1
            assert 4 * k * s <= 2 * r
            assert m * 2 * k >= r
            budgets += 1

    cone_results = []
    for n in (1, 2, 3, 6):
        k = n + 2
        A = 1 + 2 ** (3 * n + 6)
        for m in (1, 3, 5, 9, 17):
            q = power(kernel_binomial(m), 2 * k)
            denominator = cone_moment(q, n, 0)
            numerator = cone_moment(q, n, 1)
            assert denominator > 0 and numerator > 0
            mean = numerator / denominator
            assert mean <= F(A * 4 ** k, 4 * m * m)
            cone_results.append({
                "n": n, "m": m, "k": k, "q_degree_in_t": len(q) - 1,
                "mean_t_exact": rational(mean),
                "m_squared_mean_t_exact": rational(m * m * mean),
                "mean_t_decimal_for_readability": float(mean),
                "analytic_bound_check": "PASS"})

    # Nonconvex objective, two boundary minimizers, nonsmooth triangle.
    # f = x + y^2(1-y)^2; a=(0,0); ||Hf|| <= 2 on the triangle.
    # M=2; g=x+2(x^2+y^2); max_K g=3, so t=g/3.
    f = {(1, 0): F(1), (0, 2): F(1), (0, 3): F(-2), (0, 4): F(1)}
    t = {(1, 0): F(1, 3), (2, 0): F(2, 3), (0, 2): F(2, 3)}
    triangle_results = []
    n, k, B = 2, 4, F(3)
    C = B * k * k * 4 ** k * (1 + 2 ** (3 * n + 6))
    for r in (1, 7, 8, 15, 16, 24):
        s, m = r // (2 * k), 2 * (r // (2 * k)) + 1
        p = bpower(compose(kernel_binomial(m), t), k)
        q = bmul(p, p)
        assert degree(q) == 4 * k * s
        assert degree(q) <= 2 * r
        denominator = triangle_integral(q)
        numerator = triangle_integral(bmul(f, q))
        surrogate = B * triangle_integral(bmul(t, q))
        assert denominator > 0 and numerator > 0
        assert numerator <= surrogate
        mean = numerator / denominator
        assert mean <= C / (r * r)
        triangle_results.append({
            "r": r, "m": m, "q_degree": degree(q),
            "normalizer_exact": rational(denominator),
            "objective_gap_exact": rational(mean),
            "objective_gap_decimal_for_readability": float(mean),
            "surrogate_domination_and_bound_checks": "PASS"})

    output = {
        "status": "ALL EXACT ASSERTIONS PASSED",
        "arithmetic": "Python standard-library fractions.Fraction; floats only in display fields",
        "kernel_identity_odd_m_tested": identities,
        "degree_budget_integer_pairs_tested": budgets,
        "cone_exact_moment_checks": cone_results,
        "nonconvex_triangle_checks": triangle_results,
        "limitations": "Finite supplementary computations; general theorem rests on analytic proof. No numerical SDP."}
    path = Path(__file__).with_name('exact_results.json')
    path.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(output['status'])
    print(f"Kernel identities: {len(identities)}; all-order budget samples: {budgets}; "
          f"cone moments: {len(cone_results)}; triangle examples: {len(triangle_results)}")


if __name__ == '__main__':
    main()

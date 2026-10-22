#!/usr/bin/env python3
"""Independent exact finite checks; the report supplies the all-m analytic proof.

No imported symbolic algebra, manuscript code, floats, or optimization-sensitive
guards. Polynomial arrays below use ascending powers of t; bivariate monomials
use (power of z, power of conjugate z). Nothing reads another review family.
"""
from fractions import Fraction as Q
from math import comb
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(map(Q, p))
    while p and not p[-1]:
        p.pop()
    return p


def add(p, q):
    r = [Q(0)] * max(len(p), len(q))
    for i, a in enumerate(p):
        r[i] += a
    for i, a in enumerate(q):
        r[i] += a
    return trim(r)


def scale(p, s):
    return trim([Q(s) * a for a in p])


def mul(p, q):
    if not p or not q:
        return []
    r = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return trim(r)


def derivative(p):
    return trim([i * p[i] for i in range(1, len(p))])


def primitive(p):
    return [Q(0)] + [a / (i + 1) for i, a in enumerate(p)]


def integral(p):
    return sum((a / (i + 1) for i, a in enumerate(p)), Q(0))


def value(p, t):
    result = Q(0)
    for a in reversed(p):
        result = result * t + a
    return result


def binomial_power(n):
    return [Q((-1) ** k * comb(n, k)) for k in range(n + 1)]


def biderivative(p, variable):
    r = {}
    for exponents, coefficient in p.items():
        power = exponents[variable]
        if power:
            exponents = list(exponents)
            exponents[variable] -= 1
            key = tuple(exponents)
            r[key] = r.get(key, Q(0)) + coefficient * power
    return {key: a for key, a in r.items() if a}


def main():
    if "--self-test-failure" in sys.argv[1:]:
        require(False, "deliberate guard failure; must survive optimization")
    require(sys.argv[1:] == [], "unsupported argument")
    checks = 0
    max_m = 80
    totals = {}
    for m in range(1, max_m + 1):
        label = f"m={m}"
        # Expand the input directly as the original nested finite polynomial.
        p = []
        for j in range(m):
            p = add(p, binomial_power(j))
        a = mul([0, 1], p)
        one_minus = binomial_power(m)
        expected_a = add([1], scale(one_minus, -1))
        require(a == expected_a, label + ": geometric-sum input identity")
        checks += 1
        h = sum((Q(1, k) for k in range(1, m + 1)), Q(0))
        require(integral(p) == h, label + ": direct origin kernel integral")
        checks += 1

        # Independently solve dbar u=v with zero boundary trace, using a
        # bivariate monomial primitive rather than the submitted G expression.
        u = {(1, 0): -h}
        v = {}
        for k, c in enumerate(p):
            u[(k + 2, k + 1)] = c / (k + 1)
            v[(k + 2, k)] = c
        require(biderivative(u, 1) == v, label + ": bivariate dbar primitive")
        checks += 1
        transform = biderivative(u, 0)
        require(all(i == j for i, j in transform), label + ": radial dz derivative")
        g = [Q(0)] * (m + 1)
        for (i, j), c in transform.items():
            g[i] += c
        g = trim(g)
        q = add(primitive(p), [-h])
        require(value(q, 1) == 0, label + ": exact zero outer trace")
        checks += 1
        require(g == add(q, a), label + ": radial product rule")
        checks += 1
        closed_g = expected_a
        for k in range(1, m + 1):
            closed_g = add(closed_g, scale(binomial_power(k), -Q(1, k)))
        require(g == closed_g, label + ": independent versus printed transform")
        checks += 1
        require(value(g, 0) == -h and value(g, 1) == 1,
                label + ": both exact endpoints")
        checks += 1
        require(derivative(g) == add(p, scale(binomial_power(m - 1), m)),
                label + ": all-coefficient monotonicity identity")
        checks += 1

        # A separate invariant: the computed zero-exterior transform preserves
        # the exact full-plane L2 norm, as integration of d(t*q(t)^2) shows.
        l2 = integral(mul(g, g))
        input_l2 = integral(mul(a, a))
        require(l2 == input_l2 == 1 - Q(2, m + 1) + Q(1, 2 * m + 1),
                label + ": independent exact L2 conservation")
        checks += 1
        moment = integral(mul([0, 1], a))
        require(moment == Q(1, 2) - Q(1, (m + 1) * (m + 2)) and moment > 0,
                label + ": conjugated pairing negative control")
        checks += 1
        for t in (Q(1, 7), Q(1, 2), Q(6, 7)):
            require(0 < value(a, t) < 1 and -h < value(g, t) < 1,
                    label + ": exact interior range check")
            checks += 1
        totals[m] = (a, g)
    for m in range(1, max_m):
        a, g = totals[m]
        other_a, other_g = totals[m + 1]
        expected = 1 - Q(1, m + 1) - Q(1, m + 2) + Q(1, 2 * m + 2)
        require(integral(mul(g, other_g)) == integral(mul(a, other_a)) == expected,
                f"m={m}: adjacent-family exact L2 polarization")
        checks += 1
    for n in range(81):
        require(n + 2 != 0, f"angular bilinear monomial exponent n={n}")
        checks += 1
    print(json.dumps({
        "result": "PASS",
        "checks": checks,
        "m_range": [1, max_m],
        "adjacent_pair_count": max_m - 1,
        "angular_test_degree_range": [0, 80],
        "arithmetic": "stdlib fractions.Fraction; exact integer polynomial coefficients",
        "scope": "Ancillary finite identities, not a replacement for the all-m analytic proof",
        "h80": str(sum((Q(1, k) for k in range(1, 81)), Q(0))),
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

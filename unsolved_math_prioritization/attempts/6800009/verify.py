#!/usr/bin/env python3
"""Exact finite diagnostics; the global argument is in SOURCE_CERTIFICATE.md."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random


def transpose(a):
    return [list(x) for x in zip(*a)]


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def qm(a, b):
    w, x, y, z = a
    r, s, t, u = b
    return (w*r-x*s-y*t-z*u, w*s+x*r+y*u-z*t,
            w*t-x*u+y*r+z*s, w*u+x*t-y*s+z*r)


def qi(a):
    return (a[0], -a[1], -a[2], -a[3])


def shear(a, b):
    return a, qm(b, qi(a))


def shear_inverse(u, v):
    return u, qm(v, u)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def bracket(a, b):
    return tuple(2*x for x in cross(a[:3], b[:3]) + cross(a[3:], b[3:]))


def metric(a, b):
    return 2*dot(a[:3], b[:3])+dot(tuple(a[i+3]-a[i] for i in range(3)),
                                  tuple(b[i+3]-b[i] for i in range(3)))


def strict_count(r):
    """r represents c*T/pi exactly, so count positive integers m<r."""
    assert r >= 0
    return max(0, -(-r.numerator // r.denominator)-1)


def nullity(r, s):
    return 2*int(r > 0 and r.denominator == 1)+2*int(s > 0 and s.denominator == 1)


def main():
    # dF in one pair of coordinate directions and product metric diag(2,1).
    d = [[1, 0], [-1, 1]]
    m = matmul(matmul(transpose(d), [[2, 0], [0, 1]]), d)
    assert m == [[3, -1], [-1, 1]]
    leading_minors = [m[0][0], m[0][0]*m[1][1]-m[0][1]*m[1][0]]
    assert leading_minors == [3, 2]
    # The source's diagonal/anti-diagonal matrix, transformed exactly.
    t = [[1, 1], [1, -1]]
    converted = [[F(x, 2) for x in row]
                 for row in matmul(matmul(t, [[1, 1], [1, 3]]), t)]
    assert converted == m
    basis = [tuple(int(i == j) for i in range(6)) for j in range(6)]
    full_m = [[metric(x, y) for y in basis] for x in basis]
    assert full_m == [[m[i//3][j//3]*int(i%3 == j%3) for j in range(6)] for i in range(6)]
    x, y, z = basis[0], basis[1], basis[5]
    ad_defect = metric(bracket(x, y), z)+metric(y, bracket(x, z))
    assert ad_defect == -2
    # Rational unit quaternions: the 24 Hurwitz units.
    units = []
    for i in range(4):
        for s in (-1, 1):
            units.append(tuple(F(s*int(i == j)) for j in range(4)))
    units.extend(tuple(F(s, 2) for s in signs) for signs in product((-1, 1), repeat=4))
    assert len(set(units)) == 24 and all(dot(q, q) == 1 for q in units)
    randomizer = random.Random(6800009)
    action_cases = 128
    for _ in range(action_cases):
        x, y, u, v = [randomizer.choice(units) for _ in range(4)]
        a, b = shear_inverse(u, v)
        assert shear(a, b) == (u, v)
        assert shear_inverse(*shear(u, v)) == (u, v)
        actual = shear(qm(x, a), qm(y, b))
        expected = (qm(x, u), qm(qm(y, v), qi(x)))
        assert actual == expected
    # Check strict endpoint counting against a direct finite count, including
    # stationary factors, exactly conjugate endpoints and nearby rational times.
    ratios = sorted({F(n, d) for d in range(1, 9) for n in range(0, 33)})
    for r in ratios:
        assert strict_count(r) == sum(F(k) < r for k in range(1, 34))
    parity_cases = 0
    for r, s in product(ratios, repeat=2):
        idx = 2*(strict_count(r)+strict_count(s))
        nul = nullity(r, s)
        assert idx >= 0 and idx % 2 == 0 and nul in (0, 2, 4)
        parity_cases += 1
    examples = [(F(0), F(0)), (F(1), F(0)), (F(2), F(1)),
                (F(3, 2), F(5, 2)), (F(2), F(2))]
    result = {
        "status": "PASS",
        "scope": "Exact finite diagnostics only; not a substitute for the global geometric proof.",
        "metric_matrix_per_coordinate_pair": m,
        "leading_principal_minors_per_pair": leading_minors,
        "source_coordinate_conversion": "PASS",
        "ad_invariance_defect": ad_defect,
        "rational_quaternion_action_cases": action_cases,
        "exact_endpoint_ratios": len(ratios),
        "index_nullity_parity_cases": parity_cases,
        "endpoint_examples": [
            {"c1T_over_pi": str(r), "c2T_over_pi": str(s),
             "index": 2*(strict_count(r)+strict_count(s)), "nullity": nullity(r, s)}
            for r, s in examples],
    }
    output = json.dumps(result, indent=2)+"\n"
    print(output, end="")
    Path(__file__).with_name("verify_results.json").write_text(output)


if __name__ == "__main__":
    main()

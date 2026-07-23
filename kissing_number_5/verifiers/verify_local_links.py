#!/usr/bin/env python3
"""Dependency-free exact checks for proofs/local_link_geometry.md."""

from fractions import Fraction as F
from itertools import combinations, product


def padd(a, b):
    n = max(len(a), len(b))
    return [F(a[i]) if i < len(a) else F(0) for i in range(n)] if not b else [
        (F(a[i]) if i < len(a) else F(0))
        + (F(b[i]) if i < len(b) else F(0))
        for i in range(n)
    ]


def pscale(c, a):
    return [F(c) * x for x in a]


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def gegenbauer_s3():
    # Normalized Gegenbauer polynomials on S^3:
    # (k+1)P_k = 2 k t P_{k-1} - (k-1)P_{k-2}.
    polys = [[F(1)], [F(0), F(1)]]
    t = [F(0), F(1)]
    for k in range(2, 5):
        rhs = padd(pscale(2 * k, pmul(t, polys[-1])),
                   pscale(-(k - 1), polys[-2]))
        polys.append(pscale(F(1, k + 1), rhs))
    return polys


def stereographic(point):
    point = tuple(F(x) for x in point)
    r2 = sum(x * x for x in point)
    den = 1 + r2
    return tuple([2 * x / den for x in point] + [(1 - r2) / den])


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def verify_rational_code(raw, threshold, claimed_max):
    pts = [stereographic(p) for p in raw]
    assert all(dot(p, p) == 1 for p in pts)
    values = [(dot(pts[i], pts[j]), i, j)
              for i, j in combinations(range(len(pts)), 2)]
    maximum, i, j = max(values)
    assert maximum == claimed_max
    assert maximum < threshold
    return len(pts), maximum, (i, j)


def verify_polynomial():
    p = gegenbauer_s3()
    coeffs = [F(3, 16), F(2, 3), F(1), F(5, 6), F(5, 16)]
    expansion = []
    for c, q in zip(coeffs, p):
        expansion = padd(expansion, pscale(c, q))
    target = pmul(pmul([F(1, 2), 1], [F(1, 2), 1]),
                  pmul([1, 1], [F(-1, 3), 1]))
    assert expansion == target
    assert all(c > 0 for c in coeffs)
    assert sum(target) / coeffs[0] == 16  # f(1)/f_0
    for a in (0, 1):
        assert (36 - 8 * a) % 5 != 0


def verify_contact_clique_projection():
    for k in range(1, 6):
        qnorm = F(k, 2 * (k + 1))
        assert (F(1, 2) - qnorm) / (1 - qnorm) == F(1, k + 2)
        assert qnorm < 1


def verify_contact_free_maximal_code():
    axes = []
    for i in range(5):
        for sign in (-1, 1):
            p = [F(0)] * 5
            p[i] = F(sign)
            axes.append(tuple(p))
    signs = [tuple(F(s) for s in eps)
             for eps in product((-1, 1), repeat=5)
             if eps[0] * eps[1] * eps[2] * eps[3] * eps[4] == 1]
    assert len(axes) == 10 and len(signs) == 16

    # Store B points symbolically as numerator vectors divided by sqrt(5).
    # Within each homogeneous block all comparisons are rational.
    axis_dots = {dot(x, y) for x, y in combinations(axes, 2)}
    sign_numerator_dots = {dot(x, y) for x, y in combinations(signs, 2)}
    assert axis_dots == {F(-1), F(0)}
    assert sign_numerator_dots == {F(-3), F(1)}
    # Cross values are +/-1/sqrt(5), and 1/sqrt(5)<1/2 iff 4<5.
    assert 4 < 5

    # Exact inequalities used by the saturation proof.
    assert F(6, 5) * F(6, 5) > F(5, 4)
    assert F(3, 5) * 2 == F(6, 5)
    return len(axes) + len(signs)


def main():
    verify_polynomial()
    verify_contact_clique_projection()

    code7 = [
        (F(-10, 11), F(-7, 12)),
        (F(11, 19), F(-28, 19)),
        (F(16, 11), F(1, 2)),
        (F(-59, 10), F(55, 17)),
        (F(-1, 4), F(2, 19)),
        (F(-1, 8), F(21, 20)),
        (F(2, 5), F(-1, 5)),
    ]
    result7 = verify_rational_code(
        code7, F(1, 4), F(1006574101, 4532479101)
    )

    code14 = [
        (F(-7, 18), F(-1, 30), F(1, 8)),
        (F(-7, 17), F(2, 29), F(-2, 3)),
        (F(6, 29), F(-11, 28), F(2, 15)),
        (F(-1, 15), F(17, 27), F(7, 17)),
        (F(-13, 25), F(-7, 8), F(-2, 11)),
        (F(2, 11), F(6, 29), F(-5, 28)),
        (F(7, 29), F(12, 11), F(-9, 14)),
        (F(13, 16), F(5, 27), F(9, 25)),
        (F(-38, 29), F(4, 7), F(3, 25)),
        (F(1, 2), F(-3, 8), F(-16, 23)),
        (F(-4, 27), F(-7, 29), F(23, 24)),
        (F(25, 26), F(-7, 5), F(10, 21)),
        (F(11, 15), F(29, 16), F(32, 15)),
        (F(-16, 19), F(-10, 13), F(-47, 16)),
    ]
    result14 = verify_rational_code(
        code14, F(1, 3), F(87202900460, 267992911109)
    )
    maximal_size = verify_contact_free_maximal_code()

    print("S^3 Gegenbauer identity and equality obstruction: OK")
    print(f"rational S^2 code: n={result7[0]}, max={result7[1]}, pair={result7[2]}")
    print(f"rational S^3 code: n={result14[0]}, max={result14[1]}, pair={result14[2]}")
    print(f"contact-free inclusion-maximal code: n={maximal_size}")


if __name__ == "__main__":
    main()

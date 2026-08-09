#!/usr/bin/env python3
"""Exact replay for the first Bd-to-dB orbit-average obstruction at r=2.

Every calculation below uses SymPy integers and rationals.  The only
positivity device is the elementary tensor-product Bernstein enclosure on a
rational rectangle.
"""

from __future__ import annotations

from hashlib import sha256
from math import comb

import sympy as sp


x, y, u, v = sp.symbols("x y u v")
Q = sp.Rational


def phi(z):
    return z * (2 * z - 1) / (1 + 2 * z)


def lam(z):
    return -(
        (2 * z - 3) * (12 * z**2 - 12 * z + 11)
        / (16 * (2 * z + 1))
    )


def bernstein_coefficients(poly, box):
    """Return exact tensor Bernstein coefficients on one rectangle."""

    a, b, c, d = box
    pulled = sp.Poly(
        sp.expand(poly.subs({x: a + (b - a) * u, y: c + (d - c) * v})),
        u,
        v,
    )
    degree_u = pulled.degree(u)
    degree_v = pulled.degree(v)
    coefficients = []
    for i in range(degree_u + 1):
        for j in range(degree_v + 1):
            value = sum(
                pulled.coeff_monomial(u**k * v**ell)
                * Q(comb(i, k), comb(degree_u, k))
                * Q(comb(j, ell), comb(degree_v, ell))
                for k in range(i + 1)
                for ell in range(j + 1)
            )
            coefficients.append(sp.factor(value))
    return coefficients


def subdivide_until_positive(poly, box, depth=0, maximum_depth=2):
    """Produce a dyadic Bernstein certificate, failing at the depth cap."""

    coefficients = bernstein_coefficients(poly, box)
    if min(coefficients) >= 0:
        return [(box, depth, coefficients)]
    assert depth < maximum_depth
    a, b, c, d = box
    midpoint_x = (a + b) / 2
    midpoint_y = (c + d) / 2
    children = [
        (a, midpoint_x, c, midpoint_y),
        (midpoint_x, b, c, midpoint_y),
        (a, midpoint_x, midpoint_y, d),
        (midpoint_x, b, midpoint_y, d),
    ]
    return sum(
        (
            subdivide_until_positive(
                poly, child, depth + 1, maximum_depth
            )
            for child in children
        ),
        [],
    )


def exact_edge_slack():
    derivative = sp.diff(phi(x), x)
    edge_term = phi(x) - x * derivative + x * derivative.subs(x, y)
    slack = sp.factor(edge_term + (1 - y) * (lam(y) - 2 * x * lam(x)))

    numerator = sp.Poly(
        sp.cancel(slack * 16 * (1 + 2 * x) ** 2 * (1 + 2 * y) ** 2),
        x,
        y,
    ).as_expr()
    assert sp.factor(
        slack
        - numerator / (16 * (1 + 2 * x) ** 2 * (1 + 2 * y) ** 2)
    ) == 0
    assert sp.factor(sp.diff(phi(x), x, 2) - 8 / (1 + 2 * x) ** 3) == 0

    center = {x: Q(1, 2), y: Q(1, 2)}
    assert numerator.subs(center) == 0
    assert sp.diff(numerator, x).subs(center) == 0
    assert sp.diff(numerator, y).subs(center) == 0
    return numerator


def exact_square_certificate(numerator):
    """Certify N>=0 on [0,1]^2 by 26 outer boxes and one convex box."""

    lower = Q(7, 16)
    upper = Q(9, 16)

    # On the central square the Hessian is positive definite.  Positivity of
    # each displayed polynomial follows from its exact Bernstein enclosure.
    hessian_xx = sp.diff(numerator, x, 2)
    hessian_yy = sp.diff(numerator, y, 2)
    hessian_xy = sp.diff(numerator, x, y)
    determinant = sp.expand(hessian_xx * hessian_yy - hessian_xy**2)
    central_box = (lower, upper, lower, upper)
    central_minima = {
        "N_xx": min(bernstein_coefficients(hessian_xx, central_box)),
        "N_yy": min(bernstein_coefficients(hessian_yy, central_box)),
        "det_H": min(bernstein_coefficients(determinant, central_box)),
    }
    assert all(value > 0 for value in central_minima.values())

    # The remaining eight cells of the 3-by-3 grid are handled by at most two
    # dyadic subdivisions.  Every leaf has nonnegative Bernstein coefficients.
    endpoints = [Q(0), lower, upper, Q(1)]
    leaves = []
    for i in range(3):
        for j in range(3):
            if (i, j) == (1, 1):
                continue
            box = (
                endpoints[i],
                endpoints[i + 1],
                endpoints[j],
                endpoints[j + 1],
            )
            leaves.extend(subdivide_until_positive(numerator, box))

    assert len(leaves) == 26
    assert max(depth for _, depth, _ in leaves) == 2
    assert all(min(coefficients) >= 0 for _, _, coefficients in leaves)

    # Hash the complete rational certificate so any accidental change to the
    # subdivision or coefficient list is visible in replay output.
    serialization = "\n".join(
        ";".join(
            [*(str(entry) for entry in box), str(depth)]
            + [str(value) for value in coefficients]
        )
        for box, depth, coefficients in leaves
    )
    certificate_hash = sha256(serialization.encode()).hexdigest()
    expected_hash = "df5aaf698f23680e53614cbc9bc1e8b65571178455506d7ae1ad41ffcc40e0eb"
    assert certificate_hash == expected_hash
    return central_minima, leaves, certificate_hash


def main():
    numerator = exact_edge_slack()
    central_minima, leaves, certificate_hash = exact_square_certificate(
        numerator
    )
    print("PASS exact first Bd-to-dB orbit step")
    print(f"outer Bernstein leaves: {len(leaves)}")
    print(f"central Bernstein minima: {central_minima}")
    print(f"certificate sha256: {certificate_hash}")


if __name__ == "__main__":
    main()

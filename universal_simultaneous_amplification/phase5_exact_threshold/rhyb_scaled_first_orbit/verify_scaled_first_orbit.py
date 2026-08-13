#!/usr/bin/env python3
"""Exact replay of the scaled first Bd-to-dB orbit inequality near R_hyb.

The proof uses only rational arithmetic.  It constructs the edge slack from
the displayed convex tangent and linear flow multiplier, then certifies its
cleared numerator on

    [3/2, 151/100] x [0,1] x [0,1]

by tensor-product Bernstein coefficients.  A positive-definite Hessian
certificate handles the one central cell containing the moving equality
point (1/r,1/r).
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
from math import comb

import sympy as sp


r, x, y = sp.symbols("r x y")
Q = sp.Rational


def phi(z):
    c = r - 1
    return c**2 * z * (r * z - 1) / (1 + r * c * z)


def lam(z):
    c = r - 1
    return c / r - 2 * c * (z - 1 / r) / r


def exact_slack_numerator():
    """Construct the pointwise edge slack and its polynomial numerator."""

    derivative_x = sp.diff(phi(x), x)
    derivative_y = sp.diff(phi(y), y)
    tangent_edge = phi(x) - x * derivative_x + x * derivative_y
    flow_null = (1 - y) * (lam(y) - r * x * lam(x))
    slack = sp.factor(tangent_edge + flow_null)

    c = r - 1
    denominator = r**2 * (1 + r * c * x) ** 2 * (1 + r * c * y) ** 2
    numerator = sp.cancel(slack * denominator)
    assert sp.Poly(numerator, r, x, y).as_expr() == numerator
    assert sp.factor(slack - numerator / denominator) == 0

    # The scalar gap is convex on the entire nonnegative ray.
    z = sp.symbols("z")
    expected_second = 2 * r**2 * c**2 / (1 + r * c * z) ** 3
    assert sp.factor(sp.diff(phi(z), z, 2) - expected_second) == 0

    # For every r, the central equality point is stationary.
    center = {x: 1 / r, y: 1 / r}
    assert sp.factor(numerator.subs(center)) == 0
    assert sp.factor(sp.diff(numerator, x).subs(center)) == 0
    assert sp.factor(sp.diff(numerator, y).subs(center)) == 0
    return sp.expand(numerator)


def tensor_bernstein_coefficients(poly_expr, box):
    """Return exact 3-variable Bernstein coefficients on a rational box."""

    poly = sp.Poly(poly_expr, r, x, y)
    degrees = poly.degree_list()
    starts = box[::2]
    widths = tuple(box[2 * index + 1] - starts[index] for index in range(3))

    # Pull back to the unit cube in the monomial basis.
    power = {}
    for exponents, coefficient in poly.terms():
        for local_exponents in product(
            *(range(exponent + 1) for exponent in exponents)
        ):
            contribution = coefficient
            for coordinate in range(3):
                exponent = exponents[coordinate]
                local = local_exponents[coordinate]
                contribution *= (
                    sp.binomial(exponent, local)
                    * starts[coordinate] ** (exponent - local)
                    * widths[coordinate] ** local
                )
            power[local_exponents] = power.get(local_exponents, 0) + contribution

    # Convert the monomial coefficients on the unit cube to Bernstein form.
    coefficients = []
    for bernstein_index in product(*(range(degree + 1) for degree in degrees)):
        value = 0
        for local_exponents in product(
            *(range(index + 1) for index in bernstein_index)
        ):
            contribution = power.get(local_exponents, 0)
            for coordinate in range(3):
                contribution *= Q(
                    comb(bernstein_index[coordinate], local_exponents[coordinate]),
                    comb(degrees[coordinate], local_exponents[coordinate]),
                )
            value += contribution
        coefficients.append(sp.factor(value))
    return coefficients


def exact_box_certificate(numerator):
    """Certify the numerator on the full parameter box."""

    r_lower = Q(3, 2)
    r_upper = Q(151, 100)
    lower = Q(16, 25)
    upper = Q(69, 100)

    # The central square contains (1/r,1/r) for the complete r interval.
    assert lower < 1 / r_upper < 1 / r_lower < upper
    central_box = (r_lower, r_upper, lower, upper, lower, upper)
    hessian_xx = sp.diff(numerator, x, 2)
    hessian_yy = sp.diff(numerator, y, 2)
    hessian_xy = sp.diff(numerator, x, y)
    determinant = sp.expand(hessian_xx * hessian_yy - hessian_xy**2)
    central_polynomials = {
        "N_xx": hessian_xx,
        "N_yy": hessian_yy,
        "det_H": determinant,
    }
    central_coefficients = {
        name: tensor_bernstein_coefficients(poly, central_box)
        for name, poly in central_polynomials.items()
    }
    central_minima = {
        name: min(coefficients)
        for name, coefficients in central_coefficients.items()
    }
    assert all(value > 0 for value in central_minima.values())

    # The other eight cells have nonnegative numerator coefficients directly.
    endpoints = [Q(0), lower, upper, Q(1)]
    outer = []
    for i in range(3):
        for j in range(3):
            if (i, j) == (1, 1):
                continue
            box = (
                r_lower,
                r_upper,
                endpoints[i],
                endpoints[i + 1],
                endpoints[j],
                endpoints[j + 1],
            )
            coefficients = tensor_bernstein_coefficients(numerator, box)
            assert min(coefficients) >= 0
            outer.append(((i, j), box, coefficients))

    # Hash the entire rational certificate, not rounded summaries.
    serialization_parts = []
    for name in ("N_xx", "N_yy", "det_H"):
        serialization_parts.append(name)
        serialization_parts.extend(str(value) for value in central_coefficients[name])
    for cell, box, coefficients in outer:
        serialization_parts.append(str(cell))
        serialization_parts.extend(str(value) for value in box)
        serialization_parts.extend(str(value) for value in coefficients)
    certificate_hash = sha256("\n".join(serialization_parts).encode()).hexdigest()

    outer_minima = {
        cell: min(coefficients) for cell, _, coefficients in outer
    }
    return central_minima, outer_minima, certificate_hash


def main():
    # The known isolating interval for R_hyb is also independently bracketed.
    hybrid_polynomial = (
        r**6
        - 8 * r**5
        + 22 * r**4
        - 30 * r**3
        + 21 * r**2
        - 6 * r
        + 1
    )
    assert hybrid_polynomial.subs(r, Q(3, 2)) > 0
    assert hybrid_polynomial.subs(r, Q(151, 100)) < 0

    numerator = exact_slack_numerator()
    central_minima, outer_minima, certificate_hash = exact_box_certificate(
        numerator
    )

    expected_hash = "5f28f87dfe16b3be6b9f464b160999b26c74f030988f1a60ab3ab57aeb35549f"
    assert certificate_hash == expected_hash

    print("PASS exact scaled first Bd-to-dB orbit theorem")
    print("fitness interval: [3/2, 151/100]")
    print(f"central Bernstein minima: {central_minima}")
    print(f"outer Bernstein minima: {outer_minima}")
    print(f"certificate sha256: {certificate_hash}")


if __name__ == "__main__":
    main()

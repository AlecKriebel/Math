#!/usr/bin/env python3
"""Exact exploratory certificate for a two-portal, one-blade-type separator.

The intended inequality at r=31/20 is

    (q_B^0-D_B(q_B^0)) + 2/5 (q_D^0-D_D(q_D^0)) < 0.

All transforms are reconstructed from the three labelled nonempty portal
subsets.  The current adaptive Bernstein search is deterministic; once a
small cover is found its paths can be frozen into an independently replayed
certificate.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import sympy as sp


def portal_hitting(rule, r, b1, b2, edge, mark):
    d1, d2 = b1 + edge, b2 + edge
    if rule == "Bd":
        killing = (
            r**2 * b1 * mark / ((r + 1) * d1),
            r**2 * b2 * mark / ((r + 1) * d2),
            r**2 * mark / (r + 1) * (b1 / d1 + b2 / d2),
        )
        down1, up1 = b1 + edge / d2, r * edge / d1
        down2, up2 = b2 + edge / d1, r * edge / d2
        to1, to2 = b2, b1
    elif rule == "dB":
        killing = (
            r * b1 * mark / 2,
            r * b2 * mark / 2,
            r * (b1 + b2) * mark / 2,
        )
        down1, up1 = 1, r * edge / (b2 + r * edge)
        down2, up2 = 1, r * edge / (b1 + r * edge)
        to1 = b2 / (b2 + r * edge)
        to2 = b1 / (b1 + r * edge)
    else:
        raise ValueError(rule)
    matrix = sp.Matrix([
        [down1 + up1 + killing[0], 0, -up1],
        [0, down2 + up2 + killing[1], -up2],
        [-to1, -to2, to1 + to2 + killing[2]],
    ])
    return matrix.inv() * sp.Matrix(killing)


def split_bernstein(coefficients, degrees, axis):
    groups = {}
    for index, value in coefficients.items():
        other = index[:axis] + index[axis + 1:]
        groups.setdefault(other, [Fraction(0)] * (degrees[axis] + 1))[
            index[axis]
        ] = value
    left, right = {}, {}
    degree = degrees[axis]
    for other, line in groups.items():
        triangle = [line]
        for _ in range(degree):
            previous = triangle[-1]
            triangle.append([
                (previous[j] + previous[j + 1]) / 2
                for j in range(len(previous) - 1)
            ])
        for j in range(degree + 1):
            index = other[:axis] + (j,) + other[axis:]
            left[index] = triangle[j][0]
            right[index] = triangle[degree - j][j]
    return left, right


def separator_rational(r, coefficient):
    b1, b2, edge = sp.symbols("b1 b2 edge", positive=True)
    d1, d2 = b1 + edge, b2 + edge

    hb = portal_hitting("Bd", r, b1, b2, edge, 1 - 1 / r**2)
    death_b = (b1 / d1 + b2 / d2) / (r + 1)
    offspring_b = r * (b1 * hb[0] + b2 * hb[1])
    test_b = 1 / r**2 - death_b / (death_b + offspring_b)

    hd = portal_hitting("dB", r, b1, b2, edge, 2 * (r - 1) / r)
    death_d = (b1 + b2) / (2 * r)
    offspring_d = r * (b1 * hd[0] / d1 + b2 * hd[1] / d2)
    test_d = (2 - r) / r - death_d / (death_d + offspring_d)

    positive, denominator = sp.cancel(-(test_b + coefficient * test_d)).as_numer_denom()
    return positive, denominator, (b1, b2, edge), (test_b, test_d)


def separator_numerator(r, coefficient):
    positive, denominator, variables, tests = separator_rational(r, coefficient)
    b1, b2, edge = variables
    denominator_poly = sp.Poly(denominator, b1, b2, edge)
    if any(value <= 0 for _, value in denominator_poly.terms()):
        raise AssertionError("separator denominator lacks a positive monomial certificate")
    return sp.Poly(positive, b1, b2, edge), tests


def orthant_bernstein(poly):
    """Bernstein tensor after x_i=u_i/(1-u_i), without expansion.

    Multiplication by ``prod_i (1-u_i)^degree_i`` sends ``x_i^j`` to
    ``u_i^j(1-u_i)^(degree_i-j)``, exactly ``B_{j,degree_i}`` divided by
    ``binomial(degree_i,j)``.  The original power coefficients therefore
    become the compactified Bernstein coefficients after this one diagonal
    rescaling.
    """
    degrees = poly.degree_list()
    values = {
        index: Fraction(0)
        for index in itertools.product(*[range(degree + 1) for degree in degrees])
    }
    for index, coefficient in poly.terms():
        if not coefficient.is_Integer:
            raise AssertionError("orthant source polynomial is not integral")
        denominator = math.prod(
            math.comb(degree, power)
            for degree, power in zip(degrees, index)
        )
        values[index] = Fraction(int(coefficient), denominator)
    return degrees, values


def mixed_interval_orthant_bernstein(poly):
    """Power Bernstein in the first variable, orthant Bernstein thereafter."""
    degrees = poly.degree_list()
    values = {
        index: Fraction(0)
        for index in itertools.product(*[range(degree + 1) for degree in degrees])
    }
    # First collect coefficients in power(a) and compactified Bernstein(b).
    source = {}
    for index, coefficient in poly.terms():
        if not coefficient.is_Integer:
            raise AssertionError("mixed source polynomial is not integral")
        denominator = math.prod(
            math.comb(degree, power)
            for degree, power in zip(degrees[1:], index[1:])
        )
        source[index] = Fraction(int(coefficient), denominator)
    # Power-to-Bernstein conversion on the bounded fitness coordinate.
    for target in values:
        p_target, tail = target[0], target[1:]
        values[target] = sum(
            source.get((power,) + tail, Fraction(0))
            * Fraction(math.comb(p_target, power), math.comb(degrees[0], power))
            for power in range(p_target + 1)
        )
    return degrees, values


INTERVAL_PATHS = (
    ((3, 0), (1, 0), (2, 0)),
    ((3, 0), (1, 0), (2, 1)),
    ((3, 0), (1, 1), (2, 0)),
    ((3, 0), (1, 1), (2, 1)),
    ((3, 1), (1, 1), (3, 0)),
    ((3, 1), (1, 1), (3, 1)),
    ((3, 1), (1, 0), (2, 0), (3, 1)),
    ((3, 1), (1, 0), (2, 1), (3, 0)),
    ((3, 1), (1, 0), (2, 1), (3, 1)),
    ((3, 1), (1, 0), (2, 0), (3, 0), (3, 0)),
    ((3, 1), (1, 0), (2, 0), (3, 0), (3, 1)),
)


def follow_path(coefficients, degrees, path):
    values = coefficients
    intervals = [(Fraction(0), Fraction(1)) for _ in degrees]
    for axis, side in path:
        left, right = split_bernstein(values, degrees, axis)
        low, high = intervals[axis]
        midpoint = (low + high) / 2
        if side == 0:
            values = left
            intervals[axis] = (low, midpoint)
        else:
            values = right
            intervals[axis] = (midpoint, high)
    return values, intervals


def verify_fixed_cover(degrees, coefficients, paths):
    # Prefix-free leaves with Kraft sum one form an exact binary cover.
    for i, path in enumerate(paths):
        for j, other in enumerate(paths):
            if i != j and len(path) <= len(other) and path == other[:len(path)]:
                raise AssertionError("certificate paths are not prefix-free")
    if sum(Fraction(1, 2 ** len(path)) for path in paths) != 1:
        raise AssertionError("certificate paths do not cover the unit cube")

    audited_faces = 0
    for path in paths:
        values, intervals = follow_path(coefficients, degrees, path)
        if min(values.values()) < 0:
            raise AssertionError(f"negative terminal coefficient on {path}")

        # Strictness on every relative face that can meet
        # [0,1] x (0,1)^3.  Status -1 is a free local coordinate; 0 and 1
        # are its lower and upper face.  Fitness endpoints are physical,
        # while load/edge endpoints are excluded by strict positivity.
        for status in itertools.product((-1, 0, 1), repeat=len(degrees)):
            outside_physical_domain = any(
                axis > 0
                and ((side == 0 and intervals[axis][0] == 0)
                     or (side == 1 and intervals[axis][1] == 1))
                for axis, side in enumerate(status)
            )
            if outside_physical_domain:
                continue
            active = [
                value for index, value in values.items()
                if all(side == -1
                       or (side == 0 and index[axis] == 0)
                       or (side == 1 and index[axis] == degrees[axis])
                       for axis, side in enumerate(status))
            ]
            if not any(value > 0 for value in active):
                raise AssertionError(f"non-strict physical face on {path}: {status}")
            audited_faces += 1
    print("PASS fixed Bernstein cover:", len(paths), "boxes;",
          audited_faces, "physical faces strictly positive")


def main():
    # One common separator works throughout the whole nontrivial interval.
    a = sp.symbols("a")
    fitness = (3 + a) / 2  # a in [0,1] is r in [3/2,2]
    weight = sp.Rational(81, 200)
    positive, denominator, variables, _ = separator_rational(fitness, weight)
    interval_poly = sp.Poly(positive, a, *variables)
    common = sp.lcm([coefficient.q for _, coefficient in interval_poly.terms()])
    interval_poly = sp.Poly(common * interval_poly.as_expr(), a, *variables)
    denominator_poly = sp.Poly(denominator, a, *variables)
    if any(coefficient <= 0 for _, coefficient in denominator_poly.terms()):
        raise AssertionError("interval denominator lacks positive coefficients")
    print("PASS common denominator positive by", len(denominator_poly.terms()),
          "positive monomials")
    print("INTERVAL CASE [3/2,2], weight", weight)
    print("raw degrees", interval_poly.degree_list(),
          "terms", len(interval_poly.terms()))
    degrees, coefficients = mixed_interval_orthant_bernstein(interval_poly)
    print("initial negative Bernstein coefficients",
          sum(value < 0 for value in coefficients.values()))
    verify_fixed_cover(degrees, coefficients, INTERVAL_PATHS)
    print("ALL Q=2 SCALAR DIRECT-PORTAL CERTIFICATES PASS")


if __name__ == "__main__":
    main()

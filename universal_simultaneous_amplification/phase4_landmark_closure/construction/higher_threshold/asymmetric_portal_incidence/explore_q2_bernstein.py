#!/usr/bin/env python3
"""Attempt a Bernstein certificate for the OPEN two-portal inequality.

This is exploratory and is not invoked by the proved theorem's verifier.
"""

from __future__ import annotations

import math
from fractions import Fraction

import sympy as sp


def episode(d1, p1, k1, d2, p2, k2, c, a1, a2, k12):
    aa1, aa2 = d1 + p1 + k1, d2 + p2 + k2
    h12 = sp.cancel(
        (k12 + a1 * k1 / aa1 + a2 * k2 / aa2)
        / (c - a1 * p1 / aa1 - a2 * p2 / aa2)
    )
    return sp.cancel((k1 + p1 * h12) / aa1), sp.cancel(
        (k2 + p2 * h12) / aa2
    )


def polynomial():
    R, a, u, v, h = sp.symbols("R a u v h")
    x, y = h * (1 - u) / u, h * (1 - v) / v
    k1, k2 = (R - 1) * (1 - u), (R - 1) * (1 - v)
    p1, p2 = R * u, R * v
    hb = episode(
        x + v,
        p1,
        k1,
        y + u,
        p2,
        k2,
        x + y + k1 + k2,
        y,
        x,
        k1 + k2,
    )
    j1, j2 = (R - 1) * x, (R - 1) * y
    w1 = R * v / (1 + (R - 1) * v)
    w2 = R * u / (1 + (R - 1) * u)
    dn1 = (1 - u) / (1 + (R - 1) * u)
    dn2 = (1 - v) / (1 + (R - 1) * v)
    hd = episode(
        1,
        w1,
        j1,
        1,
        w2,
        j2,
        dn1 + dn2 + j1 + j2,
        dn2,
        dn1,
        j1 + j2,
    )
    slack = (
        (R - 1) * (1 + h / u)
        - R * (h / u) * hb[0]
        - R**2 * (2 - R) * hd[0]
    )
    numerator = sp.fraction(sp.cancel(slack.subs(R, 1 + a)))[0]
    numerator = sp.cancel(numerator / a**2)
    return sp.Poly(numerator, a, h, u, v)


def compact_power(poly):
    degrees = poly.degree_list()
    hdeg = degrees[1]
    power = {}
    for (ia, jh, iu, iv), coefficient in poly.terms():
        c = int(coefficient)
        for t in range(hdeg - jh + 1):
            key = (ia, jh + t, iu, iv)
            power[key] = power.get(key, 0) + c * (-1) ** t * math.comb(
                hdeg - jh, t
            )
    return tuple(degrees), {k: v for k, v in power.items() if v}


def power_to_bernstein(degrees, power):
    current = {index: Fraction(value) for index, value in power.items()}
    for axis, degree in enumerate(degrees):
        groups = {}
        for index, value in current.items():
            other = index[:axis] + index[axis + 1 :]
            groups.setdefault(other, {})[index[axis]] = value
        following = {}
        for other, values in groups.items():
            for k in range(degree + 1):
                value = sum(
                    (
                        c * Fraction(math.comb(k, i), math.comb(degree, i))
                        for i, c in values.items()
                        if i <= k
                    ),
                    Fraction(0),
                )
                index = other[:axis] + (k,) + other[axis:]
                following[index] = value
        current = following
    return current


def split(coefficients, degrees, axis):
    groups = {}
    for index, value in coefficients.items():
        other = index[:axis] + index[axis + 1 :]
        groups.setdefault(other, [Fraction(0)] * (degrees[axis] + 1))[
            index[axis]
        ] = value
    left, right = {}, {}
    n = degrees[axis]
    for other, line in groups.items():
        triangle = [line]
        for _ in range(n):
            previous = triangle[-1]
            triangle.append(
                [(previous[j] + previous[j + 1]) / 2 for j in range(len(previous) - 1)]
            )
        lline = [triangle[j][0] for j in range(n + 1)]
        rline = [triangle[n - j][j] for j in range(n + 1)]
        for j in range(n + 1):
            index = other[:axis] + (j,) + other[axis:]
            left[index], right[index] = lline[j], rline[j]
    return left, right


def certify(coefficients, degrees, max_depth=20):
    stack = [(coefficients, 0)]
    certified = 0
    while stack:
        box, depth = stack.pop()
        values = box.values()
        if min(values) >= 0:
            certified += 1
            continue
        if max(values) < 0:
            return False, certified, depth, "negative box"
        if depth >= max_depth:
            return False, certified, depth, "unresolved"
        axis = depth % 4
        left, right = split(box, degrees, axis)
        stack.append((right, depth + 1))
        stack.append((left, depth + 1))
    return True, certified, max_depth, "certified"


def main():
    poly = polynomial()
    degrees, power = compact_power(poly)
    print("degrees", degrees, "power terms", len(power))
    bernstein = power_to_bernstein(degrees, power)
    print(
        "initial Bernstein range",
        min(bernstein.values()),
        max(bernstein.values()),
    )
    for axis in range(4):
        left, right = split(bernstein, degrees, axis)
        print(
            "axis",
            axis,
            "left",
            min(left.values()),
            sum(value < 0 for value in left.values()),
            "right",
            min(right.values()),
            sum(value < 0 for value in right.values()),
        )
    near_zero = bernstein
    for depth in range(1, 13):
        near_zero, outer = split(near_zero, degrees, 1)
        print(
            "h-depth",
            depth,
            "near-zero",
            min(near_zero.values()),
            sum(value < 0 for value in near_zero.values()),
            "outer",
            min(outer.values()),
            sum(value < 0 for value in outer.values()),
        )
    # Full adaptive subdivision is intentionally disabled: the first-pass
    # coefficient audit does not produce a compact certificate yet.


if __name__ == "__main__":
    main()

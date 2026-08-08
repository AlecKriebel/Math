#!/usr/bin/env python3
"""Exact certificate for the higher-rank no-direct-portal separation.

The verifier has three independent layers:

1. symbolic reduction of the atomic labelled rates to load fractions;
2. an exact rational labelled-subset solve at Q=3,T=2;
3. fixed Bernstein certificates for the scalar separation lemma.

No floating-point sign decision is used.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import sympy as sp


def checked_zero(expr: sp.Expr, label: str) -> None:
    value = sp.factor(sp.cancel(expr))
    if value != 0:
        raise AssertionError(f"{label}: {value}")
    print(f"PASS {label}")


def atomic_symbolic_checks() -> None:
    r, B, m = sp.symbols("r B m", positive=True)
    c = r**2 / (r + 1)
    d = r / 2

    # With f_at=2*pi_t*lambda_at/B_a and sum_t f_at=1, a
    # singleton portal has these marked-child transforms directly from
    # the atomic rates delta_B=B, beta_B,t=c*f_at and
    # delta_D=1, beta_D,t=d*B*f_at.
    h_b = c * m / (B + c * m)
    h_d = d * B * m / (1 + d * B * m)
    u_b = B * m / (B + c * m)
    u_d = B * m / (1 + d * B * m)
    checked_zero(r * (r + 1) * B * h_b - r**3 * u_b,
                 "Bd portal/parent normalization")
    checked_zero(2 * r**2 * h_d - r**3 * u_d,
                 "dB portal/parent normalization")

    # The affine survival complement commutes with row averaging before
    # clipping: sum_j f_aj (A-k*s_j)=A-k*sum_j f_aj*s_j.
    f1, f2, s1, s2 = sp.symbols("f1 f2 s1 s2", positive=True)
    A = 4 * (r - 1) / r
    k = 2 * r / (r + 1)
    checked_zero(
        (
            f1 * (A - k * s1) + f2 * (A - k * s2)
            - (A - k * (f1 * s1 + f2 * s2))
        ).subs(f2, 1 - f1),
        "affine complement commutes with row averaging",
    )


def exact_labelled_subset_check() -> None:
    """Independently solve the full seven-state portal episode."""
    r = sp.Rational(8, 5)
    pi = (sp.Rational(2, 5), sp.Rational(3, 5))
    lam = (
        (sp.Rational(1, 3), sp.Rational(2, 7)),
        (sp.Rational(5, 4), sp.Rational(1, 9)),
        (sp.Rational(2, 5), sp.Rational(7, 6)),
    )
    z = (sp.Rational(3, 11), sp.Rational(5, 13))
    q_portals, types = 3, 2
    bload = [2 * sum(pi[t] * lam[a][t] for t in range(types))
             for a in range(q_portals)]
    frac = [[2 * pi[t] * lam[a][t] / bload[a] for t in range(types)]
            for a in range(q_portals)]
    masks = list(range(1, 1 << q_portals))
    row = {mask: j for j, mask in enumerate(masks)}

    singleton_transforms = {}
    for rule in ("Bd", "dB"):
        matrix = sp.zeros(len(masks)); rhs = sp.zeros(len(masks), 1)
        for mask in masks:
            j = row[mask]
            active = [a for a in range(q_portals) if mask >> a & 1]
            transitions = []
            for a in active:
                death = bload[a] if rule == "Bd" else sp.Integer(1)
                transitions.append((mask ^ (1 << a), death))
            if rule == "Bd":
                child = [
                    2 * pi[t] * r**2 / (r + 1)
                    * sum(lam[a][t] / bload[a] for a in active)
                    for t in range(types)
                ]
            else:
                child = [
                    pi[t] * r * sum(lam[a][t] for a in active)
                    for t in range(types)
                ]
            killing = sum(child[t] * (1 - z[t]) for t in range(types))
            matrix[j, j] = sum(rate for _, rate in transitions) + killing
            for nxt, rate in transitions:
                if nxt == 0:
                    rhs[j] += rate
                else:
                    matrix[j, row[nxt]] -= rate
        solution = matrix.inv() * rhs
        singleton_transforms[rule] = [solution[row[1 << a]]
                                      for a in range(q_portals)]

        for a in range(q_portals):
            mark = sum(frac[a][t] * (1 - z[t]) for t in range(types))
            if rule == "Bd":
                expected = bload[a] / (
                    bload[a] + r**2 * mark / (r + 1)
                )
            else:
                expected = 1 / (1 + r * bload[a] * mark / 2)
            checked_zero(solution[row[1 << a]] - expected,
                         f"exact labelled {rule} singleton portal {a}")

    # Independently compare the parent lifetime law with the normalized
    # higher-rank formulas for both parent types.
    for t in range(types):
        c_t = sum(frac[a][t] for a in range(q_portals))
        ell_t = sum(bload[a] * frac[a][t] for a in range(q_portals))
        h_b = [1 - value for value in singleton_transforms["Bd"]]
        h_d = [1 - value for value in singleton_transforms["dB"]]
        death_b = 2 / (r + 1) * sum(
            lam[a][t] / bload[a] for a in range(q_portals)
        )
        killed_b = 2 * r * sum(
            lam[a][t] * h_b[a] for a in range(q_portals)
        )
        direct_b = death_b / (death_b + killed_b)
        normalized_b = c_t / (
            c_t + r * (r + 1)
            * sum(bload[a] * frac[a][t] * h_b[a]
                  for a in range(q_portals))
        )
        checked_zero(direct_b - normalized_b,
                     f"exact labelled Bd parent type {t}")

        death_d = sum(lam[a][t] for a in range(q_portals)) / r
        killed_d = 2 * r * sum(
            lam[a][t] * h_d[a] / bload[a]
            for a in range(q_portals)
        )
        direct_d = death_d / (death_d + killed_d)
        normalized_d = ell_t / (
            ell_t + 2 * r**2
            * sum(frac[a][t] * h_d[a] for a in range(q_portals))
        )
        checked_zero(direct_d - normalized_d,
                     f"exact labelled dB parent type {t}")


def power_to_bernstein(poly: sp.Poly):
    degrees = poly.degree_list()
    if any(not coefficient.is_Integer for _, coefficient in poly.terms()):
        raise AssertionError("Bernstein source polynomial is not integral")
    current = {
        index: Fraction(int(coefficient))
        for index, coefficient in poly.terms()
    }
    for axis, degree in enumerate(degrees):
        groups = {}
        for index, value in current.items():
            other = index[:axis] + index[axis + 1:]
            groups.setdefault(other, {})[index[axis]] = value
        following = {}
        for other, values in groups.items():
            for k in range(degree + 1):
                value = sum(
                    (
                        coefficient
                        * Fraction(math.comb(k, i), math.comb(degree, i))
                        for i, coefficient in values.items()
                        if i <= k
                    ),
                    Fraction(0),
                )
                index = other[:axis] + (k,) + other[axis:]
                following[index] = value
        current = following
    return degrees, current


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


LOW_PATHS = (
    ((3, 0), (1, 0)),
    ((3, 0), (1, 1), (1, 0)),
    ((3, 0), (1, 1), (1, 1)),
    ((3, 1), (1, 0)),
    ((3, 1), (1, 1), (1, 0)),
    ((3, 1), (1, 1), (1, 1)),
)

HIGH_PATHS = (
    ((3, 0), (1, 0)),
    ((3, 0), (1, 1), (1, 0), (1, 0)),
    ((3, 0), (1, 1), (1, 0), (1, 1)),
    ((3, 0), (1, 1), (1, 1)),
    ((3, 1), (1, 0)),
    ((3, 1), (1, 1), (0, 0), (1, 0), (2, 0)),
    ((3, 1), (1, 1), (0, 0), (1, 0), (2, 1)),
    ((3, 1), (1, 1), (0, 0), (1, 1), (3, 0), (2, 0)),
    ((3, 1), (1, 1), (0, 0), (1, 1), (3, 0), (2, 1)),
    ((3, 1), (1, 1), (0, 0), (1, 1), (3, 1)),
    ((3, 1), (1, 1), (0, 1)),
)


def scalar_polynomial(case: str):
    a, u, v, b = sp.symbols("a u v b", nonnegative=True)
    r = (3 + a) / 2
    A = 4 * (r - 1) / r
    k = 2 * r / (r + 1)
    m0 = sp.factor((A - 1) / k)
    xmax = r**3 / (1 + r**3)
    x = sp.cancel(m0 + (xmax - m0) * u)
    y = sp.factor(A - k * x)
    B = b / (1 - b)
    c = r**2 / (r + 1)
    d = r / 2
    if case == "low":
        m, n = m0 * v, sp.Integer(1)
        positive_denominator = (
            128 * (a + 3)**3 * (a + 5)**3 * (1 - b)**3
            * (a**2 + 4 * a + 7)**2
        )
    elif case == "high":
        m = m0 + (1 - m0) * v
        n = sp.factor(A - k * m)
        positive_denominator = (
            128 * (a + 3)**3 * (a + 5)**5 * (1 - b)**3
            * (a**2 + 4 * a + 7)**2
        )
    else:
        raise ValueError(case)

    # Multiply the scalar gap by its manifestly positive physical
    # denominator (1-x)(1-y)(B+c*m)(1+d*B*n).
    numerator_form = (
        x * (1 - y) * (B + c * m) * (1 + d * B * n)
        + B * y * (1 - x) * (B + c * m) * (1 + d * B * n)
        - r**3 * (
            B * m * (1 - x) * (1 - y) * (1 + d * B * n)
            + B * n * (1 - x) * (1 - y) * (B + c * m)
        )
    )
    raw_numerator, raw_denominator = sp.fraction(sp.cancel(numerator_form))
    checked_zero(raw_denominator + positive_denominator,
                 f"{case} compactification denominator sign")
    return sp.Poly(-raw_numerator, a, u, v, b)


def verify_paths(poly: sp.Poly, paths, label: str) -> None:
    def check_partition(suffixes) -> None:
        if any(not path for path in suffixes):
            if len(suffixes) != 1 or suffixes[0]:
                raise AssertionError(f"overlapping certificate leaves: {label}")
            return
        axes = {path[0][0] for path in suffixes}
        if len(axes) != 1:
            raise AssertionError(f"inconsistent split axes: {label} {axes}")
        for side in (0, 1):
            children = [path[1:] for path in suffixes if path[0][1] == side]
            if not children:
                raise AssertionError(f"missing certificate half: {label} {side}")
            check_partition(children)

    check_partition(list(paths))
    degrees, original = power_to_bernstein(poly)
    if tuple(degrees) not in ((14, 2, 1, 3), (16, 2, 2, 3)):
        raise AssertionError(f"unexpected {label} degrees {degrees}")
    for path in paths:
        box = original
        intervals = [[Fraction(0), Fraction(1)] for _ in degrees]
        for axis, side in path:
            left, right = split_bernstein(box, degrees, axis)
            box = (left, right)[side]
            midpoint = sum(intervals[axis], Fraction(0)) / 2
            if side == 0:
                intervals[axis][1] = midpoint
            else:
                intervals[axis][0] = midpoint
        if min(box.values()) < 0:
            raise AssertionError(f"negative Bernstein coefficient: {label} {path}")
        if max(box.values()) <= 0:
            raise AssertionError(f"identically zero Bernstein box: {label} {path}")

        # The physical domain has 0<u<1 and 0<b<1.  Check every face of
        # every terminal box that can meet that domain.  A nonnegative
        # Bernstein polynomial is strictly positive on such a face once
        # at least one of its active face coefficients is positive.
        for statuses in itertools.product((-1, 0, 1), repeat=4):
            forced = [
                None if status == -1 else intervals[axis][status]
                for axis, status in enumerate(statuses)
            ]
            if forced[1] in (Fraction(0), Fraction(1)):
                continue
            if forced[3] in (Fraction(0), Fraction(1)):
                continue
            active = [
                value
                for index, value in box.items()
                if all(
                    status == -1
                    or index[axis] == (0 if status == 0 else degrees[axis])
                    for axis, status in enumerate(statuses)
                )
            ]
            if not active:
                raise AssertionError(
                    f"empty physical face: {label} {path} {statuses}"
                )
            if max(active) <= 0:
                raise AssertionError(
                    f"non-strict physical face: {label} {path} {statuses}"
                )
    print(
        f"PASS {label} Bernstein cover: {len(paths)} boxes, "
        f"maximum depth {max(map(len, paths))}, degrees {degrees}, "
        "strict on physical faces"
    )


def main() -> None:
    atomic_symbolic_checks()
    exact_labelled_subset_check()
    verify_paths(scalar_polynomial("low"), LOW_PATHS, "low-mark case")
    verify_paths(scalar_polynomial("high"), HIGH_PATHS, "high-mark case")
    print("ALL HIGHER-RANK SEPARATION CERTIFICATES PASS")


if __name__ == "__main__":
    main()

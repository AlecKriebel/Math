#!/usr/bin/env python3
"""Rigorous certificate for the regular double point of the *auxiliary fourteen-history map*.

The stochastic-process theorem in the manuscript uses a corrected map and is
proved analytically.  This verifier concerns the separate formula-audit result:
the auxiliary fourteen-history compact map has a regular double point.

All transcendental interval operations use MPFR with directed rounding through
``mpfr_interval.py``.  No Python binary float participates in a certified test.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from mpfr_interval import (
    Interval,
    Jet,
    det3,
    identity3,
    interval_matmul,
    interval_matvec,
)

HERE = os.path.dirname(os.path.abspath(__file__))
CERT_PATH = os.path.join(HERE, "certificate.json")


def frac_interval(n: int, d: int = 1) -> Interval:
    return Interval.fraction(n, d)


def parse_rational(text: str) -> Interval:
    if "/" in text:
        a, b = text.split("/", 1)
        return frac_interval(int(a), int(b))
    return Interval.decimal(text)


def target_intervals() -> list[Interval]:
    sqrt10 = frac_interval(10).sqrt()
    A = frac_interval(1017, 2500) - sqrt10 / 12500
    B = frac_interval(1013, 2500) - 3 * sqrt10 / 12500
    C = frac_interval(2543, 10000)
    return [A, B, C]


def table_map(q: Jet, x: Jet, y: Jet) -> list[Jet]:
    one = 1
    two = 2
    three = 3
    xq = x.pow(q)
    x2 = x * x
    x3 = x2 * x
    xp2 = xq * x2
    y2 = y * y
    K = q * (two * q + one) / (q + two)

    A = (
        K
        + (one - q) * x2 * (one + (one - xq) * y2)
        + q * (one - q) * xp2 / (q + two)
    )
    B = (
        K
        + (one - q) * x2 * (one + (three - xq) * y2) / two
        - (one - q) * (two - q) * xp2 / (two * (q + two))
    )
    C = (
        q * q
        + q * (one - q) * x2
        + two * q * (one - q) * x2 * y2
        + (one - q) * (one - two * q) * x3 * y2
    )
    return [A, B, C]


def eval_map_and_jac(box: Sequence[Interval]) -> tuple[list[Interval], list[list[Interval]]]:
    vars_ = [Jet.variable(box[i], i) for i in range(3)]
    out = table_map(*vars_)
    vals = [z.val for z in out]
    jac = [[out[i].der[j] for j in range(3)] for i in range(3)]
    return vals, jac


def interval_matrix_from_decimals(rows: Sequence[Sequence[str]]) -> list[list[Interval]]:
    return [[Interval.decimal(v) for v in row] for row in rows]


@dataclass(frozen=True)
class Q10:
    """Exact a+b*sqrt(10), with a,b in Q."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = as_q10(other)
        return Q10(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q10(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_q10(other))

    def __rsub__(self, other):
        return as_q10(other) - self

    def __mul__(self, other):
        other = as_q10(other)
        return Q10(self.a * other.a + 10 * self.b * other.b,
                   self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def inverse(self):
        den = self.a * self.a - 10 * self.b * self.b
        if den == 0:
            raise ZeroDivisionError
        return Q10(self.a / den, -self.b / den)

    def __truediv__(self, other):
        return self * as_q10(other).inverse()

    def __rtruediv__(self, other):
        return as_q10(other) / self


def as_q10(value) -> Q10:
    if isinstance(value, Q10):
        return value
    if isinstance(value, Fraction):
        return Q10(value, Fraction(0))
    if isinstance(value, int):
        return Q10(Fraction(value), Fraction(0))
    raise TypeError(type(value))


def exact_anchor_check() -> None:
    q = Q10(Fraction(1, 2))
    x = Q10(Fraction(1, 10))
    y = Q10(Fraction(3, 5))
    sqrt10 = Q10(Fraction(0), Fraction(1))
    xq = sqrt10 / 10  # sqrt(1/10) = sqrt(10)/10 exactly.
    x2 = x * x
    x3 = x2 * x
    xp2 = xq * x2
    y2 = y * y
    K = q * (2 * q + 1) / (q + 2)
    A = K + (1 - q) * x2 * (1 + (1 - xq) * y2) + q * (1 - q) * xp2 / (q + 2)
    B = K + (1 - q) * x2 * (1 + (3 - xq) * y2) / 2 - (1 - q) * (2 - q) * xp2 / (2 * (q + 2))
    C = q * q + q * (1 - q) * x2 + 2 * q * (1 - q) * x2 * y2 + (1 - q) * (1 - 2 * q) * x3 * y2

    A0 = Q10(Fraction(1017, 2500), Fraction(-1, 12500))
    B0 = Q10(Fraction(1013, 2500), Fraction(-3, 12500))
    C0 = Q10(Fraction(2543, 10000))
    assert A == A0 and B == B0 and C == C0

    # Independently verify the site-pattern inverse transform supplied in the
    # derivation, still exactly in Q(sqrt(10)).
    p0 = (1 + 3 * A + 6 * B + 6 * C) / 16
    p12 = 3 * (1 + 3 * A - 2 * B - 2 * C) / 16
    p13 = 3 * (1 - A + 2 * B - 2 * C) / 16
    pD = 3 * (1 - A - 2 * B + 2 * C) / 8
    assert p0 == Q10(Fraction(30887, 80000), Fraction(-21, 200000))
    assert p12 == Q10(Fraction(13521, 80000), Fraction(9, 200000))
    assert p13 == Q10(Fraction(537, 3200), Fraction(-3, 40000))
    assert pD == Q10(Fraction(4371, 40000), Fraction(21, 100000))
    assert p0 + p12 + 2 * p13 + pD == Q10(Fraction(1))


def report_interval(label: str, x: Interval) -> None:
    lo, hi = x.approx()
    print(f"  {label}: [{lo:.17e}, {hi:.17e}]")


def main() -> int:
    with open(CERT_PATH, "r", encoding="utf-8") as fh:
        cert = json.load(fh)

    print("LGT-JC69 auxiliary-table-map regular-double-point verifier")
    print("MPFR directed rounding; precision:", cert["precision_bits"], "bits")

    exact_anchor_check()
    print("PASS exact anchor and exact target/site-pattern algebra")

    names = ["q", "x", "y"]
    box = [Interval.from_bounds(*cert["second_box"][name]) for name in names]
    center = [Interval.decimal(v) for v in cert["center"]]
    Y = interval_matrix_from_decimals(cert["preconditioner"])
    target = target_intervals()

    zero = Interval.zero()
    one = Interval.one()
    inside_cube = all(z.lo.cmp(zero.lo) > 0 and z.hi.cmp(one.hi) < 0 for z in box)
    assert inside_cube
    anchor = [frac_interval(1, 2), frac_interval(1, 10), frac_interval(3, 5)]
    assert any(box[i].disjoint(anchor[i]) for i in range(3))
    print("PASS second box is strictly inside (0,1)^3 and disjoint from anchor")

    vals_X, J_X = eval_map_and_jac(box)
    det_X = det3(J_X)
    assert det_X.strictly_negative()
    print("PASS Jacobian determinant is negative throughout second box")
    report_interval("det DF(B2)", det_X)

    _, J_anchor = eval_map_and_jac(anchor)
    det_anchor = det3(J_anchor)
    assert det_anchor.strictly_positive()
    print("PASS Jacobian determinant is positive at exact anchor")
    report_interval("det DF(z1)", det_anchor)

    det_Y = det3(Y)
    assert not det_Y.contains_zero()

    vals_c, _ = eval_map_and_jac(center)
    Gc = [vals_c[i] - target[i] for i in range(3)]
    YGc = interval_matvec(Y, Gc)
    base = [center[i] - YGc[i] for i in range(3)]

    YJ = interval_matmul(Y, J_X)
    I = identity3()
    E = [[I[i][j] - YJ[i][j] for j in range(3)] for i in range(3)]
    delta = [box[i] - center[i] for i in range(3)]
    correction = interval_matvec(E, delta)
    K = [base[i] + correction[i] for i in range(3)]

    for i in range(3):
        if not K[i].strict_subset_of(box[i]):
            print(f"FAIL Krawczyk coordinate {i} is not strictly inside box")
            report_interval("K", K[i])
            report_interval("X", box[i])
            return 1

    print("PASS Krawczyk operator is strictly contained in the box")
    for name, kval, xval in zip(names, K, box):
        report_interval(f"K_{name}", kval)
        report_interval(f"B_{name}", xval)
        kw = Interval(kval.hi.copy(), kval.hi.copy()) - Interval(kval.lo.copy(), kval.lo.copy())
        bw = Interval(xval.hi.copy(), xval.hi.copy()) - Interval(xval.lo.copy(), xval.lo.copy())
        ratio = kw / bw
        _, ratio_hi = ratio.approx()
        print(f"    width(K)/width(B) <= {ratio_hi:.3e}")

    mu = frac_interval(4, 3)
    qI, xI, yI = box
    lamI = mu * qI / (1 - qI)
    t1I = -(1 - qI) * xI.log() / mu
    t2I = t1I - (1 - qI) * yI.log() / mu
    print("Certified enclosure of the second original-parameter triple:")
    report_interval("lambda", lamI)
    report_interval("t1", t1I)
    report_interval("t2", t2I)

    print("PASS exactly one zero of F-(A0,B0,C0) lies in B2")
    print("PASS both preimages are regular and distinct")
    print("ALL CERTIFIED CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print("FAIL assertion", exc, file=sys.stderr)
        raise

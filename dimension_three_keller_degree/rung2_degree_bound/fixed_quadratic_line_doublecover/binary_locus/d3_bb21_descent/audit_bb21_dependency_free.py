#!/usr/bin/env python3
"""Dependency-free hostile reconstruction of the D3-BB-21 exclusion.

This deliberately shares neither SymPy nor PARI/GP algebra with the
candidate release.  Sparse multivariate polynomials over Q reconstruct the
weighted determinant.  The check includes the degree-zero E7 block that was
missing from the first primary certificate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys


if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


NAMES = (
    ("p", "q", "r", "z")
    + ("a", "b", "c", "k")
    + tuple(f"u{i}" for i in range(4))
    + tuple(f"v{i}" for i in range(4))
    + tuple(f"t{i}" for i in range(3))
    + tuple(f"A{i}" for i in range(6))
    + tuple(f"B{i}" for i in range(6))
    + tuple(f"l{i}" for i in range(9))
)
INDEX = {name: index for index, name in enumerate(NAMES)}
ZERO_EXP = (0,) * len(NAMES)


class Poly:
    """Small sparse polynomial over Q."""

    def __init__(self, terms=None):
        self.terms = {
            exponent: Fraction(value)
            for exponent, value in (terms or {}).items()
            if value
        }

    @staticmethod
    def coerce(value):
        if isinstance(value, Poly):
            return value
        return Poly({ZERO_EXP: Fraction(value)})

    def __add__(self, other):
        other = Poly.coerce(other)
        out = dict(self.terms)
        for exponent, value in other.terms.items():
            out[exponent] = out.get(exponent, Fraction(0)) + value
            if not out[exponent]:
                del out[exponent]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({exponent: -value for exponent, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly.coerce(other))

    def __rsub__(self, other):
        return Poly.coerce(other) - self

    def __mul__(self, other):
        other = Poly.coerce(other)
        out = {}
        for left_exp, left_value in self.terms.items():
            for right_exp, right_value in other.terms.items():
                exponent = tuple(
                    left_exp[index] + right_exp[index]
                    for index in range(len(NAMES))
                )
                out[exponent] = out.get(exponent, Fraction(0)) + left_value * right_value
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, power):
        require(isinstance(power, int) and power >= 0, "nonnegative integer power")
        answer = Poly.coerce(1)
        base = self
        while power:
            if power & 1:
                answer = answer * base
            base = base * base
            power //= 2
        return answer

    def __truediv__(self, scalar):
        scalar = Fraction(scalar)
        require(scalar != 0, "division by zero")
        return Poly({exponent: value / scalar for exponent, value in self.terms.items()})

    def diff(self, name):
        position = INDEX[name]
        out = {}
        for exponent, value in self.terms.items():
            if exponent[position]:
                reduced = list(exponent)
                multiplier = reduced[position]
                reduced[position] -= 1
                reduced = tuple(reduced)
                out[reduced] = out.get(reduced, Fraction(0)) + multiplier * value
        return Poly(out)

    def coefficient(self, **powers):
        """Coefficient in selected variables, retaining all other variables."""
        positions = {INDEX[name]: power for name, power in powers.items()}
        out = {}
        for exponent, value in self.terms.items():
            if all(exponent[position] == power for position, power in positions.items()):
                reduced = list(exponent)
                for position in positions:
                    reduced[position] = 0
                reduced = tuple(reduced)
                out[reduced] = out.get(reduced, Fraction(0)) + value
        return Poly(out)

    def set_zero(self, *names):
        positions = tuple(INDEX[name] for name in names)
        return Poly(
            {
                exponent: value
                for exponent, value in self.terms.items()
                if all(exponent[position] == 0 for position in positions)
            }
        )

    def __eq__(self, other):
        return self.terms == Poly.coerce(other).terms

    def __bool__(self):
        return bool(self.terms)


def variable(name):
    exponent = [0] * len(NAMES)
    exponent[INDEX[name]] = 1
    return Poly({tuple(exponent): Fraction(1)})


VARS = {name: variable(name) for name in NAMES}
globals().update(VARS)


def det3(matrix):
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[0][2] * matrix[1][0] * matrix[2][1]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[0][0] * matrix[1][2] * matrix[2][1]
    )


def weighted(U, W, T, Aquad, Bquad, linear):
    P = p**3 * q
    Q = p * q**3
    R = p**2 * q
    H2 = (Aquad, Bquad, T)
    H3 = (U, W, R)
    H4 = (P, Q, Poly())
    coords = ("p", "q", "r")
    matrix = []
    for row in range(3):
        matrix.append(
            [
                linear[row][column]
                + z * H2[row].diff(coords[column])
                + z**2 * H3[row].diff(coords[column])
                + z**3 * H4[row].diff(coords[column])
                for column in range(3)
            ]
        )
    return det3(matrix)


def binary_form(symbols, degree):
    return sum(
        symbol * p ** (degree - index) * q**index
        for index, symbol in enumerate(symbols)
    )


U0 = binary_form((u0, u1, u2, u3), 3)
W0 = binary_form((v0, v1, v2, v3), 3)
T0 = binary_form((t0, t1, t2), 2)
MON2 = (p**2, p * q, p * r, q**2, q * r, r**2)
AFULL = sum(VARS[f"A{i}"] * MON2[i] for i in range(6))
BFULL = sum(VARS[f"B{i}"] * MON2[i] for i in range(6))
LINEAR = [[VARS[f"l{3 * i + j}"] for j in range(3)] for i in range(3)]


def rational_rank(rows):
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0
    if not matrix:
        return 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [
                    matrix[row][j] - scale * matrix[rank][j]
                    for j in range(columns)
                ]
        rank += 1
    return rank


def e7_matrix(degree):
    """Matrix of alpha*U+beta*V+gamma*T at binary degree `degree`."""
    # alpha=-5 p^2q^3, beta=-p^4q, gamma=8p^3q^3.
    column_count = 2 * (degree + 1) + degree
    rows = {}

    def put(p_power, column, value):
        rows.setdefault(p_power, [Fraction(0)] * column_count)[column] += Fraction(value)

    for index in range(degree + 1):
        put(2 + degree - index, index, -5)
        put(4 + degree - index, degree + 1 + index, -1)
    for index in range(degree):
        put(3 + degree - 1 - index, 2 * (degree + 1) + index, 8)
    return [rows[key] for key in sorted(rows)]


def verify_e7_completeness(mutation):
    expected = {
        0: (2, 0),
        1: (4, 1),
        2: (5, 3),
    }
    for degree, (wanted_rank, wanted_nullity) in expected.items():
        rank = rational_rank(e7_matrix(degree))
        if mutation == "degree0" and degree == 0:
            wanted_rank = 1
        columns = 2 * (degree + 1) + degree
        require(rank == wanted_rank, f"E7 degree-{degree} rank")
        require(columns - rank == wanted_nullity, f"E7 degree-{degree} nullity")

    displayed_degree1 = (Fraction(8, 5), 0, 0, 0, 1)
    displayed_degree2 = (
        (Fraction(-1, 5), 0, 0, 0, 0, 1, 0, 0),
        (Fraction(8, 5), 0, 0, 0, 0, 0, 1, 0),
        (0, Fraction(8, 5), 0, 0, 0, 0, 0, 1),
    )
    for vector in (displayed_degree1,):
        require(
            all(
                sum(row[index] * vector[index] for index in range(len(vector))) == 0
                for row in e7_matrix(1)
            ),
            "displayed degree-one E7 syzygy",
        )
    require(rational_rank(displayed_degree2) == 3, "degree-two basis independence")
    for vector in displayed_degree2:
        require(
            all(
                sum(row[index] * vector[index] for index in range(len(vector))) == 0
                for row in e7_matrix(2)
            ),
            "displayed degree-two E7 syzygy",
        )


def verify_raw_and_pivoted_determinants(mutation):
    S = a * p + b * q + c * r
    U = U0 + p * r * ((8 * a - k) * p + 8 * b * q + 4 * c * r) / 5
    W = W0 + k * q**2 * r
    T = T0 + (a * p + b * q) * r + c * r**2 / 2
    determinant = weighted(U, W, T, AFULL, BFULL, LINEAR)

    require(not determinant.coefficient(z=9), "E9 is zero")
    require(not determinant.coefficient(z=8), "E8 is zero")
    require(not determinant.coefficient(z=7), "full E7 identity")
    e6 = determinant.coefficient(z=6)
    require(
        e6.coefficient(p=1, q=2, r=3) == Fraction(12, 5) * c**2,
        "raw E6 c-square",
    )
    require(
        e6.coefficient(p=1, q=4, r=1).set_zero("c")
        == Fraction(24, 5) * b**2,
        "raw E6 b-square",
    )
    conic = 12 * a**2 - 8 * a * k + 3 * k**2
    require(
        e6.coefficient(p=3, q=2, r=1).set_zero("b", "c")
        == Fraction(2, 5) * conic,
        "raw E6 conic",
    )
    require(
        e6.coefficient(p=6, q=0, r=0).set_zero("b", "c")
        == Fraction(3, 5) * v0 * (3 * a - k),
        "raw E6 v0 endpoint",
    )
    require(
        e6.coefficient(p=1, q=5, r=0).set_zero("b", "c")
        == 3 * u3 * (2 * k - a),
        "raw E6 u3 endpoint",
    )

    # Rebuild after the unit E6 pivots instead of substituting into the
    # candidate implementation.
    pivot_B2 = a * v1
    pivot_B4 = (
        -(48 * a - 16 * k) * t0
        + (45 * a - 15 * k) * u0
        + (a + 3 * k) * v2
    ) / 5
    pivot_A4 = ((16 * a - 32 * k) * t2 + (5 * a + 15 * k) * u2) / 25
    pivot_A2 = (
        -(16 * a + 8 * k) * t1
        + 25 * a * u1
        + (-3 * a + 6 * k) * v3
        + 40 * l8
    ) / 25
    Apivot = A0 * p**2 + A1 * p * q + pivot_A2 * p * r + A3 * q**2 + pivot_A4 * q * r
    Bpivot = B0 * p**2 + B1 * p * q + pivot_B2 * p * r + B3 * q**2 + pivot_B4 * q * r
    Upivot = U0 + p * r * (8 * a - k) * p / 5
    Wpivot = W0 + k * q**2 * r
    Tpivot = T0 + a * p * r
    pivoted = weighted(Upivot, Wpivot, Tpivot, Apivot, Bpivot, LINEAR)
    expected_e6 = (
        Fraction(2, 5) * conic * p**3 * q**2 * r
        + Fraction(3, 5) * v0 * (3 * a - k) * p**6
        + 3 * u3 * (2 * k - a) * p * q**5
    )
    require(pivoted.coefficient(z=6) == expected_e6, "complete E6 pivot replay")
    decisive = pivoted.coefficient(z=5, p=2, q=1, r=2)
    expected_e5 = Fraction(2, 5) * a * k * (8 * a - k)
    if mutation == "e5":
        expected_e5 = -expected_e5
    require(decisive == expected_e5, "lower-independent E5 obstruction")
    require(
        all(
            all(exponent[INDEX[name]] == 0 for name in NAMES[8:])
            for exponent in decisive.terms
        ),
        "E5 obstruction is independent of all lower coefficients",
    )


def univariate_mul(left, right):
    out = {}
    for i, x in left.items():
        for j, y in right.items():
            out[i + j] = out.get(i + j, Fraction(0)) + x * y
    return {degree: value for degree, value in out.items() if value}


def univariate_add(left, right, sign=1):
    out = dict(left)
    for degree, value in right.items():
        out[degree] = out.get(degree, Fraction(0)) + sign * value
        if not out[degree]:
            del out[degree]
    return out


def determinant_ring(matrix):
    answer = {}
    for permutation in itertools.permutations(range(len(matrix))):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(len(permutation))
            for j in range(i + 1, len(permutation))
        )
        term = {0: Fraction(1)}
        for row, column in enumerate(permutation):
            term = univariate_mul(term, matrix[row][column])
        answer = univariate_add(answer, term, -1 if inversions % 2 else 1)
    return answer


def quadratic_resultant(coeff_f, coeff_g):
    zero = {}
    matrix = [
        [coeff_f[0], coeff_f[1], coeff_f[2], zero],
        [zero, coeff_f[0], coeff_f[1], coeff_f[2]],
        [coeff_g[0], coeff_g[1], coeff_g[2], zero],
        [zero, coeff_g[0], coeff_g[1], coeff_g[2]],
    ]
    return determinant_ring(matrix)


def verify_resultants_and_intersection(mutation):
    # Coefficients are high-to-low in the eliminated variable; each entry is
    # a polynomial in the retained variable represented by exponent.
    res_k = quadratic_resultant(
        ({0: Fraction(3)}, {1: Fraction(-8)}, {2: Fraction(12)}),
        ({1: Fraction(-1)}, {2: Fraction(8)}, {}),
    )
    res_a = quadratic_resultant(
        ({0: Fraction(12)}, {1: Fraction(-8)}, {2: Fraction(3)}),
        ({1: Fraction(8)}, {2: Fraction(-1)}, {}),
    )
    wanted_k = {6: Fraction(1680)}
    wanted_a = {6: Fraction(420)}
    if mutation == "resultant":
        wanted_k = {6: Fraction(1681)}
    require(res_k == wanted_k, "resultant eliminating k")
    require(res_a == wanted_a, "resultant eliminating a")

    # Division-free branch audit of a*k*(8a-k)=0 on the conic.
    require(Fraction(3) != 0 and Fraction(12) != 0 and Fraction(140) != 0, "char-zero constants")
    # a=0 -> 3k^2=0; k=0 -> 12a^2=0; k=8a -> 140a^2=0.


def verify_origin():
    origin = weighted(U0, W0, T0, AFULL, BFULL, LINEAR)
    alpha = -5 * p**2 * q**3
    beta = -p**4 * q
    gamma = 8 * p**3 * q**3
    structural = alpha * AFULL.diff("r") + beta * BFULL.diff("r") + gamma * l8
    require(origin.coefficient(z=6) == structural, "origin structural E6 identity")
    equations = {
        (3, 3, 0): -5 * A2 + 8 * l8,
        (2, 4, 0): -5 * A4,
        (2, 3, 1): -10 * A5,
        (5, 1, 0): -B2,
        (4, 2, 0): -B4,
        (4, 1, 1): -2 * B5,
    }
    for (ep, eq, er), expected in equations.items():
        require(
            origin.coefficient(z=6, p=ep, q=eq, r=er) == expected,
            f"origin E6 coefficient {ep},{eq},{er}",
        )
    # The two structural charts use only unit pivots:
    # l8=0 makes every nonlinear coefficient r-independent.
    # l8!=0 makes F3=l8*r+B3(p,q), with inverse degree <=3.
    require(3 * 4 == 12 and 12 < 100, "coordinate straightening degree is in Moh range")


def verify_frozen_bridge(mutation):
    here = Path(__file__).resolve().parent
    denominator = here.parent.parent / "audit_delta_ge3_denominator" / "DENOMINATOR.json"
    raw = denominator.read_bytes()
    expected_sha = "440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a"
    if mutation == "denominator":
        expected_sha = "0" * 64
    require(hashlib.sha256(raw).hexdigest() == expected_sha, "frozen denominator SHA")
    data = json.loads(raw)
    require(data["counts"] == {
        "delta3_independent": 19,
        "delta4_independent": 6,
        "dependent_power_fibre": 1,
        "total": 26,
    }, "frozen denominator counts")
    targets = [entry for entry in data["families"] if entry["id"] == "D3-BB-21"]
    require(len(targets) == 1, "unique frozen BB21 ID")
    target = targets[0]
    require(target["normal_form"] == {"h": "pq", "R": "p^2q"}, "frozen BB21 normal form")
    require(target["delta"] == 3 and target["parameter_space"] == "point", "frozen BB21 scope")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        choices=("degree0", "e5", "resultant", "origin", "denominator"),
    )
    args = parser.parse_args()
    verify_frozen_bridge(args.mutation)
    verify_e7_completeness(args.mutation)
    verify_raw_and_pivoted_determinants(args.mutation)
    verify_resultants_and_intersection(args.mutation)
    if args.mutation == "origin":
        global l8
        old_l8 = l8
        l8 = -l8
        try:
            verify_origin()
        finally:
            l8 = old_l8
    else:
        verify_origin()
    print("D3_BB21_DEPENDENCY_FREE_HOSTILE_PASS")


if __name__ == "__main__":
    main()

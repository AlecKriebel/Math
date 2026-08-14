#!/usr/bin/env python3
"""Independent exact constructor for the PARTITION-to-mass-action reduction."""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import sympy as sp


@dataclass(frozen=True)
class OpenCubeFamily:
    original: tuple[int, ...]
    k: int
    m: int
    a: sp.Matrix
    gamma: int
    beta: sp.Rational
    Q: sp.Matrix

    @property
    def base_dimension(self) -> int:
        return self.m + 1

    @property
    def parameter_dimension(self) -> int:
        return 2 * self.m


@dataclass(frozen=True)
class Lift:
    family: OpenCubeFamily
    B0: sp.Matrix
    U: sp.Matrix
    W: sp.Matrix
    alpha: sp.Rational

    @property
    def dimension(self) -> int:
        return self.B0.rows + self.W.rows


def choose_square_dimension(length: int) -> tuple[int, int]:
    if length < 1:
        raise ValueError("PARTITION requires at least one positive integer")
    k = math.isqrt(length) + 1
    while k * k <= length:
        k += 1
    return k, k * k


def make_family(numbers: Sequence[int]) -> OpenCubeFamily:
    if not numbers or any(isinstance(a, bool) or int(a) != a or a <= 0 for a in numbers):
        raise ValueError("numbers must be positive integers")
    original = tuple(int(a) for a in numbers)
    k, m = choose_square_dimension(len(original))
    padded = original + (0,) * (m - len(original))
    a = sp.Matrix(padded)
    gamma = int((a.T * a)[0])
    beta = sp.Rational(1) - sp.Rational(1, 2 * m * (1 + gamma))
    Q = sp.eye(m) + a * a.T
    return OpenCubeFamily(original, k, m, a, gamma, beta, Q)


def partition_witness(numbers: Sequence[int]) -> tuple[int, ...] | None:
    for signs in itertools.product((-1, 1), repeat=len(numbers)):
        if sum(a * t for a, t in zip(numbers, signs)) == 0:
            return tuple(signs)
    return None


def minimum_partition_square(numbers: Sequence[int]) -> int:
    return min(sum(a * t for a, t in zip(numbers, signs)) ** 2 for signs in itertools.product((-1, 1), repeat=len(numbers)))


def open_cube_matrix(family: OpenCubeFamily, q: Sequence[sp.Expr]) -> sp.Matrix:
    if len(q) != 2 * family.m:
        raise ValueError("q must contain y followed by x")
    y = sp.Matrix(q[: family.m])
    x = sp.Matrix(q[family.m :])
    top = (-family.k * family.Q).row_join(y)
    bottom = x.T.row_join(sp.Matrix([[family.k * family.beta]]))
    return top.col_join(bottom)


def interior_q(family: OpenCubeFamily, original_signs: Sequence[int]) -> tuple[sp.Rational, ...]:
    if len(original_signs) != len(family.original):
        raise ValueError("wrong sign-vector length")
    padded = tuple(int(t) for t in original_signs) + (1,) * (family.m - len(original_signs))
    if any(t not in (-1, 1) for t in padded) or sum(a * t for a, t in zip(family.original, original_signs)) != 0:
        raise ValueError("not a partition witness")
    r = (sp.Integer(1) + family.beta) / 2
    y = tuple(-r * t for t in padded)
    x = tuple(r * t for t in padded)
    return y + x


def make_lift(family: OpenCubeFamily, alpha: sp.Expr = 1) -> Lift:
    alpha = sp.Rational(alpha)
    n0 = family.m + 1
    B0 = sp.diag(-family.k * family.Q, sp.Matrix([[family.k * family.beta]]))
    columns: list[sp.Matrix] = []
    rows: list[sp.Matrix] = []
    for i in range(family.m):
        u = sp.zeros(n0, 1); u[i] = 1
        w = sp.zeros(1, n0); w[0, family.m] = 1
        columns.append(u); rows.append(w)
    for i in range(family.m):
        u = sp.zeros(n0, 1); u[family.m] = 1
        w = sp.zeros(1, n0); w[0, i] = 1
        columns.append(u); rows.append(w)
    U = sp.Matrix.hstack(*columns)
    W = sp.Matrix.vstack(*rows)
    return Lift(family, B0, U, W, alpha)


def X_matrix(lift: Lift, q: Sequence[sp.Expr]) -> sp.Matrix:
    if len(q) != lift.W.rows:
        raise ValueError("wrong q length")
    return sp.diag(*map(sp.sympify, q)) * lift.W


def lifted_matrix(lift: Lift, q: Sequence[sp.Expr]) -> sp.Matrix:
    X = X_matrix(lift, q)
    top = lift.B0.row_join(lift.U)
    bottom = (X * (lift.B0 + lift.alpha * sp.eye(lift.B0.rows))).row_join(X * lift.U - lift.alpha * sp.eye(lift.W.rows))
    return top.col_join(bottom)


def conjugator(lift: Lift, q: Sequence[sp.Expr]) -> sp.Matrix:
    """Return the exact lower-unitriangular similarity matrix P(q)."""
    X = X_matrix(lift, q)
    n0, d = lift.B0.rows, lift.W.rows
    top = sp.eye(n0).row_join(sp.zeros(n0, d))
    bottom = (-X).row_join(sp.eye(d))
    return top.col_join(bottom)


def triangular_form(lift: Lift, q: Sequence[sp.Expr]) -> sp.Matrix:
    B = open_cube_matrix(lift.family, q)
    n0, d = lift.B0.rows, lift.W.rows
    return B.row_join(lift.U).col_join(sp.zeros(d, n0).row_join(-lift.alpha * sp.eye(d)))


def hurwitz_determinants(matrix: sp.Matrix) -> tuple[sp.Expr, ...]:
    lam = sp.symbols("lambda")
    poly = sp.Poly(matrix.charpoly(lam).as_expr(), lam)
    coeffs = poly.all_coeffs()
    if coeffs[0] != 1:
        coeffs = [sp.simplify(c / coeffs[0]) for c in coeffs]
    n = matrix.rows
    a = [sp.Integer(1)] + coeffs[1:]
    # Hurwitz matrix H_ij = a_{2i-j} in one-based indexing, with a_0=1.
    H = sp.zeros(n)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            index = 2 * i - j
            if 0 <= index <= n:
                H[i - 1, j - 1] = a[index]
    return tuple(sp.factor(H[:r, :r].det()) for r in range(1, n + 1))


def is_hurwitz_exact(matrix: sp.Matrix) -> bool:
    return all(delta > 0 for delta in hurwitz_determinants(matrix))

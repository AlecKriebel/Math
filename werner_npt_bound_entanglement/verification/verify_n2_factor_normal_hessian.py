#!/usr/bin/env python3
"""Exact audit of the factor-normal fixed-left Hessian.

Only the Python standard library is used.  Gaussian rationals are
represented as pairs of Fractions.  The script derives the Schur
Hessian directly from the two-copy partial-trace form at one generic
complex normal vector and compares it with the invariant formula in
the note.  It also checks the spectral polynomial of the factor-plane
compression and all effective-neighborhood constant arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class G:
    re: F = F(0)
    im: F = F(0)

    def __add__(self, other: object) -> G:
        other = to_g(other)
        return G(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self) -> G:
        return G(-self.re, -self.im)

    def __sub__(self, other: object) -> G:
        return self + (-to_g(other))

    def __rsub__(self, other: object) -> G:
        return to_g(other) - self

    def __mul__(self, other: object) -> G:
        other = to_g(other)
        return G(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def conj(self) -> G:
        return G(self.re, -self.im)


def to_g(value: object) -> G:
    if isinstance(value, G):
        return value
    return G(F(value))  # type: ignore[arg-type]


Z = G()
O = G(F(1))


Matrix = list[list[G]]


def zeros(n: int, m: int) -> Matrix:
    return [[Z for _ in range(m)] for _ in range(n)]


def eye(n: int) -> Matrix:
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = O
    return out


def adjoint(a: Matrix) -> Matrix:
    return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c: object, a: Matrix) -> Matrix:
    return [[to_g(c) * x for x in row] for row in a]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum((x * y for x, y in zip(row, col)), Z) for col in bt] for row in a]


def trace(a: Matrix) -> G:
    return sum((a[i][i] for i in range(len(a))), Z)


def inner_vec(a: list[G], b: list[G]) -> G:
    return sum((x.conj() * y for x, y in zip(a, b)), Z)


def partial_basis(vector: list[G], input_index: int, site: int) -> Matrix:
    """Partial trace of |vector><input_index| on one qutrit."""
    k, ell = divmod(input_index, 3)
    out = zeros(3, 3)
    if site == 0:
        for j in range(3):
            out[j][ell] = vector[3 * k + j]
    else:
        for i in range(3):
            out[i][k] = vector[3 * i + ell]
    return out


def inner_matrix(a: Matrix, b: Matrix) -> G:
    return sum(
        (a[i][j].conj() * b[i][j] for i in range(len(a)) for j in range(len(a[0]))),
        Z,
    )


def endpoint_basis_pair(
    u: list[G], r: int, v: list[G], s: int
) -> G:
    value = inner_vec(u, v) if r == s else Z
    for site in (0, 1):
        value -= F(1, 2) * inner_matrix(
            partial_basis(u, r, site), partial_basis(v, s, site)
        )
    value += F(1, 4) * u[r].conj() * v[s]
    return value


def hbil(u: Matrix, v: Matrix) -> Matrix:
    # u and v are 9-by-2 frames; coordinate order is (physical,code).
    out = zeros(18, 18)
    for r in range(9):
        for c in range(2):
            left = [u[i][c] for i in range(9)]
            for s in range(9):
                for d in range(2):
                    right = [v[i][d] for i in range(9)]
                    out[2 * r + c][2 * s + d] = endpoint_basis_pair(
                        left, r, right, s
                    )
    return out


def norm_squared(values: list[G]) -> F:
    return sum((z.re * z.re + z.im * z.im for z in values), F(0))


def hermitian_inner(a: list[G], b: list[G]) -> G:
    return inner_vec(a, b)


def main() -> None:
    u0 = zeros(9, 2)
    u0[0][0] = O
    u0[1][1] = O
    h0 = hbil(u0, u0)

    # Spectrum 0^(3),(1/2)^(5),1^(10), hence H0^+=7H0-6H0^2.
    minimal = matmul(
        matmul(h0, add(h0, scale(-1, eye(18)))),
        add(scale(2, h0), scale(-1, eye(18))),
    )
    assert minimal == zeros(18, 18)
    assert trace(h0) == G(F(25, 2))
    assert trace(matmul(h0, h0)) == G(F(45, 4))
    h0_plus = add(scale(7, h0), scale(-6, matmul(h0, h0)))

    # One generic Gaussian-rational normal vector.  Since the formula
    # is a Hermitian quadratic identity, this is a compact arithmetic
    # audit rather than a numerical test.
    q = [
        G(F(1, 7), F(1, 11)),
        G(F(-2, 9), F(1, 13)),
        G(F(3, 10), F(-2, 15)),
        G(F(-1, 8), F(2, 17)),
        G(F(4, 13), F(1, 6)),
        G(F(-3, 14), F(-1, 9)),
        G(F(2, 11), F(3, 16)),
        G(F(-1, 5), F(1, 12)),
        G(F(3, 17), F(-2, 13)),
        G(F(1, 6), F(4, 19)),
    ]
    v = zeros(9, 2)
    v[3][0], v[4][1] = q[0], -q[0]
    v[4][0], v[3][1] = q[1], q[2]
    v[6][0], v[7][1] = q[3], -q[3]
    v[7][0], v[6][1] = q[4], q[5]
    v[5][0], v[5][1] = q[6], q[7]
    v[8][0], v[8][1] = q[8], q[9]

    gram = matmul(adjoint(v), v)
    u2 = scale(F(-1, 2), matmul(u0, gram))
    h1 = add(hbil(u0, v), hbil(v, u0))
    h2 = add(add(hbil(v, v), hbil(u0, u2)), hbil(u2, u0))

    k = zeros(18, 3)  # unnormalized kernel basis, norm squared two
    for p in range(3):
        k[6 * p][p] = O
        k[6 * p + 3][p] = O
    effective = scale(
        F(1, 2),
        add(
            matmul(matmul(adjoint(k), h2), k),
            scale(
                -1,
                matmul(
                    matmul(matmul(matmul(adjoint(k), h1), h0_plus), h1),
                    k,
                ),
            ),
        ),
    )

    a = [q[0], q[0], q[1], q[2]]  # first two encode sqrt(2)*q0
    d = [q[3], q[3], q[4], q[5]]
    b, c = q[6:8], q[8:10]
    aa, dd = norm_squared(a), norm_squared(d)
    bb, cc = norm_squared(b), norm_squared(c)
    cross = F(-1, 2) * hermitian_inner(a, d) + F(-1, 4) * hermitian_inner(b, c)
    predicted = zeros(3, 3)
    predicted[0][0] = G(F(aa + dd, 2) + F(3, 8) * (bb + cc))
    predicted[1][1] = G(F(dd, 2) + F(bb, 4) + F(cc, 2))
    predicted[2][2] = G(F(aa, 2) + F(bb, 2) + F(cc, 4))
    predicted[1][2] = cross
    predicted[2][1] = cross.conj()
    assert effective == predicted

    n = aa + dd + bb + cc
    assert trace(effective) == G(n + F(bb + cc, 8))

    # Exact constant arithmetic in the tubular estimate.
    t = F(1, 4096)
    assert F(1, 4) - 146 * t > F(1, 5)
    assert (F(1, 5) / (1 + 12 * t) ** 2) > F(1, 10)

    print("verified: exact factor-normal Hessian and local constants")


if __name__ == "__main__":
    main()

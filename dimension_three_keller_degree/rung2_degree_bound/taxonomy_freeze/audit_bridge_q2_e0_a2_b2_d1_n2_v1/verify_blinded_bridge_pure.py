#!/usr/bin/env python3
"""Dependency-free exact replay of the blinded conic-pencil obstruction maps."""

from __future__ import annotations

from fractions import Fraction


Monomial = tuple[int, int, int]
Poly = dict[Monomial, Fraction]


def poly(terms: dict[Monomial, int]) -> Poly:
    return {m: Fraction(c) for m, c in terms.items() if c}


def add(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, Fraction(0)) + c
        if not out[m]:
            del out[m]
    return out


def mul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(ma[i] + mb[i] for i in range(3))
            out[m] = out.get(m, Fraction(0)) + ca*cb
    return {m: c for m, c in out.items() if c}


def scale(a: Poly, c: int) -> Poly:
    return {m: Fraction(c)*v for m, v in a.items() if c*v}


def derivative(a: Poly, i: int) -> Poly:
    out: Poly = {}
    for m, c in a.items():
        if m[i]:
            mm = list(m)
            mm[i] -= 1
            out[tuple(mm)] = c*m[i]
    return out


def monomials(degree: int) -> list[Monomial]:
    return [
        (i, j, degree-i-j)
        for i in range(degree, -1, -1)
        for j in range(degree-i, -1, -1)
    ]


def cross_gradient(p: Poly, q: Poly) -> tuple[Poly, Poly, Poly]:
    dp = [derivative(p, i) for i in range(3)]
    dq = [derivative(q, i) for i in range(3)]
    return (
        add(mul(dp[1], dq[2]), scale(mul(dp[2], dq[1]), -1)),
        add(mul(dp[2], dq[0]), scale(mul(dp[0], dq[2]), -1)),
        add(mul(dp[0], dq[1]), scale(mul(dp[1], dq[0]), -1)),
    )


def derivation_matrix(p: Poly, q: Poly, degree: int) -> list[list[Fraction]]:
    source = monomials(degree)
    target = monomials(degree+1)
    target_index = {m: i for i, m in enumerate(target)}
    cross = cross_gradient(p, q)
    matrix = [[Fraction(0) for _ in source] for _ in target]
    for j, m in enumerate(source):
        basis = {m: Fraction(1)}
        image: Poly = {}
        for i in range(3):
            image = add(image, mul(cross[i], derivative(basis, i)))
        for mm, c in image.items():
            matrix[target_index[mm]][j] = c
    return matrix


def rref(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    A = [row[:] for row in matrix]
    if not A:
        return A, []
    rows, cols = len(A), len(A[0])
    pivots: list[int] = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if A[i][c]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        value = A[r][c]
        A[r] = [v/value for v in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                value = A[i][c]
                A[i] = [A[i][j] - value*A[r][j] for j in range(cols)]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return A, pivots


def nullspace(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    R, pivots = rref(matrix)
    cols = len(matrix[0])
    free = [c for c in range(cols) if c not in pivots]
    vectors = []
    for f in free:
        v = [Fraction(0)]*cols
        v[f] = Fraction(1)
        for r, p in enumerate(pivots):
            v[p] = -R[r][f]
        vectors.append(v)
    return vectors


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*matrix)]


def vector(f: Poly, degree: int) -> list[Fraction]:
    return [f.get(m, Fraction(0)) for m in monomials(degree)]


def mat_vec(matrix: list[list[Fraction]], v: list[Fraction]) -> list[Fraction]:
    return [sum(row[j]*v[j] for j in range(len(v))) for row in matrix]


X2 = poly({(2, 0, 0): 1})
Y2 = poly({(0, 2, 0): 1})
Z2 = poly({(0, 0, 2): 1})
XY = poly({(1, 1, 0): 1})
XZ = poly({(1, 0, 1): 1})
YZ = poly({(0, 1, 1): 1})

charts = {
    "P111": (add(X2, Z2), add(Y2, Z2), []),
    "P11_1": (
        add(X2, Y2),
        Z2,
        [poly({(0, 0, 3): 1}), mul(poly({(0, 0, 1): 1}), add(X2, Y2))],
    ),
    "P2_1": (add(Y2, Z2), add(scale(XY, 2), Z2), []),
    "P21": (
        Y2,
        add(scale(XY, 2), Z2),
        [poly({(0, 3, 0): 1}), mul(poly({(0, 1, 0): 1}), add(scale(XY, 2), Z2))],
    ),
    "P3": (scale(YZ, 2), add(scale(XZ, 2), Y2), []),
}


def main() -> None:
    for name, (p, q, expected_k3) in charts.items():
        M2 = derivation_matrix(p, q, 2)
        M3 = derivation_matrix(p, q, 3)
        rank2 = len(rref(M2)[1])
        rank3 = len(rref(M3)[1])
        k2 = nullspace(M2)
        k3 = nullspace(M3)
        ck2 = nullspace(transpose(M2))
        ck3 = nullspace(transpose(M3))
        assert (rank2, len(k2), len(ck2)) == (4, 2, 6)
        expected3 = (8, 2, 7) if expected_k3 else (10, 0, 5)
        assert (rank3, len(k3), len(ck3)) == expected3
        assert mat_vec(M2, vector(p, 2)) == [0]*10
        assert mat_vec(M2, vector(q, 2)) == [0]*10
        for f in expected_k3:
            assert mat_vec(M3, vector(f, 3)) == [0]*15
        print(
            f"PASS {name}: D2 rank/kernel/cokernel=4/2/6; "
            f"D3={rank3}/{len(k3)}/{len(ck3)}"
        )
    print("PASS: dependency-free Fraction/RREF replay of all exact obstruction maps")


if __name__ == "__main__":
    main()

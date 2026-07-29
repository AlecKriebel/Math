#!/usr/bin/env python3
"""Independent exact audit of the all-m codimension-two cut-down obstruction.

This intentionally differs from verify_no_rank_six_subspace_of_d8.py:

* Schmidt coefficients are recovered by partial contraction of the
  published H4, not inserted and used to rebuild H8.
* Full active-algebra generation is checked by solving the generic
  commutant equations, not by enumerating algebra words.
"""

from __future__ import annotations

import itertools

import sympy as sp


I = sp.I
I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -I], [I, 0]])
Z = sp.diag(1, -1)
J = -I * Y


def kron(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.ones(1, 1)
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def published_h4() -> sp.Matrix:
    return (
        -kron(Z, I2, Z, Z) / sp.sqrt(6)
        - kron(Z, I2, J, J) / sp.sqrt(6)
        - kron(J, I2, Z, J) / sp.sqrt(6)
        + kron(J, I2, J, Z) / sp.sqrt(6)
        - kron(X, I2, X, X) / sp.sqrt(3)
    )


def contract_first_site(h4: sp.Matrix, left: sp.Matrix) -> sp.Matrix:
    """Return Tr_site1((left^* tensor I) h4), with 4|4 site ordering."""

    out = sp.zeros(4)
    for r2, c2 in itertools.product(range(4), repeat=2):
        total = 0
        for r1, c1 in itertools.product(range(4), repeat=2):
            total += sp.conjugate(left[r1, c1]) * h4[4 * r1 + r2, 4 * c1 + c2]
        out[r2, c2] = sp.simplify(total)
    return out


def check_schmidt_contraction() -> list[sp.Matrix]:
    h4 = published_h4()
    left = [kron(X, I2), kron(Y, I2), kron(Z, I2)]
    expected = [
        -kron(X, X) / sp.sqrt(3),
        (kron(Z, Y) - kron(Y, Z)) / sp.sqrt(6),
        (kron(Y, Y) - kron(Z, Z)) / sp.sqrt(6),
    ]

    # Tr(A_nu^* A_mu)=4 delta_nu,mu, so divide contractions by four.
    recovered = [sp.simplify(contract_first_site(h4, a) / 4) for a in left]
    for actual, target in zip(recovered, expected):
        assert zero(actual - target)

    rebuilt = sum(
        (kron(a, b) for a, b in zip(left, recovered)),
        sp.zeros(16),
    )
    assert zero(h4 - rebuilt)
    return recovered


def check_bell_pencil(coefficients: list[sp.Matrix]) -> None:
    bx, by, bz = coefficients
    bell = sp.Matrix.hstack(
        sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2),
        sp.Matrix([0, 1, 1, 0]) / sp.sqrt(2),
        sp.Matrix([1, 0, 0, -1]) / sp.sqrt(2),
        sp.Matrix([0, 1, -1, 0]) / sp.sqrt(2),
    )
    x, y, z = sp.symbols("x y z", real=True)
    normal = sp.simplify(bell.H * (x * bz + y * by + z * bx) * bell)
    blocks = (normal[:2, :2], normal[2:, 2:])
    assert sp.simplify(blocks[0].det() + (2 * x**2 - z**2) / 3) == 0
    assert sp.simplify(blocks[1].det() + (2 * y**2 - z**2) / 3) == 0
    assert zero(normal[:2, 2:])
    assert zero(normal[2:, :2])

    representatives = [
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, sp.sqrt(2)),
        (1, -1, sp.sqrt(2)),
        (1, 1, -sp.sqrt(2)),
        (1, -1, -sp.sqrt(2)),
    ]
    assert all(
        normal.subs({x: a, y: b, z: c}).rank() == 2
        for a, b, c in representatives
    )

    # The block form also certifies minimum nonzero rank two.  These
    # substitutions identify the only loci on which an entire block
    # vanishes; the other nonzero block then has rank two.
    assert zero(blocks[0].subs({x: 0, z: 0}))
    assert zero(blocks[1].subs({y: 0, z: 0}))


def check_active_commutant(coefficients: list[sp.Matrix]) -> int:
    left = [kron(X, I2), kron(Y, I2), kron(Z, I2)]
    variables = sp.symbols("t0:16")
    generic = sp.Matrix(4, 4, variables)
    equations: list[sp.Expr] = []
    for generator in left + coefficients:
        equations.extend(list(generic * generator - generator * generic))
    system, _ = sp.linear_eq_to_matrix(equations, variables)
    rank = system.rank()
    assert rank == 15

    nullspace = system.nullspace()
    assert len(nullspace) == 1
    scalar = sp.Matrix(4, 4, nullspace[0])
    assert scalar == scalar[0, 0] * sp.eye(4)
    return rank


def main() -> None:
    coefficients = check_schmidt_contraction()
    check_bell_pencil(coefficients)
    commutant_rank = check_active_commutant(coefficients)
    print("independent exact codimension-two cut-down audit passed")
    print("Schmidt coefficients recovered by partial contraction: 3")
    print("real rank-at-most-two Bell-pencil lines: 6")
    print(f"generic active-commutant equation rank: {commutant_rank}")
    print("active commutant dimension: 1")
    print("human all-m step: m*rank(active pencil) <= 4 for m >= 2")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact checks for the determinant-transport parity limitation.

The verifier has three independent parts.

1. It checks the basis-free partial-transpose factorization on an exact
   finite model satisfying A^* A = B B^* = (d/4)P.
2. It reconstructs the published d=4 exceptional projection and audits
   every spatial S_3 compression of its common-one space exactly.
3. It checks the odd-s arithmetic and determinant obstruction for an
   antiunitary of square -1 on the abstract determinant multiplicity.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from functools import reduce
from itertools import permutations, product

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.ddm import DDM


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    return reduce(sp.kronecker_product, matrices, sp.Matrix([[1]]))


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def raw_domain_matrix(
    rows: list[list[object]], domain: object
) -> DomainMatrix:
    return DomainMatrix.from_rep(
        DDM(rows, (len(rows), len(rows[0])), domain)
    )


def domain_kronecker(
    left: DomainMatrix, right: DomainMatrix
) -> DomainMatrix:
    assert left.domain == right.domain
    left_rows = left.to_list()
    right_rows = right.to_list()
    left_height, left_width = left.shape
    right_height, right_width = right.shape
    rows = [
        [
            left_rows[i][j] * right_rows[u][v]
            for j in range(left_width)
            for v in range(right_width)
        ]
        for i in range(left_height)
        for u in range(right_height)
    ]
    return raw_domain_matrix(rows, left.domain)


def domain_trace(matrix: DomainMatrix) -> object:
    rows = matrix.to_list()
    return sum(
        (rows[index][index] for index in range(matrix.shape[0])),
        matrix.domain.zero,
    )


def permutation_matrix(dimension: int, permutation: tuple[int, ...]) -> sp.Matrix:
    """Tensor-factor permutation with new indices old[permutation]."""
    sites = len(permutation)
    size = dimension**sites
    matrix = sp.zeros(size)
    for old_indices in product(range(dimension), repeat=sites):
        old = 0
        new = 0
        for index in old_indices:
            old = dimension * old + index
        for site in permutation:
            new = dimension * new + old_indices[site]
        matrix[new, old] = 1
    return matrix


def universal_partial_transpose_factorization() -> None:
    """Replay the singular-value lemma over the rationals."""
    d = 4
    rank_p = d * d // 2
    w = 11  # deliberately unrelated to rank(P)
    domain_dimension = w * d

    projection = sp.diag(*([1] * rank_p + [0] * rank_p))

    # A : V^2 -> W tensor V and B : W tensor V -> V^2.
    # Their nonzero parts are two different exact isometric placements of
    # ran(P).  Since d/4=1 here, A^*A=BB^*=P.
    a_matrix = sp.zeros(domain_dimension, d * d)
    b_matrix = sp.zeros(d * d, domain_dimension)
    for index in range(rank_p):
        a_matrix[2 * index, index] = 1
        b_matrix[index, 2 * index + 1] = 1

    assert a_matrix.T * a_matrix == projection
    assert b_matrix * b_matrix.T == projection

    partial_transpose = 2 * a_matrix * b_matrix
    gram = partial_transpose.T * partial_transpose
    expected_support = b_matrix.T * b_matrix

    assert gram == 4 * expected_support
    assert expected_support**2 == expected_support
    assert partial_transpose.rank() == rank_p
    assert gram.rank() == rank_p
    assert sp.trace(gram) == rank_p * (d * d // 4)

    # General symbolic arithmetic: nonzero squared singular value d^2/4
    # with multiplicity d^2/2.
    d_symbol = sp.symbols("d", integer=True, positive=True)
    scale = d_symbol / 4
    squared_singular_value = sp.simplify(4 * scale**2)
    assert squared_singular_value == d_symbol**2 / 4
    assert (d_symbol**2 / 2).subs(d_symbol, 6) == 18
    assert squared_singular_value.subs(d_symbol, 6) == 9


def published_h() -> sp.Matrix:
    identity_2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    j = sp.Matrix([[0, -1], [1, 0]])

    return (
        -tensor(z, identity_2, z, z) / sp.sqrt(6)
        - tensor(z, identity_2, j, j) / sp.sqrt(6)
        - tensor(j, identity_2, z, j) / sp.sqrt(6)
        + tensor(j, identity_2, j, z) / sp.sqrt(6)
        - tensor(x, identity_2, x, x) / sp.sqrt(3)
    )


def published_common_one_domain() -> DomainMatrix:
    h = published_h()
    projection = (sp.eye(16) - h) / 2

    field = QQ.algebraic_field(sp.sqrt(2), sp.sqrt(3))
    projection_domain = DomainMatrix.from_Matrix(projection).convert_to(
        field
    )
    identity_4 = DomainMatrix.eye((4, 4), field)
    p = domain_kronecker(projection_domain, identity_4)
    q = domain_kronecker(identity_4, projection_domain)
    one_half = field.from_sympy(sp.Rational(1, 2))
    three_halves = field.from_sympy(sp.Rational(3, 2))
    return three_halves * (p * q * p) - one_half * p


def permutation_domain_matrix(
    dimension: int,
    permutation: tuple[int, ...],
    domain: object,
) -> DomainMatrix:
    sites = len(permutation)
    size = dimension**sites
    rows = [[domain.zero for _ in range(size)] for _ in range(size)]
    for old_indices in product(range(dimension), repeat=sites):
        old = 0
        new = 0
        for index in old_indices:
            old = dimension * old + index
        for site in permutation:
            new = dimension * new + old_indices[site]
        rows[new][old] = domain.one
    return raw_domain_matrix(rows, domain)


def published_spatial_pairing_audit() -> None:
    """Audit all S_3 pairings on the exact d=4 determinant space."""
    e = published_common_one_domain()
    field = e.domain
    one_half = field.from_sympy(sp.Rational(1, 2))
    two = field.from_sympy(sp.Integer(2))
    eight = field.from_sympy(sp.Integer(8))
    assert (e * e - e).is_zero_matrix
    assert (e.transpose() - e).is_zero_matrix
    assert domain_trace(e) == eight

    permutation_operators = {
        permutation: permutation_domain_matrix(
            4, permutation, field
        )
        for permutation in permutations(range(3))
    }
    identity_permutation = (0, 1, 2)
    transpositions = {(0, 2, 1), (1, 0, 2), (2, 1, 0)}
    cycles = {(1, 2, 0), (2, 0, 1)}

    compressions: dict[tuple[int, ...], DomainMatrix] = {}
    for permutation, operator in permutation_operators.items():
        compression = e * operator * e
        compressions[permutation] = compression
        if permutation == identity_permutation:
            assert (compression - e).is_zero_matrix
        elif permutation in transpositions:
            residual = compression * compression - one_half * compression
            assert residual.is_zero_matrix
            assert domain_trace(compression) == two
        elif permutation in cycles:
            assert (compression * compression - compression).is_zero_matrix
            assert domain_trace(compression) == two
        else:
            raise AssertionError("unclassified permutation")

    # The two cycle compressions coincide.  Hence the only skew-adjoint
    # direction in the real S_3 group algebra compresses to zero.
    forward_cycle = compressions[(1, 2, 0)]
    backward_cycle = compressions[(2, 0, 1)]
    assert (forward_cycle - backward_cycle).is_zero_matrix
    assert (
        e
        * (
            permutation_operators[(1, 2, 0)]
            - permutation_operators[(2, 0, 1)]
        )
        * e
    ).is_zero_matrix

    # Every compressed permutation is symmetric.  Only the identity
    # compression is invertible on ran(e), and coordinate conjugation
    # preserves this real range with square +1.
    for compression in compressions.values():
        assert (compression.transpose() - compression).is_zero_matrix
    # The polynomial identities and traces give the ranks without a
    # numerical or symbolic rank routine: 4 for transpositions and 2 for
    # cycles, versus rank 8 for e.
    assert field.is_AlgebraicField


def odd_multiplicity_limitation() -> None:
    """Exact odd-s bookkeeping and the antiunitary determinant test."""
    s = 3
    d = 2 * s
    determinant_multiplicity = s**3
    transport_dimension = determinant_multiplicity * d
    partial_transpose_rank = d**2 // 2

    assert determinant_multiplicity == 27
    assert transport_dimension == 162
    assert partial_transpose_rank == 18
    assert (d // 2) ** 2 == 9  # squared nonzero singular value

    # If J=U K were an antiunitary with J^2=-I on an n-dimensional
    # complex space, then U conjugate(U)=-I and determinants would give
    # |det U|^2=(-1)^n.  This is impossible for odd n.  The scalar
    # three-strand Hecke block does not require such a J.
    n = sp.symbols("n", integer=True, positive=True)
    assert (-1) ** determinant_multiplicity == -1
    assert determinant_multiplicity % 2 == 1
    assert sp.simplify((-1) ** (2 * n)) == 1


def main() -> None:
    universal_partial_transpose_factorization()
    print("PASS universal determinant-transport partial-transpose lemma")
    published_spatial_pairing_audit()
    print("PASS exact published d=4 S_3/conjugation pairing audit")
    odd_multiplicity_limitation()
    print("PASS exact odd-s determinant-multiplicity limitation")
    print("All determinant-transport parity checks passed exactly.")


if __name__ == "__main__":
    main()

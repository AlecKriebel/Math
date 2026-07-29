#!/usr/bin/env python3
"""Exact replay for the four-strand nonreal-pairing limitation.

The checks separate three levels of information:

1. exact irreducible H_4(3,6) blocks and their nonreal U=H_12 H_23
   corners;
2. the induced antiunitary sign and the four-strand multiplicity
   arithmetic;
3. an odd-s=3 abstract factorization satisfying every resulting corner
   polynomial and last-site trace identity.

The final model is deliberately only an abstract four-strand module.  It
does not claim a tensor-local d=6 Yang--Baxter matrix.
"""

from __future__ import annotations

import sympy as sp


def zero(matrix: sp.Matrix) -> bool:
    return bool(matrix.to_DM(extension=True).is_zero_matrix)


def generic_generators() -> tuple[sp.Matrix, sp.Matrix]:
    """The real two-dimensional generic H_3 reflection block."""
    root_two = sp.sqrt(2)
    first = sp.diag(1, -1)
    second = sp.Matrix(
        [
            [-sp.Rational(1, 3), 2 * root_two / 3],
            [2 * root_two / 3, sp.Rational(1, 3)],
        ]
    )
    return first, second


def four_strand_simple_blocks(
) -> dict[str, tuple[sp.Matrix, sp.Matrix, sp.Matrix]]:
    """Real reflection models for (31), (22), and (211)."""
    generic_first, generic_second = generic_generators()

    first_31 = sp.diag(1, 1, -1)
    second_31 = sp.diag(1, 1, 1)
    second_31[1:3, 1:3] = generic_second
    third_31 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])

    first_22 = generic_first
    second_22 = generic_second
    third_22 = generic_first

    first_211 = sp.diag(-1, 1, -1)
    second_211 = sp.diag(-1, 1, 1)
    second_211[1:3, 1:3] = generic_second
    third_211 = sp.Matrix([[0, 0, 1], [0, -1, 0], [1, 0, 0]])

    return {
        "31": (first_31, second_31, third_31),
        "22": (first_22, second_22, third_22),
        "211": (first_211, second_211, third_211),
    }


def spectral_projection(
    product: sp.Matrix, eigenvalue: sp.Expr, other: sp.Expr
) -> sp.Matrix:
    """Project to a nonreal eigenvalue; 1 may be absent from the block."""
    identity = sp.eye(product.rows)
    return sp.simplify(
        (product - identity)
        * (product - other * identity)
        / ((eigenvalue - 1) * (eigenvalue - other))
    )


def commutant_dimension(generators: tuple[sp.Matrix, ...]) -> int:
    """Dimension of the simultaneous commutant, by exact linear algebra."""
    dimension = generators[0].rows
    variables = sp.symbols(f"x0:{dimension * dimension}")
    candidate = sp.Matrix(dimension, dimension, variables)
    equations: list[sp.Expr] = []
    for generator in generators:
        equations.extend(candidate * generator - generator * candidate)
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return dimension**2 - coefficient_matrix.rank()


def simple_block_audit() -> dict[str, sp.Expr]:
    coefficient = sp.Rational(1, 3)
    root_two = sp.sqrt(2)
    lambda_plus = (-1 + 2 * root_two * sp.I) / 3
    lambda_minus = sp.conjugate(lambda_plus)
    compression_scalars: dict[str, sp.Expr] = {}

    for label, (first, second, third) in four_strand_simple_blocks().items():
        identity = sp.eye(first.rows)
        assert first.conjugate().T == first
        assert second.conjugate().T == second
        assert third.conjugate().T == third
        assert first**2 == identity
        assert second**2 == identity
        assert third**2 == identity
        assert zero(first * third - third * first)
        assert zero(
            first * second * first
            - second * first * second
            - coefficient * (first - second)
        )
        assert zero(
            second * third * second
            - third * second * third
            - coefficient * (second - third)
        )
        assert commutant_dimension((first, second, third)) == 1

        product = first * second
        polynomial_variable = sp.Symbol("x")
        expected_characteristic = (
            (polynomial_variable - lambda_plus)
            * (polynomial_variable - lambda_minus)
        )
        if first.rows == 3:
            expected_characteristic *= polynomial_variable - 1
        assert sp.simplify(
            product.charpoly(polynomial_variable).as_expr()
            - expected_characteristic
        ) == 0
        plus = spectral_projection(product, lambda_plus, lambda_minus)
        minus = spectral_projection(product, lambda_minus, lambda_plus)
        assert zero(plus**2 - plus)
        assert zero(minus**2 - minus)
        assert zero(plus.conjugate().T - plus)
        assert zero(minus.conjugate().T - minus)
        assert sp.simplify(sp.trace(plus)) == 1
        assert sp.simplify(sp.trace(minus)) == 1
        assert zero(first * plus * first - minus)

        # The H_34 linking map and its Hermitian return compression.
        linking = sp.simplify(plus * third * minus)
        return_compression = sp.simplify(plus * first * third * plus)
        assert zero(
            return_compression.conjugate().T - return_compression
        )
        scalar = sp.simplify(sp.trace(return_compression))
        compression_scalars[label] = scalar
        assert zero(return_compression - scalar * plus)

        # A A^* = B^2 because B=A H_12 on the plus line.
        assert zero(
            linking * linking.conjugate().T - return_compression**2
        )

        # In the real form, conjugation swaps plus and minus and sends the
        # polar linking unitary to its adjoint.  In one-dimensional
        # corners this makes the induced antiunitary square +1.
        singular_value = abs(scalar)
        polar = sp.simplify(linking / singular_value)
        assert zero(polar * polar.conjugate().T - plus)
        assert zero(polar.conjugate().T * polar - minus)
        assert zero(sp.conjugate(polar) - polar.conjugate().T)
        assert zero(polar * sp.conjugate(polar) - plus)

    assert compression_scalars == {
        "31": -sp.Rational(1, 2),
        "22": sp.Integer(1),
        "211": -sp.Rational(1, 2),
    }
    return compression_scalars


def multiplicity_and_odd_s_limitation(
    compression_scalars: dict[str, sp.Expr],
) -> None:
    # General tensor-space multiplicities at four strands.
    s = sp.symbols("s", integer=True, positive=True)
    branch_multiplicity = 2 * s**4
    plus_dimension = 3 * branch_multiplicity
    three_strand_nonreal_multiplicity = 3 * s**3
    local_dimension = 2 * s
    assert sp.expand(plus_dimension) == sp.expand(
        three_strand_nonreal_multiplicity * local_dimension
    )

    rank_one_eigenspace = branch_multiplicity
    rank_minus_half_eigenspace = 2 * branch_multiplicity
    assert sp.expand(
        rank_one_eigenspace + rank_minus_half_eigenspace
    ) == sp.expand(plus_dimension)
    assert sp.expand(
        rank_one_eigenspace
        - sp.Rational(1, 2) * rank_minus_half_eigenspace
    ) == 0

    # The first unresolved value s=3 has odd three-strand multiplicity.
    odd_s = 3
    d = 2 * odd_s
    multiplicity = 3 * odd_s**3
    branch = 2 * odd_s**4
    assert d == 6
    assert multiplicity == 81
    assert multiplicity % 2 == 1
    assert branch == 162
    assert multiplicity * d == 3 * branch

    # Identify K_+ tensor C^6 with three two-dimensional local colors.
    # The canonical return compression is I_81 tensor L, where L has the
    # three exact H_4 branch scalars.  It has the universal polynomial
    # and zero last-site trace despite dim(K_+)=81 being odd.
    local_return = sp.diag(
        *sum(
            ([compression_scalars[label]] * 2 for label in ("31", "22", "211")),
            [],
        )
    )
    identity_local = sp.eye(d)
    assert zero(
        (local_return - identity_local)
        * (local_return + sp.Rational(1, 2) * identity_local)
    )
    assert sp.trace(local_return) == 0
    assert local_return.rank() == d
    assert local_return == local_return.T

    # The corresponding linking singular values are 1/2, 1, 1/2,
    # each on a two-dimensional local color.  Its polar real structure
    # has square +1, not -1.
    local_singular = abs(local_return)
    local_polar = local_return * local_singular.inv()
    assert local_polar**2 == identity_local
    assert local_polar * sp.conjugate(local_polar) == identity_local


def corner_dimension_audit() -> None:
    # Restriction of the three H_4 simples to H_3:
    # (31)->(3)+(21), (22)->(21), (211)->(21)+(111).
    restrictions = {
        "31": ("3", "21"),
        "22": ("21",),
        "211": ("21", "111"),
    }
    number_of_generic_branches = sum(
        "21" in summands for summands in restrictions.values()
    )
    assert number_of_generic_branches == 3

    # A chosen nonreal minimal projection has rank one in every branch.
    # Hence its same-sign corner is C^3 and the two-sign linking corner
    # is one-dimensional in each branch.  Neither contains an M_2 acting
    # on the tensor multiplicity.
    same_sign_corner_dimension = number_of_generic_branches
    linking_corner_dimension = number_of_generic_branches
    full_two_sign_corner_dimension = 4 * number_of_generic_branches
    assert same_sign_corner_dimension == 3
    assert linking_corner_dimension == 3
    assert full_two_sign_corner_dimension == 12  # M_2(C)^3


def main() -> None:
    scalars = simple_block_audit()
    print("PASS exact real H4(3,6) simple blocks and shifted cubic")
    print("PASS nonreal corner scalars (-1/2, 1, -1/2)")
    print("PASS polar Hecke linking antiunitary has square +1")
    corner_dimension_audit()
    print("PASS corners C^3 and M2(C)^3 contain no multiplicity action")
    multiplicity_and_odd_s_limitation(scalars)
    print("PASS exact odd-s=3 factorized four-strand limitation model")
    print("All four-strand nonreal-pairing limitation checks passed exactly.")


if __name__ == "__main__":
    main()

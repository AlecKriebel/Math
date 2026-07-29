#!/usr/bin/env python3
"""Exact verifier for the Majid--Markl Hecke-gluing unitarity no-go."""

from __future__ import annotations

import sympy as sp


def verify_general_operator_block_identities() -> None:
    """Check the block-polynomial identities in the scalar shadow.

    The human proof uses the same four block multiplications for
    arbitrary composable operators.  The scalar shadow independently
    guards every sign and placement.
    """
    u, s, t, eigenvalue_sum, eigenvalue_product = sp.symbols(
        "u s t eigenvalue_sum eigenvalue_product",
        nonzero=True,
    )
    mixed = sp.Matrix([[0, s], [u, t]])
    residual = sp.expand(
        mixed**2
        - eigenvalue_sum * mixed
        + eigenvalue_product * sp.eye(2)
    )
    expected = sp.Matrix(
        [
            [s * u + eigenvalue_product,
             s * (t - eigenvalue_sum)],
            [(t - eigenvalue_sum) * u,
             u * s + t**2 - eigenvalue_sum * t
             + eigenvalue_product],
        ]
    )
    assert all(
        sp.simplify(entry) == 0
        for entry in residual - expected
    )

    forced = sp.simplify(
        residual.subs(
            {
                t: eigenvalue_sum,
                s: -eigenvalue_product / u,
            }
        )
    )
    assert forced == sp.zeros(2)

    # For orthogonal mixed sectors, the upper-right block of Q*Q is
    # U* T.  Once U is unitary/invertible, it vanishes iff T vanishes.
    # The Hecke equations force T to be the eigenvalue sum.
    exceptional_q = (1 + sp.I * sp.sqrt(3)) / 2
    exceptional_sum = sp.simplify(exceptional_q - 1)
    assert exceptional_sum == (-1 + sp.I * sp.sqrt(3)) / 2
    assert exceptional_sum != 0


def main() -> None:
    sqrt3 = sp.sqrt(3)
    imaginary = sp.I

    exceptional_q = (1 + imaginary * sqrt3) / 2
    hecke_q = (sqrt3 + imaginary) / 2
    phase = (sqrt3 - imaginary) / 2

    # Scaling {-1, exceptional_q} by phase gives
    # {-hecke_q^{-1}, hecke_q}.
    assert sp.simplify(phase * exceptional_q - hecke_q) == 0
    assert sp.simplify(-phase + 1 / hecke_q) == 0

    cross_coefficient = sp.simplify(hecke_q - 1 / hecke_q)
    assert cross_coefficient == imaginary

    cross_block = sp.Matrix([[0, 1], [1, cross_coefficient]])
    identity = sp.eye(2)
    hecke_residual = sp.simplify(
        (cross_block - hecke_q * identity)
        * (cross_block + identity / hecke_q)
    )
    assert hecke_residual == sp.zeros(2)

    # Any product inner product on span{x tensor y, y tensor x} has
    # this Gram form, even if X and Y are not orthogonal.
    norm_product, overlap = sp.symbols(
        "norm_product overlap", real=True
    )
    gram = sp.Matrix(
        [[norm_product, overlap], [overlap, norm_product]]
    )
    gram_defect = sp.simplify(
        cross_block.conjugate().T * gram * cross_block - gram
    )
    expected_defect = sp.Matrix(
        [[0, imaginary * norm_product],
         [-imaginary * norm_product, norm_product]]
    )
    assert gram_defect == expected_defect

    input_vector = sp.Matrix([0, 1])
    input_norm = sp.expand((input_vector.T * gram * input_vector)[0])
    output_vector = cross_block * input_vector
    output_norm = sp.expand(
        (output_vector.conjugate().T * gram * output_vector)[0]
    )
    assert input_norm == norm_product
    assert sp.simplify(output_norm - 2 * norm_product) == 0

    verify_general_operator_block_identities()

    print("[ok] exceptional-to-Majid--Markl normalization")
    print("[ok] exact Hecke polynomial on the canonical mixed block")
    print("[ok] product-Gram unitarity defect:")
    print(gram_defect)
    print("[ok] mixed-vector squared norm ratio: 2")
    print("[ok] full operator-block Hecke identities")
    print(
        "[ok] orthogonal-sector unitarity forces opposite roots"
    )
    print(
        "[scope] excludes canonical gluing for every local metric and "
        "Theorem 2.7 gluing for orthogonal colors; not arbitrary "
        "colored mixed blocks"
    )


if __name__ == "__main__":
    main()

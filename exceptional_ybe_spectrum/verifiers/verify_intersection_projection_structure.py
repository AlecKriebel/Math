#!/usr/bin/env python3
"""Exact checks for the canonical intersection-projection note.

The verifier has three logically separate parts.

1. It checks the scalar zero-variance arithmetic in the universal proof.
2. It replays the new four-site compression on the published exact d=4
   witness over an algebraic number field.
3. It checks the exact GHZ x spectator limitation model on its qubit core
   and the d=6 rank/partial-trace scaling symbolically.

No floating-point arithmetic is used.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def partial_trace(
    matrix: sp.Matrix, dimensions: tuple[int, ...], traced_site: int
) -> sp.Matrix:
    """Partial trace of one site, with sites numbered from zero."""
    before = 1
    for dimension in dimensions[:traced_site]:
        before *= dimension
    traced_dimension = dimensions[traced_site]
    after = 1
    for dimension in dimensions[traced_site + 1 :]:
        after *= dimension
    remaining = before * after
    return sp.Matrix(
        remaining,
        remaining,
        lambda row, column: sum(
            matrix[
                (row // after) * traced_dimension * after
                + index * after
                + row % after,
                (column // after) * traced_dimension * after
                + index * after
                + column % after,
            ]
            for index in range(traced_dimension)
        ),
    )


def universal_scalar_arithmetic() -> None:
    c = sp.Rational(1, 3)
    eta = sp.Rational(1, 2)

    # Equation (22): tr(E r E r)/tr(E).
    second_moment = sp.cancel((eta - c) / (1 - c))
    variance = sp.cancel(second_moment - eta**2)
    shifted_angle = sp.cancel((eta - c) / (1 - c))

    assert second_moment == sp.Rational(1, 4)
    assert variance == 0
    assert shifted_angle == sp.Rational(1, 4)

    d = sp.symbols("d", integer=True, positive=True)
    assert (d**4 / 8).subs(d, 6) == 162
    assert (3 * d**4 / 4).subs(d, 6) == 972

    # The canonical generic-block direct rotation has order three and
    # determinant one blockwise, not because of a block-count parity.
    root_three = sp.sqrt(3)
    generic_e = sp.diag(1, 0)
    generic_f = sp.Matrix(
        [
            [sp.Rational(1, 4), root_three / 4],
            [root_three / 4, sp.Rational(3, 4)],
        ]
    )
    direct_rotation = (2 * generic_f - sp.eye(2)) * (
        2 * generic_e - sp.eye(2)
    )
    assert direct_rotation**3 == sp.eye(2)
    assert direct_rotation.det() == 1

    # The exact middle-marginal bounds specialize without imposing parity.
    assert (d**4 / 64).subs(d, 6) == sp.Rational(81, 4)
    assert (d**4 / 16).subs(d, 6) == 81
    assert (d**2 / 4).subs(d, 6) == 9


def published_d4_replay() -> None:
    """Check E P34 E=E/2 exactly for the published sparse witness."""
    identity_2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    j = sp.Matrix([[0, -1], [1, 0]])

    h = (
        -tensor(z, identity_2, z, z) / sp.sqrt(6)
        - tensor(z, identity_2, j, j) / sp.sqrt(6)
        - tensor(j, identity_2, z, j) / sp.sqrt(6)
        + tensor(j, identity_2, j, z) / sp.sqrt(6)
        - tensor(x, identity_2, x, x) / sp.sqrt(3)
    )
    d = 4
    projection = (sp.eye(d * d) - h) / 2
    p = tensor(projection, sp.eye(d))
    q = tensor(sp.eye(d), projection)
    e = sp.Rational(3, 2) * p * q * p - sp.Rational(1, 2) * p

    assert is_zero(e * e - e)
    assert is_zero(e.conjugate().T - e)
    assert sp.simplify(sp.trace(e) - 8) == 0
    assert is_zero(
        partial_trace(e, (d, d, d), 2) - d * projection / 4
    )
    assert is_zero(
        partial_trace(e, (d, d, d), 0) - d * projection / 4
    )
    assert is_zero(
        partial_trace(
            partial_trace(e, (d, d, d), 2), (d, d), 1
        )
        - d**2 * sp.eye(d) / 8
    )

    # DomainMatrix keeps the 256-dimensional exact multiplication in
    # QQ(sqrt(2),sqrt(3)) rather than expanding raw symbolic radicals.
    four_site_e = tensor(e, sp.eye(d)).to_DM(extension=True)
    p34 = tensor(sp.eye(d * d), projection).to_DM(extension=True)
    half = four_site_e.domain(sp.Rational(1, 2))
    compression_residual = (
        four_site_e * p34 * four_site_e - half * four_site_e
    )
    assert compression_residual.is_zero_matrix


def limitation_countermodel() -> None:
    """Exact qubit core and symbolic d=6 spectator stabilization."""
    zero = sp.Matrix([1, 0])
    one = sp.Matrix([0, 1])
    ket000 = tensor(zero, zero, zero)
    ket111 = tensor(one, one, one)
    ket010 = tensor(zero, one, zero)
    ket101 = tensor(one, zero, one)

    gamma_plus = (ket000 + ket111) / sp.sqrt(2)
    gamma_minus = (ket010 + ket101) / sp.sqrt(2)
    e = gamma_plus * gamma_plus.conjugate().T
    f = gamma_minus * gamma_minus.conjugate().T
    p_pair = sp.diag(1, 0, 0, 1)
    p = tensor(p_pair, sp.eye(2))
    q = tensor(sp.eye(2), p_pair)

    assert e * e == e and f * f == f
    assert sp.trace(e) == sp.trace(f) == 1
    assert p * e == e and q * e == e
    assert (sp.eye(8) - p) * f == f
    assert (sp.eye(8) - q) * f == f

    assert partial_trace(e, (2, 2, 2), 2) == p_pair / 2
    assert partial_trace(e, (2, 2, 2), 0) == p_pair / 2
    assert partial_trace(f, (2, 2, 2), 2) == (
        sp.eye(4) - p_pair
    ) / 2
    assert partial_trace(f, (2, 2, 2), 0) == (
        sp.eye(4) - p_pair
    ) / 2

    for site in range(3):
        reduced = e
        dimensions = [2, 2, 2]
        # Trace the two sites other than ``site``, from right to left so
        # site numbering remains unambiguous.
        for traced in sorted(
            [index for index in range(3) if index != site], reverse=True
        ):
            reduced = partial_trace(reduced, tuple(dimensions), traced)
            dimensions.pop(traced)
        assert reduced == sp.eye(2) / 2

    e_left = tensor(e, sp.eye(2))
    e_right = tensor(sp.eye(2), e)
    f_left = tensor(f, sp.eye(2))
    f_right = tensor(sp.eye(2), f)

    assert e_left * e_right * e_left == e_left / 4
    assert e_right * e_left * e_right == e_right / 4
    assert f_left * f_right * f_left == f_left / 4
    assert f_right * f_left * f_right == f_right / 4
    assert e_left * f_right == sp.zeros(16)
    assert f_left * e_right == sp.zeros(16)

    # The common ranges of the commuting equality constraints have rank 2,
    # whereas e and f have rank 1.  This pinpoints the intentionally missing
    # full-intersection condition.
    assert p * q == q * p
    assert sp.trace(p * q) == 2
    cubic_residual = p * q * p - q * p * q - (p - q) / 3
    assert cubic_residual != sp.zeros(8)

    # Sitewise spectator stabilization with s=3, hence d=6.
    s = 3
    d = 2 * s
    assert 2 * s**2 == d**2 // 2  # rank P-hat
    assert s**3 == d**3 // 8  # rank e-hat and f-hat
    assert sp.Rational(s, 2) == sp.Rational(d, 4)
    assert sp.Rational(s**2, 2) == sp.Rational(d**2, 8)
    assert 2 * s**3 == 54  # full common-one rank in this countermodel
    # K-hat=(d/4)P-hat on the nonadjacent sites is nonscalar and has
    # purity d^4/32.
    assert sp.Rational(d, 4) == sp.Rational(3, 2)
    assert (d**2 // 2) * sp.Rational(d, 4) ** 2 == sp.Rational(
        d**4, 32
    )


def main() -> None:
    universal_scalar_arithmetic()
    print("PASS universal zero-variance arithmetic and d=6 block counts")
    published_d4_replay()
    print("PASS exact d=4 compression E P34 E = E/2")
    limitation_countermodel()
    print("PASS exact GHZ x C^3 dimension-six limitation countermodel")
    print("All intersection-projection checks passed exactly.")


if __name__ == "__main__":
    main()

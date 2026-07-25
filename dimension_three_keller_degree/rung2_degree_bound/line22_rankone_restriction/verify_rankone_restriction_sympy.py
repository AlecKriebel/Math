#!/usr/bin/env python3
"""Exact SymPy certificate for the rank-one-restriction line-(2,2) row.

The certified theorem is the finite-companion open orbit

    p=x^2, q=y^2+x*z,
    H4=((p-q)^2,(p+q)^2,0),
    (H3)_3=x*(p-c*q),                 c*(c^2-9) != 0.

The script also reconstructs the exact stabilizer and the raw E7 ranks on
every joint-moduli stratum.  It makes no claim on the frontier c=0, c^2=9,
c=infinity, or on the marked-critical outer-cover orbits.
"""

from __future__ import annotations

if not __debug__:
    raise RuntimeError("verification requires assertions; do not use -O")

from itertools import product

import sympy as sp


x, y, z, c = sp.symbols("x y z c")
variables = (x, y, z)
p = x**2
q = y**2 + x * z


def monomials(degree: int) -> tuple[sp.Expr, ...]:
    return tuple(
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def form(
    prefix: str, degree: int
) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    coefficients = sp.symbols(f"{prefix}0:{len(monomials(degree))}")
    return (
        sum(
            coefficient * monomial
            for coefficient, monomial in zip(coefficients, monomials(degree))
        ),
        coefficients,
    )


def jacobian(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix([first, second, third]).jacobian(variables).det()
    )


def e7_matrix(
    first: sp.Expr,
    second: sp.Expr,
    third: sp.Expr,
    prefix: str,
) -> tuple[sp.Matrix, tuple[sp.Symbol, ...], sp.Expr]:
    U, uc = form(prefix + "u", 3)
    V, vc = form(prefix + "v", 3)
    W, wc = form(prefix + "w", 2)
    E7 = sp.expand(
        jacobian(first, second, W)
        + jacobian(first, V, third)
        + jacobian(U, second, third)
    )
    polynomial = sp.Poly(E7, *variables)
    equations = [
        polynomial.coeff_monomial(monomial) for monomial in monomials(7)
    ]
    matrix, rhs = sp.linear_eq_to_matrix(equations, uc + vc + wc)
    assert rhs == sp.zeros(len(equations), 1)
    return matrix, uc + vc + wc, E7


def weighted_coefficient(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    weight: int,
) -> sp.Expr:
    matrices = tuple(
        vector.jacobian(variables)
        for vector in (linear, quadratic, cubic, quartic)
    )
    result = 0
    for row_weights in product(range(4), repeat=3):
        if sum(row_weights) != weight:
            continue
        result += sp.Matrix.vstack(
            *(matrices[row_weights[row]][row, :] for row in range(3))
        ).det()
    return sp.expand(result)


def vector_coefficients(
    first: sp.Expr, second: sp.Expr, third: sp.Expr
) -> sp.Matrix:
    answer: list[sp.Expr] = []
    for expression, degree in ((first, 3), (second, 3), (third, 2)):
        polynomial = sp.Poly(expression, *variables)
        answer.extend(
            polynomial.coeff_monomial(monomial)
            for monomial in monomials(degree)
        )
    return sp.Matrix(answer)


def stabilizer_certificate() -> None:
    """Reconstruct the full source stabilizer and its base action."""

    a, b, g, d = sp.symbols("a b g d", nonzero=True)
    transformed_x = a * x
    transformed_y = g * x + b * y
    transformed_z = d * x - 2 * b * g * y / a + b**2 * z / a
    transformed_p = sp.expand(transformed_x**2)
    transformed_q = sp.expand(
        transformed_y**2 + transformed_x * transformed_z
    )
    assert transformed_p == a**2 * p
    assert sp.expand(
        transformed_q - b**2 * q - (g**2 + a * d) * p
    ) == 0
    transformation = sp.Matrix(
        [
            [a, 0, 0],
            [g, b, 0],
            [d, -2 * b * g / a, b**2 / a],
        ]
    )
    assert sp.factor(transformation.det()) == b**3


def raw_e7_certificate() -> None:
    """Open kernel, maximal minor, and every joint-moduli rank stratum."""

    first = (p - q) ** 2
    second = (p + q) ** 2
    third = x * (p - c * q)
    matrix, unknowns, E7 = e7_matrix(first, second, third, "open")

    delta = lambda expression: sp.expand(
        2 * y * sp.diff(expression, z) - x * sp.diff(expression, y)
    )
    displayed = 2 * (
        8 * x * (p - q) * (p + q) * delta(
            sum(unknowns[20 + index] * monomial
                for index, monomial in enumerate(monomials(2)))
        )
        + (p + q) * ((-3 - 2 * c) * p + c * q) * delta(
            sum(unknowns[index] * monomial
                for index, monomial in enumerate(monomials(3)))
        )
        + (p - q) * ((2 * c - 3) * p + c * q) * delta(
            sum(unknowns[10 + index] * monomial
                for index, monomial in enumerate(monomials(3)))
        )
    )
    assert sp.expand(E7 - displayed) == 0
    assert jacobian(first, second, third) == 0

    # Six first-integral directions and the x,y source-translation jets.
    directions = (
        (x**3, 0, 0),
        (x * q, 0, 0),
        (0, x**3, 0),
        (0, x * q, 0),
        (0, 0, p),
        (0, 0, q),
        (
            sp.diff(first, x),
            sp.diff(second, x),
            sp.diff(third, x),
        ),
        (
            sp.diff(first, y),
            sp.diff(second, y),
            sp.diff(third, y),
        ),
    )
    kernel = sp.Matrix.hstack(
        *(vector_coefficients(*direction) for direction in directions)
    )
    selected_kernel_rows = (0, 1, 2, 3, 10, 12, 20, 22)
    assert kernel.extract(selected_kernel_rows, range(8)).det() == -8
    assert matrix * kernel == sp.zeros(36, 8)

    # The omitted z-translation is exactly dependent on the displayed basis.
    z_translation = vector_coefficients(
        sp.diff(first, z),
        sp.diff(second, z),
        sp.diff(third, z),
    )
    relation = (
        2 * kernel[:, 0]
        - 2 * kernel[:, 1]
        - 2 * kernel[:, 2]
        - 2 * kernel[:, 3]
        + c * kernel[:, 4]
        + z_translation
    )
    assert relation == sp.zeros(26, 1)

    # This one minor, together with the eight-dimensional kernel, proves
    # exact rank 18 whenever c*(c^2-9) is nonzero.
    selected_rows = tuple(range(16)) + (17, 19)
    selected_columns = (
        1, 2, 4, 5, 6, 7, 8, 9, 11,
        12, 14, 15, 16, 17, 18, 19, 24, 25,
    )
    determinant = sp.factor(
        matrix.extract(selected_rows, selected_columns).det()
    )
    expected = (
        -769482217582755840
        * c**6
        * (c - 3) ** 4
        * (c + 3) ** 4
    )
    assert sp.expand(determinant - expected) == 0

    # Unmarked critical pair {1,-1}; c is defined modulo sign.
    assert matrix.subs(c, 0).rank() == 16
    assert matrix.subs(c, 3).rank() == 14
    assert matrix.subs(c, -3).rank() == 14
    infinity_matrix, _, _ = e7_matrix(first, second, x * q, "infinity")
    assert infinity_matrix.rank() == 18

    # Marked critical pair {0,infinity}: the three companion orbits.
    marked_cases = (
        ("triple", p**2, q**2, x**3, 8),
        ("mixed-at-other-critical", p**2, q**2, x * q, 18),
        ("mixed-distinct", p**2, q**2, x * (p - q), 18),
    )
    for label, marked_first, marked_second, marked_third, expected_rank in marked_cases:
        marked_matrix, _, _ = e7_matrix(
            marked_first, marked_second, marked_third, "marked" + label
        )
        assert marked_matrix.rank() == expected_rank, label


def lower_exit_certificate() -> None:
    """E6 forces pencil-valued quadratics; E5 makes the linear part singular."""

    A, B, w0, w1 = sp.symbols("A B w0 w1")
    u0, uq, u1, u2, u3, u4 = sp.symbols("u0 uq u1 u2 u3 u4")
    v0, vq, v1, v2, v3, v4 = sp.symbols("v0 vq v1 v2 v3 v4")
    U2 = (
        u0 * p + uq * q + u1 * x * y + u2 * x * z
        + u3 * y * z + u4 * z**2
    )
    V2 = (
        v0 * p + vq * q + v1 * x * y + v2 * x * z
        + v3 * y * z + v4 * z**2
    )
    H4 = sp.Matrix([(p - q) ** 2, (p + q) ** 2, 0])
    H3 = sp.Matrix([A * x * q, B * x * q, x * (p - c * q)])
    H2 = sp.Matrix([U2, V2, w0 * p + w1 * q])
    ell = sp.symbols("ell0:9")
    L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])

    E6 = weighted_coefficient(L, H2, H3, H4, 6)
    constrained = (ell[7], ell[8], u1, u2, u3, u4, v1, v2, v3, v4)
    equations = [
        sp.Poly(E6, *variables).coeff_monomial(monomial)
        for monomial in monomials(6)
    ]
    matrix, rhs = sp.linear_eq_to_matrix(equations, constrained)
    assert matrix.shape == (28, 10)
    assert rhs == sp.zeros(28, 1)
    unconstrained = ell[:7] + (u0, uq, v0, vq)
    assert all(sp.diff(E6, symbol) == 0 for symbol in unconstrained)

    selected_rows = (0, 2, 4, 6, 8, 10, 16, 22, 1, 3)
    determinant = sp.factor(
        matrix.extract(selected_rows, range(10)).det()
    )
    expected = (
        -10871635968 * c**2 * (c - 3) ** 2 * (c + 3) ** 2
    )
    assert sp.expand(determinant - expected) == 0

    normalized = {symbol: 0 for symbol in constrained}
    assert sp.expand(E6.subs(normalized)) == 0
    E5 = weighted_coefficient(
        L.subs(normalized),
        H2.subs(normalized),
        H3,
        H4,
        5,
    )
    polynomial = sp.Poly(E5, *variables)
    assert sp.expand(
        polynomial.coeff_monomial(x**3 * z**2)
        + 2 * c * (ell[1] - ell[4])
    ) == 0
    assert sp.expand(
        polynomial.coeff_monomial(y**5)
        - 4 * c * (ell[2] - ell[5])
    ) == 0
    assert sp.expand(
        polynomial.coeff_monomial(x**5)
        - 2 * ((2 * c + 3) * ell[1] + (3 - 2 * c) * ell[4])
    ) == 0
    assert sp.expand(
        polynomial.coeff_monomial(x**4 * y)
        + 4 * ((2 * c + 3) * ell[2] + (3 - 2 * c) * ell[5])
    ) == 0
    singular_substitution = {
        ell[1]: 0,
        ell[2]: 0,
        ell[4]: 0,
        ell[5]: 0,
        ell[7]: 0,
        ell[8]: 0,
    }
    assert sp.Matrix(3, 3, ell).det().subs(singular_substitution) == 0


if __name__ == "__main__":
    stabilizer_certificate()
    raw_e7_certificate()
    lower_exit_certificate()
    print(
        "PASS: rank-one-restriction stabilizer, raw E7 strata, "
        "and finite-companion Keller exit"
    )

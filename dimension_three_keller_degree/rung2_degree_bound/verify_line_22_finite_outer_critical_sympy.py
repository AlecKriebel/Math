#!/usr/bin/env python3
"""Exact certificates for WORKING_LINE_22_FINITE_OUTER_CRITICAL.md.

Scope
-----
This script certifies three loci for the rank-two-restriction pencil

    p = x^2,  q = y*z:

* the finite-companion open set c*F*G != 0;
* the noncritical part of the triple branch c = 0;
* the marked-critical triple orbit with finite other critical point.

It intentionally makes no claim on the three boundary families listed in
Section 6 of the note.  Every calculation is over QQ with symbolic
parameters; no floating-point or random-rank assertion is used.
"""

from __future__ import annotations

if not __debug__:
    raise RuntimeError("verification requires assertions; do not use -O")

from functools import reduce
from itertools import combinations, product

import sympy as sp


x, y, z = sp.symbols("x y z")
variables = (x, y, z)
p = x**2
q = y * z


def homogeneous_monomials(degree: int) -> tuple[sp.Expr, ...]:
    """Degree-d monomials, ordered x-descending and then y-descending."""

    answer: list[sp.Expr] = []
    for x_degree in range(degree, -1, -1):
        for y_degree in range(degree - x_degree, -1, -1):
            z_degree = degree - x_degree - y_degree
            answer.append(x**x_degree * y**y_degree * z**z_degree)
    return tuple(answer)


def homogeneous_form(
    prefix: str, degree: int
) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    monomials = homogeneous_monomials(degree)
    coefficients = sp.symbols(f"{prefix}0:{len(monomials)}")
    return (
        sp.Add(
            *(
                coefficient * monomial
                for coefficient, monomial in zip(coefficients, monomials)
            )
        ),
        coefficients,
    )


def jacobian_matrix(vector: sp.Matrix) -> sp.Matrix:
    return vector.jacobian(variables)


def jacobian_determinant(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(jacobian_matrix(sp.Matrix([first, second, third])).det())


def weighted_determinant_coefficient(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    weight: int,
) -> sp.Expr:
    """Coefficient of s^weight in det(JL+s JH2+s^2 JH3+s^3 JH4).

    Expanding row-multilinearly is substantially faster and less fragile than
    forming a large determinant over QQ[s,parameters].
    """

    matrices = tuple(
        jacobian_matrix(vector) for vector in (linear, quadratic, cubic, quartic)
    )
    result = 0
    for row_weights in product(range(4), repeat=3):
        if sum(row_weights) != weight:
            continue
        selected = sp.Matrix.vstack(
            *(matrices[row_weights[row]][row, :] for row in range(3))
        )
        result += selected.det()
    return sp.expand(result)


def coefficient_equations(form: sp.Expr) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(form), *variables)
    return [
        polynomial.coeff_monomial(monomial)
        for monomial in homogeneous_monomials(polynomial.total_degree())
        if polynomial.coeff_monomial(monomial) != 0
    ]


def coefficient_dictionary(form: sp.Expr, degree: int) -> dict[sp.Expr, sp.Expr]:
    polynomial = sp.Poly(sp.expand(form), *variables)
    return {
        monomial: sp.factor(polynomial.coeff_monomial(monomial))
        for monomial in homogeneous_monomials(degree)
        if polynomial.coeff_monomial(monomial) != 0
    }


def delta(form: sp.Expr) -> sp.Expr:
    return sp.expand(z * sp.diff(form, z) - y * sp.diff(form, y))


def yz_weight(monomial: sp.Expr) -> int:
    powers = monomial.as_powers_dict()
    return int(powers.get(z, 0) - powers.get(y, 0))


def gcd_nonzero(polynomials: list[sp.Expr]) -> sp.Expr:
    nonzero = [sp.Poly(polynomial) for polynomial in polynomials if polynomial != 0]
    assert nonzero
    return sp.factor(reduce(sp.gcd, nonzero).as_expr())


def assert_associate(left: sp.Expr, right: sp.Expr) -> None:
    quotient = sp.cancel(left / right)
    assert quotient.is_Rational and quotient != 0, (left, right, quotient)


def contains_associate(polynomials: list[sp.Expr], target: sp.Expr) -> bool:
    for candidate in polynomials:
        quotient = sp.cancel(candidate / target)
        if quotient.is_Rational and quotient != 0:
            return True
    return False


def open_e7_certificate() -> None:
    """Weight-block minors and the complete eight-dimensional kernel."""

    a, b, c = sp.symbols("a b c")
    F = 3 * a * b - 2 * a * c - b * c
    G = 3 * a * b - a * c - 2 * b * c

    U, u_coefficients = homogeneous_form("e7u", 3)
    V, v_coefficients = homogeneous_form("e7v", 3)
    W, w_coefficients = homogeneous_form("e7w", 2)
    unknowns = u_coefficients + v_coefficients + w_coefficients

    H4_first = (p - a * q) ** 2
    H4_second = (p - b * q) ** 2
    R = x * (p - c * q)
    E7 = sp.expand(
        jacobian_determinant(H4_first, H4_second, W)
        + jacobian_determinant(H4_first, V, R)
        + jacobian_determinant(U, H4_second, R)
    )
    displayed = 2 * (
        4 * x * (a - b) * (p - a * q) * (p - b * q) * delta(W)
        + (p - b * q) * ((3 * b - 2 * c) * p - b * c * q) * delta(U)
        + (p - a * q) * ((2 * c - 3 * a) * p + a * c * q) * delta(V)
    )
    assert sp.expand(E7 - displayed) == 0

    polynomial = sp.Poly(E7, *variables)
    output_monomials = homogeneous_monomials(7)
    equations = [polynomial.coeff_monomial(monomial) for monomial in output_monomials]
    full_matrix, full_rhs = sp.linear_eq_to_matrix(equations, unknowns)
    assert full_rhs == sp.zeros(len(equations), 1)

    input_monomials = (
        homogeneous_monomials(3)
        + homogeneous_monomials(3)
        + homogeneous_monomials(2)
    )
    block_data: dict[int, sp.Matrix] = {}
    for weight in range(-3, 4):
        row_indices = [
            index
            for index, monomial in enumerate(output_monomials)
            if yz_weight(monomial) == weight
        ]
        column_indices = [
            index
            for index, monomial in enumerate(input_monomials)
            if yz_weight(monomial) == weight
        ]
        block_data[weight] = full_matrix.extract(row_indices, column_indices)

    assert [block_data[weight].shape for weight in range(-3, 4)] == [
        (3, 2),
        (3, 3),
        (4, 5),
        (4, 6),
        (4, 5),
        (3, 3),
        (3, 2),
    ]
    assert block_data[0] == sp.zeros(4, 6)

    for weight in (-3, 3):
        block = block_data[weight]
        minors = [
            block.extract(rows, range(2)).det()
            for rows in combinations(range(3), 2)
        ]
        assert_associate(gcd_nonzero(minors), a - b)

    for weight in (-2, 2):
        determinant = sp.factor(block_data[weight].det())
        assert_associate(determinant, (a - b) ** 2 * F * G)

    for weight in (-1, 1):
        block = block_data[weight]
        minors = [
            block.extract(range(4), columns).det()
            for columns in combinations(range(5), 4)
        ]
        assert_associate(
            gcd_nonzero(minors),
            c * (a - b) ** 2 * F * G,
        )

    # Six invariant directions plus the two genuine affine-translation jets.
    direction_parameters = sp.symbols("d0:8")
    d0, d1, d2, d3, d4, d5, dy, dz = direction_parameters
    kernel_U = (
        d0 * x**3
        + d1 * x * q
        + dy * sp.diff(H4_first, y)
        + dz * sp.diff(H4_first, z)
    )
    kernel_V = (
        d2 * x**3
        + d3 * x * q
        + dy * sp.diff(H4_second, y)
        + dz * sp.diff(H4_second, z)
    )
    kernel_W = (
        d4 * p
        + d5 * q
        + dy * sp.diff(R, y)
        + dz * sp.diff(R, z)
    )
    assert sp.expand(
        E7.subs(
            dict(
                zip(
                    unknowns,
                    [
                        sp.Poly(kernel_U, *variables).coeff_monomial(monomial)
                        for monomial in homogeneous_monomials(3)
                    ]
                    + [
                        sp.Poly(kernel_V, *variables).coeff_monomial(monomial)
                        for monomial in homogeneous_monomials(3)
                    ]
                    + [
                        sp.Poly(kernel_W, *variables).coeff_monomial(monomial)
                        for monomial in homogeneous_monomials(2)
                    ],
                )
            )
        )
    ) == 0
    direction_vector = sp.Matrix(
        [
            sp.Poly(kernel_U, *variables).coeff_monomial(monomial)
            for monomial in homogeneous_monomials(3)
        ]
        + [
            sp.Poly(kernel_V, *variables).coeff_monomial(monomial)
            for monomial in homogeneous_monomials(3)
        ]
        + [
            sp.Poly(kernel_W, *variables).coeff_monomial(monomial)
            for monomial in homogeneous_monomials(2)
        ]
    )
    direction_matrix = direction_vector.jacobian(direction_parameters)
    # These rows give diag(1,...,1,-c,-c), up to permutation.
    selected_rows = (0, 4, 10, 14, 20, 24, 21, 22)
    assert_associate(
        sp.factor(direction_matrix.extract(selected_rows, range(8)).det()),
        c**2,
    )

    print("  PASS open E7: symbolic weight minors and complete affine-jet kernel")


def open_e6_e5_exit_certificate() -> None:
    """The specialization-safe lower-degree exit on c*F*G != 0."""

    a, b, c, A, B, w0, w1 = sp.symbols("a b c A B w0 w1")
    H4 = sp.Matrix([(p - a * q) ** 2, (p - b * q) ** 2, 0])
    H3 = sp.Matrix([A * x * q, B * x * q, x * (p - c * q)])

    U2, u = homogeneous_form("openu", 2)
    V2, v = homogeneous_form("openv", 2)
    H2 = sp.Matrix([U2, V2, w0 * p + w1 * q])
    ell = sp.symbols("ell0:9")
    L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])

    E6 = weighted_determinant_coefficient(L, H2, H3, H4, 6)
    equations = coefficient_equations(E6)
    constrained = (ell[7], ell[8], u[1], u[2], u[3], u[5], v[1], v[2], v[3], v[5])
    unconstrained = tuple(
        symbol for symbol in ell + u + v if symbol not in constrained
    )
    E6_matrix, E6_rhs = sp.linear_eq_to_matrix(equations, constrained)
    assert E6_rhs == sp.zeros(len(equations), 1)
    assert all(sp.diff(E6, symbol) == 0 for symbol in unconstrained)
    assert E6_matrix.shape == (12, 10)
    assert E6_matrix.rank() == 10
    assert E6_matrix.nullspace() == []

    # This block certificate is stronger than a generic symbolic rank call:
    # it proves rank ten at every point a != b, F*G != 0.  The two 3-by-2
    # blocks have maximal-minor gcd a-b, so no additional hypersurface was
    # silently inverted.
    F = 3 * a * b - 2 * a * c - b * c
    G = 3 * a * b - a * c - 2 * b * c
    square_blocks = (
        E6_matrix.extract((0, 4, 8), (0, 2, 6)),
        E6_matrix.extract((1, 5, 9), (1, 3, 7)),
    )
    for index, block in enumerate(square_blocks):
        expected_sign = -1 if index == 0 else 1
        assert_associate(
            sp.factor(block.det()),
            expected_sign * (a - b) ** 2 * F * G,
        )
    rectangular_blocks = (
        E6_matrix.extract((2, 6, 10), (4, 8)),
        E6_matrix.extract((3, 7, 11), (5, 9)),
    )
    for block in rectangular_blocks:
        minors = [
            block.extract(rows, range(2)).det()
            for rows in combinations(range(3), 2)
        ]
        assert_associate(gcd_nonzero(minors), a - b)

    substitutions = {symbol: 0 for symbol in constrained}
    E5 = weighted_determinant_coefficient(
        L.subs(substitutions),
        H2.subs(substitutions),
        H3,
        H4,
        5,
    )
    actual = coefficient_dictionary(E5, 5)
    expected = {
        x**4 * y: 2 * (3 * a * ell[4] - 3 * b * ell[1] + 2 * c * ell[1] - 2 * c * ell[4]),
        x**4 * z: -2 * (3 * a * ell[5] - 3 * b * ell[2] + 2 * c * ell[2] - 2 * c * ell[5]),
        x**2 * y**2 * z: -2
        * (3 * a**2 * ell[4] - a * c * ell[4] - 3 * b**2 * ell[1] + b * c * ell[1]),
        x**2 * y * z**2: 2
        * (3 * a**2 * ell[5] - a * c * ell[5] - 3 * b**2 * ell[2] + b * c * ell[2]),
        y**3 * z**2: 2 * c * (a**2 * ell[4] - b**2 * ell[1]),
        y**2 * z**3: -2 * c * (a**2 * ell[5] - b**2 * ell[2]),
    }
    assert set(actual) == set(expected)
    for monomial, value in expected.items():
        assert sp.expand(actual[monomial] - value) == 0

    first_row = sp.Matrix([[-3 * b + 2 * c, 3 * a - 2 * c]])
    assert sp.expand(first_row[0, 0] + first_row[0, 1] - 3 * (a - b)) == 0
    assert sp.expand(
        sp.Matrix(3, 3, ell).det().subs({ell[7]: 0, ell[8]: 0})
        - ell[6] * (ell[1] * ell[5] - ell[2] * ell[4])
    ) == 0

    print("  PASS open E6/E5: ten forced coefficients and singular linear part")


def noncritical_triple_certificate() -> None:
    """Exact square obstructions for c=0 with both outer critical values finite."""

    t, uk, vk, w0, wy, wz, wq = sp.symbols("t uk vk w0 wy wz wq")
    factor = 4 * (t - 1) / (3 * t)
    H4 = sp.Matrix([(p - t * q) ** 2, (p - q) ** 2, 0])
    H3 = sp.Matrix(
        [
            uk * x * q,
            vk * x * q
            + factor * wy * (x**2 * y - y**2 * z)
            + factor * wz * (x**2 * z - y * z**2),
            x**3,
        ]
    )
    W = w0 * p + wy * x * y + wz * x * z + wq * q
    U2, u = homogeneous_form("tripleu", 2)
    V2, v = homogeneous_form("triplev", 2)
    H2 = sp.Matrix([U2, V2, W])
    ell = sp.symbols("tripleell0:9")
    L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])

    E7 = weighted_determinant_coefficient(L, H2, H3, H4, 7)
    assert sp.expand(E7) == 0

    # Completeness of the E7 normal form.  Before the four affine/target
    # normalizations, the kernel has dimension ten: six invariant terms, two
    # source-translation jets, and exactly the two displayed extra modes.
    general_U3, general_u3 = homogeneous_form("tripleE7u", 3)
    general_V3, general_v3 = homogeneous_form("tripleE7v", 3)
    general_W2, general_w2 = homogeneous_form("tripleE7w", 2)
    E7_general = (
        jacobian_determinant(H4[0], H4[1], general_W2)
        + jacobian_determinant(H4[0], general_V3, x**3)
        + jacobian_determinant(general_U3, H4[1], x**3)
    )
    output_monomials = homogeneous_monomials(7)
    input_monomials = (
        homogeneous_monomials(3)
        + homogeneous_monomials(3)
        + homogeneous_monomials(2)
    )
    polynomial = sp.Poly(E7_general, *variables)
    general_matrix, _ = sp.linear_eq_to_matrix(
        [polynomial.coeff_monomial(monomial) for monomial in output_monomials],
        general_u3 + general_v3 + general_w2,
    )
    ranks = []
    for weight in range(-3, 4):
        rows = [
            index
            for index, monomial in enumerate(output_monomials)
            if yz_weight(monomial) == weight
        ]
        columns = [
            index
            for index, monomial in enumerate(input_monomials)
            if yz_weight(monomial) == weight
        ]
        block = general_matrix.extract(rows, columns)
        ranks.append(block.rank())
        if weight in (-1, 1):
            minors = [
                block.extract(row_choice, column_choice).det()
                for row_choice in combinations(range(4), 3)
                for column_choice in combinations(range(5), 3)
            ]
            assert_associate(gcd_nonzero(minors), t * (t - 1))
    assert ranks == [2, 3, 3, 0, 3, 3, 2]

    direction_parameters = sp.symbols("tripleDirection0:10")
    d0, d1, d2, d3, d4, d5, dy, dz, sy, sz = direction_parameters
    direction_U = (
        d0 * x**3
        + d1 * x * q
        + dy * sp.diff(H4[0], y)
        + dz * sp.diff(H4[0], z)
    )
    direction_V = (
        d2 * x**3
        + d3 * x * q
        + dy * sp.diff(H4[1], y)
        + dz * sp.diff(H4[1], z)
        + factor * sy * (x**2 * y - y**2 * z)
        + factor * sz * (x**2 * z - y * z**2)
    )
    direction_W = d4 * p + d5 * q + sy * x * y + sz * x * z
    direction_vector = []
    for form, degree in (
        (direction_U, 3),
        (direction_V, 3),
        (direction_W, 2),
    ):
        form_polynomial = sp.Poly(form, *variables)
        direction_vector.extend(
            form_polynomial.coeff_monomial(monomial)
            for monomial in homogeneous_monomials(degree)
        )
    direction_matrix = sp.Matrix(direction_vector).jacobian(direction_parameters)
    selected_rows = (0, 1, 2, 4, 10, 11, 12, 14, 20, 24)
    assert_associate(
        sp.factor(direction_matrix.extract(selected_rows, range(10)).det()),
        (t - 1) ** 2,
    )

    E6 = weighted_determinant_coefficient(L, H2, H3, H4, 6)
    equations = coefficient_equations(E6)
    unknowns = u + v + ell
    matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)
    assert matrix.rank() == 10
    numerical_pivot_columns = (1, 2, 3, 5, 7, 8, 9, 11, 19, 20)
    numerical_pivot_rows = tuple(range(10))
    assert_associate(
        sp.factor(
            matrix.extract(numerical_pivot_rows, numerical_pivot_columns).det()
        ),
        t**6 * (t - 1) ** 6,
    )
    left_kernel = matrix.T.nullspace()
    assert len(left_kernel) == 2
    compatibilities = [sp.factor((vector.T * rhs)[0]) for vector in left_kernel]
    expected = [
        -sp.Rational(8, 3) * t * (t - 1) * wy**2,
        sp.Rational(8, 3) * t * (t - 1) * wz**2,
    ]
    unused = compatibilities[:]
    for target in expected:
        for index, candidate in enumerate(unused):
            quotient = sp.cancel(candidate / target)
            if quotient.is_Rational and quotient != 0:
                unused.pop(index)
                break
        else:
            raise AssertionError((compatibilities, expected))
    assert not unused

    print("  PASS c=0 noncritical: the two exact E6 square compatibilities")


def marked_critical_certificate() -> None:
    """Finite-other-critical orbit, including its resonant subcase."""

    B, sigma = sp.symbols("markedB markedSigma")
    w0, wy, wz, wyy, wq, wzz = sp.symbols(
        "markedw0 markedwy markedwz markedwyy markedwq markedwzz"
    )
    W = w0 * p + wy * x * y + wz * x * z + wyy * y**2 + wq * q + wzz * z**2
    V3, v3 = homogeneous_form("markedv", 3)
    U3 = sp.Rational(4, 3) * x * W + sigma * x**3 + B * x * q
    H4 = sp.Matrix([p**2, (p - q) ** 2, 0])
    H3 = sp.Matrix([U3, V3, x**3])
    U2, u = homogeneous_form("markedu", 2)
    V2, v = homogeneous_form("markedQuadraticV", 2)
    H2 = sp.Matrix([U2, V2, W])
    ell = sp.symbols("markedell0:9")
    L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])

    E7 = weighted_determinant_coefficient(L, H2, H3, H4, 7)
    direct_relation = delta(3 * U3 - 4 * x * W)
    assert sp.expand(E7 - 2 * x * p * (p - q) * direct_relation) == 0
    assert direct_relation == 0

    # Conversely, delta has rank eight on cubics and kernel <x^3,xq>.
    test_cubic, test_coefficients = homogeneous_form("markedDelta", 3)
    delta_matrix, _ = sp.linear_eq_to_matrix(
        coefficient_equations(delta(test_cubic)),
        test_coefficients,
    )
    assert delta_matrix.rank() == 8
    assert delta(x**3) == 0
    assert delta(x * q) == 0

    # The raw E6 compatibility ideal.  A constant 4-by-4 minor proves that
    # the rank is four at every parameter value, not just generically.
    E6 = weighted_determinant_coefficient(L, H2, H3, H4, 6)
    equations = coefficient_equations(E6)
    unknowns = u + v + ell
    matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)
    assert matrix.shape == (20, 21), matrix.shape
    assert matrix.rank() == 4
    assert matrix.extract(range(4), (1, 2, 3, 5)).det() == 5184
    compatibilities = [
        sp.factor((vector.T * rhs)[0]) for vector in matrix.T.nullspace()
    ]
    assert contains_associate(compatibilities, wyy**2)
    assert contains_associate(compatibilities, wzz**2)

    # Hence wyy=wzz=0.  The remaining two off-diagonal coefficients are
    # killed unless the total xq coefficient in U3 vanishes.
    reduced_compatibilities = [
        sp.factor(candidate.subs({wyy: 0, wzz: 0}))
        for candidate in compatibilities
    ]
    total = 3 * B + 4 * wq
    assert contains_associate(reduced_compatibilities, wy * total)
    assert contains_associate(reduced_compatibilities, wz * total)

    # If B != 0, E6 also restricts V3 to its two invariant terms plus its two
    # translation jets.  These six exact consequences are the
    # specialization-safe certificate for that normalization.
    invariant_compatibilities = [
        sp.factor(
            candidate.subs({wyy: 0, wzz: 0, wy: 0, wz: 0})
        )
        for candidate in compatibilities
    ]
    for target in (
        B * v3[3],
        B * v3[5],
        B * v3[6],
        B * v3[9],
        B * (v3[1] + v3[7]),
        B * (v3[2] + v3[8]),
    ):
        assert contains_associate(invariant_compatibilities, target)
    assert sp.expand(
        sp.diff(H4[1], z) + 2 * (x**2 * y - y**2 * z)
    ) == 0
    assert sp.expand(
        sp.diff(H4[1], y) + 2 * (x**2 * z - y * z**2)
    ) == 0

    # Resonance total=0.  For B != 0 (equivalently wq != 0 here), the
    # preceding normalization reduces V3 to C*xq.  The displayed E6 solution
    # then leaves two pure cubes in E5.
    resonance_compatibilities = [
        sp.factor(
            candidate.subs(
                {wyy: 0, wzz: 0, B: -sp.Rational(4, 3) * wq}
            )
        )
        for candidate in compatibilities
    ]
    for target in (
        wq * v3[3],
        wq * v3[5],
        wq * v3[6],
        wq * v3[9],
        wq * (v3[1] + v3[7]),
        wq * (v3[2] + v3[8]),
    ):
        assert contains_associate(resonance_compatibilities, target)

    C = sp.symbols("markedC")
    resonant_W = w0 * p + wy * x * y + wz * x * z + wq * q
    resonant_U3 = sp.Rational(4, 3) * x * (wy * x * y + wz * x * z)
    resonant_H3 = sp.Matrix([resonant_U3, C * x * q, x**3])
    resonant_H2 = sp.Matrix(
        [
            u[0] * p
            + u[1] * x * y
            + u[2] * x * z
            + sp.Rational(2, 9) * wy**2 * y**2
            + u[4] * q
            + sp.Rational(2, 9) * wz**2 * z**2,
            V2,
            resonant_W,
        ]
    )
    resonant_substitutions = {
        ell[7]: (9 * u[1] + 8 * w0 * wy + 8 * wy * wq) / 12,
        ell[8]: (9 * u[2] + 8 * w0 * wz + 8 * wz * wq) / 12,
    }
    resonant_E6 = weighted_determinant_coefficient(
        L.subs(resonant_substitutions),
        resonant_H2,
        resonant_H3,
        H4,
        6,
    )
    assert resonant_E6 == 0
    resonant_E5 = weighted_determinant_coefficient(
        L.subs(resonant_substitutions),
        resonant_H2,
        resonant_H3,
        H4,
        5,
    )
    resonant_coefficients = coefficient_dictionary(resonant_E5, 5)
    assert (
        resonant_coefficients[y**4 * z] == sp.Rational(8, 9) * wy**3
    )
    assert (
        resonant_coefficients[y * z**4] == -sp.Rational(8, 9) * wz**3
    )

    # At the endpoint B=wq=0, V3 is genuinely arbitrary.  The same E6
    # solution and the same two cubes survive without restricting it.
    deep_resonant_H3 = sp.Matrix([resonant_U3, V3, x**3])
    deep_resonant_H2 = resonant_H2.subs({wq: 0})
    deep_resonant_substitutions = {
        key: value.subs({wq: 0})
        for key, value in resonant_substitutions.items()
    }
    assert weighted_determinant_coefficient(
        L.subs(deep_resonant_substitutions),
        deep_resonant_H2,
        deep_resonant_H3,
        H4,
        6,
    ) == 0
    deep_resonant_E5 = weighted_determinant_coefficient(
        L.subs(deep_resonant_substitutions),
        deep_resonant_H2,
        deep_resonant_H3,
        H4,
        5,
    )
    deep_resonant_coefficients = coefficient_dictionary(deep_resonant_E5, 5)
    assert (
        deep_resonant_coefficients[y**4 * z]
        == sp.Rational(8, 9) * wy**3
    )
    assert (
        deep_resonant_coefficients[y * z**4]
        == -sp.Rational(8, 9) * wz**3
    )

    # Thus W is invariant in every case.  Once V3 has been reduced to its
    # invariant part, the remaining exit is uniform.
    A, D = sp.symbols("markedA markedD")
    final_H3 = sp.Matrix([A * x * q, D * x * q, x**3])
    final_H2 = sp.Matrix([U2, V2, w0 * p + wq * q])
    solution6 = {
        ell[7]: sp.Rational(3, 4) * u[1],
        ell[8]: sp.Rational(3, 4) * u[2],
        u[3]: 0,
        u[5]: 0,
    }
    final_E6 = weighted_determinant_coefficient(L, final_H2, final_H3, H4, 6)
    assert final_E6.subs(solution6) == 0
    final_E5 = weighted_determinant_coefficient(
        L.subs(solution6),
        final_H2.subs(solution6),
        final_H3,
        H4,
        5,
    )
    final_E5_coefficients = coefficient_dictionary(final_E5, 5)
    assert (
        final_E5_coefficients[y**3 * z**2]
        == -sp.Rational(3, 2) * A * u[1]
    )
    assert (
        final_E5_coefficients[y**2 * z**3]
        == sp.Rational(3, 2) * A * u[2]
    )
    deep_E5_coefficients = coefficient_dictionary(final_E5.subs({A: 0}), 5)
    expected_deep_y = 2 * (3 * ell[1] + 2 * u[1] * (w0 + wq))
    expected_deep_z = -2 * (3 * ell[2] + 2 * u[2] * (w0 + wq))
    assert sp.expand(
        deep_E5_coefficients[x**2 * y**2 * z] - expected_deep_y
    ) == 0, (
        deep_E5_coefficients[x**2 * y**2 * z],
        expected_deep_y,
    )
    assert sp.expand(
        deep_E5_coefficients[x**2 * y * z**2] - expected_deep_z
    ) == 0, (
        deep_E5_coefficients[x**2 * y * z**2],
        expected_deep_z,
    )
    final_E4 = weighted_determinant_coefficient(
        L.subs(solution6),
        final_H2.subs(solution6),
        final_H3.subs({A: 0}),
        H4,
        4,
    )
    final_E4_coefficients = coefficient_dictionary(final_E4, 4)
    assert (
        final_E4_coefficients[y**3 * z]
        == -sp.Rational(3, 2) * u[1] ** 2
    )
    assert (
        final_E4_coefficients[y * z**3]
        == sp.Rational(3, 2) * u[2] ** 2
    )
    assert sp.expand(
        sp.Matrix(3, 3, ell).det().subs(
            {ell[1]: 0, ell[2]: 0, ell[7]: 0, ell[8]: 0}
        )
    ) == 0

    # It remains to certify that the B=0 branches really reach the preceding
    # invariant-V normal form.  First take wq=0.  E4 kills u_xy,u_xz even for
    # completely arbitrary V3.  E5 either kills ell_12,ell_13 directly
    # (u_yz=0) or leaves only the two removable translation jets (u_yz!=0).
    zero_H3 = sp.Matrix([0, V3, x**3])
    zero_H2 = sp.Matrix([U2, V2, w0 * p])
    assert weighted_determinant_coefficient(
        L.subs(solution6), zero_H2.subs(solution6), zero_H3, H4, 6
    ) == 0
    zero_E4 = weighted_determinant_coefficient(
        L.subs(solution6), zero_H2.subs(solution6), zero_H3, H4, 4
    )
    zero_E4_coefficients = coefficient_dictionary(zero_E4, 4)
    assert (
        zero_E4_coefficients[y**3 * z]
        == -sp.Rational(3, 2) * u[1] ** 2
    )
    assert (
        zero_E4_coefficients[y * z**3]
        == sp.Rational(3, 2) * u[2] ** 2
    )
    zero_E5 = weighted_determinant_coefficient(
        L.subs(solution6),
        zero_H2.subs(solution6),
        zero_H3,
        H4,
        5,
    ).subs({u[1]: 0, u[2]: 0})
    zero_E5_coefficients = coefficient_dictionary(zero_E5, 5)
    zero_expected = {
        x**4 * y: -6 * ell[1] - 3 * u[4] * v3[1],
        x**4 * z: 6 * ell[2] + 3 * u[4] * v3[2],
        x**3 * y**2: -6 * u[4] * v3[3],
        x**3 * z**2: 6 * u[4] * v3[5],
        x**2 * y**3: -9 * u[4] * v3[6],
        x**2 * y**2 * z: 6 * ell[1] - 3 * u[4] * v3[7],
        x**2 * y * z**2: -6 * ell[2] + 3 * u[4] * v3[8],
        x**2 * z**3: 9 * u[4] * v3[9],
    }
    for monomial, expected in zero_expected.items():
        assert sp.expand(zero_E5_coefficients[monomial] - expected) == 0, (
            monomial,
            zero_E5_coefficients[monomial],
            expected,
        )

    # Finally B=0,wq!=0.  E5 first removes the four high-weight V3 terms and
    # gives an eliminant Delta*(v1+v7), with
    # Delta=9*u_yz+8*w0*wq-4*wq^2.  On Delta=0 the last possible
    # non-translation modes are killed by two E3 squares.
    special_H3 = sp.Matrix(
        [sp.Rational(4, 3) * wq * x * q, V3, x**3]
    )
    special_H2 = sp.Matrix([U2, V2, w0 * p + wq * q])
    assert weighted_determinant_coefficient(
        L.subs(solution6),
        special_H2.subs(solution6),
        special_H3,
        H4,
        6,
    ) == 0
    special_E5 = weighted_determinant_coefficient(
        L.subs(solution6),
        special_H2.subs(solution6),
        special_H3,
        H4,
        5,
    )
    special_coefficients = coefficient_dictionary(special_E5, 5)
    assert special_coefficients[x * y**3 * z] == (
        sp.Rational(8, 3) * v3[3] * wq**2
    )
    assert special_coefficients[x * y * z**3] == (
        -sp.Rational(8, 3) * v3[5] * wq**2
    )
    assert special_coefficients[y**4 * z] == 4 * v3[6] * wq**2
    assert special_coefficients[y * z**4] == -4 * v3[9] * wq**2

    preliminary = {
        v3[3]: 0,
        v3[5]: 0,
        v3[6]: 0,
        v3[9]: 0,
        u[1]: sp.Rational(2, 3) * v3[7] * wq,
        u[2]: sp.Rational(2, 3) * v3[8] * wq,
    }
    preliminary_E5 = sp.expand(special_E5.subs(preliminary))
    preliminary_coefficients = coefficient_dictionary(preliminary_E5, 5)
    Delta = 9 * u[4] + 8 * w0 * wq - 4 * wq**2
    assert sp.expand(
        preliminary_coefficients[x**4 * y]
        + preliminary_coefficients[x**2 * y**2 * z]
        + sp.Rational(1, 3) * Delta * (v3[1] + v3[7])
    ) == 0
    assert sp.expand(
        preliminary_coefficients[x**4 * z]
        + preliminary_coefficients[x**2 * y * z**2]
        - sp.Rational(1, 3) * Delta * (v3[2] + v3[8])
    ) == 0

    sy = v3[1] + v3[7]
    sz = v3[2] + v3[8]
    exceptional = {
        **preliminary,
        u[4]: (4 * wq**2 - 8 * w0 * wq) / 9,
        ell[1]: -(4 * wq**2 * v3[1] + 8 * w0 * wq * v3[7]) / 18,
        ell[2]: -(4 * wq**2 * v3[2] + 8 * w0 * wq * v3[8]) / 18,
        v[3]: v3[7] ** 2 / 4,
        v[5]: v3[8] ** 2 / 4,
        v[1]: sp.Rational(2, 3) * sy * (w0 + wq)
        + sp.Rational(1, 2) * v3[4] * v3[7],
        v[2]: sp.Rational(2, 3) * sz * (w0 + wq)
        + sp.Rational(1, 2) * v3[4] * v3[8],
        ell[6]: sp.Rational(3, 2) * u[0]
        + sp.Rational(4, 3) * w0**2
        - sp.Rational(2, 3) * w0 * wq
        - sp.Rational(1, 2) * v3[4] * wq,
    }
    assert weighted_determinant_coefficient(
        L.subs(solution6).subs(exceptional),
        special_H2.subs(solution6).subs(exceptional),
        special_H3.subs(exceptional),
        H4,
        5,
    ) == 0
    assert weighted_determinant_coefficient(
        L.subs(solution6).subs(exceptional),
        special_H2.subs(solution6).subs(exceptional),
        special_H3.subs(exceptional),
        H4,
        4,
    ) == 0
    exceptional_E3 = weighted_determinant_coefficient(
        L.subs(solution6).subs(exceptional),
        special_H2.subs(solution6).subs(exceptional),
        special_H3.subs(exceptional),
        H4,
        3,
    )
    exceptional_E3_coefficients = coefficient_dictionary(exceptional_E3, 3)
    assert (
        exceptional_E3_coefficients[x * y**2]
        == sp.Rational(4, 9) * wq**3 * sy**2
    )
    assert (
        exceptional_E3_coefficients[x * z**2]
        == -sp.Rational(4, 9) * wq**3 * sz**2
    )

    print("  PASS marked-critical finite orbit: exhaustive E6--E3 obstructions")


if __name__ == "__main__":
    open_e7_certificate()
    open_e6_e5_exit_certificate()
    noncritical_triple_certificate()
    marked_critical_certificate()
    print("PASS: finite-outer-critical finite-companion line-(2,2) certificate")

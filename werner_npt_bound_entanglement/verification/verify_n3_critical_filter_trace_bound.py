#!/usr/bin/env python3
"""Exact checks for the cubic-basis critical bound f < 51/64."""

import itertools

import sympy as sp


def hs_inner(left, right):
    return sp.simplify(sp.trace(left.conjugate().T * right))


def spectral_radius_squared_hermitian(matrix):
    eigenvalues = matrix.eigenvals()
    return sp.simplify(max(abs(value) ** 2 for value in eigenvalues))


def standard_basis():
    """HS-orthonormal real basis of traceless Hermitian M_3."""
    root_two = sp.sqrt(2)
    root_six = sp.sqrt(6)
    basis = []
    for row, column in ((0, 1), (0, 2), (1, 2)):
        symmetric = sp.zeros(3)
        symmetric[row, column] = symmetric[column, row] = 1 / root_two
        antisymmetric = sp.zeros(3)
        antisymmetric[row, column] = sp.I / root_two
        antisymmetric[column, row] = -sp.I / root_two
        basis.extend((symmetric, antisymmetric))
    basis.extend(
        (
            sp.diag(1, -1, 0) / root_two,
            sp.diag(1, 1, -2) / root_six,
        )
    )
    return basis


def adapted_sharpness_basis():
    root_two = sp.sqrt(2)
    root_six = sp.sqrt(6)
    basis = [
        sp.diag(2, -1, -1) / root_six,
        sp.diag(0, 1, -1) / root_two,
    ]
    for row, column in ((0, 1), (0, 2), (1, 2)):
        symmetric = sp.zeros(3)
        symmetric[row, column] = symmetric[column, row] = 1 / root_two
        antisymmetric = sp.zeros(3)
        antisymmetric[row, column] = sp.I / root_two
        antisymmetric[column, row] = -sp.I / root_two
        basis.extend((symmetric, antisymmetric))
    return basis


def symmetric_cubic(left, middle, right):
    matrices = (left, middle, right)
    value = 0
    for permutation in itertools.permutations(range(3)):
        value += sp.trace(
            matrices[permutation[0]]
            * matrices[permutation[1]]
            * matrices[permutation[2]]
        )
    return sp.simplify(value / 6)


def check_basis(basis):
    assert len(basis) == 8
    assert all(matrix.conjugate().T == matrix for matrix in basis)
    assert all(sp.trace(matrix) == 0 for matrix in basis)
    assert all(
        hs_inner(left, right) == int(left_index == right_index)
        for left_index, left in enumerate(basis)
        for right_index, right in enumerate(basis)
    )
    completeness = sum(
        (matrix * matrix for matrix in basis), sp.zeros(3)
    )
    assert sp.simplify(
        completeness - sp.Rational(8, 3) * sp.eye(3)
    ) == sp.zeros(3)


def check_cubic_tensor_invariants():
    basis = standard_basis()
    check_basis(basis)
    tensor = [
        [
            [symmetric_cubic(basis[a], basis[b], basis[c]) for c in range(8)]
            for b in range(8)
        ]
        for a in range(8)
    ]

    full_norm = sp.simplify(
        sum(tensor[a][b][c] ** 2 for a in range(8) for b in range(8) for c in range(8))
    )
    assert full_norm == sp.Rational(20, 3)
    trace_vector = [
        sp.simplify(sum(tensor[a][b][b] for b in range(8)))
        for a in range(8)
    ]
    assert trace_vector == [0] * 8

    # By unitary conjugation, a unit n may be put in the diagonal
    # Cartan plane.  Parameterize n=x H_1+y H_2 and its perpendicular
    # diagonal direction m=-y H_1+x H_2.
    x, y = sp.symbols("x y", real=True)
    n = x * basis[6] + y * basis[7]
    perpendicular = basis[:6] + [-y * basis[6] + x * basis[7]]
    qn = sp.expand(sp.trace(n**3))

    def reduce_unit_circle(expression):
        polynomial = sp.Poly(sp.together(sp.expand(expression)), x, y, extension=True)
        divisor = sp.Poly(x**2 + y**2 - 1, x, y, extension=True)
        remainder = sp.reduced(polynomial, [divisor])[1]
        return sp.simplify(remainder.as_expr())

    restricted_tensor = [
        [
            [symmetric_cubic(perpendicular[a], perpendicular[b], perpendicular[c])
             for c in range(7)]
            for b in range(7)
        ]
        for a in range(7)
    ]
    restricted_norm = sum(
        restricted_tensor[a][b][c] ** 2
        for a in range(7)
        for b in range(7)
        for c in range(7)
    )
    restricted_trace = [
        sum(restricted_tensor[a][b][b] for b in range(7))
        for a in range(7)
    ]
    restricted_trace_norm = sum(value**2 for value in restricted_trace)

    assert reduce_unit_circle(
        restricted_norm - (sp.Rational(14, 3) - qn**2)
    ) == 0
    assert reduce_unit_circle(
        restricted_trace_norm - (sp.Rational(1, 6) - qn**2)
    ) == 0

    n_operator_norm = sum(
        symmetric_cubic(n, basis[a], basis[b]) ** 2
        for a in range(8)
        for b in range(8)
    )
    assert reduce_unit_circle(n_operator_norm - sp.Rational(5, 6)) == 0


def check_sharpness_and_weighted_identity():
    basis = adapted_sharpness_basis()
    check_basis(basis)
    rho = sp.diag(sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 4))
    purity = sp.trace(rho * rho)
    assert purity == sp.Rational(3, 8)
    sigma = rho - sp.eye(3) / 3
    assert sp.simplify(
        sigma - basis[0] / (2 * sp.sqrt(6))
    ) == sp.zeros(3)

    radii = []
    weighted_norms = []
    for matrix in basis:
        mu = sp.trace(matrix * rho)
        centered = matrix - mu * sp.eye(3)
        assert sp.trace(centered * rho) == 0
        radii.append(spectral_radius_squared_hermitian(centered))
        weighted_norms.append(sp.trace(centered * centered * rho))

    assert radii[0] == sp.Rational(3, 8)
    assert radii[1:] == [sp.Rational(1, 2)] * 7
    assert sum(radii) == sp.Rational(31, 8)
    assert sum(radii) == sp.Rational(7, 2) + purity
    assert sp.simplify(sum(weighted_norms) - (3 - purity)) == 0


def check_spectral_cubic_relation():
    # Parameterize the eigenvalues by the positive dominant magnitude
    # r and the remaining pair x,y.
    r, x, y = sp.symbols("r x y", real=True)
    q = sp.expand(r**3 + x**3 + y**3)
    constraints = [
        x + y + r,
        x**2 + y**2 + r**2 - 1,
    ]
    groebner = sp.groebner(
        constraints, x, y, r, order="lex", domain=sp.QQ
    )
    assert groebner.reduce(
        q - 3 * r * (r**2 - sp.Rational(1, 2))
    )[1] == 0

    # Exact constants in the cubic-frame average.
    qn2 = sp.symbols("qn2", real=True)
    numerator = (
        6 * (sp.Rational(14, 3) - qn2)
        + 9 * (sp.Rational(1, 6) - qn2)
    )
    assert sp.expand(numerator) == sp.Rational(59, 2) - 15 * qn2
    assert sp.simplify(
        numerator.subs(qn2, sp.Rational(1, 6)) / (9 * 11)
        - sp.Rational(3, 11)
    ) == 0

    # Exact conversion from total cubic-square mass 3/11 to
    # spectral-radius gain.  The inverse of phi is concave because
    # phi is increasing and convex.
    spectral_excess = sp.symbols("spectral_excess", nonnegative=True)
    phi = 9 * spectral_excess**2 * (
        spectral_excess + sp.Rational(1, 2)
    )
    assert sp.expand(sp.diff(phi, spectral_excess)) == (
        27 * spectral_excess**2 + 9 * spectral_excess
    )
    assert sp.expand(sp.diff(phi, spectral_excess, 2)) == (
        54 * spectral_excess + 9
    )
    assert phi.subs(spectral_excess, sp.Rational(1, 6)) == sp.Rational(1, 6)
    remainder_mass = sp.Rational(3, 11) - sp.Rational(1, 6)
    assert remainder_mass == sp.Rational(7, 66)
    root_polynomial = sp.expand(
        66 * phi - 7
    )
    assert root_polynomial == (
        594 * spectral_excess**3
        + 297 * spectral_excess**2
        - 7
    )
    assert phi.subs(
        spectral_excess, sp.Rational(2, 15)
    ) == sp.Rational(38, 375)
    assert sp.Rational(38, 375) < sp.Rational(7, 66)


def check_final_constants():
    f, p, w1, w3 = sp.symbols("f p w1 w3", real=True)
    c = sp.Rational(2, 3)
    gamma = sp.symbols("gamma", positive=True)
    delta = f - c

    residual_bound = sp.expand(
        c * (3 - p)
        - delta * (sp.Rational(7, 2) + p + gamma)
    )
    gram_bound = sp.factor(f * p + residual_bound)
    expected_gram = (
        sp.Rational(13, 3)
        - sp.Rational(7, 2) * f
        - gamma * (f - c)
    )
    assert sp.simplify(gram_bound - expected_gram) == 0

    global_left = (
        sp.Rational(16, 3) * w1
        + sp.Rational(17, 3) * f
        + w3
    )
    summed_local = 3 * gram_bound
    final_defect = sp.factor(6 * (summed_local - global_left))
    assert sp.expand(
        final_defect
        - (
            78 + 12 * gamma
            - 32 * w1
            - (97 + 18 * gamma) * f
            - 6 * w3
        )
    ) == 0
    algebraic_ceiling = (78 + 12 * gamma) / (97 + 18 * gamma)
    assert sp.factor(sp.diff(algebraic_ceiling, gamma)) == (
        -240 / (18 * gamma + 97) ** 2
    )

    # The exact algebraic gain is gamma_*=1/6+xi, where
    # 594 xi^3+297 xi^2-7=0 and xi>2/15.  The rational relaxation
    # gamma>=3/10 gives the clean inequality
    # 80 w1+256 f+15 w3 <=204 and f<=51/64.
    rational_gamma = sp.Rational(3, 10)
    rational_defect = sp.factor(
        15 * (
            summed_local.subs(gamma, rational_gamma)
            - global_left
        )
    )
    assert rational_defect == (
        204 - 80 * w1 - 256 * f - 15 * w3
    )
    assert sp.solve(
        sp.Eq(rational_defect.subs({w1: 0, w3: 0}), 0), f
    ) == [sp.Rational(51, 64)]


def main():
    check_cubic_tensor_invariants()
    check_sharpness_and_weighted_identity()
    check_spectral_cubic_relation()
    check_final_constants()
    print(
        "verified: cubic-frame invariant identities and "
        "critical bound f < 51/64"
    )


if __name__ == "__main__":
    main()

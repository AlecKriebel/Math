#!/usr/bin/env python3
"""Exact checks for the extremal-frame critical bound f <= 42/53."""

import sympy as sp


def hs_inner(left, right):
    return sp.simplify(sp.trace(left.conjugate().T * right))


def spectral_radius_squared_hermitian(matrix):
    eigenvalues = matrix.eigenvals()
    return sp.simplify(max(abs(value) ** 2 for value in eigenvalues))


def elementary_adapted_basis():
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


def check_basis_and_weighted_identity():
    basis = elementary_adapted_basis()
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


def check_probability_segment():
    # For lambda=(a,b,-a-b) with a>=b>=0, the endpoint on w0=0
    # has squared norm at least 5/9.
    a, b = sp.symbols("a b", nonnegative=True)
    denominator = a + 2 * b
    w1 = (a + b) / denominator
    w2 = b / denominator
    endpoint_excess = sp.factor(
        w1**2 + w2**2 - sp.Rational(5, 9)
    )
    assert sp.simplify(
        endpoint_excess
        - (
            2 * (a - b) * (2 * a + b)
            / (9 * (a + 2 * b) ** 2)
        )
    ) == 0
    assert sp.simplify(
        b * w1 - (a + b) * w2
    ) == 0


def check_phase_orbit_identity():
    w0, w1 = sp.symbols("w0 w1", real=True)
    w2 = 1 - w0 - w1
    omega = (-1 + sp.sqrt(3) * sp.I) / 2
    overlap = w0 + w1 * omega + w2 * omega**2
    overlap_squared = sp.simplify(
        sp.expand_complex(overlap * sp.conjugate(overlap))
    )
    purity = sp.expand(w0**2 + w1**2 + w2**2)
    assert sp.simplify(
        overlap_squared - (3 * purity - 1) / 2
    ) == 0
    assert (
        (3 * sp.Rational(5, 9) - 1) / 2
        == sp.Rational(1, 3)
    )

    # Explicit exact realization at the most degenerate normal
    # direction: weights (1/3,2/3,0) form a trine.
    weights = (sp.Rational(1, 3), sp.Rational(2, 3), 0)
    normal = sp.diag(2, -1, -1) / sp.sqrt(6)
    extremals = []
    for j in range(3):
        state = sp.Matrix(
            [
                sp.sqrt(weights[k]) * omega ** (j * k)
                for k in range(3)
            ]
        )
        projector = state * state.conjugate().T
        extremal = (3 * projector - sp.eye(3)) / sp.sqrt(6)
        assert sp.simplify(hs_inner(extremal, normal)) == 0
        assert sp.simplify(hs_inner(extremal, extremal)) == 1
        assert spectral_radius_squared_hermitian(extremal) == sp.Rational(2, 3)
        extremals.append(extremal)
    assert all(
        sp.simplify(hs_inner(extremals[j], extremals[k])) == int(j == k)
        for j in range(3)
        for k in range(3)
    )


def check_final_constants():
    f, p, w1, w3, frame_sum = sp.symbols(
        "f p w1 w3 frame_sum", real=True
    )
    c = sp.Rational(2, 3)
    delta = f - c

    # The three extremal directions plus four ordinary directions give
    # sum_{a=2}^8 r(F_a)^2 >= 3(2/3)+4(1/2)=4.
    assert 3 * sp.Rational(2, 3) + 4 * sp.Rational(1, 2) == 4
    residual_bound = sp.expand(c * (3 - p) - delta * (4 + p))
    gram_bound = sp.factor(f * p + residual_bound)
    assert sp.simplify(
        gram_bound - (sp.Rational(14, 3) - 4 * f)
    ) == 0

    global_left = (
        sp.Rational(16, 3) * w1
        + sp.Rational(17, 3) * f
        + w3
    )
    summed_local = 3 * gram_bound
    final_defect = sp.factor(3 * (summed_local - global_left))
    assert final_defect == 42 - 16 * w1 - 53 * f - 3 * w3
    assert sp.solve(
        sp.Eq(final_defect.subs({w1: 0, w3: 0}), 0), f
    ) == [sp.Rational(42, 53)]

    # Exact no-go for every scalar adapted-frame trace improvement.
    general_residual = sp.expand(
        c * (3 - p) - delta * (frame_sum + p)
    )
    general_gram = sp.factor(f * p + general_residual)
    assert sp.simplify(
        general_gram - (2 + sp.Rational(2, 3) * frame_sum - frame_sum * f)
    ) == 0
    general_global_defect = sp.factor(
        3 * (3 * general_gram - global_left)
    )
    assert sp.expand(
        general_global_defect
        - (
            18
            + 6 * frame_sum
            - 16 * w1
            - (17 + 9 * frame_sum) * f
            - 3 * w3
        )
    ) == 0
    scalar_ceiling = (18 + 6 * frame_sum) / (17 + 9 * frame_sum)
    assert sp.simplify(
        scalar_ceiling
        - sp.Rational(2, 3)
        - 20 / (3 * (9 * frame_sum + 17))
    ) == 0
    assert sp.simplify(
        sp.diff(scalar_ceiling, frame_sum)
        + 60 / (9 * frame_sum + 17) ** 2
    ) == 0
    ideal_sum = sp.Rational(14, 3)
    assert scalar_ceiling.subs(frame_sum, ideal_sum) == sp.Rational(46, 59)
    assert sp.Rational(46, 59) > sp.Rational(2, 3)


def main():
    check_basis_and_weighted_identity()
    check_probability_segment()
    check_phase_orbit_identity()
    check_final_constants()
    print(
        "verified: three-extremal-direction construction and "
        "critical bound f <= 42/53; scalar trace ceiling 46/59"
    )


if __name__ == "__main__":
    main()

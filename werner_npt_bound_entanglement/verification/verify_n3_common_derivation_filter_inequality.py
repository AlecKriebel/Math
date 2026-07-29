#!/usr/bin/env python3
"""Exact checks for the common-derivation filter identities."""

import sympy as sp


def hs_inner(left, right):
    return sp.simplify(sp.trace(left.conjugate().T * right))


def partial_trace_second(matrix, first_dimension, second_dimension):
    out = sp.zeros(first_dimension)
    for a in range(first_dimension):
        for b in range(first_dimension):
            out[a, b] = sum(
                matrix[a * second_dimension + k, b * second_dimension + k]
                for k in range(second_dimension)
            )
    return out


def local(matrix, environment_dimension):
    return sp.kronecker_product(matrix, sp.eye(environment_dimension))


def traceless_hermitian_basis():
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


def check_gram_superoperator():
    # A normalized, rank-two, nonnormal exact operator on C^3 tensor C^2.
    root_three = sp.sqrt(3)
    operator = sp.zeros(6)
    operator[0, 1] = 1 / root_three
    operator[2, 4] = sp.sqrt(sp.Rational(2, 3))
    assert operator.rank() == 2
    assert hs_inner(operator, operator) == 1

    left_reduction = partial_trace_second(
        operator * operator.conjugate().T, 3, 2
    )
    right_reduction = partial_trace_second(
        operator.conjugate().T * operator, 3, 2
    )
    assert sp.trace(left_reduction) == 1
    assert sp.trace(right_reduction) == 1

    units = []
    for row in range(3):
        for column in range(3):
            unit = sp.zeros(3)
            unit[row, column] = 1
            units.append(unit)

    for test in units:
        lifted = local(test, 2)
        commutator = lifted * operator - operator * lifted
        ell = sp.trace(test * left_reduction)
        right = sp.trace(test * right_reduction)
        assert sp.simplify(
            hs_inner(operator, commutator) - (ell - right)
        ) == 0
        residual = commutator - (ell - right) * operator
        assert hs_inner(operator, residual) == 0
        assert sp.simplify(
            hs_inner(residual, residual)
            - hs_inner(commutator, commutator)
            + sp.conjugate(ell - right) * (ell - right)
        ) == 0

        phi = partial_trace_second(
            operator * lifted * operator.conjugate().T, 3, 2
        )
        psi = partial_trace_second(
            operator.conjugate().T * lifted * operator, 3, 2
        )
        gram_image = (
            test * left_reduction
            + right_reduction * test
            - phi
            - psi
        )
        for probe in units:
            probe_commutator = (
                local(probe, 2) * operator
                - operator * local(probe, 2)
            )
            assert sp.simplify(
                hs_inner(probe, gram_image)
                - hs_inner(probe_commutator, commutator)
            ) == 0


def check_derivation_integrability():
    # Use two physical qutrit sites so both same-site and cross-site
    # identities are checked exactly.
    operator = sp.zeros(9)
    operator[0, 1] = sp.Rational(1, 2)
    operator[3, 8] = sp.sqrt(3) / 2
    a = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    b = sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
    identity = sp.eye(3)
    a_first = sp.kronecker_product(a, identity)
    b_first = sp.kronecker_product(b, identity)
    a_second = sp.kronecker_product(identity, a)
    b_second = sp.kronecker_product(identity, b)

    def commutator(left, right):
        return left * right - right * left

    c_first_a = commutator(a_first, operator)
    c_first_b = commutator(b_first, operator)
    c_first_ab = commutator(
        sp.kronecker_product(a * b, identity), operator
    )
    assert sp.simplify(
        c_first_ab
        - a_first * c_first_b
        - c_first_a * b_first
    ) == sp.zeros(9)
    assert sp.simplify(
        commutator(a_first, c_first_b)
        - commutator(b_first, c_first_a)
        - commutator(
            sp.kronecker_product(a * b - b * a, identity),
            operator,
        )
    ) == sp.zeros(9)
    assert sp.simplify(
        commutator(a_first, commutator(b_second, operator))
        - commutator(b_second, c_first_a)
    ) == sp.zeros(9)


def check_scalar_certificate():
    # The exact algebra behind equation (15).
    x2, y2, real_cross, slack_left, slack_right = sp.symbols(
        "x2 y2 real_cross slack_left slack_right", real=True
    )
    difference2 = x2 + y2 - 2 * real_cross
    sum2 = x2 + y2 + 2 * real_cross
    upper_left = x2 + slack_left
    upper_right = y2 + slack_right
    certificate = sp.expand(
        2 * upper_left
        + 2 * upper_right
        - difference2
        - (2 * slack_left + 2 * slack_right + sum2)
    )
    assert certificate == 0


def check_pair_casimir_countermodel():
    basis = traceless_hermitian_basis()
    identity = sp.eye(3)
    normalized_identity = identity / sp.sqrt(3)
    zero = sp.zeros(27)
    omega_12 = sum(
        (
            sp.kronecker_product(
                matrix, matrix, normalized_identity
            )
            for matrix in basis
        ),
        zero,
    )
    omega_13 = sum(
        (
            sp.kronecker_product(
                matrix, normalized_identity, matrix
            )
            for matrix in basis
        ),
        zero,
    )
    omega_23 = sum(
        (
            sp.kronecker_product(
                normalized_identity, matrix, matrix
            )
            for matrix in basis
        ),
        zero,
    )
    pair_terms = (omega_12, omega_13, omega_23)
    assert all(hs_inner(term, term) == 8 for term in pair_terms)
    assert all(
        hs_inner(pair_terms[j], pair_terms[k]) == int(j == k) * 8
        for j in range(3)
        for k in range(3)
    )
    d_star = sum(pair_terms, zero) / 6
    assert hs_inner(d_star, d_star) == sp.Rational(2, 3)
    assert d_star.conjugate().T == d_star

    # At every site the commutator Gram is exactly (1/3) times
    # identity on the eight-dimensional traceless subspace.
    for site in range(3):
        commutators = []
        for matrix in basis:
            factors = [identity, identity, identity]
            factors[site] = matrix
            lifted = sp.kronecker_product(*factors)
            commutators.append(lifted * d_star - d_star * lifted)
        assert all(
            sp.simplify(
                hs_inner(commutators[a], commutators[b])
                - sp.Rational(1, 3) * int(a == b)
            ) == 0
            for a in range(8)
            for b in range(8)
        )

    # Formal residual and sector arithmetic for general f.
    f = sp.symbols("f", positive=True)
    z_squared = 5 * f / 72
    commutator_quarter = f / 8
    residual_coefficient = sp.factor(
        z_squared + commutator_quarter
    )
    assert residual_coefficient == 7 * f / 36
    delta = f - sp.Rational(2, 3)
    worst_filter_left = sp.factor(
        residual_coefficient
        + sp.Rational(2, 3) * delta
    )
    assert sp.simplify(
        sp.Rational(2, 9)
        - worst_filter_left
        - (24 - 31 * f) / 36
    ) == 0

    site_gram_trace = sp.factor(
        f / 3 + 8 * residual_coefficient
    )
    assert site_gram_trace == 17 * f / 9
    assert 3 * site_gram_trace == 17 * f / 3
    residual_trace = 3 * 8 * residual_coefficient
    residual_cross = sp.factor(
        3 * 8 * (z_squared - commutator_quarter)
    )
    difference_trace = 3 * 8 * (f / 2)
    assert residual_trace == 14 * f / 3
    assert residual_cross == -4 * f / 3
    assert difference_trace == 12 * f


def main():
    check_gram_superoperator()
    check_derivation_integrability()
    check_scalar_certificate()
    check_pair_casimir_countermodel()
    print(
        "verified: commutator Gram, residual projection, "
        "filter SOS, derivation integrability, and "
        "pair-Casimir obstruction through f=24/31"
    )


if __name__ == "__main__":
    main()

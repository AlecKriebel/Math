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


def main():
    check_gram_superoperator()
    check_derivation_integrability()
    check_scalar_certificate()
    print(
        "verified: commutator Gram, residual projection, "
        "filter SOS, and derivation integrability"
    )


if __name__ == "__main__":
    main()

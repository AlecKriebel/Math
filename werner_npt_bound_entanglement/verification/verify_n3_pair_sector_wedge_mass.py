#!/usr/bin/env python3
"""Dependency-free exact checks for the pair-sector wedge-mass note."""

from fractions import Fraction as F


def poly_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, F(0)) + coefficient
    return {
        monomial: coefficient
        for monomial, coefficient in out.items()
        if coefficient
    }


def poly_scale(polynomial, scalar):
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def poly_multiply(left, right):
    out = {}
    for first, coefficient_first in left.items():
        for second, coefficient_second in right.items():
            monomial = tuple(
                first[index] + second[index]
                for index in range(len(first))
            )
            out[monomial] = (
                out.get(monomial, F(0))
                + coefficient_first * coefficient_second
            )
    return {
        monomial: coefficient
        for monomial, coefficient in out.items()
        if coefficient
    }


def variable(index):
    monomial = [0] * 4
    monomial[index] = 1
    return {tuple(monomial): F(1)}


def tensor(left, right):
    out = {}
    for left_index, left_value in left.items():
        for right_index, right_value in right.items():
            key = (left_index, right_index)
            out[key] = out.get(key, F(0)) + left_value * right_value
    return {key: value for key, value in out.items() if value}


def vector_add(left, right, right_scale=F(1)):
    out = dict(left)
    for index, value in right.items():
        out[index] = out.get(index, F(0)) + right_scale * value
    return {index: value for index, value in out.items() if value}


def main():
    # Formal verification of the universal polynomial identity (6).
    # Variables are g11, g22, Re(g12), Im(g12).
    g11, g22, real12, imag12 = [variable(index) for index in range(4)]
    one = {(0, 0, 0, 0): F(1)}
    abs12_squared = poly_add(
        poly_multiply(real12, real12),
        poly_multiply(imag12, imag12),
    )
    a2 = poly_add(poly_multiply(g11, g22), poly_scale(abs12_squared, -1))
    a0 = poly_add(
        poly_multiply(poly_add(one, poly_scale(g11, -1)),
                      poly_add(one, poly_scale(g22, -1))),
        poly_scale(abs12_squared, -1),
    )
    a1 = poly_add(
        poly_add(one, poly_scale(a0, -1)),
        poly_scale(a2, -1),
    )
    wedge_expression = poly_scale(
        poly_add(
            poly_add(poly_scale(a0, 4), poly_scale(a1, -2)),
            a2,
        ),
        F(1, 9),
    )
    determinant = poly_add(
        poly_multiply(
            poly_add(poly_scale(one, F(2, 3)), poly_scale(g11, -1)),
            poly_add(poly_scale(one, F(2, 3)), poly_scale(g22, -1)),
        ),
        poly_scale(abs12_squared, -1),
    )
    assert wedge_expression == determinant

    # Verify the common-origin identity without irrational numbers.
    # With unnormalized wedge/symmetric tensors, it reads
    # 2(E1 tensor E2 - E2 tensor E1)
    # = u_wedge tensor v_symmetric + u_symmetric tensor v_wedge.
    u1 = {0: F(1)}
    u2 = {1: F(1)}
    v1 = {0: F(1)}
    v2 = {1: F(1)}
    e1 = tensor(u1, v1)
    e2 = tensor(u2, v2)
    left = vector_add(tensor(e1, e2), tensor(e2, e1), F(-1))
    left = {index: 2 * value for index, value in left.items()}
    u_wedge = vector_add(tensor(u1, u2), tensor(u2, u1), F(-1))
    u_symmetric = vector_add(tensor(u1, u2), tensor(u2, u1))
    v_wedge = vector_add(tensor(v1, v2), tensor(v2, v1), F(-1))
    v_symmetric = vector_add(tensor(v1, v2), tensor(v2, v1))
    right = vector_add(
        tensor(u_wedge, v_symmetric),
        tensor(u_symmetric, v_wedge),
    )

    # The tensor nesting differs: regroup ((u,v),(u,v)) to
    # ((u,u),(v,v)) before comparison.
    regrouped_left = {}
    for ((first_u, first_v), (second_u, second_v)), value in left.items():
        key = ((first_u, second_u), (first_v, second_v))
        regrouped_left[key] = value
    assert regrouped_left == right

    # Sharp shifted-Gram example: G is the all-ones matrix divided by 3.
    g11_value = F(1, 3)
    g22_value = F(1, 3)
    abs12_squared_value = F(1, 9)
    a2_value = g11_value * g22_value - abs12_squared_value
    a0_value = (
        (1 - g11_value) * (1 - g22_value)
        - abs12_squared_value
    )
    a1_value = 1 - a0_value - a2_value
    assert (a0_value, a1_value, a2_value) == (
        F(1, 3), F(2, 3), F(0)
    )
    assert 6 * a0_value + 3 * a2_value == 2

    print(
        "verified: compound determinant, common-origin Pluecker split, "
        "and sharp wedge masses"
    )


if __name__ == "__main__":
    main()

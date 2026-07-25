#!/usr/bin/env python3
"""Deterministic modular certificate for the level-five transposition."""

from __future__ import annotations

from finite_field_norm_depth4 import (
    deepest_norm,
    deepest_norm_derivative,
    hensel_profile,
    tower_profile,
)


PRIME = 23
PARAMETER = 3
EXPECTED_PROFILE = {
    "dimension": 81,
    "discriminant_norms": (10, 22, 10, 4, 0),
    "leading_norms": (2, 14, 19, 11, 1),
    "reconstruction_guard_norms": (
        18,
        14,
        5,
        2,
        8,
        21,
        13,
        13,
        7,
        8,
        17,
        12,
    ),
}
EXPECTED_LIFTED_NORMS = (460, 299, 138)
EXPECTED_DERIVATIVE = 16


Dual = tuple[int, int]


def dual_add(left: Dual, right: Dual) -> Dual:
    return ((left[0] + right[0]) % PRIME, (left[1] + right[1]) % PRIME)


def dual_neg(value: Dual) -> Dual:
    return (-value[0] % PRIME, -value[1] % PRIME)


def dual_sub(left: Dual, right: Dual) -> Dual:
    return dual_add(left, dual_neg(right))


def dual_mul(left: Dual, right: Dual) -> Dual:
    return (
        left[0] * right[0] % PRIME,
        (left[1] * right[0] + left[0] * right[1]) % PRIME,
    )


def dual_scale(value: Dual, scalar: int) -> Dual:
    return (scalar * value[0] % PRIME, scalar * value[1] % PRIME)


def dual_inverse(value: Dual) -> Dual:
    inverse_value = pow(value[0], -1, PRIME)
    return (
        inverse_value,
        -value[1] * inverse_value * inverse_value % PRIME,
    )


def dual_divide(numerator: Dual, denominator: Dual) -> Dual:
    return dual_mul(numerator, dual_inverse(denominator))


def dual_power(value: Dual, exponent: int) -> Dual:
    result = (1, 0)
    base = value
    while exponent:
        if exponent & 1:
            result = dual_mul(result, base)
        base = dual_mul(base, base)
        exponent //= 2
    return result


def dual_reconstruct(
    point: tuple[Dual, Dual, Dual], root: Dual
) -> tuple[Dual, Dual, Dual]:
    """Independently transcribe the rational inverse reconstruction."""
    _a, b, c = point
    root2 = dual_power(root, 2)
    numerator_y = dual_add(
        dual_add(dual_mul(b, root2), dual_scale(c, 3)),
        dual_scale(root, -6),
    )
    y = dual_neg(dual_divide(numerator_y, dual_scale(root2, 2)))
    x = dual_divide(root, dual_sub((1, 0), dual_mul(root, y)))
    numerator_z = dual_sub(
        dual_sub(
            dual_scale(x, 2),
            dual_scale(dual_mul(dual_power(x, 2), y), 3),
        ),
        c,
    )
    z = dual_divide(numerator_z, dual_power(x, 3))
    return x, y, z


def dual_discriminant(point: tuple[Dual, Dual, Dual]) -> Dual:
    a, b, c = point
    result = dual_scale(dual_mul(dual_power(a, 2), dual_power(c, 2)), 27)
    result = dual_add(result, dual_scale(dual_mul(dual_mul(a, b), c), -18))
    result = dual_add(result, dual_scale(a, 16))
    result = dual_add(result, dual_mul(dual_power(b, 3), c))
    return dual_sub(result, dual_power(b, 2))


def lift_simple_root(
    point: tuple[Dual, Dual, Dual], root_value: int
) -> Dual:
    """Implicitly differentiate one inverse-cubic root."""
    a, b, c = point
    polynomial_value = (
        2 * a[0] * root_value**3
        - b[0] * root_value**2
        + 2 * root_value
        - c[0]
    ) % PRIME
    derivative_in_root = (
        6 * a[0] * root_value**2 - 2 * b[0] * root_value + 2
    ) % PRIME
    assert polynomial_value == 0
    assert derivative_in_root != 0
    explicit_derivative = (
        2 * a[1] * root_value**3 - b[1] * root_value**2 - c[1]
    ) % PRIME
    root_derivative = (
        -explicit_derivative * pow(derivative_in_root, -1, PRIME)
    )
    return root_value % PRIME, root_derivative % PRIME


def scalar_reconstruct(
    point: tuple[int, int, int], root: int
) -> tuple[int, int, int]:
    _a, b, c = point
    y = -(
        b * root**2 + 3 * c - 6 * root
    ) * pow(2 * root**2, -1, PRIME) % PRIME
    x = root * pow(1 - root * y, -1, PRIME) % PRIME
    z = (
        (2 * x - 3 * x**2 * y - c) * pow(x**3, -1, PRIME)
    ) % PRIME
    return x, y, z


def scalar_discriminant(point: tuple[int, int, int]) -> int:
    a, b, c = point
    return (
        27 * a**2 * c**2
        - 18 * a * b * c
        + 16 * a
        + b**3 * c
        - b**2
    ) % PRIME


def check_explicit_sheet() -> None:
    """Check the vanishing sheet without quotient-algebra determinants."""
    point: tuple[Dual, Dual, Dual] = ((1, 0), (2, 0), (PARAMETER, 1))
    root_path = (10, 22, 13, 1)
    expected_points = (
        ((2, 0), (18, 2), (22, 17)),
        ((11, 19), (1, 8), (6, 16)),
        ((10, 7), (9, 9), (13, 13)),
        ((22, 12), (2, 16), (21, 5)),
    )
    for root_value, expected_point in zip(root_path, expected_points):
        root = lift_simple_root(point, root_value)
        point = dual_reconstruct(point, root)
        assert point == expected_point
    assert dual_discriminant(point) == (0, 18)

    a, b, c = (coordinate[0] for coordinate in point)
    roots = tuple(
        value
        for value in range(PRIME)
        if (2 * a * value**3 - b * value**2 + 2 * value - c) % PRIME
        == 0
    )
    assert roots == (1, 22)
    root_derivatives = tuple(
        (6 * a * value**2 - 2 * b * value + 2) % PRIME
        for value in roots
    )
    assert root_derivatives[0] != 0
    assert root_derivatives[1] == 0

    states = [((1, 2, PARAMETER), ())]
    rational_sheet_counts = []
    for _level in range(4):
        next_states = []
        for scalar_point, path in states:
            scalar_a, scalar_b, scalar_c = scalar_point
            for root_value in range(PRIME):
                if (
                    2 * scalar_a * root_value**3
                    - scalar_b * root_value**2
                    + 2 * root_value
                    - scalar_c
                ) % PRIME:
                    continue
                next_states.append(
                    (
                        scalar_reconstruct(scalar_point, root_value),
                        path + (root_value,),
                    )
                )
        states = next_states
        rational_sheet_counts.append(len(states))
    assert tuple(rational_sheet_counts) == (3, 3, 3, 7)
    assert [
        (scalar_point, path)
        for scalar_point, path in states
        if scalar_discriminant(scalar_point) == 0
    ] == [((22, 2, 21), (10, 22, 13, 1))]


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)


def conjugate(
    element: tuple[int, ...], by: tuple[int, ...]
) -> tuple[int, ...]:
    return compose(compose(by, element), inverse(by))


def power(permutation: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(permutation)))
    base = permutation
    while exponent:
        if exponent & 1:
            result = compose(result, base)
        base = compose(base, base)
        exponent //= 2
    return result


def generated_group(
    generators: tuple[tuple[int, ...], ...]
) -> set[tuple[int, ...]]:
    identity = tuple(range(len(generators[0])))
    result = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            product = compose(element, generator)
            if product not in result:
                result.add(product)
                frontier.append(product)
    return result


def check_kernel_lemma() -> None:
    """A 243-cycle and one leaf transposition generate S_3^81."""
    cycle = tuple((index + 1) % 243 for index in range(243))
    transposition_list = list(range(243))
    transposition_list[0], transposition_list[81] = 81, 0
    transposition = tuple(transposition_list)
    within_block = power(cycle, 81)
    local = generated_group(
        (transposition, conjugate(transposition, within_block))
    )
    assert len(local) == 6
    assert {
        index
        for permutation in local
        for index, image in enumerate(permutation)
        if image != index
    } == {0, 81, 162}

    supports = []
    for shift in range(81):
        shifted = power(cycle, shift)
        shifted_local = {
            conjugate(element, shifted) for element in local
        }
        support = {
            index
            for permutation in shifted_local
            for index, image in enumerate(permutation)
            if image != index
        }
        assert len(shifted_local) == 6
        assert support == {shift, shift + 81, shift + 162}
        supports.append(support)
    assert set().union(*supports) == set(range(243))
    assert sum(map(len, supports)) == 243


def main() -> None:
    profile = tower_profile(PRIME, PARAMETER)
    assert profile == EXPECTED_PROFILE

    hensel = hensel_profile(PRIME, PARAMETER)
    assert hensel["modulus"] == PRIME * PRIME
    assert hensel["lifted_parameters"] == (3, 26, 49)
    assert hensel["lifted_norms"] == EXPECTED_LIFTED_NORMS
    assert hensel["divided_differences_mod_p"] == (16, 9)
    assert hensel["derivative_mod_p"] == EXPECTED_DERIVATIVE
    assert deepest_norm_derivative(PRIME, PARAMETER) == EXPECTED_DERIVATIVE
    assert deepest_norm(PRIME, PARAMETER) == 0

    discriminants = profile["discriminant_norms"]
    assert isinstance(discriminants, tuple)
    assert all(value != 0 for value in discriminants[:-1])
    assert discriminants[-1] == 0
    for label in ("leading_norms", "reconstruction_guard_norms"):
        values = profile[label]
        assert isinstance(values, tuple)
        assert all(value != 0 for value in values)

    check_explicit_sheet()
    check_kernel_lemma()

    print("PASS p=23, s=3: every lower branch norm and guard is a unit")
    print("PASS deepest norm is zero with derivative 16 mod 23")
    print("PASS sheet (10,22,13,1): Delta=0 with derivative 18")
    print("PASS final cubic has a double root 22 and simple root 1")
    print("PASS W5 kernel lemma: deepest transposition generates S_3^81")


if __name__ == "__main__":
    main()

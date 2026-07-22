#!/usr/bin/env python3
"""Deterministic modular certificate for the W4 transposition.

This script recomputes the one useful specialization from the quotient tower;
the exploratory full-field scan is checked only for integrity and is not an
input to the mathematical certificate.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from finite_field_norm import deepest_norm, deepest_norm_derivative, tower_profile


PRIME = 1009
PARAMETER = 801
EXPECTED_PROFILE = {
    "discriminant_norms": (497, 650, 840, 0),
    "leading_norms": (2, 511, 972, 127),
    "reconstruction_guard_norms": (
        763,
        881,
        827,
        437,
        517,
        668,
        247,
        706,
        985,
    ),
}
EXPECTED_N_AT_S_MOD_P2 = 655850
EXPECTED_N_AT_S_PLUS_P_MOD_P2 = 563022
EXPECTED_N_AT_S_PLUS_2P_MOD_P2 = 470194
EXPECTED_DERIVATIVE = 917
EXPECTED_SCAN_SHA256 = "c48e3f4b7e402e6bf8076ca0b83702590a6df241bb8c42bcc08d81f0fe28fda4"
EXPECTED_EXCEPTIONAL = (0, 2, 99, 540, 708, 769)


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
    """Independently transcribe the three rational reconstruction formulas."""
    _a, b, c = point
    root2 = dual_power(root, 2)
    numerator_y = dual_add(
        dual_add(dual_mul(b, root2), dual_scale(c, 3)),
        dual_scale(root, -6),
    )
    y = dual_neg(dual_divide(numerator_y, dual_scale(root2, 2)))
    x = dual_divide(root, dual_sub((1, 0), dual_mul(root, y)))
    numerator_z = dual_sub(
        dual_sub(dual_scale(x, 2), dual_scale(dual_mul(dual_power(x, 2), y), 3)),
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
    """Implicitly differentiate one inverse cubic root modulo ``PRIME``."""
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
    root_derivative = -explicit_derivative * pow(derivative_in_root, -1, PRIME)
    return root_value % PRIME, root_derivative % PRIME


def check_explicit_sheet() -> None:
    """Check the unique vanishing sheet without quotient-algebra determinants."""
    point: tuple[Dual, Dual, Dual] = ((1, 0), (2, 0), (PARAMETER, 1))
    root_path = (803, 282, 899)
    expected_points = (
        ((77, 395), (620, 532), (874, 194)),
        ((984, 859), (54, 582), (608, 526)),
        ((727, 453), (885, 915), (561, 443)),
    )
    for root_value, expected_point in zip(root_path, expected_points):
        root = lift_simple_root(point, root_value)
        point = dual_reconstruct(point, root)
        assert point == expected_point
    assert dual_discriminant(point) == (0, 527)

    # The final cubic has one simple root and one double root modulo p.
    a, b, c = (coordinate[0] for coordinate in point)
    roots = tuple(
        value
        for value in range(PRIME)
        if (2 * a * value**3 - b * value**2 + 2 * value - c) % PRIME == 0
    )
    assert roots == (171, 437)
    root_derivatives = tuple(
        (6 * a * value**2 - 2 * b * value + 2) % PRIME for value in roots
    )
    assert root_derivatives[0] != 0
    assert root_derivatives[1] == 0


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
    """An 81-cycle and one leaf transposition generate S_3^27."""
    cycle = tuple((index + 1) % 81 for index in range(81))
    transposition_list = list(range(81))
    transposition_list[0], transposition_list[27] = 27, 0
    transposition = tuple(transposition_list)
    within_block = power(cycle, 27)
    local = generated_group(
        (transposition, conjugate(transposition, within_block))
    )
    assert len(local) == 6
    assert {
        index
        for permutation in local
        for index, image in enumerate(permutation)
        if image != index
    } == {0, 27, 54}

    # The first 27 cycle-conjugates have pairwise disjoint three-point
    # supports and therefore generate the direct product of 27 local S_3's.
    supports = []
    for shift in range(27):
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
        assert support == {shift, shift + 27, shift + 54}
        supports.append(support)
    assert set().union(*supports) == set(range(81))
    assert sum(map(len, supports)) == 81
    assert 6**27 == 1023490369077469249536
    assert 6**40 == 13367494538843734067838845976576


def check_scan_integrity() -> None:
    scan = Path(__file__).with_name("scan_p1009.jsonl")
    raw = scan.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SCAN_SHA256
    records = [json.loads(line) for line in raw.splitlines()]
    assert len(records) == PRIME
    assert [record["s"] for record in records] == list(range(PRIME))
    exceptional = tuple(
        record["s"] for record in records if record["status"] == "exceptional"
    )
    roots = tuple(
        record["s"]
        for record in records
        if record["status"] == "ok" and record["norm"] == 0
    )
    assert exceptional == EXPECTED_EXCEPTIONAL
    assert roots == (PARAMETER,)


def main() -> None:
    profile = tower_profile(PRIME, PARAMETER)
    assert profile == EXPECTED_PROFILE

    modulus = PRIME * PRIME
    at_s = deepest_norm(modulus, PARAMETER)
    at_s_plus_p = deepest_norm(modulus, PARAMETER + PRIME)
    at_s_plus_2p = deepest_norm(modulus, PARAMETER + 2 * PRIME)
    assert at_s == EXPECTED_N_AT_S_MOD_P2
    assert at_s_plus_p == EXPECTED_N_AT_S_PLUS_P_MOD_P2
    assert at_s_plus_2p == EXPECTED_N_AT_S_PLUS_2P_MOD_P2
    difference = (at_s_plus_p - at_s) % modulus
    assert difference == PRIME * EXPECTED_DERIVATIVE
    assert (at_s_plus_2p - at_s) % modulus == 2 * PRIME * EXPECTED_DERIVATIVE % modulus
    assert deepest_norm_derivative(PRIME, PARAMETER) == EXPECTED_DERIVATIVE
    assert EXPECTED_DERIVATIVE != 0

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
    check_scan_integrity()

    print("PASS p=1009, s=801: lower branch norms are units")
    print("PASS every cubic-leading and reconstruction guard is a unit")
    print("PASS deepest branch norm is zero with derivative 917 mod 1009")
    print("PASS explicit sheet (803,282,899): Delta=0 with derivative 527")
    print("PASS full scan integrity: one usable root, six exceptional values")
    print("PASS W4 kernel lemma: deepest transposition generates S_3^27")


if __name__ == "__main__":
    main()

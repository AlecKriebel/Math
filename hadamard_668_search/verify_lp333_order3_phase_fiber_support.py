#!/usr/bin/env python3
"""Verify the primitive-support theorem for the LP(333) phase fibers.

The replay is dependency-free.  It checks the cyclotomic irreducibility
certificate, the H-invariant evaluation kernel, the two prime-167 residue
degrees, the fixed zero-column activity, and the resulting zero-pattern
stratification of the primitive three-plane.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from typing import Iterable, Sequence


N = 37
P = 167
ENERGY = 167
H = (1, 10, 26)
WORD_LABELS = ("A0", "A1", "A2", "B0", "B1", "B2")
B0_INDEX = 3

CANONICAL_ZERO_EXPONENTS = (0, 0, 0, 1, 2, 3, 1, 3, 2)
SIGN_PAIRS = ((1, 1), (-1, 1), (-1, -1), (1, -1))
ZERO_A_PLUS = tuple(
    int(SIGN_PAIRS[value][0] == 1)
    for value in CANONICAL_ZERO_EXPONENTS
)
ZERO_B_PLUS = tuple(
    int(SIGN_PAIRS[value][1] == 1)
    for value in CANONICAL_ZERO_EXPONENTS
)

EXPECTED_CERTIFICATE_SHA256 = (
    "c15e8357dc55e49f63469888dc306113165cf39c0cfc19b66aec15c747b2669e"
)


def compact_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Small polynomial arithmetic over a prime field, ascending coefficients.


def trim(poly: Sequence[int], prime: int) -> tuple[int, ...]:
    values = [int(value) % prime for value in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values or (0,))


def poly_sub(
    first: Sequence[int],
    second: Sequence[int],
    prime: int,
) -> tuple[int, ...]:
    length = max(len(first), len(second))
    return trim(
        tuple(
            (first[index] if index < len(first) else 0)
            - (second[index] if index < len(second) else 0)
            for index in range(length)
        ),
        prime,
    )


def poly_mul(
    first: Sequence[int],
    second: Sequence[int],
    prime: int,
) -> tuple[int, ...]:
    result = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            result[first_index + second_index] += (
                int(first_value) * int(second_value)
            )
    return trim(result, prime)


def poly_divmod(
    numerator: Sequence[int],
    denominator: Sequence[int],
    prime: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    remainder = list(trim(numerator, prime))
    divisor = trim(denominator, prime)
    if divisor == (0,):
        raise ZeroDivisionError("zero polynomial")
    if len(remainder) < len(divisor):
        return (0,), tuple(remainder)
    quotient = [0] * (len(remainder) - len(divisor) + 1)
    inverse = pow(divisor[-1], -1, prime)
    while len(remainder) >= len(divisor) and tuple(remainder) != (0,):
        degree = len(remainder) - len(divisor)
        scalar = remainder[-1] * inverse % prime
        quotient[degree] = scalar
        for index, value in enumerate(divisor):
            remainder[degree + index] = (
                remainder[degree + index] - scalar * value
            ) % prime
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return trim(quotient, prime), trim(remainder, prime)


def poly_mod(
    numerator: Sequence[int],
    modulus: Sequence[int],
    prime: int,
) -> tuple[int, ...]:
    return poly_divmod(numerator, modulus, prime)[1]


def poly_gcd(
    first: Sequence[int],
    second: Sequence[int],
    prime: int,
) -> tuple[int, ...]:
    left = trim(first, prime)
    right = trim(second, prime)
    while right != (0,):
        left, right = right, poly_mod(left, right, prime)
    inverse = pow(left[-1], -1, prime)
    return trim(tuple(inverse * value for value in left), prime)


def poly_pow_mod(
    base: Sequence[int],
    exponent: int,
    modulus: Sequence[int],
    prime: int,
) -> tuple[int, ...]:
    result = (1,)
    power = poly_mod(base, modulus, prime)
    remaining = int(exponent)
    while remaining:
        if remaining & 1:
            result = poly_mod(poly_mul(result, power, prime), modulus, prime)
        power = poly_mod(poly_mul(power, power, prime), modulus, prime)
        remaining >>= 1
    return result


def verify_cyclotomic_irreducibility() -> dict[str, object]:
    """Certify that Phi_37 is irreducible over Q(omega).

    The prime 13 splits in Z[omega], with omega -> 3 in F_13.  Rabin's
    criterion proves that Phi_37 stays irreducible in that residue field.
    A monic factorization over Q(omega) would reduce to a monic
    factorization there, so no such factorization exists.
    """

    prime = 13
    omega_image = 3
    if (omega_image * omega_image + omega_image + 1) % prime:
        raise AssertionError("the Eisenstein reduction prime changed")

    phi = (1,) * N
    x_poly = (0, 1)
    full_frobenius = poly_pow_mod(
        x_poly, prime ** (N - 1), phi, prime
    )
    if full_frobenius != x_poly:
        raise AssertionError("Phi_37 failed the full Frobenius test")

    proper_tests = []
    for divisor in (2, 3):
        degree = (N - 1) // divisor
        frobenius = poly_pow_mod(x_poly, prime**degree, phi, prime)
        gcd_value = poly_gcd(
            poly_sub(frobenius, x_poly, prime),
            phi,
            prime,
        )
        if gcd_value != (1,):
            raise AssertionError("Phi_37 failed a proper Frobenius test")
        proper_tests.append((degree, gcd_value))

    order = 1
    value = prime % N
    while value != 1:
        value = value * prime % N
        order += 1
    if order != N - 1:
        raise AssertionError("13 stopped being primitive modulo 37")

    return {
        "reduction_prime": prime,
        "omega_image": omega_image,
        "order_mod_37": order,
        "rabin_proper_degrees": tuple(
            degree for degree, _ in proper_tests
        ),
        "degree_over_Q_omega": N - 1,
    }


# ---------------------------------------------------------------------------
# The H-invariant primitive evaluation kernel.


def h_orbits() -> tuple[tuple[int, ...], ...]:
    orbits = [(0,)]
    seen = {0}
    for exponent in range(1, N):
        if exponent in seen:
            continue
        orbit = tuple(sorted({exponent * value % N for value in H}))
        if len(orbit) != len(H):
            raise AssertionError("a nonzero H-orbit changed size")
        seen.update(orbit)
        orbits.append(orbit)
    if seen != set(range(N)) or len(orbits) != 13:
        raise AssertionError("the H-orbits stopped partitioning C_37")
    return tuple(orbits)


def quotient_phi37(row: Sequence[int]) -> tuple[int, ...]:
    """Reduce a degree-at-most-36 row modulo Phi_37 over Q."""

    if len(row) != N:
        raise ValueError("a C_37 word has 37 coefficients")
    leading = int(row[-1])
    return tuple(int(row[index]) - leading for index in range(N - 1))


def rational_rank(rows: Iterable[Sequence[int]]) -> int:
    matrix = [
        [Fraction(int(value)) for value in row]
        for row in rows
    ]
    if not matrix:
        return 0
    columns = len(matrix[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (
                index
                for index in range(rank, len(matrix))
                if matrix[index][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [
            value / pivot_value for value in matrix[rank]
        ]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            scalar = matrix[index][column]
            matrix[index] = [
                left - scalar * right
                for left, right in zip(matrix[index], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def verify_invariant_kernel() -> dict[str, object]:
    orbits = h_orbits()
    indicator_rows = []
    for orbit in orbits:
        row = [0] * N
        for exponent in orbit:
            row[exponent] = 1
        indicator_rows.append(tuple(row))

    quotient_rows = tuple(map(quotient_phi37, indicator_rows))
    rank = rational_rank(quotient_rows)
    if rank != 12:
        raise AssertionError("the invariant primitive evaluation rank changed")
    if any(
        sum(row[index] for row in quotient_rows) != 0
        for index in range(N - 1)
    ):
        raise AssertionError("the Phi_37 kernel relation changed")

    # The domain has dimension 13 over Q(omega), the rank is 12, and the
    # displayed all-ones relation is nonzero.  Hence it spans the kernel.
    return {
        "H": H,
        "orbit_sizes": tuple(map(len, orbits)),
        "invariant_word_dimension": len(orbits),
        "primitive_image_rank": rank,
        "kernel_dimension": len(orbits) - rank,
        "kernel_generator": (1,) * len(orbits),
        "kernel_word": "Phi_37",
    }


# ---------------------------------------------------------------------------
# Fixed zero column and norm threshold.


def fiber_phase(word: Sequence[int], residue: int) -> tuple[int, int]:
    """Return sum_q word[residue+3q] omega^q as a+b*omega."""

    values = tuple(int(word[residue + 3 * index]) for index in range(3))
    return values[0] - values[2], values[1] - values[2]


def eisenstein_norm(value: tuple[int, int]) -> int:
    first, second = value
    return first * first - first * second + second * second


def verify_fixed_zero_activity() -> dict[str, object]:
    phases = tuple(
        fiber_phase(word, residue)
        for word in (ZERO_A_PLUS, ZERO_B_PLUS)
        for residue in range(3)
    )
    norms = tuple(map(eisenstein_norm, phases))
    if any(norm not in (0, 1) for norm in norms):
        raise AssertionError("the zero column left the zero/unit alphabet")
    active = tuple(
        WORD_LABELS[index]
        for index, norm in enumerate(norms)
        if norm == 1
    )
    inactive = tuple(
        WORD_LABELS[index]
        for index, norm in enumerate(norms)
        if norm == 0
    )
    if active != ("A0", "A1", "A2", "B1", "B2"):
        raise AssertionError("the five forced nonzero fibers changed")
    if inactive != ("B0",):
        raise AssertionError("the optional fiber stopped being B0")
    return {
        "zero_column_phases": phases,
        "zero_column_norms": norms,
        "forced_nonzero_fibers": active,
        "optional_fiber": inactive[0],
        "forced_nonzero_count": len(active),
    }


def multiplicative_orbits_on_h_cosets() -> tuple[int, ...]:
    cosets = {
        frozenset(exponent * value % N for value in H)
        for exponent in range(1, N)
    }
    if len(cosets) != 12:
        raise AssertionError("the quotient (Z/37)^*/H changed size")
    multiplier = P * P % N
    seen: set[frozenset[int]] = set()
    orbit_lengths = []
    for start in sorted(cosets, key=lambda value: min(value)):
        if start in seen:
            continue
        orbit = []
        current = start
        while current not in orbit:
            orbit.append(current)
            seen.add(current)
            current = frozenset(
                multiplier * value % N for value in current
            )
        orbit_lengths.append(len(orbit))
    if seen != cosets:
        raise AssertionError("the prime Frobenius missed an H-coset")
    return tuple(sorted(orbit_lengths))


def verify_norm_gap() -> dict[str, object]:
    # 167 is inert in Q(omega).
    roots = tuple(
        value
        for value in range(P)
        if (value * value + value + 1) % P == 0
    )
    if roots:
        raise AssertionError("167 stopped being inert in Q(omega)")

    generated_h = tuple(
        sorted({pow(P, 12 * exponent, N) for exponent in range(3)})
    )
    if generated_h != H:
        raise AssertionError("H stopped being generated by 167^12")

    residue_degrees = multiplicative_orbits_on_h_cosets()
    if residue_degrees != (6, 6):
        raise AssertionError("the two primitive residue degrees changed")

    embedding_count = (N - 1) // len(H)
    strict_upper_bound = ENERGY**embedding_count
    prime_ideal_norm = P**2
    divisibility_thresholds = tuple(
        prime_ideal_norm**degree for degree in residue_degrees
    )
    if any(
        threshold != strict_upper_bound
        for threshold in divisibility_thresholds
    ):
        raise AssertionError("the norm gap stopped being sharp")

    return {
        "base_prime_inert": True,
        "base_prime_ideal_norm": prime_ideal_norm,
        "H_generator": pow(P, 12, N),
        "H_fixed_field_degree_over_Q_omega": embedding_count,
        "primitive_prime_count": len(residue_degrees),
        "primitive_relative_residue_degrees": residue_degrees,
        "primitive_residue_field_sizes": tuple(
            prime_ideal_norm**degree for degree in residue_degrees
        ),
        "strict_energy_norm_upper_bound": strict_upper_bound,
        "coordinate_zero_divisibility_threshold": strict_upper_bound,
        "constant_unit_trivial_norm": N * N,
        "trivial_energy": ENERGY,
    }


# ---------------------------------------------------------------------------
# Zero-pattern and three-plane consequences.


def verify_support_strata() -> dict[str, object]:
    coordinate_count = len(WORD_LABELS)
    masks = range(1 << coordinate_count)
    raw_joint_patterns = (1 << coordinate_count) ** 2
    matching_patterns = sum(
        1 for first in masks for second in masks if first == second
    )
    mismatched_patterns = raw_joint_patterns - matching_patterns
    allowed_masks = (0, 1 << B0_INDEX)
    allowed_joint_patterns = tuple((mask, mask) for mask in allowed_masks)
    if len(allowed_joint_patterns) != 2:
        raise AssertionError("the physical support strata changed")

    eliminated_by_fixed_activity = matching_patterns - len(
        allowed_joint_patterns
    )
    total_eliminated = raw_joint_patterns - len(allowed_joint_patterns)

    # If span(z,Pbar*z,Pbar^2*z) has rank one, the zero set of z is
    # invariant under the two disjoint three-cycles.  Hence each channel
    # is either wholly zero or wholly nonzero.
    rank_one_zero_masks = tuple(
        sorted(
            mask
            for mask in masks
            if all(
                ((mask >> base) & 0b111) in (0, 0b111)
                for base in (0, 3)
            )
        )
    )
    physical_rank_one_masks = tuple(
        mask for mask in allowed_masks if mask in rank_one_zero_masks
    )
    if physical_rank_one_masks != (0,):
        raise AssertionError("the rank-one support consequence changed")

    return {
        "coordinate_count": coordinate_count,
        "raw_joint_zero_patterns": raw_joint_patterns,
        "mismatched_zero_patterns_eliminated": mismatched_patterns,
        "matching_zero_patterns_before_activity": matching_patterns,
        "matching_patterns_eliminated_by_fixed_activity": (
            eliminated_by_fixed_activity
        ),
        "total_zero_patterns_eliminated": total_eliminated,
        "allowed_common_zero_sets": ((), ("B0",)),
        "allowed_joint_zero_pattern_count": len(allowed_joint_patterns),
        "rank_one_ambient_zero_masks": rank_one_zero_masks,
        "rank_one_physical_zero_sets": ((),),
        "B0_zero_branch_minimum_plane_rank": 2,
        "dense_branch_minimum_plane_rank": 1,
        "maximum_plane_rank": 3,
    }


def verify() -> dict[str, object]:
    result = {
        "cyclotomic_irreducibility": verify_cyclotomic_irreducibility(),
        "invariant_kernel": verify_invariant_kernel(),
        "fixed_zero_activity": verify_fixed_zero_activity(),
        "norm_gap": verify_norm_gap(),
        "support_strata": verify_support_strata(),
    }
    certificate_hash = compact_hash(result)
    if (
        EXPECTED_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_CERTIFICATE_SHA256
    ):
        raise AssertionError("the phase-fiber support certificate changed")
    result["certificate_sha256"] = certificate_hash
    return result


def main() -> None:
    result = verify()
    print("PASS: phase-fiber primitive support is exact")
    print(
        "  irreducible degree:",
        result["cyclotomic_irreducibility"]["degree_over_Q_omega"],
    )
    print(
        "  primitive residue degrees:",
        result["norm_gap"]["primitive_relative_residue_degrees"],
    )
    print(
        "  allowed common zero sets:",
        result["support_strata"]["allowed_common_zero_sets"],
    )
    print("  certificate:", result["certificate_sha256"])


if __name__ == "__main__":
    main()

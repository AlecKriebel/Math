#!/usr/bin/env python3
"""Verify the local-global CRT closure of the LP(333) profile zero gate.

For an energy-167 pair of Eisenstein sequences, every nonzero periodic
correlation ``D_t`` has Eisenstein norm at most ``167**2`` by Cauchy.
The primitive-nine profile ideal says

    D_t in 3(1-omega) Z[omega],

while the complete characteristic-37 logarithmic transfer says

    D_t in 37 Z[omega].

The two ideals are coprime.  Their intersection has least nonzero norm

    Norm(37 * 3(1-omega)) = 37**2 * 27 = 36,963,

strictly larger than ``167**2 = 27,889``.  Therefore the two modular
conditions together force ``D_t=0`` exactly.

This verifier checks the ideal arithmetic, the sharp lambda-adic threshold,
the invertible characteristic-37 transfer, the exact energy/Cauchy bounds,
and the theorem on the 22 pinned primitive-nine-ideal profile tuples.  It
uses exact integer arithmetic and the Python standard library only.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from typing import Sequence

from verify_lp333_order3_char37_transfer import (
    CLASSES,
    TRANSFER_MATRIX,
    class_coefficients,
    class_log_transfer,
    direct_log_transfer,
    matrix_rank_and_determinant,
    norm_transfer,
    scalar_matrix_vector,
)
from verify_lp333_order3_profile9 import (
    profile_column_values,
    profile_correlation_table,
)
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES


Eisenstein = tuple[int, int]  # a+b*omega, omega^2+omega+1=0.

P = 37
TARGET_ENERGY = 167
LAMBDA = (1, -1)
THREE_LAMBDA = (3, -3)
CRT_KERNEL_GENERATOR = (111, -111)
CAUCHY_NORM_BOUND = TARGET_ENERGY**2
CRT_KERNEL_MINIMUM_NORM = P**2 * 27

EXPECTED_CORPUS_SHA256 = (
    "1b991b731a934c0c4361a93a1570c15fba69118fe1e15492ef5119385dcb7866"
)


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def e_norm(value: Eisenstein) -> int:
    return value[0] * value[0] - value[0] * value[1] + value[1] * value[1]


def e_power(value: Eisenstein, exponent: int) -> Eisenstein:
    if exponent < 0:
        raise ValueError("the exponent must be nonnegative")
    result = (1, 0)
    for _ in range(exponent):
        result = e_multiply(result, value)
    return result


def e_scale(factor: int, value: Eisenstein) -> Eisenstein:
    return factor * value[0], factor * value[1]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def lies_in_lambda_cube(value: Eisenstein) -> bool:
    """Test membership in ``3(1-omega) Z[omega]``.

    Since ``3(1-omega)`` is associated to ``(1-omega)^3``, this is the
    three-digit Eisenstein-prime condition used by the profile ideal.
    """

    first, second = value
    return (
        first % 3 == 0
        and second % 3 == 0
        and (first // 3 + second // 3) % 3 == 0
    )


def lies_in_37(value: Eisenstein) -> bool:
    return value[0] % P == 0 and value[1] % P == 0


def crt_kernel_quotient(value: Eisenstein) -> Eisenstein | None:
    """Divide by ``37*3(1-omega)`` when both modular tests pass."""

    if not lies_in_lambda_cube(value) or not lies_in_37(value):
        return None
    reduced = value[0] // P, value[1] // P
    # If reduced=3(1-omega)(x+y*omega), then
    #   reduced=(3(x+y), 3(2y-x)).
    numerator_x = 2 * reduced[0] - reduced[1]
    numerator_y = reduced[0] + reduced[1]
    if numerator_x % 9 or numerator_y % 9:
        raise AssertionError("coprime ideal intersection division failed")
    quotient = numerator_x // 9, numerator_y // 9
    if e_multiply(CRT_KERNEL_GENERATOR, quotient) != value:
        raise AssertionError("CRT kernel quotient does not reconstruct")
    return quotient


def exact_profile_residuals(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> tuple[Eisenstein, ...]:
    """Return all 37 exact coefficients of ``AA*+BB*-167e``."""

    sequences = (
        profile_column_values(0, identifiers_a),
        profile_column_values(1, identifiers_b),
    )
    result = []
    for lag in range(P):
        total = (0, 0)
        for sequence in sequences:
            for column in range(P):
                total = e_add(
                    total,
                    e_multiply(
                        sequence[(column + lag) % P],
                        e_conjugate(sequence[column]),
                    ),
                )
        if lag == 0:
            total = total[0] - TARGET_ENERGY, total[1]
        result.append(total)
    return tuple(result)


def profile_energy(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> int:
    sequences = (
        profile_column_values(0, identifiers_a),
        profile_column_values(1, identifiers_b),
    )
    return sum(e_norm(value) for sequence in sequences for value in sequence)


def invariant_parts(residuals: Sequence[Eisenstein]) -> tuple[Eisenstein, ...]:
    if len(residuals) != P:
        raise ValueError("expected a length-37 correlation word")
    parts = [tuple((0,))]
    parts.extend(CLASSES)
    result = []
    for part in parts:
        value = residuals[part[0]]
        if any(residuals[index] != value for index in part):
            raise AssertionError("the residual word is not H-invariant")
        result.append(value)
    return tuple(result)


def characteristic37_residual_transfer(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> tuple[Eisenstein, ...]:
    """Return the thirteen transfer residuals modulo 37."""

    a_transfer = class_log_transfer(
        (-1, 0), class_coefficients(0, identifiers_a)
    )
    b_transfer = class_log_transfer(
        (2, 0), class_coefficients(1, identifiers_b)
    )
    combined = list(norm_transfer(a_transfer, b_transfer))
    combined[0] = (
        (combined[0][0] - TARGET_ENERGY) % P,
        combined[0][1] % P,
    )
    return tuple(combined)


def verify_characteristic37_equivalence(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
    residuals: Sequence[Eisenstein] | None = None,
) -> dict[str, object]:
    """Check transfer-zero iff every invariant residual is zero modulo 37."""

    exact = (
        tuple(residuals)
        if residuals is not None
        else exact_profile_residuals(identifiers_a, identifiers_b)
    )
    parts = invariant_parts(exact)
    reduced_physical = tuple(
        (value[0] % P, value[1] % P) for value in exact
    )
    direct = direct_log_transfer(reduced_physical)
    short = characteristic37_residual_transfer(
        identifiers_a, identifiers_b
    )
    if direct != short:
        raise AssertionError("direct and short characteristic-37 transfers differ")

    # Independently apply the 13-by-13 scalar transfer to both Eisenstein
    # coordinates of the invariant coefficient word.
    coordinate_transfer = tuple(
        zip(
            scalar_matrix_vector(
                TRANSFER_MATRIX, tuple(value[0] % P for value in parts)
            ),
            scalar_matrix_vector(
                TRANSFER_MATRIX, tuple(value[1] % P for value in parts)
            ),
        )
    )
    if coordinate_transfer != direct:
        raise AssertionError("the invariant transfer matrix orientation changed")

    physical_zero = all(
        value[0] % P == 0 and value[1] % P == 0 for value in parts
    )
    transfer_zero = all(value == (0, 0) for value in short)
    if physical_zero != transfer_zero:
        raise AssertionError("invertible transfer lost the zero predicate")
    return {
        "physical_zero_mod_37": physical_zero,
        "transfer_zero_mod_37": transfer_zero,
        "nonzero_transfer_coefficients": sum(
            value != (0, 0) for value in short
        ),
        "transfer": short,
    }


def verify_characteristic37_basis_orientation() -> dict[str, object]:
    """Check both Eisenstein coordinates on all 13 invariant basis words."""

    checks = 0
    for part_index in range(13):
        for coordinate in ((1, 0), (0, 1)):
            parts = [(0, 0)] * 13
            parts[part_index] = coordinate
            physical = [(0, 0)] * P
            physical[0] = parts[0]
            for class_index, part in enumerate(CLASSES):
                for column in part:
                    physical[column] = parts[class_index + 1]

            direct = direct_log_transfer(tuple(physical))
            expected = tuple(
                zip(
                    scalar_matrix_vector(
                        TRANSFER_MATRIX,
                        tuple(value[0] for value in parts),
                    ),
                    scalar_matrix_vector(
                        TRANSFER_MATRIX,
                        tuple(value[1] for value in parts),
                    ),
                )
            )
            if direct != expected:
                raise AssertionError(
                    "the characteristic-37 basis orientation changed"
                )
            checks += 1
    return {
        "invariant_basis_words": 13,
        "eisenstein_coordinates": 2,
        "basis_orientation_checks": checks,
    }


def verify_ideal_arithmetic() -> dict[str, object]:
    """Replay the CRT threshold and its minimal lambda-power statement."""

    lambda_norms = tuple(e_norm(e_power(LAMBDA, exponent)) for exponent in range(5))
    if lambda_norms != (1, 3, 9, 27, 81):
        raise AssertionError("the Eisenstein-prime norms changed")
    if e_norm(THREE_LAMBDA) != 27:
        raise AssertionError("3(1-omega) must have norm 27")
    if e_norm(CRT_KERNEL_GENERATOR) != CRT_KERNEL_MINIMUM_NORM:
        raise AssertionError("the CRT kernel norm changed")
    if not (
        P**2 * lambda_norms[2]
        <= CAUCHY_NORM_BOUND
        < P**2 * lambda_norms[3]
    ):
        raise AssertionError("lambda cubed is no longer the first sufficient power")

    # Check the explicit ideal-intersection quotient on a deterministic box.
    quotient_checks = 0
    for first in range(-5, 6):
        for second in range(-5, 6):
            quotient = (first, second)
            value = e_multiply(CRT_KERNEL_GENERATOR, quotient)
            if crt_kernel_quotient(value) != quotient:
                raise AssertionError("CRT quotient failed on a lattice fixture")
            quotient_checks += 1

    # Directly exhaust a coordinate box containing the Cauchy disk.  From
    # a^2-a*b+b^2 <= E^2 one gets |a|,|b| <= 2E/sqrt(3); the integer radius
    # 2E is a deliberately loose standard-library-only enclosure.
    # The theorem itself uses the norm inequality, not this enumeration.
    disk_points = 0
    kernel_points = []
    coordinate_radius = 2 * TARGET_ENERGY
    for first in range(-coordinate_radius, coordinate_radius + 1):
        for second in range(-coordinate_radius, coordinate_radius + 1):
            value = (first, second)
            if e_norm(value) > CAUCHY_NORM_BOUND:
                continue
            disk_points += 1
            if lies_in_lambda_cube(value) and lies_in_37(value):
                kernel_points.append(value)
    if kernel_points != [(0, 0)]:
        raise AssertionError("a nonzero CRT-kernel point entered the Cauchy disk")

    return {
        "lambda_power_norms_0_through_4": lambda_norms,
        "first_sufficient_lambda_power": 3,
        "lambda_squared_kernel_minimum_norm": P**2 * lambda_norms[2],
        "lambda_cubed_kernel_minimum_norm": P**2 * lambda_norms[3],
        "cauchy_norm_bound": CAUCHY_NORM_BOUND,
        "strict_norm_gap": CRT_KERNEL_MINIMUM_NORM - CAUCHY_NORM_BOUND,
        "quotient_checks": quotient_checks,
        "cauchy_disk_coordinate_radius": coordinate_radius,
        "cauchy_disk_lattice_points": disk_points,
        "kernel_points_in_cauchy_disk": tuple(kernel_points),
    }


def audit_profile_tuple(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, object]:
    residuals = exact_profile_residuals(identifiers_a, identifiers_b)
    parts = invariant_parts(residuals)
    table = profile_correlation_table(identifiers_a, identifiers_b)
    if parts != table:
        raise AssertionError("physical and profile correlation tables differ")

    energy = profile_energy(identifiers_a, identifiers_b)
    if residuals[0] != (energy - TARGET_ENERGY, 0):
        raise AssertionError("the origin residual is not energy minus 167")
    cauchy_checks = 0
    for residual in residuals[1:]:
        if e_norm(residual) > energy**2:
            raise AssertionError("an exact correlation violates Cauchy")
        cauchy_checks += 1

    ideal_pass = all(lies_in_lambda_cube(value) for value in parts[1:])
    transfer = verify_characteristic37_equivalence(
        identifiers_a, identifiers_b, residuals
    )
    modular_pass = (
        energy == TARGET_ENERGY
        and ideal_pass
        and bool(transfer["transfer_zero_mod_37"])
    )
    exact_pass = all(value == (0, 0) for value in residuals)
    if modular_pass != exact_pass:
        raise AssertionError("the local-global zero predicate failed")
    return {
        "energy": energy,
        "origin_zero": residuals[0] == (0, 0),
        "cauchy_checks": cauchy_checks,
        "maximum_nonzero_residual_norm": max(
            e_norm(value) for value in residuals[1:]
        ),
        "lambda_cube_ideal_pass": ideal_pass,
        "characteristic37_transfer_pass": transfer[
            "transfer_zero_mod_37"
        ],
        "nonzero_transfer_coefficients": transfer[
            "nonzero_transfer_coefficients"
        ],
        "exact_zero_pass": exact_pass,
        "local_global_pass": modular_pass,
        "part_table": parts,
        "transfer": transfer["transfer"],
    }


def verify_profile_corpus() -> dict[str, object]:
    rank, determinant = matrix_rank_and_determinant(TRANSFER_MATRIX)
    if rank != 13 or determinant == 0:
        raise AssertionError("the characteristic-37 transfer is not invertible")

    certificate = []
    transfer_failure_histogram: Counter[int] = Counter()
    maximum_residual_norm = 0
    for index, (target, identifiers_a, identifiers_b) in enumerate(
        PROFILE9_SHARD_WITNESSES
    ):
        audit = audit_profile_tuple(identifiers_a, identifiers_b)
        if audit["energy"] != TARGET_ENERGY or not audit["origin_zero"]:
            raise AssertionError("a profile witness lost its energy equation")
        if not audit["lambda_cube_ideal_pass"]:
            raise AssertionError("an ideal-compatible witness lost lambda cubed")
        if audit["characteristic37_transfer_pass"]:
            raise AssertionError("a fixed witness unexpectedly passes mod 37")
        if audit["exact_zero_pass"]:
            raise AssertionError("a fixed witness unexpectedly passes exact zero")
        bad = int(audit["nonzero_transfer_coefficients"])
        transfer_failure_histogram[bad] += 1
        maximum_residual_norm = max(
            maximum_residual_norm,
            int(audit["maximum_nonzero_residual_norm"]),
        )
        certificate.append(
            (
                index,
                target,
                identifiers_a,
                identifiers_b,
                audit["part_table"],
                audit["transfer"],
            )
        )

    certificate_hash = compact_hash(tuple(certificate))
    if EXPECTED_CORPUS_SHA256 and certificate_hash != EXPECTED_CORPUS_SHA256:
        raise AssertionError("the local-global profile corpus changed")
    expected_histogram = ((7, 1), (8, 1), (10, 4), (11, 16))
    if tuple(sorted(transfer_failure_histogram.items())) != expected_histogram:
        raise AssertionError("the characteristic-37 failure histogram changed")
    if maximum_residual_norm != 2916:
        raise AssertionError("the fixed-corpus residual maximum changed")
    return {
        "transfer_rank": rank,
        "transfer_determinant_mod_37": determinant,
        "fixed_profile_tuples": len(certificate),
        "lambda_cube_survivors": len(certificate),
        "characteristic37_survivors": 0,
        "exact_zero_survivors": 0,
        "aggregate_shard_exclusions": 0,
        "transfer_failure_histogram": expected_histogram,
        "maximum_residual_norm": maximum_residual_norm,
        "cauchy_bound_checks": 36 * len(certificate),
        "certificate_sha256": certificate_hash,
    }


def verify() -> dict[str, object]:
    arithmetic = verify_ideal_arithmetic()
    basis = verify_characteristic37_basis_orientation()
    corpus = verify_profile_corpus()
    return {
        "ideal_arithmetic": arithmetic,
        "characteristic37_basis": basis,
        "profile_corpus": corpus,
        "theorem": (
            "for energy-167 H-invariant profile pairs, exact D_t=0 is "
            "equivalent to the lambda-cubed profile ideal plus the complete "
            "characteristic-37 transfer"
        ),
        "limitation": (
            "the pinned corpus excludes fixed profile tuples only; no "
            "aggregate shard is exhausted"
        ),
    }


def main() -> None:
    result = verify()
    arithmetic = result["ideal_arithmetic"]
    corpus = result["profile_corpus"]
    print(
        "first_sufficient_lambda_power="
        f"{arithmetic['first_sufficient_lambda_power']}"
    )
    print(f"cauchy_norm_bound={arithmetic['cauchy_norm_bound']}")
    print(
        "lambda_cubed_kernel_minimum_norm="
        f"{arithmetic['lambda_cubed_kernel_minimum_norm']}"
    )
    print(f"strict_norm_gap={arithmetic['strict_norm_gap']}")
    print(f"transfer_rank={corpus['transfer_rank']}")
    print(f"fixed_profile_tuples={corpus['fixed_profile_tuples']}")
    print(
        "transfer_failure_histogram="
        f"{corpus['transfer_failure_histogram']}"
    )
    print(f"certificate_sha256={corpus['certificate_sha256']}")
    print("PASS: local-global profile-zero CRT theorem replayed")
    print("STATUS: exact modular closure; no aggregate shard excluded")


if __name__ == "__main__":
    main()

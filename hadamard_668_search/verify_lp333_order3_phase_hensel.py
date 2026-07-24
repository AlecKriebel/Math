#!/usr/bin/env python3
"""Verify the first lambda-adic phase digit for order-three LP(333).

Put ``lambda=1-omega``.  Once a residue-profile tuple is fixed, every
nonzero three-fiber phase is

    sigma * omega ** L(u),

where ``sigma`` is a sign and ``L`` is affine in one placement trit over
F_3.  Thus a coefficient of either exact phase-factor equation is a signed
sum ``F=sum sigma*omega**L - target``.  If its fixed lambda-zero digit
vanishes, then

    F/lambda = -sum sigma*L                  (mod lambda).

This module constructs those affine equations exactly and replays their
rank on all 22 pinned profile-ideal shard witnesses.  No solver search is
performed.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Sequence

from verify_lp333_order3_char37_transfer import CLASS_OF, P, PROFILES
from verify_lp333_order3_labeled_jet import ZERO_A_PLUS, ZERO_B_PLUS
from verify_lp333_order3_phase_factor import (
    Eisenstein,
    fiber_phase,
    phase_columns,
    phase_equations,
)
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES
from verify_lp333_order3_quotient import PARTS
from verify_lp333_order3_trit_lift import (
    Profiles,
    active_trit_coordinates,
    normalized_mask_from_profile_trits,
)


MODULUS = 3
EXCLUDED_PINNED_TARGET = (-3, 0, 0, 3)

# The twenty displayed rows are ordered as
#   E0(origin,C0,...,C5), E1(origin,C0,...,C11).
# Twice E0(C0) plus twice E1(C6) is the normalized contradiction 0=1.
EXPECTED_EXCLUSION_MULTIPLIERS = (
    0, 2, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
)

EXPECTED_CENSUS_SHA256 = (
    "db2a578380db873b9c7db711d7638fcf3b01b4155592a1e1584e5a2d2634d205"
)
EXPECTED_SOLUTION_CORPUS_SHA256 = (
    "5805264e94cef3ff8ce50e24a57261f736ac8ef688bb2948e2233331fdeb985a"
)
EXPECTED_EXCLUSION_CERTIFICATE_SHA256 = (
    "4d89429afda3af26471cb07f71e155d9763c03d314acf4d6cea3b5f9687bf27b"
)


@dataclass(frozen=True)
class PhaseEntry:
    """A nonzero phase ``sign*omega^(constant+slope*u)``."""

    sign: int
    constant: int
    variable: int | None
    slope: int


@dataclass(frozen=True)
class PhaseTerm:
    """One signed affine power of omega."""

    sign: int
    constant: int
    coefficients: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class FirstDigitEquation:
    """An affine polynomial, constant first."""

    component: str
    class_index: int | None
    constant_at_lambda_zero: int
    affine: tuple[int, ...]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def lambda_digits(value: Eisenstein, count: int) -> tuple[int, ...]:
    """Return exact base-``lambda`` digits of ``a+b*omega`` in F_3."""

    if count < 0:
        raise ValueError("the digit count must be nonnegative")
    first, second = map(int, value)
    result = []
    for _ in range(count):
        digit = (first + second) % MODULUS
        result.append(digit)
        first -= digit
        numerator_first = 2 * first - second
        numerator_second = first + second
        if numerator_first % 3 or numerator_second % 3:
            raise AssertionError("exact lambda division failed")
        first = numerator_first // 3
        second = numerator_second // 3
    return tuple(result)


def profiles_from_ids(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> Profiles:
    identifiers = tuple(
        tuple(int(identifier) for identifier in channel)
        for channel in (identifiers_a, identifiers_b)
    )
    if any(len(channel) != 12 for channel in identifiers):
        raise ValueError("each channel must have twelve profile identifiers")
    if any(
        not 0 <= identifier < len(PROFILES)
        for channel in identifiers
        for identifier in channel
    ):
        raise ValueError("a profile identifier lies outside the catalog")
    return tuple(
        tuple(PROFILES[identifier] for identifier in channel)
        for channel in identifiers
    )  # type: ignore[return-value]


def root_representation(value: Eisenstein) -> tuple[int, int] | None:
    """Represent zero or a signed cube root as ``(sign, exponent)``."""

    catalog: dict[Eisenstein, tuple[int, int] | None] = {
        (0, 0): None,
        (1, 0): (1, 0),
        (0, 1): (1, 1),
        (-1, -1): (1, 2),
        (-1, 0): (-1, 0),
        (0, -1): (-1, 1),
        (1, 1): (-1, 2),
    }
    if value not in catalog:
        raise ValueError("the value is not zero or a signed cube root")
    return catalog[value]


ZERO_PHASES = tuple(
    tuple(root_representation(fiber_phase(word, residue)) for residue in range(3))
    for word in (ZERO_A_PLUS, ZERO_B_PLUS)
)


def phase_entries(
    profiles: Profiles,
) -> tuple[
    tuple[tuple[PhaseEntry | None, ...], ...],
    tuple[tuple[PhaseEntry | None, ...], ...],
]:
    """Construct the signed affine phase at every physical column/fiber."""

    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    result = []
    for channel in range(2):
        columns = []
        columns.append(
            tuple(
                None
                if representation is None
                else PhaseEntry(
                    representation[0], representation[1], None, 0
                )
                for representation in ZERO_PHASES[channel]
            )
        )
        for column in range(1, P):
            class_index = CLASS_OF[column]
            high_weight = (
                class_index % 2 == 0
                if channel == 0
                else class_index % 2 == 1
            )
            entries = []
            for residue, count in enumerate(
                profiles[channel][class_index]
            ):
                if count not in (1, 2):
                    entries.append(None)
                    continue
                # A normalized count-one fiber is omega^(-u), while a
                # count-two fiber is -omega^u.  Complementation negates it.
                sign = (1 if count == 1 else -1) * (
                    -1 if high_weight else 1
                )
                entries.append(
                    PhaseEntry(
                        sign=sign,
                        constant=0,
                        variable=coordinate_index[
                            (channel, class_index, residue)
                        ],
                        slope=(-1 if count == 1 else 1) % MODULUS,
                    )
                )
            columns.append(tuple(entries))
        result.append(tuple(columns))
    return tuple(result)  # type: ignore[return-value]


def multiply_phase_entries(
    left: PhaseEntry,
    right: PhaseEntry,
    extra_exponent: int,
) -> PhaseTerm:
    coefficients: dict[int, int] = {}
    if left.variable is not None:
        coefficients[left.variable] = left.slope
    if right.variable is not None:
        coefficients[right.variable] = (
            coefficients.get(right.variable, 0) - right.slope
        ) % MODULUS
    return PhaseTerm(
        sign=left.sign * right.sign,
        constant=(
            left.constant - right.constant + extra_exponent
        ) % MODULUS,
        coefficients=tuple(
            (variable, coefficient)
            for variable, coefficient in sorted(coefficients.items())
            if coefficient
        ),
    )


def coefficient_terms(
    entries: Sequence[Sequence[Sequence[PhaseEntry | None]]],
    component: str,
    lag: int,
) -> tuple[tuple[PhaseTerm, ...], int]:
    if component == "E0":
        residue_pairs = ((0, 0, 0), (1, 1, 0), (2, 2, 0))
    elif component == "E1":
        residue_pairs = ((1, 0, 0), (2, 1, 0), (0, 2, 2))
    else:
        raise ValueError("the component must be E0 or E1")
    terms = []
    for channel in range(2):
        for column in range(P):
            for left_residue, right_residue, extra in residue_pairs:
                left = entries[channel][
                    (column + lag) % P
                ][left_residue]
                right = entries[channel][column][right_residue]
                if left is not None and right is not None:
                    terms.append(
                        multiply_phase_entries(left, right, extra)
                    )
    target = 167 if component == "E0" and lag == 0 else 0
    return tuple(terms), target


def first_digit_equations(
    profiles: Profiles,
) -> tuple[FirstDigitEquation, ...]:
    """Return the twenty reversal-independent displayed equations."""

    variable_count = len(active_trit_coordinates(profiles))
    entries = phase_entries(profiles)
    specifications: list[tuple[str, int | None, int]] = [
        ("E0", None, PARTS[0][0])
    ]
    specifications.extend(
        ("E0", class_index, PARTS[class_index + 1][0])
        for class_index in range(6)
    )
    specifications.append(("E1", None, PARTS[0][0]))
    specifications.extend(
        ("E1", class_index, PARTS[class_index + 1][0])
        for class_index in range(12)
    )

    equations = []
    for component, class_index, lag in specifications:
        terms, target = coefficient_terms(entries, component, lag)
        constant_at_zero = sum(term.sign for term in terms) - target
        if constant_at_zero % 3:
            raise ValueError("the profile fails the lambda-zero digit")
        affine = [0] * (variable_count + 1)
        for term in terms:
            sign = term.sign % MODULUS
            affine[0] = (
                affine[0] - sign * term.constant
            ) % MODULUS
            for variable, coefficient in term.coefficients:
                affine[variable + 1] = (
                    affine[variable + 1] - sign * coefficient
                ) % MODULUS
        equations.append(
            FirstDigitEquation(
                component,
                class_index,
                constant_at_zero,
                tuple(affine),
            )
        )
    return tuple(equations)


def matrix_rref(
    rows: Sequence[Sequence[int]],
    track_transform: bool = False,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...] | None,
]:
    if not rows:
        return (), (), () if track_transform else None
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("the matrix is not rectangular")
    matrix = [[int(value) % MODULUS for value in row] for row in rows]
    transform = (
        [
            [int(row == column) for column in range(len(matrix))]
            for row in range(len(matrix))
        ]
        if track_transform
        else None
    )
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        if transform is not None:
            transform[pivot_row], transform[pivot] = (
                transform[pivot],
                transform[pivot_row],
            )
        inverse = pow(matrix[pivot_row][column], -1, MODULUS)
        matrix[pivot_row] = [
            value * inverse % MODULUS for value in matrix[pivot_row]
        ]
        if transform is not None:
            transform[pivot_row] = [
                value * inverse % MODULUS
                for value in transform[pivot_row]
            ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % MODULUS
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
            if transform is not None:
                transform[row] = [
                    (left - factor * right) % MODULUS
                    for left, right in zip(
                        transform[row], transform[pivot_row]
                    )
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return (
        tuple(tuple(row) for row in matrix),
        tuple(pivots),
        None
        if transform is None
        else tuple(tuple(row) for row in transform),
    )


def matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    return len(matrix_rref(rows)[1])


def augmented_system(
    equations: Sequence[FirstDigitEquation],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(equation.affine[1:])
        + ((-equation.affine[0]) % MODULUS,)
        for equation in equations
    )


def canonical_solution(
    rows: Sequence[Sequence[int]],
    variable_count: int,
) -> tuple[int, ...] | None:
    rref, pivots, _ = matrix_rref(rows)
    if any(
        not any(row[:variable_count]) and row[variable_count]
        for row in rref
    ):
        return None
    solution = [0] * variable_count
    pivot_row = 0
    for pivot in pivots:
        if pivot == variable_count:
            continue
        solution[pivot] = rref[pivot_row][variable_count]
        pivot_row += 1
    return tuple(solution)


def inconsistency_certificate(
    rows: Sequence[Sequence[int]],
    variable_count: int,
) -> tuple[int, ...] | None:
    rref, _, transform = matrix_rref(rows, track_transform=True)
    if transform is None:
        raise AssertionError("the row transform was not retained")
    for row, multipliers in zip(rref, transform):
        if (
            not any(row[:variable_count])
            and row[variable_count] == 1
        ):
            combined = tuple(
                sum(
                    multipliers[source] * rows[source][column]
                    for source in range(len(rows))
                )
                % MODULUS
                for column in range(variable_count + 1)
            )
            if combined != (0,) * variable_count + (1,):
                raise AssertionError("the inconsistency certificate failed")
            return multipliers
    return None


def masks_from_trits(
    profiles: Profiles,
    trits: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    coordinates = active_trit_coordinates(profiles)
    if len(trits) != len(coordinates):
        raise ValueError("the trit vector has the wrong length")
    values = {
        coordinate: int(trits[index]) % MODULUS
        for index, coordinate in enumerate(coordinates)
    }
    result = []
    for channel in range(2):
        masks = []
        for class_index, profile in enumerate(profiles[channel]):
            local = tuple(
                values[(channel, class_index, residue)]
                for residue, count in enumerate(profile)
                if count in (1, 2)
            )
            masks.append(normalized_mask_from_profile_trits(profile, local))
        result.append(tuple(masks))
    return tuple(result)  # type: ignore[return-value]


def direct_first_digits(
    profiles: Profiles,
    trits: Sequence[int],
) -> tuple[int, ...]:
    masks_a, masks_b = masks_from_trits(profiles, trits)
    equations = phase_equations(phase_columns(masks_a, masks_b))
    values = [equations[PARTS[0][0]][0]]
    values.extend(
        equations[PARTS[class_index + 1][0]][0]
        for class_index in range(6)
    )
    values.append(equations[PARTS[0][0]][1])
    values.extend(
        equations[PARTS[class_index + 1][0]][1]
        for class_index in range(12)
    )
    return tuple(lambda_digits(value, 2)[1] for value in values)


def symbolic_first_digits(
    equations: Sequence[FirstDigitEquation],
    trits: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        (
            equation.affine[0]
            + sum(
                coefficient * int(trits[index])
                for index, coefficient in enumerate(equation.affine[1:])
            )
        )
        % MODULUS
        for equation in equations
    )


def audit_profile_witness(
    target: Sequence[int],
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
    witness_index: int,
) -> dict[str, object]:
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    coordinates = active_trit_coordinates(profiles)
    if len(coordinates) != 54:
        raise AssertionError("the active placement-trit count changed")
    equations = first_digit_equations(profiles)
    if len(equations) != 20:
        raise AssertionError("the displayed equation count changed")
    rows = augmented_system(equations)
    coefficient_rank = matrix_rank(tuple(row[:-1] for row in rows))
    augmented_rank = matrix_rank(rows)
    solution = canonical_solution(rows, len(coordinates))
    certificate = inconsistency_certificate(rows, len(coordinates))
    consistent = coefficient_rank == augmented_rank
    if consistent != (solution is not None and certificate is None):
        raise AssertionError("the consistency audits disagree")

    fixture = tuple(
        (index * index + 2 * witness_index + 1) % 3
        for index in range(len(coordinates))
    )
    if symbolic_first_digits(equations, fixture) != direct_first_digits(
        profiles, fixture
    ):
        raise AssertionError("symbolic and direct first digits disagree")
    if solution is not None:
        if symbolic_first_digits(equations, solution) != (0,) * 20:
            raise AssertionError("the canonical affine solution failed")
        if direct_first_digits(profiles, solution) != (0,) * 20:
            raise AssertionError("the direct canonical solution failed")

    return {
        "witness_index": witness_index,
        "target": tuple(int(value) for value in target),
        "placement_trits": len(coordinates),
        "displayed_equations": len(equations),
        "identically_zero_rows": sum(
            not any(equation.affine) for equation in equations
        ),
        "coefficient_rank": coefficient_rank,
        "augmented_rank": augmented_rank,
        "consistent": consistent,
        "nullity": (
            len(coordinates) - coefficient_rank if consistent else None
        ),
        "canonical_solution": solution,
        "inconsistency_certificate": certificate,
    }


def verify_local_phase_expansion() -> dict[str, object]:
    """Exhaust ``omega^L = 1-L lambda mod lambda^2``."""

    roots = ((1, 0), (0, 1), (-1, -1))
    checks = 0
    for constant in range(3):
        for left_slope in range(3):
            for right_slope in range(3):
                for left in range(3):
                    for right in range(3):
                        exponent = (
                            constant
                            + left_slope * left
                            + right_slope * right
                        ) % 3
                        digits = lambda_digits(roots[exponent], 2)
                        if digits != (1, (-exponent) % 3):
                            raise AssertionError(
                                "the local lambda expansion failed"
                            )
                        checks += 1
    return {
        "affine_exponents_checked": checks,
        "lambda_modulus_power": 2,
        "first_placement_digit_degree": 1,
    }


def verify() -> dict[str, object]:
    local = verify_local_phase_expansion()
    audits = tuple(
        audit_profile_witness(target, identifiers_a, identifiers_b, index)
        for index, (target, identifiers_a, identifiers_b) in enumerate(
            PROFILE9_SHARD_WITNESSES
        )
    )
    excluded_witnesses = tuple(
        (audit["witness_index"], audit["target"])
        for audit in audits
        if not audit["consistent"]
    )
    if excluded_witnesses != ((3, EXCLUDED_PINNED_TARGET),):
        raise AssertionError("the first-digit exclusion census changed")
    exceptional = next(
        audit for audit in audits if not audit["consistent"]
    )
    if (
        exceptional["coefficient_rank"],
        exceptional["augmented_rank"],
    ) != (16, 17):
        raise AssertionError("the exceptional rank pair changed")
    if (
        exceptional["inconsistency_certificate"]
        != EXPECTED_EXCLUSION_MULTIPLIERS
    ):
        raise AssertionError("the explicit contradiction changed")

    survivor_rank_pairs = {
        (audit["coefficient_rank"], audit["augmented_rank"])
        for audit in audits
        if audit["consistent"]
    }
    if survivor_rank_pairs != {(18, 18)}:
        raise AssertionError("a surviving first-digit rank changed")
    if any(
        audit["nullity"] != 36
        for audit in audits
        if audit["consistent"]
    ):
        raise AssertionError("a surviving first-digit nullity changed")
    identically_zero_rows = {
        int(audit["identically_zero_rows"]) for audit in audits
    }
    if identically_zero_rows != {2}:
        raise AssertionError("the identically-zero row count changed")

    census = tuple(
        (
            audit["target"],
            audit["coefficient_rank"],
            audit["augmented_rank"],
            audit["nullity"],
        )
        for audit in audits
    )
    solutions = tuple(
        (audit["target"], audit["canonical_solution"])
        for audit in audits
        if audit["consistent"]
    )
    exclusion_certificate = (
        exceptional["target"],
        exceptional["coefficient_rank"],
        exceptional["augmented_rank"],
        exceptional["inconsistency_certificate"],
    )
    census_hash = compact_hash(census)
    solution_hash = compact_hash(solutions)
    exclusion_hash = compact_hash(exclusion_certificate)
    if EXPECTED_CENSUS_SHA256 and census_hash != EXPECTED_CENSUS_SHA256:
        raise AssertionError("the first-digit census changed")
    if (
        EXPECTED_SOLUTION_CORPUS_SHA256
        and solution_hash != EXPECTED_SOLUTION_CORPUS_SHA256
    ):
        raise AssertionError("the canonical solution corpus changed")
    if (
        EXPECTED_EXCLUSION_CERTIFICATE_SHA256
        and exclusion_hash != EXPECTED_EXCLUSION_CERTIFICATE_SHA256
    ):
        raise AssertionError("the exclusion certificate changed")

    return {
        "local_expansion": local,
        "profile_witnesses": len(audits),
        "placement_trits_per_witness": 54,
        "displayed_first_digit_equations": 20,
        "identically_zero_rows_per_witness": identically_zero_rows.pop(),
        "generic_rank": 18,
        "generic_nullity": 36,
        "first_digit_survivors": sum(
            bool(audit["consistent"]) for audit in audits
        ),
        "excluded_fixed_profile_witnesses": excluded_witnesses,
        "excluded_aggregate_shards": 0,
        "exceptional_rank_pair": (
            exceptional["coefficient_rank"],
            exceptional["augmented_rank"],
        ),
        "census_sha256": census_hash,
        "solution_corpus_sha256": solution_hash,
        "exclusion_certificate_sha256": exclusion_hash,
        "audits": audits,
    }


def main() -> None:
    result = verify()
    print(f"profile_witnesses={result['profile_witnesses']}")
    print(
        "displayed_first_digit_equations="
        f"{result['displayed_first_digit_equations']}"
    )
    print(f"first_digit_survivors={result['first_digit_survivors']}")
    print(
        "excluded_fixed_profile_witnesses="
        f"{result['excluded_fixed_profile_witnesses']}"
    )
    print(
        "exceptional_rank_pair="
        f"{result['exceptional_rank_pair']}"
    )
    print(f"census_sha256={result['census_sha256']}")
    print(
        "solution_corpus_sha256="
        f"{result['solution_corpus_sha256']}"
    )
    print(
        "exclusion_certificate_sha256="
        f"{result['exclusion_certificate_sha256']}"
    )
    print("PASS: exact first lambda-adic phase digit reconstructed")
    print("STATUS: one pinned profile tuple excluded; no shard excluded")


if __name__ == "__main__":
    main()

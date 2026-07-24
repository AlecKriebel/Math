#!/usr/bin/env python3
"""Audit a compact carry model for the third and fourth lambda digits.

This is scratch research code.  It derives the two integer statistics

    A = C - sum_t sigma_t L_t,
    Q = C/3 - sum_t sigma_t 1[L_t=2],

for every displayed phase row after composition with the 36-dimensional
first-digit affine space.  Here L_t is the canonical representative in
{0,1,2} of an affine F_3 form.  The exact Eisenstein coefficient is

    F = A + (3 Q - A) omega.

Consequently:

    digits 0..2 vanish  <=> A == 0 (mod 3), Q == 0 (mod 3);
    digits 0..3 vanish  <=> A == 0 (mod 9), Q == 0 (mod 3);
    digits 0..4 vanish  <=> A == 0 (mod 9), Q == 0 (mod 9);
    F is exactly zero   <=> A == Q == 0.

The script independently replays these identities against exact
Eisenstein arithmetic, derives the digit-3 carry as a cubic function over
F_3, and audits its Jacobian together with the known quadratic digit.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HIGHER_DIGITS))
sys.path.insert(0, str(SEARCH_ROOT))

import solve_lambda_prefix_sat as prefix  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402


WITNESS = HIGHER_DIGITS / "full_second_digit_witness.json"
SECOND_DIGIT_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))
THIRD_DIGIT_ROWS = tuple(range(1, 20))


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def effective_rows(candidate_index: int):
    """Compose every signed phase term with the first-digit affine space."""

    candidate = second.CANDIDATES[candidate_index]
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(equations, 54)
    rows = []
    for terms, constant_at_zero in second.second_digit_term_data(profiles):
        grouped: dict[tuple[int, tuple[int, ...]], int] = defaultdict(int)
        for term in terms:
            constant = (
                term.constant
                + sum(
                    coefficient * origin[variable]
                    for variable, coefficient in term.coefficients
                )
            ) % 3
            slopes = tuple(
                sum(
                    coefficient * basis[column][variable]
                    for variable, coefficient in term.coefficients
                )
                % 3
                for column in range(36)
            )
            grouped[(constant, slopes)] += term.sign
        rows.append(
            (
                constant_at_zero,
                tuple(
                    (form, multiplicity)
                    for form, multiplicity in sorted(grouped.items())
                    if multiplicity
                ),
            )
        )
    return profiles, origin, basis, tuple(rows)


def row_statistics(
    row: tuple[
        int,
        Sequence[tuple[tuple[int, Sequence[int]], int]],
    ],
    point: Sequence[int],
) -> tuple[int, int]:
    """Return the exact A,Q statistics at one affine point."""

    constant_at_zero, grouped = row
    phase_sum = 0
    twos = 0
    for (constant, slopes), multiplicity in grouped:
        exponent = (
            constant
            + sum(slope * value for slope, value in zip(slopes, point))
        ) % 3
        phase_sum += multiplicity * exponent
        twos += multiplicity * int(exponent == 2)
    return (
        constant_at_zero - phase_sum,
        constant_at_zero // 3 - twos,
    )


def carry_of_affine_form(
    constant: int,
    slopes: Sequence[int],
    point: Sequence[int],
) -> int:
    """The first base-3 carry of an affine integer lift, modulo 3."""

    total = int(constant) + sum(
        int(slope) * int(value)
        for slope, value in zip(slopes, point)
    )
    return (total // 3) % 3


def cubic_digit_three(
    row: tuple[
        int,
        Sequence[tuple[tuple[int, Sequence[int]], int]],
    ],
    point: Sequence[int],
) -> int:
    """Evaluate A/3 mod 3 using the cubic carry decomposition.

    If t=d+s.y and L is t reduced to {0,1,2}, then

        L = t - 3 floor(t/3).

    The first-digit identity makes C-sum sigma*t coefficientwise divisible
    by three.  The quotient is affine, while floor(t/3) mod 3 is a reduced
    cubic polynomial over F_3 (the first ternary Witt carry).
    """

    constant_at_zero, grouped = row
    base_constant = constant_at_zero
    base_slopes = [0] * len(point)
    for (constant, slopes), multiplicity in grouped:
        base_constant -= multiplicity * constant
        for index, slope in enumerate(slopes):
            base_slopes[index] -= multiplicity * slope
    if base_constant % 3 or any(value % 3 for value in base_slopes):
        raise AssertionError("the first-digit identity is not coefficientwise")
    result = base_constant // 3
    result += sum(
        (value // 3) * int(point[index])
        for index, value in enumerate(base_slopes)
    )
    result += sum(
        multiplicity
        * carry_of_affine_form(constant, slopes, point)
        for (constant, slopes), multiplicity in grouped
    )
    return result % 3


def active_system(rows, point: Sequence[int]) -> tuple[int, ...]:
    """Return the 18 quadratic and 19 cubic residuals.

    E0 at the origin is exactly zero.  E1 at the origin (row 7) has an
    identically zero second digit but becomes a genuine constraint at the
    third digit.
    """

    statistics = tuple(row_statistics(row, point) for row in rows)
    quadratic = tuple(
        statistics[index][1] % 3 for index in SECOND_DIGIT_ROWS
    )
    cubic = tuple(
        cubic_digit_three(rows[index], point) for index in THIRD_DIGIT_ROWS
    )
    if cubic != tuple(
        (statistics[index][0] // 3) % 3 for index in THIRD_DIGIT_ROWS
    ):
        raise AssertionError("the cubic carry decomposition failed")
    return quadratic + cubic


def central_jacobian(evaluate, point: Sequence[int]):
    """Formal Jacobian for reduced polynomials of individual degree <= 2."""

    rows = len(evaluate(point))
    result = [[0] * len(point) for _ in range(rows)]
    for variable in range(len(point)):
        plus = list(point)
        minus = list(point)
        plus[variable] = (plus[variable] + 1) % 3
        minus[variable] = (minus[variable] - 1) % 3
        value_plus = evaluate(tuple(plus))
        value_minus = evaluate(tuple(minus))
        for row in range(rows):
            # For f(t)=a+b*t+c*t^2 over F_3,
            # f'(t)=2*(f(t+1)-f(t-1)).
            result[row][variable] = (
                2 * (value_plus[row] - value_minus[row])
            ) % 3
    return tuple(tuple(row) for row in result)


def solve_linear(
    matrix: Sequence[Sequence[int]],
    target: Sequence[int],
) -> tuple[int, ...] | None:
    augmented = tuple(
        tuple(int(value) % 3 for value in row)
        + ((-int(rhs)) % 3,)
        for row, rhs in zip(matrix, target)
    )
    return second.canonical_solution(augmented, len(matrix[0]))


def audit_delayed_e1_origin(
    profiles,
    rows,
    first_digit_equations,
) -> dict[str, object]:
    """Audit the E1-origin equation delayed from digit 2 to digit 3."""

    raw_target, raw_grouped = prefix.grouped_term_rows(profiles)[7]
    if raw_target != 0 or len(raw_grouped) != 42:
        raise AssertionError("the E1-origin sparse row changed")
    if any(multiplicity not in (-3, 3) for _, multiplicity in raw_grouped):
        raise AssertionError("the E1-origin multiplicities left +/-3")

    constant_at_zero = sum(
        multiplicity for _, multiplicity in raw_grouped
    )
    original_constant = constant_at_zero // 3
    original_linear = [0] * 54
    for (constant, coefficients), multiplicity in raw_grouped:
        epsilon = multiplicity // 3
        original_constant -= epsilon * constant
        for variable, coefficient in coefficients:
            original_linear[variable] -= epsilon * coefficient
    original_linear = tuple(value % 3 for value in original_linear)
    original_constant %= 3

    first_augmented = second.augmented_system(first_digit_equations)
    first_coefficients = tuple(row[:-1] for row in first_augmented)
    delayed_augmented = (
        *first_augmented,
        original_linear + ((-original_constant) % 3,),
    )
    if second.matrix_rank(first_coefficients) != 18:
        raise AssertionError("the first-digit rank changed")
    if second.matrix_rank(tuple(row[:-1] for row in delayed_augmented)) != 19:
        raise AssertionError("the delayed linear row is no longer independent")
    if second.matrix_rank(delayed_augmented) != 19:
        raise AssertionError("the delayed linear row became inconsistent")

    # Compose the delayed digit-3 linear row and its digit-4 quadratic
    # successor with the 36-dimensional first-digit affine space.
    effective_constant, effective_grouped = rows[7]
    delayed_constant = effective_constant // 3
    delayed_linear = [0] * 36
    digit4_constant = effective_constant // 9
    digit4_linear = [0] * 36
    digit4_polar = [[0] * 36 for _ in range(36)]
    for (constant, slopes), multiplicity in effective_grouped:
        if multiplicity % 3:
            raise AssertionError("effective E1-origin multiplicity changed")
        epsilon = multiplicity // 3
        delayed_constant -= epsilon * constant
        digit4_constant -= epsilon * (
            2 * constant * constant + constant
        )
        for left, slope in enumerate(slopes):
            delayed_linear[left] -= epsilon * slope
            digit4_linear[left] -= (
                epsilon * (constant + 1) * slope
            )
            for right, other in enumerate(slopes):
                digit4_polar[left][right] -= (
                    epsilon * slope * other
                )
    delayed_constant %= 3
    delayed_linear = tuple(value % 3 for value in delayed_linear)
    digit4_constant %= 3
    digit4_linear = tuple(value % 3 for value in digit4_linear)
    digit4_polar = tuple(
        tuple(value % 3 for value in row) for row in digit4_polar
    )
    delayed_kernel = second.nullspace_basis((delayed_linear,), 36)
    restricted_polar = tuple(
        tuple(
            sum(
                delayed_kernel[left][source_left]
                * digit4_polar[source_left][source_right]
                * delayed_kernel[right][source_right]
                for source_left in range(36)
                for source_right in range(36)
            )
            % 3
            for right in range(35)
        )
        for left in range(35)
    )

    # Every term is internal to one (channel,class) three-fiber block.
    coordinates = second.active_trit_coordinates(profiles)
    blocks: dict[
        tuple[int, int],
        list[
            tuple[
                tuple[int, tuple[tuple[int, int], ...]],
                int,
            ]
        ],
    ] = defaultdict(list)
    for form, multiplicity in raw_grouped:
        touched = {
            coordinates[variable][:2]
            for variable, _ in form[1]
        }
        if len(touched) != 1:
            raise AssertionError("E1-origin term crossed local blocks")
        blocks[next(iter(touched))].append((form, multiplicity // 3))
    if Counter(map(len, blocks.values())) != Counter({1: 12, 3: 10}):
        raise AssertionError("the E1-origin local-block split changed")

    local_catalogs = Counter()
    for block in blocks.values():
        variables = tuple(
            sorted(
                {
                    variable
                    for (_, coefficients), _ in block
                    for variable, _ in coefficients
                }
            )
        )
        histogram = Counter()
        for values in itertools.product(range(3), repeat=len(variables)):
            assignment = dict(zip(variables, values))
            digit3 = 0
            digit4 = 0
            for (constant, coefficients), epsilon in block:
                exponent = (
                    constant
                    + sum(
                        coefficient * assignment[variable]
                        for variable, coefficient in coefficients
                    )
                ) % 3
                digit3 -= epsilon * exponent
                digit4 -= epsilon * int(exponent == 2)
            histogram[(digit3 % 3, digit4 % 3)] += 1
        local_catalogs[
            (
                len(block),
                tuple(sorted(histogram.items())),
            )
        ] += 1

    expected_catalogs = Counter(
        {
            (
                1,
                (
                    ((0, 0), 3),
                    ((1, 0), 3),
                    ((2, 1), 3),
                ),
            ): 12,
            (
                3,
                (
                    ((1, 0), 9),
                    ((1, 1), 9),
                    ((1, 2), 9),
                ),
            ): 10,
        }
    )
    if local_catalogs != expected_catalogs:
        raise AssertionError("the E1-origin local catalogs changed")

    return {
        "displayed_row": 7,
        "raw_grouped_forms": len(raw_grouped),
        "raw_multiplicity_histogram": {"-3": 12, "3": 30},
        "all_forms_are_two_variable": all(
            len(form[1]) == 2 for form, _ in raw_grouped
        ),
        "local_blocks": len(blocks),
        "local_block_size_histogram": {"1": 12, "3": 10},
        "digit3": {
            "degree": 1,
            "constant": delayed_constant,
            "support": sum(value != 0 for value in delayed_linear),
            "linear_sha256": compact_hash(delayed_linear),
            "independent_first_digit_rank": 19,
            "remaining_affine_dimension": 35,
        },
        "digit4_after_digit3": {
            "degree": 2,
            "constant": digit4_constant,
            "linear_sha256": compact_hash(digit4_linear),
            "polar_sha256": compact_hash(digit4_polar),
            "polar_rank_on_36_space": second.matrix_rank(digit4_polar),
            "polar_rank_on_digit3_hyperplane": second.matrix_rank(
                restricted_polar
            ),
        },
        "local_catalogs": {
            "twelve_singletons": {
                "(digit3,digit4)=(0,0)": 3,
                "(digit3,digit4)=(1,0)": 3,
                "(digit3,digit4)=(2,1)": 3,
            },
            "ten_three_cycles": {
                "(digit3,digit4)=(1,0)": 9,
                "(digit3,digit4)=(1,1)": 9,
                "(digit3,digit4)=(1,2)": 9,
            },
        },
    }


def audit() -> dict[str, object]:
    stored = json.loads(WITNESS.read_text())
    candidate_index = int(stored["candidate_index"])
    profiles, origin, basis, rows = effective_rows(candidate_index)
    first_digit_equations = second.first_digit_equations(profiles)
    point = tuple(map(int, stored["affine_coordinates"]))
    placement = second.lift_affine_point(origin, basis, point)
    if placement != tuple(stored["placement_trits"]):
        raise AssertionError("the pinned placement changed")

    exact_values = second.displayed_values(profiles, placement)
    statistics = tuple(row_statistics(row, point) for row in rows)
    reconstructed = tuple((a, 3 * q - a) for a, q in statistics)
    if reconstructed != exact_values:
        raise AssertionError("the A,Q coordinates failed exact replay")

    digits = tuple(second.lambda_digits(value, 9) for value in exact_values)
    for row, ((a, q), row_digits) in enumerate(zip(statistics, digits)):
        conditions = (
            a % 3 == 0,
            a % 3 == 0 and q % 3 == 0,
            a % 9 == 0 and q % 3 == 0,
            a % 9 == 0 and q % 9 == 0,
            a % 27 == 0 and q % 9 == 0,
            a % 27 == 0 and q % 27 == 0,
            a % 81 == 0 and q % 27 == 0,
            a % 81 == 0 and q % 81 == 0,
        )
        expected = (
            not any(row_digits[:2]),
            not any(row_digits[:3]),
            not any(row_digits[:4]),
            not any(row_digits[:5]),
            not any(row_digits[:6]),
            not any(row_digits[:7]),
            not any(row_digits[:8]),
            not any(row_digits[:9]),
        )
        if conditions != expected:
            raise AssertionError(
                f"prefix congruence mismatch in displayed row {row}"
            )

    system = active_system(rows, point)
    jacobian = central_jacobian(
        lambda value: active_system(rows, value), point
    )
    quadratic_jacobian = jacobian[: len(SECOND_DIGIT_ROWS)]
    cubic_jacobian = jacobian[len(SECOND_DIGIT_ROWS) :]
    full_rank = second.matrix_rank(jacobian)
    q_rank = second.matrix_rank(quadratic_jacobian)
    r_rank = second.matrix_rank(cubic_jacobian)
    correction = solve_linear(jacobian, system)
    corrected = None
    if correction is not None:
        next_point = tuple(
            (left + right) % 3 for left, right in zip(point, correction)
        )
        next_system = active_system(rows, next_point)
        corrected = {
            "correction": correction,
            "point_sha256": compact_hash(next_point),
            "quadratic_nonzero": sum(
                value != 0
                for value in next_system[: len(SECOND_DIGIT_ROWS)]
            ),
            "cubic_nonzero": sum(
                value != 0
                for value in next_system[len(SECOND_DIGIT_ROWS) :]
            ),
        }

    row_summary = tuple(
        {
            "row": index,
            "constant_at_zero": constant,
            "effective_forms": len(grouped),
            "maximum_form_support": max(
                (
                    sum(value != 0 for value in slopes)
                    for (_, slopes), _ in grouped
                ),
                default=0,
            ),
        }
        for index, (constant, grouped) in enumerate(rows)
    )
    result = {
        "schema": "lp333-order3-digit3-carry-audit-v1",
        "label": stored["label"],
        "second_digit_rows": SECOND_DIGIT_ROWS,
        "third_digit_rows": THIRD_DIGIT_ROWS,
        "exact_coordinate_identity": "F=A+(3Q-A)omega",
        "prefix_lattice": {
            "digits_0_through_2": "A=0 mod 3, Q=0 mod 3",
            "digits_0_through_3": "A=0 mod 9, Q=0 mod 3",
            "digits_0_through_4": "A=0 mod 9, Q=0 mod 9",
            "digits_0_through_8": "A=0 mod 81, Q=0 mod 81",
            "exact": "A=Q=0",
        },
        "witness": {
            "quadratic_nonzero": sum(
                value != 0
                for value in system[: len(SECOND_DIGIT_ROWS)]
            ),
            "cubic_nonzero": sum(
                value != 0
                for value in system[len(SECOND_DIGIT_ROWS) :]
            ),
            "a_values": tuple(a for a, _ in statistics),
            "q_values": tuple(q for _, q in statistics),
        },
        "jacobian_at_witness": {
            "quadratic_rank": q_rank,
            "cubic_rank": r_rank,
            "combined_rank": full_rank,
            "combined_shape": (len(jacobian), len(jacobian[0])),
            "newton_correction": corrected,
        },
        "delayed_e1_origin": audit_delayed_e1_origin(
            profiles, rows, first_digit_equations
        ),
        "row_summary": row_summary,
    }
    return result


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")


if __name__ == "__main__":
    main()

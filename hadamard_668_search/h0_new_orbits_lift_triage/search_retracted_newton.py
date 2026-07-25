#!/usr/bin/env python3
"""Retracted Newton search for the three new exact h=0 profile orbits.

This is a bounded witness finder, not a verifier.  Five (or four) structured
quadratic combinations are solved identically by translating along a common
polar radical.  Newton steps are then taken on that exact quadratic zero set.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
HIGHER = SECOND / "higher_digits"
ORBIT2_THEORY = SEARCH / "h0_orbit2_quadric_theory"
sys.path[:0] = [
    str(ORBIT2_THEORY),
    str(HIGHER),
    str(SECOND),
    str(SEARCH),
]

import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_labeled_jet import actual_word  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    row_sum_catalog,
)
from verify_quadric_character_compression import (  # noqa: E402
    canonical_solution as solve_linear,
    nullspace_mod3,
    rank_mod3,
)


ACTIVE_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))
PROFILES = {
    "c90c": {
        "digest": "0xc90c2887b652140a",
        "ids_a": (1, 1, 5, 5, 2, 4, 5, 2, 5, 2, 4, 1),
        "ids_b": (1, 7, 8, 2, 6, 7, 5, 2, 4, 7, 6, 5),
        "target": (-3, 0, 0, 3),
        "retraction_subset": (0, 1, 3, 4, 5),
    },
    "6e45": {
        "digest": "0x6e45edfb0bfb0974",
        "ids_a": (1, 2, 7, 5, 5, 2, 6, 6, 1, 5, 8, 7),
        "ids_b": (2, 7, 7, 1, 1, 5, 4, 5, 6, 6, 5, 8),
        "target": (0, 3, -4, -2),
        "retraction_subset": (0, 1, 2, 5),
    },
    "533a": {
        "digest": "0x533a4ccf9d6a91d8",
        "ids_a": (1, 5, 6, 4, 4, 1, 5, 6, 6, 5, 2, 8),
        "ids_b": (8, 5, 2, 4, 2, 5, 7, 7, 4, 5, 2, 6),
        "target": (2, -2, -2, 2),
        "retraction_subset": (0, 2, 3, 4, 5),
    },
}


def exact_forms_record(
    ids_a: tuple[int, ...], ids_b: tuple[int, ...]
):
    profiles = profiles_from_ids(ids_a, ids_b)
    equations = first_digit_equations(profiles)
    rows = augmented_system(equations)
    coefficients = tuple(row[:-1] for row in rows)
    origin = canonical_solution(rows, 54)
    if origin is None:
        raise AssertionError("first placement digit became inconsistent")
    basis = second.nullspace_basis(coefficients, columns=54)
    if matrix_rank(coefficients) != 18 or len(basis) != 36:
        raise AssertionError("first placement rank/nullity changed")
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles), origin, basis
    )
    active = tuple(
        index
        for index in range(20)
        if (
            constants[index]
            or any(linears[index])
            or any(value for row in polars[index] for value in row)
        )
    )
    if active != ACTIVE_ROWS:
        raise AssertionError("active second-digit rows changed")
    return (
        profiles,
        origin,
        basis,
        np.array([constants[index] for index in active], dtype=np.int16),
        np.array([linears[index] for index in active], dtype=np.int16),
        np.array([polars[index] for index in active], dtype=np.int16),
    )


def exact_forms(label: str):
    record = PROFILES[label]
    return exact_forms_record(record["ids_a"], record["ids_b"])


def structured_forms(
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return (
        np.array(
            [
                constants[index]
                + constants[index + 6]
                + constants[index + 12]
                for index in range(6)
            ],
            dtype=np.int16,
        )
        % 3,
        np.array(
            [
                linears[index]
                + linears[index + 6]
                + linears[index + 12]
                for index in range(6)
            ],
            dtype=np.int16,
        )
        % 3,
        np.array(
            [
                polars[index]
                + polars[index + 6]
                + polars[index + 12]
                for index in range(6)
            ],
            dtype=np.int16,
        )
        % 3,
    )


def evaluate(
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
    point: np.ndarray,
) -> np.ndarray:
    return (
        constants
        + linears @ point
        + 2 * np.einsum("i,eij,j->e", point, polars, point)
    ) % 3


def evaluate_batch(
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
    points: np.ndarray,
) -> np.ndarray:
    result = np.empty((len(points), len(constants)), dtype=np.int16)
    for equation in range(len(constants)):
        result[:, equation] = (
            constants[equation]
            + points @ linears[equation]
            + 2
            * np.sum((points @ polars[equation]) * points, axis=1)
        ) % 3
    return result


def affine_solve(
    matrix: np.ndarray, rhs: np.ndarray
) -> tuple[np.ndarray, np.ndarray] | None:
    rows, columns = matrix.shape
    work = np.column_stack((matrix % 3, rhs % 3)).astype(np.int16)
    pivot_columns: list[int] = []
    row = 0
    for column in range(columns):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        if work[row, column] == 2:
            work[row] = 2 * work[row] % 3
        for other in range(rows):
            if other != row and work[other, column]:
                work[other] = (
                    work[other] - work[other, column] * work[row]
                ) % 3
        pivot_columns.append(column)
        row += 1
        if row == rows:
            break
    if any(
        not np.any(work[index, :-1]) and work[index, -1]
        for index in range(row, rows)
    ):
        return None
    free = [
        column for column in range(columns) if column not in pivot_columns
    ]
    particular = np.zeros(columns, dtype=np.int16)
    for equation, pivot in enumerate(pivot_columns):
        particular[pivot] = work[equation, -1]
    basis = np.zeros((len(free), columns), dtype=np.int16)
    for index, free_column in enumerate(free):
        basis[index, free_column] = 1
        for equation, pivot in enumerate(pivot_columns):
            basis[index, pivot] = -work[equation, free_column] % 3
    return particular, basis


def retraction_data(
    subset: tuple[int, ...],
    g_linears: np.ndarray,
    g_polars: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    radical = nullspace_mod3(g_polars[list(subset)].reshape(-1, 36))
    restriction = g_linears[list(subset)] @ radical.T % 3
    if rank_mod3(restriction) != len(subset):
        raise AssertionError("the selected structured forms do not retract")
    columns = []
    for coordinate in range(len(subset)):
        target = np.zeros(len(subset), dtype=np.int16)
        target[coordinate] = 1
        coefficients = solve_linear(restriction, target)
        columns.append(coefficients @ radical % 3)
    directions = np.array(columns, dtype=np.int16).T % 3
    if np.any(
        np.einsum(
            "eij,jk->eik", g_polars[list(subset)], directions
        )
        % 3
    ):
        raise AssertionError("a retraction direction left the common radical")
    if not np.array_equal(
        g_linears[list(subset)] @ directions % 3,
        np.eye(len(subset), dtype=np.int16),
    ):
        raise AssertionError("the retraction directions lost unit response")
    return radical, directions


def equation_basis(subset: tuple[int, ...]) -> np.ndarray:
    rows = []
    for structured_index in subset:
        row = np.zeros(18, dtype=np.int16)
        row[structured_index] = 1
        row[structured_index + 6] = 1
        row[structured_index + 12] = 1
        rows.append(row)
    rank = rank_mod3(np.array(rows, dtype=np.int16))
    for index in range(18):
        row = np.zeros(18, dtype=np.int16)
        row[index] = 1
        candidate = np.array(rows + [row], dtype=np.int16)
        next_rank = rank_mod3(candidate)
        if next_rank > rank:
            rows.append(row)
            rank = next_rank
        if rank == 18:
            break
    transform = np.array(rows, dtype=np.int16)
    if transform.shape != (18, 18) or rank_mod3(transform) != 18:
        raise AssertionError("failed to complete an equation basis")
    return transform


def replay(label: str, affine: np.ndarray) -> dict[str, object]:
    profiles, origin, basis, _, _, _ = exact_forms(label)
    placement = second.lift_affine_point(
        origin, basis, tuple(map(int, affine))
    )
    first = second.symbolic_first_digits(
        first_digit_equations(profiles), placement
    )
    second_symbolic = second.symbolic_second_digits(
        second.second_digit_term_data(profiles), placement
    )
    second_direct = second.direct_second_digits(profiles, placement)
    if first != (0,) * 20:
        raise AssertionError("witness failed first-digit replay")
    if second_symbolic != (0,) * 20 or second_direct != (0,) * 20:
        raise AssertionError("witness failed second-digit replay")
    values = second.displayed_values(profiles, placement)
    digits = tuple(second.lambda_digits(value, 12) for value in values)
    masks_a, masks_b = second.masks_from_trits(profiles, placement)
    # This is the exact 18-coordinate physical catalog word, not a proxy.
    words = tuple(
        tuple(
            actual_word(channel, class_index, masks[class_index])
            for class_index in range(12)
        )
        for channel, masks in enumerate((masks_a, masks_b))
    )
    aggregate = []
    for row in range(9):
        plus_a = sum(word[row] for word in words[0])
        plus_b = sum(word[row] for word in words[1])
        aggregate.extend((plus_a + plus_b - 12, plus_b - plus_a))
    aggregate_tuple = tuple(aggregate)
    return {
        "affine_coordinates": tuple(map(int, affine)),
        "placement_trits": placement,
        "masks_a": masks_a,
        "masks_b": masks_b,
        "displayed_exact_values": values,
        "lambda_digits_through_11": digits,
        "nonzero_rows_by_digit": tuple(
            sum(row[digit] != 0 for row in digits) for digit in range(12)
        ),
        "row_margin_aggregate": aggregate_tuple,
        "row_margin_catalog_member": aggregate_tuple in row_sum_catalog(),
    }


def search(
    label: str,
    seconds: float,
    seed: int,
    samples: int,
    collect: int,
) -> dict[str, object]:
    (
        _,
        _,
        _,
        q_constants,
        q_linears,
        q_polars,
    ) = exact_forms(label)
    g_constants, g_linears, g_polars = structured_forms(
        q_constants, q_linears, q_polars
    )
    subset = tuple(PROFILES[label]["retraction_subset"])
    radical, directions = retraction_data(
        subset, g_linears, g_polars
    )
    transform = equation_basis(subset)
    h_constants = transform @ q_constants % 3
    h_linears = transform @ q_linears % 3
    h_polars = np.einsum(
        "ae,eij->aij", transform, q_polars
    ) % 3
    rng = np.random.default_rng(seed)

    def retract(points: np.ndarray) -> np.ndarray:
        values = evaluate_batch(
            g_constants[list(subset)],
            g_linears[list(subset)],
            g_polars[list(subset)],
            points,
        )
        corrected = (points - values @ directions.T) % 3
        if np.any(
            evaluate_batch(
                g_constants[list(subset)],
                g_linears[list(subset)],
                g_polars[list(subset)],
                corrected,
            )
        ):
            raise AssertionError("quadratic retraction failed exact replay")
        return corrected

    started = time.monotonic()
    iterations = 0
    restarts = 0
    best_defect = 19
    best_point: np.ndarray | None = None
    best_values: np.ndarray | None = None
    witnesses: list[dict[str, object]] = []
    seen: set[tuple[int, ...]] = set()
    while time.monotonic() - started < seconds and len(witnesses) < collect:
        point = retract(
            rng.integers(0, 3, size=(1, 36), dtype=np.int16)
        )[0]
        for _ in range(100):
            values = evaluate(
                h_constants, h_linears, h_polars, point
            )
            defect = int(np.count_nonzero(values))
            if defect < best_defect:
                best_defect = defect
                best_point = point.copy()
                best_values = values.copy()
            if defect == 0:
                key = tuple(map(int, point))
                if key not in seen:
                    seen.add(key)
                    witnesses.append(replay(label, point))
                break
            jacobian = (
                h_linears
                + np.einsum("eij,j->ei", h_polars, point)
            ) % 3
            solved = affine_solve(jacobian, -values)
            if solved is None:
                break
            particular, kernel = solved
            coefficients = rng.integers(
                0,
                3,
                size=(samples, len(kernel)),
                dtype=np.int16,
            )
            deltas = (particular + coefficients @ kernel) % 3
            candidates = retract((point + deltas) % 3)
            candidate_values = evaluate_batch(
                h_constants, h_linears, h_polars, candidates
            )
            scores = np.count_nonzero(candidate_values, axis=1)
            minimum = int(scores.min())
            choices = np.flatnonzero(scores == minimum)
            point = candidates[int(rng.choice(choices))]
            iterations += 1
            if time.monotonic() - started >= seconds:
                break
        restarts += 1

    result: dict[str, object] = {
        "schema": "h668-new-h0-retracted-newton-v1",
        "scope": (
            "Bounded digit-2 witness search; UNKNOWN is not an exclusion "
            "and a witness is not an LP(333) or H(668)."
        ),
        "label": label,
        "profile": PROFILES[label],
        "retraction": {
            "structured_subset": subset,
            "equations": len(subset),
            "common_radical_dimension": len(radical),
            "direction_matrix": directions.tolist(),
        },
        "search": {
            "seconds_limit": seconds,
            "seconds_used": time.monotonic() - started,
            "seed": seed,
            "samples_per_step": samples,
            "iterations": iterations,
            "restarts": restarts,
            "best_defect": best_defect,
            "status": "SAT" if witnesses else "UNKNOWN",
        },
        "witnesses": witnesses,
    }
    if best_point is not None and best_values is not None:
        result["best_affine_coordinates"] = best_point.tolist()
        result["best_basis_residuals"] = best_values.tolist()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=tuple(PROFILES), required=True)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--seed", type=int, default=668_330)
    parser.add_argument("--samples", type=int, default=512)
    parser.add_argument("--collect", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = search(
        args.profile,
        args.seconds,
        args.seed,
        args.samples,
        args.collect,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()

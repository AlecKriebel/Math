#!/usr/bin/env python3
"""Tabu repair inside one exact row-margin phase-sum fiber.

For a fixed compatible six-sum target, every move replaces two placement
trits whose combined phase contribution is unchanged.  Row-margin
membership is therefore invariant by construction.  The search repairs the
rank-18 first layer and the eighteen active digit-2 quadrics
lexicographically.  It is a bounded witness search, never an exclusion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HIGHER_DIGITS))
sys.path.insert(0, str(SEARCH_ROOT))

import solve_full_second_digit_sat as quadratic  # noqa: E402
import solve_sparse_histogram_cp_sat as sparse  # noqa: E402


def initial_margin_point(
    candidate_index: int,
    target_index: int,
    seed: int,
) -> tuple[int, ...]:
    candidate = quadratic.second.CANDIDATES[candidate_index]
    profiles = quadratic.second.profiles_from_ids(
        candidate[3], candidate[4]
    )
    model = cp_model.CpModel()
    placement = tuple(
        model.new_int_var(0, 2, f"placement_{index}")
        for index in range(54)
    )
    sparse.add_row_margin_membership(
        model,
        placement,
        profiles,
        candidate[3],
        candidate[4],
        target_index,
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    solver.parameters.randomize_search = True
    status = solver.solve(model)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        raise AssertionError("a compatible phase-sum target became empty")
    return tuple(int(solver.value(variable)) for variable in placement)


def original_quadratic_forms(profiles):
    variables = 54
    origin = (0,) * variables
    basis = tuple(
        tuple(int(row == column) for column in range(variables))
        for row in range(variables)
    )
    constants, linears, polars = quadratic.second.derive_quadratics(
        quadratic.second.second_digit_term_data(profiles),
        origin,
        basis,
    )
    active = tuple(range(1, 7)) + tuple(range(8, 20))
    return (
        np.array(tuple(constants[index] for index in active), dtype=np.int16),
        np.array(tuple(linears[index] for index in active), dtype=np.int16),
        np.array(tuple(polars[index] for index in active), dtype=np.int16),
    )


def first_linear_forms(profiles):
    equations = quadratic.second.first_digit_equations(profiles)
    constants = np.array(
        tuple(int(equation.affine[0]) for equation in equations),
        dtype=np.int16,
    )
    linears = np.array(
        tuple(
            tuple(map(int, equation.affine[1:]))
            for equation in equations
        ),
        dtype=np.int16,
    )
    return constants, linears


def exact_state(
    point: np.ndarray,
    first_constants: np.ndarray,
    first_linears: np.ndarray,
    quadratic_constants: np.ndarray,
    quadratic_linears: np.ndarray,
    polars: np.ndarray,
):
    first = (first_constants + first_linears @ point) % 3
    quadratics = (
        quadratic_constants
        + quadratic_linears @ point
        + 2
        * np.einsum(
            "i,eij,j->e", point, polars, point, optimize=True
        )
    ) % 3
    gradients = (
        quadratic_linears
        + np.einsum("eij,j->ei", polars, point, optimize=True)
    ) % 3
    return first, quadratics, gradients


def preserving_pair_moves(
    point: np.ndarray,
    effects: np.ndarray,
    groups,
):
    left_variables = []
    right_variables = []
    left_deltas = []
    right_deltas = []
    for group in groups:
        for left_offset, left in enumerate(group):
            for right in group[left_offset + 1 :]:
                current = (
                    effects[left, point[left]]
                    + effects[right, point[right]]
                )
                for left_value in range(3):
                    if left_value == point[left]:
                        continue
                    for right_value in range(3):
                        if right_value == point[right]:
                            continue
                        if np.array_equal(
                            effects[left, left_value]
                            + effects[right, right_value],
                            current,
                        ):
                            left_variables.append(left)
                            right_variables.append(right)
                            left_deltas.append(
                                (left_value - int(point[left])) % 3
                            )
                            right_deltas.append(
                                (right_value - int(point[right])) % 3
                            )
    return (
        np.array(left_variables, dtype=np.int16),
        np.array(right_variables, dtype=np.int16),
        np.array(left_deltas, dtype=np.int16),
        np.array(right_deltas, dtype=np.int16),
    )


def replay(
    candidate_index: int,
    point: np.ndarray,
    target_index: int,
) -> dict[str, object]:
    candidate = quadratic.second.CANDIDATES[candidate_index]
    profiles = quadratic.second.profiles_from_ids(
        candidate[3], candidate[4]
    )
    placement = tuple(map(int, point))
    first = quadratic.second.symbolic_first_digits(
        quadratic.second.first_digit_equations(profiles), placement
    )
    second_digits = quadratic.second.symbolic_second_digits(
        quadratic.second.second_digit_term_data(profiles), placement
    )
    masks = quadratic.second.masks_from_trits(profiles, placement)
    phase_sums = sparse.phase_sums_from_masks(*masks)
    catalog = sparse.catalog_phase_sum_intersection(
        candidate[3], candidate[4]
    )
    target = catalog["phase_sum_corpus"][target_index][0]
    if phase_sums != target:
        raise AssertionError("a permutation move left its margin target")
    exact_values = quadratic.second.displayed_values(profiles, placement)
    digits = tuple(
        quadratic.second.lambda_digits(value, 10)
        for value in exact_values
    )
    if tuple(row[1] for row in digits) != first:
        raise AssertionError("the first-digit replay changed")
    if tuple(row[2] for row in digits) != second_digits:
        raise AssertionError("the second-digit replay changed")
    return {
        "placement_trits": placement,
        "placement_trits_sha256": quadratic.compact_hash(placement),
        "phase_sums": phase_sums,
        "row_margin_target_index": target_index,
        "first_digit_nonzero_rows": sum(value != 0 for value in first),
        "second_digit_nonzero_rows": sum(
            value != 0 for value in second_digits
        ),
        "digit_nonzero_rows_through_8": tuple(
            sum(row[digit] != 0 for row in digits)
            for digit in range(9)
        ),
    }


def search(
    candidate_index: int,
    target_index: int,
    seconds: float,
    seed: int,
    first_weight: int,
    restart_updates: int,
) -> dict[str, object]:
    if first_weight <= 18:
        raise ValueError("first_weight must make the search lexicographic")
    candidate = quadratic.second.CANDIDATES[candidate_index]
    profiles = quadratic.second.profiles_from_ids(
        candidate[3], candidate[4]
    )
    first_constants, first_linears = first_linear_forms(profiles)
    quadratic_constants, quadratic_linears, polars = (
        original_quadratic_forms(profiles)
    )
    baseline, raw_effects = sparse.phase_sum_affine_data(profiles)
    effects = np.array(raw_effects, dtype=np.int16) - np.array(
        baseline, dtype=np.int16
    )[None, None, :]
    coordinates = quadratic.second.active_trit_coordinates(profiles)
    groups = tuple(
        tuple(
            index
            for index, coordinate in enumerate(coordinates)
            if coordinate[0] == channel and coordinate[2] == residue
        )
        for channel in range(2)
        for residue in range(3)
    )
    if sum(map(len, groups)) != 54 or any(not group for group in groups):
        raise AssertionError("the six phase-sum groups changed")

    rng = np.random.default_rng(seed)
    started = time.monotonic()
    deadline = started + seconds
    updates = 0
    restarts = 0
    best_pair = (21, 19)
    best_point = None
    best_replay = None

    while time.monotonic() < deadline:
        point = np.array(
            initial_margin_point(
                candidate_index,
                target_index,
                seed + 1009 * restarts,
            ),
            dtype=np.int16,
        )
        # Diversify within the exact target fiber before objective repair.
        for _ in range(200 + 50 * (restarts % 7)):
            moves = preserving_pair_moves(point, effects, groups)
            if len(moves[0]) == 0:
                break
            move = int(rng.integers(0, len(moves[0])))
            point[moves[0][move]] = (
                point[moves[0][move]] + moves[2][move]
            ) % 3
            point[moves[1][move]] = (
                point[moves[1][move]] + moves[3][move]
            ) % 3

        first, quadratics, gradients = exact_state(
            point,
            first_constants,
            first_linears,
            quadratic_constants,
            quadratic_linears,
            polars,
        )
        tabu_until = np.zeros(54, dtype=np.int64)
        for _ in range(restart_updates):
            pair = (
                int(np.count_nonzero(first)),
                int(np.count_nonzero(quadratics)),
            )
            if pair < best_pair:
                best_pair = pair
                best_point = point.copy()
                best_replay = replay(
                    candidate_index, point, target_index
                )
                if (
                    best_replay["first_digit_nonzero_rows"],
                    best_replay["second_digit_nonzero_rows"],
                ) != pair:
                    raise AssertionError(
                        "incremental and replayed objectives disagree"
                    )
                print(
                    f"best_first={pair[0]} best_digit2={pair[1]} "
                    f"updates={updates} restarts={restarts} "
                    f"seconds={time.monotonic()-started:.3f}",
                    flush=True,
                )
                if pair == (0, 0):
                    break

            left, right, delta_left, delta_right = (
                preserving_pair_moves(point, effects, groups)
            )
            if len(left) == 0:
                break
            moved_first = (
                first[:, None]
                + first_linears[:, left] * delta_left
                + first_linears[:, right] * delta_right
            ) % 3
            diagonal_left = polars[:, left, left]
            diagonal_right = polars[:, right, right]
            cross = polars[:, left, right]
            quadratic_change = (
                gradients[:, left] * delta_left
                + gradients[:, right] * delta_right
                + 2
                * (
                    diagonal_left * delta_left * delta_left
                    + 2 * cross * delta_left * delta_right
                    + diagonal_right * delta_right * delta_right
                )
            ) % 3
            moved_quadratics = (
                quadratics[:, None] + quadratic_change
            ) % 3
            first_counts = np.count_nonzero(moved_first, axis=0)
            quadratic_counts = np.count_nonzero(
                moved_quadratics, axis=0
            )
            scores = first_weight * first_counts + quadratic_counts
            allowed = (
                (tabu_until[left] <= updates)
                & (tabu_until[right] <= updates)
            ) | (
                (first_counts < best_pair[0])
                | (
                    (first_counts == best_pair[0])
                    & (quadratic_counts < best_pair[1])
                )
            )
            ranked = np.where(allowed, scores, 32767)
            choices = np.flatnonzero(ranked == ranked.min())
            move = int(rng.choice(choices))
            left_variable = int(left[move])
            right_variable = int(right[move])
            left_change = int(delta_left[move])
            right_change = int(delta_right[move])
            point[left_variable] = (
                point[left_variable] + left_change
            ) % 3
            point[right_variable] = (
                point[right_variable] + right_change
            ) % 3
            first = moved_first[:, move]
            quadratics = moved_quadratics[:, move]
            gradients = (
                gradients
                + left_change * polars[:, :, left_variable]
                + right_change * polars[:, :, right_variable]
            ) % 3
            tenure = 4 + int(rng.integers(0, 5))
            tabu_until[left_variable] = updates + tenure
            tabu_until[right_variable] = updates + tenure
            updates += 1
            if pair == (0, 0) or time.monotonic() >= deadline:
                break
        if best_pair == (0, 0):
            break
        restarts += 1

    if best_point is None or best_replay is None:
        raise AssertionError("the permutation search evaluated no point")
    result = {
        "schema": "lp333-order3-row-margin-permutation-tabu-v1",
        "scope": (
            "Bounded exact-target permutation search; UNKNOWN is not an "
            "exclusion."
        ),
        "candidate_index": candidate_index,
        "label": candidate[0],
        "row_margin_target_index": target_index,
        "status": "SAT" if best_pair == (0, 0) else "UNKNOWN",
        "seconds": seconds,
        "seed": seed,
        "first_weight": first_weight,
        "updates": updates,
        "restarts": restarts,
        "best_first_digit_nonzero_rows": best_pair[0],
        "best_second_digit_nonzero_rows": best_pair[1],
        "best_replay": best_replay,
    }
    result["semantic_sha256"] = quadratic.compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=0, choices=range(5))
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--first-weight", type=int, default=30)
    parser.add_argument("--restart-updates", type=int, default=100000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = search(
        args.candidate,
        args.target,
        args.seconds,
        args.seed,
        args.first_weight,
        args.restart_updates,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bounded digit-three search with the exact physical row-margin gate.

This augments the sparse 54-trit digit-three model by requiring its six
Eisenstein phase sums to occur in the exact row-sum catalog for the fixed
profile.  A returned assignment is replayed independently.  ``UNKNOWN`` is
never an exclusion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
CARRY = SEARCH_ROOT / "digit3_carry_algebra"
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
for path in (SEARCH_ROOT, CARRY, SECOND_DIGIT, HIGHER_DIGITS):
    sys.path.insert(0, str(path))

import audit_digit3_carry as carry  # noqa: E402
import solve_sparse_histogram_cp_sat as sparse  # noqa: E402
import verify_full_second_digit_witness as witness  # noqa: E402
import verify_lp333_order3_phase_transfer as transfer  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402


ROOTS = ((1, 0), (0, 1), (-1, -1))


def flatten_sums(sums):
    return tuple(
        coordinate
        for channel in sums
        for value in channel
        for coordinate in value
    )


def add_row_margin_gate(
    model: cp_model.CpModel,
    placement,
    profiles,
    candidate,
    target_index: int | None,
) -> tuple[cp_model.IntVar, tuple[tuple[object, int], ...]]:
    """Add exact membership in the compatible six-sum catalog."""

    catalog = transfer.catalog_phase_sum_intersection(
        candidate[3], candidate[4]
    )
    corpus = tuple(catalog["phase_sum_corpus"])
    if not corpus:
        raise AssertionError("the fixed profile lost every row-margin target")
    if target_index is not None and not 0 <= target_index < len(corpus):
        raise ValueError("target index lies outside the compatible corpus")

    entries = second.phase_entries(profiles)
    fixed = [[[0, 0] for _ in range(3)] for _ in range(2)]
    occurrences: dict[int, list[tuple[int, int, int, int, int]]] = {}
    for channel in range(2):
        for column in range(37):
            for residue in range(3):
                entry = entries[channel][column][residue]
                if entry is None:
                    continue
                if entry.variable is None:
                    root = ROOTS[entry.constant % 3]
                    fixed[channel][residue][0] += entry.sign * root[0]
                    fixed[channel][residue][1] += entry.sign * root[1]
                    continue
                occurrences.setdefault(int(entry.variable), []).append(
                    (
                        channel,
                        residue,
                        int(entry.sign),
                        int(entry.constant),
                        int(entry.slope),
                    )
                )

    if set(occurrences) != set(range(54)):
        raise AssertionError("the phase-sum gate lost a placement trit")
    contributions = []
    grouped: list[list[list[tuple[int, cp_model.IntVar]]]] = [
        [[], [], []],
        [[], [], []],
    ]
    for variable in range(54):
        records = occurrences[variable]
        if len(records) != 3 or len(set(records)) != 1:
            raise AssertionError(
                "a nonzero multiplier class lost its threefold phase entry"
            )
        channel, residue, sign, constant, slope = records[0]
        first = model.new_int_var(-1, 1, f"margin_a_{variable}")
        omega_coordinate = model.new_int_var(
            -1, 1, f"margin_b_{variable}"
        )
        rows = []
        for trit in range(3):
            root = ROOTS[(constant + slope * trit) % 3]
            rows.append((trit, sign * root[0], sign * root[1]))
        model.add_allowed_assignments(
            (placement[variable], first, omega_coordinate), rows
        )
        grouped[channel][residue].append((3, first))
        grouped[channel][residue].append((3, omega_coordinate))
        contributions.append((first, omega_coordinate))

    coordinate_variables = []
    for channel in range(2):
        for residue in range(3):
            for coordinate in range(2):
                variable = model.new_int_var(
                    -37, 37, f"margin_sum_{channel}_{residue}_{coordinate}"
                )
                terms = [
                    grouped[channel][residue][2 * index + coordinate][0]
                    * grouped[channel][residue][2 * index + coordinate][1]
                    for index in range(
                        len(grouped[channel][residue]) // 2
                    )
                ]
                model.add(
                    variable
                    == fixed[channel][residue][coordinate] + sum(terms)
                )
                coordinate_variables.append(variable)

    selected = model.new_int_var(
        0, len(corpus) - 1, "row_margin_target_index"
    )
    allowed = tuple(
        (index, *flatten_sums(sums))
        for index, (sums, _) in enumerate(corpus)
        if target_index is None or index == target_index
    )
    model.add_allowed_assignments(
        (selected, *coordinate_variables), allowed
    )
    if target_index is not None:
        model.add(selected == target_index)
    return selected, corpus


def solve(
    candidate_index: int,
    seconds: float,
    workers: int,
    seed: int,
    target_index: int | None,
    initial_placement: tuple[int, ...] | None,
) -> dict[str, object]:
    started = time.monotonic()
    model, placement, profiles, _, construction = sparse.build_model(
        candidate_index, "digit3"
    )
    candidate = second.CANDIDATES[candidate_index]
    selected, corpus = add_row_margin_gate(
        model, placement, profiles, candidate, target_index
    )
    if initial_placement is not None:
        if len(initial_placement) != 54:
            raise ValueError("the initial placement must have 54 trits")
        for variable, value in zip(placement, initial_placement):
            model.add_hint(variable, int(value))
        masks = second.masks_from_trits(profiles, initial_placement)
        initial_sums = transfer.phase_sums_from_masks(*masks)
        initial_indices = tuple(
            index
            for index, (sums, _) in enumerate(corpus)
            if sums == initial_sums
        )
        if len(initial_indices) == 1:
            model.add_hint(selected, initial_indices[0])
    built = time.monotonic()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.cp_model_presolve = True
    status = solver.solve(model)
    finished = time.monotonic()
    result: dict[str, object] = {
        "schema": "lp333-order3-row-margin-digit3-cp-sat-v1",
        "scope": (
            "Bounded exact row-margin plus digit-three search. UNKNOWN is "
            "not an exclusion."
        ),
        "label": candidate[0],
        "candidate_index": candidate_index,
        "target_index": target_index,
        "initial_placement": initial_placement is not None,
        "compatible_targets": len(corpus),
        "status": solver.status_name(status),
        "construction": {
            **construction,
            "row_margin_contribution_pairs": 54,
            "row_margin_sum_coordinates": 12,
            "row_margin_allowed_rows": (
                1 if target_index is not None else len(corpus)
            ),
            "final_variables": len(model.proto.variables),
            "final_constraints": len(model.proto.constraints),
        },
        "solver": {
            "seconds": seconds,
            "workers": workers,
            "seed": seed,
            "build_seconds": built - started,
            "solve_seconds": finished - built,
            "branches": solver.num_branches,
            "conflicts": solver.num_conflicts,
            "wall_time": solver.wall_time,
        },
    }
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        point = tuple(int(solver.value(variable)) for variable in placement)
        selected_index = int(solver.value(selected))
        exact_values = second.displayed_values(profiles, point)
        digits = tuple(second.lambda_digits(value, 9) for value in exact_values)
        if any(any(row[:4]) for row in digits):
            raise AssertionError("the returned point failed digit-three replay")
        masks_a, masks_b = second.masks_from_trits(profiles, point)
        sums = transfer.phase_sums_from_masks(masks_a, masks_b)
        if sums != corpus[selected_index][0]:
            raise AssertionError("the returned point failed row-margin replay")
        columns = witness.expand_columns(masks_a, masks_b)
        proper_fixed = tuple(
            witness.fixed_by_multiplier(columns, multiplier)
            for multiplier in witness.SUPERGROUP_GENERATORS
        )
        result.update(
            {
                "selected_target_index": selected_index,
                "selected_target_multiplicity": int(
                    corpus[selected_index][1]
                ),
                "phase_sums": sums,
                "placement_trits": point,
                "placement_trits_sha256": carry.compact_hash(point),
                "displayed_exact_values": exact_values,
                "lambda_digits_through_8": digits,
                "proper_supergroup_fixed": proper_fixed,
                "digit4_nonzero_rows": sum(row[4] != 0 for row in digits),
            }
        )
    result["semantic_sha256"] = carry.compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=0, choices=range(5))
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--target-index", type=int)
    parser.add_argument("--initial-certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    initial = None
    if args.initial_certificate is not None:
        stored = json.loads(args.initial_certificate.read_text())
        if int(stored["candidate_index"]) != args.candidate:
            raise ValueError("initial certificate profile mismatch")
        initial = tuple(map(int, stored["placement_trits"]))
    result = solve(
        args.candidate,
        args.seconds,
        args.workers,
        args.seed,
        args.target_index,
        initial,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact XOR lift of the first h=2 profile-zero LP(333) survivor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
if str(SEARCH) not in sys.path:
    sys.path.insert(0, str(SEARCH))

import search_lp333_order3_cp_sat as quotient_search  # noqa: E402
from verify_lp333_order3_char37_transfer import PROFILES  # noqa: E402
from verify_lp333_order3_labeled_jet import CLASSES  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    audit_profile_witness,
    profiles_from_ids,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
    affine_upper_system,
    words_from_profile_trits,
)


TARGET = (2, -2, -2, 2)
PROFILE_IDS_A = (2, 5, 8, 1, 7, 9, 5, 8, 5, 5, 5, 7)
PROFILE_IDS_B = (2, 5, 3, 6, 5, 5, 5, 4, 7, 5, 4, 7)


def add_profile_and_hensel_constraints(
    bundle: quotient_search.Order3Model,
) -> tuple[tuple[cp_model.IntVar, ...], tuple[cp_model.IntVar, ...]]:
    profiles = profiles_from_ids(PROFILE_IDS_A, PROFILE_IDS_B)
    model = bundle.model

    for channel, nodes in enumerate((bundle.a_nodes, bundle.b_nodes)):
        for class_index in range(12):
            high_weight = (
                class_index % 2 == 0
                if channel == 0
                else class_index % 2 == 1
            )
            for residue, normalized_count in enumerate(
                profiles[channel][class_index]
            ):
                actual_count = (
                    3 - normalized_count if high_weight else normalized_count
                )
                model.add(
                    sum(
                        nodes[residue + 3 * quotient][class_index + 1]
                        for quotient in range(3)
                    )
                    == actual_count
                )

    coordinates = active_trit_coordinates(profiles)
    affine = affine_upper_system(profiles)
    if coordinates != affine.coordinates or not affine.consistent:
        raise AssertionError("the fixed profile lost its affine first digit")
    trits = tuple(
        model.new_int_var(0, 2, f"profile_trit_{index}")
        for index in range(len(coordinates))
    )
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    local_quotients = []
    for channel, class_index, residue in coordinates:
        nodes = (bundle.a_nodes, bundle.b_nodes)[channel]
        high_weight = (
            class_index % 2 == 0 if channel == 0 else class_index % 2 == 1
        )
        bit_q1 = nodes[residue + 3][class_index + 1]
        bit_q2 = nodes[residue + 6][class_index + 1]
        normalized_q1 = 1 - bit_q1 if high_weight else bit_q1
        normalized_q2 = 1 - bit_q2 if high_weight else bit_q2
        index = coordinate_index[(channel, class_index, residue)]
        quotient = model.new_int_var(0, 1, f"local_trit_q_{index}")
        model.add(
            2 * normalized_q1 + normalized_q2
            == trits[index] + 3 * quotient
        )
        local_quotients.append(quotient)

    affine_quotients = []
    for equation, row in enumerate(affine.rref_rows):
        quotient = model.new_int_var(-100, 100, f"hensel_q_{equation}")
        model.add(
            sum(row[index] * trits[index] for index in range(len(trits)))
            == row[-1] + 3 * quotient
        )
        affine_quotients.append(quotient)

    first_digit = audit_profile_witness(
        TARGET, PROFILE_IDS_A, PROFILE_IDS_B, 668
    )
    canonical = first_digit["canonical_solution"]
    if canonical is None or len(canonical) != len(trits):
        raise AssertionError("the fixed profile lost its canonical hint")
    hinted_words = words_from_profile_trits(profiles, canonical)
    for variable, value in zip(trits, canonical):
        model.add_hint(variable, int(value))
    for channel, nodes in enumerate((bundle.a_nodes, bundle.b_nodes)):
        for class_index in range(12):
            for row in range(9):
                model.add_hint(
                    nodes[row][class_index + 1],
                    hinted_words[channel][class_index][row],
                )

    model.add_decision_strategy(
        bundle.primary_variables,
        cp_model.CHOOSE_FIRST,
        cp_model.SELECT_MIN_VALUE,
    )
    return trits, tuple((*local_quotients, *affine_quotients))


def expand_sequences(
    solver: cp_model.CpSolver, bundle: quotient_search.Order3Model
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    class_of = {
        value: class_index
        for class_index, part in enumerate(CLASSES)
        for value in part
    }
    sequences = []
    for nodes in (bundle.a_nodes, bundle.b_nodes):
        sequence = []
        for index in range(333):
            row = index % 9
            column = index % 37
            part = 0 if column == 0 else class_of[column] + 1
            node = nodes[row][part]
            plus = int(node) if type(node) is int else solver.value(node)
            sequence.append(1 if plus else -1)
        sequences.append(tuple(sequence))
    return tuple(sequences)  # type: ignore[return-value]


def exact_replay(a: tuple[int, ...], b: tuple[int, ...]) -> dict[str, object]:
    if len(a) != 333 or len(b) != 333:
        raise AssertionError("decoded sequences have the wrong length")
    if set(a) != {-1, 1} or set(b) != {-1, 1}:
        raise AssertionError("decoded sequences are not binary signs")
    if sum(a) != 1 or sum(b) != 1:
        raise AssertionError("decoded sequences have the wrong sums")
    correlations = []
    for lag in range(167):
        value = sum(
            a[index] * a[(index + lag) % 333]
            + b[index] * b[(index + lag) % 333]
            for index in range(333)
        )
        correlations.append(value)
    if correlations[0] != 666 or any(value != -2 for value in correlations[1:]):
        raise AssertionError("decoded sequences fail an exact LP(333) correlation")
    return {
        "sum_a": sum(a),
        "sum_b": sum(b),
        "correlations_checked": len(correlations),
        "zero_lag": correlations[0],
        "nonzero_lag_value": -2,
        "valid": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-memory-mb", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument(
        "--row-sum-index",
        type=int,
        help="fix one global row-sum catalog entry instead of joining all 72",
    )
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.time_limit <= 0 or args.workers <= 0:
        raise SystemExit("time limit and workers must be positive")
    if args.row_sum_index is not None:
        catalog = quotient_search.row_sum_catalog()
        if not 0 <= args.row_sum_index < len(catalog):
            raise SystemExit("--row-sum-index lies outside the catalog")
        from verify_lp333_order3_profile_zero_gate import aggregate_shard_target

        actual_target = aggregate_shard_target(catalog[args.row_sum_index])
        if actual_target != TARGET:
            raise SystemExit(
                "the selected row-sum entry belongs to target "
                f"{actual_target}, not {TARGET}"
            )
    bundle = quotient_search.build_model(
        row_sum_index=args.row_sum_index,
        c6_symmetry=False,
        c2_symmetry=False,
    )
    trits, extra_quotients = add_profile_and_hensel_constraints(bundle)
    proto = bundle.model.proto
    print(
        "model_counts="
        + json.dumps(
            {
                **bundle.exact_counts(),
                "profile_trits": len(trits),
                "extra_quotients": len(extra_quotients),
                "final_variables": len(proto.variables),
                "final_constraints": len(proto.constraints),
                "row_sum_index": args.row_sum_index,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log
    status = solver.solve(bundle.model)
    print(f"status={solver.status_name(status)}")
    print(f"wall_time_seconds={solver.wall_time}")
    print(f"branches={solver.num_branches}")
    print(f"conflicts={solver.num_conflicts}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print("NO CLAIM: the bounded exact lift returned no assignment")
        raise SystemExit(2 if status == cp_model.UNKNOWN else 1)

    a, b = expand_sequences(solver, bundle)
    replay = exact_replay(a, b)
    payload = {
        "status": "verified_lp333",
        "target": TARGET,
        "profiles_a": PROFILE_IDS_A,
        "profiles_b": PROFILE_IDS_B,
        "a": a,
        "b": b,
        "verification": replay,
    }
    print("replay=" + json.dumps(replay, sort_keys=True))
    print("PASS: exact LP(333) independently replayed")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"candidate={args.output}")


if __name__ == "__main__":
    main()

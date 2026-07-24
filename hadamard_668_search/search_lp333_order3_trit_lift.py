#!/usr/bin/env python3
"""Bounded CP-SAT lift of the pinned primitive-nine residue profiles."""

from __future__ import annotations

import argparse

from ortools.sat.python import cp_model

from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_AGGREGATE,
    validate_labelled_certificate,
)
from verify_lp333_order3_trit_lift import (
    PINNED_PROFILES,
    build_trit_lift_model,
    normalized_masks_from_solver,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--time-limit", type=float, default=10.0)
    parser.add_argument("--workers", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.time_limit <= 0:
        raise SystemExit("--time-limit must be positive")
    if args.workers <= 0:
        raise SystemExit("--workers must be positive")
    bundle = build_trit_lift_model(
        LABELLED_SURVIVOR_AGGREGATE,
        PINNED_PROFILES,
    )
    print(f"model_counts={bundle.exact_counts()}")
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    status = solver.solve(bundle.model)
    print(f"solver_status={solver.status_name(status)}")
    print(f"wall_time_seconds={solver.wall_time}")
    print(f"branches={solver.num_branches}")
    print(f"conflicts={solver.num_conflicts}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print("NO CLAIM: no certificate was returned")
        raise SystemExit(2)
    masks_a, masks_b = normalized_masks_from_solver(bundle, solver)
    replay = validate_labelled_certificate(
        LABELLED_SURVIVOR_AGGREGATE,
        masks_a,
        masks_b,
    )
    print(f"masks_a={masks_a}")
    print(f"masks_b={masks_b}")
    print(f"replay={replay}")
    print("PASS: solver assignment independently replayed")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compact CP-SAT model for digit-3, digit-4, or exact phase equations.

The model uses the exact identity from ``audit_digit3_carry.py``.  It has
one canonical exponent L and one Boolean indicator 1[L=2] per distinct
affine phase form.  It does not introduce the three redundant root
coordinates used by the generic prefix model.

Every solver witness is replayed independently through the exact
Eisenstein equations.  UNKNOWN is never interpreted as exclusion.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HIGHER_DIGITS))
sys.path.insert(0, str(SEARCH_ROOT))

import audit_digit3_carry as carry  # noqa: E402
import verify_full_second_digit_witness as full_witness  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402


def expression_bounds(
    constant: int,
    terms: list[tuple[int, cp_model.IntVar]],
) -> tuple[int, int]:
    lower = int(constant)
    upper = int(constant)
    for coefficient, variable in terms:
        domain_lower = int(variable.proto.domain[0])
        domain_upper = int(variable.proto.domain[-1])
        choices = (
            int(coefficient) * domain_lower,
            int(coefficient) * domain_upper,
        )
        lower += min(choices)
        upper += max(choices)
    return lower, upper


def add_congruence(
    model: cp_model.CpModel,
    constant: int,
    terms: list[tuple[int, cp_model.IntVar]],
    modulus: int,
    name: str,
) -> None:
    lower, upper = expression_bounds(constant, terms)
    quotient = model.new_int_var(
        lower // modulus - 1,
        upper // modulus + 1,
        f"{name}_quotient",
    )
    model.add(
        int(constant)
        + sum(
            int(coefficient) * variable
            for coefficient, variable in terms
        )
        == modulus * quotient
    )


def build_model(candidate_index: int, mode: str):
    profiles, origin, basis, rows = carry.effective_rows(candidate_index)
    model = cp_model.CpModel()
    affine = tuple(
        model.new_int_var(0, 2, f"affine_{index}")
        for index in range(36)
    )

    all_forms = tuple(
        sorted(
            {
                form
                for _, grouped in rows
                for form, _ in grouped
            }
        )
    )
    form_variables = {}
    for form_index, (constant, slopes) in enumerate(all_forms):
        exponent = model.new_int_var(0, 2, f"L_{form_index}")
        indicator_two = model.new_bool_var(f"Z_{form_index}")
        terms = [
            (int(slope), affine[index])
            for index, slope in enumerate(slopes)
            if int(slope)
        ]
        lower, upper = expression_bounds(int(constant), terms)
        quotient = model.new_int_var(
            lower // 3 - 1,
            upper // 3 + 1,
            f"L_{form_index}_quotient",
        )
        model.add(
            int(constant)
            + sum(
                coefficient * variable
                for coefficient, variable in terms
            )
            == exponent + 3 * quotient
        )
        model.add_allowed_assignments(
            (exponent, indicator_two),
            ((0, 0), (1, 0), (2, 1)),
        )
        form_variables[(constant, slopes)] = (exponent, indicator_two)

    # E0(origin), row 0, is exactly zero.  Every other displayed row is a
    # genuine exact equation at digit 3 or above, including E1(origin).
    for row_index in range(1, 20):
        constant_at_zero, grouped = rows[row_index]
        a_terms = [
            (-multiplicity, form_variables[form][0])
            for form, multiplicity in grouped
        ]
        q_terms = [
            (-multiplicity, form_variables[form][1])
            for form, multiplicity in grouped
        ]
        if mode == "digit3":
            add_congruence(
                model,
                constant_at_zero,
                a_terms,
                9,
                f"row_{row_index}_A",
            )
            add_congruence(
                model,
                constant_at_zero // 3,
                q_terms,
                3,
                f"row_{row_index}_Q",
            )
        elif mode == "digit4":
            add_congruence(
                model,
                constant_at_zero,
                a_terms,
                9,
                f"row_{row_index}_A",
            )
            add_congruence(
                model,
                constant_at_zero // 3,
                q_terms,
                9,
                f"row_{row_index}_Q",
            )
        elif mode == "exact":
            model.add(
                constant_at_zero
                + sum(
                    coefficient * variable
                    for coefficient, variable in a_terms
                )
                == 0
            )
            model.add(
                constant_at_zero // 3
                + sum(
                    coefficient * variable
                    for coefficient, variable in q_terms
                )
                == 0
            )
        else:
            raise ValueError("mode must be digit3, digit4, or exact")

    statistics = {
        "mode": mode,
        "affine_variables": len(affine),
        "unique_effective_phase_forms": len(all_forms),
        "model_variables": len(model.proto.variables),
        "model_constraints": len(model.proto.constraints),
        "linear_constraints": sum(
            constraint.HasField("linear")
            for constraint in model.proto.constraints
        ),
        "table_constraints": sum(
            constraint.HasField("table")
            for constraint in model.proto.constraints
        ),
    }
    return model, affine, profiles, origin, basis, rows, statistics


def solve(
    candidate_index: int,
    mode: str,
    seconds: float,
    workers: int,
    seed: int,
    initial_affine: tuple[int, ...] | None,
) -> dict[str, object]:
    started = time.monotonic()
    model, affine, profiles, origin, basis, rows, construction = build_model(
        candidate_index, mode
    )
    if initial_affine is not None:
        if len(initial_affine) != 36:
            raise ValueError("the initial affine point must have 36 trits")
        for variable, value in zip(affine, initial_affine):
            model.add_hint(variable, int(value))
    built = time.monotonic()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(seconds)
    solver.parameters.num_search_workers = int(workers)
    solver.parameters.random_seed = int(seed)
    solver.parameters.cp_model_presolve = True
    status = solver.solve(model)
    finished = time.monotonic()

    candidate = second.CANDIDATES[candidate_index]
    result: dict[str, object] = {
        "schema": "lp333-order3-carry-cp-sat-v1",
        "scope": (
            "Bounded exact witness search in the compact A,Q coordinate "
            "model. UNKNOWN is not an exclusion."
        ),
        "label": candidate[0],
        "candidate_index": candidate_index,
        "status": solver.status_name(status),
        "construction": construction,
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
        point = tuple(int(solver.value(variable)) for variable in affine)
        placement = second.lift_affine_point(origin, basis, point)
        exact_values = second.displayed_values(profiles, placement)
        digits = tuple(
            second.lambda_digits(value, 10) for value in exact_values
        )
        required_digit = {
            "digit3": 3,
            "digit4": 4,
            "exact": 8,
        }[mode]
        if mode == "exact":
            if any(value != (0, 0) for value in exact_values):
                raise AssertionError("an exact CP-SAT witness was not exact")
        elif any(
            any(row[: required_digit + 1]) for row in digits
        ):
            raise AssertionError("the CP-SAT prefix failed exact replay")
        masks_a, masks_b = second.masks_from_trits(profiles, placement)
        columns = full_witness.expand_columns(masks_a, masks_b)
        proper_fixed = tuple(
            full_witness.fixed_by_multiplier(columns, multiplier)
            for multiplier in full_witness.SUPERGROUP_GENERATORS
        )
        statistics = tuple(
            carry.row_statistics(row, point) for row in rows
        )
        result.update(
            {
                "affine_coordinates": point,
                "affine_coordinates_sha256": carry.compact_hash(point),
                "placement_trits": placement,
                "placement_trits_sha256": carry.compact_hash(placement),
                "displayed_exact_values": exact_values,
                "lambda_digits_through_9": digits,
                "a_values": tuple(a for a, _ in statistics),
                "q_values": tuple(q for _, q in statistics),
                "proper_supergroup_fixed": proper_fixed,
                "next_digit_nonzero_rows": (
                    0
                    if mode == "exact"
                    else sum(
                        row[required_digit + 1] != 0 for row in digits
                    )
                ),
            }
        )
    result["semantic_sha256"] = carry.compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=1, choices=range(5))
    parser.add_argument(
        "--mode",
        choices=("digit3", "digit4", "exact"),
        default="digit3",
    )
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--initial-certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    initial = None
    if args.initial_certificate is not None:
        stored = json.loads(args.initial_certificate.read_text())
        if int(stored["candidate_index"]) != args.candidate:
            raise ValueError("initial certificate profile mismatch")
        initial = tuple(map(int, stored["affine_coordinates"]))
    result = solve(
        args.candidate,
        args.mode,
        args.seconds,
        args.workers,
        args.seed,
        initial,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()

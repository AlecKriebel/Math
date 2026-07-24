#!/usr/bin/env python3
"""Bounded CP-SAT search for exact consecutive lambda-adic prefixes.

This uses the integral lattice criterion implemented and independently
replayed in ``solve_lambda_prefix_sat.py``.  CP-SAT is only a witness finder:
every reported placement is checked by exact Eisenstein arithmetic.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import solve_lambda_prefix_sat as prefix  # noqa: E402


def quotient_bounds(terms: list[tuple[int, cp_model.IntVar]], constant: int):
    minimum = constant
    maximum = constant
    for coefficient, variable in terms:
        lower = int(variable.proto.domain[0])
        upper = int(variable.proto.domain[-1])
        values = (coefficient * lower, coefficient * upper)
        minimum += min(values)
        maximum += max(values)
    return minimum, maximum


def add_divisibility(
    model: cp_model.CpModel,
    terms: list[tuple[int, cp_model.IntVar]],
    constant: int,
    modulus: int,
    name: str,
) -> None:
    minimum, maximum = quotient_bounds(terms, constant)
    quotient = model.new_int_var(
        minimum // modulus - 1,
        maximum // modulus + 1,
        f"{name}_quotient",
    )
    model.add(
        constant + sum(coefficient * variable for coefficient, variable in terms)
        == modulus * quotient
    )


def build_model(candidate_index: int, maximum_digit: int):
    _, _, _, identifiers_a, identifiers_b = prefix.second.CANDIDATES[
        candidate_index
    ]
    profiles = prefix.second.profiles_from_ids(
        identifiers_a, identifiers_b
    )
    first_equations = prefix.second.first_digit_equations(profiles)
    origin, basis = prefix.second.affine_parameterization(
        first_equations, 54
    )
    rows = prefix.grouped_term_rows(profiles)
    coordinate_modulus, sum_modulus = prefix.prefix_lattice(maximum_digit)

    model = cp_model.CpModel()
    affine = tuple(
        model.new_int_var(0, 2, f"affine_{index}")
        for index in range(36)
    )
    placement = []
    for row in range(54):
        variable = model.new_int_var(0, 2, f"placement_{row}")
        coefficients = tuple(basis[column][row] for column in range(36))
        terms = [
            (int(coefficient), affine[column])
            for column, coefficient in enumerate(coefficients)
            if int(coefficient)
        ]
        minimum, maximum = quotient_bounds(terms, int(origin[row]))
        quotient = model.new_int_var(
            minimum // 3 - 1,
            maximum // 3 + 1,
            f"placement_{row}_quotient",
        )
        model.add(
            int(origin[row])
            + sum(coefficient * source for coefficient, source in terms)
            == variable + 3 * quotient
        )
        placement.append(variable)
    placement = tuple(placement)

    form_cache = {}
    for _, grouped in rows:
        for (constant, coefficients), _ in grouped:
            key = (constant, coefficients)
            if key in form_cache:
                continue
            exponent = model.new_int_var(
                0, 2, f"exponent_{len(form_cache)}"
            )
            terms = [
                (int(coefficient), placement[int(variable)])
                for variable, coefficient in coefficients
            ]
            minimum, maximum = quotient_bounds(terms, int(constant))
            quotient = model.new_int_var(
                minimum // 3 - 1,
                maximum // 3 + 1,
                f"exponent_{len(form_cache)}_quotient",
            )
            model.add(
                int(constant)
                + sum(coefficient * source for coefficient, source in terms)
                == exponent + 3 * quotient
            )
            root_a = model.new_int_var(
                -1, 1, f"root_a_{len(form_cache)}"
            )
            root_b = model.new_int_var(
                -1, 1, f"root_b_{len(form_cache)}"
            )
            root_sum = model.new_int_var(
                -2, 1, f"root_sum_{len(form_cache)}"
            )
            model.add_allowed_assignments(
                (exponent, root_a, root_b, root_sum),
                (
                    (0, 1, 0, 1),
                    (1, 0, 1, 1),
                    (2, -1, -1, -2),
                ),
            )
            form_cache[key] = (root_a, root_b, root_sum)

    for row_index, (target, grouped) in enumerate(rows):
        a_terms = []
        b_terms = []
        sum_terms = []
        for form, multiplicity in grouped:
            root_a, root_b, root_sum = form_cache[form]
            a_terms.append((multiplicity, root_a))
            b_terms.append((multiplicity, root_b))
            sum_terms.append((multiplicity, root_sum))
        if coordinate_modulus > 1:
            add_divisibility(
                model, a_terms, -target, coordinate_modulus,
                f"row_{row_index}_a",
            )
            add_divisibility(
                model, b_terms, 0, coordinate_modulus,
                f"row_{row_index}_b",
            )
        if sum_modulus is not None:
            add_divisibility(
                model, sum_terms, -target, sum_modulus,
                f"row_{row_index}_sum",
            )

    statistics = {
        "maximum_zero_digit": maximum_digit,
        "coordinate_modulus": coordinate_modulus,
        "sum_modulus": 0 if sum_modulus is None else sum_modulus,
        "unique_affine_phase_forms": len(form_cache),
        "grouped_phase_terms": sum(len(grouped) for _, grouped in rows),
        "model_variables": len(model.proto.variables),
        "model_constraints": len(model.proto.constraints),
    }
    return model, affine, origin, basis, profiles, statistics


def solve(
    candidate_index: int,
    maximum_digit: int,
    seconds: float,
    workers: int,
    seed: int,
    initial_affine: tuple[int, ...] | None,
) -> dict[str, object]:
    started = time.monotonic()
    model, affine, origin, basis, profiles, construction = build_model(
        candidate_index, maximum_digit
    )
    if initial_affine is not None:
        if len(initial_affine) != 36:
            raise ValueError("the initial affine point needs 36 trits")
        for variable, value in zip(affine, initial_affine):
            model.add_hint(variable, int(value))
    built = time.monotonic()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.cp_model_presolve = True
    status = solver.solve(model)
    finished = time.monotonic()
    label, partition, target, identifiers_a, identifiers_b = (
        prefix.second.CANDIDATES[candidate_index]
    )
    result: dict[str, object] = {
        "schema": "lp333-order3-lambda-prefix-cp-sat-v1",
        "scope": (
            "A bounded exact lambda-prefix witness search; not an exact "
            "phase solution, LP(333), Legendre pair, or H(668)."
        ),
        "label": label,
        "partition": partition,
        "target": target,
        "profile_ids_a": identifiers_a,
        "profile_ids_b": identifiers_b,
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
        coordinates = tuple(int(solver.value(value)) for value in affine)
        placement_trits = prefix.second.lift_affine_point(
            origin, basis, coordinates
        )
        displayed = prefix.second.displayed_values(
            profiles, placement_trits
        )
        digits = tuple(
            prefix.second.lambda_digits(value, 12)
            for value in displayed
        )
        if any(
            any(row[index] for index in range(maximum_digit + 1))
            for row in digits
        ):
            raise AssertionError("CP-SAT prefix failed exact replay")
        masks_a, masks_b = prefix.second.masks_from_trits(
            profiles, placement_trits
        )
        result.update({
            "affine_coordinates": coordinates,
            "affine_coordinates_sha256": prefix.compact_hash(coordinates),
            "placement_trits": placement_trits,
            "placement_trits_sha256": prefix.compact_hash(placement_trits),
            "masks_a": masks_a,
            "masks_b": masks_b,
            "displayed_exact_values": displayed,
            "displayed_lambda_digits_through_11": digits,
            "next_digit_residual_count": sum(
                int(row[maximum_digit + 1] != 0) for row in digits
            ),
        })
    result["semantic_sha256"] = prefix.compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=0, choices=range(5))
    parser.add_argument("--maximum-digit", type=int, default=3)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--initial-certificate", type=Path)
    parser.add_argument("--initial-affine")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    initial = None
    if args.initial_certificate is not None:
        stored = json.loads(args.initial_certificate.read_text())
        if int(stored["candidate_index"]) != args.candidate:
            raise ValueError("the initial certificate profile disagrees")
        initial = tuple(map(int, stored["affine_coordinates"]))
    if args.initial_affine is not None:
        if initial is not None:
            raise ValueError("provide only one initial-point source")
        initial = tuple(
            int(value) for value in args.initial_affine.split(",")
        )
    result = solve(
        args.candidate,
        args.maximum_digit,
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

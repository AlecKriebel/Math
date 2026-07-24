#!/usr/bin/env python3
"""Exact SAT search for consecutive lambda-adic placement digits.

For one of the five exact h=2 profiles, every displayed phase equation is
an Eisenstein integer

    F = a + b*omega = sum_t sigma_t*omega**L_t(x) - target,

where x consists of 54 placement trits and each L_t is affine over F_3.
Vanishing through lambda digit d has a particularly small integral test.
If k=d+1 digits vanish, then

    k=2m:   a == b == 0 (mod 3**m),
    k=2m+1: a == b == 0 (mod 3**m)
             and a+b == 0 (mod 3**(m+1)).

The CNF below encodes these congruences directly.  It does not expand the
quadratic second digit and it does not mistake a modular prefix for an exact
Legendre pair.  Every SAT assignment is independently replayed through the
exact Eisenstein equations.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import threading
import time
from typing import Sequence


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402


Trit = tuple[int, int, int]
ROOT_A = (1, 0, -1)
ROOT_B = (0, 1, -1)
ROOT_SUM = (1, 1, -2)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


class PrefixCnf:
    """Small exact-one and deterministic-transition CNF builder."""

    def __init__(self) -> None:
        self.next_variable = 1
        self.clauses: list[list[int]] = []
        self.one_hot_wires = 0
        self.transition_steps = 0
        self.affine_forms = 0
        self.ternary_gates = 0
        self._constants: dict[int, Trit] = {}

    def new_variable(self) -> int:
        result = self.next_variable
        self.next_variable += 1
        return result

    def new_one_hot(self, size: int) -> tuple[int, ...]:
        result = tuple(self.new_variable() for _ in range(size))
        self.clauses.append(list(result))
        for left in range(size):
            for right in range(left + 1, size):
                self.clauses.append([-result[left], -result[right]])
        self.one_hot_wires += 1
        return result

    def affine_trit(
        self,
        inputs: Sequence[Trit],
        constant: int,
        coefficients: Sequence[tuple[int, int]],
    ) -> Trit:
        output = self.new_one_hot(3)
        support = tuple(
            (int(variable), int(coefficient) % 3)
            for variable, coefficient in coefficients
            if int(coefficient) % 3
        )
        if not support:
            self.clauses.append([output[int(constant) % 3]])
        else:
            assignments = [[]]
            for variable, _ in support:
                assignments = [
                    (*prefix, value)
                    for prefix in assignments
                    for value in range(3)
                ]
            for values in assignments:
                exponent = int(constant)
                antecedent = []
                for (variable, coefficient), value in zip(
                    support, values
                ):
                    exponent += coefficient * value
                    antecedent.append(-inputs[variable][value])
                self.clauses.append(
                    [*antecedent, output[exponent % 3]]
                )
        self.affine_forms += 1
        return output

    def constant_trit(self, value: int) -> Trit:
        value %= 3
        if value not in self._constants:
            wire = self.new_one_hot(3)
            self.clauses.append([wire[value]])
            self._constants[value] = wire
        return self._constants[value]

    @staticmethod
    def scaled_view(wire: Trit, coefficient: int) -> Trit:
        coefficient %= 3
        if coefficient == 1:
            return wire
        if coefficient == 2:
            return wire[0], wire[2], wire[1]
        raise ValueError("a zero coefficient has no nonconstant view")

    def add_trits(self, left: Trit, right: Trit) -> Trit:
        output = self.new_one_hot(3)
        for left_value in range(3):
            for right_value in range(3):
                self.clauses.append([
                    -left[left_value],
                    -right[right_value],
                    output[(left_value + right_value) % 3],
                ])
        self.ternary_gates += 1
        return output

    def affine_sum_trit(
        self,
        inputs: Sequence[Trit],
        constant: int,
        coefficients: Sequence[int],
    ) -> Trit:
        if len(inputs) != len(coefficients):
            raise ValueError("affine-sum data lengths disagree")
        accumulator = self.constant_trit(constant)
        for wire, coefficient in zip(inputs, coefficients):
            if int(coefficient) % 3:
                accumulator = self.add_trits(
                    accumulator,
                    self.scaled_view(wire, coefficient),
                )
        return accumulator

    def modular_sum(
        self,
        exponent_wires: Sequence[Trit],
        weights: Sequence[Sequence[int]],
        initial: int,
        modulus: int,
    ) -> tuple[int, ...]:
        if len(exponent_wires) != len(weights):
            raise ValueError("modular-sum data lengths disagree")
        current_constant = int(initial) % modulus
        current_wire: tuple[int, ...] | None = None
        for exponent, contributions in zip(exponent_wires, weights):
            if len(contributions) != 3:
                raise ValueError("a root contribution needs three values")
            following = self.new_one_hot(modulus)
            if current_wire is None:
                for root in range(3):
                    destination = (
                        current_constant + int(contributions[root])
                    ) % modulus
                    self.clauses.append(
                        [-exponent[root], following[destination]]
                    )
            else:
                for state in range(modulus):
                    for root in range(3):
                        destination = (
                            state + int(contributions[root])
                        ) % modulus
                        self.clauses.append([
                            -current_wire[state],
                            -exponent[root],
                            following[destination],
                        ])
            current_wire = following
            self.transition_steps += 1
        if current_wire is None:
            if current_constant:
                self.clauses.append([])
            dummy = self.new_one_hot(modulus)
            self.clauses.append([dummy[0]])
            return dummy
        self.clauses.append([current_wire[0]])
        return current_wire


def grouped_term_rows(
    profiles,
) -> tuple[
    tuple[
        int,
        tuple[
            tuple[
                tuple[int, tuple[tuple[int, int], ...]],
                int,
            ],
            ...,
        ],
    ],
    ...,
]:
    """Return target and signed multiplicity of each distinct phase form."""

    rows = []
    entries = second.phase_entries(profiles)
    for component, lag in second.displayed_specifications():
        terms, target = second.coefficient_terms(entries, component, lag)
        grouped = Counter(
            (
                int(term.constant) % 3,
                tuple(
                    (int(variable), int(coefficient) % 3)
                    for variable, coefficient in term.coefficients
                    if int(coefficient) % 3
                ),
            )
            for term in terms
            if term.sign > 0
        )
        grouped.subtract(
            (
                int(term.constant) % 3,
                tuple(
                    (int(variable), int(coefficient) % 3)
                    for variable, coefficient in term.coefficients
                    if int(coefficient) % 3
                ),
            )
            for term in terms
            if term.sign < 0
        )
        rows.append(
            (
                int(target),
                tuple(
                    (form, int(multiplicity))
                    for form, multiplicity in sorted(grouped.items())
                    if multiplicity
                ),
            )
        )
    return tuple(rows)


def prefix_lattice(maximum_digit: int) -> tuple[int, int | None]:
    """Return coordinate modulus and optional a+b modulus."""

    if maximum_digit < 0:
        raise ValueError("the maximum digit must be nonnegative")
    digits = maximum_digit + 1
    half = digits // 2
    coordinate_modulus = 3**half
    sum_modulus = 3 ** (half + 1) if digits % 2 else None
    return coordinate_modulus, sum_modulus


def build_prefix_cnf(
    candidate_index: int,
    maximum_digit: int,
) -> tuple[
    PrefixCnf,
    tuple[Trit, ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
    dict[str, int],
]:
    _, _, _, identifiers_a, identifiers_b = second.CANDIDATES[
        candidate_index
    ]
    profiles = second.profiles_from_ids(identifiers_a, identifiers_b)
    first_equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(first_equations, 54)
    rows = grouped_term_rows(profiles)
    coordinate_modulus, sum_modulus = prefix_lattice(maximum_digit)
    circuit = PrefixCnf()
    inputs = tuple(circuit.new_one_hot(3) for _ in range(36))
    placement_wires = tuple(
        circuit.affine_sum_trit(
            inputs,
            origin[row],
            tuple(basis[column][row] for column in range(36)),
        )
        for row in range(54)
    )
    form_cache: dict[
        tuple[int, tuple[tuple[int, int], ...]], Trit
    ] = {}

    for target, grouped in rows:
        exponent_wires = []
        multiplicities = []
        for (constant, coefficients), multiplicity in grouped:
            key = (constant, coefficients)
            if key not in form_cache:
                form_cache[key] = circuit.affine_trit(
                    placement_wires, constant, coefficients
                )
            exponent_wires.append(form_cache[key])
            multiplicities.append(multiplicity)

        if coordinate_modulus > 1:
            circuit.modular_sum(
                exponent_wires,
                tuple(
                    tuple(multiplicity * value for value in ROOT_A)
                    for multiplicity in multiplicities
                ),
                -target,
                coordinate_modulus,
            )
            circuit.modular_sum(
                exponent_wires,
                tuple(
                    tuple(multiplicity * value for value in ROOT_B)
                    for multiplicity in multiplicities
                ),
                0,
                coordinate_modulus,
            )
        if sum_modulus is not None:
            circuit.modular_sum(
                exponent_wires,
                tuple(
                    tuple(multiplicity * value for value in ROOT_SUM)
                    for multiplicity in multiplicities
                ),
                -target,
                sum_modulus,
            )

    statistics = {
        "maximum_zero_digit": maximum_digit,
        "coordinate_modulus": coordinate_modulus,
        "sum_modulus": 0 if sum_modulus is None else sum_modulus,
        "unique_affine_phase_forms": len(form_cache),
        "grouped_phase_terms": sum(len(grouped) for _, grouped in rows),
        "boolean_variables": circuit.next_variable - 1,
        "clauses": len(circuit.clauses),
        "one_hot_wires": circuit.one_hot_wires,
        "transition_steps": circuit.transition_steps,
        "ternary_gates": circuit.ternary_gates,
    }
    return circuit, inputs, origin, basis, profiles, statistics


def decode_inputs(model: Sequence[int], inputs: Sequence[Trit]) -> tuple[int, ...]:
    positive = {literal for literal in model if literal > 0}
    result = []
    for trit in inputs:
        values = tuple(
            value for value, literal in enumerate(trit)
            if literal in positive
        )
        if len(values) != 1:
            raise AssertionError("a SAT input trit is not one-hot")
        result.append(values[0])
    return tuple(result)


def solve_prefix(
    candidate_index: int,
    maximum_digit: int,
    solver_name: str,
    time_limit: float | None,
) -> dict[str, object]:
    try:
        from pysat.solvers import Solver
    except ImportError as error:
        raise SystemExit(
            "Python-SAT is required; use the pinned local research "
            "environment."
        ) from error

    started = time.monotonic()
    circuit, inputs, origin, basis, profiles, construction = build_prefix_cnf(
        candidate_index, maximum_digit
    )
    built = time.monotonic()
    timer = None
    with Solver(
        name=solver_name,
        bootstrap_with=circuit.clauses,
    ) as solver:
        if time_limit is not None:
            timer = threading.Timer(time_limit, solver.interrupt)
            timer.start()
            satisfiable = solver.solve_limited(expect_interrupt=True)
        else:
            satisfiable = solver.solve()
        if timer is not None:
            timer.cancel()
        model = solver.get_model() if satisfiable is True else None
        solver_statistics = solver.accum_stats()
    solved = time.monotonic()

    label, partition, target, identifiers_a, identifiers_b = (
        second.CANDIDATES[candidate_index]
    )
    result: dict[str, object] = {
        "schema": "lp333-order3-lambda-prefix-sat-v1",
        "scope": (
            "A bounded exact lambda-prefix SAT audit on one h=2 profile; "
            "not an exact phase solution, LP(333), Legendre pair, or H(668)."
        ),
        "label": label,
        "partition": partition,
        "target": target,
        "profile_ids_a": identifiers_a,
        "profile_ids_b": identifiers_b,
        "status": (
            "SAT"
            if satisfiable is True
            else "UNSAT"
            if satisfiable is False
            else "UNKNOWN"
        ),
        "construction": construction,
        "solver": {
            "name": solver_name,
            "time_limit_seconds": time_limit,
            "build_seconds": built - started,
            "solve_seconds": solved - built,
            "statistics": solver_statistics,
        },
    }
    if model is not None:
        affine_coordinates = decode_inputs(model, inputs)
        placement_trits = second.lift_affine_point(
            origin, basis, affine_coordinates
        )
        displayed = second.displayed_values(profiles, placement_trits)
        prefixes = tuple(
            second.lambda_digits(value, 12) for value in displayed
        )
        if any(
            any(prefix[index] for index in range(maximum_digit + 1))
            for prefix in prefixes
        ):
            raise AssertionError("SAT prefix failed exact replay")
        masks_a, masks_b = second.masks_from_trits(
            profiles, placement_trits
        )
        result.update({
            "affine_coordinates": affine_coordinates,
            "affine_coordinates_sha256": compact_hash(affine_coordinates),
            "placement_trits": placement_trits,
            "placement_trits_sha256": compact_hash(placement_trits),
            "masks_a": masks_a,
            "masks_b": masks_b,
            "displayed_exact_values": displayed,
            "displayed_lambda_digits_through_11": prefixes,
            "next_digit_residual_count": sum(
                int(prefix[maximum_digit + 1] != 0)
                for prefix in prefixes
            ),
        })
    result["semantic_sha256"] = compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=0, choices=range(5))
    parser.add_argument("--maximum-digit", type=int, default=3)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--time-limit", type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = solve_prefix(
        args.candidate,
        args.maximum_digit,
        args.solver,
        args.time_limit,
    )
    payload = json.dumps(certificate, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()

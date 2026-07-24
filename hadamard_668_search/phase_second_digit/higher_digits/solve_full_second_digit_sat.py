#!/usr/bin/env python3
"""Find a full 18-equation second-digit witness with a local SAT solver.

This is a bounded witness search, not a counting proof.  Each F_3 variable
and each shared quadratic monomial is encoded one-hot.  Ternary addition and
multiplication are exact truth-table gates, after which the eighteen
quadratic equations are asserted by chained mod-three adders.

The script requires Python-SAT.  The resulting 36- and 54-trit witnesses
are independently replayed by exact Eisenstein arithmetic before printing.

This is retained as the first stage of the higher-digit audit.  A witness
is only useful when its subsequent exact lambda digits are also measured.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Callable, Sequence


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402


Trit = tuple[int, int, int]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


@dataclass
class TernaryCnf:
    """Minimal exact one-hot ternary circuit builder."""

    next_variable: int = 1

    def __post_init__(self) -> None:
        self.clauses: list[list[int]] = []
        self.trits = 0
        self.gates = 0

    def new_trit(self) -> Trit:
        result = tuple(
            range(self.next_variable, self.next_variable + 3)
        )
        self.next_variable += 3
        self.trits += 1
        self.clauses.append(list(result))
        self.clauses.extend(
            ([-result[left], -result[right]])
            for left in range(3)
            for right in range(left + 1, 3)
        )
        return result  # type: ignore[return-value]

    def constant(self, value: int) -> Trit:
        result = self.new_trit()
        self.clauses.append([result[value % 3]])
        return result

    def gate(
        self,
        left: Trit,
        right: Trit,
        operation: Callable[[int, int], int],
    ) -> Trit:
        result = self.new_trit()
        for left_value in range(3):
            for right_value in range(3):
                output = operation(left_value, right_value) % 3
                self.clauses.append([
                    -left[left_value],
                    -right[right_value],
                    result[output],
                ])
        self.gates += 1
        return result

    def add(self, left: Trit, right: Trit) -> Trit:
        return self.gate(left, right, lambda a, b: a + b)

    def multiply(self, left: Trit, right: Trit) -> Trit:
        return self.gate(left, right, lambda a, b: a * b)


def scaled_view(trit: Trit, coefficient: int) -> Trit:
    coefficient %= 3
    if coefficient == 0:
        raise ValueError("a zero coefficient has no nonconstant view")
    if coefficient == 1:
        return trit
    # Output value a is active when the original value is 2*a.
    return trit[0], trit[2], trit[1]


def polynomial_monomials(
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
) -> tuple[tuple[tuple[int, int], int], ...]:
    """Return reduced quadratic coefficients, including squares."""

    variables = len(linear)
    result = []
    for left in range(variables):
        diagonal = 2 * int(polar[left][left]) % 3
        if diagonal:
            result.append(((left, left), diagonal))
        for right in range(left + 1, variables):
            coefficient = int(polar[left][right]) % 3
            if coefficient:
                result.append(((left, right), coefficient))
    return tuple(result)


def build_cnf(
    constants: Sequence[int],
    linears: Sequence[Sequence[int]],
    polars: Sequence[Sequence[Sequence[int]]],
) -> tuple[TernaryCnf, tuple[Trit, ...]]:
    if not (
        len(constants) == len(linears) == len(polars)
    ):
        raise ValueError("the polynomial row counts disagree")
    variables = len(linears[0])
    circuit = TernaryCnf()
    inputs = tuple(circuit.new_trit() for _ in range(variables))

    needed_pairs = {
        pair
        for linear, polar in zip(linears, polars)
        for pair, _ in polynomial_monomials(linear, polar)
    }
    products = {
        pair: circuit.multiply(inputs[pair[0]], inputs[pair[1]])
        for pair in sorted(needed_pairs)
    }

    for constant, linear, polar in zip(constants, linears, polars):
        terms: list[Trit] = []
        terms.extend(
            scaled_view(inputs[index], coefficient)
            for index, coefficient in enumerate(linear)
            if coefficient % 3
        )
        terms.extend(
            scaled_view(products[pair], coefficient)
            for pair, coefficient in polynomial_monomials(linear, polar)
        )
        accumulator = circuit.constant(constant)
        for term in terms:
            accumulator = circuit.add(accumulator, term)
        circuit.clauses.append([accumulator[0]])
    return circuit, inputs


def exact_forms(
    candidate_index: int,
) -> tuple[
    tuple[tuple[tuple[int, ...], ...], ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    _, _, _, identifiers_a, identifiers_b = second.CANDIDATES[
        candidate_index
    ]
    profiles = second.profiles_from_ids(identifiers_a, identifiers_b)
    equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(equations, 54)
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles), origin, basis
    )
    active = tuple(
        index
        for index, matrix in enumerate(polars)
        if any(value for row in matrix for value in row)
    )
    if active != tuple(range(1, 7)) + tuple(range(8, 20)):
        raise AssertionError("the active second-digit rows changed")
    return (
        profiles,
        origin,
        basis,
        tuple(constants[index] for index in active),
        tuple(linears[index] for index in active),
        tuple(polars[index] for index in active),
    )


def decode_trits(model: Sequence[int], inputs: Sequence[Trit]) -> tuple[int, ...]:
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


def solve_candidate(candidate_index: int, solver_name: str) -> dict[str, object]:
    try:
        from pysat.solvers import Solver
    except ImportError as error:
        raise SystemExit(
            "Python-SAT is required for witness search; set PYTHONPATH "
            "to the pinned local installation."
        ) from error

    (
        profiles,
        origin,
        basis,
        constants,
        linears,
        polars,
    ) = exact_forms(candidate_index)
    circuit, inputs = build_cnf(constants, linears, polars)
    with Solver(
        name=solver_name,
        bootstrap_with=circuit.clauses,
    ) as solver:
        satisfiable = solver.solve()
        if not satisfiable:
            raise AssertionError("the full second-digit system is UNSAT")
        model = solver.get_model()
        if model is None:
            raise AssertionError("a SAT result had no model")
        affine_coordinates = decode_trits(model, inputs)
        statistics = solver.accum_stats()

    label, partition, target, identifiers_a, identifiers_b = (
        second.CANDIDATES[candidate_index]
    )
    placement_trits = second.lift_affine_point(
        origin, basis, affine_coordinates
    )
    equations = second.first_digit_equations(profiles)
    if second.symbolic_first_digits(
        equations, placement_trits
    ) != (0,) * 20:
        raise AssertionError("the SAT witness left the first-digit space")
    term_data = second.second_digit_term_data(profiles)
    if second.symbolic_second_digits(
        term_data, placement_trits
    ) != (0,) * 20:
        raise AssertionError("the SAT witness failed symbolic second digits")
    if second.direct_second_digits(
        profiles, placement_trits
    ) != (0,) * 20:
        raise AssertionError("the SAT witness failed exact second digits")

    displayed = second.displayed_values(profiles, placement_trits)
    digit_prefixes = tuple(
        second.lambda_digits(value, 8) for value in displayed
    )
    if any(prefix[:3] != (0, 0, 0) for prefix in digit_prefixes):
        raise AssertionError("the exact witness lost a lower lambda digit")
    masks_a, masks_b = second.masks_from_trits(
        profiles, placement_trits
    )
    return {
        "schema": "lp333-order3-full-second-digit-sat-witness-v1",
        "scope": (
            "One placement witness for all eighteen nonzero second-digit "
            "equations on a fixed exact h=2 profile; not a full phase "
            "solution, LP(333), Legendre pair, or H(668)."
        ),
        "label": label,
        "partition": partition,
        "target": target,
        "profile_ids_a": identifiers_a,
        "profile_ids_b": identifiers_b,
        "affine_coordinates": affine_coordinates,
        "placement_trits": placement_trits,
        "masks_a": masks_a,
        "masks_b": masks_b,
        "displayed_exact_values": displayed,
        "displayed_lambda_digits_through_7": digit_prefixes,
        "affine_coordinates_sha256": compact_hash(affine_coordinates),
        "placement_trits_sha256": compact_hash(placement_trits),
        "cnf": {
            "boolean_variables": circuit.next_variable - 1,
            "ternary_wires": circuit.trits,
            "truth_table_gates": circuit.gates,
            "clauses": len(circuit.clauses),
            "solver": solver_name,
            "statistics": statistics,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=0, choices=range(5))
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    certificate = solve_candidate(args.candidate, args.solver)
    print(json.dumps(certificate, indent=2))
    print(f"semantic_sha256={compact_hash(certificate)}")


if __name__ == "__main__":
    main()

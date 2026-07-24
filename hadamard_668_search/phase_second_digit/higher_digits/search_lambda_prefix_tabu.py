#!/usr/bin/env python3
"""Low-memory ternary tabu search for consecutive placement digits.

This is an instrumental search, not a verifier.  It composes every exact
phase exponent with the 36-dimensional first-digit affine space and updates
the two Eisenstein coordinates of all twenty displayed equations exactly.
The objective is the number of nonzero lambda digits from digit 2 through a
requested maximum.  Any zero objective is replayed through the independent
exact phase implementation before it is reported.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import solve_lambda_prefix_sat as prefix  # noqa: E402


ROOT_A = np.array((1, 0, -1), dtype=np.int16)
ROOT_B = np.array((0, 1, -1), dtype=np.int16)


def lambda_objective(
    first: np.ndarray,
    second: np.ndarray,
    maximum_digit: int,
    lower_digit_weight: int = 1,
) -> np.ndarray:
    """Count nonzero digits 2..maximum_digit columnwise."""

    if first.ndim == 1:
        first = first[:, None]
        second = second[:, None]
    left = first.copy()
    right = second.copy()
    result = np.zeros(first.shape[1], dtype=np.int16)
    for digit in range(maximum_digit + 1):
        residue = (left + right) % 3
        if digit >= 2:
            weight = lower_digit_weight if digit == 2 else 1
            result += weight * np.count_nonzero(residue, axis=0)
        left -= residue
        next_left = (2 * left - right) // 3
        next_right = (left + right) // 3
        left, right = next_left, next_right
    return result


class ExactPhaseObjective:
    def __init__(self, candidate_index: int) -> None:
        candidate = prefix.second.CANDIDATES[candidate_index]
        self.profiles = prefix.second.profiles_from_ids(
            candidate[3], candidate[4]
        )
        equations = prefix.second.first_digit_equations(self.profiles)
        self.origin, self.basis = prefix.second.affine_parameterization(
            equations, 54
        )
        rows = prefix.grouped_term_rows(self.profiles)
        forms = tuple(
            sorted({form for _, grouped in rows for form, _ in grouped})
        )
        form_index = {form: index for index, form in enumerate(forms)}
        self.multiplicity = np.zeros(
            (len(rows), len(forms)), dtype=np.int16
        )
        self.targets = np.zeros(len(rows), dtype=np.int16)
        for row, (target, grouped) in enumerate(rows):
            self.targets[row] = target
            for form, value in grouped:
                self.multiplicity[row, form_index[form]] = value

        self.constants = np.zeros(len(forms), dtype=np.int16)
        self.slopes = np.zeros((len(forms), 36), dtype=np.int16)
        for form_number, (constant, coefficients) in enumerate(forms):
            self.constants[form_number] = (
                constant
                + sum(
                    coefficient * self.origin[variable]
                    for variable, coefficient in coefficients
                )
            ) % 3
            for affine_variable in range(36):
                self.slopes[form_number, affine_variable] = sum(
                    coefficient
                    * self.basis[affine_variable][variable]
                    for variable, coefficient in coefficients
                ) % 3
        self.move_variables = np.tile(np.arange(36), 2)
        self.move_deltas = np.repeat((1, 2), 36)
        self.delayed_constraint = None
        self.move_pivot_deltas = np.zeros(72, dtype=np.int16)

    def enforce_delayed_e1_origin(self) -> None:
        """Parameterize the digit-3 E1-origin linear hyperplane."""

        if any(int(value) % 3 for value in self.multiplicity[7]):
            raise AssertionError(
                "the delayed-origin multiplicities left multiples of three"
            )
        effective = self.multiplicity[7] // 3
        constant = int(
            np.sum(effective * (1 - self.constants)) % 3
        )
        linear = (-effective @ self.slopes) % 3
        support = np.flatnonzero(linear)
        if len(support) == 0:
            raise AssertionError("the delayed-origin hyperplane vanished")
        pivot = int(support[0])
        inverse = 1 if int(linear[pivot]) == 1 else 2
        free = np.array(
            tuple(index for index in range(36) if index != pivot)
        )
        self.move_variables = np.tile(free, 2)
        self.move_deltas = np.repeat((1, 2), len(free))
        self.move_pivot_deltas = (
            -linear[self.move_variables]
            * self.move_deltas
            * inverse
        ) % 3
        self.delayed_constraint = (constant, linear, pivot, inverse)

    def project_delayed_hyperplane(
        self, coordinates: np.ndarray
    ) -> None:
        if self.delayed_constraint is None:
            return
        constant, linear, pivot, inverse = self.delayed_constraint
        residual_without_pivot = (
            constant
            + int(linear @ coordinates)
            - int(linear[pivot]) * int(coordinates[pivot])
        ) % 3
        coordinates[pivot] = (
            -residual_without_pivot * inverse
        ) % 3

    def state(self, coordinates: np.ndarray):
        exponents = (self.constants + self.slopes @ coordinates) % 3
        first = self.multiplicity @ ROOT_A[exponents] - self.targets
        second = self.multiplicity @ ROOT_B[exponents]
        return exponents, first, second

    def candidates(
        self,
        exponents: np.ndarray,
        first: np.ndarray,
        second: np.ndarray,
    ):
        moved_exponents = (
            exponents[:, None]
            + self.slopes[:, self.move_variables] * self.move_deltas
            + (
                0
                if self.delayed_constraint is None
                else self.slopes[
                    :, self.delayed_constraint[2]
                ][:, None]
                * self.move_pivot_deltas
            )
        ) % 3
        moved_first = (
            first[:, None]
            + self.multiplicity
            @ (ROOT_A[moved_exponents] - ROOT_A[exponents, None])
        )
        moved_second = (
            second[:, None]
            + self.multiplicity
            @ (ROOT_B[moved_exponents] - ROOT_B[exponents, None])
        )
        return moved_exponents, moved_first, moved_second

    def apply_move(
        self, coordinates: np.ndarray, move: int
    ) -> tuple[int, int]:
        variable = int(self.move_variables[move])
        delta = int(self.move_deltas[move])
        coordinates[variable] = (coordinates[variable] + delta) % 3
        if self.delayed_constraint is not None:
            pivot = int(self.delayed_constraint[2])
            coordinates[pivot] = (
                coordinates[pivot] + int(self.move_pivot_deltas[move])
            ) % 3
        return variable, delta

    def exact_replay(
        self,
        coordinates: np.ndarray,
        maximum_digit: int,
        lower_digit_weight: int = 1,
    ) -> dict[str, object]:
        affine = tuple(map(int, coordinates))
        placement = prefix.second.lift_affine_point(
            self.origin, self.basis, affine
        )
        values = prefix.second.displayed_values(
            self.profiles, placement
        )
        digits = tuple(
            prefix.second.lambda_digits(value, 10) for value in values
        )
        residual_counts = tuple(
            sum(row[digit] != 0 for row in digits)
            for digit in range(2, maximum_digit + 1)
        )
        score = (
            lower_digit_weight * residual_counts[0]
            + sum(residual_counts[1:])
        )
        return {
            "affine_coordinates": affine,
            "affine_coordinates_sha256": prefix.compact_hash(affine),
            "placement_trits": placement,
            "placement_trits_sha256": prefix.compact_hash(placement),
            "displayed_exact_values": values,
            "lambda_digits_through_9": digits,
            "objective": score,
            "digit_residual_counts": residual_counts,
        }


def search(
    candidate_index: int,
    maximum_digit: int,
    seconds: float,
    seed: int,
    restart_updates: int,
    initial_affine: tuple[int, ...] | None,
    enforce_delayed_linear: bool,
    lower_digit_weight: int,
) -> dict[str, object]:
    if lower_digit_weight < 1:
        raise ValueError("the lower-digit weight must be positive")
    objective = ExactPhaseObjective(candidate_index)
    if enforce_delayed_linear:
        objective.enforce_delayed_e1_origin()
    rng = np.random.default_rng(seed)
    started = time.monotonic()
    deadline = started + seconds
    updates = 0
    restarts = 0
    best_score = 10**9
    best_coordinates = None
    initial_pending = initial_affine is not None

    while time.monotonic() < deadline:
        if initial_pending:
            coordinates = np.array(initial_affine, dtype=np.int16)
            initial_pending = False
        else:
            coordinates = rng.integers(
                0, 3, 36, dtype=np.int16
            )
        objective.project_delayed_hyperplane(coordinates)
        exponents, first, second = objective.state(coordinates)
        tabu_until = np.zeros(36, dtype=np.int64)
        for local_step in range(restart_updates):
            scores = lambda_objective(
                first,
                second,
                maximum_digit,
                lower_digit_weight,
            )
            current_score = int(scores[0])
            if current_score < best_score:
                replay = objective.exact_replay(
                    coordinates,
                    maximum_digit,
                    lower_digit_weight,
                )
                if int(replay["objective"]) != current_score:
                    raise AssertionError(
                        "incremental and exact objectives disagree"
                    )
                best_score = current_score
                best_coordinates = coordinates.copy()
                print(
                    f"best={best_score} updates={updates} "
                    f"restarts={restarts} "
                    f"seconds={time.monotonic()-started:.3f}",
                    flush=True,
                )
                if best_score == 0:
                    break

            moved_exponents, moved_first, moved_second = (
                objective.candidates(exponents, first, second)
            )
            moved_scores = lambda_objective(
                moved_first,
                moved_second,
                maximum_digit,
                lower_digit_weight,
            )
            allowed = (
                tabu_until[objective.move_variables] <= updates
            ) | (moved_scores < best_score)
            ranked = np.where(allowed, moved_scores, 32767)
            minimum = int(ranked.min())
            choices = np.flatnonzero(ranked == minimum)
            move = int(rng.choice(choices))
            variable, delta = objective.apply_move(coordinates, move)
            exponents = moved_exponents[:, move]
            first = moved_first[:, move]
            second = moved_second[:, move]
            tabu_until[variable] = (
                updates + 7 + int(rng.integers(0, 5))
            )
            updates += 1
            if best_score == 0 or time.monotonic() >= deadline:
                break
        if best_score == 0:
            break
        restarts += 1

    if best_coordinates is None:
        raise AssertionError("the bounded search evaluated no point")
    best_replay = objective.exact_replay(
        best_coordinates,
        maximum_digit,
        lower_digit_weight,
    )
    candidate = prefix.second.CANDIDATES[candidate_index]
    result = {
        "schema": "lp333-order3-lambda-prefix-tabu-checkpoint-v1",
        "scope": (
            "A bounded stochastic placement search checkpoint; only a "
            "zero objective is a consecutive-digit witness."
        ),
        "label": candidate[0],
        "candidate_index": candidate_index,
        "maximum_digit": maximum_digit,
        "status": "SAT" if best_score == 0 else "UNKNOWN",
        "best_objective": best_score,
        "seed": seed,
        "delayed_e1_origin_enforced": enforce_delayed_linear,
        "lower_digit_weight": lower_digit_weight,
        "updates": updates,
        "restarts": restarts,
        "wall_seconds": time.monotonic() - started,
        "best_replay": best_replay,
    }
    result["semantic_sha256"] = prefix.compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=1, choices=range(5))
    parser.add_argument("--maximum-digit", type=int, default=3)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--restart-updates", type=int, default=100000)
    parser.add_argument("--initial-certificate", type=Path)
    parser.add_argument(
        "--initial-affine",
        help="comma-separated 36-trit affine point",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--enforce-delayed-linear",
        action="store_true",
        help="stay on the exact E1-origin digit-3 hyperplane",
    )
    parser.add_argument(
        "--lower-digit-weight",
        type=int,
        default=1,
        help="weight for every nonzero digit-2 row",
    )
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
        if len(initial) != 36 or any(
            value not in (0, 1, 2) for value in initial
        ):
            raise ValueError("the initial affine point needs 36 trits")
    result = search(
        args.candidate,
        args.maximum_digit,
        args.seconds,
        args.seed,
        args.restart_updates,
        initial,
        args.enforce_delayed_linear,
        args.lower_digit_weight,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()

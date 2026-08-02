#!/usr/bin/env python3
"""Numerical reconnaissance for exactly lumpable asymptotic families.

This script is deliberately dependency-free.  It builds transition
probabilities directly from the two update definitions and solves the
embedded (holding-step-free) absorbing chain by Gauss--Seidel iteration.

The output is reconnaissance, not a positivity certificate.  The analytic
claims supported by the calculations are proved separately in report.md.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


State2 = Tuple[int, int]
WindmillState = Tuple[int, int, int]


def baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1.0 - 1.0 / r) / (1.0 - r ** (-n))
    if rule == "dB":
        return (n - 1.0) / n * (1.0 - 1.0 / r) / (1.0 - r ** (-(n - 1)))
    raise ValueError(rule)


def _gauss_seidel(
    states: Sequence[Tuple[int, ...]],
    transitions: Sequence[Sequence[Tuple[int, float]]],
    extinction: int,
    fixation: int,
    tolerance: float = 2.0e-12,
    max_iterations: int = 500_000,
) -> Tuple[List[float], int, float]:
    values = [0.0 for _ in states]
    values[fixation] = 1.0
    order = sorted(
        range(len(states)), key=lambda k: sum(states[k]), reverse=True
    )
    error = float("inf")
    for iteration in range(max_iterations):
        error = 0.0
        for source in order:
            if source in (extinction, fixation):
                continue
            new_value = sum(
                probability * values[target]
                for target, probability in transitions[source]
            )
            error = max(error, abs(new_value - values[source]))
            values[source] = new_value
        if error < tolerance:
            return values, iteration + 1, error
    raise RuntimeError(
        f"Gauss--Seidel did not converge: residual {error:g} after "
        f"{max_iterations} iterations"
    )


@dataclass(frozen=True)
class TwoClass:
    """Two automorphism classes with constant weights on each edge orbit."""

    size_a: int
    size_b: int
    within_a: float
    within_b: float
    cross: float

    @property
    def n(self) -> int:
        return self.size_a + self.size_b

    @property
    def degree_a(self) -> float:
        return self.within_a * (self.size_a - 1) + self.cross * self.size_b

    @property
    def degree_b(self) -> float:
        return self.within_b * (self.size_b - 1) + self.cross * self.size_a

    def changing_transitions(
        self, state: State2, r: float, rule: str
    ) -> List[Tuple[State2, float]]:
        i, j = state
        a, b = self.size_a, self.size_b
        x, y, g = self.within_a, self.within_b, self.cross
        n = a + b
        if state in ((0, 0), (a, b)):
            return []
        result: List[Tuple[State2, float]] = []

        if rule == "Bd":
            degree_a, degree_b = self.degree_a, self.degree_b
            total_fitness = n + (r - 1.0) * (i + j)
            if i < a:
                result.append(
                    (
                        (i + 1, j),
                        r
                        * (a - i)
                        / total_fitness
                        * (i * x / degree_a + j * g / degree_b),
                    )
                )
            if i:
                result.append(
                    (
                        (i - 1, j),
                        i
                        / total_fitness
                        * ((a - i) * x / degree_a + (b - j) * g / degree_b),
                    )
                )
            if j < b:
                result.append(
                    (
                        (i, j + 1),
                        r
                        * (b - j)
                        / total_fitness
                        * (j * y / degree_b + i * g / degree_a),
                    )
                )
            if j:
                result.append(
                    (
                        (i, j - 1),
                        j
                        / total_fitness
                        * ((b - j) * y / degree_b + (a - i) * g / degree_a),
                    )
                )
        elif rule == "dB":
            if i < a:
                mutant_mass = i * x + j * g
                resident_mass = (a - i - 1) * x + (b - j) * g
                if mutant_mass:
                    result.append(
                        (
                            (i + 1, j),
                            (a - i)
                            / n
                            * r
                            * mutant_mass
                            / (r * mutant_mass + resident_mass),
                        )
                    )
            if i:
                mutant_mass = (i - 1) * x + j * g
                resident_mass = (a - i) * x + (b - j) * g
                if resident_mass:
                    result.append(
                        (
                            (i - 1, j),
                            i
                            / n
                            * resident_mass
                            / (r * mutant_mass + resident_mass),
                        )
                    )
            if j < b:
                mutant_mass = j * y + i * g
                resident_mass = (b - j - 1) * y + (a - i) * g
                if mutant_mass:
                    result.append(
                        (
                            (i, j + 1),
                            (b - j)
                            / n
                            * r
                            * mutant_mass
                            / (r * mutant_mass + resident_mass),
                        )
                    )
            if j:
                mutant_mass = (j - 1) * y + i * g
                resident_mass = (b - j) * y + (a - i) * g
                if resident_mass:
                    result.append(
                        (
                            (i, j - 1),
                            j
                            / n
                            * resident_mass
                            / (r * mutant_mass + resident_mass),
                        )
                    )
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in result if p > 0.0]

    def fixation(self, r: float, rule: str) -> Tuple[float, int, float]:
        states = [
            (i, j)
            for i in range(self.size_a + 1)
            for j in range(self.size_b + 1)
        ]
        index = {state: k for k, state in enumerate(states)}
        rows: List[List[Tuple[int, float]]] = []
        for state in states:
            row = self.changing_transitions(state, r, rule)
            mass = sum(p for _, p in row)
            rows.append(
                [(index[target], p / mass) for target, p in row] if mass else []
            )
        values, iterations, residual = _gauss_seidel(
            states,
            rows,
            index[(0, 0)],
            index[(self.size_a, self.size_b)],
        )
        average = (
            self.size_a * values[index[(1, 0)]]
            + self.size_b * values[index[(0, 1)]]
        ) / self.n
        return average, iterations, residual


@dataclass(frozen=True)
class Windmill:
    """m triangles sharing a hub; pair edges have weight pair_weight."""

    modules: int
    pair_weight: float

    @property
    def n(self) -> int:
        return 2 * self.modules + 1

    def changing_transitions(
        self, state: WindmillState, r: float, rule: str
    ) -> List[Tuple[WindmillState, float]]:
        # state=(hub type, number of mixed pairs, number of mutant pairs)
        h, mixed, mutant_pairs = state
        m, edge, n = self.modules, self.pair_weight, self.n
        resident_pairs = m - mixed - mutant_pairs
        mutant_leaves = mixed + 2 * mutant_pairs
        resident_leaves = 2 * resident_pairs + mixed
        if state in ((0, 0, 0), (1, 0, m)):
            return []
        result: List[Tuple[WindmillState, float]] = []

        if rule == "Bd":
            leaf_degree = edge + 1.0
            total_fitness = n + (r - 1.0) * (h + mutant_leaves)
            if not h and mutant_leaves:
                result.append(
                    ((1, mixed, mutant_pairs), r * mutant_leaves / (total_fitness * leaf_degree))
                )
            if h and resident_leaves:
                result.append(
                    ((0, mixed, mutant_pairs), resident_leaves / (total_fitness * leaf_degree))
                )
            if h and resident_pairs:
                result.append(
                    (
                        (h, mixed + 1, mutant_pairs),
                        r * resident_pairs / (total_fitness * m),
                    )
                )
            if mixed:
                result.append(
                    (
                        (h, mixed - 1, mutant_pairs + 1),
                        r
                        * mixed
                        / total_fitness
                        * (edge / leaf_degree + h / (2 * m)),
                    )
                )
                result.append(
                    (
                        (h, mixed - 1, mutant_pairs),
                        mixed
                        / total_fitness
                        * (edge / leaf_degree + (1 - h) / (2 * m)),
                    )
                )
            if mutant_pairs and not h:
                result.append(
                    (
                        (h, mixed + 1, mutant_pairs - 1),
                        mutant_pairs / (total_fitness * m),
                    )
                )
        elif rule == "dB":
            if not h and mutant_leaves:
                result.append(
                    (
                        (1, mixed, mutant_pairs),
                        r
                        * mutant_leaves
                        / (n * (r * mutant_leaves + resident_leaves)),
                    )
                )
            if h and resident_leaves:
                result.append(
                    (
                        (0, mixed, mutant_pairs),
                        resident_leaves
                        / (n * (r * mutant_leaves + resident_leaves)),
                    )
                )
            if h and resident_pairs:
                result.append(
                    (
                        (h, mixed + 1, mutant_pairs),
                        2 * resident_pairs / n * r / (r + edge),
                    )
                )
            if mixed:
                result.append(
                    (
                        (h, mixed - 1, mutant_pairs + 1),
                        mixed
                        / n
                        * r
                        * (edge + h)
                        / (r * (edge + h) + 1 - h),
                    )
                )
                result.append(
                    (
                        (h, mixed - 1, mutant_pairs),
                        mixed
                        / n
                        * (edge + 1 - h)
                        / (edge + 1 - h + r * h),
                    )
                )
            if mutant_pairs and not h:
                result.append(
                    (
                        (h, mixed + 1, mutant_pairs - 1),
                        2 * mutant_pairs / (n * (r * edge + 1)),
                    )
                )
        else:
            raise ValueError(rule)
        return [(target, p) for target, p in result if p > 0.0]

    def fixation(self, r: float, rule: str) -> Tuple[float, int, float]:
        states = [
            (h, mixed, mutant_pairs)
            for h in (0, 1)
            for mutant_pairs in range(self.modules + 1)
            for mixed in range(self.modules - mutant_pairs + 1)
        ]
        index = {state: k for k, state in enumerate(states)}
        rows: List[List[Tuple[int, float]]] = []
        for state in states:
            row = self.changing_transitions(state, r, rule)
            mass = sum(p for _, p in row)
            rows.append(
                [(index[target], p / mass) for target, p in row] if mass else []
            )
        values, iterations, residual = _gauss_seidel(
            states,
            rows,
            index[(0, 0, 0)],
            index[(1, 0, self.modules)],
        )
        average = (
            values[index[(1, 0, 0)]]
            + 2 * self.modules * values[index[(0, 1, 0)]]
        ) / self.n
        return average, iterations, residual


def two_type_branching_survival(
    fraction_a: float,
    degree_ratio: float,
    cross_from_a: float,
    r: float,
    rule: str,
) -> Tuple[float, Tuple[float, float]]:
    """Greatest survival solution for the two-type rare-mutant process.

    The limiting weighted degrees are delta_a=degree_ratio, delta_b=1.
    P_ab=cross_from_a and detailed balance determines P_ba.
    """

    q = fraction_a
    x = degree_ratio
    a = cross_from_a
    b = q * x * a / (1.0 - q)
    if not (0.0 <= b <= 1.0):
        raise ValueError("parameters violate detailed balance / stochasticity")
    p = ((1 - a, a), (b, 1 - b))
    transpose_similarity = ((1 - a, x * a), (b / x, 1 - b))
    temperatures = (1 - a + x * a, 1 - b + b / x)
    survival = [1.0, 1.0]
    for _ in range(1_000_000):
        matrix = p if rule == "Bd" else transpose_similarity
        mass = [
            matrix[i][0] * survival[0] + matrix[i][1] * survival[1]
            for i in range(2)
        ]
        new = [
            r
            * mass[i]
            / ((temperatures[i] if rule == "Bd" else 1.0) + r * mass[i])
            for i in range(2)
        ]
        if max(abs(new[i] - survival[i]) for i in range(2)) < 1.0e-14:
            average = q * new[0] + (1 - q) * new[1]
            return average, (new[0], new[1])
        survival = new
    raise RuntimeError("branching fixed-point iteration did not converge")


def run_default_scan() -> None:
    print("# Numerical reconnaissance only; deltas are graph minus K_n")
    print("# two-class family")
    for n in (10, 20, 40):
        graph = TwoClass(n // 2, n - n // 2, 0.1, 1.0, 1.0)
        for r in (1.1, 2.0, 10.0):
            fields = []
            for rule in ("Bd", "dB"):
                value, iterations, residual = graph.fixation(r, rule)
                fields.append(
                    f"{rule}_delta={value-baseline(n,r,rule):+.9g} "
                    f"iterations={iterations} residual={residual:.2g}"
                )
            print(f"two_class n={n} r={r:g} " + " ".join(fields))

    print("# windmill family")
    for modules in (5, 10, 20):
        graph = Windmill(modules, pair_weight=1.0)
        for r in (1.1, 2.0, 10.0):
            fields = []
            for rule in ("Bd", "dB"):
                value, iterations, residual = graph.fixation(r, rule)
                fields.append(
                    f"{rule}_delta={value-baseline(graph.n,r,rule):+.9g} "
                    f"iterations={iterations} residual={residual:.2g}"
                )
            print(
                f"windmill modules={modules} n={graph.n} r={r:g} "
                + " ".join(fields)
            )

    print("# two-type branching limits")
    for r in (1.1, 2.0, 10.0):
        bd, _ = two_type_branching_survival(0.5, 2.0, 0.4, r, "Bd")
        db, _ = two_type_branching_survival(0.5, 2.0, 0.4, r, "dB")
        limiting_baseline = 1.0 - 1.0 / r
        print(
            f"branching r={r:g} Bd_delta={bd-limiting_baseline:+.9g} "
            f"dB_delta={db-limiting_baseline:+.9g}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--default-scan", action="store_true", help="run the documented scan"
    )
    args = parser.parse_args()
    if args.default_scan:
        run_default_scan()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

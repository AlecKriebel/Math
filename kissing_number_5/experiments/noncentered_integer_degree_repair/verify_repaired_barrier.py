#!/usr/bin/env python3
"""Exact audit of the final repaired noncentered relaxation witness."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path

from verifiers.verify_fixed41_bv_all_harmonics import verify as verify_all
from verifiers.verify_fixed41_bv_degree5 import determinant
from verifiers.verify_noncentered_integer_degree_mixture import (
    verify as verify_mixture,
)


N = 41


class VerificationError(ValueError):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def gegenbauer(t: Q, maximum: int = 3) -> tuple[Q, ...]:
    values = [Q(1)]
    if maximum:
        values.append(t)
    for degree in range(2, maximum + 1):
        values.append(
            (
                (2 * degree + 1) * t * values[-1]
                - (degree - 1) * values[-2]
            )
            / (degree + 2)
        )
    return tuple(values)


def harmonic_dimension(degree: int) -> int:
    return math.comb(degree + 4, 4) - (
        math.comb(degree + 2, 4) if degree >= 2 else 0
    )


@dataclass(frozen=True)
class Kernel:
    name: str
    weights: tuple[tuple[int, Q], ...]

    @property
    def rank(self) -> int:
        return sum(harmonic_dimension(degree) for degree, _ in self.weights)

    @property
    def diagonal(self) -> Q:
        return sum(weight for _, weight in self.weights)

    def value(self, node: Q) -> Q:
        values = gegenbauer(node, max(degree for degree, _ in self.weights))
        return sum(values[degree] * weight for degree, weight in self.weights)


def kernels() -> tuple[Kernel, ...]:
    basic = [
        Kernel("H1", ((1, Q(1)),)),
        Kernel("H2", ((2, Q(1)),)),
        Kernel("H3", ((3, Q(1)),)),
        Kernel("H0+5H1", ((0, Q(1, 6)), (1, Q(5, 6)))),
        Kernel("H0-5H1", ((0, Q(1, 6)), (1, Q(-5, 6)))),
        Kernel("H0+14H2", ((0, Q(1, 15)), (2, Q(14, 15)))),
        Kernel("H0-14H2", ((0, Q(1, 15)), (2, Q(-14, 15)))),
        Kernel("5H1+14H2", ((1, Q(5, 19)), (2, Q(14, 19)))),
        Kernel("5H1-14H2", ((1, Q(5, 19)), (2, Q(-14, 19)))),
        Kernel("H0+H1", ((0, Q(1, 2)), (1, Q(1, 2)))),
        Kernel("H0-H1", ((0, Q(1, 2)), (1, Q(-1, 2)))),
        Kernel("H0+H2", ((0, Q(1, 2)), (2, Q(1, 2)))),
        Kernel("H0-H2", ((0, Q(1, 2)), (2, Q(-1, 2)))),
        Kernel("H1+H2", ((1, Q(1, 2)), (2, Q(1, 2)))),
        Kernel("H1-H2", ((1, Q(1, 2)), (2, Q(-1, 2)))),
        Kernel(
            "H0+5H1+14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(7, 10))),
        ),
        Kernel(
            "H0+5H1-14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(-7, 10))),
        ),
        Kernel(
            "H0-5H1+14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(7, 10))),
        ),
        Kernel(
            "H0-5H1-14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(-7, 10))),
        ),
        Kernel("H0+30H3", ((0, Q(1, 31)), (3, Q(30, 31)))),
        Kernel("H0-30H3", ((0, Q(1, 31)), (3, Q(-30, 31)))),
        Kernel("5H1+30H3", ((1, Q(1, 7)), (3, Q(6, 7)))),
        Kernel("5H1-30H3", ((1, Q(1, 7)), (3, Q(-6, 7)))),
        Kernel(
            "H0+5H1+30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(5, 6))),
        ),
        Kernel(
            "H0+5H1-30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(-5, 6))),
        ),
        Kernel(
            "H0-5H1+30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(5, 6))),
        ),
        Kernel(
            "H0-5H1-30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(-5, 6))),
        ),
    ]
    return tuple(basic)


def common_capacity(projected: Q) -> int | None:
    if projected > 1:
        return 0
    if projected > Q(3, 4):
        return 1
    if projected > Q(2, 3):
        return 2
    if projected > Q(5, 8):
        return 3
    if projected > Q(1, 2):
        return 4
    if projected == Q(1, 2):
        return 6
    return None


def capacity_slacks(
    nodes: tuple[Q, ...],
    triples: tuple[tuple[int, int, int], ...],
    alpha: tuple[Q, ...],
    nu: tuple[Q, ...],
) -> tuple[list[Q], list[Q]]:
    nonpositive = tuple(i for i, node in enumerate(nodes) if node <= 0)
    positive = tuple(i for i, node in enumerate(nodes) if node > 0)
    stratified = []
    for lower in range(len(nonpositive)):
        for upper in range(lower, len(nonpositive)):
            bases = nonpositive[lower : upper + 1]
            top = nodes[bases[-1]]
            for high_index in positive:
                high = nodes[high_index]
                capacity = (
                    0
                    if top == -1
                    else common_capacity(2 * high**2 / (1 + top))
                )
                if capacity is None:
                    continue
                base_set = set(bases)
                left = Q(0)
                for triple, mass in zip(triples, nu, strict=True):
                    count = sum(
                        triple[position] in base_set
                        and all(
                            nodes[triple[other]] >= high
                            for other in range(3)
                            if other != position
                        )
                        for position in range(3)
                    )
                    left += count * mass
                right = 3 * capacity * sum(alpha[index] for index in bases)
                stratified.append(right - left)

    weighted = []
    for high in positive:
        threshold = nodes[high]
        capacities = {}
        for base, node in enumerate(nodes):
            if node == -1:
                capacities[base] = 0
            elif node <= 0:
                capacity = common_capacity(2 * threshold**2 / (1 + node))
                if capacity is not None:
                    capacities[base] = capacity
            elif threshold == Q(1, 2):
                capacities[base] = 7
        left = Q(0)
        for triple, mass in zip(triples, nu, strict=True):
            count = sum(
                triple[position] in capacities
                and all(
                    nodes[triple[other]] >= threshold
                    for other in range(3)
                    if other != position
                )
                for position in range(3)
            )
            left += count * mass
        right = 3 * sum(
            capacity * alpha[index]
            for index, capacity in capacities.items()
        )
        weighted.append(right - left)
    return stratified, weighted


def all_principal_minors_nonnegative(matrix: list[list[Q]]) -> bool:
    for size in range(1, len(matrix) + 1):
        for indices in itertools.combinations(range(len(matrix)), size):
            minor = determinant(
                [[matrix[i][j] for j in indices] for i in indices]
            )
            if minor < 0:
                return False
    return True


def verify(
    source_path: Path,
    all_harmonics_path: Path,
    mixture_path: Path,
) -> dict[str, object]:
    source = json.loads(source_path.read_text())
    nodes = tuple(Q(value) for value in source["grid"])
    alpha = tuple(Q(value) for value in source["alpha"])
    triples = tuple(tuple(item) for item in source["triples"])
    nu = tuple(Q(value) for value in source["nu"])
    check(sum(alpha) == 40 and sum(nu) == 1560, "mass mismatch")
    check(sum(alpha[:4]) >= 7, "negative robust-depth mass fails")
    check(sum(alpha[5:]) >= 6, "positive robust-depth mass fails")
    check(alpha[0] <= Q(36, 41), "antipode-pair bound fails")
    check(alpha[0] + alpha[1] >= Q(46, 41), "deep-edge bound fails")
    check(alpha[1] <= 5 and alpha[6] <= 15, "local degree cap fails")

    harmonic_result = verify_all(source_path, all_harmonics_path)
    check(harmonic_result["status"] == "PASS", "all-harmonic audit failed")
    mixture_result = verify_mixture(mixture_path, source_path)
    check(mixture_result["status"] == "PASS", "integer mixture audit failed")

    stratified, weighted = capacity_slacks(
        nodes, triples, alpha, nu
    )
    check(len(stratified) == 18, "unexpected stratified row count")
    check(len(weighted) == 2, "unexpected weighted row count")
    check(all(value >= 0 for value in stratified), "stratified cap fails")
    check(all(value >= 0 for value in weighted), "weighted cap fails")

    values = [gegenbauer(node) for node in nodes]
    dimensions = (1, 5, 14, 30)
    subsets = (
        (1,),
        (0, 1),
        (2,),
        (0, 2),
        (1, 2),
        (0, 1, 2),
        (3,),
        (0, 3),
        (1, 3),
        (0, 1, 3),
    )
    for subset in subsets:
        rank = sum(dimensions[index] for index in subset)
        matrix = [
            [
                1
                + sum(
                    mass * values[index][first] * values[index][second]
                    for index, mass in enumerate(alpha)
                )
                - Q(N, rank)
                for second in subset
            ]
            for first in subset
        ]
        check(
            all_principal_minors_nonnegative(matrix),
            f"frame block fails for {subset}",
        )

    residuals = {}
    for kernel in kernels():
        kernel_values = tuple(kernel.value(node) for node in nodes)
        diagonal = kernel.diagonal
        rank = kernel.rank
        trace_one = N * diagonal
        pair_square = sum(
            mass * value**2
            for mass, value in zip(alpha, kernel_values, strict=True)
        )
        trace_two = N * diagonal**2 + N * pair_square
        triple_product = sum(
            mass
            * kernel_values[triple[0]]
            * kernel_values[triple[1]]
            * kernel_values[triple[2]]
            for triple, mass in zip(triples, nu, strict=True)
        )
        trace_three = (
            N * diagonal**3
            + 3 * N * diagonal * pair_square
            + N * triple_product
        )
        variance = trace_two - trace_one**2 / rank
        centered = (
            trace_three
            - 3 * trace_one * trace_two / rank
            + 2 * trace_one**3 / rank**2
        )
        residual = (
            (rank - 2) ** 2 * variance**3
            - rank * (rank - 1) * centered**2
        )
        check(variance >= 0, f"negative variance for {kernel.name}")
        check(residual >= 0, f"sharp rank inequality fails for {kernel.name}")
        residuals[kernel.name] = residual
    check(len(residuals) == 27, "unexpected sharp-rank kernel count")

    return {
        "status": "PASS",
        "all_harmonic_tail": harmonic_result["analytic_harmonic_tail"],
        "pair_tail": harmonic_result["pair_moment_analytic_tail"],
        "integer_row_atoms": mixture_result["positive_atoms"],
        "stratified_capacity_rows": len(stratified),
        "weighted_capacity_rows": len(weighted),
        "minimum_capacity_slack": str(min(stratified + weighted)),
        "frame_blocks": len(subsets),
        "sharp_rank_kernels": len(residuals),
        "minimum_sharp_rank_residual": str(min(residuals.values())),
        "scope": (
            "exact pair/triple and finite-population relaxation witness; "
            "not a spherical code or a global Gram matrix"
        ),
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=here / "candidate_exact_6.json"
    )
    parser.add_argument(
        "--all-harmonics",
        type=Path,
        default=here / "all_harmonics_certificate_6.json",
    )
    parser.add_argument(
        "--mixture",
        type=Path,
        default=here / "integer_row_mixture_6.json",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            verify(args.source, args.all_harmonics, args.mixture),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

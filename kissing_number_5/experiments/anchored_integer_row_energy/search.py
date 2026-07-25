#!/usr/bin/env python3
"""Discovery SDP for one-anchor row energy with integer contact degree.

This is an atomic-grid relaxation/search, not a rigorous bound.  For a fixed
code point x, ``a[u]`` models the number of the other 40 points at height
<x,y>=u.  ``z[u,v,t]`` models unordered pairs among those 40 points.  The
axisymmetric harmonic moment matrices are imposed directly.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import combinations_with_replacement
import json
from pathlib import Path

import cvxpy as cp
import numpy as np

from experiments.continuous_rank_bv_search.search import (
    gram_determinant,
    transverse_q,
)


NEIGHBORS = 40
MAX_INNER = Q(1, 2)


def rational_grid(denominator: int) -> tuple[Q, ...]:
    return tuple(
        Q(numerator, denominator)
        for numerator in range(-denominator, denominator // 2 + 1)
    )


def feasible_local_orbits(
    heights: tuple[Q, ...],
    pair_nodes: tuple[Q, ...],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (left, right, pair)
        for left, right in combinations_with_replacement(
            range(len(heights)), 2
        )
        for pair in range(len(pair_nodes))
        if gram_determinant(
            heights[left], heights[right], pair_nodes[pair]
        )
        >= 0
    )


def z_matrix(
    u: Q,
    v: Q,
    t: Q,
    harmonic_degree: int,
    radial_degree: int,
) -> np.ndarray:
    transverse = transverse_q(u, v, t, harmonic_degree)[harmonic_degree]
    return np.asarray(
        [
            [
                float(transverse * u**row * v**column)
                for column in range(radial_degree + 1)
            ]
            for row in range(radial_degree + 1)
        ],
        dtype=float,
    )


def solve_case(
    denominator: int,
    contact_degree: int,
    antipode_count: int,
    maximum_harmonic_degree: int,
    radial_degree: int,
) -> dict[str, object]:
    heights = rational_grid(denominator)
    pair_nodes = heights
    orbits = feasible_local_orbits(heights, pair_nodes)
    contact_index = heights.index(MAX_INNER)
    antipode_index = heights.index(Q(-1))

    a = cp.Variable(len(heights), nonneg=True)
    z = cp.Variable(len(orbits), nonneg=True)
    constraints: list[cp.Constraint] = [
        cp.sum(a) == NEIGHBORS,
        a[contact_index] == contact_degree,
        a[antipode_index] == antipode_count,
        cp.sum(
            a[index]
            for index, height in enumerate(heights)
            if height < 0
        )
        >= 7,
        cp.sum(
            a[index]
            for index, height in enumerate(heights)
            if height > 0
        )
        >= 6,
    ]

    # Every point at height u is incident to 39 unordered pairs among the
    # 40 non-anchor points.  A same-height pair contributes two incidences.
    for index in range(len(heights)):
        terms = []
        for orbit_index, (left, right, _) in enumerate(orbits):
            multiplicity = (left == index) + (right == index)
            if multiplicity:
                terms.append(multiplicity * z[orbit_index])
        constraints.append(cp.sum(terms) == (NEIGHBORS - 1) * a[index])

    # Moment matrices sum over all ordered pairs y,z, including y=z.
    minimum_eigenvalue_slack = 1.0e-9
    for harmonic_degree in range(maximum_harmonic_degree + 1):
        matrix = 0
        for index, height in enumerate(heights):
            matrix = matrix + a[index] * z_matrix(
                height,
                height,
                Q(1),
                harmonic_degree,
                radial_degree,
            )
        for orbit_index, (left, right, pair) in enumerate(orbits):
            u = heights[left]
            v = heights[right]
            t = pair_nodes[pair]
            contribution = z_matrix(
                u, v, t, harmonic_degree, radial_degree
            )
            contribution += z_matrix(
                v, u, t, harmonic_degree, radial_degree
            )
            matrix = matrix + z[orbit_index] * contribution
        constraints.append(
            matrix
            >> minimum_eigenvalue_slack
            * np.eye(radial_degree + 1)
        )

    objective = cp.Maximize(
        cp.sum(
            [float(height**2) * a[index]
             for index, height in enumerate(heights)]
        )
    )
    problem = cp.Problem(objective, constraints)
    value = problem.solve(
        solver="CLARABEL",
        tol_gap_abs=1.0e-8,
        tol_feas=1.0e-8,
        tol_gap_rel=1.0e-8,
        max_iter=1000,
    )

    result: dict[str, object] = {
        "denominator": denominator,
        "contact_degree": contact_degree,
        "antipode_count": antipode_count,
        "maximum_harmonic_degree": maximum_harmonic_degree,
        "radial_degree": radial_degree,
        "orbit_count": len(orbits),
        "status": problem.status,
        "objective": None if value is None else float(value),
        "warning": (
            "NUMERICAL EVIDENCE ONLY: atomic height/pair grid and "
            "floating-point SDP"
        ),
    }
    if a.value is not None:
        result["height_masses"] = {
            str(height): float(a.value[index])
            for index, height in enumerate(heights)
            if a.value[index] > 1.0e-7
        }
        result["negative_count"] = float(
            sum(
                a.value[index]
                for index, height in enumerate(heights)
                if height < 0
            )
        )
        result["positive_count"] = float(
            sum(
                a.value[index]
                for index, height in enumerate(heights)
                if height > 0
            )
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--denominator", type=int, default=8)
    parser.add_argument("--harmonic-degree", type=int, default=6)
    parser.add_argument("--radial-degree", type=int, default=4)
    parser.add_argument("--contact-min", type=int, default=0)
    parser.add_argument("--contact-max", type=int, default=15)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    results = []
    for contact_degree in range(args.contact_min, args.contact_max + 1):
        for antipode_count in (0, 1):
            result = solve_case(
                args.denominator,
                contact_degree,
                antipode_count,
                args.harmonic_degree,
                args.radial_degree,
            )
            results.append(result)
            print(
                contact_degree,
                antipode_count,
                result["status"],
                result["objective"],
                flush=True,
            )

    payload = {
        "schema": "anchored-integer-row-energy-atomic-search-v1",
        "results": results,
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()

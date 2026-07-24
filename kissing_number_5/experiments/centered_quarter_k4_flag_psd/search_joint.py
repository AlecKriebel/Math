#!/usr/bin/env python3
"""Joint quarter-grid K2/K3/K4 ordered-edge flag SDP.

Numerical discovery only.  Pair, triple, and Gram-PSD K4 orbit masses are
all variables.  For each base-edge color q, a Schur-complement block imposes
the covariance PSD condition for the 49 ordered extension profiles.
"""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path

import cvxpy as cp
import numpy as np

from experiments.centered_quarter_k4_flag_psd.search import (
    enumerate_orbits,
    face_types,
    flag_coefficients,
)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    source = json.loads(
        (root / "certificates/centered_quarter_bv_pseudodistribution.json")
        .read_text()
    )
    grid = [Q(value) for value in source["grid"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_index = {triple: index for index, triple in enumerate(triples)}
    color_count = len(grid)
    categories = tuple(itertools.product(range(color_count), repeat=2))
    category_index = {
        category: index for index, category in enumerate(categories)
    }

    orbits, labeled = enumerate_orbits(source)
    orbit_count = len(orbits)
    print(f"labeled={labeled} orbits={orbit_count}", flush=True)

    face_incidence = np.zeros((len(triples), orbit_count))
    flag = [
        np.zeros((len(categories), len(categories), orbit_count))
        for _ in range(color_count)
    ]
    for column, pattern in enumerate(orbits):
        for face in face_types(pattern):
            face_incidence[triple_index[face], column] += 1
        blocks = flag_coefficients(
            pattern, color_count, category_index, True
        )
        for color in range(color_count):
            flag[color][:, :, column] = blocks[color]

    # first_coeff[q,s,t] maps triple masses to oriented base-extension
    # incidence L[q,s], normalized by N.
    first_coeff = np.zeros(
        (color_count, len(categories), len(triples))
    )
    for triple_column, triple in enumerate(triples):
        triangle_edges = {
            (0, 1): triple[0],
            (0, 2): triple[1],
            (1, 2): triple[2],
        }
        for i, j in itertools.permutations(range(3), 2):
            k = next(vertex for vertex in range(3) if vertex not in (i, j))
            base_color = triangle_edges[tuple(sorted((i, j)))]
            profile = (
                triangle_edges[tuple(sorted((i, k)))],
                triangle_edges[tuple(sorted((j, k)))],
            )
            first_coeff[
                base_color, category_index[profile], triple_column
            ] += 1 / 6

    # marginal_coeff[q,t] is the average multiplicity of color q among the
    # three edges of triple orbit t.
    marginal_coeff = np.zeros((color_count, len(triples)))
    for column, triple in enumerate(triples):
        for color in triple:
            marginal_coeff[color, column] += 1 / 3

    alpha = cp.Variable(color_count, nonneg=True)
    nu = cp.Variable(len(triples), nonneg=True)
    k4 = cp.Variable(orbit_count, nonneg=True)
    margin = cp.Variable()
    constraints = [
        cp.sum(alpha) == 40,
        1 + np.array([float(value) for value in grid]) @ alpha == 0,
        marginal_coeff @ nu == 39 * alpha,
        face_incidence @ k4 == nu / 390,
        alpha >= margin,
        nu >= margin,
    ]

    factor = math.comb(41, 4) / 41
    identity = np.eye(len(categories) + 1)
    for color in range(color_count):
        first = first_coeff[color] @ nu
        flat_flag = flag[color].reshape(
            len(categories) * len(categories), orbit_count
        )
        distinct = factor * cp.reshape(
            flat_flag @ k4,
            (len(categories), len(categories)),
            order="C",
        )
        second = cp.diag(first) + distinct
        block = cp.bmat(
            [
                [second, cp.reshape(first, (len(categories), 1), order="C")],
                [
                    cp.reshape(first, (1, len(categories)), order="C"),
                    cp.reshape(alpha[color], (1, 1), order="C"),
                ],
            ]
        )
        # The common all-ones direction forces kernels, so do not require a
        # positive eigenvalue margin.  `margin` protects only pair/triple
        # masses from a spurious boundary solution.
        constraints.append(block >> 0)

    problem = cp.Problem(cp.Maximize(margin), constraints)
    value = problem.solve(solver="CLARABEL", verbose=True)
    report = {
        "status": problem.status,
        "objective_pair_triple_margin": value,
        "minimum_alpha": (
            None if alpha.value is None else float(np.min(alpha.value))
        ),
        "minimum_nu": None if nu.value is None else float(np.min(nu.value)),
        "positive_k4_orbits": (
            None if k4.value is None else int(np.sum(k4.value > 1e-10))
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

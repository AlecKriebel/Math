#!/usr/bin/env python3
"""Discovery search for edge-flag PSD extensions of the centered witness.

This is numerical discovery code.  It enumerates every unlabeled
quarter-grid Gram-PSD K4 orbit, matches the exact K3 marginal, and imposes
the covariance PSD matrix of extension-profile counts over every base-edge
color.  A solver status is never treated as a certificate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path

import cvxpy as cp
import numpy as np


EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def determinant(matrix: list[list[int]]) -> int:
    """Exact determinant for matrices of order at most four."""
    size = len(matrix)
    answer = 0
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = -1 if inversions % 2 else 1
        for i in range(size):
            term *= matrix[i][permutation[i]]
        answer += term
    return answer


def transform(pattern: tuple[int, ...], permutation: tuple[int, ...]):
    transformed = []
    for i, j in EDGES:
        image = tuple(sorted((permutation[i], permutation[j])))
        transformed.append(pattern[EDGE_INDEX[image]])
    return tuple(transformed)


def canonical(pattern: tuple[int, ...]) -> tuple[int, ...]:
    return min(transform(pattern, permutation) for permutation in PERMUTATIONS)


def face_types(pattern: tuple[int, ...]):
    a, b, c, d, e, f = pattern
    return (
        tuple(sorted((a, b, d))),
        tuple(sorted((a, c, e))),
        tuple(sorted((b, c, f))),
        tuple(sorted((d, e, f))),
    )


def scaled_gram(pattern: tuple[int, ...], values: list[int]):
    matrix = [[4 if i == j else 0 for j in range(4)] for i in range(4)]
    for color, (i, j) in zip(pattern, EDGES):
        matrix[i][j] = values[color]
        matrix[j][i] = values[color]
    return matrix


def gram_psd(pattern: tuple[int, ...], values: list[int]) -> bool:
    matrix = scaled_gram(pattern, values)
    for size in range(1, 5):
        for indices in itertools.combinations(range(4), size):
            principal = [
                [matrix[i][j] for j in indices] for i in indices
            ]
            if determinant(principal) < 0:
                return False
    return True


def flag_coefficients(
    pattern: tuple[int, ...],
    color_count: int,
    category_index: dict[tuple[int, int], int],
    ordered: bool,
):
    category_count = len(category_index)
    blocks = [
        np.zeros((category_count, category_count), dtype=float)
        for _ in range(color_count)
    ]
    base_pairs = (
        tuple(itertools.permutations(range(4), 2))
        if ordered
        else EDGES
    )
    for i, j in base_pairs:
        base_color = pattern[EDGE_INDEX[tuple(sorted((i, j)))]]
        remaining = [k for k in range(4) if k not in (i, j)]
        profiles = []
        for k in remaining:
            ik = EDGE_INDEX[tuple(sorted((i, k)))]
            jk = EDGE_INDEX[tuple(sorted((j, k)))]
            profile = (pattern[ik], pattern[jk])
            if not ordered:
                profile = tuple(sorted(profile))
            profiles.append(category_index[profile])
        first, second = profiles
        if first == second:
            blocks[base_color][first, first] += 2
        else:
            blocks[base_color][first, second] += 1
            blocks[base_color][second, first] += 1
    return blocks


def enumerate_orbits(source: dict):
    grid = [Q(value) for value in source["grid"]]
    values = [int(4 * value) for value in grid]
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_set = set(triples)
    representatives: dict[tuple[int, ...], tuple[int, ...]] = {}
    labeled = 0
    for pattern in itertools.product(range(len(grid)), repeat=6):
        faces = face_types(pattern)
        if any(face not in triple_set for face in faces):
            continue
        if not gram_psd(pattern, values):
            continue
        labeled += 1
        representative = canonical(pattern)
        representatives.setdefault(representative, representative)
    return tuple(sorted(representatives)), labeled


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ordered", action="store_true")
    parser.add_argument("--run-scs", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    source = json.loads(
        (root / "certificates/centered_quarter_bv_pseudodistribution.json")
        .read_text()
    )
    alpha = [Q(value) for value in source["alpha"]]
    nu = [Q(value) for value in source["nu"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_index = {triple: index for index, triple in enumerate(triples)}
    color_count = len(alpha)
    categories = tuple(
        itertools.product(range(color_count), repeat=2)
        if args.ordered
        else itertools.combinations_with_replacement(range(color_count), 2)
    )
    category_index = {
        category: index for index, category in enumerate(categories)
    }

    orbits, labeled = enumerate_orbits(source)
    print(f"labeled={labeled} orbits={len(orbits)}", flush=True)
    orbit_count = len(orbits)

    face_incidence = np.zeros((len(triples), orbit_count))
    flag = [
        np.zeros((len(categories), len(categories), orbit_count))
        for _ in range(color_count)
    ]
    for column, pattern in enumerate(orbits):
        for face in face_types(pattern):
            face_incidence[triple_index[face], column] += 1
        blocks = flag_coefficients(
            pattern, color_count, category_index, args.ordered
        )
        for color in range(color_count):
            flag[color][:, :, column] = blocks[color]

    # L[color, profile] is the total number of incidences between base
    # edges of that color and third vertices of that profile, divided by N.
    first = [
        [Q(0) for _ in categories] for _ in range(color_count)
    ]
    for triple, weight in zip(triples, nu):
        if args.ordered:
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
                first[base_color][category_index[profile]] += weight / 6
        else:
            for position, base_color in enumerate(triple):
                profile = tuple(
                    sorted(
                        triple[index]
                        for index in range(3)
                        if index != position
                    )
                )
                first[base_color][category_index[profile]] += weight / 6

    variable = cp.Variable(orbit_count, nonneg=True)
    constraints = [
        face_incidence @ variable
        == np.array([float(weight / 390) for weight in nu])
    ]
    flag_factor = math.comb(41, 4) / 41
    for color in range(color_count):
        first_float = np.array([float(value) for value in first[color]])
        constant = np.diag(first_float) - np.outer(
            first_float, first_float
        ) / float(alpha[color] if args.ordered else alpha[color] / 2)
        flat_flag = flag[color].reshape(
            len(categories) * len(categories), orbit_count
        )
        affine = cp.Constant(constant) + flag_factor * cp.reshape(
            flat_flag @ variable,
            (len(categories), len(categories)),
            order="C",
        )
        constraints.append(affine >> 0)

    problem = cp.Problem(cp.Maximize(cp.min(variable)), constraints)
    solver_options = [("CLARABEL", {})]
    if args.run_scs:
        solver_options.append(
            (
                "SCS",
                {
                    "eps": 1e-7,
                    "max_iters": 500_000,
                    "normalize": True,
                },
            )
        )
    for solver, options in solver_options:
        try:
            objective = problem.solve(solver=solver, verbose=True, **options)
        except Exception as error:  # discovery log
            print(f"{solver}: {type(error).__name__}: {error}", flush=True)
            continue
        print(
            json.dumps(
                {
                    "solver": solver,
                    "status": problem.status,
                    "objective_min_weight": objective,
                    "positive_variables": (
                        None
                        if variable.value is None
                        else int(np.sum(variable.value > 1e-9))
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()

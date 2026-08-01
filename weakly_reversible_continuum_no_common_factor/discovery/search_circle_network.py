#!/usr/bin/env python3
"""Random structured search for a reversible network equilibrated on a circle.

The target curve is

    z = 1,  (x-2)^2 + (y-2)^2 = 1,

with rational parametrization

    x=(3+t^2)/(1+t^2),
    y=(2+2t+2t^2)/(1+t^2),
    z=1.

For each sparse connected undirected graph, both directed rates are variables.
We maximize the smallest normalized rate subject to the exact (integer)
coefficient equations obtained after parametrization.  A positive optimum is a
candidate reversible realization.
"""

from __future__ import annotations

import argparse
import itertools
import random

import numpy as np
from numpy.polynomial.polynomial import polymul, polypow
from scipy.optimize import linprog


def complexes_through_degree(degree: int):
    return [
        (a, b, c)
        for a in range(degree + 1)
        for b in range(degree + 1 - a)
        for c in range(degree + 1 - a - b)
    ]


def curve_numerators(complexes):
    denominator_degree = max(a + b for a, b, _ in complexes)
    numerators = []
    for a, b, _ in complexes:
        polynomial = np.array([1.0])
        for base, exponent in (
            ([3, 0, 1], a),
            ([2, 2, 2], b),
            ([1, 0, 1], denominator_degree - a - b),
        ):
            polynomial = polymul(
                polynomial, polypow(np.asarray(base, dtype=float), exponent)
            )
        numerators.append(
            np.pad(polynomial, (0, 2 * denominator_degree + 1 - len(polynomial)))
        )
    return numerators


def constraints(complexes, numerators, edges):
    arcs = [(i, j) for i, j in edges for (i, j) in ((i, j), (j, i))]
    rows = []
    for coordinate in range(3):
        for coefficient in range(len(numerators[0])):
            row = [
                (complexes[j][coordinate] - complexes[i][coordinate])
                * numerators[i][coefficient]
                for i, j in arcs
            ]
            if any(row):
                rows.append(row)
    return np.asarray(rows), arcs


def maximize_minimum_rate(matrix):
    arc_count = matrix.shape[1]
    # Variables are normalized rates followed by their common lower bound tau.
    objective = np.r_[np.zeros(arc_count), -1.0]
    equalities = np.block(
        [
            [matrix, np.zeros((matrix.shape[0], 1))],
            [np.ones((1, arc_count)), np.zeros((1, 1))],
        ]
    )
    rhs = np.r_[np.zeros(matrix.shape[0]), 1.0]
    # tau - rate_i <= 0.
    inequalities = np.hstack([-np.eye(arc_count), np.ones((arc_count, 1))])
    result = linprog(
        objective,
        A_ub=inequalities,
        b_ub=np.zeros(arc_count),
        A_eq=equalities,
        b_eq=rhs,
        bounds=[(0, None)] * arc_count + [(0, None)],
        method="highs",
        options={
            "dual_feasibility_tolerance": 1e-9,
            "primal_feasibility_tolerance": 1e-9,
        },
    )
    return result


def affine_rank(points):
    array = np.asarray(points, dtype=float)
    return np.linalg.matrix_rank(array[1:] - array[0])


def random_connected_edges(vertices, edge_count, rng):
    order = list(vertices)
    rng.shuffle(order)
    edges = []
    for index in range(1, len(order)):
        parent = rng.choice(order[:index])
        edges.append(tuple(sorted((order[index], parent))))
    all_edges = list(itertools.combinations(sorted(vertices), 2))
    remaining = list(set(all_edges) - set(edges))
    rng.shuffle(remaining)
    edges.extend(remaining[: edge_count - len(edges)])
    return sorted(edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--trials", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=20260801)
    args = parser.parse_args()

    complexes = complexes_through_degree(args.degree)
    numerators = curve_numerators(complexes)
    rng = random.Random(args.seed)

    for trial in range(1, args.trials + 1):
        vertex_count = rng.randint(5, len(complexes))
        vertices = sorted(rng.sample(range(len(complexes)), vertex_count))
        if affine_rank([complexes[index] for index in vertices]) < 3:
            continue
        maximum_edges = vertex_count * (vertex_count - 1) // 2
        edge_count = rng.randint(vertex_count - 1, min(maximum_edges, vertex_count + 5))
        edges = random_connected_edges(vertices, edge_count, rng)
        matrix, arcs = constraints(complexes, numerators, edges)
        result = maximize_minimum_rate(matrix)
        if result.success and result.x[-1] > 1e-9:
            print("FOUND on trial", trial, "tau", result.x[-1])
            print("complexes", [(index, complexes[index]) for index in vertices])
            print("edges", [(complexes[i], complexes[j]) for i, j in edges])
            print("rates", result.x[:-1].tolist())
            print("maximum residual", np.max(np.abs(matrix @ result.x[:-1])))
            return
        if trial % 5000 == 0:
            print("completed", trial)
    print("no candidate in", args.trials, "trials")


if __name__ == "__main__":
    main()

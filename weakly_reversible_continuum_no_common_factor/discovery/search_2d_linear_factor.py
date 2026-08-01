#!/usr/bin/env python3
"""Exploratory LP search for reversible 2-species fields vanishing on z=x+1.

This is a discovery aid, not a verifier.  For a chosen complex set and
undirected graph it builds the exact homogeneous linear constraints on all
directed positive rate constants and asks whether their normalized kernel has
an interior point.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

import numpy as np
from scipy.optimize import linprog


def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    ans = 1
    for j in range(1, k + 1):
        ans = ans * (n + 1 - j) // j
    return ans


def constraint_matrix(complexes, edges):
    arcs = [(i, j) for i, j in edges for (i, j) in ((i, j), (j, i))]
    max_degree = max(a + b for a, b in complexes)
    rows = []
    for coordinate in range(2):
        for degree in range(max_degree + 1):
            row = []
            for i, j in arcs:
                a, b = complexes[i]
                delta = complexes[j][coordinate] - complexes[i][coordinate]
                # x^a (x+1)^b: coefficient of x^degree.
                row.append(delta * binomial(b, degree - a))
            if any(row):
                rows.append(row)
    return np.asarray(rows, dtype=float), arcs


def interior_solution(complexes, edges, epsilon=1e-7):
    matrix, arcs = constraint_matrix(complexes, edges)
    count = len(arcs)
    equalities = np.vstack([matrix, np.ones((1, count))])
    rhs = np.zeros(equalities.shape[0])
    rhs[-1] = 1.0
    result = linprog(
        np.zeros(count),
        A_eq=equalities,
        b_eq=rhs,
        bounds=[(epsilon, None)] * count,
        method="highs",
    )
    return result, arcs, matrix


def main():
    for max_total_degree in range(2, 7):
        complexes = [
            (a, b)
            for a in range(max_total_degree + 1)
            for b in range(max_total_degree + 1 - a)
        ]
        edges = list(combinations(range(len(complexes)), 2))
        result, arcs, matrix = interior_solution(complexes, edges)
        print(
            "degree",
            max_total_degree,
            "complexes",
            len(complexes),
            "arcs",
            len(arcs),
            "rank",
            np.linalg.matrix_rank(matrix),
            "success",
            result.success,
        )
        if result.success:
            print("minimum normalized rate", result.x.min())
            break


if __name__ == "__main__":
    main()

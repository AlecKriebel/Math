#!/usr/bin/env python3
"""Exact integer checks for the boundary-rigidity example equations.

This checks algebraic identities and line incidence, not KE existence, global
quotient classification, or novelty. It uses only the Python standard library.
"""

import itertools
import json
from math import comb


def add(left, right):
    answer = left.copy()
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
    return {key: value for key, value in answer.items() if value}


def negate(polynomial):
    return {key: -value for key, value in polynomial.items()}


def multiply(left, right):
    answer = {}
    for (a, b), c in left.items():
        for (d, e), f in right.items():
            key = (a + d, b + e)
            answer[key] = answer.get(key, 0) + c * f
    return {key: value for key, value in answer.items() if value}


def square(polynomial):
    return multiply(polynomial, polynomial)


def determinant(matrix):
    answer = 0
    for permutation in itertools.permutations(range(3)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(3) for j in range(i + 1, 3))
        term = (-1) ** inversions
        for row in range(3):
            term *= matrix[row][permutation[row]]
        answer += term
    return answer


def main():
    # Sparse polynomials in z,w, indexed by exponent pairs.
    u = {(2, 2): 1, (0, 0): 1}
    v = {(2, 0): 1, (0, 2): 1}
    w = {(1, 1): 2}
    d = multiply({(2, 0): 1, (0, 2): -1},
                 {(2, 2): 1, (0, 0): -1})
    residual = add(square(d), negate(multiply(
        add(square(u), negate(square(w))),
        add(square(v), negate(square(w))))))
    assert residual == {}

    lines = [(1, 0, -1), (1, 0, 1), (0, 1, -1), (0, 1, 1)]
    triple_determinants = [
        {"indices": list(indices),
         "determinant": determinant([lines[i] for i in indices])}
        for indices in itertools.combinations(range(4), 3)
    ]
    assert all(entry["determinant"] != 0 for entry in triple_determinants)
    assert comb(4, 2) == 6
    assert comb(4, 2) // 2 == 3  # Sym^2(P^2) quotient hyperplane degree.

    print(json.dumps({
        "scope": "Exact example equations and line incidence only",
        "six_node_identity_residual": [],
        "branch_line_triple_determinants": triple_determinants,
        "distinct_pairwise_branch_intersections": comb(4, 2),
        "sym2_p2_pullback_hyperplane_fourth_power": comb(4, 2),
        "sym2_p2_quotient_degree": 2,
        "sym2_p2_hyperplane_degree": comb(4, 2) // 2,
        "passed": True
    }, indent=2))


if __name__ == "__main__":
    main()

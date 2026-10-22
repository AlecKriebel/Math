#!/usr/bin/env python3
"""Exact finite-graph check of the claimed recurrence, using rational elimination."""
from fractions import Fraction as F
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def graph(q, m, n):
    spine = [('s', i) for i in range(n + 1)]
    parent = {spine[i]: spine[i + 1] for i in range(n)}
    parent[spine[-1]] = None
    for i in range(n):
        for child in range(q if i == 0 else q - 1):
            branch_root = (i, child, ())
            parent[branch_root] = spine[i]
            words = [()]
            for word in words:
                if len(word) < m:
                    for symbol in range(q):
                        next_word = word + (symbol,)
                        words.append(next_word)
                        parent[(i, child, next_word)] = (i, child, word)
    vertices = list(parent)
    index = {u: k for k, u in enumerate(vertices)}
    edges = set()
    for u, p in parent.items():
        if p is not None:
            edges.add(tuple(sorted((index[u], index[p]))))
            pp = parent[p]
            if pp is not None:
                edges.add(tuple(sorted((index[u], index[pp]))))
    return len(vertices), edges


def resistances(vertices, edges):
    # Ground vertex 0. Eliminate all other vertices simultaneously, with two
    # RHS columns for unit sources at vertices 1 and 2. No series recurrence.
    N = vertices - 1
    matrix = [[F(0) for _ in range(N + 2)] for _ in range(N)]
    for u, v in edges:
        for a, b in ((u, v), (v, u)):
            if a > 0:
                matrix[a - 1][a - 1] += 1
                if b > 0:
                    matrix[a - 1][b - 1] -= 1
    matrix[0][N] = 1
    matrix[1][N + 1] = 1
    for column in range(N):
        pivot = matrix[column][column]
        require(pivot > 0, 'nonpositive grounded-Laplacian pivot')
        for row in range(column + 1, N):
            if not matrix[row][column]:
                continue
            coefficient = matrix[row][column] / pivot
            for j in range(column + 1, N + 2):
                matrix[row][j] -= coefficient * matrix[column][j]
            matrix[row][column] = 0
    solutions = []
    for rhs in range(2):
        solution = [F(0)] * N
        for row in reversed(range(N)):
            solution[row] = (matrix[row][N + rhs] - sum(matrix[row][j] * solution[j] for j in range(row + 1, N))) / matrix[row][row]
        solutions.append(solution[rhs])
    return solutions


results = []
for q in (2, 3):
    for m in (0, 1, 2):
        for n in (2, 3, 4):
            vertices, edges = graph(q, m, n)
            actual = resistances(vertices, edges)
            k = F(1, 2)
            for _ in range(m):
                k = (1 + q * k) / (2 + q * k)
            A, c = 1 + q * k, 1 + (q - 1) * k
            B = c
            for _ in range(n - 2):
                B = c + B / (1 + B)
            predicted = [1 / (A + B / (1 + B)), 1 / (1 + A * B / (A + B))]
            require(actual == predicted, f'reduction failure at q={q}, m={m}, n={n}')
            results.append({'q': q, 'm': m, 'n': n, 'vertices': vertices, 'edges': len(edges), 'parent_resistance': str(actual[0]), 'grandparent_resistance': str(actual[1])})
print(json.dumps({'verdict': 'PASS', 'exact_finite_instances': len(results), 'cases': results}, indent=2))

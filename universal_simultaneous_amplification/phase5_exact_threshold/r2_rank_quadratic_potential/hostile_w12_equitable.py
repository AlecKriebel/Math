#!/usr/bin/env python3
"""Sparse discovery solver for the combined equitable W12 certificate.

This is a hostile-search implementation, not a theorem verifier.  For a
class-symmetric weighted graph it solves the exact symmetry-reduced *form*
of the primal with floating arithmetic, retaining on every rank

    constants + all invariant one-marks + E1 + s^T K0 s.

The two quadratic columns are omitted on ranks where they are affine in
the one-marks.  Unlike the older discovery script, this implementation
uses an explicit independent column basis and a sparse drift matrix, so
quotients with tens of thousands of states can be screened without a
dense singular-value decomposition.  Any positive gap must still be
rebuilt and certified independently over the rationals.
"""

from __future__ import annotations

from itertools import product

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix


class W12Equitable:
    def __init__(self, sizes: tuple[int, ...]):
        self.sizes = tuple(sizes)
        self.q = len(sizes)
        self.n = sum(sizes)
        self.empty = (0,) * self.q
        self.full = self.sizes
        all_states = list(product(*(range(size + 1) for size in sizes)))
        self.transient = [
            state
            for state in all_states
            if state not in (self.empty, self.full)
        ]
        self.state_index = {state: j for j, state in enumerate(self.transient)}

        self.keys: list[tuple[int, object]] = []
        for rank in range(1, self.n):
            self.keys.append((rank, "constant"))
            self.keys.extend((rank, a) for a in range(self.q - 1))
            if 2 <= rank <= self.n - 2:
                self.keys.extend(((rank, "internal"), (rank, "collision")))
        self.keys.append((self.n, "constant"))
        self.column = {key: j for j, key in enumerate(self.keys)}
        self.baseline = (
            (self.n - 1) * 2 ** (self.n - 2)
            / (self.n * (2 ** (self.n - 1) - 1))
        )

    def _graph_data(self, weights: np.ndarray):
        assert weights.shape == (self.q, self.q)
        assert np.all(weights >= 0)
        assert np.allclose(weights, weights.T)
        degrees = np.array([
            (self.sizes[a] - 1) * weights[a, a]
            + sum(
                self.sizes[b] * weights[a, b]
                for b in range(self.q)
                if b != a
            )
            for a in range(self.q)
        ])
        assert np.all(degrees > 0)
        total_degree = float(np.dot(self.sizes, degrees))
        pi_per_vertex = degrees / total_degree
        return degrees, total_degree, pi_per_vertex

    def solve(self, weights: np.ndarray):
        degrees, total_degree, pi = self._graph_data(weights)
        dimension = len(self.keys)

        def features(state: tuple[int, ...]):
            rank = sum(state)
            values: dict[int, float] = {}
            if rank == 0:
                return values
            if rank == self.n:
                values[self.column[(self.n, "constant")]] = 1.0
                return values
            values[self.column[(rank, "constant")]] = 1.0
            for a in range(self.q - 1):
                if state[a]:
                    values[self.column[(rank, a)]] = float(state[a])
            if 2 <= rank <= self.n - 2:
                internal = sum(
                    weights[a, a] * state[a] * (state[a] - 1) / 2
                    for a in range(self.q)
                ) + sum(
                    weights[a, b] * state[a] * state[b]
                    for a in range(self.q)
                    for b in range(a + 1, self.q)
                )
                collision = 0.0
                for a, size in enumerate(self.sizes):
                    weighted_mutants = sum(
                        weights[a, b] * state[b] for b in range(self.q)
                    )
                    if state[a]:
                        x = (weighted_mutants - weights[a, a]) / degrees[a]
                        collision += state[a] * pi[a] * x * (1 - x)
                    if state[a] < size:
                        x = weighted_mutants / degrees[a]
                        collision += (size - state[a]) * pi[a] * x * (1 - x)
                values[self.column[(rank, "internal")]] = internal / total_degree
                values[self.column[(rank, "collision")]] = collision
            return values

        cache = {self.empty: {}}
        cache.update({state: features(state) for state in self.transient})
        cache[self.full] = features(self.full)

        objective = np.zeros(dimension)
        for a, size in enumerate(self.sizes):
            singleton = tuple(int(b == a) for b in range(self.q))
            for column, value in cache[singleton].items():
                objective[column] += size * value / self.n

        row_indices: list[int] = []
        column_indices: list[int] = []
        data: list[float] = []
        for row_index, state in enumerate(self.transient):
            events = []
            total = 0.0
            for a, size in enumerate(self.sizes):
                weighted_mutants = sum(
                    weights[a, b] * state[b] for b in range(self.q)
                )
                if state[a] < size:
                    x = weighted_mutants / degrees[a]
                    rate = (size - state[a]) * 2 * x / (1 + x)
                    if rate:
                        target = list(state)
                        target[a] += 1
                        events.append((tuple(target), rate))
                        total += rate
                if state[a]:
                    x = (weighted_mutants - weights[a, a]) / degrees[a]
                    rate = state[a] * (1 - x) / (1 + x)
                    if rate:
                        target = list(state)
                        target[a] -= 1
                        events.append((tuple(target), rate))
                        total += rate
            assert total > 0
            drift: dict[int, float] = {}
            current = cache[state]
            for target, rate in events:
                scale = rate / total
                for column, value in cache[target].items():
                    drift[column] = drift.get(column, 0.0) + scale * value
                for column, value in current.items():
                    drift[column] = drift.get(column, 0.0) - scale * value
            for column, value in drift.items():
                if value:
                    row_indices.append(row_index)
                    column_indices.append(column)
                    data.append(value)

        inequalities = csr_matrix(
            (data, (row_indices, column_indices)),
            shape=(len(self.transient), dimension),
        )
        boundary = np.zeros((1, dimension))
        boundary[0, self.column[(self.n, "constant")]] = 1.0
        return linprog(
            objective,
            A_ub=inequalities,
            b_ub=np.zeros(len(self.transient)),
            A_eq=boundary,
            b_eq=np.ones(1),
            bounds=[(None, None)] * dimension,
            method="highs",
        )

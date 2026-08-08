#!/usr/bin/env python3
"""Independent rare-coupling trace for clique-pendants plus K2 satellites.

The center module is a unit clique on ``C`` vertices with ``m`` unit hub
pendants.  There are ``q`` identical K2 modules of internal edge weight
``C/sigma``.  Every K2 vertex is joined to every center-module vertex by a
common coupling epsilon, and epsilon tends to zero after ``C,m,q`` are fixed.

The center-module singleton fixation values and inverse-degree weighted
values are solved from their exact three-count chain.  These are then
inserted into the four rare-invasion rates derived directly from the update
rules.  The resulting two-coordinate star trace has only ``2(q+1)`` states.

This implementation is independent of ``hybrid_pair_pendant_search.py``:
the latter solves the full five-coordinate chain at positive epsilon.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from equitable_search import complete_baseline


def center_singletons(core: int, pendants: int, fitness: float, rule: str):
    c, m = core - 1, pendants
    empty = (0, 0, 0)
    full = (1, c, m)
    states = [
        (h, i, j)
        for h in (0, 1)
        for i in range(c + 1)
        for j in range(m + 1)
        if (h, i, j) not in (empty, full)
    ]
    index = {state: row for row, state in enumerate(states)}
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(len(states))
    hub_degree = c + m
    for state, row in index.items():
        h, i, j = state
        moves = []

        def add(target, rate):
            if rate > 0:
                moves.append((target, float(rate)))

        if rule == "Bd":
            if i < c:
                add((h, i + 1, j), fitness * (c - i) * (h / hub_degree + i / c))
            if i:
                add((h, i - 1, j), i * ((1 - h) / hub_degree + (c - i) / c))
            if h == 0:
                add((1, i, j), fitness * (i / c + j))
            else:
                add((0, i, j), (c - i) / c + m - j)
            if h and j < m:
                add((h, i, j + 1), fitness * (m - j) / hub_degree)
            if not h and j:
                add((h, i, j - 1), j / hub_degree)
        elif rule == "dB":
            if i < c:
                mutant = h + i
                resident = c - mutant
                add((h, i + 1, j), (c - i) * fitness * mutant / (fitness * mutant + resident))
            if i:
                mutant = h + i - 1
                resident = c - mutant
                add((h, i - 1, j), i * resident / (fitness * mutant + resident))
            mutant = i + j
            resident = hub_degree - mutant
            if h == 0 and mutant:
                add((1, i, j), fitness * mutant / (fitness * mutant + resident))
            if h == 1 and resident:
                add((0, i, j), resident / (fitness * mutant + resident))
            if h and j < m:
                add((h, i, j + 1), m - j)
            if not h and j:
                add((h, i, j - 1), j)
        else:
            raise ValueError(rule)
        total = sum(rate for _, rate in moves)
        rows.append(row); columns.append(row); entries.append(1.0)
        for target, rate in moves:
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target != empty:
                rows.append(row); columns.append(index[target]); entries.append(-probability)
    matrix = coo_matrix(
        (entries, (rows, columns)), shape=(len(states), len(states))
    ).tocsr()
    harmonic = spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ harmonic - rhs)))
    if residual > 5e-9:
        raise FloatingPointError(residual)
    hub = float(harmonic[index[(1, 0, 0)]])
    ordinary = float(harmonic[index[(0, 1, 0)]])
    leaf = float(harmonic[index[(0, 0, 1)]]) if m else 0.0
    uniform = (hub + c * ordinary + m * leaf) / (core + m)
    # Internal degrees in the isolated center module.
    inverse_degree_sum = 1.0 / hub_degree + 1.0 + m
    inverse_weighted = hub / hub_degree + ordinary + m * leaf
    return {
        "hub": hub,
        "ordinary": ordinary,
        "leaf": leaf,
        "uniform": uniform,
        "core_uniform": (hub + c * ordinary) / core,
        "I": inverse_degree_sum,
        "I_core": 1.0 / hub_degree + 1.0,
        "J": inverse_weighted,
        "J_core": hub / hub_degree + ordinary,
        "residual": residual,
    }


def macro_fixation(q: int, A: float, D: float, B: float, C: float):
    """Return center-start and one-leaf-start fixation in the star trace."""
    empty = (0, 0)
    full = (1, q)
    states = [
        (h, k)
        for h in (0, 1)
        for k in range(q + 1)
        if (h, k) not in (empty, full)
    ]
    index = {state: row for row, state in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    rhs = np.zeros(len(states))
    for state, row in index.items():
        h, k = state
        moves = []
        if h == 0:
            if k:
                moves.append(((1, k), k * A))
                moves.append(((0, k - 1), k * D))
        else:
            if k < q:
                moves.append(((1, k + 1), (q - k) * B))
                moves.append(((0, k), (q - k) * C))
        total = sum(rate for _, rate in moves)
        matrix[row, row] = 1.0
        for target, rate in moves:
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target != empty:
                matrix[row, index[target]] -= probability
    harmonic = np.linalg.solve(matrix, rhs)
    center_start = float(harmonic[index[(1, 0)]]) if q else 1.0
    pair_start = float(harmonic[index[(0, 1)]]) if q else 0.0
    return center_start, pair_start


@dataclass(frozen=True)
class TraceHybrid:
    core: int
    pair_modules: int
    pendants: int
    sigma: float
    fitness: float = 1.5

    @property
    def order(self):
        return self.core + self.pendants + 2 * self.pair_modules

    def fixation(self, rule: str):
        r = self.fitness
        forward = center_singletons(self.core, self.pendants, r, rule)
        reverse = center_singletons(self.core, self.pendants, 1.0 / r, rule)
        size_h = self.core + self.pendants
        pair_degree = self.core / self.sigma
        if rule == "Bd":
            pair_I = 2.0 / pair_degree
            pair_forward = r / (r + 1.0)
            pair_reverse = 1.0 / (r + 1.0)
            # The weak pair--center bundle touches clique vertices only, not
            # the hub pendants.  Therefore invasion establishment is uniform
            # over the clique portal and source pressure uses only clique
            # inverse degrees.
            A = self.core * r * pair_I * forward["core_uniform"]
            D = 2.0 * forward["I_core"] * pair_reverse
            B = 2.0 * r * forward["I_core"] * pair_forward
            C = self.core * pair_I * reverse["core_uniform"]
            local_pair = pair_forward
        else:
            pair_J = 1.0 / pair_degree
            A = 2.0 * r * forward["J_core"]
            D = self.core / r * pair_J
            B = self.core * r * pair_J
            C = 2.0 / r * reverse["J_core"]
            local_pair = 0.5
        center_macro, pair_macro = macro_fixation(
            self.pair_modules, A, D, B, C
        )
        rho = (
            size_h * forward["uniform"] * center_macro
            + 2.0 * self.pair_modules * local_pair * pair_macro
        ) / self.order
        return rho, {
            "forward": forward,
            "reverse": reverse,
            "macro_center": center_macro,
            "macro_pair": pair_macro,
            "rates": (A, D, B, C),
        }

    def score(self):
        bd, bd_data = self.fixation("Bd")
        db, db_data = self.fixation("dB")
        x = bd / complete_baseline(self.order, self.fitness, "Bd")
        y = db / complete_baseline(self.order, self.fitness, "dB")
        return {
            "Bd": bd,
            "dB": db,
            "x": x,
            "y": y,
            "M": min(x, y),
            "scaled_x": self.order / self.pair_modules * (x - 1)
            if self.pair_modules else 0.0,
            "scaled_y": self.order / self.pair_modules * (y - 1)
            if self.pair_modules else 0.0,
            "Bd_macro": (bd_data["macro_center"], bd_data["macro_pair"]),
            "dB_macro": (db_data["macro_center"], db_data["macro_pair"]),
        }


def predicted_coefficients(r: float, sigma: float, lam: float):
    f_bd = 2.0 * (sigma - 1.0) / (1.0 + sigma * (r * r - 1.0))
    f_db = 2.0 * (r * (2.0 - r) - sigma) / (
        sigma + 2.0 * r * (r - 1.0)
    )
    return f_bd + lam / (r - 1.0), f_db - lam


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=int, default=800)
    parser.add_argument("--pairs", type=int, default=20)
    parser.add_argument("--pendants", type=int, default=15)
    parser.add_argument("--sigma", type=float, default=19 / 137)
    parser.add_argument("--fitness", type=float, default=1.5)
    args = parser.parse_args()
    model = TraceHybrid(
        args.core, args.pairs, args.pendants, args.sigma, args.fitness
    )
    score = model.score()
    predicted = predicted_coefficients(
        args.fitness, args.sigma, args.pendants / args.pairs
    )
    print(json.dumps({
        "parameters": model.__dict__,
        **score,
        "predicted_scaled": predicted,
    }, indent=2))


if __name__ == "__main__":
    main()

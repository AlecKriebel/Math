#!/usr/bin/env python3
"""Lumped screen for a hybrid strong-pair / hub-pendant construction.

The graph has a unit clique on ``C`` vertices, one distinguished clique hub,
``q`` exchangeable disjoint strong pairs, and ``k`` exchangeable pendants at
the hub.  Each pair vertex is joined to every clique vertex by weight
``epsilon``; there are no edges between distinct pairs or from pairs to
pendants.  Pair internal weight is ``gamma*C`` and pendant weight is ``tau``.

A state is ``(h,i,u,v,l)``: hub type, mutant ordinary-clique count, number of
mixed pairs, number of all-mutant pairs, and mutant pendant count.  This is
a strong orbit lumping under ``S_(C-1) x (S_2 wr S_q) x S_k``.  Every rate
below is the aggregate of labelled update events from the Bd or dB rule.

Floating results are discovery only.  The intended singular regime is
``q,k -> infinity``, ``q/C,k/C -> 0``, with ``k/q`` near 0.73.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from equitable_search import complete_baseline


R = 1.5


@dataclass(frozen=True)
class Hybrid:
    core: int
    pairs: int
    pendants: int
    gamma: float
    epsilon: float
    tau: float = 1.0

    @property
    def order(self):
        return self.core + 2 * self.pairs + self.pendants

    def states(self):
        answer = []
        for h in (0, 1):
            for i in range(self.core):
                for v in range(self.pairs + 1):
                    for u in range(self.pairs - v + 1):
                        for l in range(self.pendants + 1):
                            state = (h, i, u, v, l)
                            if state not in (self.empty, self.full):
                                answer.append(state)
        return answer

    @property
    def empty(self):
        return (0, 0, 0, 0, 0)

    @property
    def full(self):
        return (1, self.core - 1, 0, self.pairs, self.pendants)

    def rates(self, state, rule: str):
        h, i, u, v, l = state
        c = self.core - 1
        q, k = self.pairs, self.pendants
        n0 = q - u - v
        mutant_pair_vertices = u + 2 * v
        resident_pair_vertices = 2 * q - mutant_pair_vertices
        W, e, t = self.gamma * self.core, self.epsilon, self.tau
        d_h = c + 2 * q * e + k * t
        d_o = c + 2 * q * e
        d_p = W + self.core * e
        moves = []

        def add(target, rate):
            if rate > 0:
                moves.append((target, float(rate)))

        if rule == "Bd":
            # Distinguished clique hub.
            if h == 0:
                incoming = i / d_o + mutant_pair_vertices * e / d_p + l * t / t
                add((1, i, u, v, l), R * incoming)
            else:
                incoming = (c - i) / d_o + resident_pair_vertices * e / d_p + (k - l)
                add((0, i, u, v, l), incoming)

            # Ordinary clique vertices.
            if i < c:
                incoming = h / d_h + i / d_o + mutant_pair_vertices * e / d_p
                add((h, i + 1, u, v, l), R * (c - i) * incoming)
            if i:
                incoming = (1 - h) / d_h + (c - i) / d_o + resident_pair_vertices * e / d_p
                add((h, i - 1, u, v, l), i * incoming)

            # Pair vertices, separated by the partner's type.
            mutant_bulk = e * (h / d_h + i / d_o)
            resident_bulk = e * ((1 - h) / d_h + (c - i) / d_o)
            if n0:
                add((h, i, u + 1, v, l), R * 2 * n0 * mutant_bulk)
            if u:
                add((h, i, u - 1, v + 1, l), R * u * (mutant_bulk + W / d_p))
                add((h, i, u - 1, v, l), u * (resident_bulk + W / d_p))
            if v:
                add((h, i, u + 1, v - 1, l), 2 * v * resident_bulk)

            # Pendant targets; their source is the hub.
            if h and l < k:
                add((h, i, u, v, l + 1), R * (k - l) * t / d_h)
            if not h and l:
                add((h, i, u, v, l - 1), l * t / d_h)

        elif rule == "dB":
            # Hub death.
            mm = i + mutant_pair_vertices * e + l * t
            rm = (c - i) + resident_pair_vertices * e + (k - l) * t
            if h == 0 and mm:
                add((1, i, u, v, l), R * mm / (R * mm + rm))
            if h == 1 and rm:
                add((0, i, u, v, l), rm / (R * mm + rm))

            # Ordinary clique death.
            if i < c:
                mm = h + i + mutant_pair_vertices * e
                rm = d_o - mm
                add((h, i + 1, u, v, l), (c - i) * R * mm / (R * mm + rm))
            if i:
                mm = h + (i - 1) + mutant_pair_vertices * e
                rm = d_o - mm
                add((h, i - 1, u, v, l), i * rm / (R * mm + rm))

            mutant_bulk = e * (h + i)
            resident_bulk = e * ((1 - h) + (c - i))
            if n0 and mutant_bulk:
                add(
                    (h, i, u + 1, v, l),
                    2 * n0 * R * mutant_bulk / (R * mutant_bulk + W + resident_bulk),
                )
            if u:
                add(
                    (h, i, u - 1, v + 1, l),
                    u * R * (W + mutant_bulk) / (R * (W + mutant_bulk) + resident_bulk),
                )
                add(
                    (h, i, u - 1, v, l),
                    u * (W + resident_bulk) / (R * mutant_bulk + W + resident_bulk),
                )
            if v and resident_bulk:
                add(
                    (h, i, u + 1, v - 1, l),
                    2 * v * resident_bulk / (R * (W + mutant_bulk) + resident_bulk),
                )

            # Pendant death copies the unique hub neighbor with certainty.
            if h and l < k:
                add((h, i, u, v, l + 1), k - l)
            if not h and l:
                add((h, i, u, v, l - 1), l)
        else:
            raise ValueError(rule)
        return moves

    def fixation(self, rule: str):
        states = self.states()
        index = {state: row for row, state in enumerate(states)}
        rows: list[int] = []
        columns: list[int] = []
        entries: list[float] = []
        rhs = np.zeros(len(states))
        for state, row in index.items():
            moves = self.rates(state, rule)
            total = sum(rate for _, rate in moves)
            if not total > 1e-280:
                raise FloatingPointError((state, total))
            rows.append(row); columns.append(row); entries.append(1.0)
            for target, rate in moves:
                probability = rate / total
                if target == self.full:
                    rhs[row] += probability
                elif target != self.empty:
                    rows.append(row); columns.append(index[target]); entries.append(-probability)
        matrix = coo_matrix(
            (entries, (rows, columns)), shape=(len(states), len(states))
        ).tocsr()
        harmonic = spsolve(matrix, rhs)
        residual = float(np.max(np.abs(matrix @ harmonic - rhs)))
        if residual > 5e-8 or not np.all(np.isfinite(harmonic)):
            raise FloatingPointError(f"residual {residual}")
        singleton_sum = harmonic[index[(1, 0, 0, 0, 0)]]
        singleton_sum += (self.core - 1) * harmonic[index[(0, 1, 0, 0, 0)]]
        if self.pairs:
            singleton_sum += 2 * self.pairs * harmonic[index[(0, 0, 1, 0, 0)]]
        if self.pendants:
            singleton_sum += self.pendants * harmonic[index[(0, 0, 0, 0, 1)]]
        return float(singleton_sum / self.order), residual, len(states)

    def score(self):
        bd, residual_b, count = self.fixation("Bd")
        db, residual_d, _ = self.fixation("dB")
        x = bd / complete_baseline(self.order, R, "Bd")
        y = db / complete_baseline(self.order, R, "dB")
        return {
            "x": x,
            "y": y,
            "M": min(x, y),
            "Bd": bd,
            "dB": db,
            "states": count,
            "residual": max(residual_b, residual_d),
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=int, default=60)
    parser.add_argument("--pairs", type=int, default=3)
    parser.add_argument("--pendants", type=int, default=2)
    parser.add_argument("--gamma", type=float, default=7.0)
    parser.add_argument("--epsilon-power", type=float, default=4.0)
    parser.add_argument("--tau", type=float, default=1.0)
    args = parser.parse_args()
    model = Hybrid(
        args.core,
        args.pairs,
        args.pendants,
        args.gamma,
        args.core ** (-args.epsilon_power),
        args.tau,
    )
    print(json.dumps({
        "parameters": model.__dict__,
        **model.score(),
    }, indent=2))


if __name__ == "__main__":
    main()

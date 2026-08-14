from __future__ import annotations

import itertools
import random
import sys
import unittest
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from network_parser import Network, Reaction, parse_network  # noqa: E402
from mass_action_jacobian import (  # noqa: E402
    direct_symbolic_jacobian,
    factorized_jacobian,
    rates_to_flux,
    reconstruct_rates,
)


class IndependentMassActionTests(unittest.TestCase):
    def test_feature_networks(self) -> None:
        cases = [
            # Zero complex plus autocatalysis and outflow.
            {
                "species": ["X"],
                "reactions": [
                    {"source": [0], "target": [1]},
                    {"source": [1], "target": [0]},
                    {"source": [2], "target": [3]},
                    {"source": [4], "target": [3]},
                ],
            },
            # Parallel reactions, repeated sources, and rank-deficient conservation.
            {
                "species": ["A", "B"],
                "reactions": [
                    {"source": [2, 1], "target": [1, 2]},
                    {"source": [2, 1], "target": [1, 2]},
                    {"source": [0, 3], "target": [1, 2]},
                    {"source": [0, 3], "target": [1, 2]},
                ],
            },
            # High molecularity and three linkage classes.
            {
                "species": ["A", "B", "C"],
                "reactions": [
                    {"source": [9, 0, 2], "target": [10, 0, 2]},
                    {"source": [4, 5, 1], "target": [3, 5, 1]},
                    {"source": [0, 7, 0], "target": [0, 8, 0]},
                    {"source": [1, 2, 3], "target": [1, 1, 3]},
                    {"source": [2, 0, 8], "target": [2, 0, 9]},
                    {"source": [0, 1, 6], "target": [0, 1, 5]},
                ],
            },
            # Rank-zero empty reaction list.
            {"species": ["A", "B"], "reactions": []},
        ]
        for raw in cases:
            network = parse_network(raw)
            x = [sp.Rational(i + 2, i + 1) for i in range(network.n)]
            rates = [sp.Rational(i + 3, i + 2) for i in range(network.m)]
            flux = rates_to_flux(network, rates, x)
            h = [sp.simplify(1 / xi) for xi in x]
            self.assertEqual(direct_symbolic_jacobian(network, rates, x), factorized_jacobian(network, flux, h))

    def test_reconstruction_on_independent_row_balances(self) -> None:
        rng = random.Random(20260813)
        for n in range(1, 6):
            for _ in range(80):
                reactions: list[dict] = []
                flux: list[sp.Rational] = []
                for i in range(n):
                    # Two upward reactions and one downward reaction, with arbitrary
                    # source complexes.  This guarantees the rowwise balance.
                    y1 = [rng.randint(0, 6) for _ in range(n)]
                    y2 = [rng.randint(0, 6) for _ in range(n)]
                    y0 = [rng.randint(0, 6) for _ in range(n)]
                    y0[i] = max(y0[i], 1)
                    t1 = y1.copy(); t1[i] += 1
                    t2 = y2.copy(); t2[i] += 1
                    td = y0.copy(); td[i] -= 1
                    reactions.extend([
                        {"source": y1, "target": t1},
                        {"source": y2, "target": t2},
                        {"source": y0, "target": td},
                    ])
                    u = sp.Rational(rng.randint(1, 9), rng.randint(1, 5))
                    w = sp.Rational(rng.randint(1, 9), rng.randint(1, 5))
                    flux.extend([u, w, u + w])
                raw = {"species": [f"X{i}" for i in range(n)], "reactions": reactions}
                network = parse_network(raw)
                v = sp.Matrix(flux)
                self.assertEqual(network.stoichiometric_matrix() * v, sp.zeros(n, 1))
                x = [sp.Rational(rng.randint(1, 7), rng.randint(1, 7)) for _ in range(n)]
                rates = reconstruct_rates(network, flux, x)
                self.assertTrue(all(rate > 0 for rate in rates))
                self.assertEqual(rates_to_flux(network, rates, x), v)
                h = [sp.simplify(1 / xi) for xi in x]
                self.assertEqual(direct_symbolic_jacobian(network, rates, x), factorized_jacobian(network, flux, h))

    def test_basis_similarity(self) -> None:
        rng = random.Random(20260813)
        for n in range(2, 7):
            for s in range(1, n + 1):
                for _ in range(20):
                    while True:
                        B = sp.Matrix(n, s, [rng.randint(-4, 4) for _ in range(n * s)])
                        if B.rank() == s:
                            break
                    # Select an exact left inverse.
                    _, row_pivots = B.T.rref()
                    rows = list(row_pivots[:s])
                    inv = B.extract(rows, range(s)).inv()
                    C = sp.zeros(s, n)
                    for local, row in enumerate(rows):
                        C[:, row] = inv[:, local]
                    R = sp.Matrix(s, s, [sp.Rational(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(s * s)])
                    J = B * R * C
                    while True:
                        T = sp.Matrix(s, s, [rng.randint(-3, 3) for _ in range(s * s)])
                        if T.det() != 0:
                            break
                    B2 = B * T
                    C2 = T.inv() * C
                    reduced1 = C * J * B
                    reduced2 = C2 * J * B2
                    self.assertEqual(reduced1, R)
                    self.assertEqual(reduced2, T.inv() * R * T)


if __name__ == "__main__":
    unittest.main(verbosity=2)

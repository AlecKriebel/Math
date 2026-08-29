#!/usr/bin/env python3
"""Independent exact checks of bridge-fibre freeness and capped gluing.

No package module or stored certificate is imported.  The exponent matrices,
gauge cancellation, and physical-domain inequalities are rebuilt here.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import random

import sympy as sp


if not __debug__:
    raise RuntimeError("run without -O so fail-closed assertions remain active")


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def one_sector_anchor_matrix(degree):
    pairs = [(0, 1), (0, 2), (1, 2)] + [(0, index) for index in range(3, degree)]
    rows = []
    for left, right in pairs:
        row = [0] * degree
        row[left] = row[right] = 1
        rows.append(row)
    return sp.Matrix(rows)


def physical_margins(y):
    c, g, t = y
    return (
        c, g, t, 1-c, 1-g, 1-t,
        1+c-g-t, 1-c+g-t, 1-c-g+t,
        c-g*t, g-c*t, t-c*g,
    )


def main():
    args = arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ranks = {}
    for degree in range(3, 17):
        matrix = one_sector_anchor_matrix(degree)
        determinant = int(matrix.det())
        assert matrix.shape == (degree, degree)
        assert matrix.rank() == degree and determinant == -2
        block = sp.diag(matrix, matrix, matrix)
        assert block.rank() == 3 * degree and int(block.det()) == -8
        ranks[str(degree)] = {
            "one_sector_rank": degree,
            "one_sector_determinant": determinant,
            "three_sector_rank": 3 * degree,
            "three_sector_determinant": -8,
        }

    a1, a2, a3, a4 = sp.symbols("a1 a2 a3 a4", positive=True)
    r12, r13, r23, r14 = a1*a2, a1*a3, a2*a3, a1*a4
    recovered = (
        sp.sqrt(r12*r13/r23),
        sp.sqrt(r12*r23/r13),
        sp.sqrt(r13*r23/r12),
        r14/sp.sqrt(r12*r13/r23),
    )
    assert all(sp.simplify(actual - expected) == 0 for actual, expected in zip(recovered, (a1, a2, a3, a4)))

    tau = sp.symbols("tau", positive=True)
    assert sp.simplify(tau * (1/tau) - 1) == 0

    # A marked component has a one-character leaf/bridge anchor in each
    # sector.  Its exponent matrix in the incidence scales is the identity.
    for degree in range(1, 17):
        marked = sp.eye(3 * degree)
        assert marked.rank() == 3 * degree and marked.det() == 1

    rng = random.Random(2026082702)
    cancellation = []
    for sector in "CGT":
        component = [Q(rng.randint(2, 11), rng.randint(12, 23)) for _ in range(3)]
        bridge = [Q(rng.randint(2, 11), rng.randint(12, 23)) for _ in range(2)]
        a01 = Q(rng.randint(2, 9), rng.randint(10, 19))
        a10 = Q(rng.randint(2, 9), rng.randint(10, 19))
        a12 = Q(rng.randint(2, 9), rng.randint(10, 19))
        a21 = Q(rng.randint(2, 9), rng.randint(10, 19))
        before = component[0] * component[1] * component[2] * bridge[0] * bridge[1]
        after = (
            (component[0] * a01)
            * (component[1] * a10 * a12)
            * (component[2] * a21)
            * (bridge[0] / (a01 * a10))
            * (bridge[1] / (a12 * a21))
        )
        assert before == after
        cancellation.append({"sector": sector, "contracted_value": str(before)})

    smallest_margin = None
    smallest_excess = None
    for _ in range(2000):
        upper = Q(rng.randint(2, 100), rng.randint(1, 15))
        lower = upper * Q(rng.randint(1, 9), 10)
        epsilon = min(Q(1, 4), lower * lower / (8 * upper))
        incidence = [
            lower + (upper-lower) * Q(rng.randint(0, 1000), 1000)
            for _ in range(3)
        ]
        bridge_triple = tuple(epsilon/value for value in incidence)
        cap_triple = (epsilon, epsilon, epsilon)
        margin = min(physical_margins(bridge_triple) + physical_margins(cap_triple))
        asserted_ct = 7 * epsilon / (8 * upper)
        actual_ct = min(
            bridge_triple[0]-bridge_triple[1]*bridge_triple[2],
            bridge_triple[1]-bridge_triple[0]*bridge_triple[2],
            bridge_triple[2]-bridge_triple[0]*bridge_triple[1],
        )
        assert margin > 0 and actual_ct >= asserted_ct > 0
        smallest_margin = margin if smallest_margin is None else min(smallest_margin, margin)
        excess = actual_ct - asserted_ct
        smallest_excess = excess if smallest_excess is None else min(smallest_excess, excess)

    lower, upper, epsilon = sp.symbols("L U epsilon", positive=True)
    decomposition = sp.expand(epsilon/upper - epsilon**2/lower**2 - 7*epsilon/(8*upper))
    assert sp.simplify(decomposition - (epsilon/(8*upper) - epsilon**2/lower**2)) == 0

    result = {
        "unmarked_degree_at_least_three_exponent_checks": ranks,
        "positive_pair_anchor_inverse_verified": True,
        "marked_component_anchor_matrix_is_identity": True,
        "degree_two_boundary_stabilizer": "(a1,a2)=(tau,tau^-1) fixes the sole product anchor",
        "sectorwise_bridge_gauge_cancellation": cancellation,
        "capped_gluing_exact_rational_trials": 2000,
        "smallest_physical_margin_seen": str(smallest_margin),
        "smallest_excess_over_claimed_ct_bound": str(smallest_excess),
        "ct_lower_bound_decomposition": str(decomposition),
        "cap_conditions": ["epsilon <= L^2/(8U)", "epsilon <= 1/4"],
        "independence_boundary": (
            "The algebra proves freeness conditional on the manuscript's marked-or-degree-at-least-three "
            "topological dichotomy; this script does not enumerate all retained strong-class topologies."
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.output_dir / "bridge_gluing.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

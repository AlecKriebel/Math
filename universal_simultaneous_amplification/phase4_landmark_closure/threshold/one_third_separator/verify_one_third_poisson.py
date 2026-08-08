#!/usr/bin/env python3
"""Exact Green--Poisson audit for the one-third endpoint separator.

At fitness 3/2 put

    e_B = rho_Bd(G)/rho_Bd(K_n)-1,
    e_D = rho_dB(G)/rho_dB(K_n)-1.

The conjectured affine separator is ``e_B + 2 e_D <= 0``.  This verifier
rebuilds the weighted version of the exact tangent-square decomposition and
checks it over rational arithmetic on the saved hostile corpus.  It also
checks the clique--pendant product counterexample through its independent
strongly lumped solver.

This is a reduction and hostile audit, not a proof of the universal sign.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve()
THRESHOLD = HERE.parents[1]
HOSTILE = THRESHOLD / "endpoint_hostile_exact"
PENDANT = THRESHOLD / "clique_pendant_product_audit"
sys.path.insert(0, str(HOSTILE))
sys.path.insert(0, str(PENDANT))

import verify_balanced_poisson as balanced  # noqa: E402
from verify_clique_pendant_product import (  # noqa: E402
    complete_baselines,
    exact_fixation as pendant_fixation,
)
from verify_endpoint_candidates import hostile_corpus  # noqa: E402


Q = sp.Rational(2, 3)


def one_third_terms(weights):
    """Return the exact decomposition of ``e_B+2e_D``."""
    n = len(weights)
    full = (1 << n) - 1
    original = balanced.analyze(weights)
    z_d = balanced.green_occupation(weights, "dB")
    tangent = sp.Integer(0)
    ranks = defaultdict(lambda: [sp.Integer(0), sp.Integer(0), sp.Integer(0)])

    for state in range(1, full):
        row = state - 1
        k = state.bit_count()
        a_cut, b_cut, _, _, c_m, _, _ = balanced.state_geometry(weights, state)
        tangent_atom = sp.cancel(
            Q ** (k - 1)
            * z_d[row]
            * c_m
            * (a_cut - b_cut)
            / (n - 1)
        )
        tangent += tangent_atom
        # The weighted decomposition is
        #   T_2 = e_B - 2 X, C_2 = 2 C, N_2 = 2(-E),
        # where X is the dB tangent term accumulated above.
        ranks[k][0] -= 2 * tangent_atom

    for k, original_rank in original["ranks"].items():
        ranks[k][1] = 2 * original_rank[1]
        ranks[k][2] = 2 * original_rank[2]

    tangent = sp.cancel(tangent)
    mismatch = sp.cancel(original["excess_b"] - 2 * tangent)
    cut = sp.cancel(2 * original["cut"])
    dispersion = sp.cancel(2 * original["dispersion"])

    # Add the Bd excess to its rank-resolved tangent column.  The existing
    # verifier does not expose rank-resolved e_B, so recompute only this
    # transparent complete-harmonic drift.
    phi_b = balanced.harmonics(n, "Bd")
    baseline_b = balanced.complete_baseline(n, "Bd")
    z_b = balanced.green_occupation(weights, "Bd")
    for state in range(1, full):
        row = state - 1
        k = state.bit_count()
        ranks[k][0] += sp.cancel(
            z_b[row]
            * balanced.harmonic_drift(weights, state, "Bd", phi_b)
            / baseline_b
        )

    total = sp.cancel(mismatch + cut + dispersion)
    target = sp.cancel(original["excess_b"] + 2 * original["excess_d"])
    assert total == target
    assert dispersion <= 0
    rank_difference = sp.cancel(
        sum(sum(values) for values in ranks.values()) - total
    )
    assert rank_difference == 0, rank_difference
    return {
        "e_b": original["excess_b"],
        "e_d": original["excess_d"],
        "total": total,
        "mismatch": mismatch,
        "cut": cut,
        "dispersion": dispersion,
        "ranks": {k: tuple(map(sp.cancel, values)) for k, values in ranks.items()},
    }


def audit_pendant(c: int, m: int):
    n = c + m + 1
    baseline_b, baseline_d = complete_baselines(n)
    rho_b = pendant_fixation(c, m, "Bd")[0]
    rho_d = pendant_fixation(c, m, "dB")[0]
    x = rho_b / baseline_b
    y = rho_d / baseline_d
    slack = 1 - (x + 2 * y) / 3
    crossing = (1 - y) / (x - y)
    assert x > 1 > y
    assert crossing > sp.Rational(1, 3)
    assert slack > 0
    assert slack == (x - y) * (crossing - sp.Rational(1, 3))
    return x, y, crossing, slack


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--pendant", action="store_true")
    parser.add_argument("--c", type=int, default=31)
    parser.add_argument("--m", type=int, default=4)
    args = parser.parse_args()

    labels = None if args.all else {
        "weighted-star",
        "rationalized-nearest-five-edge",
        "exact-dB-amplifying-windmill",
        "affine-lower-multiplier-witness",
    }
    count = 0
    mismatch_positive = False
    cut_dispersion_positive = False
    rank_positive = False
    affine_lower = None
    for label, weights in hostile_corpus():
        if labels is not None and label not in labels:
            continue
        result = one_third_terms(weights)
        assert result["total"] <= 0
        mismatch_positive |= result["mismatch"] > 0
        cut_dispersion_positive |= result["cut"] + result["dispersion"] > 0
        rank_positive |= any(sum(values) > 0 for values in result["ranks"].values())
        if label == "affine-lower-multiplier-witness":
            x = 1 + result["e_b"]
            y = 1 + result["e_d"]
            affine_lower = sp.cancel((y - 1) / (y - x))
            assert x < 1 < y
            assert affine_lower > sp.Rational(177, 2000)
        print(
            f"PASS {label}: eB~{sp.N(result['e_b'], 10)}, "
            f"eD~{sp.N(result['e_d'], 10)}, "
            f"eB+2eD~{sp.N(result['total'], 10)}, "
            f"T2~{sp.N(result['mismatch'], 10)}, "
            f"C2~{sp.N(result['cut'], 10)}, "
            f"-2E~{sp.N(result['dispersion'], 10)}",
            flush=True,
        )
        count += 1

    # These flags document that the additional dB weight does not restore a
    # separately signed Green decomposition on the hostile corpus.
    assert mismatch_positive
    assert cut_dispersion_positive
    assert rank_positive
    if args.all:
        assert affine_lower is not None
        print(
            "PASS exact affine lower crossing "
            f"theta_-~{sp.N(affine_lower, 16)} > 177/2000"
        )
    print(f"PASS exact one-third Green--Poisson identity on {count} witnesses")
    print("PASS separate mismatch, cut-dispersion, and fixed-rank signs remain false")

    if args.pendant:
        x, y, crossing, slack = audit_pendant(args.c, args.m)
        print(
            f"PASS exact G(c={args.c},m={args.m}) one-third separator: "
            f"x~{float(x):.12g}, y~{float(y):.12g}, "
            f"lambda_0~{float(crossing):.12g}, slack~{float(slack):.12g}"
        )


if __name__ == "__main__":
    main()

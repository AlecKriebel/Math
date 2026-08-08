#!/usr/bin/env python3
"""Exact refutation of the strongest near-disconnected floating candidate."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve()
HOSTILE = HERE.parents[1] / "endpoint_hostile_exact"
sys.path.insert(0, str(HOSTILE))

from verify_endpoint_candidates import (  # noqa: E402
    complete_baseline,
    exact_fixation,
    graph,
)


def main():
    # A triangle on 0,1,3 and an edge 2--4, joined by the much weaker 0--4
    # edge.  A double-precision solve at a still more extreme scale reported
    # a false simultaneous and affine violation.
    weights = graph(
        5,
        [
            (0, 1, 2825),
            (0, 3, 2829),
            (0, 4, 1),
            (1, 3, 2047),
            (2, 4, 3938),
        ],
    )
    rho_b = exact_fixation(weights, "Bd")
    rho_d = exact_fixation(weights, "dB")
    x = sp.cancel(rho_b / complete_baseline(5, "Bd"))
    y = sp.cancel(rho_d / complete_baseline(5, "dB"))
    score = sp.cancel((x + 2 * y) / 3)
    assert x > 1 > y
    assert score < 1
    print(f"Bd ratio ~ {sp.N(x, 16)}")
    print(f"dB ratio ~ {sp.N(y, 16)}")
    print(f"one-third score ~ {sp.N(score, 16)}")
    print("PASS exact rational solve refutes the conditioning artifact")


if __name__ == "__main__":
    main()

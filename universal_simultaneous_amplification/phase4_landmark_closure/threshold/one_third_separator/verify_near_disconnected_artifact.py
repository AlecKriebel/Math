#!/usr/bin/env python3
"""Exact refutation of two near-disconnected floating candidates."""

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


def five_vertex_artifact():
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
    print(f"n=5 Bd ratio ~ {sp.N(x, 16)}")
    print(f"n=5 dB ratio ~ {sp.N(y, 16)}")
    print(f"n=5 one-third score ~ {sp.N(score, 16)}")


def six_vertex_artifact():
    # Rational reconstruction of an adjoint-gradient endpoint candidate.
    # The double solve returned x~0.988016, y~1.104986 and score~1.065996.
    # Freezing all fifteen effective edge ratios and solving over QQ shows
    # that only the Bd number was reliable; the dB solve was ill-conditioned.
    weights = graph(
        6,
        [
            (0, 1, 29),
            (0, 2, 990131),
            (0, 3, 990580),
            (0, 4, 990737),
            (0, 5, 20141055117907212632064),
            (1, 2, 17091939448407612981248),
            (1, 3, 1014696),
            (1, 4, 1014696),
            (1, 5, 990294),
            (2, 3, 423423162887509508096),
            (2, 4, 1014696),
            (2, 5, 990131),
            (3, 4, 15053663072322829942784),
            (3, 5, 990580),
            (4, 5, 29),
        ],
    )
    rho_b = exact_fixation(weights, "Bd")
    rho_d = exact_fixation(weights, "dB")
    x = sp.cancel(rho_b / complete_baseline(6, "Bd"))
    y = sp.cancel(rho_d / complete_baseline(6, "dB"))
    score = sp.cancel((x + 2 * y) / 3)
    assert x < 1 and y < 1 and score < 1
    print(f"n=6 Bd ratio ~ {sp.N(x, 20)}")
    print(f"n=6 dB ratio ~ {sp.N(y, 20)}")
    print(f"n=6 one-third score ~ {sp.N(score, 20)}")


def main():
    five_vertex_artifact()
    six_vertex_artifact()
    print("PASS two exact rational solves refute conditioning artifacts")


if __name__ == "__main__":
    main()

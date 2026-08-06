#!/usr/bin/env python3
"""Independent deterministic checks for Phase-II finite certificates."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PHASE2 = HERE.parent
PHASE1_SRC = PHASE2.parent / "src"
sys.path.insert(0, str(PHASE1_SRC.parent))

from src.class_analyzer import is_weakly_reversible, safe_supports  # type: ignore  # noqa:E402
from src.generator import Reaction  # type: ignore  # noqa:E402


def stress_network(alpha: Fraction, beta: Fraction, gamma: Fraction) -> list[Reaction]:
    return [
        Reaction((0, 0), (1, 1), alpha),
        Reaction((1, 1), (0, 1), beta),
        Reaction((0, 1), (0, 0), gamma),
    ]


def verify_safe_support_graph_lemma(reactions: list[Reaction]) -> None:
    """Finite check of the safe-support conclusion for a concrete network.

    If I is quadratically safe and a linkage class contains a binary complex
    supported in I, every complex reached from it must be binary and supported
    in I.  The universal proof is graph-theoretic; this routine independently
    checks each concrete instance by exhaustive reachability.
    """
    from src.class_analyzer import linkage_classes, support  # type: ignore

    for I in safe_supports(reactions):
        for linkage in linkage_classes(reactions):
            seeds = [y for y in linkage if sum(y) == 2 and support(y).issubset(I)]
            if not seeds:
                continue
            assert all(sum(y) == 2 and support(y).issubset(I) for y in linkage)


def self_test() -> None:
    rs = stress_network(Fraction(2), Fraction(3), Fraction(5))
    assert is_weakly_reversible(rs)
    verify_safe_support_graph_lemma(rs)

    # A purely binary linkage is allowed on a safe support.
    rs2 = [Reaction((2, 0), (1, 1)), Reaction((1, 1), (2, 0))]
    assert is_weakly_reversible(rs2)
    verify_safe_support_graph_lemma(rs2)


if __name__ == "__main__":
    self_test()
    print("phase2_verifier.py self-test: OK")

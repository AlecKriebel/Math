#!/usr/bin/env python3
"""Exact finite lexicographic reward and Bellman certificates.

This module implements the finite algebra used in the tier-induction proof.
It deliberately does not infer asymptotic tiers from floating point data: a
caller supplies an integer reward vector ordered lexicographically.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Iterable, Sequence

try:
    from .reward_cycle import RewardEdge, classify_reward_cycles, CoboundaryCertificate
    from .bellman_certificate import solve_nonpositive_cycle_bellman, BellmanCertificate
except ImportError:
    from reward_cycle import RewardEdge, classify_reward_cycles, CoboundaryCertificate
    from bellman_certificate import solve_nonpositive_cycle_bellman, BellmanCertificate

Vertex = Hashable
Lex = tuple[int, ...]


def lex_sign(v: Sequence[int]) -> int:
    for a in v:
        if a:
            return 1 if a > 0 else -1
    return 0


def lex_add(a: Sequence[int], b: Sequence[int]) -> Lex:
    if len(a) != len(b):
        raise ValueError("dimension mismatch")
    return tuple(x + y for x, y in zip(a, b))


@dataclass(frozen=True, slots=True)
class LexRewardEdge:
    source: Vertex
    target: Vertex
    reward: Lex
    label: str = ""


@dataclass(frozen=True, slots=True)
class Scalarization:
    base: int
    scalar_edges: tuple[RewardEdge, ...]


def safe_scalarization(vertices: Iterable[Vertex], edges: Sequence[LexRewardEdge]) -> Scalarization:
    """Encode finite lexicographic rewards by one exact integer.

    For every simple directed cycle, the sign of the scalarized cycle reward
    equals the lexicographic sign of its vector reward.  A simple cycle has at
    most |V| edges, so a base larger than twice the maximum possible tail is
    sufficient.
    """
    vertices = tuple(vertices)
    if not edges:
        return Scalarization(2, ())
    dim = len(edges[0].reward)
    if any(len(e.reward) != dim for e in edges):
        raise ValueError("inconsistent reward dimensions")
    m = max((abs(a) for e in edges for a in e.reward), default=0)
    base = max(2, 2 * len(vertices) * max(1, m) + 1)
    weights = [base ** (dim - 1 - j) for j in range(dim)]
    scalar = tuple(
        RewardEdge(e.source, e.target, sum(a * w for a, w in zip(e.reward, weights)), e.label)
        for e in edges
    )
    return Scalarization(base, scalar)


def classify_lex_cycles(vertices: Iterable[Vertex], edges: Sequence[LexRewardEdge]):
    sc = safe_scalarization(vertices, edges)
    return classify_reward_cycles(tuple(vertices), sc.scalar_edges)


def solve_lex_bellman(
    vertices: Iterable[Vertex],
    edges: Sequence[LexRewardEdge],
    strict_vertices: Iterable[Vertex] = (),
) -> tuple[Scalarization, BellmanCertificate]:
    sc = safe_scalarization(vertices, edges)
    cert = solve_nonpositive_cycle_bellman(tuple(vertices), sc.scalar_edges, strict_vertices)
    return sc, cert


def verify_lex_coboundary(vertices: Iterable[Vertex], edges: Sequence[LexRewardEdge]) -> bool:
    """Return True exactly when every coordinate reward is a coboundary."""
    vertices = tuple(vertices)
    if not edges:
        return True
    dim = len(edges[0].reward)
    for j in range(dim):
        scalar = tuple(RewardEdge(e.source, e.target, e.reward[j], e.label) for e in edges)
        if not isinstance(classify_reward_cycles(vertices, scalar), CoboundaryCertificate):
            return False
    return True


def self_test() -> None:
    vs = (0, 1, 2)
    # First coordinate dominates the second: (-1,100) is lexicographically negative.
    es = (
        LexRewardEdge(0, 1, (0, 1)),
        LexRewardEdge(1, 2, (-1, 100)),
        LexRewardEdge(2, 0, (0, 0)),
    )
    sc = safe_scalarization(vs, es)
    cyc = classify_reward_cycles(vs, sc.scalar_edges)
    assert not isinstance(cyc, CoboundaryCertificate)
    assert cyc.total_reward < 0

    cob = (
        LexRewardEdge(0, 1, (1, -2)),
        LexRewardEdge(1, 2, (-1, 1)),
        LexRewardEdge(2, 0, (0, 1)),
    )
    assert verify_lex_coboundary(vs, cob)


if __name__ == "__main__":
    self_test()
    print("tier_induction.py self-test: OK")

#!/usr/bin/env python3
"""Finite terminal-complex episode library and exact drift recursion."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from math import log
from pathlib import Path
import sys
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))

from src.generator import Complex, Reaction  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.target_source_residual import (  # type: ignore  # noqa:E402
    aggregate_source_rates,
    expected_increment,
    increment_ratio,
    nontrivial_reactions,
    source_probabilities,
)

State = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class DesignatedStep:
    source: Complex
    target: Complex
    reaction_index: int
    conditional_edge_probability: Fraction


@dataclass(frozen=True, slots=True)
class EpisodePath:
    start: Complex
    terminal: Complex
    steps: tuple[DesignatedStep, ...]

    @property
    def jump_bound(self) -> int:
        return len(self.steps) + 1


@dataclass(frozen=True, slots=True)
class DriftRecursionLine:
    phase: Complex
    one_jump_drift: float
    source_probability: Fraction
    continuation_probability: Fraction
    remaining_drift: float
    total_drift: float


def complexes(reactions: Iterable[Reaction]) -> tuple[Complex, ...]:
    rs = nontrivial_reactions(reactions)
    return tuple(sorted({r.source for r in rs} | {r.target for r in rs}))


def shortest_designated_path(
    reactions: Sequence[Reaction], start: Complex, terminal: Complex
) -> EpisodePath:
    """A deterministic simple directed path, with one exact edge per step."""
    rs = nontrivial_reactions(reactions)
    by_source: dict[Complex, list[tuple[int, Reaction]]] = defaultdict(list)
    for idx, reaction in enumerate(rs):
        by_source[reaction.source].append((idx, reaction))
    for source in by_source:
        by_source[source].sort(key=lambda item: (item[1].target, item[1].rate, item[0]))
    if start == terminal:
        return EpisodePath(start, terminal, ())
    queue = deque([start])
    parent: dict[Complex, tuple[Complex, int, Reaction] | None] = {start: None}
    while queue:
        y = queue.popleft()
        for idx, reaction in by_source.get(y, ()):
            u = reaction.target
            if u in parent:
                continue
            parent[u] = (y, idx, reaction)
            if u == terminal:
                queue.clear()
                break
            queue.append(u)
    if terminal not in parent:
        raise ValueError("terminal is not reachable from start")
    reversed_edges: list[tuple[int, Reaction]] = []
    node = terminal
    while node != start:
        item = parent[node]
        if item is None:
            raise AssertionError("broken path parent")
        prev, idx, reaction = item
        reversed_edges.append((idx, reaction))
        node = prev
    edges = list(reversed(reversed_edges))
    aggregate = aggregate_source_rates(rs)
    steps = tuple(
        DesignatedStep(
            reaction.source,
            reaction.target,
            idx,
            reaction.rate / aggregate[reaction.source],
        )
        for idx, reaction in edges
    )
    return EpisodePath(start, terminal, steps)


def lifted_path_states(residual: Sequence[int], path: EpisodePath) -> tuple[State, ...]:
    r = tuple(residual)
    states = [tuple(ri + yi for ri, yi in zip(r, path.start))]
    current = path.start
    for step in path.steps:
        if current != step.source:
            raise AssertionError("path is not composable")
        states.append(tuple(ri + yi for ri, yi in zip(r, step.target)))
        current = step.target
    if current != path.terminal:
        raise AssertionError("path terminal mismatch")
    return tuple(states)


def expected_template_drift(
    reactions: Sequence[Reaction],
    residual: Sequence[int],
    path: EpisodePath,
) -> tuple[float, tuple[DriftRecursionLine, ...]]:
    """Exact finite recursion, with logarithms evaluated in double precision.

    All probabilities are exact Fractions.  The returned floating drift is
    only a numerical rendering of a finite linear combination of logarithms
    of positive rational numbers.
    """
    rs = nontrivial_reactions(reactions)
    states = lifted_path_states(residual, path)
    phases = [path.start] + [step.target for step in path.steps]
    if len(states) != len(phases):
        raise AssertionError("phase/state mismatch")

    # Terminal phase takes one jump and stops.
    k = len(phases) - 1
    x = states[k]
    t = phases[k]
    probs = source_probabilities(x, rs)
    drift = expected_increment(x, t, rs)
    reverse_lines: list[DriftRecursionLine] = [
        DriftRecursionLine(t, drift, probs[t], Fraction(0), 0.0, drift)
    ]

    # At earlier phases, only the designated exact edge continues.
    for k in range(len(path.steps) - 1, -1, -1):
        x = states[k]
        t = phases[k]
        probs = source_probabilities(x, rs)
        p_source = probs[t]
        q = path.steps[k].conditional_edge_probability
        continuation = p_source * q
        one = expected_increment(x, t, rs)
        total = one + float(continuation) * drift
        reverse_lines.append(
            DriftRecursionLine(t, one, p_source, continuation, drift, total)
        )
        drift = total
    return drift, tuple(reversed(reverse_lines))


def enumerate_episode_outcomes(
    reactions: Sequence[Reaction], residual: Sequence[int], path: EpisodePath
) -> tuple[tuple[Fraction, float], ...]:
    """Independently enumerate all terminal branches of one template."""
    rs = nontrivial_reactions(reactions)
    phases = [path.start] + [step.target for step in path.steps]
    states = lifted_path_states(residual, path)
    branches: list[tuple[Fraction, float]] = []

    def visit(k: int, probability: Fraction, accumulated: float) -> None:
        x = states[k]
        t = phases[k]
        total_rate = sum((r.propensity(x) for r in rs), Fraction(0))
        if total_rate <= 0:
            raise AssertionError("episode phase has no jump")
        designated_idx = path.steps[k].reaction_index if k < len(path.steps) else None
        for idx, reaction in enumerate(rs):
            propensity = reaction.propensity(x)
            if not propensity:
                continue
            prob = propensity / total_rate
            reward = log(float(increment_ratio(x, t, reaction.source)))
            if designated_idx is not None and idx == designated_idx:
                if abs(reward) > 1e-15:
                    raise AssertionError("designated carried-target reward is not zero")
                visit(k + 1, probability * prob, accumulated + reward)
            else:
                branches.append((probability * prob, accumulated + reward))

    visit(0, Fraction(1), 0.0)
    if sum((p for p, _ in branches), Fraction(0)) != 1:
        raise AssertionError("episode branch probabilities do not sum to one")
    return tuple(branches)


def full_library(reactions: Sequence[Reaction]) -> dict[tuple[Complex, Complex], EpisodePath]:
    C = complexes(reactions)
    return {(t, c): shortest_designated_path(reactions, t, c) for t in C for c in C}


def self_test() -> None:
    reactions = (
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    )
    path = shortest_designated_path(reactions, (0, 0), (0, 1))
    assert path.jump_bound <= 3
    residual = (20, 0)
    drift, _ = expected_template_drift(reactions, residual, path)
    branches = enumerate_episode_outcomes(reactions, residual, path)
    independent = sum(float(p) * reward for p, reward in branches)
    assert abs(drift - independent) < 1e-12
    assert len(full_library(reactions)) == 9


if __name__ == "__main__":
    self_test()
    print("episode_library.py self-test: OK")

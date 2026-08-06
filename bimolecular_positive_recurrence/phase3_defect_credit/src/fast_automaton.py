#!/usr/bin/env python3
"""Finite bounded-defect automata for a safe dominant species set.

All dominant species in I are treated as available.  A vertex is the exact
J-coordinate inside a supplied finite box.  q_I=1 source reactions are fast;
q_I=0 source reactions are slow.  Transitions leaving the box go to an EXIT
sentinel and are not hidden inside the finite automaton.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import sys
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from src.generator import Reaction  # type: ignore  # noqa:E402

State = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class AutomatonEdge:
    source: State
    target: State | None  # None is EXIT
    reaction_index: int
    reward_M: int
    reward_N: int
    fast: bool


@dataclass(frozen=True, slots=True)
class FastAutomaton:
    I: tuple[int, ...]
    J: tuple[int, ...]
    bounds: tuple[int, ...]
    states: tuple[State, ...]
    edges: tuple[AutomatonEdge, ...]

    def outgoing(self, state: State, *, fast: bool | None = None) -> tuple[AutomatonEdge, ...]:
        return tuple(
            e for e in self.edges
            if e.source == state and (fast is None or e.fast == fast)
        )


def q_count(y: Sequence[int], I: Sequence[int]) -> int:
    return sum(y[i] for i in I)


def build_fast_automaton(
    reactions: Sequence[Reaction], I: Iterable[int], bounds: Sequence[int]
) -> FastAutomaton:
    if not reactions:
        raise ValueError("empty reaction list")
    d = reactions[0].dimension
    I = tuple(sorted(set(I)))
    J = tuple(i for i in range(d) if i not in I)
    bounds = tuple(int(b) for b in bounds)
    if len(bounds) != len(J) or any(b < 0 for b in bounds):
        raise ValueError("one nonnegative bound is required for each defect coordinate")
    for r in reactions:
        if q_count(r.source, I) not in (0, 1) or q_count(r.target, I) not in (0, 1):
            raise ValueError("automaton requires the safe q_I in {0,1} reduction")
    states = tuple(product(*(range(b + 1) for b in bounds))) if J else ((),)
    edges: list[AutomatonEdge] = []
    for z in states:
        for idx, r in enumerate(reactions):
            source_J = tuple(r.source[j] for j in J)
            if any(z[a] < source_J[a] for a in range(len(J))):
                continue
            z2 = tuple(z[a] + r.vector[J[a]] for a in range(len(J)))
            target = z2 if all(0 <= z2[a] <= bounds[a] for a in range(len(J))) else None
            dm = q_count(r.target, I) - q_count(r.source, I)
            edges.append(
                AutomatonEdge(
                    source=z,
                    target=target,
                    reaction_index=idx,
                    reward_M=dm,
                    reward_N=r.delta_molecularity,
                    fast=q_count(r.source, I) == 1,
                )
            )
    return FastAutomaton(I, J, bounds, states, tuple(edges))


def self_test() -> None:
    rs = [
        Reaction((0, 0), (1, 1)),
        Reaction((1, 1), (0, 1)),
        Reaction((0, 1), (0, 0)),
    ]
    a = build_fast_automaton(rs, {0}, (3,))
    assert any(not e.fast and e.reward_M == 1 for e in a.edges)
    assert any(e.fast and e.reward_M == -1 for e in a.edges)


if __name__ == "__main__":
    self_test()
    print("fast_automaton.py self-test: OK")

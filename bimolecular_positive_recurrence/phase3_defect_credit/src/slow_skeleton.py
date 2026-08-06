#!/usr/bin/env python3
"""Exact graph-level trigger checks for bounded safe-support automata."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from .fast_automaton import AutomatonEdge, FastAutomaton, State


@dataclass(frozen=True, slots=True)
class TriggerCheck:
    slow_edge: AutomatonEdge
    zero_death_quiescent_reachable: bool
    witness_path: tuple[int, ...]


def quiescent_states(a: FastAutomaton) -> frozenset[State]:
    return frozenset(s for s in a.states if not a.outgoing(s, fast=True))


def check_birth_triggers(a: FastAutomaton) -> tuple[TriggerCheck, ...]:
    """Check that an R_01 birth cannot fast-relax to quiescence without death.

    The search uses only zero-M-reward fast edges.  A found path would yield a
    positive (+1) collapsed reward and is therefore an exact finite witness
    against the trigger lemma in the supplied box.
    """
    quiet = quiescent_states(a)
    out=[]
    for slow in a.edges:
        if slow.fast or slow.reward_M != 1 or slow.target is None:
            continue
        start=slow.target
        q=deque([start])
        parent: dict[State, tuple[State,int] | None]={start:None}
        found=None
        while q:
            s=q.popleft()
            if s in quiet:
                found=s;break
            for e in a.outgoing(s,fast=True):
                if e.target is None or e.reward_M<0: continue
                if e.target not in parent:
                    parent[e.target]=(s,e.reaction_index);q.append(e.target)
        path=[]
        if found is not None:
            s=found
            while parent[s] is not None:
                p,idx=parent[s]  # type: ignore[misc]
                path.append(idx);s=p
            path.reverse()
        out.append(TriggerCheck(slow,found is not None,tuple(path)))
    return tuple(out)


def verify_no_positive_birth_relaxation(a: FastAutomaton) -> None:
    bad=[c for c in check_birth_triggers(a) if c.zero_death_quiescent_reachable]
    if bad:
        raise AssertionError(f"positive collapsed birth reward witness: {bad[0]}")


def self_test() -> None:
    from src.generator import Reaction
    from .fast_automaton import build_fast_automaton
    rs=[Reaction((0,0),(1,1)),Reaction((1,1),(0,1)),Reaction((0,1),(0,0))]
    a=build_fast_automaton(rs,{0},(3,))
    verify_no_positive_birth_relaxation(a)


if __name__=="__main__":
    self_test();print("slow_skeleton.py self-test: OK")

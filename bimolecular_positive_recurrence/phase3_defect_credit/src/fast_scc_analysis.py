#!/usr/bin/env python3
"""Exact SCC reward classification and finite death-credit potentials."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Sequence

from .fast_automaton import AutomatonEdge, FastAutomaton, State


@dataclass(frozen=True, slots=True)
class FastSCCCertificate:
    components: tuple[tuple[State, ...], ...]
    component_of: tuple[tuple[State, int], ...]
    catalytic_components: tuple[int, ...]
    credit: tuple[tuple[State, int], ...]


def _tarjan(states: Sequence[State], edges: Sequence[AutomatonEdge]) -> list[list[State]]:
    adj: dict[State, list[State]] = defaultdict(list)
    for e in edges:
        if e.target is not None:
            adj[e.source].append(e.target)
    for s in states:
        adj.setdefault(s, [])
    index = 0
    stack: list[State] = []
    on: set[State] = set()
    ind: dict[State, int] = {}
    low: dict[State, int] = {}
    out: list[list[State]] = []

    def visit(v: State) -> None:
        nonlocal index
        ind[v] = low[v] = index
        index += 1
        stack.append(v); on.add(v)
        for w in sorted(set(adj[v])):
            if w not in ind:
                visit(w); low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], ind[w])
        if low[v] == ind[v]:
            comp: list[State] = []
            while True:
                w = stack.pop(); on.remove(w); comp.append(w)
                if w == v: break
            out.append(sorted(comp))
    for s in sorted(states):
        if s not in ind: visit(s)
    return out


def analyze_fast_sccs(automaton: FastAutomaton) -> FastSCCCertificate:
    fast = [e for e in automaton.edges if e.fast]
    comps = _tarjan(automaton.states, fast)
    cid = {s: i for i, comp in enumerate(comps) for s in comp}
    catalytic: set[int] = set()
    for e in fast:
        if e.target is not None and cid[e.source] == cid[e.target] and e.reward_M < 0:
            catalytic.add(cid[e.source])

    # If there is no catalytic SCC on a path, negative fast reward can occur
    # only while traversing the acyclic condensation graph.  The maximal
    # number of such deaths is a finite integer credit.  Catalytic states get
    # no finite credit and are marked -1.
    dag: dict[int, list[tuple[int, int]]] = defaultdict(list)
    indeg = [0] * len(comps)
    for e in fast:
        if e.target is None: continue
        a, b = cid[e.source], cid[e.target]
        if a != b:
            dag[a].append((b, -e.reward_M))
    # Collapse duplicate edges by retaining maximal death cost.
    dag2: dict[int, dict[int, int]] = defaultdict(dict)
    for a, arr in dag.items():
        for b, w in arr: dag2[a][b] = max(dag2[a].get(b, 0), w)
    for a in range(len(comps)):
        for b in dag2[a]: indeg[b] += 1
    q = deque(i for i,v in enumerate(indeg) if v == 0)
    topo=[]
    while q:
        a=q.popleft(); topo.append(a)
        for b in dag2[a]:
            indeg[b]-=1
            if indeg[b]==0:q.append(b)
    if len(topo)!=len(comps): raise AssertionError("SCC condensation is cyclic")
    val=[0]*len(comps)
    for a in reversed(topo):
        if a in catalytic:
            val[a]=-1
            continue
        best=0
        for b,w in dag2[a].items():
            if val[b] < 0:
                # Path reaches a catalytic component; finite credit is not the
                # correct classification there.
                best=-1; break
            best=max(best,w+val[b])
        val[a]=best
    credit=tuple((s,val[cid[s]]) for s in sorted(automaton.states))
    return FastSCCCertificate(
        tuple(tuple(c) for c in comps),
        tuple(sorted(cid.items())),
        tuple(sorted(catalytic)),
        credit,
    )


def verify_credit_inequality(automaton: FastAutomaton, cert: FastSCCCertificate) -> None:
    h=dict(cert.credit)
    cid=dict(cert.component_of)
    catalytic=set(cert.catalytic_components)
    for e in automaton.edges:
        if not e.fast or e.target is None: continue
        if cid[e.source] in catalytic or cid[e.target] in catalytic or h[e.source] < 0 or h[e.target] < 0:
            continue
        # h is remaining death credit: after a death edge, remaining credit can
        # fall by at most one.  Equivalently reward_M - (h'-h) <= 0.
        if e.reward_M - (h[e.target] - h[e.source]) > 0:
            raise AssertionError("fast credit inequality failed")


def self_test() -> None:
    from fractions import Fraction
    from src.generator import Reaction
    from .fast_automaton import build_fast_automaton
    rs=[
        Reaction((0,0),(1,1),Fraction(1)),
        Reaction((1,1),(0,1),Fraction(1)),
        Reaction((0,1),(0,0),Fraction(1)),
    ]
    a=build_fast_automaton(rs,{0},(3,))
    c=analyze_fast_sccs(a)
    verify_credit_inequality(a,c)
    # B>=1 is catalytic because A+B->B leaves B unchanged and can repeat.
    assert c.catalytic_components


if __name__=="__main__":
    self_test(); print("fast_scc_analysis.py self-test: OK")

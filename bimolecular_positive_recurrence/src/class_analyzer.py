#!/usr/bin/env python3
"""Exact graph, stoichiometric, and support-closure analysis."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Iterable, Sequence

import sympy as sp

from .generator import Complex, Reaction


def complexes(reactions: Iterable[Reaction]) -> tuple[Complex, ...]:
    return tuple(sorted({r.source for r in reactions} | {r.target for r in reactions}))


def reaction_adjacency(reactions: Iterable[Reaction]) -> dict[Complex, set[Complex]]:
    graph: dict[Complex, set[Complex]] = defaultdict(set)
    for r in reactions:
        graph[r.source].add(r.target)
        graph.setdefault(r.target, set())
    return dict(graph)


def strongly_connected_components(graph: dict[Complex, set[Complex]]) -> list[set[Complex]]:
    """Tarjan SCC, deterministic ordering."""
    index = 0
    stack: list[Complex] = []
    on_stack: set[Complex] = set()
    indices: dict[Complex, int] = {}
    low: dict[Complex, int] = {}
    out: list[set[Complex]] = []

    def visit(v: Complex) -> None:
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in sorted(graph.get(v, ())):
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            component: set[Complex] = set()
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.add(w)
                if w == v:
                    break
            out.append(component)

    for v in sorted(graph):
        if v not in indices:
            visit(v)
    return out


def is_weakly_reversible(reactions: Iterable[Reaction]) -> bool:
    rs = tuple(reactions)
    graph = reaction_adjacency(rs)
    membership: dict[Complex, int] = {}
    for idx, component in enumerate(strongly_connected_components(graph)):
        for y in component:
            membership[y] = idx
    return all(membership[r.source] == membership[r.target] for r in rs)


def linkage_classes(reactions: Iterable[Reaction]) -> list[set[Complex]]:
    """Connected components of the underlying undirected complex graph."""
    graph: dict[Complex, set[Complex]] = defaultdict(set)
    for r in reactions:
        graph[r.source].add(r.target)
        graph[r.target].add(r.source)
    seen: set[Complex] = set()
    answer: list[set[Complex]] = []
    for root in sorted(graph):
        if root in seen:
            continue
        comp: set[Complex] = set()
        queue = deque([root])
        seen.add(root)
        while queue:
            v = queue.popleft()
            comp.add(v)
            for w in sorted(graph[v]):
                if w not in seen:
                    seen.add(w)
                    queue.append(w)
        answer.append(comp)
    return answer


def molecularity_profile(linkage: Iterable[Complex]) -> frozenset[int]:
    return frozenset(sum(y) for y in linkage)


def stoichiometric_matrix(reactions: Sequence[Reaction]) -> sp.Matrix:
    if not reactions:
        return sp.zeros(0, 0)
    d = reactions[0].dimension
    return sp.Matrix(d, len(reactions), lambda i, j: reactions[j].vector[i])


def rational_conservation_basis(reactions: Sequence[Reaction]) -> list[tuple[Fraction, ...]]:
    """Basis of left-nullspace conservation vectors over Q."""
    if not reactions:
        return []
    basis = stoichiometric_matrix(reactions).T.nullspace()
    result: list[tuple[Fraction, ...]] = []
    for vector in basis:
        result.append(tuple(Fraction(v.p, v.q) for v in vector))
    return result


def positive_conservation_vector(reactions: Sequence[Reaction]) -> tuple[Fraction, ...] | None:
    """Find a strictly positive rational conservation vector, if one exists.

    Feasibility is reduced to linear programming over rational polyhedra via
    Fourier-Motzkin-compatible SymPy simplex.  Scaling permits w_i >= 1.
    """
    if not reactions:
        return None
    d = reactions[0].dimension
    variables = sp.symbols(f"w0:{d}")
    constraints = [v >= 1 for v in variables]
    constraints.extend(
        sum(sp.Integer(z) * variables[i] for i, z in enumerate(r.vector)) == 0
        for r in reactions
    )
    try:
        # lpmin returns an exact rational optimum or raises InfeasibleLPError.
        _, solution = sp.solvers.simplex.lpmin(sum(variables), constraints)
    except Exception:
        return None
    return tuple(Fraction(solution[v].p, solution[v].q) for v in variables)


def support(y: Sequence[int]) -> frozenset[int]:
    return frozenset(i for i, value in enumerate(y) if value)


@dataclass(frozen=True)
class QuadraticClosure:
    initial: frozenset[int]
    closure: frozenset[int]
    descent_sources: frozenset[Complex]
    witnessed_paths: tuple[tuple[Complex, ...], ...]

    @property
    def dissipative(self) -> bool:
        return bool(self.descent_sources)


def quadratic_support_closure(
    reactions: Sequence[Reaction], initial: Iterable[int]
) -> QuadraticClosure:
    """Close a species set under degree-two reactions.

    Starting with I, whenever a degree-two source is supported in the current
    set, add every species in its target.  Record every enabled degree-two
    source whose target has molecularity <2.  This is the exact face closure
    of the homogeneous quadratic ODE, including boundary production.
    """
    current = set(initial)
    changed = True
    descents: set[Complex] = set()
    while changed:
        changed = False
        for r in reactions:
            if sum(r.source) != 2 or not support(r.source).issubset(current):
                continue
            if sum(r.target) < 2:
                descents.add(r.source)
            for i in support(r.target):
                if i not in current:
                    current.add(i)
                    changed = True
    return QuadraticClosure(
        initial=frozenset(initial),
        closure=frozenset(current),
        descent_sources=frozenset(descents),
        witnessed_paths=(),
    )


def safe_supports(reactions: Sequence[Reaction]) -> list[frozenset[int]]:
    """Species sets closed under quadratic products and with no quadratic descent."""
    if not reactions:
        return []
    d = reactions[0].dimension
    result: list[frozenset[int]] = []
    for mask in range(1, 1 << d):
        initial = frozenset(i for i in range(d) if mask & (1 << i))
        closure = quadratic_support_closure(reactions, initial)
        if closure.closure == initial and not closure.dissipative:
            result.append(initial)
    return result


def lifted_cycle(
    reaction: Reaction,
    reverse_path: Sequence[Reaction],
    residual: Sequence[int],
) -> list[tuple[int, ...]]:
    """Return states of the exact lifted complex cycle.

    `reverse_path` must start at reaction.target and end at reaction.source.
    The returned list begins and ends at residual+reaction.source.
    """
    if not reverse_path:
        raise ValueError("reverse path is empty")
    if reverse_path[0].source != reaction.target:
        raise ValueError("reverse path does not start at reaction target")
    if reverse_path[-1].target != reaction.source:
        raise ValueError("reverse path does not end at reaction source")
    for left, right in zip(reverse_path, reverse_path[1:]):
        if left.target != right.source:
            raise ValueError("reverse path is not composable")
    states = [tuple(a + b for a, b in zip(residual, reaction.source))]
    state = reaction.fire(states[-1])
    states.append(state)
    for step in reverse_path:
        state = step.fire(state)
        states.append(state)
    if states[-1] != states[0]:
        raise AssertionError("lifted path did not close")
    return states


def self_test() -> None:
    rs = [
        Reaction((0, 0), (1, 1)),
        Reaction((1, 1), (0, 1)),
        Reaction((0, 1), (0, 0)),
    ]
    assert is_weakly_reversible(rs)
    assert [molecularity_profile(c) for c in linkage_classes(rs)] == [frozenset({0, 1, 2})]
    assert safe_supports(rs) == [frozenset({0}), frozenset({1})]
    path = [rs[1], rs[2]]
    states = lifted_cycle(rs[0], path, (5, 0))
    assert states[0] == states[-1] == (5, 0)
    assert states == [(5, 0), (6, 1), (5, 1), (5, 0)]


if __name__ == "__main__":
    self_test()
    print("class_analyzer.py self-test: OK")

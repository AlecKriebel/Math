#!/usr/bin/env python3
"""Exact finite graph certificates for actual-target priority service.

The module checks the combinatorial theorem used by the unconditioned
source-layer proof.  Priorities are exact integers obtained from a rational
scalarization of a complete source-rate flag.  A larger value means a faster
source layer.
"""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from typing import Hashable, Iterable, Sequence

Node = Hashable

@dataclass(frozen=True, slots=True)
class Edge:
    source: Node
    target: Node
    source_priority: int
    target_priority: int
    label: str = ""

    @property
    def reward(self) -> int:
        return self.target_priority - self.source_priority


def adjacency(edges: Sequence[Edge]) -> dict[Node, list[tuple[int, Node]]]:
    out: dict[Node, list[tuple[int, Node]]] = defaultdict(list)
    for i, edge in enumerate(edges):
        out[edge.source].append((i, edge.target))
    return out


def strongly_connected(nodes: Iterable[Node], edges: Sequence[Edge]) -> bool:
    nodes = tuple(nodes)
    if not nodes:
        return False
    adj = adjacency(edges)
    rev = defaultdict(list)
    for i, edge in enumerate(edges):
        rev[edge.target].append((i, edge.source))
    def reach(graph, root):
        seen = {root}; stack = [root]
        while stack:
            v = stack.pop()
            for _, w in graph.get(v, ()): 
                if w not in seen:
                    seen.add(w); stack.append(w)
        return seen
    return len(reach(adj, nodes[0])) == len(nodes) and len(reach(rev, nodes[0])) == len(nodes)


def first_drop_path(nodes: Iterable[Node], edges: Sequence[Edge], start: Node) -> tuple[int, ...] | None:
    """Path whose first nonneutral edge is a priority drop.

    If the linkage is not flat at the priority of ``start``, strong
    connectivity gives a path from ``start`` to a lower-priority node.  The
    returned prefix has neutral edges until its final negative edge.
    """
    nodes = tuple(nodes); priorities = {v: None for v in nodes}
    for edge in edges:
        if edge.source in priorities:
            if priorities[edge.source] is None:
                priorities[edge.source] = edge.source_priority
            elif priorities[edge.source] != edge.source_priority:
                raise ValueError("priority is not node-defined")
    if priorities[start] is None:
        raise ValueError("start has no outgoing edge")
    alpha = priorities[start]
    lower = {v for v, p in priorities.items() if p is not None and p < alpha}
    if not lower:
        return None
    adj = adjacency(edges)
    queue = deque([start]); parent: dict[Node, tuple[Node, int] | None] = {start: None}
    endpoint = None
    while queue:
        v = queue.popleft()
        if v in lower:
            endpoint = v; break
        for index, w in adj.get(v, ()):
            edge = edges[index]
            # Before the first drop we retain only neutral transitions at the
            # starting priority.  A positive transition raises the target
            # priority and is handled by the outer monotone-priority routine.
            if edge.reward == 0 and edge.source_priority == alpha and w not in parent:
                parent[w] = (v, index); queue.append(w)
            elif edge.reward < 0 and edge.source_priority == alpha:
                parent[w] = (v, index); endpoint = w; queue.clear(); break
    if endpoint is None:
        return None
    reverse = [];
    v = endpoint
    while parent[v] is not None:
        u, index = parent[v]; reverse.append(index); v = u
    path = tuple(reversed(reverse))
    if not path or edges[path[-1]].reward >= 0:
        raise AssertionError((start, path))
    if any(edges[i].reward != 0 for i in path[:-1]):
        raise AssertionError(path)
    return path


def top_flat_or_service(nodes: Iterable[Node], edges: Sequence[Edge], top_priority: int) -> tuple[str, tuple[int, ...] | None]:
    """Classify a strongly connected linkage at its top priority.

    Returns ``("flat", None)`` when every complex has the top priority.
    Otherwise it returns a neutral-prefix/negative-edge path from a top
    complex.  This is the exact graph part of the actual-target clock lemma.
    """
    nodes = tuple(nodes)
    top = [v for v in nodes if any(e.source == v and e.source_priority == top_priority for e in edges)]
    if not top:
        raise ValueError("no top node")
    priorities = {v: next(e.source_priority for e in edges if e.source == v) for v in nodes}
    if all(priorities[v] == top_priority for v in nodes):
        return ("flat", None)
    for start in top:
        path = first_drop_path(nodes, edges, start)
        if path is not None:
            return ("service", path)
    raise AssertionError("nonflat strongly connected linkage has no top drop")


@dataclass(frozen=True, slots=True)
class PriorityRaceBound:
    block_success: Fraction
    mean_top_events: Fraction
    lower_interruption_bound: Fraction


def priority_race_bound(path_length: int, tied_channel_lower_bound: Fraction, lower_source_ratio: Fraction) -> PriorityRaceBound:
    """Exact geometric block and lower-layer interruption bound.

    A block follows a fixed neutral-prefix/negative path.  At each path stage
    the designated target-source channel has conditional probability at least
    ``tied_channel_lower_bound`` among current-or-faster events.  A lower
    source event has hazard at most ``lower_source_ratio`` times the enabled
    current-target source.  The returned interruption bound is a union/
    compensator bound and is intentionally conservative.
    """
    if path_length <= 0:
        raise ValueError("path must be nonempty")
    if not (0 < tied_channel_lower_bound <= 1):
        raise ValueError("invalid tied probability")
    if lower_source_ratio < 0:
        raise ValueError("invalid ratio")
    success = tied_channel_lower_bound ** path_length
    mean = Fraction(path_length, 1) / success
    interruption = min(Fraction(1), mean * lower_source_ratio)
    return PriorityRaceBound(success, mean, interruption)


def credit_trial_drift(service: Fraction, maximum_arrival: Fraction, interruption_probability: Fraction) -> Fraction:
    if service <= 0 or maximum_arrival < 0 or not (0 <= interruption_probability <= 1):
        raise ValueError
    return -(1 - interruption_probability) * service + interruption_probability * maximum_arrival


def exhaustive_small_graph_audit() -> int:
    """Exhaust all strongly connected directed graphs through four nodes.

    Node priorities range over 0,1,2.  The check verifies that every nonflat
    top layer has a neutral-prefix strict drop.  It is calibration of a graph
    theorem, not a substitute for its proof.
    """
    total = 0
    for n in (2, 3, 4):
        nodes = tuple(range(n)); possible = tuple(permutations(nodes, 2))
        # Full n=4 universe has 2^12=4096 supports and is modest.
        for mask in range(1 << len(possible)):
            pairs = [possible[i] for i in range(len(possible)) if mask >> i & 1]
            for levels in product(range(3), repeat=n):
                edges = tuple(Edge(a, b, levels[a], levels[b], f"{a}->{b}") for a, b in pairs)
                if not strongly_connected(nodes, edges):
                    continue
                top = max(levels)
                kind, path = top_flat_or_service(nodes, edges, top)
                if len(set(levels)) == 1:
                    assert kind == "flat"
                else:
                    assert kind == "service" and path
                total += 1
    return total


def self_test() -> None:
    edges = (
        Edge("u", "v", 2, 2, "neutral"),
        Edge("v", "s", 2, 0, "drop"),
        Edge("s", "u", 0, 2, "activation"),
    )
    assert strongly_connected(("s", "u", "v"), edges)
    kind, path = top_flat_or_service(("s", "u", "v"), edges, 2)
    assert kind == "service" and path == (0, 1)
    bound = priority_race_bound(2, Fraction(1, 3), Fraction(1, 1000))
    assert bound.block_success == Fraction(1, 9)
    assert bound.mean_top_events == 18
    assert bound.lower_interruption_bound == Fraction(9, 500)
    assert credit_trial_drift(Fraction(1), Fraction(2), bound.lower_interruption_bound) < 0


if __name__ == "__main__":
    self_test()
    print("actual_target_priority.py self-test: OK")

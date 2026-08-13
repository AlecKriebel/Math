#!/usr/bin/env python3
"""Tiny independent check of the four minimal strong repairs of weak Theta.

This file intentionally uses only the Python standard library.  It does not
import any project graph, Fourier, or atlas code.  Its scope is the 2 x 2
comparison requested in PROOF_ATTEMPT.md: source/target weak-Theta placement
versus repair on the root-created A-C side or on the A-F side.

The certificate is combinatorial.  It enumerates the four displayed trees,
then records every displayed quartet split on each four-subset of the five
labels.  A difference invokes Englander et al., Theorem 2.11; equality is not
treated as evidence of stochastic overlap.
"""

from __future__ import annotations

from itertools import combinations, product


VERTICES = {"rho", "A", "B", "C", "D", "E", "F", "R"}
LEAVES = {str(i) for i in range(5)}


def network(placement: str, repair: str) -> tuple[set[str], set[tuple[str, str]]]:
    if placement not in {"source", "target"}:
        raise ValueError(placement)
    if repair not in {"AC", "AF"}:
        raise ValueError(repair)

    arcs = {
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "E"),
        ("E", "F"),
    }
    if repair == "AF":
        arcs |= {
            ("rho", "A"), ("rho", "C"),
            ("A", "R"), ("R", "F"), ("R", "0"),
        }
    else:
        # The root lies on the undirected A-R edge.  Suppressing it gives
        # A--R->C, the strong subdivision of the root-created A->C side.
        arcs |= {
            ("rho", "A"), ("rho", "R"),
            ("R", "C"), ("R", "0"), ("A", "F"),
        }

    attach = (
        {"B": "1", "D": "2", "F": "3", "E": "4"}
        if placement == "source"
        else {"E": "1", "D": "2", "F": "3", "B": "4"}
    )
    arcs |= {(parent, leaf) for parent, leaf in attach.items()}
    nodes = VERTICES | LEAVES
    validate(nodes, arcs)
    return nodes, arcs


def validate(nodes: set[str], arcs: set[tuple[str, str]]) -> None:
    indeg = {v: 0 for v in nodes}
    outdeg = {v: 0 for v in nodes}
    for u, v in arcs:
        assert u in nodes and v in nodes and u != v
        indeg[v] += 1
        outdeg[u] += 1
    assert (indeg["rho"], outdeg["rho"]) == (0, 2)
    for leaf in LEAVES:
        assert (indeg[leaf], outdeg[leaf]) == (1, 0)
    assert {v for v in nodes if (indeg[v], outdeg[v]) == (2, 1)} == {"C", "F"}
    for v in nodes - LEAVES - {"rho", "C", "F"}:
        assert (indeg[v], outdeg[v]) == (1, 2), (v, indeg[v], outdeg[v])

    # Acyclicity and reachability, independently by Kahn's algorithm.
    remaining = dict(indeg)
    queue = [v for v in nodes if remaining[v] == 0]
    seen = []
    while queue:
        u = queue.pop()
        seen.append(u)
        for a, b in arcs:
            if a == u:
                remaining[b] -= 1
                if remaining[b] == 0:
                    queue.append(b)
    assert set(seen) == nodes

    # Lowest-stable-ancestor condition: no proper descendant of the root lies
    # on every root-to-leaf path.  For each candidate, at least one leaf must
    # remain reachable when that candidate is deleted.
    for forbidden in nodes - LEAVES - {"rho"}:
        reachable = {"rho"}
        stack = ["rho"]
        while stack:
            u = stack.pop()
            for a, b in arcs:
                if a == u and b != forbidden and b not in reachable:
                    reachable.add(b)
                    stack.append(b)
        assert reachable & LEAVES, forbidden

    # Rooted tree-child check.
    children = {u: {v for a, v in arcs if a == u} for u in nodes}
    for u in nodes - LEAVES:
        assert any(v in LEAVES or indeg[v] == 1 for v in children[u]), u


def displayed_trees(nodes: set[str], arcs: set[tuple[str, str]]):
    parents = {r: sorted(u for u, v in arcs if v == r) for r in ("C", "F")}
    assert all(len(parents[r]) == 2 for r in parents)
    for choices in product((0, 1), repeat=2):
        keep = set(arcs)
        for r, choice in zip(("C", "F"), choices):
            keep.remove((parents[r][1 - choice], r))
        undirected = {tuple(sorted(edge)) for edge in keep}
        assert len(undirected) == len(nodes) - 1
        yield choices, undirected


def sd0_metadata(nodes: set[str], arcs: set[tuple[str, str]]) -> dict[str, object]:
    """Apply the locked one-step root suppression and audit the result."""
    retics = {"C", "F"}
    directed = {(u, v) for u, v in arcs if v in retics}
    undirected = {tuple(sorted((u, v))) for u, v in arcs if v not in retics}
    root_children = sorted(v for u, v in arcs if u == "rho")
    assert len(root_children) == 2
    undirected = {e for e in undirected if "rho" not in e}
    directed = {e for e in directed if "rho" not in e}
    a, b = root_children
    replacement = (a, b) if b in retics else ((b, a) if a in retics else tuple(sorted((a, b))))
    if b in retics or a in retics:
        assert replacement not in directed
        directed.add(replacement)
    else:
        assert replacement not in undirected
        undirected.add(replacement)

    live = nodes - {"rho"}
    degree = {v: 0 for v in live}
    for u, v in undirected | {tuple(sorted(e)) for e in directed}:
        degree[u] += 1
        degree[v] += 1
    assert all(degree[v] == (1 if v in LEAVES else 3) for v in live)
    assert len(undirected) + len(directed) == len(set(undirected) | {tuple(sorted(e)) for e in directed})

    tails = {}
    for u, v in directed:
        tails.setdefault(u, 0)
        tails[u] += 1
    assert max(tails.values(), default=0) <= 1  # no omnian

    graph_edges = set(undirected) | {tuple(sorted(e)) for e in directed}
    internal = live - LEAVES
    internal_edges = {e for e in graph_edges if e[0] in internal and e[1] in internal}

    # The internal theta core is one blob: every internal edge lies on a
    # cycle, equivalently none is a bridge.  It contains exactly C and F as
    # reticulations, hence is level 2.
    for blocked in internal_edges:
        reached = component(blocked[0], blocked, internal_edges)
        assert blocked[1] in reached, blocked
    assert retics <= internal

    def cycles() -> set[tuple[str, ...]]:
        found = set()
        for start in sorted(internal):
            def walk(path: list[str]) -> None:
                u = path[-1]
                for edge in internal_edges:
                    if u not in edge:
                        continue
                    v = edge[0] if edge[1] == u else edge[1]
                    if v == start and len(path) >= 3:
                        cyc = path[:]
                        reps = []
                        for seq in (cyc, list(reversed(cyc))):
                            for i in range(len(seq)):
                                reps.append(tuple(seq[i:] + seq[:i]))
                        found.add(min(reps))
                    elif v not in path and v >= start:
                        walk(path + [v])
            walk([start])
        return found

    cycle_lengths = sorted(len(c) for c in cycles())
    assert sum(1 for n in cycle_lengths if n == 3) == (0 if ("R", "C") in directed else 1)
    return {
        "directed": sorted(directed),
        "undirected": sorted(undirected),
        "cycle_lengths": cycle_lengths,
        "no_omnian": True,
    }


def component(start: str, blocked: tuple[str, str], edges: set[tuple[str, str]]) -> set[str]:
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for edge in edges:
            if edge == blocked or u not in edge:
                continue
            v = edge[0] if edge[1] == u else edge[1]
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def quartet_split(
    subset: tuple[str, ...], edges: set[tuple[str, str]]
) -> tuple[tuple[str, str], tuple[str, str]]:
    candidates = set()
    labels = set(subset)
    for edge in edges:
        side = component(edge[0], edge, edges) & labels
        if len(side) == 2:
            other = labels - side
            pair = tuple(sorted((tuple(sorted(side)), tuple(sorted(other)))))
            candidates.add(pair)
    assert len(candidates) == 1, (subset, candidates)
    return next(iter(candidates))


def deck(placement: str, repair: str):
    nodes, arcs = network(placement, repair)
    result = {}
    for subset in combinations(sorted(LEAVES), 4):
        splits = {
            quartet_split(subset, edges)
            for _, edges in displayed_trees(nodes, arcs)
        }
        result[subset] = tuple(sorted(splits))
    return result


def main() -> None:
    decks = {
        (placement, repair): deck(placement, repair)
        for placement in ("source", "target")
        for repair in ("AC", "AF")
    }
    # Omitting the repair taxon recovers the same displayed-quartet deck of
    # the weak four-leaf pair.  Thus the fifth taxon is genuinely carrying
    # the separating information.
    original = ("1", "2", "3", "4")
    original_decks = {decks[key][original] for key in decks}
    assert len(original_decks) == 1
    assert next(iter(original_decks)) == (
        (("1", "2"), ("3", "4")),
        (("1", "3"), ("2", "4")),
    )
    print("minimal strong-repair displayed-quartet comparison")
    for placement in ("source", "target"):
        for repair in ("AC", "AF"):
            nodes, arcs = network(placement, repair)
            meta = sd0_metadata(nodes, arcs)
            print(
                f"{placement}-{repair}: sd0 simple binary, no omnian; "
                f"cycle lengths {meta['cycle_lengths']}"
            )
    for sr in ("AC", "AF"):
        for tr in ("AC", "AF"):
            left = decks[("source", sr)]
            right = decks[("target", tr)]
            witnesses = [s for s in left if left[s] != right[s]]
            print(f"source-{sr} versus target-{tr}: ", end="")
            if witnesses:
                s = witnesses[0]
                print(f"DIFFERENT; witness {s}: {left[s]} != {right[s]}")
            else:
                print("SAME displayed-quartet deck")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exhaustive bounded census of simple standard semi-directed topologies.

The generation starts from edge subsets of the complete graph on the
unlabelled internal vertices.  No rooted-network or historical generator list
is used.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Sequence, Set, Tuple

from clean_graph import (
    MixedGraph,
    canonical_mixed_code,
    class_membership,
    graph_to_record,
    level,
    triangle_counts_by_blob,
)


Edge = Tuple[int, int]


def _adjacency_code(m: int, edges: Set[Edge], order: Sequence[int]) -> Tuple[int, ...]:
    code = []
    for i in range(m):
        for j in range(i + 1, m):
            u, v = order[i], order[j]
            code.append(int((u, v) in edges or (v, u) in edges))
    return tuple(code)


def _connected(m: int, edges: Set[Edge]) -> bool:
    if m == 1:
        return True
    nbr = [set() for _ in range(m)]
    for u, v in edges:
        nbr[u].add(v)
        nbr[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in nbr[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == m


def _orders_grouped_by_degree(degrees: Sequence[int]) -> Iterator[Tuple[int, ...]]:
    groups = []
    for d in sorted(set(degrees)):
        groups.append(tuple(i for i, x in enumerate(degrees) if x == d))
    per_group = [tuple(itertools.permutations(group)) for group in groups]
    for pieces in itertools.product(*per_group):
        yield tuple(x for piece in pieces for x in piece)


def canonical_internal_core(m: int, edges: Set[Edge]) -> Tuple[Tuple[int, ...], Tuple[Edge, ...]]:
    degrees = [0] * m
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    best = None
    best_order = None
    degree_prefix = tuple(sorted(degrees))
    for order in _orders_grouped_by_degree(degrees):
        code = degree_prefix + _adjacency_code(m, edges, order)
        if best is None or code < best:
            best = code
            best_order = order
    assert best is not None and best_order is not None
    old_to_new = {old: new for new, old in enumerate(best_order)}
    canon_edges = tuple(sorted((min(old_to_new[u], old_to_new[v]), max(old_to_new[u], old_to_new[v])) for u, v in edges))
    return best, canon_edges


def core_automorphisms(m: int, edges: Sequence[Edge]) -> Tuple[Tuple[int, ...], ...]:
    eset = set(edges)
    degrees = [0] * m
    for u, v in eset:
        degrees[u] += 1
        degrees[v] += 1
    raw_code = _adjacency_code(m, eset, tuple(range(m)))
    out = []
    # ``order`` is new-position -> old-vertex.  Invert it to obtain the
    # old-vertex -> new-position automorphism used below.
    for order in _orders_grouped_by_degree(degrees):
        if _adjacency_code(m, eset, order) != raw_code:
            continue
        old_to_new = [0] * m
        for new, old in enumerate(order):
            old_to_new[old] = new
        out.append(tuple(old_to_new))
    return tuple(sorted(set(out)))


def internal_cores(n: int, r: int) -> Tuple[Tuple[Tuple[Edge, ...], Tuple[Tuple[int, ...], ...]], ...]:
    m = n + 2 * r - 2
    ecount = n + 3 * r - 3
    if m <= 0 or ecount < 0:
        return ()
    possible = tuple(itertools.combinations(range(m), 2))
    unique: Dict[Tuple[int, ...], Tuple[Edge, ...]] = {}
    for combo in itertools.combinations(possible, ecount):
        edges = set(combo)
        degrees = [0] * m
        for u, v in combo:
            degrees[u] += 1
            degrees[v] += 1
        if any(d > 3 for d in degrees):
            continue
        if sum(3 - d for d in degrees) != n:
            continue
        if not _connected(m, edges):
            continue
        code, canon = canonical_internal_core(m, edges)
        unique.setdefault(code, canon)
    return tuple((edges, core_automorphisms(m, edges)) for _, edges in sorted(unique.items()))


def leaf_allocations(n: int, m: int, edges: Sequence[Edge], auts: Sequence[Sequence[int]]) -> Iterator[Tuple[Tuple[int, ...], Tuple[Tuple[int, ...], ...]]]:
    degrees = [0] * m
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    capacities = [3 - d for d in degrees]
    if sum(capacities) != n:
        return

    attach = [-1] * n

    def recurse(v: int, remaining: Tuple[int, ...]) -> Iterator[Tuple[int, ...]]:
        if v == m:
            if not remaining:
                yield tuple(attach)
            return
        c = capacities[v]
        for chosen in itertools.combinations(remaining, c):
            chosen_set = set(chosen)
            for leaf in chosen:
                attach[leaf] = v
            yield from recurse(v + 1, tuple(x for x in remaining if x not in chosen_set))

    seen = set()
    for allocation in recurse(0, tuple(range(n))):
        orbit = [tuple(p[allocation[leaf]] for leaf in range(n)) for p in auts]
        canonical = min(orbit)
        if allocation != canonical or canonical in seen:
            continue
        seen.add(canonical)
        stabilizer = tuple(p for p in auts if tuple(p[allocation[leaf]] for leaf in range(n)) == allocation)
        yield allocation, stabilizer


def reticulation_sets(m: int, r: int, stabilizer: Sequence[Sequence[int]]) -> Iterator[Tuple[Tuple[int, ...], Tuple[Tuple[int, ...], ...]]]:
    seen = set()
    for retics in itertools.combinations(range(m), r):
        transformed = [tuple(sorted(p[v] for v in retics)) for p in stabilizer]
        canonical = min(transformed)
        if retics != canonical or canonical in seen:
            continue
        seen.add(canonical)
        rset = set(retics)
        rstabilizer = tuple(p for p in stabilizer if {p[v] for v in rset} == rset)
        yield retics, rstabilizer


def mixed_graphs(
    n: int,
    r: int,
    cores: Sequence[Tuple[Tuple[Edge, ...], Tuple[Tuple[int, ...], ...]]] | None = None,
) -> Tuple[MixedGraph, ...]:
    m = n + 2 * r - 2
    found: List[MixedGraph] = []
    if cores is None:
        cores = internal_cores(n, r)
    for core_edges, auts in cores:
        nbr_internal = [set() for _ in range(m)]
        for u, v in core_edges:
            nbr_internal[u].add(v)
            nbr_internal[v].add(u)
        for attach, stabilizer in leaf_allocations(n, m, core_edges, auts):
            internal_edges_global = [(n + u, n + v) for u, v in core_edges]
            leaf_edges = [(leaf, n + attach[leaf]) for leaf in range(n)]
            all_edges = tuple(internal_edges_global + leaf_edges)
            nbr = {v: set() for v in range(n + m)}
            for u, v in all_edges:
                nbr[u].add(v)
                nbr[v].add(u)
            for retics_local, rstabilizer in reticulation_sets(m, r, stabilizer):
                retics = tuple(n + v for v in retics_local)
                choices = [tuple(sorted(nbr[v])) for v in retics]
                sorted_edges = tuple(sorted(tuple(sorted(e)) for e in all_edges))
                orientation_seen = set()
                for outgoing_neighbors in itertools.product(*choices):
                    arrows = {tuple(sorted(e)): set() for e in all_edges}
                    for rv, outgoing in zip(retics, outgoing_neighbors):
                        for other in nbr[rv]:
                            if other != outgoing:
                                arrows[tuple(sorted((rv, other)))].add(rv)
                    def transformed_code(p: Sequence[int]) -> Tuple[int, ...]:
                        mapping = {leaf: leaf for leaf in range(n)}
                        mapping.update({n + old: n + p[old] for old in range(m)})
                        states = {}
                        for e in sorted_edges:
                            nu, nv = mapping[e[0]], mapping[e[1]]
                            ne = tuple(sorted((nu, nv)))
                            heads = {mapping[h] for h in arrows[e]}
                            state = 1
                            if ne[0] in heads:
                                state |= 2
                            if ne[1] in heads:
                                state |= 4
                            states[ne] = state
                        return tuple(states[e] for e in sorted_edges)

                    orbit_codes = [transformed_code(p) for p in rstabilizer]
                    canonical_orientation = min(orbit_codes)
                    identity_code = transformed_code(tuple(range(m)))
                    if identity_code != canonical_orientation or canonical_orientation in orientation_seen:
                        continue
                    orientation_seen.add(canonical_orientation)
                    found.append(MixedGraph.make(n, m, retics, all_edges, arrows))
    return tuple(found)


def census(max_n: int, output: Path) -> dict:
    summary = {
        "schema": 1,
        "scope": {"min_leaves": 3, "max_leaves": max_n, "reticulations": [0, 1, 2], "simple_sd0": True},
        "cells": [],
        "topologies": [],
        "automatic_triangle_falsifiers": [],
    }
    global_codes = set()
    for n in range(3, max_n + 1):
        for r in range(3):
            t0 = time.time()
            cores = internal_cores(n, r)
            candidates = mixed_graphs(n, r, cores)
            classes = Counter()
            rootings_total = 0
            tc_rootings = 0
            accepted = []
            for graph in candidates:
                assert graph.validate_binary()
                assert level(graph) <= 2
                membership, roots = class_membership(graph)
                classes[membership] += 1
                rootings_total += len(roots)
                tc_rootings += sum(x.tree_child for x in roots)
                if membership in {"S_TC", "W_TC_NOT_S_TC"}:
                    rec = graph_to_record(graph, roots)
                    rec["membership"] = membership
                    accepted.append(rec)
                    code_tuple = tuple(rec["canonical_code"])
                    assert code_tuple not in global_codes
                    global_codes.add(code_tuple)
                    if membership != "NOT_W_TC" and rec["triangle_counts_by_blob"] and rec["triangle_counts_by_blob"][0] > 1:
                        summary["automatic_triangle_falsifiers"].append(rec)
            cell = {
                "n": n,
                "reticulations": r,
                "internal_vertices": n + 2 * r - 2,
                "internal_edges": n + 3 * r - 3,
                "internal_core_count": len(cores),
                "mixed_candidate_count": len(candidates),
                "membership_counts": dict(sorted(classes.items())),
                "admissible_rooting_count": rootings_total,
                "tree_child_rooting_count": tc_rootings,
                "accepted_W_or_S_count": len(accepted),
            }
            summary["cells"].append(cell)
            summary["topologies"].extend(accepted)
            print(json.dumps({**cell, "elapsed_seconds": round(time.time() - t0, 6)}, sort_keys=True), flush=True)
    summary["topology_count"] = len(summary["topologies"])
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded)
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not (3 <= args.max_n <= 5):
        raise SystemExit("the audited implementation supports max_n in 3..5")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    census(args.max_n, args.output)


if __name__ == "__main__":
    main()

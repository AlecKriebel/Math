#!/usr/bin/env python3
"""Decode a CaDiCaL witness into graph and one-guard game data."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import sys


CAMPAIGN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
)


N = 13
S = (0, 1, 2)


def read_assignment(path: Path) -> frozenset[int]:
    positive: set[int] = set()
    seen: set[int] = set()
    status = None
    with path.open(encoding="ascii") as handle:
        for raw in handle:
            fields = raw.split()
            if not fields:
                continue
            if fields[0] == "s":
                status = " ".join(fields[1:])
            elif fields[0] == "v":
                for text in fields[1:]:
                    literal = int(text)
                    if literal == 0:
                        continue
                    variable = abs(literal)
                    if variable in seen:
                        raise ValueError(f"duplicate assignment for {variable}")
                    seen.add(variable)
                    if literal > 0:
                        positive.add(variable)
    if status != "SATISFIABLE":
        raise ValueError(f"not a SAT witness: {status}")
    return frozenset(positive)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    positive = read_assignment(args.model)

    pairs = tuple(itertools.combinations(range(N), 2))
    edge_var = {pair: index + 1 for index, pair in enumerate(pairs)}
    h_edges = {
        pair for pair, variable in edge_var.items() if variable in positive
    }
    g_edges = set(pairs) - h_edges
    graph = BitGraph.from_edges(N, g_edges)

    family_offset = 78 + 78 * 11
    triples = tuple(itertools.combinations(range(N), 3))
    family_var = {
        triple: family_offset + index + 1
        for index, triple in enumerate(triples)
    }
    selected = {
        triple
        for triple, variable in family_var.items()
        if variable in positive
    }

    def dominates(state: tuple[int, int, int]) -> bool:
        occupied = sum(1 << vertex for vertex in state)
        covered = occupied
        for vertex in state:
            covered |= graph.adj[vertex]
        return covered == graph.full

    failures: list[dict[str, object]] = []
    for state in sorted(selected):
        for attacked in range(N):
            if attacked in state:
                continue
            replies = []
            for guard in state:
                if graph.adj[guard] & (1 << attacked):
                    successor = tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    if successor in selected:
                        replies.append((guard, successor))
            if not replies:
                failures.append({"state": state, "attack": attacked})

    response_lists: dict[str, list[int]] = {}
    signatures: dict[str, list[int]] = {}
    for target in range(3, N):
        response_lists[str(target)] = [
            anchor
            for anchor in S
            if tuple(sorted((set(S) - {anchor}) | {target})) in selected
        ]
        signatures[str(target)] = [
            anchor for anchor in S if (min(anchor, target), max(anchor, target)) in h_edges
        ]

    fixed = eternal_fixed_point(graph, 3)
    payload = {
        "source_model": str(args.model),
        "positive_variables": len(positive),
        "graph6_G": graph.to_graph6(),
        "n": graph.n,
        "m_G": graph.size,
        "parameters": {
            "gamma": domination_number(graph),
            "i": independent_domination_number(graph),
            "alpha": alpha(graph),
            "gamma_infinity": eternal_domination_number(graph),
            "theta": theta(graph),
        },
        "selected_family": {
            "size": len(selected),
            "all_states_dominate": all(dominates(state) for state in selected),
            "closure_failure_count": len(failures),
            "first_closure_failures": failures[:10],
            "contains_anchor_state": S in selected,
        },
        "greatest_eternal_triple_family_size": len(fixed.family),
        "anchor_response_lists": response_lists,
        "anchor_H_signatures": signatures,
        "neutral_vertices": [
            int(vertex)
            for vertex, signature in signatures.items()
            if not signature
        ],
        "H_edges": sorted(h_edges),
        "G_edges": sorted(g_edges),
    }
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(raw, encoding="utf-8")
    print(raw, end="")


if __name__ == "__main__":
    main()

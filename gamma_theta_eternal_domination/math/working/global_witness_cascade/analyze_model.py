#!/usr/bin/env python3
"""Inspect a three-critical-witness boundary-cycle SAT model.

This is a discovery helper.  It rebuilds the variable order used by
``probe_boundary_cycle.py`` and independently recomputes elementary graph
parameters and the greatest eternal triple kernel.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
SOURCE = CAMPAIGN / "math" / "working" / "three_gate_odd_holonomy"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_model(path: Path) -> dict[int, bool]:
    literals = [
        int(piece)
        for line in path.read_text(encoding="ascii").splitlines()
        if line.startswith("v ")
        for piece in line.split()[1:]
        if piece != "0"
    ]
    return {abs(literal): literal > 0 for literal in literals}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--spares", type=int, default=3)
    parser.add_argument("--full-gates", action="store_true")
    args = parser.parse_args()

    probe = load_module("boundary_probe", SOURCE / "probe_boundary_cycle.py")
    utility = load_module("boundary_inspect", SOURCE / "inspect_model.py")
    cnf, metadata = probe.build(
        (0, 1, 2),
        (1, 1, 1),
        enforce_gamma=False,
        spare_vertices=args.spares,
        full_gates=args.full_gates,
        all_two_lists=True,
    )
    assignment = parse_model(args.model)
    if len(assignment) != len(cnf.names) - 1:
        raise RuntimeError(
            f"incomplete model: {len(assignment)} / {len(cnf.names) - 1}"
        )

    edge = metadata["edge"]
    family_variables = metadata["family"]
    assert isinstance(edge, dict)
    assert isinstance(family_variables, dict)
    order = int(metadata["order"])
    h_edges = {uv for uv, variable in edge.items() if assignment[variable]}
    all_edges = set(combinations(range(order), 2))
    g_edges = all_edges - h_edges
    selected = {
        state
        for state, variable in family_variables.items()
        if assignment[variable]
    }
    kernel3 = utility.greatest_family(order, 3, g_edges)
    gamma = min(
        size
        for size in range(1, 4)
        if any(
            utility.dominates(state, order, g_edges)
            for state in combinations(range(order), size)
        )
    )
    alpha = 3
    if any(
        utility.independent(state, g_edges)
        for state in combinations(range(order), 4)
    ):
        raise RuntimeError("model unexpectedly has an independent four-set")
    independent_domination = min(
        size
        for size in range(1, 4)
        if any(
            utility.independent(state, g_edges)
            and utility.dominates(state, order, g_edges)
            for state in combinations(range(order), size)
        )
    )
    theta, coloring = utility.chromatic_number(order, h_edges)

    direct_lists: dict[int, list[int]] = {}
    anchor = {0, 1, 2}
    for vertex in range(3, order):
        direct_lists[vertex] = [
            omitted
            for omitted in range(3)
            if tuple(sorted((anchor - {omitted}) | {vertex})) in selected
        ]

    dominating_pairs = [
        list(pair)
        for pair in combinations(range(order), 2)
        if utility.dominates(pair, order, g_edges)
    ]
    common_h = {
        f"{u},{v}": [
            w
            for w in range(order)
            if w not in (u, v)
            and tuple(sorted((u, w))) in h_edges
            and tuple(sorted((v, w))) in h_edges
        ]
        for u, v in combinations(range(order), 2)
    }
    first_spare = order - args.spares
    if args.spares < 3:
        raise RuntimeError("analysis requires at least three spare witnesses")
    critical = (
        (4, 6, first_spare),
        (5, 7, first_spare + 1),
        (3, 8, first_spare + 2),
    )
    result = {
        "schema": "global-witness-cascade-model-v1",
        "order": order,
        "graph6": utility.graph6(order, g_edges),
        "size": len(g_edges),
        "selected_family_size": len(selected),
        "greatest_triple_family_size": len(kernel3),
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": theta,
        },
        "h_coloring": coloring,
        "selected_family_sha256": sha256(
            "\n".join(
                ",".join(map(str, state)) for state in sorted(selected)
            ).encode("ascii")
        ).hexdigest(),
        "direct_lists": {str(k): v for k, v in direct_lists.items()},
        "critical_witnesses": [
            {
                "pair": [u, v],
                "witness": q,
                "common_h_neighbors": common_h[f"{u},{v}"],
                "witness_list": direct_lists[q],
                "anchor_h_incident": tuple(sorted((i, q))) in h_edges,
            }
            for i, (u, v, q) in enumerate(critical)
        ],
        "dynamic_anchor_pair_common_h": [
            {
                "pair": [i, q],
                "common_h_neighbors": common_h[
                    f"{min(i, q)},{max(i, q)}"
                ],
            }
            for i, q in enumerate(range(first_spare, first_spare + 3))
        ],
        "dominating_pair_count": len(dominating_pairs),
        "dominating_pairs": dominating_pairs,
        "h_edges": [list(edge_pair) for edge_pair in sorted(h_edges)],
        "selected_family": [list(state) for state in sorted(selected)],
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"graph6={result['graph6']} selected={len(selected)} "
        f"kernel3={len(kernel3)} dominating_pairs={len(dominating_pairs)}"
    )


if __name__ == "__main__":
    main()

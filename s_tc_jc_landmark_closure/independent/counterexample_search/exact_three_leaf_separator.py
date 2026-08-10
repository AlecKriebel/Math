#!/usr/bin/env python3
"""Graph-derived exact tree/3-sunlet JC separator under Theta_0."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

from audit_io import load_json
from clean_graph import class_membership
from fourier_engine import build_model, evaluate_fraction
from screen_models import graph_from_record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, default=Path("census_n5_deterministic.json.gz"))
    args = parser.parse_args()
    census = load_json(args.census)
    tree_record = next(
        t for t in census["topologies"]
        if t["n"] == 3 and t["membership"] == "S_TC" and len(t["reticulations"]) == 0
    )
    sunlet_record = next(
        t for t in census["topologies"]
        if t["n"] == 3 and t["membership"] == "S_TC" and len(t["reticulations"]) == 1
    )

    def symbolic_values(record):
        graph = graph_from_record(record)
        membership, roots = class_membership(graph)
        assert membership == "S_TC"
        model = build_model(graph, roots[0])
        params = sp.symbols(f"p0:{model.parameter_count}", positive=True)
        return graph, model, params, evaluate_fraction(model, params)

    _, tree_model, tree_params, tree = symbolic_values(tree_record)
    _, sun_model, sun_params, sun = symbolic_values(sunlet_record)
    assert tree_model.coordinates == sun_model.coordinates == (
        (0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 2, 3)
    )

    tree_pullback = sp.factor(tree[0] * tree[1] * tree[2] - tree[3] ** 2)
    sun_pullback = sp.factor(sun[0] * sun[1] * sun[2] - sun[3] ** 2)
    assert tree_pullback == 0

    # With the graph-generated parameter ordering, p7 is the inheritance
    # probability and p0 is an ordinary edge multiplier.  Normalize the
    # factor to an explicitly positive product on 0<p_i<1.
    expected = (
        sun_params[0] ** 2 * sun_params[1] * sun_params[2]
        * sun_params[3] ** 2 * sun_params[4] * sun_params[5] ** 2
        * sun_params[6] ** 2 * sun_params[7]
        * (1 - sun_params[2]) ** 2 * (1 - sun_params[7])
    )
    assert sp.expand(sun_pullback - expected) == 0

    payload = {
        "schema": 1,
        "status": "PROVED",
        "coordinate_order": [list(g) for g in sun_model.coordinates],
        "separator": "q011*q101*q110-q123^2",
        "tree_pullback": "0",
        "sunlet_pullback": str(sun_pullback),
        "positive_normal_form": str(sp.factor(expected)),
        "domain": "0 < every edge multiplier p0,...,p6 < 1 and 0 < inheritance p7 < 1",
        "conclusion": "The open three-leaf JC tree and 3-sunlet loci are strictly separated; neither is generically contained in the other. The three labelled sunlet orientations are ordinary-T-related.",
        "derivation": {
            "tree_arcs": [list(a) for a in tree_model.arcs],
            "sunlet_arcs": [list(a) for a in sun_model.arcs],
            "sunlet_incoming_arc_indices": [list(x) for x in sun_model.incoming_arcs],
        },
    }
    out = Path("three_leaf_separator_certificate.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()

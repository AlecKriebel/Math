#!/usr/bin/env python3
"""Extract the deterministic six-vertex gamma-two SAT control."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def load_search():
    path = Path(__file__).with_name("search_control.py")
    spec = importlib.util.spec_from_file_location("control_search", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load search encoder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    search = load_search()
    cnf, metadata = search.build(
        6,
        frozenset((0,)),
        "two",
    )
    literals = [
        int(piece)
        for line in args.model.read_text(encoding="ascii").splitlines()
        if line.startswith("v ")
        for piece in line.split()[1:]
        if piece != "0"
    ]
    assignment = {abs(literal): literal > 0 for literal in literals}
    if len(assignment) != len(cnf.names) - 1:
        raise RuntimeError("incomplete SAT model")

    edge_h = metadata["edge_h"]
    family_variables = metadata["family"]
    assert isinstance(edge_h, dict)
    assert isinstance(family_variables, dict)
    h_edges = sorted(
        uv for uv, variable in edge_h.items() if assignment[variable]
    )
    family = sorted(
        state
        for state, variable in family_variables.items()
        if assignment[variable]
    )
    payload = "\n".join(
        ",".join(map(str, state)) for state in family
    ).encode("ascii")
    result = {
        "schema": "dynamic-type-sparsity-gamma-two-control-v1",
        "classification": "sharp control; not a gamma-theta counterexample",
        "order": 6,
        "h_edges": [list(uv) for uv in h_edges],
        "selected_family": [list(state) for state in family],
        "selected_family_sha256": sha256(payload).hexdigest(),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"H-edges={len(h_edges)} family={len(family)} "
        f"hash={result['selected_family_sha256']}"
    )


if __name__ == "__main__":
    main()

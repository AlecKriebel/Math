#!/usr/bin/env python3
"""Materialize the empty free-boundary metadata for full Hamming balls.

The existing core-radius generator treats all edges outside a validated free
boundary as distance-counted core edges.  An empty incident-vertex boundary
therefore makes all 903 order-43 edges contribute to Hamming distance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from graph_io import encode_graph6, read_graph, validate_simple


GENERATOR_ID = "ramsey55_empty_boundary_for_full_hamming_v1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.base_graph.read_bytes()
    adjacency = read_graph(args.base_graph)
    validate_simple(adjacency)
    result = {
        "generator": GENERATOR_ID,
        "base_file_sha256": hashlib.sha256(raw).hexdigest(),
        "base_graph6": encode_graph6(adjacency),
        "order": len(adjacency),
        "forbidden_size": 5,
        "induced_free_vertices": [],
        "incident_free_vertices": [],
        "free_edges": [],
        "variable_count": 0,
        "scope": (
            "empty free boundary: every graph edge contributes to the "
            "full-graph Hamming distance"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

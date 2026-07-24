#!/usr/bin/env python3
"""Finite tight-graph audit for the rigidity-mode escape search."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "flex_topology_escape.json"
OUTPUT = HERE / "results" / "flex_topology.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


graph_tools = load_module(
    "flex_graph_tools", HERE / "block_topology.py"
)


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    artifact = json.loads(source_bytes)
    tolerance = float(artifact["parameters"]["tight_tolerance"])
    reports = []
    for analysis in artifact["analyses"]:
        cardinality = int(analysis["cardinality"])
        (
            source_maximum,
            source_clearance,
            source_adjacency,
            _source_edges,
        ) = graph_tools.tight_graph(
            analysis["source"]["coordinates_float64"], tolerance
        )
        source_invariants = graph_tools.graph_invariants(
            source_adjacency
        )
        source_array = np.asarray(
            analysis["source"]["coordinates_float64"], dtype=float
        )
        source_gram = source_array @ source_array.T
        for run in artifact["runs"]:
            if run["cardinality"] != cardinality:
                continue
            (
                retained_maximum,
                retained_clearance,
                retained_adjacency,
                _retained_edges,
            ) = graph_tools.tight_graph(
                run["retained"]["coordinates_float64"], tolerance
            )
            retained_invariants = graph_tools.graph_invariants(
                retained_adjacency
            )
            mapping, visited = graph_tools.isomorphism(
                source_adjacency, retained_adjacency
            )
            gram_difference = None
            if mapping is not None:
                retained_array = np.asarray(
                    run["retained"]["coordinates_float64"],
                    dtype=float,
                )
                retained_gram = retained_array @ retained_array.T
                gram_difference = float(
                    np.max(
                        np.abs(
                            source_gram
                            - retained_gram[np.ix_(mapping, mapping)]
                        )
                    )
                )
            reports.append(
                {
                    "cardinality": cardinality,
                    "restart": run["restart"],
                    "source_maximum": source_maximum,
                    "retained_maximum": retained_maximum,
                    "maximum_change": (
                        retained_maximum - source_maximum
                    ),
                    "source_cutoff_clearance": source_clearance,
                    "retained_cutoff_clearance": retained_clearance,
                    "source_graph": source_invariants,
                    "retained_graph": retained_invariants,
                    "isomorphic_to_source": mapping is not None,
                    "isomorphism_search_nodes": visited,
                    "source_to_retained_isomorphism": mapping,
                    "mapped_gram_maximum_difference": gram_difference,
                    "topology_changed_up_to_isomorphism": (
                        mapping is None
                    ),
                    "strictly_beats_source_at_1e-12": (
                        retained_maximum
                        < source_maximum - 1.0e-12
                    ),
                }
            )
    output = {
        "schema": "kissing5.flex_topology.v1",
        "evidence_status": (
            "FINITE GRAPH RESULTS EXACT FOR GRAPHS FORMED FROM "
            "BINARY64 COORDINATES; GEOMETRIC INTERPRETATION IS "
            "NUMERICAL EVIDENCE ONLY"
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "tight_tolerance": tolerance,
        "reports": reports,
        "summary": {
            "run_count": len(reports),
            "nonisomorphic_to_source_count": sum(
                report["topology_changed_up_to_isomorphism"]
                for report in reports
            ),
            "strict_improvement_count": sum(
                report["strictly_beats_source_at_1e-12"]
                for report in reports
            ),
        },
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output["summary"], sort_keys=True))


if __name__ == "__main__":
    main()

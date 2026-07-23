#!/usr/bin/env python3
"""Reconstruct Exoo's (5,5;42) graph from its published cyclic definition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from graph_io import encode_graph6, write_canonical_artifact


SOURCE = "https://arxiv.org/abs/2212.12630"
RED_LENGTHS = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}
RECOLORED_CONSECUTIVE_STARTS = {
    4,
    5,
    6,
    7,
    13,
    14,
    15,
    16,
    23,
    24,
    30,
    33,
    39,
    40,
    41,
}
RECOLORED_EDGES = {
    *(tuple(sorted((start, start + 1))) for start in RECOLORED_CONSECUTIVE_STARTS),
    (11, 32),
}


def construct() -> list[int]:
    """Use red edges as graph edges; original labels 1..42 become 0..41."""
    original_vertices = list(range(1, 43))
    adjacency = [0] * 42
    for new_left, old_left in enumerate(original_vertices):
        for new_right in range(new_left + 1, 42):
            old_right = original_vertices[new_right]
            difference = abs(old_left - old_right)
            distance = min(difference, 43 - difference)
            red = distance in RED_LENGTHS
            if tuple(sorted((old_left, old_right))) in RECOLORED_EDGES:
                if not red:
                    raise AssertionError("published recoloring must change red to blue")
                red = False
            if red:
                adjacency[new_left] |= 1 << new_right
                adjacency[new_right] |= 1 << new_left
    return adjacency


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph6", type=Path, default=Path("data/exoo42_constructed.g6")
    )
    parser.add_argument(
        "--artifact",
        type=Path,
        default=Path("data/exoo42_constructed.canonical.json"),
    )
    args = parser.parse_args()

    adjacency = construct()
    args.graph6.parent.mkdir(parents=True, exist_ok=True)
    args.graph6.write_text(encode_graph6(adjacency) + "\n", encoding="ascii")
    digest = write_canonical_artifact(
        adjacency,
        args.artifact,
        {
            "type": "reconstructed_from_published_definition",
            "source": SOURCE,
            "original_labels": "1..42, relabeled to 0..41",
            "edge_color_used": "red",
            "red_lengths_mod_43": sorted(RED_LENGTHS),
            "deleted_original_vertex": 0,
            "recolored_red_to_blue": [
                list(edge) for edge in sorted(RECOLORED_EDGES)
            ],
        },
    )
    print(
        json.dumps(
            {
                "graph6_path": str(args.graph6),
                "artifact_path": str(args.artifact),
                "artifact_sha256": digest,
                "edge_count": sum(row.bit_count() for row in adjacency) // 2,
                "degree_sequence": sorted(row.bit_count() for row in adjacency),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

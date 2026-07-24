#!/usr/bin/env python3
"""Audit forbidden-set color and overlap topology in the 44-graph pool."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import read_graph  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def topology(path: Path) -> dict[str, object]:
    adjacency = read_graph(path)
    conflicts: list[tuple[str, tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edges == 10:
            conflicts.append(("C5", vertices))
        elif edges == 0:
            conflicts.append(("I5", vertices))
    return {
        "E": len(conflicts),
        "colors": [color for color, _ in conflicts],
        "vertex_sets": [list(vertices) for _, vertices in conflicts],
        "mixed_colors": (
            conflicts[0][0] != conflicts[1][0]
            if len(conflicts) == 2
            else None
        ),
        "pair_overlap": (
            len(set(conflicts[0][1]).intersection(conflicts[1][1]))
            if len(conflicts) == 2
            else None
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary_path = (
        args.summary
        if args.summary.is_absolute()
        else ROOT / args.summary
    )
    output_path = (
        args.output if args.output.is_absolute() else ROOT / args.output
    )
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    records: list[dict[str, object]] = []
    for run in summary["runs"]:
        for kind, path_key, hash_key in (
            ("catalog_start", "start", "start_sha256"),
            ("conflict_block_final", "final_candidate", "final_candidate_sha256"),
        ):
            path = ROOT / run[path_key]
            if sha256(path) != run[hash_key]:
                raise SystemExit(f"pool graph hash mismatch: {path}")
            item = topology(path)
            records.append(
                {
                    "kind": kind,
                    "catalog_line": run["catalog_line"],
                    "path": run[path_key],
                    "sha256": run[hash_key],
                    **item,
                }
            )
    groups: dict[str, dict[str, object]] = {}
    for kind in ("catalog_start", "conflict_block_final"):
        selected = [item for item in records if item["kind"] == kind]
        color_patterns = Counter(
            "+".join(sorted(str(color) for color in item["colors"]))
            for item in selected
        )
        overlaps = Counter(str(item["pair_overlap"]) for item in selected)
        groups[kind] = {
            "count": len(selected),
            "color_pattern_counts": dict(sorted(color_patterns.items())),
            "pair_overlap_counts": dict(sorted(overlaps.items())),
            "all_E2": all(item["E"] == 2 for item in selected),
            "all_same_color": all(
                item["mixed_colors"] is False for item in selected
            ),
            "all_pair_overlap_4": all(
                item["pair_overlap"] == 4 for item in selected
            ),
        }
    result = {
        "schema": "ramsey55.path_relink_pool_conflict_topology.v1",
        "checker": "exhaustive_five_set_color_overlap_v1",
        "summary": str(summary_path.relative_to(ROOT)),
        "summary_sha256": sha256(summary_path),
        "graph_count": len(records),
        "groups": groups,
        "records": records,
        "status": "PASS",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

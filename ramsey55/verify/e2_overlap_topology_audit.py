#!/usr/bin/env python3
"""Audit the exact two-conflict topology of the 22+22 elite corpus."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import read_graph  # noqa: E402


CHECKER_ID = "ramsey55_e2_overlap_topology_audit_v1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def conflict_sets(path: Path) -> list[dict[str, object]]:
    adjacency = read_graph(path)
    if len(adjacency) != 43:
        raise ValueError(f"{path} is not order 43")
    result: list[dict[str, object]] = []
    for vertices in itertools.combinations(range(43), 5):
        count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if count in {0, 10}:
            result.append(
                {
                    "color": "I5" if count == 0 else "C5",
                    "vertices": list(vertices),
                }
            )
    return result


def checked_record(path: Path, expected_sha256: str) -> dict[str, object]:
    if digest(path) != expected_sha256:
        raise ValueError(f"hash mismatch for {path}")
    conflicts = conflict_sets(path)
    if len(conflicts) != 2:
        raise ValueError(f"{path} has {len(conflicts)} conflicts")
    first = set(conflicts[0]["vertices"])
    second = set(conflicts[1]["vertices"])
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": expected_sha256,
        "conflicts": conflicts,
        "same_color": conflicts[0]["color"] == conflicts[1]["color"],
        "intersection": sorted(first & second),
        "intersection_size": len(first & second),
        "union": sorted(first | second),
        "union_size": len(first | second),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    catalog_summary_path = (
        ROOT / "results/verification/catalog_seed_search_stratified_v1.summary.json"
    )
    followup_summary_path = (
        ROOT / "results/verification/conflict_block_catalog22_followup_summary.json"
    )
    catalog_summary = json.loads(catalog_summary_path.read_text())
    followup_summary = json.loads(followup_summary_path.read_text())

    catalog: list[dict[str, object]] = []
    for line in catalog_summary["searched_lines"]:
        record_path = (
            ROOT
            / "results/constructive/catalog_seed_search_stratified_v1"
            / f"line_{line:03d}.result.json"
        )
        record = json.loads(record_path.read_text())
        if record["catalog_line"] != line or record["E"] != 2:
            raise ValueError(f"bad catalog result {record_path}")
        catalog.append(
            checked_record(Path(record["graph_path"]), record["graph_sha256"])
        )

    followup: list[dict[str, object]] = []
    for run in followup_summary["runs"]:
        if run["E"] != 2 or run["verification"]["verified"] is not True:
            raise ValueError("bad conflict-block record")
        followup.append(
            checked_record(
                ROOT / run["final_candidate"], run["final_candidate_sha256"]
            )
        )
    if len(catalog) != 22 or len(followup) != 22:
        raise ValueError("expected 22 records in each corpus")

    def distribution(records: list[dict[str, object]]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for record in records:
            colors = "+".join(
                str(conflict["color"]) for conflict in record["conflicts"]
            )
            key = f"{colors}:intersection_{record['intersection_size']}"
            counts[key] = counts.get(key, 0) + 1
        return counts

    combined = [*catalog, *followup]
    result = {
        "checker": CHECKER_ID,
        "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "input_bindings": {
            "catalog_summary": str(catalog_summary_path.relative_to(ROOT)),
            "catalog_summary_sha256": digest(catalog_summary_path),
            "followup_summary": str(followup_summary_path.relative_to(ROOT)),
            "followup_summary_sha256": digest(followup_summary_path),
        },
        "corpora": {
            "catalog_seed_starts": catalog,
            "conflict_block_finals": followup,
        },
        "distributions": {
            "catalog_seed_starts": distribution(catalog),
            "conflict_block_finals": distribution(followup),
        },
        "record_count": len(combined),
        "all_have_exactly_two_conflicts": True,
        "all_pairs_same_color": all(record["same_color"] for record in combined),
        "all_intersection_size_four": all(
            record["intersection_size"] == 4 for record in combined
        ),
        "claim_boundary": (
            "This exhaustively audits 44 stored labeled near-misses only. It is "
            "not a theorem about every E=2 graph and is neither a construction "
            "nor a nonexistence result."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({**result, "corpora": "omitted"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
